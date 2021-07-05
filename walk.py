# Hello_single_hand  Mentore

# Import libraries
import RPi.GPIO as GPIO
import time

# Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

GPIO.setup(3,GPIO.OUT) #gpio right hand
GPIO.setup(5,GPIO.OUT) #gpio right arm
GPIO.setup(7,GPIO.OUT) #gpio right leg
GPIO.setup(11,GPIO.OUT) #gpio left leg
GPIO.setup(13,GPIO.OUT) #gpio left arm
GPIO.setup(15,GPIO.OUT) #gpio left hand 

servo_righthand = GPIO.PWM(3,50) # pin 3 for servo_righthand
servo_rightarm = GPIO.PWM(5,50) # pin 5 for servo_rightarm
servo_leftleg = GPIO.PWM(7,50) # pin 3 for servo_rihtleg
servo_rightleg = GPIO.PWM(11,50) # pin 5 for servo_leftleg
servo_leftarm = GPIO.PWM(13,50) # pin 13 for servo_righthand
servo_lefthand= GPIO.PWM(15,50) # pin 15 for servo_rightarm

#initialize servos with pulse off
servo_righthand.start(0)
servo_rightarm.start(0)
servo_leftleg.start(0)
servo_rightleg.start(0)
servo_leftarm.start(0)
servo_lefthand.start(0)
# 
t=1
while(t<10):
  
    m=0
    while (m<0.5):
        
       servo_leftleg.ChangeDutyCycle(9.5-m)
       servo_rightleg.ChangeDutyCycle(10-m)
       time.sleep(0.1)
       servo_rightleg.stop
       servo_leftleg.stop
       m=m+0.1

     
    m=0.5
    while (m>0):
       servo_leftleg.ChangeDutyCycle(9.5-m)
       servo_rightleg.ChangeDutyCycle(10-m)
       time.sleep(0.1)
       servo_rightleg.stop
       servo_leftleg.stop
       m=m-0.1
    t=t+1

time.sleep(0.1)
servo_rightleg.stop
servo_leftleg.stop
     

GPIO.cleanup()