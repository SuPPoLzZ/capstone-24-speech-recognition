# main.py

import time
from djitellopy import tello
import voice_control
import waypoint_control
from vosk import Model, KaldiRecognizer
import pyaudio
import cv2


Drone = tello.Tello()

def main():
    # Drone setup
    Drone.connect()
    print(f"Battery: {Drone.get_battery()}%")
    Drone.streamon()

    while True:
        # Get the return value and store it in a variable
        keyValues = voice_control.getVoiceInput()



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
