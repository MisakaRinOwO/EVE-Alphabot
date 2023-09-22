from PIL import ImageGrab,ImageOps
import os, time, win32api, win32con, pytesseract
from pathlib import Path
from win32api import GetSystemMetrics
from datetime import datetime
from pprint import pprint
from virtualkeyboard import*
from virtualmouse import*
import cv2 as cv

def screengrab(option):
    getscrrenres()
    box = (x_pad+1, y_pad+1,x_pad+2560 ,y_pad+1440)
    img = ImageGrab.grab(box)
    if option == 1:
        img.save(os.getcwd() +'\\full_snap' + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG')
    return img

def boxgrab(box,option,name):
    getscrrenres()
    img = ImageGrab.grab(box)
    if option == 1:
        img.save(os.getcwd() +'\\full_snap\\check boxes\\' + f"{'name'} {getdatetimestr()}.png", 'PNG')
    return img

def get_cords():
    x,y = win32api.GetCursorPos()
    x = x - x_pad
    y = y - y_pad
    return (x,y)

def getscrrenres():
    global x_pad, y_pad
    w = GetSystemMetrics(0)
    h = GetSystemMetrics(1)
    if w == 2560 and h == 1440:
        x_pad = 0
        y_pad = 0
    return x_pad,y_pad
def rgbchecker():
    getscrrenres()
    im = screengrab(0)
    cords = get_cords()
    print(f'Mouse coordinate: {cords}')
    print(f'RGB: {im.getpixel(cords)}')

def getdatetimestr():
    datetimelst = str(datetime.fromtimestamp(time.time())).split(':')
    datetimestr = datetimelst[0] + datetimelst[1] + datetimelst[-1].split('.')[0]
    return datetimestr

def mousepos(cord):
    win32api.SetCursorPos((x_pad + cord[0], y_pad + cord[1]))

def getdata(img):
    img_data = pytesseract.image_to_data(img).split('\n')
    org_data = []

    for i in img_data:
        org_data.append(i.split('\t'))

    text_coords = []
    for i in org_data[1::]:
        text_coord = []
        if i[-1].strip() != '' and len(i[-1])>3:
            text_coord.append((int(i[-6]),int(i[-5])))
            text_coord.append(i[-1])
            text_coords.append(text_coord)

    pprint(text_coords)#print image_to_string(Image.open(‘find.jpg’))
    return text_coords

def mousegrabscan():
    getscrrenres()
    state_left = win32api.GetKeyState(0x01)
    c = 0
    d = 0
    while c < 1 or d < 1:
        a = win32api.GetKeyState(0x01)
        if a != state_left:  # Button state changed
            state_left = a
            if a < 0:
                box1 = get_cords()
                c = 1
            else:
                box2 = get_cords()
                d = 1
        time.sleep(0.001)
    if box2[0] > box1[0] and box2[1] > box1[1]:
        box = (box1[0],box1[1],box2[0],box2[1])
    else:
        box = (box2[0],box2[1],box1[0],box1[1])
    img = boxgrab(box,0,'')
    getdata(img)
    print(box)

def mousegrab():
    getscrrenres()
    state_left = win32api.GetKeyState(0x01)
    c = 0
    d = 0
    while c < 1 or d < 1:
        a = win32api.GetKeyState(0x01)
        if a != state_left:  # Button state changed
            state_left = a
            if a < 0:
                box1 = get_cords()
                c = 1
            else:
                box2 = get_cords()
                d = 1
        time.sleep(0.001)
    if box2[0] > box1[0] and box2[1] > box1[1]:
        box = (box1[0],box1[1],box2[0],box2[1])
    else:
        box = (box2[0],box2[1],box1[0],box1[1])
    img = boxgrab(box,0,'')
    return [img,box]

def getboxes():
    neut()
    img = screengrab(0)
    img = img.load()
    lstx = []
    lst = []
    c = 0
    d = 0
    for x in range(1,2559):
        for y in range(1,1439):
            if img[x,y] == (141,141,141):
                lst.append((x,y))

    for i,j,k in zip(lst,lst[1:],lst[2:]):
        if (i[0]==j[0]==k[0] and abs(i[1]-k[1]) == 2) or (i[1]==j[1]==k[1] and abs(i[0]-k[0]) == 2):
            lstx.append(i)

    for i in lstx:
        if 1352 == i[1] or 1379 == i[1]:
            lstx.pop(lstx.index(i))
    for i in lstx:
        if 1352 == i[1] or 1379 == i[1]:
            lstx.pop(lstx.index(i))


    if len(lstx)%4 == 0:
        dic = {}
        boxes = []
        for i in lstx:
            for j in lstx:
                if i[1] == j[1] and i != j and j not in dic.keys():
                    dic[i] = j

        for i,j in zip(list(dic.keys())[::2],list(dic.values())[1::2]):
            boxes.append(i+j)

        return boxes
    else:
        return 0


def reposition():
    getscrrenres()

    mousepos((1185, 144))
    leftclick()
    time.sleep(0.5)
    roll(5000)

    time.sleep(0.5)
    mousepos((1185, 144))
    lefthold()
    mousepos((1185, 1200))
    time.sleep(0.5)
    leftrelease()

    time.sleep(0.5)
    mousepos((1185, 144))
    lefthold()
    mousepos((1300, 144))
    leftrelease()
    time.sleep(0.5)

def neut():
    getscrrenres()

    mousepos((1185, 144))
    time.sleep(0.3)
    leftclick()
    time.sleep(0.6)



pytesseract.pytesseract.tesseract_cmd = 'C:\\Python39\\tesseract-ocr\\tesseract.exe'