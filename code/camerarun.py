#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
from picamera2.encoders import H264Encoder
from picamera2 import Picamera2, Preview

#picam init
picam2 = Picamera2()

preview_config = picam2.create_preview_configuration(main={"size": (1920, 1080)})
picam2.configure(preview_config)
video_config = picam2.create_video_configuration()

encoder = H264Encoder(bitrate=10000000)

cameramode = True
isrecording = False

#gpio init
shutterbutton = 40
rotaryA = 31
rotaryB = 32
sbuttondown = False

GPIO.setmode(GPIO.BOARD)
GPIO.setup(shutterbutton, GPIO.IN, pull_up_down=GPIO.PUD.UP)
GPIO.setup(rotaryA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(rotaryB, GPIO.IN, pull_up_down=GPIO.PUD_UP)

aLastState = GPIO.input(rotaryA) #read initial state of rotaryA

print('\033[1;37m' + "Photograph mode" + '\033[0;0')
print('\033[1;37m' + "Waiting for input" + '\033[0;0')

while True:
  aState = GPIO.input(rotaryA)
  if aState != aLastState:
    if GPIO.input(rotaryB) != aState:
      if cameramode == False:
        cameramode = True
        picam2.configure(preview_config)
        print('\033[1;37m' + "Switched to photograph mode" + '\033[0;0')
        time.sleep(0.1)
    else:
      if cameramode == True:
        cameramode = False
        picam2.configure(video_config)
        print('\033[1;37m' + "Switched to video mode" + '\033[0;0')
        time.sleep(0.1)
  aLastState = aState #update the previous state of rotaryA with current state

  if GPIO.input(shutterbutton) == GPIO.LOW:
    sbuttondown = True
  else:
    sbuttondown = False
    
  if sbuttondown == True:
    if isrecording == False:
      if cameramode == True:
        picam2.start_preview(Preview.QTGL, x=0, y=0, width=1920, height=1080)
        picam2.start()
        time.sleep(2)
        current_time = time.strftime("%yy-%MM-%dd-%HH-mm-ss", time.localtime())
        picam2.capture_file("/home/ceres/Pictures/{}.jpg".format(current_time))
        picam2.stop_preview()
        Picam2.stop()
        print("Photo taken!", current_time)
        time.sleep(1)
      else:
        isrecording = True
        current_time = time.strftime("%yy-%MM-%dd-%HH-mm-ss", time.localtime())
        picam2.start_encoder(encoder, "/home/ceres/Pictures/{}.h264".format(current_time))
        picam2.start()   
        print("Recording starting!", current_time)
        time.sleep(1)
    else:
      time.wait(1)
  else:
    If isrecording == True:
      picam2.stop()
      picam2.stop_encoder()
      isrecording = False
      print("Recording ended!") 
      time.sleep(1)
