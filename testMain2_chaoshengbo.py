from serialControl import *
from distanceGpio import *
from colorDetect import *
from moveGpio import *
# from detection_demo import *
import os
#os.environ['CUDA_VISIBLE_DEVICES'] = '0'
#import cv2
import numpy as np
#import tensorflow as tf
#from yolov3.utils import detect_image, detect_realtime, detect_video, Load_Yolo_model, detect_video_realtime_mp
#from yolov3.configs import *

color_inf = {
'blue':{'lower':np.array([88, 78, 113]),
'upper':np.array([134, 255, 255]),'bgr':(255, 0, 0),'x':102},

'green':{'lower':np.array([31,34,0]),
'upper':np.array([119, 255, 255]),'bgr':(0, 255, 0),'x':147},

'red':{'lower':np.array([111, 60, 0]),
'upper':np.array([255, 240, 255]),'bgr':(0,0,255),'x':192},

'grey':{'lower':np.array([74, 1, 51]),
'upper':np.array([170, 255, 153]),'bgr':(128,128,128),'x':237},

'yellow':{'lower':np.array([0, 43, 102]),
'upper':np.array([50, 255, 255]),'bgr':(0,255,255)}
    }

lj_inf = {
        'bottle':{'state':0,'color':'blue',
        'x_crood':102, 'y_crood':587},

        'paper':{'state':0,'color':'blue',
        'x_crood':102, 'y_crood':587},

        'orange':{'state':0,'color':'green',
        'x_crood':147, 'y_crood':587},

        'battery':{'state':0,'color':'red',
        'x_crood':192, 'y_crood':587},

        'cup':{'state':0,'color':'grey',
        'x_crood':237, 'y_crood':587}
        }

storage_x = 170
storage_y = {1:90,2:161,3:250,4:331,5:412}

init_state()
#time.sleep(1)
#先把框框升起来
#putup()
#模型一直加载在内存中,升起来同时加载模型
#yolo = Load_Yolo_model()
#time.sleep(2)
# 目标垃圾
target_lj = 'lj'
# 开启移动控制
control_on()
##putdown() #框选放下
#putup()
#更新坐标
crood_update4(crood,0)
'''
#----------------第一个垃圾-----------------------
while 'done' != move_to(storage_x,storage_y[1],crood['x'],crood['y'],3):
    crood_update4(crood,0)
    print('第一个')
#stop(0.01)
while 'done' != move_to(storage_x,storage_y[1],crood['x'],crood['y'],3):
    crood_update4(crood,0)
# 套下去 
putdown()
time.sleep(10)
#前进一点,接收k210,知道垃圾类型,更新target_lj,不知道的去蓝色(bottle和纸团),蓝色的满了去随机挑选一个
forward(25)
#stop(1)

try:
    lj_210 = receive_serial() # 收到就关闭
except:
    lj_210 = 'bottle'
if lj_210 != None:
    target_lj = lj_210
else:
    target_lj = 'bottle'        
#如果有信息
#target = receive_serial()
#如果没有,几乎不可能
#targer = 'bottle'  #假如为bottle
print('目标垃圾:' + target_lj)    
# 已经确定好目标垃圾,左右移动
crood_update4(crood)

# 打开摄像头,开启颜色识别.废案

#目标垃圾的颜色
ljbin_color = lj_inf[target_lj]['color']
ljbin_x = color_inf[ljbin_color]['x']
print(ljbin_color,ljbin_x)
print('移到垃圾桶中间')
if ljbin_color == 'blue' or ljbin_color == 'green':
    turn_left(35)
    stop(0.1)
    while 'done' != move_to(135,storage_y[1]+30,crood['x'],crood['y']):
        crood_update4(crood,0)
    stop(0.1)
    while 'done' != move_to(135,storage_y[1]+28,crood['x'],crood['y']):
        crood_update4(crood,0)

    forward2(250)
    stop(0.05)
    while 'done' != move_to(135,storage_y[1]+28+250,crood['x'],crood['y']):
        crood_update4(crood)
    stop(0.05)

    forward2(80)
    while 'done' != move_to(135,470,crood['x'],crood['y']):
        crood_update4(crood) 
    stop(0.05)
else:
    turn_right(35)
    while 'done' != move_to(200,storage_y[1]+28,crood['x'],crood['y']):
        crood_update4(crood,0)
    stop(0.2)
    while 'done' != move_to(200,storage_y[1]+28,crood['x'],crood['y']):
        crood_update4(crood,0)

    forward2(250)
    stop(0.2)
    while 'done' != move_to(200,storage_y[1]+28+250,crood['x'],crood['y']):
        crood_update4(crood)
    stop(0.1)

    forward2(80)
    while 'done' != move_to(200,470,crood['x'],crood['y']):
        crood_update4(crood) 
    stop(0.1)

print('垃圾进入点')
while 'done' != move_to(ljbin_x,470,crood['x'],crood['y']):
    crood_update4(crood) 
    #print('垃圾进入点')
stop(0.1)
while 'done' != move_to(ljbin_x ,470,crood['x'],crood['y']):
    crood_update4(crood)

print('进入')

forward2(60)
print('进到垃圾筐里面,抬起来')
putup()
stop(0.2)
print('退出垃圾篓,进入黄色区域')
print('back 30')
back(30)

if ljbin_color == 'blue' or ljbin_color == 'green':
    print('垃圾进入点')
    while 'done' != move_to(ljbin_x,470,crood['x'],crood['y']):
        crood_update4(crood) 
        #print('垃圾进入点')
    stop(0.1)
    
    while 'done' != move_to(ljbin_x ,470,crood['x'],crood['y']):
        crood_update4(crood)
    print('返回垃圾进入点')
    while 'done' != move_to(135,470,crood['x'],crood['y']):
        crood_update4(crood) 
    stop(0.1)
    while 'done' != move_to(135 ,470,crood['x'],crood['y']):
        crood_update4(crood)
    print('下一个')

    back(100)
    while 'done' != move_to(135,390,crood['x'],crood['y']):
        crood_update4(crood,0) 
    stop(0.1)

    back(250)
    stop(0.05)
    while 'done' != move_to(135,storage_y[1]+50,crood['x'],crood['y']):
        crood_update4(crood,0)
    stop(0.1)

    turn_right(35)
    stop(0.05)
    while 'done' != move_to(storage_x,storage_y[1]+40,crood['x'],crood['y']):
        crood_update4(crood,0)
    stop(0.2)
    while 'done' != move_to(storage_x,storage_y[1]+40,crood['x'],crood['y']):
        crood_update4(crood,0)
else:
    print('垃圾进入点')
    while 'done' != move_to(ljbin_x,470,crood['x'],crood['y']):
        crood_update4(crood) 
        #print('垃圾进入点')
    stop(0.1)
    print('返回垃圾进入点')
    while 'done' != move_to(200,470,crood['x'],crood['y']):
        crood_update4(crood) 
    stop(0.1)
    while 'done' != move_to(200 ,470,crood['x'],crood['y']):
        crood_update4(crood)

    print('下一个')
    back(70)
    while 'done' != move_to(200,390,crood['x'],crood['y']):
        crood_update4(crood) 
    stop(0.1)

    back(200)
    stop(0.05)
    while 'done' != move_to(200,storage_y[1]+50,crood['x'],crood['y']):
        crood_update4(crood,0)
    stop(0.1)

    turn_left(35)
    stop(0.05)
    while 'done' != move_to(storage_x,storage_y[1] + 40,crood['x'],crood['y']):
        crood_update4(crood,0)
    stop(0.2)
    while 'done' != move_to(storage_x,storage_y[1] + 40,crood['x'],crood['y']):
        crood_update4(crood,0)

lj_inf[target_lj]['state'] = 1
'''
#----------------第二个垃圾-----------------------
while 'done' != move_to(storage_x,storage_y[2],crood['x'],crood['y'],3):
    crood_update4(crood,0)
    print('第二个')
#stop(0.01)
while 'done' != move_to(storage_x,storage_y[2],crood['x'],crood['y'],3):
    crood_update4(crood,0)
# 套下去 
putdown()
time.sleep(10)
#前进一点,接收k210,知道垃圾类型,更新target_lj,不知道的去蓝色(bottle和纸团),蓝色的满了去随机挑选一个
forward(25)
#stop(1)

try:
    lj_210 = receive_serial() # 收到就关闭
except:
    lj_210 = 'bottle'
if lj_210 != None:
    target_lj = lj_210
else:
    target_lj = 'bottle'        
#如果有信息
#target = receive_serial()
#如果没有,几乎不可能
#targer = 'bottle'  #假如为bottle
print('目标垃圾:' + target_lj)    
# 已经确定好目标垃圾,左右移动
crood_update4(crood)

# 打开摄像头,开启颜色识别.废案

#目标垃圾的颜色
ljbin_color = lj_inf[target_lj]['color']
ljbin_x = color_inf[ljbin_color]['x']
print(ljbin_color,ljbin_x)
print('移到垃圾桶中间')
if ljbin_color == 'blue' or ljbin_color == 'green':
    turn_left(35)
    stop(0.1)
    while 'done' != move_to(135,storage_y[2]+30,crood['x'],crood['y']):
        crood_update4(crood,0)
    stop(0.1)
    while 'done' != move_to(135,storage_y[2]+28,crood['x'],crood['y']):
        crood_update4(crood,0)

    forward2(250)
    stop(0.05)
    while 'done' != move_to(135,storage_y[2]+28+250,crood['x'],crood['y']):
        crood_update4(crood)
    stop(0.05)

    forward2(80)
    while 'done' != move_to(135,470,crood['x'],crood['y']):
        crood_update4(crood) 
    stop(0.05)
else:
    turn_right(35)
    while 'done' != move_to(200,storage_y[2]+28,crood['x'],crood['y']):
        crood_update4(crood,0)
    stop(0.2)
    while 'done' != move_to(200,storage_y[2]+28,crood['x'],crood['y']):
        crood_update4(crood,0)

    forward2(250)
    stop(0.2)
    while 'done' != move_to(200,storage_y[2]+28+250,crood['x'],crood['y']):
        crood_update4(crood)
    stop(0.1)

    forward2(80)
    while 'done' != move_to(200,470,crood['x'],crood['y']):
        crood_update4(crood) 
    stop(0.1)

print('垃圾进入点')
while 'done' != move_to(ljbin_x,470,crood['x'],crood['y']):
    crood_update4(crood) 
    #print('垃圾进入点')
stop(0.1)
while 'done' != move_to(ljbin_x ,470,crood['x'],crood['y']):
    crood_update4(crood)

print('进入')

forward2(60)
print('进到垃圾筐里面,抬起来')
putup()
stop(0.2)
print('退出垃圾篓,进入黄色区域')
print('back 30')
back(30)

if ljbin_color == 'blue' or ljbin_color == 'green':
    print('垃圾进入点')
    while 'done' != move_to(ljbin_x,470,crood['x'],crood['y']):
        crood_update4(crood) 
        #print('垃圾进入点')
    stop(0.1)
    
    while 'done' != move_to(ljbin_x ,470,crood['x'],crood['y']):
        crood_update4(crood)
        print('返回垃圾进入点')
    while 'done' != move_to(135,470,crood['x'],crood['y']):
        crood_update4(crood) 
    stop(0.1)
    while 'done' != move_to(135 ,470,crood['x'],crood['y']):
        crood_update4(crood)
    print('下一个')

    back(100)
    while 'done' != move_to(135,390,crood['x'],crood['y']):
        crood_update4(crood,0) 
    stop(0.1)

    back(250)
    stop(0.05)
    while 'done' != move_to(135,storage_y[2]+50,crood['x'],crood['y']):
        crood_update4(crood,0)
    stop(0.1)

    turn_right(35)
    stop(0.05)
    while 'done' != move_to(storage_x,storage_y[2]+40,crood['x'],crood['y']):
        crood_update4(crood,0)
    stop(0.2)
    while 'done' != move_to(storage_x,storage_y[2]+40,crood['x'],crood['y']):
        crood_update4(crood,0)
else:
    print('垃圾进入点')
    while 'done' != move_to(ljbin_x,470,crood['x'],crood['y']):
        crood_update4(crood) 
        #print('垃圾进入点')
    stop(0.1)
    print('返回垃圾进入点')
    while 'done' != move_to(200,470,crood['x'],crood['y']):
        crood_update4(crood) 
    stop(0.1)
    while 'done' != move_to(200 ,470,crood['x'],crood['y']):
        crood_update4(crood)

    print('下一个')
    back(70)
    while 'done' != move_to(200,390,crood['x'],crood['y']):
        crood_update4(crood) 
    stop(0.1)

    back(200)
    stop(0.05)
    while 'done' != move_to(200,storage_y[1]+50,crood['x'],crood['y']):
        crood_update4(crood,0)
    stop(0.1)

    turn_left(35)
    stop(0.05)
    while 'done' != move_to(storage_x,storage_y[2] + 40,crood['x'],crood['y']):
        crood_update4(crood,0)
    stop(0.2)
    while 'done' != move_to(storage_x,storage_y[2] + 40,crood['x'],crood['y']):
        crood_update4(crood,0)

lj_inf[target_lj]['state'] = 1

