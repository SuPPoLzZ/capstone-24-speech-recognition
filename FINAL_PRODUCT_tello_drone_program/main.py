import time
from djitellopy import Tello
import voice_control
import waypoint_control
from vosk import Model, KaldiRecognizer
import pyaudio
import cv2
import video_stream as vs

# Initialize the drone
Drone = Tello()

def main():
    # Drone setup
    Drone.connect()
    print(f"Battery: {Drone.get_battery()}%")

    # Optionally, you can start the video stream in a separate thread to avoid blocking
    vs.start_video_stream()

    while True:
        # Get voice command input
        keyValues = voice_control.getVoiceInput()

        if keyValues == [None]:  # On 'Exit' command, stop the loop
            print("Exiting...")
            break

        # Check if valid movement values are returned
        if keyValues != [0, 0, 0, 0]:
            # Drone control (send the corresponding movement commands)
            print(f"Values: {keyValues[0], keyValues[1], keyValues[2], keyValues[3]}")
            Drone.send_rc_control(keyValues[0], keyValues[1], keyValues[2], keyValues[3])

        # Optional: Check and display the drone's camera feed (uncomment if needed)
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
