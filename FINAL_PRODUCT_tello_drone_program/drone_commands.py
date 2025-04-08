from djitellopy import tello
import matrix_control as mx
import main as m
import time

# Initialize the drone
Drone = tello.Tello()

def try_display_matrix(matrix_command):
    if m.has_matrix_screen:
        try:
            matrix_command()  # Try to execute the matrix command
        except Exception as e:
            print(f"Error displaying matrix: {e}")

# Movement functions for the drone with matrix checks
def Go_up(distance):
    Drone.move_up(distance)
    try_display_matrix(mx.up_matrix)

def Go_down(distance):
    Drone.move_down(distance)
    try_display_matrix(mx.down_matrix)

def Go_left(distance):
    Drone.move_left(distance)
    try_display_matrix(mx.left_matrix)

def Go_right(distance):
    Drone.move_right(distance)
    try_display_matrix(mx.right_matrix)

def Go_forward(distance):
    Drone.move_forward(distance)
    try_display_matrix(mx.matrix_o)

def Go_back(distance):
    Drone.move_back(distance)
    try_display_matrix(mx.matrix_x)

# Rotation functions
def Rotate_right():
    Drone.rotate_clockwise(90)

def Rotate_left():
    Drone.rotate_counter_clockwise(90)

def Spin_clockwise(speed):
    Drone.rotate_clockwise(speed)

# Flip actions with matrix feedback
def Frontflip():
    try_display_matrix(mx.smile_matrix)
    Drone.flip_forward()
    

def Backflip():
    try_display_matrix(mx.smile_matrix)
    Drone.flip_back()

# Takeoff and landing with matrix feedback
def Takingoff():
    Drone.takeoff()
    try_display_matrix(mx.take_off_matrix)

def LandingSequence():
    try_display_matrix(mx.emergency_matrix)
    print("Landing...")
    Drone.land()
    time.sleep(3)

# Testing sequence
def Testing():
    try_display_matrix(mx.emergency_matrix)
    Drone.turn_motor_on()
    time.sleep(5)
    Drone.turn_motor_off()
    print("Test done")
