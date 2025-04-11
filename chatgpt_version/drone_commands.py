from djitellopy import tello
import matrix_control as mx
import time
import main as m

# === Drone Setup === #
Drone = tello.Tello()

# === Configs (can be updated externally from main) === #
distance = m.distance
elevation = m.elevation
matrix_enabled = m.matrix

# === Matrix Display Wrapper === #
def try_display_matrix(matrix_func):
    if matrix_enabled:
        try:
            matrix_func()
        except Exception as e:
            print(f"[Matrix Error] {e}")
    else:
        print("Matrix not enabled — skipping visual.")

# === Movement Commands === #
def Go_up():
    try_display_matrix(mx.up_matrix)
    Drone.move_up(elevation)

def Go_down():
    try_display_matrix(mx.down_matrix)
    Drone.move_down(elevation)

def Go_left():
    try_display_matrix(mx.left_matrix)
    Drone.move_left(distance)

def Go_right():
    try_display_matrix(mx.right_matrix)
    Drone.move_right(distance)

def Go_forward():
    try_display_matrix(mx.o_matrix)
    Drone.move_forward(distance)

def Go_back():
    try_display_matrix(mx.x_matrix)
    Drone.move_back(distance)

# === Rotational Commands === #
def Rotate_right():
    Drone.rotate_clockwise(90)

def Rotate_left():
    Drone.rotate_counter_clockwise(90)

def Spin_clockwise(speed=100):
    try_display_matrix(mx.rotate_right)
    Drone.rotate_clockwise(speed)

def Spin_counter(speed=100):
    try_display_matrix(mx.rotate_left)
    Drone.rotate_counter_clockwise(speed)

# === Flip Commands === #
def Frontflip():
    try_display_matrix(mx.smile_matrix)
    Drone.flip_forward()

def Backflip():
    try_display_matrix(mx.smile_matrix)
    Drone.flip_back()

# === Takeoff & Landing === #
def Takingoff():
    try_display_matrix(mx.take_off_matrix)
    Drone.takeoff()

def LandingSequence():
    try_display_matrix(mx.emergency_matrix)
    print("Landing...")
    Drone.land()
    time.sleep(3)

# === Testing Demo === #
def Testing():
    Drone.turn_motor_on()

    matrix_sequence = [
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

    if matrix_enabled:
        for func in matrix_sequence:
            func()
            time.sleep(1)
    else:
        print("Matrix not enabled — skipping matrix test.")

    Drone.turn_motor_off()
    print("✅ Test complete.")
