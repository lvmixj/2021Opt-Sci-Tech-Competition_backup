
# -*- coding: utf-8 -*raspberry receive
import serial
import time
from moveGpio import *
ser = serial.Serial('/dev/ttyS0', 115200)
# usb = serial.Serial('/dev/ttyUSB0', 115200)

if ser.isOpen == False:
    ser.open()                # 打开串口
#print('-----------------------------')
def init_state():
    ser.write(b"$DGT:2-3,1!") #初始

def putdown():
    ser.write(b"$DGT:4-11,1!") # 放下

def putup():
    ser.write(b"$DGT:12-22,1!")# 收起
#print('#################################')

def receive_serial():                 
    start_time = time.time()
    while True:
        size = ser.inWaiting()           # 获得缓冲区字符
        response = ser.read(size)        # 读取内容并显示
        str_res = str(response)
        #print(str_res)
        
        # if 'battery' in str_res :
        #     return 'battery'
        # elif 'orange' in str_res:
        #     print('ooo')
        #     return 'orange'
        # elif 'paper' in str_res:
        #     return 'paper'
        # elif 'cup' in str_res:
        #     return 'cup'
        # elif 'bottle' in str_res:
        #     return 'bottle'
        # else :
        #     print('bbb')
        #     return 'bottle'
        
        #进行数据处理
        #response.split(b'\n') 
        ser.flushInput()                 # 清空接收缓存区
        
        time.sleep(0.4)
        if time.time() - start_time > 1:
            #return response
            break
        str_res = ' '
    if 'battery' in str_res :
            return 'battery'
    elif 'orange' in str_res:
        print('ooo')
        return 'orange'
    elif 'paper' in str_res:
        return 'paper'
    elif 'cup' in str_res:
        return 'cup'
    elif 'bottle' in str_res:
        return 'bottle'
    else :
        print('bbb')
        return 'bottle'        
    #return response


if __name__ == '__main__':
    #control_on()
    # init_state()
    # time.sleep(2)
    # putdown()
    # time.sleep(12)
    #putdown()
    #forward(20)
    #turn_left(20)
    #turn_right(20)
    # time.sleep(8)
    # putup()
    #time.sleep(5)
    #init_state()
    print(receive_serial())