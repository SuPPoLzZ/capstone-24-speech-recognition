import time
from djitellopy import Tello

# Initialize the Tello object
tello = Tello()

# Connect to the Tello drone
tello.connect()

# Function to send the LED matrix command
def send_led_matrix_command(matrix_pattern):
    # Send the 'EXT mled g' command to control the LED matrix
    command = f"EXT mled  {matrix_pattern}"
    tello.send_control_command(command)
    print(f"Sent command: {command}")

#LED patterns 
matrix_o = "0pppppp0p000000pp000000pp000000pp000000pp000000pp000000p0pppppp0"
matrix_x = "p000000p" + "0p0000p0" + "00p00p00" + "000pp000"+ "000pp000" + "00p00p00" + "0p0000p0" +"p000000p"


# Run the matrix commands
try:
    while True:
        #send_led_matrix_command(matrix_b3)  # Set matrix to display number 3
        time.sleep(3)  # Wait for 3 seconds

        send_led_matrix_command(matrix_x)  # Set matrix to display number 2
        time.sleep(1)  # Wait for 1 second

        # Uncomment if you want to add matrix_b1 for number 1
        # send_led_matrix_command(matrix_b1)
        # time.sleep(1)

except KeyboardInterrupt:
    print("Program interrupted.")
    tello.end()
