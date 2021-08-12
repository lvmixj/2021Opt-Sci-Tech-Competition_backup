# encoding:utf-8
from collections import deque
from types import CodeType
import numpy as np
import time
# import serial
import struct
# import imutils
import cv2

# 串口初始化
# ser = serial.Serial("/dev/ttyAMA0",115200)
# print("uart open:",ser.isOpen())
# 协议数组
#arr = [0xaa, 0xaf, 0x03, 0x00, 0x00, 0x01, 0x5d]

color_inf = {'blue':{'lower':np.array([68, 180, 126]),
'upper':np.array([124, 255, 255]),'bgr':(255, 0, 0)},
'red':{'lower':np.array([0, 123, 100]),
'upper':np.array([7, 255, 255]),'bgr':(0,0,255)},
'grey':{'lower':np.array([0, 0, 46]),
'upper':np.array([180, 30, 146]),'bgr':(128,128,128)},
'green':{'lower':np.array([51,143,200]),
'upper':np.array([67, 255, 255]),'bgr':(0, 255, 0)},
'black':{'lower':np.array([0, 0, 0]),
'upper':np.array([180, 255, 54]),'bgr':(255, 255, 255)},
'yellow':{'lower':np.array([25, 43, 146]),
'upper':np.array([34, 255, 255]),'bgr':(0,255,255)}}

# 通过串口发送数据
# SendData(ser,arr)
# 蓝色 红色 灰色 绿色
# 黑色 黄色
blue_bgr = (255, 0, 0)
# 颜色阈值下界(HSV) lower boudnary
blue_lower = (68, 180, 126)
# 颜色阈值上界(HSV) upper boundary
blue_upper = (124, 255, 255)
# red
red_bgr = (0, 0, 255)
red_lower = (0, 123, 100)
red_upper = (10, 255, 255)
# grey
grey_bgr = (128, 128, 128)
grey_lower = (0, 0, 46)
grey_upper = (180, 30, 146)
# green
green_bgr = (0, 255, 0)
green_lower = (51, 143, 200)
green_upper = (67, 255, 255)
# black
black_bgr = (255, 255, 255)
black_lower = (0, 0, 0)
black_upper = (180, 255, 54)
# yellow
yellow_bgr = (0, 255, 255)
yellow_lower = (26, 170, 146)
yellow_upper = (34, 255, 255)

# 乒乓球橙色
originLower = np.array([26, 43, 43])
originUpper = np.array([34, 255, 255])


# 初始化追踪点的列表
mybuffer = 16
pts = deque(maxlen=mybuffer)
counter = 0
# 打开摄像头
camera = cv2.VideoCapture(0)
# 等待1秒
time.sleep(1)

def find_storage():
    color = 'red'
    # 遍历每一帧
    # 初始化追踪点的列表
    mybuffer = 16
    pts = deque(maxlen=mybuffer)
    #counter = 0
    #while True:
    # 读取帧
    #global camera
    (ret, frame) = camera.read()
    # 判断是否成功打开摄像头
    if not ret:
        print('No Camera')
    #    break
    # e1 = cv2.getTickCount()
    # frame = imutils.resize(frame, width=600)
    # 转到HSV空间
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # 根据阈值构建掩膜
    mask = cv2.inRange(hsv, color_inf[color]['lower'], color_inf[color]['upper'])
    # 腐蚀操作
    mask = cv2.erode(mask, None, iterations=2)
    # 膨胀操作，其实先腐蚀再膨胀的效果是开运算，去除噪点
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    # 初始化圆形轮廓质心
    center = None
    
    if len(cnts)  > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        if radius < 5:
            cv2.circle(frame, (int(x), int(y)), int(radius), color_inf[color]['bgr'], 2)
            cv2.circle(frame, center, 3, color_inf[color]['bgr'], -1)
            pts.appendleft(center)
            #print(color, int(x), int(y))
            #cv2.imshow('Frame', frame)
            #print(int(radius))
            return {'x': int(x), 'y':int(y)}
    else:
        pts.clear()
    #cv2.imshow('Frame', frame)


def color_detect(color):
    # 遍历每一帧
    # 初始化追踪点的列表
    mybuffer = 16
    pts = deque(maxlen=mybuffer)
    #counter = 0
    #while True:
    # 读取帧
    #global camera
    (ret, frame) = camera.read()
    # 判断是否成功打开摄像头
    if not ret:
        print('No Camera')
    #    break
    # e1 = cv2.getTickCount()
    # frame = imutils.resize(frame, width=600)
    # 转到HSV空间
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # 根据阈值构建掩膜
    mask = cv2.inRange(hsv, color_inf[color]['lower'], color_inf[color]['upper'])
    # 腐蚀操作
    mask = cv2.erode(mask, None, iterations=2)
    # 膨胀操作，其实先腐蚀再膨胀的效果是开运算，去除噪点
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    # 初始化圆形轮廓质心
    center = None
    
    if len(cnts)  > 1:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        if radius > 30:
            cv2.circle(frame, (int(x), int(y)), int(radius), color_inf[color]['bgr'], 2)
            cv2.circle(frame, center, 3, color_inf[color]['bgr'], -1)
            pts.appendleft(center)
            #print(color, int(x), int(y))
            #cv2.imshow('Frame', frame)
            #print(int(radius))
            return {color:{'x': int(x), 'y':int(y)}}
    else:
        pts.clear()
    #cv2.imshow('Frame', frame)
        
def every_color():
    while True:
        #time.sleep(0.2)
        color_detect('red')
        color_detect('grey')
        color_detect('blue')
        color_detect('green')
        color_detect('yellow')
        color_detect('black')
        print(color_detect('red'),color_detect('grey'),color_detect('blue'),
                        color_detect('green'),color_detect('yellow'),color_detect('black'))
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

#every_color()
if __name__ == '__main__':
    while 1:
        time.sleep(0.1)
        print(color_detect('red'))
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
    camera.release()
    # 销毁所有窗口
    cv2.destroyAllWindows()
           
