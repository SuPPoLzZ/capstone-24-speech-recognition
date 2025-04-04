from djitellopy import tello
import time
import matrix_control as mx

# === DRONE_CONTROL_FUNCTIONS ===
Drone = tello.Tello()

# Movement variables
moveSpeed, liftSpeed, rotationSpeed = 25, 25, 50

def Go_left():
    return Drone.move_left(moveSpeed) and mx.left_matrix()

def Go_right():
    return Drone.move_right(moveSpeed) and mx.right_matrix()

def Go_forward():
    return Drone.move_forward(moveSpeed)

def Go_back():
    return Drone.move_back(moveSpeed)

def Go_up():
    return Drone.move_up(liftSpeed) and mx.up_matrix()

def Go_down():
    return Drone.move_down(liftSpeed) and mx.down_matrix()

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

def amin():
    Drone.takeoff()
    time.sleep(3)
    Drone.rotate_clockwise(360)
    time.sleep(3)
    Drone.rotate_counter_clockwise(360)
    time.sleep(5)
    Drone.flip_forward()
    time.sleep(3)
    Drone.land()


def Testing():
    mx.emergency_matrix()
    time.sleep(1)
    mx.up_matrix()
    time.sleep(1)
    mx.down_matrix()
    time.sleep(1)
    mx.left_matrix()
    time.sleep(1)
    mx.right_matrix()
    time.sleep(1)
    mx.smile_matrix()
    time.sleep(1)
    Drone.turn_motor_on()
    mx.emergency_matrix()
    time.sleep(10)
    Drone.turn_motor_off()
    print("Test done")
    return