__author__ = 'fuckboy'

import win32api, win32con, win32gui, win32ui
import time
from Tkinter import *


key_pad = {
    '0': [900, 670],
    '1': [900, 600],
    '2': [950, 600],
    '3': [1025, 600],
    '4': [900, 550],
    '5': [950, 550],
    '6': [1025, 550],
    '7': [900, 475],
    '8': [950, 475],
    '9': [1025, 475],
}


def left_click(x, y, window):
    point = y << 15 | x
    win32api.SetCursorPos((x, y))
    window.SendMessage(win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, point)
    time.sleep(.05)
    window.SendMessage(win32con.WM_LBUTTONUP, 0, point)


def right_click(x, y, window):
    point = y << 15 | x
    window.SendMessage(win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, point)
    time.sleep(.05)
    window.SendMessage(win32con.WM_RBUTTONUP, 0, point)


def write_char(window, char):
    window.SendMessage(win32con.WM_CHAR, ord(char), 0)
    window.UpdateWindow()


def break_key(window, s, f):
    time.sleep(3)
    for i in range(s, f):
        # right click to open keypad
        time.sleep(.5)
        right_click(960, 540, window)
        time.sleep(.5)
        # get string version of code
        code = "%04i" % i
        print code
        for digit in code:
            time.sleep(.3)
            x, y = key_pad[digit]
            left_click(x, y, window)


def create_window(handle):
    PyCwnd = win32ui.CreateWindowFromHandle(handle)
    return PyCwnd


def callback(hwnd, hwnds):
    if win32gui.IsWindowVisible(hwnd):
        hwnds[win32gui.GetClassName(hwnd)] = hwnd
    return True


def get_window_handle():
    hwnds = {}
    win32gui.EnumWindows(callback, hwnds)
    print hwnds
    return hwnds['UnityWndClass']


def run_break(start, finish):
    handle = get_window_handle()
    window = create_window(handle)
    time.sleep(2)
    s = start.get()
    f = finish.get() + 1
    break_key(window, s, f)


def build_gui():
    # Main window
    root = Tk()
    root.title("RustBreaker")
    root.geometry("200x50")

    # Frames
    top_frame = Frame(root)
    top_frame.pack()
    bottom_frame = Frame(root)
    bottom_frame.pack(side=BOTTOM)

    # Field variables
    start = IntVar()
    finish = IntVar()

    # Starting value field
    code_start = Entry(top_frame, width=4, textvariable=start)
    code_start.pack(side=LEFT)
    code_start.focus_set()

    # Finish value field
    code_finish = Entry(top_frame, width=4, textvariable=finish)
    code_finish.pack(side=RIGHT)

    # Execute button
    break_button = Button(bottom_frame, text="Run Break", command=lambda: run_break(start, finish))
    break_button.pack()

    # Text label
    to = Label(top_frame, text="     to     ")
    to.pack()

    # Main loop
    root.mainloop()

build_gui()
