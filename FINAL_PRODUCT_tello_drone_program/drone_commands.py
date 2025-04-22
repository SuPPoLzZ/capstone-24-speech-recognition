import time
from djitellopy import tello
import matrix_control as mx

# Initialize the drone
Drone = tello.Tello()

def DefineMovements():
    SetMatrixStatus()
    global moveDistance
    global rotation
    moveDistance = SetNewMovement()
    rotation = SetNewRotation()

def SetMatrixStatus():
    # Flag to specify if the drone has a matrix screen 
    global has_matrix_screen
    matrix_Choice = input("Does the drone have a matrix screen? (y/n): ").strip().lower()
    if matrix_Choice == 'y':
        has_matrix_screen = True
    else:
        has_matrix_screen = False

def SetNewMovement():
    movementDef = 50
    newMovement = input("Enter the distance to move.\n(range 20-500, default 50):")
    try:
        if int(newMovement) in range(20, 501):
            print(f"MoveDistance set to {newMovement}")
            return newMovement
        else:
            print("Outside of range, using default")
            return movementDef
    except:
        print("Error in input value, Input Not INT")
    finally:
        print(f"Using the default movement, {movementDef}.")
        return movementDef

def SetNewRotation():
    rotationDef = 90
    newRotation = input("\nEnter the new angle to rotate.\n(range 1-360, default 90):")
    try:
        if int(newRotation) in range(1, 361):
            print(f"Rotation set to {newRotation}")
            return newRotation
        else:
            print("Outside of range, using default")
            return rotationDef
    except:
        print("Error in input value, Input Not INT")
    finally:
        print(f"Using the default rotation, {rotationDef}")
        return rotationDef

def try_display_matrix(matrix_command):
    if has_matrix_screen == True:
        try:
            matrix_command()  # Try to execute the matrix command
        except Exception as e:
            print(f"Error displaying matrix: {e}")
    else:
        pass

# Movement functions for the drone with matrix checks
def Go_up():
    print(f"Going up by {moveDistance}")
    try_display_matrix(mx.up_matrix)
    Drone.move_up(moveDistance)

def Go_down():
    print(f"Going down by {moveDistance}")
    try_display_matrix(mx.down_matrix)
    Drone.move_down(moveDistance)

def Go_left():
    print(f"Going left by {moveDistance}")
    try_display_matrix(mx.left_matrix)
    Drone.move_left(moveDistance)

def Go_right():
    print(f"Going right by {moveDistance}")
    try_display_matrix(mx.right_matrix)
    Drone.move_right(moveDistance)

def Go_forward():
    print(f"Going forward by {moveDistance}")
    try_display_matrix(mx.matrix_o)
    Drone.move_forward(moveDistance)    

def Go_back():
    print(f"Going back by {moveDistance}")
    try_display_matrix(mx.matrix_x)
    Drone.move_back(moveDistance)

# Rotation functions
def Rotate_right():
    print(f"rotating right by {rotation}")
    Drone.rotate_clockwise(rotation)

def Rotate_left():
    print(f"rotating left by {rotation}")
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
    try_display_matrix(mx.take_off_matrix)
    Drone.takeoff()

def LandingSequence():
    print("Landing...")
    try_display_matrix(mx.emergency_matrix)
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