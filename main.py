# SECTION - Import necessary modules
import time
import math
from classes import Pin, PWM, ADC

# Game introduction and calibration setup:
print("welcome to the etch a sketch game")
print("Use the right potentiometer to control Y and the left potentiometer to control X")
print("Use the middle button to raise and lower the pen")
time.sleep(5)
offset_shoulder = input("Enter the offset for the shoulder servo motor: ")
offset_elbow = input("Enter the offset for the elbow servo motor: ")
time.sleep(5)
print("Calibration complete")

# SECTION - GLOBAL VARIABLES

# Constants for PWM range
PWM_MIN = INSERT_MIN_PWM_VALUE_HERE
PWM_MAX = INSERT_MAX_PWM_VALUE_HERE

# Initialize the servo motors
shoulder_servo = PWM(Pin(INSERT_PIN_NUMBER_HERE))
elbow_servo = PWM(Pin(INSERT_PIN_NUMBER_HERE))
pen_servo = PWM(Pin(INSERT_PIN_NUMBER_HERE))


def setUpPotPins():
    right_potentiometer = ADC(Pin(26))
    left_potentiometer = ADC(Pin(27))
    return left_potentiometer, right_potentiometer

# SECTION - FUNCTIONS

# Calibration offset function
def run_calibration(offset_shoulder, offset_elbow):
    shoulder_angle, elbow_angle = inverse_kinematics(0, 0)
    servo_shoulder_offset = shoulder_angle - offset_shoulder
    servo_elbow_offset = offset_elbow - elbow_angle
    return servo_shoulder_offset, servo_elbow_offset

# This function reads the input from the potentiometers
def readRLInput(left_potentiometer, right_potentiometer):
    right_val = right_potentiometer.read_u16()
    left_val = left_potentiometer.read_u16()
    return right_val, left_val



# Inverse Kinematics Function
def inverse_kinematics(Cx, Cy):
    # Code to calculate the angle for the shoulder and elbow servo motors
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

# Function to control the shoulder servo motor
# def move_shoulder(angle):


# Function to control the elbow servo motor
# def move_elbow(angle):

# def raise_lower_pen(is_pen_down):
# Code to control the elbow servo motor



# SECTION - MAIN PROGRAM
servo_shoulder_offset, servo_elbow_offset = run_calibration()
left_poten, right_poten = setUpPotPins()

while True:
    right, left = readRLInput(left_poten, right_poten)
    shoulder_angle, elbow_angle = inverse_kinematics(left, right)
    move_shoulder(shoulder_angle + servo_shoulder_offset)
    move_elbow(elbow_angle + servo_elbow_offset)
    
