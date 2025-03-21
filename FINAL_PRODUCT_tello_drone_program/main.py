import time
from djitellopy import Tello
import voice_control
import waypoint_control  # Assuming this module will be used later for waypoint control.
import cv2

# Initialize the drone
Drone = Tello()

def main():
    # Drone setup
    Drone.connect()
    print(f"Battery: {Drone.get_battery()}%")

    while True:
        # Get voice command input from voice_control
        command = voice_control.getVoiceInput()

        if command:
            print(f"Received command: {command}")

            # Execute the corresponding drone command
            if command == "go exit":
                print("Exiting...")
                break  # Exit the loop

            # Drone control commands (example)
            elif command == "go left":
                Drone.move_left(20)
            elif command == "go right":
                Drone.move_right(20)
            elif command == "go forward":
                Drone.move_forward(25)
            elif command == "go back":
                Drone.move_back(25)
            elif command == "go up":
                Drone.move_up(20)
            elif command == "go down":
                Drone.move_down(20)
            elif command == "go turn left":
                Drone.rotate_counter_clockwise(50)
            elif command == "go turn right":
                Drone.rotate_clockwise(50)
            elif command == "go stop":
                print("Landing...")
                Drone.land()
                time.sleep(3)
            
            # Additional voice commands (e.g., take off, flip, etc.)
            elif command == "go take off":
                Drone.takeoff()
            elif command == "go flip front":
                Drone.flip('f')
            elif command == "go flip back":
                Drone.flip('b')
            else:
                print("Unknown command.")

        # Optionally, you can start the video stream in a separate thread to avoid blocking
        # img = Drone.get_frame_read().frame
        # img = cv2.resize(img, (1080, 720))
        # cv2.imshow("DroneCapture", img)
        # cv2.waitKey(1)

        # Sleep to avoid overloading the control loop
        time.sleep(0.1)

    # Clean-up
    Drone.end()

if __name__ == "__main__":
    main()
