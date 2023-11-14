from uiltility import*
import os
from PIL import ImageGrab,ImageOps
from ocrbatch2_0 import*


# w = GetSystemMetrics(0)
# h = GetSystemMetrics(1)
# if w == 2560 and h == 1440:
#     x_pad = 0
#     y_pad = 0

# box = (x_pad+1, y_pad+1,x_pad+2560 ,y_pad+1440)
# img = ImageGrab.grab(box)
# temp_path = os.getcwd() +'\\full_snap\\evaluate_temp.png'
# img.save(temp_path, 'PNG')


# tmpl_path_lst = list(Path(os.getcwd()+'\\full_snap\\check boxes').iterdir())

# for i in range(len(tmpl_path_lst)):
#     tmpl_path_lst[0] = str(tmpl_path_lst[0])

# ev = ocr(temp_path,tmpl_path_lst)

grabEvaluate()