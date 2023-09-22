from PIL import ImageGrab,ImageOps
import os, time, win32api, win32con
from pathlib import Path
from win32api import GetSystemMetrics
from datetime import datetime
'''
 
All coordinates assume a screen resolution of 2560*1440, and 
eve clients are in the default window
Play area =  x_pad+1, y_pad+1, 1927, 1065
'''
def getscrrenres():
    global x_pad,y_pad
    w = GetSystemMetrics(0)
    h = GetSystemMetrics(1)
    if w == 2560 and h == 1440:
        x_pad = 647
        y_pad = 341


def screengrab():
    box = (x_pad+1, y_pad+1,x_pad+1280,y_pad+724)
    img = ImageGrab.grab(box)
    ##img.save(os.getcwd() +'\\full_snap' + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG')
    return img

def leftclick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.2)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    print("Left Click.")

def roll(x):
    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL,0,0,x)

def mousepos(cord):
    win32api.SetCursorPos((x_pad + cord[0], y_pad + cord[1]))

def get_cords():
    x,y = win32api.GetCursorPos()
    x = x - x_pad
    y = y - y_pad
    print(x,y)

def pagetop():
    page = (391,386)
    mousepos(page)
    time.sleep(.3)
    roll(120000)
    time.sleep(.3)

def startgame():
    #location of character selection
    mousepos((359, 324))
    time.sleep(.5)
    leftclick()
    time.sleep(15)

    #location of making character sheet active
    mousepos((373, 56))
    time.sleep(.5)
    leftclick()

def click_gunnery():
    gunnery = (302,170)
    mousepos(gunnery)
    time.sleep(.5)
    leftclick()
    time.sleep(1)
    pagetop()
    time.sleep(.5)

def click_missiles():
    missiles = (312,197)
    mousepos(missiles)
    time.sleep(.5)
    leftclick()
    time.sleep(1)
    pagetop()
    time.sleep(.5)

def nextpage(step):
    #roll skills to the next page
    page = (391,386)
    mousepos(page)
    time.sleep(.3)
    roll(step)
    time.sleep(.3)

def drag_to_add():
    add = (400,700)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.2)
    mousepos(add)
    time.sleep(.2)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(.2)

def closeclient():
    close = (1252,18)
    mousepos(close)
    time.sleep(1)
    leftclick()
    time.sleep(1)

def checkpath():
    global skill
    global times
    global f
    coor_path = Path(os.getcwd())/'coor.txt'
    skills_path = Path(os.getcwd())/'skills.txt'

    if os.path.exists(coor_path):
        f = open(coor_path).read()
        f = eval(f.replace(' ','').replace('\n',' '))
        print('skills and coordinations loaded.')
        coor_res = True
        open(coor_path).close()
    else:
        print('skills and coordinations fail to load.')
        coor_res = False

    if os.path.exists(skills_path):
        g = open(skills_path).readlines()
        skill, times = [], []
        for i in g:
            i = i.strip('\n')
            skill.append(i[0:-1].strip(' '))
            times.append(i[-1])
        print('skill plan loaded.')
        skill_res = True
        open(skills_path).close()
    else:
        print('skill plan fail to load.')
        skill_res = False

    res = coor_res and skill_res
    return res

def skilltype_pos(str1):
    s = str(str1).replace(' ','')
    for i in range(4):
        if  s in f['Gunnery']['page'][i]['skill'].keys():
            pg = i
            pos = f['Gunnery']['page'][i]['skill'][s]
            stype = 'Gunnery'
            coord = pos_coords(pos)
            return [pg,pos,stype,coord]
    for i in range(2):
        if s in f['Missiles']['page'][i]['skill'].keys():
            pg = i
            pos = f['Missiles']['page'][i]['skill'][s]
            stype = 'Missiles'
            coord = pos_coords(pos)
            return [pg,pos,stype,coord]

def pos_coords(pos):
    return f['coords'][int(pos)]

def farm(n):
    page_g = [0,-1100,-1200,-1200,-1100]
    page_m = [0,-650]
    neutral = (370,297)
    exit = (1256,18)
    getscrrenres()
    if checkpath() is True:
        for i in range(n):
            startgame()
            for s in skill:
                loc = skilltype_pos(s)
                if loc[-2] == 'Gunnery':
                    click_gunnery()
                    for x in page_g[0:loc[0]+1]:
                        nextpage(x)
                    mousepos(neutral)
                    time.sleep(1)
                    mousepos(loc[-1])
                    time.sleep(1)
                    drag_to_add()
                    print('Skill added')

                elif loc[-2] == 'Missiles':
                    click_missiles()
                    for x in page_m[0:loc[0]+1]:
                        nextpage(x)
                    mousepos(neutral)
                    time.sleep(1)
                    mousepos(loc[-1])
                    time.sleep(1)
                    drag_to_add()
                    print('Skill added')
            mousepos(exit)
            time.sleep(2)
            leftclick()
            print(f'Client {i+1} finished.')
            time.sleep(1)

            




