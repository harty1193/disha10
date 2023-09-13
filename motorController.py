import time
import RPi.GPIO as GPIO

# Right motor
MOTOR_RIGHT_ENABLE = 33 
MOTOR_RIGHT_PINA = 31
MOTOR_RIGHT_PINB = 29

# Left motor
MOTOR_LEFT_ENABLE = 32
MOTOR_LEFT_PINA = 36
MOTOR_LEFT_PINB = 38

TURN_TIME = 0.25

PWM_SETUP_VALUE = 1000 
MAX_MOTOR_SPEED  = 100
MIN_MOTOR_SPEED = 60

LEFT_MOTOR_SPEED = None
RIGHT_MOTOR_SPEED = None

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(MOTOR_RIGHT_ENABLE, GPIO.OUT)
GPIO.setup(MOTOR_RIGHT_PINA, GPIO.OUT)
GPIO.setup(MOTOR_RIGHT_PINB, GPIO.OUT)
GPIO.setup(MOTOR_LEFT_ENABLE, GPIO.OUT)
GPIO.setup(MOTOR_LEFT_PINA, GPIO.OUT)
GPIO.setup(MOTOR_LEFT_PINB, GPIO.OUT)

GPIO.output(MOTOR_RIGHT_PINA, 0)
GPIO.output(MOTOR_RIGHT_PINB, 0)

LEFT_MOTOR_SPEED = GPIO.PWM(MOTOR_LEFT_ENABLE, PWM_SETUP_VALUE)
RIGHT_MOTOR_SPEED = GPIO.PWM(MOTOR_RIGHT_ENABLE, PWM_SETUP_VALUE)

LEFT_MOTOR_SPEED.start( MIN_MOTOR_SPEED)
RIGHT_MOTOR_SPEED.start(MIN_MOTOR_SPEED)

def setMotorSpeed(val):
    if val >= MIN_MOTOR_SPEED and val <= 100:
        LEFT_MOTOR_SPEED.start(val)
        RIGHT_MOTOR_SPEED.start(val)

def stay_put():
    GPIO.output(MOTOR_LEFT_PINA, 0)
    GPIO.output(MOTOR_LEFT_PINB, 0)
    GPIO.output(MOTOR_RIGHT_PINA, 0)
    GPIO.output(MOTOR_RIGHT_PINB, 0)

def rightMotorForword():
    
    GPIO.output(MOTOR_RIGHT_PINA, 1)
    GPIO.output(MOTOR_RIGHT_PINB, 0)

def leftMotorForword():
    
    GPIO.output(MOTOR_LEFT_PINA, 1)
    GPIO.output(MOTOR_LEFT_PINB, 0)

def rightMotorBackword():
    
    GPIO.output(MOTOR_RIGHT_PINA, 0)
    GPIO.output(MOTOR_RIGHT_PINB, 1)

def leftMotorBackword():
    
    GPIO.output(MOTOR_LEFT_PINA, 0)
    GPIO.output(MOTOR_LEFT_PINB, 1)


def front():
    rightMotorForword()
    leftMotorForword()
    print("Move Front")


def back():
    rightMotorBackword()
    leftMotorBackword()
    print("Move Back")


def left():
    rightMotorForword()
    leftMotorBackword()
    print("Move Left")


def right():
    leftMotorForword()
    rightMotorBackword()
    print("Turn right")
