import time
import RPi.GPIO as GPIO

# On track proximity sensor reading is 1
# Declare GPIO pins
SENSOR_1 = 19
SENSOR_2 = 21
SENSOR_3 = 23
SENSOR_4 = 36


MOTOR_RIGHT_ENABLE1 = 33
MOTOR_RIGHT_PIN1 = 15
MOTOR_RIGHT_PIN2 = 13
MOTOR_LEFT_ENABLE2 = 32
MOTOR_LEFT_PIN3 = 16
MOTOR_LEFT_PIN4 = 18


PWM_CONTROL_RIGHT = None
PWM_CONTROL_LEFT = None
SPEED_HIGH = 100
SPEED_LOW = 60


# Left to Right
S1 = "One"
S2 = "Two"
S3 = "Three"
S4 = "Four"

ADJUSTING_TIME_DELAY = 0.03  # Adjusting movement


def speedDownRightMotor():
    global SPEED_LOW
    PWM_CONTROL_RIGHT.ChangeDutyCycle(SPEED_LOW)


def speedDownLeftMotor():
    global SPEED_LOW
    PWM_CONTROL_LEFT.ChangeDutyCycle(SPEED_LOW)


def speedUpRightMotor():
    global SPEED_HIGH
    PWM_CONTROL_RIGHT.ChangeDutyCycle(SPEED_HIGH)


def speedUpLeftMotor():
    global SPEED_HIGH
    PWM_CONTROL_LEFT.ChangeDutyCycle(SPEED_HIGH)


def setupMotorIO():
    global PWM_CONTROL_LEFT
    global PWM_CONTROL_RIGHT
    global SPEED_HIGH
    GPIO.setup(MOTOR_RIGHT_ENABLE1, GPIO.OUT)
    GPIO.setup(MOTOR_RIGHT_PIN1, GPIO.OUT)
    GPIO.setup(MOTOR_RIGHT_PIN2, GPIO.OUT)
    GPIO.setup(MOTOR_LEFT_ENABLE2, GPIO.OUT)
    GPIO.setup(MOTOR_LEFT_PIN3, GPIO.OUT)
    GPIO.setup(MOTOR_LEFT_PIN4, GPIO.OUT)
    PWM_CONTROL_RIGHT = GPIO.PWM(MOTOR_RIGHT_ENABLE1, 100)  # Initial Freq 100
    PWM_CONTROL_LEFT = GPIO.PWM(MOTOR_LEFT_ENABLE2, 100)  # Initial Freq 100
    PWM_CONTROL_LEFT.start(SPEED_HIGH)
    PWM_CONTROL_RIGHT.start(SPEED_HIGH)


def setupSensorIO():
    GPIO.setup(SENSOR_1, GPIO.IN)
    GPIO.setup(SENSOR_2, GPIO.IN)
    GPIO.setup(SENSOR_3, GPIO.IN)
    GPIO.setup(SENSOR_4, GPIO.IN)


def setupIO():
    GPIO.setmode(GPIO.BOARD)
    setupMotorIO()
    setupSensorIO()


def moveRightMotorForward():
    GPIO.output(MOTOR_RIGHT_ENABLE1, 1)
    GPIO.output(MOTOR_RIGHT_PIN1, 1)
    GPIO.output(MOTOR_RIGHT_PIN2, 0)


def moveRightMotorBackward():
    GPIO.output(MOTOR_RIGHT_ENABLE1, 1)
    GPIO.output(MOTOR_RIGHT_PIN1, 0)
    GPIO.output(MOTOR_RIGHT_PIN2, 1)


def moveLeftMotorForward():
    GPIO.output(MOTOR_LEFT_ENABLE2, 1)
    GPIO.output(MOTOR_LEFT_PIN3, 1)
    GPIO.output(MOTOR_LEFT_PIN4, 0)


def moveLeftMotorBackward():
    GPIO.output(MOTOR_LEFT_ENABLE2, 1)
    GPIO.output(MOTOR_LEFT_PIN3, 0)
    GPIO.output(MOTOR_LEFT_PIN4, 1)


def stay_put():
    GPIO.output(MOTOR_LEFT_ENABLE2, 0)
    GPIO.output(MOTOR_LEFT_PIN3, 0)
    GPIO.output(MOTOR_LEFT_PIN4, 0)
    GPIO.output(MOTOR_RIGHT_ENABLE1, 0)
    GPIO.output(MOTOR_RIGHT_PIN1, 0)
    GPIO.output(MOTOR_RIGHT_PIN2, 0)
    time.sleep(ADJUSTING_TIME_DELAY)


def getSensorReadings():
    val = {
        S1: GPIO.input(SENSOR_1),
        S2: GPIO.input(SENSOR_2),
        S3: GPIO.input(SENSOR_3),
        S4: GPIO.input(SENSOR_4),
    }
    # printSensorReadings(val)
    return val


def printSensorReadings(sensorVal):
    print(S1 + ": " + str(sensorVal[S1]) + " " + S2 + ": " + str(sensorVal[S2]) + " " + S3 + ": " + str(sensorVal[S3]) +
          " " + S4 + ": " + str(sensorVal[S4]))


def stopRotation():
    sensorVal = getSensorReadings()
    if (sensorVal[S2] == 1 or sensorVal[S3] == 1):
        return True
    else:
        return False


def turn_left():
    speedDownLeftMotor()
    speedDownRightMotor()
    moveRightMotorForward()
    moveLeftMotorBackward()
    time.sleep(ADJUSTING_TIME_DELAY)
    stay_put()
    while True:
        moveRightMotorForward()
        moveLeftMotorBackward()
        time.sleep(ADJUSTING_TIME_DELAY)
        stay_put()
        if (stopRotation()):
            break
    speedUpLeftMotor()
    speedUpRightMotor()
    # print("Turn Left")


def turn_right():
    speedDownLeftMotor()
    speedDownRightMotor()
    moveRightMotorBackward()
    moveLeftMotorForward()
    time.sleep(ADJUSTING_TIME_DELAY)
    stay_put()
    while True:
        moveRightMotorBackward()
        moveLeftMotorForward()
        time.sleep(ADJUSTING_TIME_DELAY)
        stay_put()
        if (stopRotation()):
            break
    speedUpLeftMotor()
    speedUpRightMotor()
    # print("Turn Right")


def adjust_left():
    speedDownRightMotor()
    moveRightMotorForward()
    time.sleep(ADJUSTING_TIME_DELAY)
    stay_put()
    speedUpRightMotor()
    # print("Adjust left")


def adjust_right():
    speedDownLeftMotor()
    moveLeftMotorForward()
    time.sleep(ADJUSTING_TIME_DELAY)
    stay_put()
    speedUpLeftMotor()
    # print("Adjust right")


def straight(steps=1):
    for step in range(steps):
        moveLeftMotorForward()
        moveRightMotorForward()
        time.sleep(ADJUSTING_TIME_DELAY)
        stay_put()
    # print("Straight")


def back(steps=1):
    for step in range(steps):
        moveLeftMotorBackward()
        moveRightMotorBackward()
        time.sleep(ADJUSTING_TIME_DELAY)
        stay_put()
    # print("Back")


def turn_around():
    # print("Turn around")
    turn_right()


def unmapped():
    stay_put()
    # print("Unmapped, this should not happen")


def decideAction():
    sensorVal = getSensorReadings()

    # map sensorVal to BOT_MOVEMENT

    if (sensorVal[S2] == 0 and sensorVal[S3] == 1) or (sensorVal[S1] == 0 and sensorVal[S2] == 0 and sensorVal[S3] == 0 and sensorVal[S4] == 1):
        return "adjust_right"
    elif (sensorVal[S2] == 1 and sensorVal[S3] == 0) or (sensorVal[S1] == 1 and sensorVal[S2] == 0 and sensorVal[S3] == 0 and sensorVal[S4] == 0):
        return "adjust_left"
    elif sensorVal[S1] == 0 and sensorVal[S2] == 0 and sensorVal[S3] == 0 and sensorVal[S4] == 0:
        adjust_left()
        time.sleep(ADJUSTING_TIME_DELAY)
        sensorValLeft = getSensorReadings()
        adjust_right()
        adjust_right()
        time.sleep(ADJUSTING_TIME_DELAY)
        sensorValRight = getSensorReadings()
        adjust_left()
        if (sensorValLeft[S1] == 0 and sensorValLeft[S2] == 0 and sensorValLeft[S3] == 0 and sensorValLeft[S4] == 0) and (sensorValRight[S1] == 0 and sensorValRight[S2] == 0 and sensorValRight[S3] == 0 and sensorValRight[S4] == 0):
            return "dead_end"
        else:
            return ""

    nextReading = ""
    sensorValNew = None
    if sensorVal[S1] == 1 or sensorVal[S4] == 1:
        stay_put()
        sensorValNew = getSensorReadings()
        if sensorVal[S1] == 1 or sensorValNew[S1] == 1:
            nextReading = nextReading + "left"
        if sensorVal[S4] == 1 or sensorValNew[S4] == 1:
            nextReading = nextReading + "right"
        while True:
            straight()
            sensorValNew = getSensorReadings()
            if (sensorVal[S1] == 1 and sensorValNew[S1] == 0) or (sensorVal[S4] and sensorValNew[S4] == 0):
                # move just one more step
                straight()
                sensorValNew = getSensorReadings()
                break
        if sensorValNew[S2] == 1 or sensorValNew[S3] == 1:
            nextReading = nextReading + "straight"

    elif sensorVal[S2] == 1 and sensorVal[S3] == 1:
        return "straight"

    return nextReading


nodesFound = []


def logDecisions(decision):
    if (decision != "straight" and decision != "adjust_left" and decision != "adjust_right" and decision != ""):
        print(decision)
        nodesFound.append(decision)


def act():
    decision = decideAction()
    # print(decision)
    logDecisions(decision)
    if decision == "straight":
        straight()
    elif decision == "adjust_left":
        adjust_left()
    elif decision == "adjust_right":
        adjust_right()
    elif decision == "left":
        turn_left()
    elif decision == "right":
        turn_right()
    elif decision == "leftright":
        turn_left()
    elif decision == "leftstraight":
        turn_left()
    elif decision == "rightstraight":
        straight()
    elif decision == "leftrightstraight":
        turn_left()
    elif decision == "dead_end":
        turn_around()
    elif decision == "stay":
        stay_put()
        return false
    else:
        unmapped()


print("Starting program")
setupIO()
try:
    while True:
        act()


except KeyboardInterrupt:
    GPIO.cleanup()
    print(nodesFound)
