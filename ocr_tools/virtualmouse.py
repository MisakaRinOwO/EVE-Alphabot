from win32api import GetSystemMetrics
import os, time, win32api, win32con

def leftclick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.2)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def rightclick():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
    time.sleep(.2)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)

def lefthold():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)

def righthold():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)

def leftrelease():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def rightrelease():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)

#roll up: positive x
#roll down: negative x
def roll(x):
    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL,0,0,x)