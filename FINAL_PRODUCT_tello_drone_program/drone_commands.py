import time
from djitellopy import tello
import main as m
import matrix_control as mx

# Initialize the drone
Drone = tello.Tello()

def DefineMovements():
    global moveDistance, rotation
    moveDistance = SetNewMovement()
    rotation = SetNewRotation()
    
def SetNewMovement():
    movementDef = 50
    newMovement = input("Enter the distance to move(range 20-500, default 50):")
    if newMovement in range(20, 501):
        print(f"MoveDistance set to {newMovement}")
        return newMovement
    else:
        print("Outside of range, using default")
        return movementDef

def SetNewRotation():
    rotationDef = 90
    newRotation = input("\nEnter the new angle to rotate(range 1-360, default 90):")
    if newRotation in range(1, 361):
        print(f"Rotation set to {newRotation}")
        return newRotation
    else:
        print("Outside of range, using default")
        return rotationDef


def try_display_matrix(matrix_command):
    if m.has_matrix_screen == True:
        try:
            matrix_command()  # Try to execute the matrix command
        except Exception as e:
            print(f"Error displaying matrix: {e}")
    else:
        pass

# Movement functions for the drone with matrix checks
def Go_up():
    print("Going up")
    Drone.move_up(moveDistance)
    try_display_matrix(mx.up_matrix)

def Go_down():
    print("Going down")
    Drone.move_down(moveDistance)
    try_display_matrix(mx.down_matrix)

def Go_left():
    print("Going left")
    Drone.move_left(moveDistance)
    try_display_matrix(mx.left_matrix)

def Go_right():
    print("Going right")
    Drone.move_right(moveDistance)
    try_display_matrix(mx.right_matrix)

def Go_forward():
    print("Going forward")
    Drone.move_forward(moveDistance)
    try_display_matrix(mx.matrix_o)

def Go_back():
    print("Going back")
    Drone.move_back(moveDistance)
    try_display_matrix(mx.matrix_x)

# Rotation functions
def Rotate_right():
    print("rotating right")
    Drone.rotate_clockwise(rotation)

def Rotate_left():
    print("rotating left")
    Drone.rotate_counter_clockwise(rotation)

def Spin_clockwise():
    print("spinning clockwise")
    Drone.rotate_clockwise(rotation*4)

# Flip actions with matrix feedback
def Frontflip():
    print("frontflip")
    try_display_matrix(mx.smile_matrix)
    Drone.flip_forward()

def Backflip():
    print("backflip")
    try_display_matrix(mx.smile_matrix)
    Drone.flip_back()

# Takeoff and landing with matrix feedback
def Takingoff():
    print("Taking off")
    Drone.takeoff()
    try_display_matrix(mx.take_off_matrix)

def LandingSequence():
    try_display_matrix(mx.emergency_matrix)
    print("Landing...")
    Drone.land()
    time.sleep(3)

# Testing sequence
def Testing():
    print("testing")
    try_display_matrix(mx.emergency_matrix)
    Drone.turn_motor_on()
    time.sleep(5)
    Drone.turn_motor_off()
    print("Test done")