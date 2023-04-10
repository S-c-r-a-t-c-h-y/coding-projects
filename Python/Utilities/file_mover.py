from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

import os, time

folder_to_track = "D:\\Sorted"
folder_destination = "D:\\Sorted"

types = {
		'Images': ('.bmp', '.dds', '.dif', '.heic', '.jpg', '.jpeg', '.png', '.PNG', '.psd', '.pspimage', '.tga', '.thm', '.tif', '.tiff', '.yuv'),
		'Executables': ('.apk', '.app', '.bat', '.cgi', '.com', '.exe', '.gadget', '.jar', '.wsf'),
		'Audio': ('.flp', '.aif', '.iff', '.m3u', '.m4a', '.mid', '.mp3', '.mpa', '.wav', '.wma'),
		'Video': ('.3g2', '.3gp', '.asf', '.avi', '.flv', '.m4v', '.mov', '.mp4', '.mpg', '.rm', '.srt', '.swf', '.vob', '.wmv'),
		'Text': ('.doc', '.docx', '.log', '.msg', '.odt', '.pages', '.rtf', '.tex', '.txt', '.text', '.wpd', '.wps'),
		'Compressed': ('.7z', '.cbr', '.deb', '.gz', '.pkg', '.rar', '.rpm', '.sitx', '.tar.gz', '.zip', '.zipx'),
		'Spreadsheet': ('.xlsx', '.ods', '.numbers', '.xlr', '.xls'),
		'Data': ('.csv', '.dat', '.ged', '.key', '.keychain', '.ppt', '.pptx', '.sdf', '.tar', '.vcf', '.xml'),
		'Database': ('.accdb', '.db', '.dbf', '.mdb', '.pdb', '.sql'),
		'Font': ('.fnt', '.fon', '.otf', '.ttf'),
		'System': ('.cab', '.cpl', '.cur', '.deskthemepack', '.dll', '.dmp', '.drv', '.icns', '.ico', '.lnk', '.sys'),
		'Code': ('.c', '.java', '.py', '.class', '.cpp', '.cs', '.h', '.lua', '.m', '.p', '.pl', '.py', '.sh', '.sln', '.swift', '.vb', '.vcxproj', '.xcodeproj', '.js', '.html', '.css', '.php'),
		'PDF': ('.pdf', '.pct', '.indd'),
		'3D Images': ('.3dm', '.3ds', '.max', '.obj'),
		'Vector Images': ('.ai', '.eps', '.svg'),
		'Misc': ('.ics', '.msi', '.part', '.torrent'),
		'Plugin': ('.crx', '.plugin'),
		'Settings': ('.cfg', '.ini', '.prf'),
		'Encoded': ('.hqx', '.mim', '.uue'),
		'Disk Images': ('.bin', '.cue', '.dmg', '.iso', '.mdf', '.toast', '.vcd'),
		'Backup': ('.bak', '.tmp')
	}

def on_modified(event):
	process()

def process():
	for filename in os.listdir(folder_to_track):
		src = f'{folder_to_track}\\{filename}'

		if os.path.isfile(src):

			extension = os.path.splitext(filename)[1]
			sub_dir = 'Other'
			for type, extensions in types.items():
				if extension in extensions:
					sub_dir = type

			if not os.path.exists(f'{folder_destination}\\{sub_dir}'):
				os.mkdir(f'{folder_destination}\\{sub_dir}')

			new_destination = f'{folder_destination}\\{sub_dir}\\{filename}'
			try:
				os.rename(src, new_destination)
			except:
				print(f'Failed to move file {filename}.')
				continue


if __name__ == '__main__':
	print('Auto file handling system started')

	patterns = ["*"]
	ignore_patterns = None
	ignore_directories = False
	case_sensitive = True
	my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

	my_event_handler.on_modified = on_modified
	# my_event_handler.on_created = on_created
	# my_event_handler.on_deleted = on_deleted
	# my_event_handler.on_moved = on_moved

	path = folder_to_track
	go_recursively = True
	my_observer = Observer()
	my_observer.schedule(my_event_handler, path, recursive=go_recursively)

	my_observer.start()
	try:
		while True:
			time.sleep(5)
	except KeyboardInterrupt:
		print('Auto file handling system stopped')
		my_observer.stop()
		my_observer.join()
