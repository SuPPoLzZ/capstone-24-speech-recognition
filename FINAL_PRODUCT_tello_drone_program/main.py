import time
from djitellopy import tello
import voice_control as vc
import drone_commands as dc
import video_stream as vids

# Initialize the drone
Drone = tello.Tello()
given_command = ""

def initialize_drone():
    # Flag to specify if the drone has a matrix screen 
    global has_matrix_screen
    matrix_Choice = input("Does the drone have a matrix screen? (y/n): ").strip().lower()
    if matrix_Choice == 'y':
        has_matrix_screen = True
    else:
        has_matrix_screen = False
    
    takeVideo = input("Do you want to take a video? (y/n): ").strip().lower()
    if takeVideo == 'y':
        print("Taking video, you can quit the video by pressing 'q'")
        vids.TakeDroneVideo()
    else:
        print("No video")
    
    dc.DefineMovements()

def main():
    # Drone setup
    Drone.connect()
    print(f"Battery: {Drone.get_battery()}%")

    # Initialize the drone
    initialize_drone()

    while True:

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
        else:
            print(f"Valid Command: {given_command}")

        # Step 3: Ask to Run command
        print("Do you want to run the command? \nKeyboard: \n - y to run \n - n to cancel \n - k to exit")
        result = get_y_or_n()
        if result == 'y':
            vc.RunCommand(verified_command)
        elif result == 'n':
            print("Command cancelled")
            continue
        elif result == 'k':
            print("Emergency stop triggered!")
            vc.ExitNow()
            break
        else:
            print("Wrong input, continuing!")
            continue
        
        # Sleep to avoid overloading the control loop
        time.sleep(0.1)

def get_y_or_n():
    answer = input("Answer here: ").strip().lower()
    if answer in ['y', 'n', 'k']:
        return answer
    else:
        return None

if __name__ == "__main__":
    main()