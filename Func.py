#############################################
# moveGpio
import RPi.GPIO as GPIO
import time
import serialControl
import distanceGpio

#31 33 35 37 36 38
#2  3  4  5  6  7

Forward_pin = 31;                   #前进引脚
Back_pin = 33;                      #后引脚

Turn_Right_pin = 35;                #右平移引脚
Turn_Left_pin = 37;                 #左平移引脚

Clockwise_Rotation_Pin = 36;        #顺时针旋转引脚
Counter_Clockwise_Rotation_pin = 38;#逆时针旋转引脚

#小车的线速度和角速度
y_line_speed = 19 # cm/s
x_line_speed = 17 # cm/s
w_speed = 43    # °/s
move_state = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(Forward_pin,GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(Back_pin,GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(Turn_Right_pin,GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(Turn_Left_pin,GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(Clockwise_Rotation_Pin,GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(Counter_Clockwise_Rotation_pin,GPIO.OUT,initial = GPIO.LOW)

def set_gpio_state(state_forward_pin = 0,state_back_pin = 0,state_right_pin = 0,state_left_pin = 0,state_clock_pin = 0,state_counter_pin = 0):
    GPIO.output(Forward_pin,state_forward_pin)
    GPIO.output(Back_pin,state_back_pin)
    GPIO.output(Turn_Right_pin,state_right_pin)
    GPIO.output(Turn_Left_pin,state_left_pin)
    GPIO.output(Clockwise_Rotation_Pin,state_clock_pin)
    GPIO.output(Counter_Clockwise_Rotation_pin,state_counter_pin)

def stop(t = 0):
    set_gpio_state(0,0,0,0,0,0)
    time.sleep(0.1)
    if t != 0:
        time.sleep(t)

def control_on():
    set_gpio_state(1,0,1,0,1,0)
    time.sleep(0.1)

def control_off():
    global move_state
    move_state = 0
    stop()
    time.sleep(0.1)
    set_gpio_state(0,1,0,1,0,1)

# 函数变量为距离,单位cm
def forward(s = 0):
    global move_state
    move_state = 1
    set_gpio_state(1,0,0,0,0,0)
    if s != 0:
        time.sleep(s/y_line_speed)
        stop()

def back(s = 0):
    global move_state
    move_state = 2
    set_gpio_state(0,1,0,0,0,0)
    if s != 0:
        time.sleep(s/y_line_speed)
        stop()

def turn_left(s = 0):
    global move_state
    move_state = 4
    set_gpio_state(0,0,0,1,0,0)
    if s != 0:
        time.sleep(s/x_line_speed)
        stop()

def turn_right(s = 0):
    global move_state
    move_state = 3
    set_gpio_state(0,0,1,0,0,0)
    if s != 0:
        time.sleep(s/x_line_speed)
        stop()

def clock(w = 0):
    set_gpio_state(0,0,0,0,1,0)
    if w != 0:
        time.sleep(w/w_speed)
        stop()

def counter(w = 0):
    set_gpio_state(0,0,0,0,0,1)
    if w != 0:
        time.sleep(w/w_speed)
        stop()

    #摄像头的
def move_to(x_current = 259, y_current = 342, x_destination = 259, y_destination = 342,commit_error=15):
    
    #目标-目前
    commit_error = 15
    x_distance = x_destination - x_current
    y_distance = y_destination - y_current

    if(x_distance<-commit_error):
        #sent_move_data(-x_distance,0,0)    
        turn_left()
    elif(x_distance>commit_error):
        #sent_move_data(x_distance,0,0)    
        turn_right()
    else:
        if(y_distance>commit_error):
            #sent_move_data(0,y_distance,0)   
            forward()
        elif(y_distance<-commit_error):
            #sent_move_data(0,-y_distance,0)   
            back() 
        else:
            stop()
            return 'done'
        #这下面的应该给调用函数去搞    
            

            #sent_move_data(0,0,0)
            #sent Serial
            #close wutishibie
            #open color shibie
    #time.sleep(0.5)
#这个坐标用框框的中心点来表示


    
#########################################################
#distanceGpio
import RPi.GPIO as GPIO #导入 GPIO库
import time

GPIO.setmode(GPIO.BOARD) #设置 GPIO 模式为BOARD
GPIO.setwarnings(False) #关闭错误提示

Trig_forward = 11 #定义 GPIO 前面
Echo_forward = 12
Trig_left = 13 #定义 GPIO pin 左边
Echo_left = 15
Trig_right = 16 #定义 GPIO pin 右边
Echo_right = 18
Trig_back = 29
Echo_back = 32

wave_out_list = [Trig_forward, Trig_left, Trig_right]
wave_in_list = [Echo_forward, Echo_left, Echo_right]
GPIO.setup(wave_out_list, GPIO.OUT) #设置 GPIO 的工作方式 (IN / OUT)
GPIO.setup(wave_in_list, GPIO.IN)

#crood = {'x':155,'y':70}
#x_crood = 155
#y_crood = 70



def get_median(data):
   data = sorted(data)
   size = len(data)
   if size % 2 == 0: # 判断列表长度为偶数
    median = (data[size//2]+data[size//2-1])/2
    data[0] = median
   if size % 2 == 1: # 判断列表长度为奇数
    median = data[(size-1)//2]
    data[0] = median
   return data[0]

def wave_distance(Trig, Echo):
    try:
        distance_list = []
        #for i in range(10):
        #start_time = time.time()
        #stop_time = time.time()
        for i in range(10):
            time.sleep(0.02)
            start_time = time.time()
            stop_time = start_time      
            GPIO.output(Trig, True) # 发送高电平信号到 Trig 引脚
            time.sleep(0.00001) # 持续 10 us
            GPIO.output(Trig, False)
            orgin_start_time = time.time()
            while GPIO.input(Echo) == 0: # 记录发送超声波的时刻1
                start_time = time.time()           
                # print(start_time)
            while GPIO.input(Echo) == 1: # 记录接收到返回超声波的时刻2
                stop_time = time.time()
                time_elapsed = stop_time - start_time # 计算超声波的往返时间 = 时刻2 - 时刻1
                distance = (time_elapsed * 34300) / 2 # 声波的速度为 343m/s， 转化34300cm/s          
                distance = int(distance)      
            if time.time() > orgin_start_time + 0.1:
                break
            distance_list.append(distance)
            #print(distance)
        result = max(distance_list, key=distance_list.count)
        if(3 < result < 600):
            return result       
    except:
        wave_distance(Trig, Echo)

def forward_wave_distance():
    distance = wave_distance(11,12)
    if distance != None:
        return distance
    else:
        return 0

def left_wave_distance():
    distance = wave_distance(13,15)
    if distance != None:
        return distance
    else:
        return 0

def right_wave_distance():
    # return wave_distance(16,18)
    distance = wave_distance(16,18)
    if distance != None:
        return distance
    else:
        return 0

def crood_update(crood):
    #y坐标，超声放前面，所以得减去超声波的测距距离
    #global x_crood
    #global y_crood

    b_distance = back_wave_distance()
    l_distance = left_wave_distance()
    #r_distance = right_wave_distance
    try:
        if(b_distance != 0):      
            #print('ddd') 
            crood['y'] = b_distance + 40
        elif(b_distance == 0):
            crood['y'] = 580 - forward_wave_distance()
        if(l_distance != 0):
            crood['x'] = l_distance + 7
        elif(l_distance == 0):
            print('ddd') 
            crood['x'] = 333 - right_wave_distance()
    except:
        crood_update(crood)

    #print(x_crood,y_crood)
    

#def crood_move(x_destination,y_destination):
    
######################################################
#colorDetect
# encoding:utf-8
from collections import deque
from types import CodeType
import numpy as np
import time
# import serial
import struct
# import imutils
import cv2

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

###############################################
# 串口初始化
# ser = serial.Serial("/dev/ttyAMA0",115200)
# print("uart open:",ser.isOpen())
# 协议数组
#arr = [0xaa, 0xaf, 0x03, 0x00, 0x00, 0x01, 0x5d]
import serial
import time
ser = serial.Serial('/dev/ttyS0', 115200) #打开串口
if ser.isOpen == False:
    ser.open()  

'''
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
'''

# 初始化追踪点的列表
# mybuffer = 16
# pts = deque(maxlen=mybuffer)
# counter = 0
# # 打开摄像头
# camera = cv2.VideoCapture(0)
# # 等待1秒
# time.sleep(1)

def find_storage(camera):
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
        
###############################################
#serialControl

# usb = serial.Serial('/dev/ttyUSB0', 115200)

              # 打开串口
#print('-----------------------------')
def init_state():
    ser.write(b"$DGT:2-3,1!") #初始

def putdown():
    ser.write(b"$DGT:4-10,1!") # 放下

def putup():
    ser.write(b"$DGT:11-21,1!")# 收起
#print('#################################')

def receive_serial():
    size = ser.inWaiting()               # 获得缓冲区字符
    start_time = time.time()
    while size != 0:
        response = ser.read(size)        # 读取内容并显示
        print(response)        
        ser.flushInput()                 # 清空接收缓存区
        time.sleep(0.1)
        if time.time() - start_time > 5.0:
            return response
    #return response



           

