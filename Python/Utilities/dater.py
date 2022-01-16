import sys
import time
from datetime import datetime, timedelta
import os
import pathlib
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

creation = "C:\\Date de création"
today = "C:\\Date d'aujourd'hui"
last_modification = "C:\\Date de dernière modification"


class MyHandler(FileSystemEventHandler):

    deleted_files = []
    tracked_folders = [creation, today, last_modification]

    def on_created(self, event):
        file_name = event.src_path.split("\\")[-1]
        folder = "\\".join(event.src_path.split("\\")[:-1])

        if file_name in (only_file_names := [couple[0] for couple in self.deleted_files]):
            couple = self.deleted_files[only_file_names.index(file_name)]
            if folder in self.tracked_folders:
                date = ""
                if folder == today:
                    date = datetime.today().strftime("%d-%m-%Y")
                elif folder == creation:
                    creation_date = datetime.fromtimestamp(pathlib.Path(event.src_path).stat().st_ctime).date()
                    modification_date = datetime.fromtimestamp(pathlib.Path(event.src_path).stat().st_mtime).date()
                    date = (
                        creation_date.strftime("%d-%m-%Y")
                        if (creation_date - modification_date) < timedelta()
                        else modification_date.strftime("%d-%m-%Y")
                    )
                elif folder == last_modification:
                    date = (
                        datetime.fromtimestamp(pathlib.Path(event.src_path).stat().st_mtime).date().strftime("%d-%m-%Y")
                    )
                os.rename(event.src_path, f"{couple[1]}\\{date} - {file_name}")

            self.deleted_files.remove(couple)

    def on_deleted(self, event):
        self.deleted_files.append((event.src_path.split("\\")[-1], "\\".join(event.src_path.split("\\")[:-1])))


if __name__ == "__main__":

    path = "C:\\"
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
