import time
import keyboard
from djitellopy import tello
import voice_control as vc

# === Global Config === #
Drone = tello.Tello()
matrix = False       # Does the drone have a matrix screen?
distance = 20        # Default movement distance in cm
elevation = 20       # Default elevation in cm (150 cm recommended for flips)

def initialize_drone():
    global matrix, distance, elevation

    # Get matrix screen info
    response = input("Does the drone have a matrix screen? (y/n): ").strip().lower()
    matrix = response == 'y'

    # Get default movement distance
    try:
        distance_input = input("Enter distance for movement commands (default 20cm): ").strip()
        distance = int(distance_input) if distance_input else 20
    except ValueError:
        print("Invalid input. Using default distance of 20cm.")
        distance = 20

    # Get elevation
    try:
        elevation_input = input("Enter elevation (default 20cm, 150cm for flips): ").strip()
        elevation = int(elevation_input) if elevation_input else 20
    except ValueError:
        print("Invalid input. Using default elevation of 20cm.")
        elevation = 20

def get_y_or_n(prompt="Do you want to continue? (y/n): "):
    while True:
        answer = input(prompt).strip().lower()
        if answer in ['y', 'n']:
            return answer
        print("Invalid input. Please enter 'y' or 'n'.")

def main():
    initialize_drone()

    Drone.connect()
    print(f"Battery: {Drone.get_battery()}%")

    while True:
        if keyboard.is_pressed('k'):
            print("Emergency stop triggered!")
            vc.ExitNow()
            break

        given_command = vc.GetVoiceInput()
        if given_command in (None, "exit"):
            if given_command == "exit":
                vc.ExitNow()
            continue

        verified_command = vc.CheckCommand(given_command)
        if not verified_command:
            print(f"Invalid command: '{given_command}' not recognized")
            continue

        print(f"Valid Command: {given_command}")
        if get_y_or_n("Run this command? (y/n): ") == 'y':
            vc.RunCommand(verified_command)
        else:
            print("Command cancelled.")

        time.sleep(0.1)

if __name__ == "__main__":
    main()
