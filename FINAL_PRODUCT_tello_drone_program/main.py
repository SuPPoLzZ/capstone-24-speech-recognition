import time
from djitellopy import Tello
import voice_control
import waypoint_control  # Assuming this module will be used later for waypoint control.
import cv2
import keyboard

# Initialize the drone
Drone = Tello()

speed = 20
moveSpeed = 25
rotationSpeed = 50
liftSpeed = 20

def main():
    # Drone setup
    Drone.connect()
    print(f"Battery: {Drone.get_battery()}%")

    while True:
        # Get voice command input from voice_control
        command = voice_control.getVoiceInput()

        if command or not keyboard.is_pressed('s'):
            print(f"Received command: {command}")

            # Execute the corresponding drone command
            if command == "go exit":
                print("Exiting...")
                break  # Exit the loop


            # Drone control commands (example)
            elif command == "go left":
                Drone.move_left(speed)
            elif command == "go takeoff":
                Drone.takeoff()
            elif command == "go right":
                Drone.move_right(speed)
            elif command == "go forward":
                Drone.move_forward(speed)
            elif command == "go back":
                Drone.move_back(speed)
            elif command == "go up":
                Drone.move_up(liftSpeed)
            elif command == "go down":
                Drone.move_down(liftSpeed)
            elif command == "go turn left":
                Drone.rotate_counter_clockwise(rotationSpeed)
            elif command == "go turn right":
                Drone.rotate_clockwise(rotationSpeed)
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
            elif command == "go test":
                Drone.turn_motor_on()
                time.sleep(5)
                Drone.turn_motor_off()
            else:
                print("Unknown command.")
            
            

        # Optionally, you can start the video stream in a separate thread to avoid blocking
        #img = Drone.get_frame_read().frame
        #img = cv2.resize(img, (1080, 720))
        #cv2.imshow("DroneCapture", img)
        #cv2.waitKey(1)

    print("S pressed! Landing the drone.")
    Drone.land()  # Land the drone
    time.sleep(3) 

    # Clean-up
    Drone.end()

if __name__ == "__main__":
    main()
