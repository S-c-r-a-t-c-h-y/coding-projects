import tkinter as tk
from tkinter.constants import BOTH, FLAT
import tkinter.font as tkFont
import os

COMMANDS = {'cmd': 'start cmd',
            'chrome': 'start chrome',
            'browser': 'start chrome',
            'music': 'start spotify',
            'spotify': 'start spotify',
            'discord': 'start discord',
            'code': r'code "C:\Users\Personne\Desktop\Coding Projects"'}

if __name__ == '__main__':
    top = tk.Tk()
    WIDTH = top.winfo_screenwidth()
    HEIGHT = 30
    X = -8
    Y = -32
    top.geometry(f'{WIDTH}x{HEIGHT}+{X}+{Y}')
    top.configure(bg='black')
    top.resizable(width=True, height=True)
    
    entry = tk.Entry(top, bg='black', fg='white', font=tkFont.Font(size=15), relief=FLAT, bd=0)
    entry.pack(fill=BOTH)
    entry.focus()
    
    def print_entry(event):
        if (command := COMMANDS.get(entry.get(),'')):
            os.system(command)
        top.destroy()
    
    top.bind('<Return>', print_entry)
    top.mainloop()