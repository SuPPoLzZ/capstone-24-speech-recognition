import time
from djitellopy import Tello

# Initialize the Tello object
tello = Tello()

# Connect to the Tello drone
tello.connect()

# Function to send the LED matrix command
def send_led_matrix_command(matrix_pattern):
    # Send the 'EXT mled g' command to control the LED matrix
    command = f"EXT mled g {matrix_pattern}"
    tello.send_control_command(command)
    print(f"Sent command: {command}")

# Example LED patterns (simplified as strings for this example)
#matrix_b3 = "0000000000p00p0000000000000pp000p00pp00pp000000p0p0000p000pppp00"  # Representing a number 3 in some pattern
#matrix_b2 =   # Representing a number 2 in some pattern
matrix_up = "bbbrrbbb"+"bbrrrrbb"+"brrrrrrb"+"bbbrrbbb"+"bbbrrbbb"+"bbbrrbbb"+"bbbrrbbb"+"bbbrrbbb"
matrix_down = "bbbrrbbb"+"bbbrrbbb"+"bbbrrbbb"+"bbbrrbbb"+"bbbrrbbb"+"brrrrrrb"+"bbrrrrbb"+"bbbrrbbb"
matrix_emergency= "pprrrrpp"+"prrpprrp"+"rrrpprrr"+"rrrpprrr"+"rrrpprrr"+"rrrrrrrr"+"prrpprrp"+"pprrrrpp"  # Emergency pattern
matrix_emergency_inverted ="rrpppprr"+"rpprrppr"+"ppprrppp"+"ppprrppp"+"ppprrppp"+"pppppppp"+"rpprrppr"+"rrpppprr" #works



# Run the matrix commands
try:
    while True:
        #send_led_matrix_command(matrix_b2)  # Set matrix to display number 3
        #time.sleep(5)  # Wait for 3 seconds

        send_led_matrix_command(matrix_emergency)  # Set matrix to display number 2
        tello.send_expansion_command("led 255 0 0")
        time.sleep(0.5)  # Wait for 1 second
        send_led_matrix_command(matrix_emergency_inverted)  # Set matrix to display number 2
        tello.send_expansion_command("led 255 255 255")
        time.sleep(0.5)
        #send_led_matrix_command(matrix_down)
        #time.sleep(1)
        #send_led_matrix_command(matrix_up)
        #time.sleep(1)

        # Uncomment if you want to add matrix_b1 for number 1
        # send_led_matrix_command(matrix_b1)
        # time.sleep(1)

except KeyboardInterrupt:
    print("Program interrupted.")
    tello.end()
