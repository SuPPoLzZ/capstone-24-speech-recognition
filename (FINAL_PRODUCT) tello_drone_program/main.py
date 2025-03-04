# main.py

import time
from drone_connection import Drone
from voice_control import getVoiceInput
from matrix_control import update_matrix, X_pattern, O_pattern
from waypoint_control import waypoints
import cv2

def main():
    # Drone setup
    Drone.connect()
    print(f"Battery: {Drone.get_battery()}%")
    Drone.streamon()

    while True:
        # Get the return value and store it in a variable
        keyValues = getVoiceInput()

        # Get distance data from the drone
        distance = Drone.get_distance()
        print(f"Distance from object: {distance} cm")
        update_matrix(O_pattern)  # Update the matrix panel with O pattern

        if distance < 20:  # If something is too close
            print("Obstacle detected! Moving back!")
            Drone.move_back(15)  # Move the drone back if the object is too close
            update_matrix(X_pattern)  # Update matrix to show 'X' pattern
        else:
            print("Path is clear")

        if keyValues == [None]:  # On 'Exit' command, stop the loop
            print("Exiting...")
            break

        # Drone control
        print(f"Values: {keyValues[0], keyValues[1], keyValues[2], keyValues[3]}")
        Drone.send_rc_control(keyValues[0], keyValues[1], keyValues[2], keyValues[3])

        # Get image from drone cam
        img = Drone.get_frame_read().frame
        img = cv2.resize(img, (1080, 720))

        # Show frame
        cv2.imshow("DroneCapture", img)
        cv2.waitKey(1)
        time.sleep(1)

    # Clean-up
    Drone.end()

if __name__ == "__main__":
    main()
