import math

def inverse_kinematics(Cx, Cy):
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

def translate(angle):
    DEG = (8192 - 1638) / 180  # Value per degree of rotation
    angle = max(0, min(180, angle))  # Clamp angle to be between 0 and 180
    duty_value = int(angle * DEG + 1638)
    return duty_value