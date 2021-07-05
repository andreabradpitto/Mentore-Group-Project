# Hello_single_hand  Mentore

# Import libraries
import RPi.GPIO as GPIO
import time

# Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

GPIO.setup(3,GPIO.OUT)
GPIO.setup(5,GPIO.OUT)
servo_righthand = GPIO.PWM(3,50) # pin 3 for servo_righthand
servo_rightarm = GPIO.PWM(5,50) # pin 5 for servo_rightarm
#initialize servos with pulse off
servo_righthand.start(0)
servo_rightarm.start(0)


#lifting up the  right arm 
n=1
while n < 8:
    servo_rightarm.ChangeDutyCycle(n)
    time.sleep(0.1)
    n=n+0.5
    servo_rightarm.stop
    

m=1
while m < 4:
    servo_righthand.ChangeDutyCycle(11)
    time.sleep(0.5)
    servo_righthand.ChangeDutyCycle(2)
    time.sleep(0.5)
    m=m+1   

#putting the arm in resting position
n=8

while n > 1:
    servo_rightarm.ChangeDutyCycle(n)
    time.sleep(0.1)
    n=n-0.5
       
servo_rightarm.stop
servo_righthand.stop
GPIO.cleanup()