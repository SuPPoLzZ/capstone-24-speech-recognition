import time
from djitellopy import Tello

# Initialize the Tello object
tello = Tello()

# Connect to the Tello drone
#tello.connect()

#LED patterns 
matrix_o = "0pppppp0"+"p000000p"+"p000000p"+"p000000p"+"p000000p"+"p000000p"+"p000000p"+"0pppppp0"
matrix_x = "p000000p"+"0p0000p0"+"00p00p00"+"000pp000"+"000pp000"+"00p00p00"+"0p0000p0"+"p000000p"

matrix_up = "bbbrrbbb"+"bbrrrrbb"+"brrrrrrb"+"bbbrrbbb"+"bbbrrbbb"+"bbbrrbbb"+"bbbrrbbb"+"bbbrrbbb"
matrix_down ="bbbrrbbb"+"bbbrrbbb"+"bbbrrbbb"+"bbbrrbbb"+"bbbrrbbb"+"brrrrrrb"+"bbrrrrbb"+"bbbrrbbb"
matrix_left ="bbbbbbbb"+"bbrbbbbb"+"brrbbbbb"+"rrrrrrrr"+"rrrrrrrr"+"brrbbbbb"+"bbrbbbbb"+"bbbbbbbb"
matrix_right = "bbbbbbbb"+"bbbbbrbb"+"bbbbbrrb"+"rrrrrrrr"+"rrrrrrrr"+"bbbbbrrb"+"bbbbbrbb"+"bbbbbbbb"

matrix_emergency= "pprrrrpp"+"prrpprrp"+"rrrpprrr"+"rrrpprrr"+"rrrpprrr"+"rrrrrrrr"+"prrpprrp"+"pprrrrpp"  
matrix_emergency_inverted ="rrpppprr"+"rpprrppr"+"ppprrppp"+"ppprrppp"+"ppprrppp"+"pppppppp"+"rpprrppr"+"rrpppprr" 
matrix_smile ="00000000"+"0pp00pp0"+"0pp00pp0"+"00000000"+"p000000p"+"0p0000p0"+"00pppp00"+"00000000"

matrix_flip_backward = "00000000" + "0pppppp0" + "p000000p" + "p000000p" + "p000000p" + "p000000p" + "0pppppp0" + "00000000"
matrix_flip_forward = "00000000" + "0pppppp0" + "p000000p" + "p000000p" + "p000000p" + "0p0000p0" + "00pppp00" + "00000000"
matrix_flip_left = "00000000" + "0pppppp0" + "0p0000p0" + "p000000p" + "p000000p" + "0p0000p0" + "0pppppp0" + "00000000"
matrix_flip_right = "00000000" + "0pppppp0" + "0p0000p0" + "p000000p" + "p000000p" + "0p0000p0" + "0pppppp0" + "00000000"

matrix_rotate_left ="00ppp000"+"0p000000"+"p0000ppp"+"p0000pp0"+"p0000p0p"+"p000000p"+"0p0000p0"+"00pppp00"


# Function to send the LED matrix command
def send_led_matrix_command(matrix_pattern):
    # Send the 'EXT mled g' command to control the LED matrix IT HAS TO BE g documentation said that its color 'rgb' but only works when g is specified
    command = f"EXT mled g {matrix_pattern}"
    tello.send_control_command(command)
    print(f"Sent command: {command}")


def send_scroll_text_command(text_matrix):
    # Join the text matrix into a single string to send to the drone
    matrix_pattern = ''.join(text_matrix)
    send_led_matrix_command(matrix_pattern)


def emergency_matrix():
    i=0
    while i < 4:
        send_led_matrix_command(matrix_emergency)  # Set matrix to display number 2
        tello.send_expansion_command("led 255 0 0")
        time.sleep(1) 
        send_led_matrix_command(matrix_emergency_inverted)  # Set matrix to display number 2
        tello.send_expansion_command("led 255 255 255")
        tello.send_expansion_command("led 0 0 0")
        i += 1


def take_off_matrix():
    tello.send_expansion_command("led 0 255 0")
    send_led_matrix_command(matrix_smile)



def scroll_smile():
    # Define the 8x8 matrix for each letter in "SMILE"
    smile_text = {
        'S': [
            "00rrr000",
            "0r000r00",
            "0r000000",
            "00rrr000",
            "00000r00",
            "0r000r00",
            "00rrr000",
            "00000000"
        ],
        'M': [
            "0r000r00",
            "0rr0rr00",
            "0r0r0r00",
            "0r0r0r00",
            "0r000r00",
            "0r000r00",
            "0r000r00",
            "0r000r00",
        ],
        'I': [
            "00rrrrr0",
            "0000r000",
            "0000r000",
            "0000r000",
            "0000r000",
            "0000r000",
            "0000r000",
            "00rrrrr0"
        ],
        'L': [
            "p0000000",
            "p0000000",
            "p0000000",
            "p0000000",
            "p0000000",
            "p0000000",
            "pppppppp",
            "00000000"
        ],
        'E': [
            "0ppppp0p",
            "0pp00000",
            "0ppppp00",
            "0p000000",
            "0ppppp0p",
            "00000000",
            "0ppppp00",
            "00000000"
        ]
    }

    # Concatenate the letter matrices to form the word "SMILE"
    smile_matrix = []
    for letter in "SMILE":
        smile_matrix.extend(smile_text[letter])  # Add each letter's 8x8 grid

    # We will scroll this matrix to the left
    total_width = len(smile_matrix[0])  # Total width of "SMILE"
    for shift in range(total_width + 8):  # Shift to the end (total length + 8 for buffer)
        shifted_pattern = []
        for row in smile_matrix:
            shifted_row = row[shift % total_width:] + row[:shift % total_width]  # Shift each row
            shifted_pattern.append(shifted_row)
        
        # Convert the list into a single string for the LED matrix command
        matrix_pattern = ''.join(shifted_pattern)
        
        # Send the updated pattern to the drone
        send_scroll_text_command(matrix_pattern)
        
        time.sleep(0.3)  # Adjust delay for scrolling speed

def smile_matrix():
    send_led_matrix_command(matrix_smile)
    
#directional matrix
def up_matrix():
    send_led_matrix_command(matrix_up)

def down_matrix():
    send_led_matrix_command(matrix_down)

def left_matrix():
    send_led_matrix_command(matrix_left)

def right_matrix():
    send_led_matrix_command(matrix_right)

def flip_forward_matrix():
    send_led_matrix_command(matrix_flip_forward)

def flip_backward_matrix():
    send_led_matrix_command(matrix_flip_backward)

def flip_left_matrix():
    send_led_matrix_command(matrix_flip_left)   

def flip_right_matrix():
    send_led_matrix_command(matrix_flip_right)  

def rotate_left():
    send_led_matrix_command(matrix_rotate_left)
    



#debugging 
if __name__ == "__main__":
    # Connect to the drone
    tello.connect()
    print(f"Battery: {tello.get_battery()}%")

    # List of matrix functions to run
    matrix_functions = [
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
        smile_matrix,
        rotate_left
    ]

    for matrix_func in matrix_functions:
        matrix_func()  
        time.sleep(1)