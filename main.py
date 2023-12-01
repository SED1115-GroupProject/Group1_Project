# SECTION - Import necessary modules
import time 
import math
from classes import Pin, PWM, ADC

#Prints welcome to the game: 
print("welcome to the etch a sketch game")
print("Use the right potentiometer to control Y and the left potentiometer to control X")
print("Use the middle button to raise and lower the pen")

# SECTION - Define global variables

def setUpPotPins():
    right_potentiometer = ADC(0)
    left_potentiometer = ADC(1)
    return left_potentiometer, right_potentiometer

# SECTION - Define functions

def readRLInput(left_potentiometer,right_potentiometer):       
    right_val = right_potentiometer.read_u16()
    left_val = left_potentiometer.read_u16()

    return right_val, left_val

left_poten,right_poten = setUpPotPins()
while True:

    right,left = readRLInput(left_poten,right_poten)
    print(right,left)
    time.sleep(0.1) #100ms delay
    


# SECTION - Define functions

#def move_shoulder(angle):
    #Code to control the shoulder servo motor 

#def move_elbow(angle):
    #Code to control the elbow servo motor

#def raise_lower_pen(is_pen_down):
    #Code to raise or lower the pen servo motor 
    #is_pen_down could be a boolean variable where True means the pen is down and False means the pen in up.

#def get_x_potentiometer_value():
    #Code to read input for X-axis
    #ADC to read analog value from potentiometer

#def get_y_potentiometer_value():
    #Code to read input for Y-axis
    #ADC to read analog value from potentiometer

# Calibration Function
#def calibrate():

    
# Inverse Kinematics Function
def inverse_kinematics(Cx, Cy):
    #Code to calculate the angle for the shoulder and elbow servo motors
    #return shoulder_angle, elbow_angle
    Ax = -50
    Ay = 139.5
    La = 155
    Lb = 155
    AC = math.sqrt((Ax-Cx)**2 + (Ay-Cy)**2)
    AbaseC = math.sqrt((Ax-Cx)**2 + Cy**2)
    BAC = math.acos((La**2 + AC**2 - Lb**2)/(2*La*AC))
    ACB = math.asin((La*math.sin(BAC))/Lb)
    YAC = math.acos((Ay**2 + AC**2 - AbaseC**2)/(2*Ay*AC))
    alpha = math.degrees(BAC + YAC)
    beta = math.degrees(BAC + ACB)
    return alpha, beta

# Calibration offset
shoulder_angle, elbow_angle = inverse_kinematics(0, 0)
servo_shoulder_offset = shoulder_angle - 75
servo_elbow_offset = 150- elbow_angle
