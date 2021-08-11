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
crood_update4(crood)
'''
#----------------第一个垃圾-----------------------
#移到垃圾桶中间
if ljbin_color == 'blue' or ljbin_color == 'green':
    turn_left(35)
    while 'done' != move_to(135,storage_y[1]+28,crood['x'],crood['y']):
        crood_update4(crood,0)
    stop(0.2)
    while 'done' != move_to(135,storage_y[1]+28,crood['x'],crood['y']):
        crood_update4(crood,0)

    forward2(200)
    stop(0.2)
    while 'done' != move_to(135,storage_y[1]+28+250,crood['x'],crood['y']):
        crood_update4(crood)
    stop(0.1)

    forward2(80)
    while 'done' != move_to(135,470,crood['x'],crood['y']):
        crood_update4(crood) 
    stop(0.1)
else:
    turn_right(35)
    while 'done' != move_to(200,storage_y[1]+28,crood['x'],crood['y']):
        crood_update4(crood,0)
    stop(0.2)
    while 'done' != move_to(200,storage_y[1]+28,crood['x'],crood['y']):
        crood_update4(crood,0)

    forward2(200)
    stop(0.2)
    while 'done' != move_to(200,storage_y[1]+28+250,crood['x'],crood['y']):
        crood_update4(crood)
    stop(0.1)

    forward2(80)
    while 'done' != move_to(200,470,crood['x'],crood['y']):
        crood_update4(crood) 
    stop(0.1)

while 'done' != move_to(storage_x,storage_y[1],crood['x'],crood['y'],3):
    crood_update4(crood,0)
stop(0.02)
while 'done' != move_to(storage_x,storage_y[1],crood['x'],crood['y'],3):
    crood_update4(crood,0)
# 套下去 
putdown()
time.sleep(10)
#前进一点,接收k210,知道垃圾类型,更新target_lj,不知道的去蓝色(bottle和纸团),蓝色的满了去随机挑选一个
forward(25)
stop(1)
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
print(target_lj)    
# 已经确定好目标垃圾,左右移动
crood_update4(crood)

# 打开摄像头,开启颜色识别.废案

#目标垃圾的颜色
ljbin_color = lj_inf[target_lj]['color']
ljbin_x = color_inf[ljbin_color]['x']
# 到垃圾分拣点
while 'done' != move_to(color_inf['blue']['x'],storage_y[1]+28,crood['x'],crood['y']):
    crood_update4(crood,0)
stop(0.4)
while 'done' != move_to(color_inf['blue']['x'],storage_y[1]+28,crood['x'],crood['y']):
    crood_update4(crood,0)

while 'done' != move_to(color_inf['blue']['x'],200,crood['x'],crood['y']):
    crood_update4(crood,0)
stop(0.02)
while 'done' != move_to(color_inf['blue']['x'],300,crood['x'],crood['y']):
    crood_update4(crood,0)  
stop(0.02)
while 'done' != move_to(color_inf['blue']['x'],400,crood['x'],crood['y']):
    crood_update4(crood) 
stop(0.02)
while 'done' != move_to(color_inf['blue']['x'],400,crood['x'],crood['y']):
    crood_update4(crood) 
#进入黄色区域
while 'done' != move_to(color_inf['blue']['x'],485,crood['x'],crood['y']):
    crood_update4(crood) 
stop(0.15)

#选择进入颜色
while 'done' != move_to(color_inf['blue']['x']+(ljbin_x - color_inf['blue']['x'])/3,470,crood['x'],crood['y']):
    crood_update4(crood) 
stop(0.1)
while 'done' != move_to(color_inf['blue']['x']+(ljbin_x - color_inf['blue']['x'])/3,470,crood['x'],crood['y']):
    crood_update4(crood)
stop(0.1)
while 'done' != move_to(color_inf['blue']['x']+(ljbin_x - color_inf['blue']['x'])*2/3,470,crood['x'],crood['y']):
    crood_update4(crood) 
stop(0.1)
while 'done' != move_to(color_inf['blue']['x']+(ljbin_x - color_inf['blue']['x'])*2/3,470,crood['x'],crood['y']):
    crood_update4(crood)
stop(0.1)

#进入
while(crood['y'] < 520):
    forward()
    crood_update4(crood)
# 进到垃圾筐里面,抬起来
putup()
stop(0.2)
# 退出垃圾篓,进入黄色区域
back(40)
# 下一个点
while 'done' != move_to(color_inf['blue']['x'],470,crood['x'],crood['y']):
    crood_update4(crood)
while 'done' != move_to(color_inf['blue']['x'],400,crood['x'],crood['y']):
    crood_update4(crood)
stop(0.02)
while 'done' != move_to(color_inf['blue']['x'],300,crood['x'],crood['y']):
    crood_update4(crood,0)  
stop(0.02)
while 'done' != move_to(color_inf['blue']['x'],200,crood['x'],crood['y']):
    crood_update4(crood,0)
stop(0.02)
while 'done' != move_to(color_inf['blue']['x'],200,crood['x'],crood['y']):
    crood_update4(crood,0)
stop(0.02)
while 'done' != move_to(color_inf['blue']['x'],storage_y[1] + 40,crood['x'],crood['y']):
    crood_update4(crood,0)
stop(0.2)
while 'done' != move_to(storage_x,storage_y[1] + 50,crood['x'],crood['y'],3):
    crood_update4(crood,0)
stop(0.4)
while 'done' != move_to(storage_x,storage_y[1] + 50,crood['x'],crood['y']):
    crood_update4(crood,0)

lj_inf[target_lj]['state'] = 1

'''

#------------------------第二个垃圾--------------------------------
while 'done' != move_to(storage_x,storage_y[2],crood['x'],crood['y'],3):
    crood_update4(crood,0)
stop(0.02)
while 'done' != move_to(storage_x,storage_y[2],crood['x'],crood['y'],3):
    crood_update4(crood,0)
# 套下去 
putdown()
#stop(1)
time.sleep(10)
# 开启tf识别 10s
#detect_realtime(12,lj_inf, yolo, '', input_size=YOLO_INPUT_SIZE, show=False, rectangle_colors=(255, 0, 0))
# 10s自动关闭tf识别 如果有 更新target_lj

#前进一点,接收k210,知道垃圾类型,更新target_lj,不知道的去蓝色(bottle和纸团),蓝色的满了去随机挑选一个
forward(25)
stop(1)
try:
    lj_210 = receive_serial() # 收到就关闭
except:
    lj_210 = 'papper'
if lj_210 != None:
    target_lj = lj_210
else:
    target_lj = 'papper'      
    #如果有信息
    #target = receive_serial()
    #如果没有,几乎不可能
    #targer = 'bottle'  #假如为bottle
print(target_lj) 
# 已经确定好目标垃圾,左右移动
crood_update4(crood,0)

# 打开摄像头,开启颜色识别.废案

#目标垃圾的颜色
ljbin_color = lj_inf[target_lj]['color']
ljbin_x = color_inf[ljbin_color]['x']
# 到垃圾分拣点
while 'done' != move_to(color_inf['blue']['x'],storage_y[2]+28,crood['x'],crood['y']):
    crood_update4(crood,0)
stop(0.02)
while 'done' != move_to(color_inf['blue']['x'],storage_y[2]+28,crood['x'],crood['y']):
    crood_update4(crood,0)
stop(0.02)
while 'done' != move_to(color_inf['blue']['x'],300,crood['x'],crood['y']):
    crood_update4(crood,0)  
stop(0.02)
while 'done' != move_to(color_inf['blue']['x'],400,crood['x'],crood['y']):
    crood_update4(crood)
#进入黄色区域
while 'done' != move_to(color_inf['blue']['x'],485,crood['x'],crood['y']):
    crood_update4(crood)
stop(0.15)

#选择进入颜色
while 'done' != move_to(color_inf['blue']['x']+(ljbin_x - color_inf['blue']['x'])/3,470,crood['x'],crood['y']):
    crood_update4(crood) 
stop(0.2)
while 'done' != move_to(color_inf['blue']['x']+(ljbin_x - color_inf['blue']['x'])/3,470,crood['x'],crood['y']):
    crood_update4(crood)
stop(0.2)
while 'done' != move_to(color_inf['blue']['x']+(ljbin_x - color_inf['blue']['x'])*2/3,470,crood['x'],crood['y']):
    crood_update4(crood) 
stop(0.2)
while 'done' != move_to(color_inf['blue']['x']+(ljbin_x - color_inf['blue']['x'])*2/3,470,crood['x'],crood['y']):
    crood_update4(crood)
stop(0.2)

#进入
while(crood['y'] < 530):
    forward()
    crood_update4(crood)
# 进到垃圾筐里面,抬起来
putup()
stop(0.2)
# 退出垃圾篓,进入黄色区域

back(40)
 
stop(0.02)


while 'done' != move_to(color_inf['blue']['x']+(ljbin_x - color_inf['blue']['x'])/3,470,crood['x'],crood['y']):
    crood_update4(crood) 
stop(0.2)
while 'done' != move_to(color_inf['blue']['x']+(ljbin_x - color_inf['blue']['x'])/3,470,crood['x'],crood['y']):
    crood_update4(crood)
stop(0.2)
while 'done' != move_to(color_inf['blue']['x']+(ljbin_x - color_inf['blue']['x'])*2/3,470,crood['x'],crood['y']):
    crood_update4(crood) 
stop(0.2)
while 'done' != move_to(color_inf['blue']['x']+(ljbin_x - color_inf['blue']['x'])*2/3,470,crood['x'],crood['y']):
    crood_update4(crood)
stop(0.2)
# 下一个点
while 'done' != move_to(color_inf['blue']['x'],300,crood['x'],crood['y']):
    crood_update4(crood,0)
stop(0.02)
while 'done' != move_to(color_inf['blue']['x'],storage_y[2]+50,crood['x'],crood['y']):
    crood_update4(crood,0)
stop(0.02)


lj_inf[target_lj]['state'] = 1




#------------------------第三个垃圾--------------------------------
#左移 后退 右移, 到第三个垃圾前面  

while 'done' != move_to(storage_x,storage_y[3],crood['x'],crood['y'],3):
    crood_update4(crood,0)
stop(0.02)
while 'done' != move_to(storage_x,storage_y[3],crood['x'],crood['y'],3):
    crood_update4(crood,0)
# 套下去 
putdown()
time.sleep(10)
# 开启tf识别 10s
#detect_realtime(12,lj_inf, yolo, '', input_size=YOLO_INPUT_SIZE, show=False, rectangle_colors=(255, 0, 0))
# 10s自动关闭tf识别 如果有 更新target_lj

#前进一点,接收k210,知道垃圾类型,更新target_lj,不知道的去蓝色(bottle和纸团),蓝色的满了去随机挑选一个
forward(25)
stop(1)
try:
    lj_210 = receive_serial() # 收到就关闭
except:
    lj_210 = 'orange'
if lj_210 != None:
    target_lj = lj_210
else:
    target_lj = 'orange'      
    #如果有信息
    #target = receive_serial()
    #如果没有,几乎不可能
    #targer = 'bottle'  #假如为bottle
print(target_lj) 
# 已经确定好目标垃圾,左右移动
crood_update4(crood,0)

# 打开摄像头,开启颜色识别.废案

#目标垃圾的颜色
ljbin_color = lj_inf[target_lj]['color']
ljbin_x = color_inf[ljbin_color]['x']
# 到垃圾分拣点
while 'done' != move_to(color_inf['blue']['x'],storage_y[3]+28,crood['x'],crood['y']):
    crood_update4(crood,0)
stop(0.2)
while 'done' != move_to(color_inf['blue']['x'],storage_y[3]+28,crood['x'],crood['y']):
    crood_update4(crood,0)
stop(0.2)
while 'done' != move_to(color_inf['blue']['x'],400,crood['x'],crood['y']):
    crood_update4(crood) 
stop(0.02)
while 'done' != move_to(color_inf['blue']['x'],400,crood['x'],crood['y']):
    crood_update4(crood) 
#进入黄色区域
while 'done' != move_to(color_inf['blue']['x'],470,crood['x'],crood['y']):
    crood_update4(crood) 
stop(0.15)

#选择进入颜色
while 'done' != move_to(color_inf['blue']['x']+(ljbin_x - color_inf['blue']['x'])/3,470,crood['x'],crood['y']):
    crood_update4(crood) 
stop(0.2)
while 'done' != move_to(color_inf['blue']['x']+(ljbin_x - color_inf['blue']['x'])/3,470,crood['x'],crood['y']):
    crood_update4(crood)
stop(0.2)
while 'done' != move_to(color_inf['blue']['x']+(ljbin_x - color_inf['blue']['x'])*2/3,470,crood['x'],crood['y']):
    crood_update4(crood) 
stop(0.2)
while 'done' != move_to(color_inf['blue']['x']+(ljbin_x - color_inf['blue']['x'])*2/3,470,crood['x'],crood['y']):
    crood_update4(crood)
stop(0.2)
#进入
while(crood['y'] < 530):
    forward()
    crood_update4(crood)
# 进到垃圾筐里面,抬起来
putup()
stop(0.2)
# 退出垃圾篓,进入黄色区域

back(40)

stop(0.02)




# 回到垃圾选择点
while 'done' != move_to(color_inf['blue']['x']+(ljbin_x - color_inf['blue']['x'])/3,470,crood['x'],crood['y']):
    crood_update4(crood) 
stop(0.2)
while 'done' != move_to(color_inf['blue']['x']+(ljbin_x - color_inf['blue']['x'])/3,470,crood['x'],crood['y']):
    crood_update4(crood)
stop(0.2)
while 'done' != move_to(color_inf['blue']['x']+(ljbin_x - color_inf['blue']['x'])*2/3,470,crood['x'],crood['y']):
    crood_update4(crood) 
stop(0.2)
while 'done' != move_to(color_inf['blue']['x']+(ljbin_x - color_inf['blue']['x'])*2/3,470,crood['x'],crood['y']):
    crood_update4(crood)
stop(0.2)
# 下一个点
while 'done' != move_to(color_inf['blue']['x'],300,crood['x'],crood['y']):
    crood_update4(crood,0)
stop(0.02)
while 'done' != move_to(color_inf['blue']['x'],storage_y[2] + 50,crood['x'],crood['y']):
    crood_update4(crood,0)
stop(0.02)

lj_inf[target_lj]['state'] = 1

'''
#------------------------第四个垃圾--------------------------------
#左移 后退 右移, 到第四个垃圾前面  

while 'done' != move_to(storage_x,storage_y[4],crood['x'],0):
    crood_update4(crood)
stop(0.2)
while 'done' != move_to(storage_x,storage_y[4],crood['x'],0):
    crood_update4(crood)

while 'done' != move_to(storage_x,storage_y[4],crood['x'],crood['y'],3):
    crood_update4(crood)
stop(0.2)
while 'done' != move_to(storage_x,storage_y[4],crood['x'],crood['y'],3):
    crood_update4(crood)
#套下去 
#putdown()
#开启tf识别 10s
detect_realtime(5,lj_inf, yolo, '', input_size=YOLO_INPUT_SIZE, show=False, rectangle_colors=(255, 0, 0))

#10s自动关闭tf识别 如果有 更新target_lj
if lj_inf['bottle']['state'] == 1 :
    target_lj = 'bottle'
elif lj_inf['cup']['state'] == 1 :
    target_lj = 'cup'
else:
    #前进一点,接收k210,知道垃圾类型,更新target_lj,不知道的去蓝色(bottle和纸团),蓝色的满了去随机挑选一个
    forward(10)
    #stop(2)
    lj_210 = receive_serial() #设置接收5s,自动关闭
    if lj_210 != None:
        target_lj = lj_210
    else:
        target_lj = 'bottle'      
    #如果有信息
    #target = receive_serial()
    #如果没有,几乎不可能
    #targer = 'bottle'  #假如为bottle
print(target_lj)
# 已经确定好目标垃圾,左右移动
crood_update4(crood)

#目标垃圾的颜色和坐标
ljbin_color = lj_inf[target_lj]['color']
ljbin_x = color_inf[ljbin_color]['x']

if ljbin_color == 'blue' or ljbin_color == 'green':
    while 'done' != move_to(130,storage_y[4],crood['x'],0):
        crood_update4(crood)
    stop(0.1)
    while 'done' != move_to(130,storage_y[4],crood['x'],0):
        crood_update4(crood)

    while 'done' != move_to(130,430,crood['x'],crood['y']):
        crood_update4(crood)   

    while 'done' != move_to(color_inf[ljbin_color]['x'],430,crood['x'],crood['y']):
        crood_update4(crood)      
    stop(0.2)
    while 'done' != move_to(color_inf[ljbin_color]['x'],430,crood['x'],crood['y']):
        crood_update4(crood)   

else :
    while 'done' != move_to(200,storage_y[4],crood['x'],0):
        crood_update4(crood)
    stop(0.1)
    while 'done' != move_to(200,storage_y[4],crood['x'],0):
        crood_update4(crood) 

    while 'done' != move_to(200,430,crood['x'],crood['y']):
        crood_update4(crood)

    while 'done' != move_to(color_inf[ljbin_color]['x'],430,crood['x'],crood['y']):
        crood_update4(crood)      
    stop(0.2)
    while 'done' != move_to(color_inf[ljbin_color]['x'],430,crood['x'],crood['y']):
        crood_update4(crood) 

stop(0.1)
forward(80)
putup()
time.sleep(0.1)
back(85)

while back_wave_distance() > storage_y[4] + 40:
    back()
stop(0.1)
lj_inf[target_lj]['state'] = 1


#------------------------第五个垃圾--------------------------------
#左移 后退 右移, 到第五个垃圾前面  

while 'done' != move_to(storage_x,storage_y[5],crood['x'],0):
    crood_update4(crood)
stop(0.2)
while 'done' != move_to(storage_x,storage_y[5],crood['x'],0):
    crood_update4(crood)

while 'done' != move_to(storage_x,storage_y[5],crood['x'],crood['y'],3):
    crood_update4(crood)
stop(0.2)
while 'done' != move_to(storage_x,storage_y[5],crood['x'],crood['y'],3):
    crood_update4(crood)
#套下去 
#putdown()
#开启tf识别 10s
detect_realtime(5,lj_inf, yolo, '', input_size=YOLO_INPUT_SIZE, show=False, rectangle_colors=(255, 0, 0))

#10s自动关闭tf识别 如果有 更新target_lj
if lj_inf['bottle']['state'] == 1 :
    target_lj = 'bottle'
elif lj_inf['cup']['state'] == 1 :
    target_lj = 'cup'
else:
    #前进一点,接收k210,知道垃圾类型,更新target_lj,不知道的去蓝色(bottle和纸团),蓝色的满了去随机挑选一个
    forward(10)
    #stop(2)
    lj_210 = receive_serial() #设置接收5s,自动关闭
    if lj_210 != None:
        target_lj = lj_210
    else:
        target_lj = 'bottle'      
    #如果有信息
    #target = receive_serial()
    #如果没有,几乎不可能
    #targer = 'bottle'  #假如为bottle
print(target_lj)
# 已经确定好目标垃圾,左右移动
crood_update4(crood)

#目标垃圾的颜色和坐标
ljbin_color = lj_inf[target_lj]['color']
ljbin_x = color_inf[ljbin_color]['x']

if ljbin_color == 'blue' or ljbin_color == 'green':
    while 'done' != move_to(130,storage_y[5],crood['x'],0):
        crood_update4(crood)
    stop(0.1)
    while 'done' != move_to(130,storage_y[5],crood['x'],0):
        crood_update4(crood)

    while 'done' != move_to(130,430,crood['x'],crood['y']):
        crood_update4(crood)   

    while 'done' != move_to(color_inf[ljbin_color]['x'],430,crood['x'],crood['y']):
        crood_update4(crood)      
    stop(0.2)
    while 'done' != move_to(color_inf[ljbin_color]['x'],430,crood['x'],crood['y']):
        crood_update4(crood)   

else :
    while 'done' != move_to(200,storage_y[5],crood['x'],0):
        crood_update4(crood)
    stop(0.1)
    while 'done' != move_to(200,storage_y[5],crood['x'],0):
        crood_update4(crood) 

    while 'done' != move_to(200,430,crood['x'],crood['y']):
        crood_update4(crood)

    while 'done' != move_to(color_inf[ljbin_color]['x'],430,crood['x'],crood['y']):
        crood_update4(crood)      
    stop(0.2)
    while 'done' != move_to(color_inf[ljbin_color]['x'],430,crood['x'],crood['y']):
        crood_update4(crood) 

stop(0.1)
forward(80)
putup()
time.sleep(0.1)
back(85)






#套下去 
##putdown()
#开启tf识别 10s
detect_realtime(10,lj_inf, yolo, '', input_size=YOLO_INPUT_SIZE, show=False, rectangle_colors=(255, 0, 0))
#10s自动关闭tf识别 如果有 更新target_lj
if lj_inf['bottle']['state'] == 1 :
    target_lj = 'bottle'
elif lj_inf['cup']['state'] == 1 :
    target_lj = 'cup'
else:
    #前进一点,接收k210,知道垃圾类型,更新target_lj,不知道的去蓝色(bottle和纸团),蓝色的满了去随机挑选一个
    forward(10)
    lj_210 = receive_serial() #设置接收5s,自动关闭
    if lj_210 != None:
        target_lj = lj_210
    else:
        target_lj = 'bottle'      
    #如果有信息
    #target = receive_serial()
    #如果没有,几乎不可能
    #targer = 'bottle'  #假如为bottle
print(target_lj)    
#左移 前进到颜色识别点
crood_update4(crood)
while 'done' != move_to(130,145,crood['x'],crood['y']):
    crood_update4(crood)
stop(0.2)
while 'done' != move_to(130,145,crood['x'],crood['y']):
    crood_update4(crood)

while 'done' != move_to(130,520,crood['x'],crood['y']):
    crood_update4(crood)
while 'done' != move_to(150,520,crood['x'],crood['y']):
    crood_update4(crood)
    
# 打开摄像头,开启颜色识别
camera = cv2.VideoCapture(0)
#找到目标垃圾的颜色
ljbin_color = lj_inf[target_lj]['color']
while True:
    ljbin_xy = color_detect(camera, ljbin_color)
    if None != ljbin_xy:
        if 'done' != camera_move_to(ljbin_xy['x']):
            print('seek for bin')
        else:
            stop()
            break
# 摄像头释放
camera.release()

#移动到颜色前,向前走
while forward_wave_distance() > 60:
    forward(5)
putup()
time.sleep(1)
back(50)
lj_inf[target_lj]['state'] = 1



# 摄像头释放
camera.release()
#移动到颜色前面后向前走,
while forward_wave_distance > 60:
    forward(5)
putup()
back(30)

#----------------第三个垃圾-----------------------
while 'done' != move_to(130,520,crood['x'],crood['y']):
    crood_update4(crood)
stop(0.2)
while 'done' != move_to(130,520,crood['x'],crood['y']):
    crood_update4(crood)

while 'done' != move_to(130,275,crood['x'],crood['y']):
    crood_update4(crood)
stop(0.2)
while 'done' != move_to(130,275,crood['x'],crood['y']):
    crood_update4(crood)

while 'done' != move_to(170,305,crood['x'],crood['y']):
    crood_update4(crood)
    
#套下去 
#putdown()
#开启tf识别 10s
detect_realtime(10,lj_inf, yolo, '', input_size=YOLO_INPUT_SIZE, show=False, rectangle_colors=(255, 0, 0))
#10s自动关闭tf识别 如果有 更新target_lj
if lj_inf['bottle']['state'] == 1 :
    target_lj = 'bottle'
elif lj_inf['cup']['state'] == 1 :
    target_lj = 'cup'
else:
    #前进一点,接收k210,知道垃圾类型,更新target_lj,不知道的去蓝色(bottle和纸团),蓝色的满了去随机挑选一个
    forward(10)
    lj_210 = receive_serial() #设置接收5s,自动关闭
    if lj_210 != None:
        target_lj = lj_210
    else:
        target_lj = 'bottle'      
    #如果有信息
    #target = receive_serial()
    #如果没有,几乎不可能
    #targer = 'bottle'  #假如为bottle
print(target_lj)    
#左移 前进到颜色识别点
crood_update4(crood)
while 'done' != move_to(130,145,crood['x'],crood['y']):
    crood_update4(crood)
stop(0.2)
while 'done' != move_to(130,145,crood['x'],crood['y']):
    crood_update4(crood)
while 'done' != move_to(130,520,crood['x'],crood['y']):
    crood_update4(crood)
while 'done' != move_to(150,520,crood['x'],crood['y']):
    crood_update4(crood)
    
# 打开摄像头,开启颜色识别
camera = cv2.VideoCapture(0)
#找到目标垃圾的颜色
ljbin_color = lj_inf[target_lj]['color']
while True:
    ljbin_xy = color_detect(camera, ljbin_color)
    if None != ljbin_xy:
        if 'done' != camera_move_to(ljbin_xy['x']):
            print('seek for bin')
        else:
            stop()
            break
# 摄像头释放 
camera.release()

#移动到颜色前,向前走
while forward_wave_distance() > 60:
    forward(5)
putup()
time.sleep(1)
back(50)
lj_inf[target_lj]['state'] = 1
'''
# mybuffer = 16
# pts = deque(maxlen=mybuffer)
# counter = 0
# # 打开摄像头
# camera = cv2.VideoCapture(0)



control_off()
GPIO.cleanup()

# 摄像头释放
#camera.release()
# 销毁所有窗口
cv2.destroyAllWindows()
print('end')

