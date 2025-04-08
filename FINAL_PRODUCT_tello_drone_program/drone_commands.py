from djitellopy import tello
import time
import matrix_control as mx

# === DRONE_CONTROL_FUNCTIONS ===
Drone = tello.Tello()

# Movement variables
moveSpeed, liftSpeed, rotationSpeed = 20, 20, 90

# ============SHOWROOM COMMANDS=============

def Go_left():
    try:
        mx.left_matrix()
    finally:
        return Drone.move_left(moveSpeed)

def Go_right():
    try:
        mx.right_matrix()
    finally:
        return Drone.move_right(moveSpeed)

def Go_forward():
    return Drone.move_forward(moveSpeed)

def Go_back():
    return Drone.move_back(moveSpeed)

def Go_up():
    try:
        mx.up_matrix()
    finally:
        return Drone.move_up(liftSpeed)

def Go_down():
    try:
        mx.down_matrix()
    finally:
        return Drone.move_down(liftSpeed)

def Rotate_right():
    return Drone.rotate_clockwise(rotationSpeed)

def Rotate_left():
    return Drone.rotate_counter_clockwise(rotationSpeed)

def Spin_clockwise():
    return Drone.rotate_clockwise(rotationSpeed*4)

def Spin_counter():
    return Drone.rotate_counter_clockwise(rotationSpeed*4)

def Frontflip():
    return Drone.flip_forward()

def Backflip():
    return Drone.flip_back()

def LandingSequence():
    print("Landing...")
    Drone.land()
    time.sleep(3)
    mx.emergency_matrix()
    return

def Takingoff():
    return Drone.takeoff() and mx.take_off_matrix()

def Testing():
    Drone.turn_motor_on()
    time.sleep(5)
    Drone.turn_motor_off()
    print("Test done")