# importing libraries
import speech_recognition as sr
import os
import shutil
from pydub import AudioSegment
from pydub.silence import split_on_silence, detect_nonsilent
import datetime

# create a speech recognition object
r = sr.Recognizer()


def get_timestamps(sound):

    nonsilent_data = detect_nonsilent(
        sound, min_silence_len=500, silence_thresh=sound.dBFS - 14, seek_step=1
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


def make_subtitle(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """

    filename, extension = "".join(path.split(".")[:-1]), str(
        path.split(".")[-1]
    )
    subtitle_filename = f"{filename}.srt"
    if (
        os.path.exists(subtitle_filename)
        and os.stat(subtitle_filename).st_size
    ):
        os.remove(subtitle_filename)

    # open the audio file using pydub
    sound = AudioSegment.from_file(path, extension)
    print(type(sound))
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(
        sound,
        # experiment with this value for your target audio file
        min_silence_len=500,
        # adjust this per requirement
        silence_thresh=sound.dBFS - 14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""

    timestamps = get_timestamps(sound)

    # process each chunk
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", e)
            else:
                text = f"{text.capitalize()}. "
                start, finish = timestamps[i - 1][0], timestamps[i - 1][1]
                with open(subtitle_filename, "a") as f:
                    f.write(f"{i}\n{start} --> {finish}\n{text}\n\n")
                print(chunk_filename, ":", text)
                whole_text += text
    # return the text for all chunks detected
    shutil.rmtree(folder_name)
    return whole_text


# path = "7601-291468-0006.wav"
path = "harvard.wav"
# print("\nFull text:", make_subtitle(path))
print(make_subtitle(path))
