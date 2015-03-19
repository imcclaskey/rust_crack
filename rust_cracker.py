__author__ = 'fuckboy'

import win32api, win32con, win32gui, win32ui
import time

key_pad = {
    '0': [900,  670],
    '1': [900,  600],
    '2': [950,  600],
    '3': [1025, 600],
    '4': [900,  550],
    '5': [950,  550],
    '6': [1025, 550],
    '7': [900,  475],
    '8': [950,  475],
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


def break_key(window):
    time.sleep(3)
    for i in range(0, 1000):
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


def run():
    handle = get_window_handle()
    window = create_window(handle)
    time.sleep(2)
    break_key(window)
