from djitellopy import Tello
import time

# Initialize Tello drone
drone = Tello()

def display_x_on_matrix():
    # Matrix "X" pattern as a single string, all rows in one command
    matrix_pattern = "1000001 0100010 0010100 0001000 0010100 0100010 1000001"
    
    # Send the entire matrix pattern as one command
    drone.send_expansion_command(f"matrix {matrix_pattern}")

def clear_matrix_display():
    # Clear the matrix display (turn off all LEDs)
    clear_pattern = "0000000 0000000 0000000 0000000 0000000 0000000 0000000"
    drone.send_expansion_command(f"matrix {clear_pattern}")
    time.sleep(1)

# Main execution
if __name__ == "__main__":
    # Connect to the drone
    drone.connect()

    # Display the X pattern
    display_x_on_matrix()
    time.sleep(4)

    # Clear the matrix after showing the X pattern
    clear_matrix_display()

    # End the connection
    drone.end()
