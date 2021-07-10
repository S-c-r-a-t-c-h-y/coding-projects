import os
import time

def push_all(message):
    os.system('cd "C:\\Users\\amorm\\Desktop\\Coding Projects"')
    os.system('git pull')
    os.system('git add .')
    os.system(f'git commit -m {message}')
    os.system('git push')
    
delay = 3600    

try:
    while True:
        push_all('automatic commit')
        time.sleep(delay)
except KeyboardInterrupt:
    exit()