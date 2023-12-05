import time
import math
from machine import Pin, PWM, ADC

# Game introduction and calibration setup:
print("Welcome to the etch a sketch game")
print("Use the right potentiometer to control Y and the left potentiometer to control X")
print("Use the middle button to raise and lower the pen")


# SECTION - GLOBAL VARIABLES

# Constants for PWM range (specify according to your servo specifications)
PWM_MIN = 1638  # Minimum PWM value (0 degrees)
PWM_MAX = 8192  # Maximum PWM value (180 degrees)

# Initialize the servo motors
shoulder_servo = PWM(Pin(0))  # GPIO0
elbow_servo = PWM(Pin(1))     # GPIO1
pen_servo = PWM(Pin(2))       # GPIO2
shoulder_servo.freq(50)
elbow_servo.freq(50)
pen_servo.freq(50)
button = Pin(22, Pin.IN, Pin.PULL_DOWN)
pen_down = False

# SECTION - FUNCTIONS

def setUpPotPins():
    right_potentiometer = ADC(Pin(26))
    left_potentiometer = ADC(Pin(27))
    return left_potentiometer, right_potentiometer
'''
def run_calibration(offset_shoulder, offset_elbow):
    shoulder_angle, elbow_angle = inverse_kinematics(0, 0)
    servo_shoulder_offset = float(offset_shoulder) - 75
    servo_elbow_offset = 150 - float(offset_elbow)
    return servo_shoulder_offset, servo_elbow_offset
    '''

def readRLInput(left_potentiometer, right_potentiometer):
    right_val = right_potentiometer.read_u16()
    left_val = left_potentiometer.read_u16()
    return right_val, left_val

def inverse_kinematics(Cx, Cy):
    # Code to calculate the angle for the shoulder and elbow servo motors
    Cx = (Cx/65535)*216 #Converting u-16 to paper scale values
    Cy = (Cy/65535)*279
    Ax = -50
    Ay = 139.5
    La = 155
    Lb = 155
    AC = math.sqrt((Ax-Cx)**2 + (Ay-Cy)**2)
    AbaseC = math.sqrt((Ax-Cx)**2 + Cy**2)
    BAC = math.acos((La**2 + AC**2 - Lb**2)/(2*La*AC))
    ACB = math.asin((La*math.sin(BAC))/Lb)
    YAC = math.acos((Ay**2 + AC**2 - AbaseC**2)/(2*Ay*AC))
    alpha_angle = math.degrees(BAC + YAC)
    beta_angle = math.degrees(BAC + ACB)
    return alpha_angle, beta_angle

def translate(angle):
    DEG = (PWM_MAX - PWM_MIN) / 180  # Value per degree of rotation
    angle = max(0, min(180, angle))  # Clamp angle to be between 0 and 180
    duty_value = int(angle * DEG + PWM_MIN)
    return duty_value


def lower_raise_pen():
    global pen_down  # Declare that we will use the global variable
    if button.value() == 1:
        pen_down = not pen_down
        if pen_down:
            pen_servo.duty_u16(translate(0))
        else:
            pen_servo.duty_u16(translate(30))  # Lower pen
        


# SECTION - MAIN PROGRAM

#servo_shoulder_offset, servo_elbow_offset = run_calibration(offset_shoulder, offset_elbow)
left_poten, right_poten = setUpPotPins()

try:
    while True:
        left, right = readRLInput(left_poten, right_poten)
        shoulder_angle, elbow_angle = inverse_kinematics(left, right)
        shoulder_servo.duty_u16(translate(shoulder_angle-75))
        elbow_servo.duty_u16(translate(150 -elbow_angle))
        lower_raise_pen()
        time.sleep(0.1)  # 100ms delay
finally:
    shoulder_servo.deinit()
    elbow_servo.deinit()
    pen_servo.deinit()

