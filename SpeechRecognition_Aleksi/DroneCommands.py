from djitellopy import tello
import time

# === DRONE_CONTROL_FUNCTIONS ===
Drone = tello.Tello()

# Movement variables
moveSpeed, liftSpeed, rotationSpeed = 25, 25, 50

def Go_left():
    return Drone.move_left(moveSpeed)

def Go_right():
    return Drone.move_right(moveSpeed)

def Go_forward():
    return Drone.move_forward(moveSpeed)

def Go_back():
    return Drone.move_back(moveSpeed)

def Go_up():
    return Drone.move_up(liftSpeed)

def Go_down():
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
    return

def Takingoff():
    return Drone.takeoff()

def Testing():
    Drone.turn_motor_on()
    time.sleep(10)
    Drone.turn_motor_off()
    print("Test done")
    return