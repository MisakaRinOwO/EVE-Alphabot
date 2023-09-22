from PIL import ImageGrab,ImageOps
import os, time, win32api, win32con, pytesseract
from win32api import GetSystemMetrics
from datetime import datetime
from pprint import pprint
from virtualkeyboard import*
from virtualmouse import*
from uiltility import*
import cv2 as cv
import numpy as np

class ImagePathError(Exception):
    pass


class ocr():
    def __init__(self,background_img_path = None,template_img_paths = None,method = None):
        self.bg_img_path = background_img_path
        self.tpl_img_paths_lst = template_img_paths
        self.method = method
        self.results_lst = []


    def proccess_img(self): #load templates into list of images, load background image
        self.tpl_imgs_lst = []
        if os.path.exists(Path(self.bg_img_path)):
            self.bg_img = cv.imread(self.bg_img_path, cv.IMREAD_COLOR)
            for i in self.tpl_img_paths_lst:
                if os.path.exists(Path(i)):
                    tpl_img = cv.imread(str(i), cv.IMREAD_COLOR)
                    self.tpl_imgs_lst.append(tpl_img)
                else:
                    raise ImagePathError('Wrong or missing image path.')
        else:
            raise ImagePathError('Wrong or missing image path.')

    def comparison(self): #compare templates with background image, and creates a list of results
        self.proccess_img()
        if self.method != None:
            for i in self.tpl_imgs_lst:
                self.results_lst.append(cv.matchTemplate(self.bg_img, i, self.method))

        else:
            for i in self.tpl_imgs_lst:
                self.results_lst.append(cv.matchTemplate(self.bg_img, i, cv.TM_CCOEFF_NORMED))

    def showPositions(self): #show background image(with or without template boxes)
        cv.imshow('result',self.bg_img)
        cv.waitKey()

    def getPosition(self): #creates list of individual positions, creates list of individual names that matches index with the position list
        self.comparison()
        self.maxvals_lst = []
        self.ind_positions_lst = []
        self.ind_position_name_lst = []

        if len(self.results_lst) != 0:
            for i,j,k in zip(self.results_lst,self.tpl_imgs_lst,self.tpl_img_paths_lst):
                ind_positions = []
                ind_position_name = []
                minval, maxval, minloc, maxloc = cv.minMaxLoc(i)
                self.maxvals_lst.append(maxval)
                tpl_width = j.shape[1]
                tpl_height = j.shape[0]
                bottom_right = (maxloc[0]+tpl_width , maxloc[1]+tpl_height)

                tpl_name = k.split('\\')[-1].split('.')[0]
                if tpl_name == 'HUD' or tpl_name == 'inventory_sign':
                    loc = np.where(i >= 0.8)
                elif tpl_name == 'system_sign':
                    loc = np.where(i >= 0.85)
                else:
                    loc = np.where(i >= 0.95)
                ind_topleft = [i for i in zip(*loc[::-1])]
                for topleft in ind_topleft:
                    ind_bottomright = (topleft[0] + tpl_width, topleft[1] + tpl_height)
                    ind_center = (topleft[0] + round(tpl_width/2), topleft[1]+ round(tpl_height/2))
                    ind_positions.append(ind_center)
                    ind_position_name.append(tpl_name)

                    cv.rectangle(self.bg_img, topleft, ind_bottomright, color = (0,255,0))
                self.ind_positions_lst.append(ind_positions)
                self.ind_position_name_lst.append(ind_position_name)
    
    def showCounts(self):   #print counts of templates detected in the background image and its highest confidence
        for i,j,k in zip(self.tpl_img_paths_lst,self.maxvals_lst,self.ind_position_name_lst):
            print(i.split('\\')[-1].split('.')[0])
            print(f'MaxConfidence: {j}')
            print(f'Count: {len(k)}\n')

    def checkPositions(self):   #print the templates' name and position, and move cursor to their positions (press ENTER to continue)
        for i,j in zip(self.ind_positions_lst,self.ind_position_name_lst):
            for k,l in zip(i,j):
                mousepos(k)
                print(k)
                print(l)
                a = input()

def quickEvaluate(filename):    #compare templates in folder with filename.png using ocr class
    global ev

    tmpl_path_lst = list(Path(os.getcwd()+'\\full_snap\\check boxes').iterdir())
    for i in range(len(tmpl_path_lst)):
        tmpl_path_lst[i] = str(tmpl_path_lst[i])

    bg_path = os.getcwd() +f'\\full_snap\\{filename}.png'
    ev = ocr(bg_path,tmpl_path_lst)
    ev.getPosition()

def grabEvaluate(): #grab current screen as background image, and compare templates in folder with it using ocr class
    global ev
    x_pad,y_pad = getscrrenres()
    box = (x_pad+1, y_pad+1,x_pad+2560 ,y_pad+1440)
    img = ImageGrab.grab(box)
    
    if os.path.exists(os.getcwd() +'\\full_snap\\temp.png'):
        os.remove(os.getcwd() +'\\full_snap\\temp.png')

    img.save(os.getcwd() +'\\full_snap\\temp.png', 'PNG')
    quickEvaluate('temp')
