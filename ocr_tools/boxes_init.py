from PIL import Image, ImageEnhance, ImageFilter
import pytesseract, os, time
from uiltility import*
from pprint import pprint
from virtualkeyboard import*
from virtualmouse import*
from pathlib import Path




class Profile():
    def __init__(self, charname):
        self.filename = charname
        self.path = Path(os.getcwd())/'Profile'
        self.time = getdatetimestr()
        self.systems = 'ansila, jita'
        self.coords = {}

    def create_path(self):
        if os.path.exists(self.path):
            if os.path.exists(self.path/(self.filename)):
                self.path = self.path/(self.filename)
            else:
                os.mkdir(self.path/(self.filename))
                self.path = self.path/(self.filename)
        else:
            os.mkdir(self.path)
            os.mkdir(self.path/(self.filename))
            self.path = self.path/(self.filename)

        if os.path.exists(self.path/'Coordinates.txt'):
            self.coordpath = self.path/'Coordinates.txt'
        else:
            self.coordpath = self.path/'Coordinates.txt'
            f = open(self.coordpath, 'x')
            f.close()

    def read_coords(self):
        if os.path.exists(self.coordpath):
            f = open(self.coordpath,'r')
            if f.readlines() != []:
                f.seek(0)
                self.coords = eval(f.read())
                pprint.pprint(file)
            else:
                print('EMPTY')
            f.close()

    def save_coords(self,coord_dict):
        if os.path.exists(self.coordpath):
            f = open(self.coordpath,'r')
            if f.readlines() == []:
                f.close()
                f = open(self.coordpath,'w')
                f.write(str(coord_dict))
                f.close()
            else:
                f.close()
                f = open(self.coordpath,'w').close()
                self.save_coords(coord_dict)

    def set_box(self,boxname,img):
        if os.path.exists(self.path/boxname):
            os.remove(self.path/boxname)
            img.save(self.path/(boxname + '.png'),'PNG')
        else:
            img.save(self.path/(boxname + '.png'),'PNG')

    def create_box(self,boxes):
        for box in boxes[:-1]:
            img = boxgrab(box,0,0)
            data = getdata(img)

            for i in data:
                if 'nventor' in i[1].lower():
                    self.set_box('Inventory', img)
                    self.coords['inventory'] = box
                if 'ctiv' in i[1].lower():
                    self.set_box('Active Ship', img)
                    self.coords['active ship'] = box
                if 'orvett' in i[1].lower():
                    self.set_box('Undock', img)
                    self.coords['undock'] = box
                if 'vervie' in i[1].lower():
                    self.set_box('Overview', img)
                    self.coords['overview'] = box
                if 'electe' in i[1].lower():
                    self.set_box('Selected Item', img)
                    self.coords['selected item'] = box
                if 'rones' in i[1].lower():
                    self.set_box('Drones', img)
                    self.coords['drones'] = box
        c = 0
        ct = 0
        while c==0 and ct<5:
            sys_img = boxgrab(boxes[-1],0,0)
            sys_data = getdata(sys_img)
            
            for i in sys_data:
                if (i[1].lower() in self.systems):
                    self.set_box('System', sys_img)
                    self.coords['system'] = boxes[-1]
                    c += 1
            if c == 0:
                reposition()
                ct += 1



def main():
    system_box = (118,136,356,156)
    special_characters = "[!@#$%^&*()-+?_=,<>/]'"
    getscrrenres()

    p = Profile('Imaja Koraka')
    p.create_path()

    c = 0
    ct = 0
    while c == 0 and ct<10:
        boxes = getboxes()
        if boxes != 0:
            boxes.append(system_box)
            try:
                p.create_box(boxes)
                c += 1
            except:
                reposition()
                ct += 1
        else:
            reposition()
            ct += 1

    if ct >=5:
        print('Please Check windows setting')
    else:
        p.save_coords(p.coords)
main()
