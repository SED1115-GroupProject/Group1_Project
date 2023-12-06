import time
import math
from machine import Pin, PWM, ADC

# Game introduction and calibration setup:
print("Welcome to the etch a sketch game")
print("Use the right potentiometer to control Y and the left potentiometer to control X")
print("Push the middle button to raise and lower the pen")


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

# Initialize the button
button = Pin(22, Pin.IN, Pin.PULL_DOWN)
pen_down = False

# SECTION - FUNCTIONS

def setUpPotPins(): # Aarani
    left_potentiometer = ADC(Pin(27))
    right_potentiometer = ADC(Pin(26))
    return left_potentiometer, right_potentiometer
'''
def run_calibration(offset_shoulder, offset_elbow):
    shoulder_angle, elbow_angle = inverse_kinematics(0, 0)
    servo_shoulder_offset = float(offset_shoulder) - 75
    servo_elbow_offset = 150 - float(offset_elbow)
    return servo_shoulder_offset, servo_elbow_offset
    '''

# Function to read the input values from potentiometers
def readRLInput(left_potentiometer, right_potentiometer): # Aarani
    # Read the analog input values from the left and right potentiometers
    left_val = left_potentiometer.read_u16()
    right_val = right_potentiometer.read_u16()
    # Return the read values from both potentiometers
    return left_val, right_val

def inverse_kinematics(Cx, Cy): # Ennio
    '''
    Function to calculate the angle for the shoulder and elbow servo motors
    Cx and Cy are the coordinates of the pen tip in the coordinate system of the arm. 
    Ax and Ay are the coordinates of the shoulder joint. La and Lb are the lengths of the upper and lower arm respectively.
    AC is the distance between the shoulder joint and the pen tip. AbaseC is the distance between the shoulder joint and the pen tip projected onto the x-axis.
    BAC is the angle between the upper arm and the line connecting the shoulder joint and the pen tip. ACB is the angle between the upper arm and the lower arm.
    YAC is the angle between the upper arm and the y-axis.
    alpha_angle is the angle between the upper arm and the x-axis. beta_angle is the angle between the lower arm and the x-axis.
    '''

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

# Function to translate the angle to a duty cycle value
def translate(angle): # Nick
    DEG = (PWM_MAX - PWM_MIN) / 180  # Value per degree of rotation
    angle = max(0, min(180, angle))  # Clamp angle to be between 0 and 180
    duty_value = int(angle * DEG + PWM_MIN)
    return duty_value

# Function to raise and lower the pen
def lower_raise_pen(): # Gemma
    global pen_down  
    if button.value() == 1: # If the button is pressed
        time.sleep_ms(100) # Pause between button presses to debounce
        pen_down = not pen_down
        if pen_down:
            pen_servo.duty_u16(translate(0))
        else:
            pen_servo.duty_u16(translate(30))  # Lower pen
        


# SECTION - MAIN PROGRAM 

# Initialize the potentiometers
left_poten, right_poten = setUpPotPins()


try: # Shared
    while True:
        left, right = readRLInput(left_poten, right_poten) # Read the input values from the potentiometers
        shoulder_angle, elbow_angle = inverse_kinematics(left, right) # Calculate the angles for the shoulder and elbow servo motors
        shoulder_servo.duty_u16(translate(shoulder_angle-75)) # Set the duty cycle for the shoulder servo motor with offset
        elbow_servo.duty_u16(translate(150 -elbow_angle))   # Set the duty cycle for the elbow servo motor with offset
        lower_raise_pen()
        time.sleep(0.1)  # 100ms delay
finally:
    # De-initialize the servo motors
    shoulder_servo.deinit()
    elbow_servo.deinit()
    pen_servo.deinit()
