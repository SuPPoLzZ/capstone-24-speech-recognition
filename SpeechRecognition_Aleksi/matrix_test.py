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
matrix_b2 = "ppppppppprrrrrrrrrrrrrrrrrggggggggggg0000000000000000000000000000"  # Representing a number 2 in some pattern

# Run the matrix commands
try:
    while True:
        #send_led_matrix_command(matrix_b3)  # Set matrix to display number 3
        time.sleep(3)  # Wait for 3 seconds

        send_led_matrix_command(matrix_b2)  # Set matrix to display number 2
        time.sleep(1)  # Wait for 1 second

        # Uncomment if you want to add matrix_b1 for number 1
        # send_led_matrix_command(matrix_b1)
        # time.sleep(1)

except KeyboardInterrupt:
    print("Program interrupted.")
    tello.end()
