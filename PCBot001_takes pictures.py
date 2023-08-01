#!/usr/bin/env python3
import serial
import time
from picamera import PiCamera
from datetime import datetime
import os

camera = PiCamera() #define a camera object
camera.resolution = (640,480) # 640,480 / 1280,720 
image_folder_name = "/home/pi/camera"
if not os.path.exists(image_folder_name):
    os.mkdir(image_folder_name)

name = "PCBot001_" #filename root

while True:
    try:
        ser = serial.Serial('/dev/ttyUSB0',115200, timeout=0.5)
        #ACM0 for arduino, USB0 for other boards
        break
    except serial.SerialException:
        print("Could not connect to serial. Trying again")
        
#time.sleep(1)  
ser.reset_input_buffer()
print("Open serial communication/n")

last_time_servo_move = time.time()
servo_delay = 3 # 3 sec = 3,000 msec 
servo_counter = -5
servo_going_up = True

try:
    while True:
        #------------------Servo Sweep------------------------
              
        time_now = time.time()
        
        if time_now - last_time_servo_move >= servo_delay:
            last_time_servo_move = time_now
            if servo_going_up:
                servo_counter += 5
                filename = image_folder_name + "/" + name + str(servo_counter) + "_" + datetime.now().strftime("%Y-%m-%d_%H.%M.%S.jpg")
                camera.capture(filename)
                time.sleep(2)  
                if servo_counter == 45:
                    servo_going_up = False
            else:
                servo_counter -= 5
                filename = image_folder_name + "/" + name + str(servo_counter) + "_" + datetime.now().strftime("%Y-%m-%d_%H.%M.%S.jpg")
                camera.capture(filename)
                time.sleep(2)  
                if servo_counter == 0:
                    servo_going_up = True
                    
            Tx = str(servo_counter) + "\n" #Transmitte command to Arduino
            ser.write(Tx.encode('utf-8'))
            
            if ser.in_waiting > 0:
                #time.sleep(0.01)
                Rx = ser.readline().decode('utf-8').rstrip() #Receive command from Arduino
                print(Rx)
            
except KeyboardInterrupt: #press ctrl + C
    print("Close serial communication")
    ser.close()