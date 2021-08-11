#先不加tf
from serialControl import *
from distanceGpio import *
from colorDetect import *
from moveGpio import *
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
import cv2
import numpy as np
import tensorflow as tf
from yolov3.utils import detect_image, detect_realtime, detect_video, Load_Yolo_model, detect_video_realtime_mp
from yolov3.configs import *


#back(400)
color_inf = {
'blue':{'lower':np.array([79, 184, 113]),
'upper':np.array([110, 255, 255]),'bgr':(255, 0, 0)},
'red':{'lower':np.array([147, 100, 142]),
'upper':np.array([225, 235, 255]),'bgr':(0,0,255)},
'grey':{'lower':np.array([92, 42, 62]),
'upper':np.array([141, 94, 129]),'bgr':(128,128,128)},
'green':{'lower':np.array([31,68,74]),
'upper':np.array([67, 134, 166]),'bgr':(0, 255, 0)},
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


# 打开摄像头
#camera = cv2.VideoCapture(0)
#putup()
#模型一直加载在内存中
#yolo = Load_Yolo_model()
#detect_realtime(tf_inf, yolo, '', input_size=YOLO_INPUT_SIZE, show=False, rectangle_colors=(255, 0, 0))
target_lj = 'lj'
#starttime = time.time()
control_on()
putdown() #框选放下 第一个是识别时间
#detect_realtime(5,lj_inf, yolo, '', input_size=YOLO_INPUT_SIZE, show=False, rectangle_colors=(255, 0, 0))
        
#print(lj_inf)
while 'done' != move_to(170,145,crood['x'],crood['y'],5):
    crood_update(crood)
    
#套下去 
putdown()
#开启tf识别 10s
detect_realtime(10,lj_inf, yolo, '', input_size=YOLO_INPUT_SIZE, show=False, rectangle_colors=(255, 0, 0))
#10s自动关闭tf识别 如果有 更新target_lj
if lj_inf['bottle']['state'] == 1 :
    target_lj = 'bottle'
elif lj_inf['cup']['state'] == 1 :
    target_lj = 'cup'
else:
    target_lj = ['bottle']
    #前进一点,接收k210,知道垃圾类型,更新target_lj,不知道的去蓝色(bottle和纸团),蓝色的满了去随机挑选一个
    #forward(10)
    #lj_210 = receive_serial() #设置接收5s,自动关闭
    #if lj_210 != None:
        #target_lj = lj_210
    #else:
        #target_lj = 'bottle'      
    #如果有信息
    #target = receive_serial()
    #如果没有,几乎不可能
    #targer = 'bottle'  #假如为bottle
print(target_lj)    
#左移 前进到颜色识别点
crood_update(crood)
while 'done' != move_to(130,145,crood['x'],crood['y']):
    crood_update(crood)
stop(0.2)
while 'done' != move_to(130,145,crood['x'],crood['y']):
    crood_update(crood)
    
while 'done' != move_to(130,290,crood['x'],crood['y']):
    crood_update(crood)
while 'done' != move_to(150,290,crood['x'],crood['y']):
    crood_update(crood)
    


#移动到颜色前,向前走

putup()
time.sleep(1)
back(50)
lj_inf[target_lj]['state'] = 1


control_off()
GPIO.cleanup()

# 摄像头释放
#camera.release()
# 销毁所有窗口
cv2.destroyAllWindows()
print('end')

