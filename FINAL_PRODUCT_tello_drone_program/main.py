import time
import keyboard
from djitellopy import tello
import voice_control as vc

# Initialize the drone
Drone = tello.Tello()

def main():
    # Drone setup
    #Drone.connect()
    #print(f"Battery: {Drone.get_battery()}%")

    # Optionally, you can start the video stream in a separate thread to avoid blocking
    #vs.start_video_stream()

    while not keyboard.is_pressed('k'):
        # Get voice command input
        command = vc.getVoiceInput()

        if command == "exit":  # On 'Exit' command, stop the loop
            vc.ExitNow()
            break

        command_is_valid = vc.checkCommand(command)
        print(f"Command: {command_is_valid}")
        time.sleep(1)

        # Optional: Check and display the drone's camera feed (uncomment if needed)
        # img = Drone.get_frame_read().frame
        # img = cv2.resize(img, (1080, 720))
        # cv2.imshow("DroneCapture", img)
        # cv2.waitKey(1)
        
        # Sleep to avoid overloading the control loop
        time.sleep(0.1)

    # Clean-up
    vc.ExitNow()

if __name__ == "__main__":
    main()
