# 把前面的超声波毙了

import RPi.GPIO as GPIO #导入 GPIO库
import time
import serialControl

#serialControl.putdown()
#time.sleep(8)
#serialControl.putup()

GPIO.setmode(GPIO.BOARD) #设置 GPIO 模式为BOARD
GPIO.setwarnings(False) #关闭错误提示

Trig_forward = 7#11 #定义 GPIO 前面
Echo_forward = 22
Trig_left = 13 #定义 GPIO pin 左边
Echo_left = 15
Trig_right = 16 #定义 GPIO pin 右边
Echo_right = 18
Trig_back = 29
Echo_back = 32


crood = {'x':155,'y':70}
#x_crood = 155
#y_crood = 70

wave_out_list = [Trig_forward, Trig_left, Trig_right,Trig_back]
wave_in_list = [Echo_forward, Echo_left, Echo_right, Echo_back]
GPIO.setup(wave_out_list, GPIO.OUT) #设置 GPIO 的工作方式 (IN / OUT)
GPIO.setup(wave_in_list, GPIO.IN)

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
    #try:
    distance_list = []
    #for i in range(10):
    #start_time = time.time()
    #stop_time = time.time()
    for i in range(5):
        time.sleep(0.01)
        start_time = time.time()
        stop_time = start_time      
        GPIO.output(Trig, True) # 发送高电平信号到 Trig 引脚
        time.sleep(0.00001) # 持续 10 us
        GPIO.output(Trig, False)
        orgin_start_time = time.time()
        while GPIO.input(Echo) == 0: # 记录发送超声波的时刻1
            start_time = time.time()
            if time.time() > orgin_start_time + 0.1:
                distance = 0
                distance_list.append(distance)
                break           
            # print(start_time)
        while GPIO.input(Echo) == 1: # 记录接收到返回超声波的时刻2
            stop_time = time.time()
            time_elapsed = stop_time - start_time # 计算超声波的往返时间 = 时刻2 - 时刻1
            distance = (time_elapsed * 34300) / 2 # 声波的速度为 343m/s， 转化34300cm/s          
            distance = int(distance)      
        try:
            distance_list.append(distance)
        except:
            distance = 0
            distance_list.append(distance)
        #print(distance)
    try:
        result = max(distance_list, key=distance_list.count)
    except:
        result = 0
    if(3 < result < 450):
        return result        
    # except:
    #     wave_distance(Trig, Echo)

def forward_wave_distance():
    distance = wave_distance(7,Echo_forward)
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

def back_wave_distance():
    # return wave_distance(16,18)
    distance = wave_distance(29,32)
    if distance != None:
        return distance
    else:
        return 0

def crood_update4(crood = crood, dec = 1):
    print(crood)
    before_x_crood = crood['x']
    before_y_crood = crood['y']
    b_distance = back_wave_distance()
    l_distance = left_wave_distance()
    #r_distance = right_wave_distance
    if dec == 0:
        # print('====')
        # if b_distance != None:
        #     if b_distance != 0:
        #         if (b_distance <= 340):
        #             print('1')
        crood['y'] = b_distance + 4
    elif dec == 1:
        #print('2')
        crood['y'] = 610 - forward_wave_distance() - 18  
        
    if(l_distance <= 200):
        #print('3')
        crood['x'] = l_distance + 6
    elif (l_distance > 200):
        #print('4')
        crood['x'] = 345 - right_wave_distance() 
        #print(crood)


def crood_update(crood = crood):
    #y坐标，超声放前面，所以得减去超声波的测距距离
    before_x_crood = crood['x']
    before_y_crood = crood['y']

    b_distance = back_wave_distance()
    l_distance = left_wave_distance()
    #r_distance = right_wave_distance
    try:
        print('====')
        if(b_distance != 0):      
            print('1') 
            crood['y'] = b_distance + 4
        elif(b_distance == 0):
            crood['y'] = 610 - forward_wave_distance() - 30
        if(l_distance != 0):
            crood['x'] = l_distance + 6
        elif(l_distance == 0):
            crood['x'] = 345 - right_wave_distance()           
            print('右边超声波启动')
        
    except:
        crood_update(crood = crood)

def crood_update_x(crood = crood):
    l_distance = left_wave_distance()
    if(l_distance != None):
        if l_distance != 0 :
            crood['x'] = l_distance + 6
        elif(r_distance == 0):
            crood['x'] = 345 - right_wave_distance()           
            print('左边超声波启动')
        print(crood)



#print(x_crood,y_crood)
#def crood_move(x_destination,y_destination):
    
if __name__ == '__main__':
    #serialControl.init()
    #serialControl.putdown()
    #serialControl.putup()
    while True:
        #x_crood = 155
        #y_crood = 25
        #time.sleep(0.1)
        print('forward',forward_wave_distance())
        print('left',wave_distance(13,15))
        #wave_distance(16,18)
        print('right',wave_distance(16,18))
        print('back',back_wave_distance())
        #crood_update(crood)
        #crood_update4(crood,0)
        #crood_update4(crood)
        #print(crood)
        #print(crood['x'],crood['y'])
        #print('-------------------')
