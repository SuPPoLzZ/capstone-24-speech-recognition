# test_voice_recognition.py

import time
from voice_control import getVoiceInput  # Import the function from voice_control.py

# List of valid commands to be recognized
VALID_COMMANDS = [
    "left", "right", "forward", "back", 
    "up", "down", "turn left", "turn right",
    "spin", "spin counter clockwise", 
    "front flip", "backflip", "stop", "exit"
]

def test_voice_recognition():
    print("Starting voice recognition test...")

    # Test the function by calling it and printing the recognized command
    while True:
        print("Listening for command...")

        # Get the voice input
        result = getVoiceInput()
        
        # If None is returned, it means we should exit the program (from 'exit' command)
        if result == [None]:
            print("Exiting the program.")
            break
        
        # If the result is valid (non-zero), process the command
        if result != [0, 0, 0, 0]:
            # Get the movement values (from result)
            lr, fb, ud, yv = result

            # Map recognized commands to specific actions
            print(f"Recognized movement values: Left/Right={lr}, Forward/Backward={fb}, Up/Down={ud}, Yaw={yv}")
            
            # Check if the command is in the valid list
            # Here we're just printing the result, but you could also act on the command (like controlling the drone)
            if result in VALID_COMMANDS:
                print(f"Command '{result}' recognized and processed.")
            else:
                print(f"Command '{result}' is invalid or not recognized.")

        # If no command was recognized within the timeout period, let the user know
        else:
            print("No command detected or not recognized.")

        # Wait a bit before trying again (to avoid constant listening)
        time.sleep(1)

if __name__ == "__main__":
    test_voice_recognition()
