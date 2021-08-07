import os

for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
	for root, dirs, files in os.walk((path := f'{letter}:/')):
		for name in files:
			if name.endswith((".py")):
				print(name)