from PIL import ImageGrab,ImageOps
import os, time, win32api, win32con
from pathlib import Path
from win32api import GetSystemMetrics


#all coords are subjected to change when automation implies.
coor_dict = {'in_station' : {'undock_btn' : (1,2,3,4)} , 
'in_space' : {'HUD' : (1064,1205,1665,1389), 'drones' : (1840,222,2111,396), 'locked' : (1988,40,2102,196), 'system' : (116,135,363,157), 
'overview' : (2115,160,2543,1398), 'selected_item' : (2115,40,2542,157), 'msg_box': (1130,226,1429,286)}}

#full screen senario
def getscrrenres():
    global x_pad, y_pad
    w = GetSystemMetrics(0)
    h = GetSystemMetrics(1)
    if w == 2560 and h == 1440:
        x_pad = 0
        y_pad = 0

def screengrab():
    box = (x_pad+1, y_pad+1,x_pad+2560 ,y_pad+1440)
    img = ImageGrab.grab(box)
    ##img.save(os.getcwd() +'\\full_snap' + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG')
    return img

def mousePos(cord):
    win32api.SetCursorPos((x_pad + cord[0], y_pad + cord[1]))
     
def get_cords():
    x,y = win32api.GetCursorPos()
    x = x - x_pad
    y = y - y_pad
    print(x,y)
    return (x,y)

def rgbchecker():
    im = screengrab()
    cords = get_cords()
    print(im.getpixel(cords))

