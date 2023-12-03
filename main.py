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
shoulder_servo = PWM(Pin(INSERT_PIN_NUMBER_HERE)) # GPIO0
elbow_servo = PWM(Pin(INSERT_PIN_NUMBER_HERE)) # GPIO1
pen_servo = PWM(Pin(INSERT_PIN_NUMBER_HERE)) # GPIO 2
shoulder_servo.freq(50) 
elbow_servo.freq(50)
pen_servo.freq(50)


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

def translate(angle):
    '''
    Function to convert an angle in degrees to duty cycle value
    Input is a degree between 0 and 180
    Output is a value between 0 and 65535
    Alpha angle is shoulder
    Beta angle is elbow 
    '''
    MIN = 1638 # 0 degrees
    MAX = 8192 # 180 degrees
    DEG = (MAX - MIN) / 180 #Value per degree of rotation
    
    angle = max(0, min(180, angle)) # Clamp angle to be between 0 and 180
    duty_value = int(angle * DEG + MIN) 
    
    return duty_value

# def raise_lower_pen(is_pen_down):
import time 
from machine import Pin, PWM, ADC

servo_pin = Pin(2)  # Replace with the actual GPIO pin number
servo_pwm = PWM(servo_pin)    
pin = Pin(2, Pin.OUT)
pin.value(1)  # Set pin
servo = PWM(Pin(2))

sw5 = Pin(22, Pin.IN, Pin.PULL_UP) 
sw5 = Pin(22, Pin.IN, Pin.PULL_DOWN)

def raise_pen():
    pen_position = "up" 
        
def lower_pen():
    pen_position = "down"

    #write code to move the pen up and down
    # Simulate pin button press to raise the pen with the correct pin
    robotic_arm.raise_lower_pen_with_pin_button(pin_button_pressed=True, pin_number=22)

    # Simulate pin button press to lower the pen with the correct pin
    robotic_arm.raise_lower_pen_with_pin_button(pin_button_pressed=True, pin_number=22)

    # Simulate pin button press with an incorrect pin
    robotic_arm.raise_lower_pen_with_pin_button(pin_button_pressed=True, pin_number=22)

    # Simulate pin button not pressed
    robotic_arm.raise_lower_pen_with_pin_button(pin_button_pressed=False, pin_number=22)

    

# Code to control the elbow servo motor



# SECTION - MAIN PROGRAM
servo_shoulder_offset, servo_elbow_offset = run_calibration()
left_poten, right_poten = setUpPotPins()

while True:
    right, left = readRLInput(left_poten, right_poten)
    shoulder_angle, elbow_angle = inverse_kinematics(left, right)
    move_shoulder(shoulder_angle + servo_shoulder_offset)
    move_elbow(elbow_angle + servo_elbow_offset)

'''
Should the function calls be in a while loop so they run continuously until the user exits the program ???
'''
angle1 = translate(alpha_angle) # Call translate function to calculate PWM Value for alpha
angle2 = translate(beta_angle) # Call translate function to calculate PWM Value for beta 

shoulder_servo.duty_u16(angle1) # Pass the alpha duty value to the servo 1 using u16 method 
elbow_servo.duty_u16(angle2) # Pass the beta duty value to the servo 2 using u16 method 

print("duty value 1 =", angle1, "Duty value 2 =", angle2) # Print statement to monitor translated values 

