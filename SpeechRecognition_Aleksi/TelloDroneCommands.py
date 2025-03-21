from djitellopy import tello
import time

# === DRONE_CONTROL_FUNCTIONS ===
Drone = tello.Tello()

# Movement variables
moveSpeed, liftSpeed, rotationSpeed = 25, 25, 50

def go_left():
    return Drone.move_left(moveSpeed)
def go_right():
    return Drone.move_right(moveSpeed)
def go_forward():
    return Drone.move_forward(moveSpeed)
def go_back():
    return Drone.move_back(moveSpeed)
def go_up():
    return Drone.move_up(liftSpeed)
def go_down():
    return Drone.move_down(liftSpeed)
def rotate_right():
    return Drone.rotate_clockwise(rotationSpeed)
def rotate_left():
    return Drone.rotate_counter_clockwise(rotationSpeed)
def spin_clockwise():
    return Drone.rotate_clockwise(rotationSpeed*4)
def spin_counter():
    return Drone.rotate_counter_clockwise(rotationSpeed*4)
def frontflip():
    return Drone.flip_forward()
def backflip():
    return Drone.flip_back()

def LandingSequence():
    print("Landing...")
    Drone.land()
    time.sleep(3)

def Takingoff():
    return Drone.takeoff()

def Testing():
    Drone.turn_motor_on()
    time.sleep(10)
    Drone.turn_motor_off()
    print("Test done")