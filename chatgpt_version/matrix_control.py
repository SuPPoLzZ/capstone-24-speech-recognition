import time
from djitellopy import Tello

# === Drone Setup === #
tello = Tello()

# === Matrix Patterns === #
matrix_o = "0pppppp0"+"p000000p"+"p000000p"+"p000000p"+"p000000p"+"p000000p"+"p000000p"+"0pppppp0"
matrix_x = "p000000p"+"0p0000p0"+"00p00p00"+"000pp000"+"000pp000"+"00p00p00"+"0p0000p0"+"p000000p"

matrix_up = "bbbrrbbb"+"bbrrrrbb"+"brrrrrrb"+"bbbrrbbb"+"bbbrrbbb"+"bbbrrbbb"+"bbbrrbbb"+"bbbrrbbb"
matrix_down = "bbbrrbbb"+"bbbrrbbb"+"bbbrrbbb"+"bbbrrbbb"+"bbbrrbbb"+"brrrrrrb"+"bbrrrrbb"+"bbbrrbbb"
matrix_left = "bbbbbbbb"+"bbrbbbbb"+"brrbbbbb"+"rrrrrrrr"+"rrrrrrrr"+"brrbbbbb"+"bbrbbbbb"+"bbbbbbbb"
matrix_right = "bbbbbbbb"+"bbbbbrbb"+"bbbbbrrb"+"rrrrrrrr"+"rrrrrrrr"+"bbbbbrrb"+"bbbbbrbb"+"bbbbbbbb"

matrix_emergency = "pprrrrpp"+"prrpprrp"+"rrrpprrr"+"rrrpprrr"+"rrrpprrr"+"rrrrrrrr"+"prrpprrp"+"pprrrrpp"
matrix_emergency_inverted = "rrpppprr"+"rpprrppr"+"ppprrppp"+"ppprrppp"+"ppprrppp"+"pppppppp"+"rpprrppr"+"rrpppprr"
matrix_smile = "00000000"+"0pp00pp0"+"0pp00pp0"+"00000000"+"p000000p"+"0p0000p0"+"00pppp00"+"00000000"

matrix_flip_forward = "00000000"+"0pppppp0"+"p000000p"+"p000000p"+"p000000p"+"0p0000p0"+"00pppp00"+"00000000"
matrix_flip_backward = "00000000"+"0pppppp0"+"p000000p"+"p000000p"+"p000000p"+"p000000p"+"0pppppp0"+"00000000"
matrix_flip_left = "00000000"+"0pppppp0"+"0p0000p0"+"p000000p"+"p000000p"+"0p0000p0"+"0pppppp0"+"00000000"
matrix_flip_right = "00000000"+"0pppppp0"+"0p0000p0"+"p000000p"+"p000000p"+"0p0000p0"+"0pppppp0"+"00000000"

matrix_rotate_left = "00ppp000"+"0p000000"+"p0000ppp"+"p0000pp0"+"p0000p0p"+"p000000p"+"0p0000p0"+"00pppp00"
matrix_rotate_right = "00pppp00"+"000000p0"+"ppp0000p"+"0pp0000p"+"p0p0000p"+"p000000p"+"0p0000p0"+"00pppp00"

# === Core Matrix Sender === #
def send_led_matrix_command(matrix_pattern):
    command = f"EXT mled g {matrix_pattern}"
    tello.send_control_command(command)
    print(f"[Matrix] Sent: {command}")

def send_scroll_text_command(text_matrix):
    matrix_pattern = ''.join(text_matrix)
    send_led_matrix_command(matrix_pattern)

# === Matrix Display Functions === #
def emergency_matrix():
    for _ in range(4):
        send_led_matrix_command(matrix_emergency)
        tello.send_expansion_command("led 255 0 0")
        time.sleep(1)
        send_led_matrix_command(matrix_emergency_inverted)
        tello.send_expansion_command("led 255 255 255")
        tello.send_expansion_command("led 0 0 0")
        time.sleep(1)

def take_off_matrix():
    tello.send_expansion_command("led 0 255 0")
    send_led_matrix_command(matrix_smile)

def smile_matrix():
    send_led_matrix_command(matrix_smile)

# === Directional Matrices === #
def up_matrix(): send_led_matrix_command(matrix_up)
def down_matrix(): send_led_matrix_command(matrix_down)
def left_matrix(): send_led_matrix_command(matrix_left)
def right_matrix(): send_led_matrix_command(matrix_right)

# === Flip & Rotation Matrices === #
def flip_forward_matrix(): send_led_matrix_command(matrix_flip_forward)
def flip_backward_matrix(): send_led_matrix_command(matrix_flip_backward)
def flip_left_matrix(): send_led_matrix_command(matrix_flip_left)
def flip_right_matrix(): send_led_matrix_command(matrix_flip_right)

def rotate_left(): send_led_matrix_command(matrix_rotate_left)
def rotate_right(): send_led_matrix_command(matrix_rotate_right)

# === Feedback Matrix === #
def o_matrix(): send_led_matrix_command(matrix_o)
def x_matrix(): send_led_matrix_command(matrix_x)


# === Debugging Preview === #
if __name__ == "__main__":
    tello.connect()
    print(f"Battery: {tello.get_battery()}%")
    print("Running matrix pattern test...")

    pattern_list = [
        take_off_matrix,
        flip_forward_matrix,
        flip_backward_matrix,
        flip_left_matrix,
        flip_right_matrix,
        up_matrix,
        down_matrix,
        left_matrix,
        right_matrix,
        emergency_matrix,
        rotate_left,
        smile_matrix,
        rotate_right,
    ]

    for func in pattern_list:
        print(f"Running: {func.__name__}")
        func()
        time.sleep(1)
