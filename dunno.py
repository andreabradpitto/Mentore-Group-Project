# dunno  Mentore

# Import libraries
import RPi.GPIO as GPIO
import time

# Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

GPIO.setup(3,GPIO.OUT)
GPIO.setup(5,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)

servo_righthand = GPIO.PWM(3,50) # pin 3 for servo_righthand
servo_rightarm = GPIO.PWM(5,50) # pin 5 for servo_rightarm
servo_leftarm = GPIO.PWM(13,50) # pin 13 for servo_righthand
servo_lefthand= GPIO.PWM(15,50) # pin 15 for servo_rightarm

#initialize servos with pulse off
servo_righthand.start(0)
servo_rightarm.start(0)
servo_leftarm.start(0)
servo_lefthand.start(0)



servo_righthand.ChangeDutyCycle(2)
servo_lefthand.ChangeDutyCycle(2)
m=1
while m < 2:
    servo_rightarm.ChangeDutyCycle(2)
    servo_leftarm.ChangeDutyCycle(11)
    
    servo_righthand.ChangeDutyCycle(11)
    servo_lefthand.ChangeDutyCycle(3)
    servo_leftarm.stop
    servo_rightarm.stop
    time.sleep(1)
    servo_righthand.ChangeDutyCycle(2)
    servo_lefthand.ChangeDutyCycle(11)
    time.sleep(0.4)
    servo_rightarm.ChangeDutyCycle(2)
    servo_leftarm.ChangeDutyCycle(11)
    time.sleep(0.5)
    m=m+1   



       

GPIO.cleanup()