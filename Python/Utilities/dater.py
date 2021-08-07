import sys
import time
from datetime import datetime
import os
import pathlib
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

creation = 'C:\\Date de création'
today = "C:\\Date d'aujourd'hui"
last_modification = "C:\\Date de dernière modification"

class MyHandler(FileSystemEventHandler):

    last_deleted_file = None
    previous_file_path = None
    
    tracked_folders = [creation, today, last_modification]

    def on_created(self, event):
        file_name = event.src_path.split('\\')[-1]
        folder = '\\'.join(event.src_path.split('\\')[:-1])
        
        if file_name == self.last_deleted_file and folder in self.tracked_folders:
            
            date = ''
            if folder == today:
                date = datetime.today().strftime('%d-%m-%Y')
            elif folder == creation:
                date = datetime.fromtimestamp(pathlib.Path(event.src_path).stat().st_ctime).date().strftime('%d-%m-%Y')
            elif folder == last_modification:
                date = datetime.fromtimestamp(pathlib.Path(event.src_path).stat().st_mtime).date().strftime('%d-%m-%Y')
         
            os.rename(event.src_path, f"{self.previous_file_path}\\{date} - {file_name}")
            self.last_deleted_file = None
            self.previous_file_path = None
            
    def on_deleted(self, event):
        self.last_deleted_file = event.src_path.split('\\')[-1]
        self.previous_file_path = '\\'.join(event.src_path.split('\\')[:-1])

if __name__ == "__main__":
    
    path = 'C:\\'
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