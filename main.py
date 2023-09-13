import BlynkLib
from motorController import front, stay_put, back, right, left, setMotorSpeed, MIN_MOTOR_SPEED, MAX_MOTOR_SPEED
from servoController import Servo
 
servo = Servo(pin=40,duty_cycle_range=(2.5, 7.5))
 
# Initialize Blynk
blynk = BlynkLib.Blynk('HviiBXOrIARr2SjQaBe-16IAsm8k5Ml5', server='blynk.cloud')
 
@blynk.on("V0")
def my_V0_write_handler(value):
    print('Current V0 value: {}'.format(value))
    if int(value[0]) != 0:
        back()
        print('Moving Backward')
    else:
        stay_put()
        print('Stay')
 
@blynk.on("V1")
def my_V1_write_handler(value):
    print('Current V1 value: {}'.format(value))
    if int(value[0]) != 0:
        front()
        print('Moving Forward')
    else:
        stay_put()
        print('Stay')
 
@blynk.on("V2")
def my_V2_write_handler(value):
    print('Current V2 value: {}'.format(value))
    if int(value[0]) != 0:
        left()
        print('Moving Left')
    else:
        stay_put()
        print('Stay')
 
@blynk.on("V3")
def my_V3_write_handler(value):
    print('Current V3 value: {}'.format(value))
    if int(value[0]) != 0:
        right()
        print('Moving Right')
    else:
        stay_put()
        print('Stay')
 
@blynk.on("V4")
def my_V4_write_handler(value):
    print('Current V4 value: {}'.format(value))
    servo.servo_toggle()
 
 
while True:
    blynk.run()
