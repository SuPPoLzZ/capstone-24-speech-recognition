from djitellopy import Tello
import time

Drone = Tello()
Drone.connect()

def send_led_matrix_command(matrix_pattern):
    # Send the 'EXT mled g' command to control the LED matrix
    command = f"EXT mled g {matrix_pattern}"
    Drone.send_control_command(command)
    print(f"Sent command: {command}")

def basic_test():
    Drone.takeoff()
    Drone.move_up(150)
    time.sleep(3)
    Drone.rotate_clockwise(90)
    time.sleep(3)
    Drone.rotate_counter_clockwise(90)
    time.sleep(5)
    Drone.flip_forward()
    time.sleep(2)
    Drone.move_back(20)
    time.sleep(2)
    Drone.flip_left()
    time.sleep(2)
    Drone.move_right(20)
    time.sleep(2)
    Drone.flip_right()
    time.sleep(2)
    Drone.move_left(20)
    time.sleep(3)
    Drone.land()


    

def get_BasicInfo():
    print(f"Temp: {tello.get_temperature()}")
    print(f"Battery: {tello.get_battery()}")

# Example LED patterns (simplified as strings for this example)
some_pattern = "0pppppp0"+"pppppppp"+"prrpprrp"+"prrpprrp"+"pppprppp"+"pppppppp"+"0prprpr0"+"0prprpr0"

# Connect to drone

basic_test()

# Run the matrix commands
#send_led_matrix_command(some_pattern)  # Set matrix to display to pattern
#time.sleep(5)  # Wait for 5 second

#print("press space to quit")
#keyboard.wait("space")
#final_pattern = "00000000"+"00000000"+"00000000"+"00000000"+"00000000"+"00000000"+"00000000"+"00000000"
#send_led_matrix_command(final_pattern) # Turns the led matrix off

print("Ending")
tello.end()