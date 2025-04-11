from djitellopy import tello
import matrix_control as mx
import main as m
import time

# Initialize the drone
Drone = tello.Tello()

distance = m.distance
elevation = m.elevation

def try_display_matrix(matrix_command):
    if m.has_matrix_screen:
        try:
            matrix_command()  # Try to execute the matrix command
        except Exception as e:
            print(f"Error displaying matrix: {e}")
    else:
        print("Matrix screen not available. Skipping matrix display.")

# Movement functions for the drone with matrix checks
def Go_up(elevation):
    try_display_matrix(mx.up_matrix)
    Drone.move_up(elevation)
    

def Go_down(elevation):
    try_display_matrix(mx.down_matrix)
    Drone.move_down(elevation)

def Go_left(distance):
    try_display_matrix(mx.left_matrix)
    Drone.move_left(distance)

def Go_right(distance):
    try_display_matrix(mx.right_matrix)
    Drone.move_right(distance)
    

def Go_forward(distance):
    try_display_matrix(mx.matrix_o)
    Drone.move_forward(distance)
    

def Go_back(distance):
    try_display_matrix(mx.matrix_x)
    Drone.move_back(distance)

# Rotation functions
def Rotate_right():
    Drone.rotate_clockwise(90)

def Rotate_left():
    Drone.rotate_counter_clockwise(90)

def Spin_clockwise(speed):
    Drone.rotate_clockwise(speed)

def Spin_counter(speed):
    Drone.rotate_counter_clockwise(speed)

# Flip actions with matrix feedback
def Frontflip():
    try_display_matrix(mx.smile_matrix)
    Drone.flip_forward()
    

def Backflip():
    try_display_matrix(mx.smile_matrix)
    Drone.flip_back()

# Takeoff and landing with matrix feedback
def Takingoff():
    try_display_matrix(mx.take_off_matrix)
    Drone.takeoff()

def LandingSequence():
    try_display_matrix(mx.emergency_matrix)
    print("Landing...")
    Drone.land()
    time.sleep(3)

# Testing sequence
def Testing():

    Drone.turn_motor_on()
     # List of matrix functions to run
    matrix_functions = [
        mx.take_off_matrix,
        mx.flip_forward_matrix,
        mx.flip_backward_matrix,
        mx.flip_left_matrix,
        mx.flip_right_matrix,
        mx.up_matrix,
        mx.down_matrix,
        mx.left_matrix,
        mx.right_matrix,
        mx.emergency_matrix,
        mx.rotate_left,
        mx.smile_matrix,
        mx.rotate_left,
        mx.rotate_right,
    ]

    for matrix_func in matrix_functions:
        matrix_func()  
        time.sleep(1)

    
    Drone.turn_motor_off()
    print("Test done")
