import RPi.GPIO as GPIO
import time
import distanceGpio
from colorDetect import *



#31 33 35 37 36 38
#2  3  4  5  6  7

Forward_pin = 31;                   #前进引脚
Back_pin = 33;                      #后引脚

Turn_Right_pin = 35;                #右平移引脚
Turn_Left_pin = 37;                 #左平移引脚

Clockwise_Rotation_Pin = 36;        #顺时针旋转引脚
Counter_Clockwise_Rotation_pin = 38;#逆时针旋转引脚

crood = {'x':155,'y':70}
#小车的线速度和角速度
y_line_speed = 14.7 # cm/s
x_line_speed = 8  # cm/s
w_speed = 43    # °/s

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(Forward_pin,GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(Back_pin,GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(Turn_Right_pin,GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(Turn_Left_pin,GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(Clockwise_Rotation_Pin,GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(Counter_Clockwise_Rotation_pin,GPIO.OUT,initial = GPIO.LOW)

#time.sleep(1)

def set_gpio_state(state_forward_pin = 0,state_back_pin = 0,state_right_pin = 0,state_left_pin = 0,state_clock_pin = 0,state_counter_pin = 0):
    GPIO.output(Forward_pin,state_forward_pin)
    GPIO.output(Back_pin,state_back_pin)
    GPIO.output(Turn_Right_pin,state_right_pin)
    GPIO.output(Turn_Left_pin,state_left_pin)
    GPIO.output(Clockwise_Rotation_Pin,state_clock_pin)
    GPIO.output(Counter_Clockwise_Rotation_pin,state_counter_pin)

def stop(t = 0):
    print('stop')
    set_gpio_state(0,0,0,0,0,0)
    time.sleep(1)
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
    #stop(0.1)
    print('前进')
    global move_state
    move_state = 1
    set_gpio_state(1,0,0,0,0,0)
    if s != 0:
        time.sleep(s/y_line_speed)
        stop()

def forward2(s = 0):
    #stop(0.1)
    print('前进2')
    set_gpio_state(1,1,0,0,0,0)
    if s != 0:
        time.sleep(s/19)
        stop()

def back(s = 0):
    #stop(0.1)
    print('后退')
    set_gpio_state(0,1,0,0,0,0)
    if s != 0:
        time.sleep(s/y_line_speed)
        stop()

def back2(s = 0):
    #stop(0.1)
    print('后退')
    global move_state
    move_state = 2
    set_gpio_state(0,1,0,0,0,0)
    if s != 0:
        time.sleep(s/y_line_speed)
        stop()

def turn_left(s = 0):
    #stop(0.)
    print('←')
    set_gpio_state(0,0,0,1,0,0)
    if s != 0:
        time.sleep(s / x_line_speed)
        stop()

def turn_right(s = 0):
    #stop(0.1)
    print('→')
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

    #坐标的
def move_to(
    x_destination = 259, y_destination = 342,
            x_current = crood['x'], y_current = crood['y'],commit_error=5):
    #crood_update()
    #if x_destination == 0:
        
    #目标-目前
    #commit_error = 
    x_distance = x_destination - x_current
    y_distance = y_destination - y_current
    
    if y_current == 0:
        if(x_distance<-commit_error):
        #sent_move_data(-x_distance,0,0)    
            turn_left()
        elif(x_distance>commit_error):
            #sent_move_data(x_distance,0,0)    
            turn_right()
        else:
            stop()
            return 'done'
    else:
        if(y_distance>commit_error):
            #sent_move_data(0,y_distance,0)   
            forward()
        elif(y_distance<-commit_error):
            #sent_move_data(0,-y_distance,0)   
            back()
        else:
            if(x_distance<-commit_error):
                #sent_move_data(-x_distance,0,0)    
                turn_left()
            elif(x_distance>commit_error):
                #sent_move_data(x_distance,0,0)    
                turn_right()
            else:
                stop()
                return 'done'
        
#摄像头的移动
def camera_move_to(x_current = 320,
    x_destination = 280,commit_error=20):
    #crood_update()
    #if x_destination == 0:
        
    #目标-目前
    x_distance = x_destination - x_current
    if(x_distance<-commit_error):
        #sent_move_data(-x_distance,0,0)    
        turn_right()
    elif(x_distance>commit_error):
        #sent_move_data(x_distance,0,0)    
        turn_left()
    else:
        stop()
        return 'done'

#这个坐标用框框的中心点来表示


def move_test():
    # 打开摄像头,开启颜色识别
    camera = cv2.VideoCapture(0)
    #找到目标垃圾的颜色
    ljbin_color = 'red'
    while True:
        ljbin_xy = color_detect(camera, ljbin_color)
        if 'done' != camera_move_to(ljbin_xy['x'],ljbin_xy['y'],320,240):  
            crood_update()
        else :
            break

    # 摄像头释放
    camera.release()
    back(1)
    while 0:
        #wink()
        print('here is in main of moveGpio')
        control_on()
        # distanceGpio.crood_update(crood)
        #if 'done' == move_to(crood['x'],crood['y'],70,100,10):
        #    break
        print(crood)
        #counter(30)
        #set_gpio_state(0,1,0,1,0,1)
        #time.sleep(1)
        # forward(100)#forward
        # time.sleep(5)
        # #forward(80)
        # #time.sleep(5)
        # back(100)#back
        # time.sleep(5)
        #turn_right(50)
        #back(80)
        #turn_left(100)
        #time.sleep(7)
        #turn_right(100)
        back(1)
        #time.sleep(7)
        #turn_left(50)#left     
#         time.sleep(3)
        #clock(30)#sun
        #time.sleep(3)
        #counter(90)#ni
        #clock()
        #time.sleep(3)
        #time.sleep(0.1)
        #stop()#stop
        #time.sleep(3)
        #set_gpio_state(0,1,0,1,0,1)
        #time.sleep(2)
        #set_gpio_state(0,0,0,0,1,0)#sun
        #control_off()
        #time.sleep(10)
    control_off()
    GPIO.cleanup()   

if __name__ == '__main__':
    try:
        back(30)
        #move_test()
    except KeyboardInterrupt:   
        GPIO.cleanup()