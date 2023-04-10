import os
import zipfile
import sys

def zip_directory(path):
	with zipfile.ZipFile(f'{path}.zip', mode='w') as zipf:
		if os.path.isfile(path):
			zipf.write(path)
		else:
			len_dir_path = len(path)
			for root, _, files in os.walk(path):
				for file in files:
					file_path = os.path.join(root, file)
					zipf.write(file_path, file_path[len_dir_path:])
			   
if len(sys.argv) > 1:
	zip_directory(sys.argv[1])
else:
	print('No folder to zip.')