#from collections import deque
print('--------')
from types import CodeType
print('--------')
import numpy as np
print('--------')
import time
print('--------')
import struct
print('--------')
import cv2
print('--------')
import colorDetect 
print('--------')
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
import tensorflow as tf
from yolov3.utils import detect_image, detect_realtime, detect_video, Load_Yolo_model, detect_video_realtime_mp
from yolov3.configs import *

# 初始化追踪点的列表
mybuffer = 16
pts = deque(maxlen=mybuffer)
counter = 0
# 打开摄像头
camera = cv2.VideoCapture(0)


yolo = Load_Yolo_model()
camera = cv2.VideoCapture(0)
(ret, frame) = camera.read()
# 判断是否成功打开摄像头
if not ret:
    print('No Camera')

while True:
    print('1')
    tf_inf = detect_realtime(camera,yolo, '', input_size=YOLO_INPUT_SIZE, show=False, rectangle_colors=(255, 0, 0))
    if 'bottle'== tf_inf['label']:
        bottle_x = tf_inf['x']
        bottle_y = tf_inf['y']
    elif 'cup' == tf_inf['label']:
        cup_x = tf_inf['x']
        cup_y = tf_inf['y']
    print(bottle_x,bottle_y)

while True:
    print('2')
    rec_inf = colorDetect.find_storage()
    k = cv2.waitKey(1) & 0xFF
    if rec_inf != None:
        print(rec_inf) 
    if k == 27:
        break

 # 摄像头释放
camera.release()
# 销毁所有窗口
cv2.destroyAllWindows()

