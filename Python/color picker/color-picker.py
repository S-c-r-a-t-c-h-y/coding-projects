from tkinter import *
import tkinter.messagebox
import pyautogui

import win32gui , win32con , ctypes, time

# ------------------------------------------------------------------------------------------------------------------

def change_cursor(cursor_image):
    """Change the cursor and return old cursor."""
    hold = win32gui.LoadImage(0, 32512, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_SHARED )
    hsave = ctypes.windll.user32.CopyImage(hold, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_COPYFROMRESOURCE)
    
    if type(cursor_image) is int:
        ctypes.windll.user32.SetSystemCursor(cursor_image, 32512)
        
    elif type(cursor_image) is str:
        
        hnew = win32gui.LoadImage(0, cursor_image, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_LOADFROMFILE)

        ctypes.windll.user32.SetSystemCursor(hnew, 32512)

    return hsave

# ------------------------------------------------------------------------------------------------------------------

def get_pixel_colour(i_x, i_y):
    i_desktop_window_id = win32gui.GetDesktopWindow()
    i_desktop_window_dc = win32gui.GetWindowDC(i_desktop_window_id)
    long_colour = win32gui.GetPixel(i_desktop_window_dc, i_x, i_y)
    i_colour = int(long_colour)
    return i_colour

# ------------------------------------------------------------------------------------------------------------------

def get_pixel_color():

    global current_color

    x, y = pyautogui.position()

    color = get_pixel_colour(x, y)
    hex_val = f'{color:X}'
    hex_val = hex_val[4:] + hex_val[2:4] + hex_val[:2]
    rgb_val = f'{(color & 0xff), ((color >> 8) & 0xff), ((color >> 16) & 0xff)}'

    current_color.set(f'#{hex_val} - {rgb_val}')

    top.after(60, get_pixel_color)

# ------------------------------------------------------------------------------------------------------------------

def main():

    # initialisation de la fenêtre
    global top, current_color, window
    top = Tk()
    top.title("Color picker")
    top.geometry('600x600')
    top.configure(bg='#333333')
    top.resizable(width=False, height=True)
    #top.configure(cursor='tcross')

    current_color = StringVar()
    current_color.set('')
    current_color_label = Label(top, textvariable=current_color, font='30',
                                bg='#333333', fg='white', height=1)
    current_color_label.pack()

    get_pixel_color()

    top.mainloop()

# ------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    old = change_cursor('crosshair2.cur')
    main()
    change_cursor(old)
