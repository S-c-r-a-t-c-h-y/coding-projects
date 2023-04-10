from time import perf_counter
from typing import Callable, Dict, Optional, Tuple
import os
import datetime
import enum
import speech_recognition as sr
from googletrans import Translator, LANGUAGES
from pydub import AudioSegment
from pydub.silence import split_on_silence, detect_nonsilent
from multiprocessing import Pool


TEMP_DIR_NAME = "temp"


@enum.unique
class Engine(enum.Enum):
    google = enum.auto()
    google_cloud = enum.auto()


class Subtitler:
    def __init__(
        self,
        *,
        engine: Engine = Engine.google,
        source_language: str = "en-US",
        target_language: str = "en",
        min_silence_len: int = 500,
    ):
        self.recognizer = sr.Recognizer()
        self.recognize_function = self._select_recognize_function(engine)
        self.engine = engine

        self.translator = Translator()
        self.msl = min_silence_len

        self.src_language = source_language
        self.tgt_language = target_language

        if target_language not in LANGUAGES:
            raise ValueError("Invalid language to translate the subtitles.")

        if type(engine) != Engine:
            raise TypeError(
                "'engine' parameter must be an element of the 'Engine' enum."
            )

    def _get_timestamps(self, sound_data: AudioSegment):
        """Returns the timestamps of the nonsilent moments in a sound."""

        nonsilent_data = detect_nonsilent(
            sound_data,
            min_silence_len=self.msl,
            silence_thresh=sound_data.dBFS - 14,
            seek_step=1,
        )

        return [
            [
                datetime.datetime.strptime(f"{chunk / 1000}", "%S.%f").strftime(
                    "%H:%M:%S,%f"
                )[:-3]
                for chunk in chunks
            ]
            for chunks in nonsilent_data
        ]

    def _match_target_amplitude(self, sound: AudioSegment, target_dBFS: float):
        change_in_dBFS = target_dBFS - sound.dBFS
        return sound.apply_gain(change_in_dBFS)

    def _clear_old_files(self, *args) -> None:
        for filename in args:
            if os.path.exists(filename) and os.stat(filename).st_size:
                os.remove(filename)

    def _select_recognize_function(self, engine: Engine) -> Callable:
        recognizers: Dict[Engine, Callable] = {
            Engine.google: self.recognizer.recognize_google,
            Engine.google_cloud: self.recognizer.recognize_google_cloud,
        }
        # selects the recognizer based on the desired engine
        return recognizers[engine]

    def _append_to_srt(
        self,
        srt_filename: str,
        text: str,
        lign_nb: int,
        start: str,
        finish: str,
    ) -> None:
        with open(srt_filename, "a", encoding="utf-8") as f:
            f.write(f"{lign_nb}\n{start} --> {finish}\n{text}\n\n")

    def _create_temp_dir(self):
        if not os.path.isdir(TEMP_DIR_NAME):
            os.mkdir(TEMP_DIR_NAME)

    def _convert_mp4_to_wav(self, mp4_filename: str) -> Tuple[str, str]:
        self._clear_old_files(f"{mp4_filename}.wav")
        os.system(f'ffmpeg -i "{mp4_filename}.mp4" "{mp4_filename}.wav"')
        return f"{mp4_filename}.wav", "wav"

    def _convert_mp4_to_mp3(self, mp4_filename: str) -> Tuple[str, str]:
        self._clear_old_files(f"{mp4_filename}.mp3")
        os.system(f'ffmpeg -i "{mp4_filename}.mp4" "{mp4_filename}.mp3"')
        return f"{mp4_filename}.mp3", "mp3"

    def _split_audio(self, filename: str, output_folder: str = "output"):
        os.system(f"spleeter separate {filename} -o {output_folder}")
        return output_folder

    def _process_audio_chunk(self, audio_chunk, i: int) -> Optional[Tuple[str, int]]:
        chunk_filename = os.path.join(TEMP_DIR_NAME, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = self.recognizer.record(source)
            # try converting it to text
            try:
                text = self.recognize_function(
                    audio_listened, language=self.src_language
                )
                return text, i
            except sr.UnknownValueError as e:
                print("Error:", e)
                return None

    def create_subtitles(self, path: str, *, translate: bool = False):
        """
        Splitting the large audio file into chunks
        and apply speech recognition on each of these chunks
        """

        t_start = perf_counter()

        if not os.path.exists(path):
            raise FileNotFoundError(f'file "{path}" not found')

        filename, extension = os.path.splitext(path)
        extension = extension[1:]

        if extension == "mp4":
            path, extension = self._convert_mp4_to_mp3(filename)

        if extension != "mp3":
            os.system(f"ffmpeg -i {path} -acodec libmp3lame {filename}.mp3")
            extension = "mp3"
            path = f"{filename}.mp3"

        # self._split_audio(path)

        print(path, extension)

        subtitle_filename_src = f"{filename}-{self.engine.name}-{self.src_language}.srt"
        subtitle_filename_dest = (
            f"{filename}-{self.engine.name}-{self.tgt_language}.srt"
        )
        self._clear_old_files(subtitle_filename_src, subtitle_filename_dest)

        # open the audio file using pydub
        audio_segment = AudioSegment.from_file(path, format=extension)

        # splits the audio between every silence
        chunks = split_on_silence(
            audio_segment,
            min_silence_len=self.msl,
            silence_thresh=audio_segment.dBFS - 14,
            keep_silence=500,
        )

        # create a directory to store the audio chunks
        self._create_temp_dir()

        # retrieves the nonsilence timestamps from the audio clip
        timestamps = self._get_timestamps(audio_segment)
        with Pool() as pool:
            print("getting results")
            results = pool.starmap(
                self._process_audio_chunk, enumerate(chunks, start=1)
            )

            print("got results back")
            for result in results:
                if result is None:
                    continue

                text, i = result

                # formats the text
                src_text = f"{text.capitalize()}. "

                # retrieves the timestamps corresponding to the start
                # and finish of the sequence
                start, finish = timestamps[i - 1][0], timestamps[i - 1][1]

                # appends the text with the timestamps to the .srt file
                self._append_to_srt(subtitle_filename_src, src_text, i, start, finish)

                if self.src_language != self.tgt_language and translate:
                    translated_text = self.translator.translate(
                        src_text, dest=self.tgt_language
                    ).text
                    self._append_to_srt(
                        subtitle_filename_dest,
                        translated_text,
                        i,
                        start,
                        finish,
                    )

        # delete the temporary directory
        os.rmdir(TEMP_DIR_NAME)

        t_end = perf_counter()
        duration = t_end - t_start
        print(f"took {duration:.2f}s")


if __name__ == "__main__":
    s = Subtitler()
    # s.make_subtitle("invalid.vbs")
    s.create_subtitles("test.mp4")
    # s.make_subtitle("harvard.wav", target_language="fr")
    # s.make_subtitle("7601-291468-0006.wav", target_language="ja")
