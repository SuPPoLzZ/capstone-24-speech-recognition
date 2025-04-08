import time
import keyboard
from djitellopy import tello
import voice_control as vc

# Initialize the drone
Drone = tello.Tello()
given_command = ""


def initialize_drone():
    # Flag to specify if the drone has a matrix screen 
    has_matrix_screen = False
    input("Does the drone have a matrix screen? (y/n): ").strip().lower()
    if has_matrix_screen == 'y':
        has_matrix_screen = True
    else:
        has_matrix_screen = False
    
    
    

def main():
    # Initialize the drone
    initialize_drone()
    # Drone setup
    Drone.connect()
    print(f"Battery: {Drone.get_battery()}%")

    # Optionally, you can start the video stream in a separate thread to avoid blocking
    #vs.start_video_stream()

    while True:
        
        if keyboard.is_pressed('k'):
            print("Emergency stop triggered!")
            vc.ExitNow()
            break

        # Step 1: Get voice commands
        given_command = vc.GetVoiceInput()
        if given_command == "exit":
            vc.ExitNow()
            break
        if given_command == None:
            continue

        # Step 2: Verifiy command
        verified_command = vc.CheckCommand(given_command)
        if verified_command is None:
            print(f"Invalid command: '{given_command}' not recognized")
            continue
        print(f"Valid Command: {given_command}")

        # Step 3: Ask to Run command
        print("Do you want to run the command? \nKeyboard: \n - y to run \n - n to cancel")
        result = get_y_or_n()
        if result == 'y':
            vc.RunCommand(verified_command)
        elif result == 'n':
            print("Command cancelled")
            continue

        # Optional: Check and display the drone's camera feed (uncomment if needed)
        # img = Drone.get_frame_read().frame
        # img = cv2.resize(img, (1080, 720))
        # cv2.imshow("DroneCapture", img)
        # cv2.waitKey(1)
        
        # Sleep to avoid overloading the control loop
        time.sleep(0.1)

def get_y_or_n():
    answer = input("Do you want to continue? (y/n): ").strip().lower()
    if answer in ['y', 'n']:
        return answer
    else:
        return None

if __name__ == "__main__":
    main()