import time
import json
import pyaudio
from vosk import Model, KaldiRecognizer
from djitellopy import Tello

# Vosk model path
MODEL_PATH = "vosk/vosk-model-small-en-us-0.15"

drone = Tello()

# Define valid commands for the drone
valid_commands = {
    "go diagnostic": "Perform a diagnostic test",
    "go exit": "Exit the program",
    "go left": "Move drone left",
    "go right": "Move drone right",
    "go forward": "Move drone forward",
    "go back": "Move drone back",
    "go up": "Move drone up",
    "go take off": "Take off the drone",
    "go down": "Move drone down",
    "go turn left": "Turn drone left",
    "go turn right": "Turn drone right",
    "go clock spin": "Spin the drone 360 degrees",
    "go spin counter clockwise": "Spin the drone 360 degrees counter clockwise",
    "go flip front": "Make the drone perform a front flip",
    "go flip back": "Make the drone perform a back flip",
    "go stop": "Land the drone"
}

# Setup Vosk model and recognizer
model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, 16000)

# Microphone setup
mic = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=16000, 
                             input=True, frames_per_buffer=4096)
mic.start_stream()

def getVoiceInput():
    print("Listening... (Speak!)")
    while True:
        data = mic.read(4096)
        if len(data) == 0:
            continue

        if recognizer.AcceptWaveform(data):
            result_str = recognizer.Result()
            result = json.loads(result_str)

            if "text" in result:
                recognized_text = result["text"].strip().lower()
                print(f"Recognized text: {recognized_text}")

                # Check if recognized text contains any valid command
                for command in valid_commands:
                    if command in recognized_text:
                        print(f"Command '{command}' detected!")
                        return command

                print("No valid command detected.")
                return None


def executeCommand(command):
    speed = 20
    liftSpeed = 20
    moveSpeed = 25
    rotationSpeed = 50



    if command == "drone exit":
        return False  # Exit the program

    if command == "test":
        print(f"Temperature: {Tello.get_temperature()}")
        print(f"Battery: {Tello.get_battery()}")
        Tello.turn_motor_on()
        time.sleep(5)
        Tello.turn_motor_off()
        print("Test complete.")
        Tello.end()

    elif command == "go left":
        return drone.move_left(speed)
    elif command == "go right":
        return drone.move_right(speed)
    elif command == "go forward": 
        return drone.move_forward(speed)
    elif command == "go back":
        return drone.move_back(speed)
    elif command == "go up": 
        return drone.move_up(liftSpeed)

    elif command == "go down":
        return drone.move_down(liftSpeed)
    elif command == "go turn left":
        return drone.rotate_counter_clockwise(rotationSpeed)
    elif command == "go turn right": 
        return drone.rotate_clockwise(rotationSpeed)

    elif command == "go clock spin": 
        return drone.rotate_clockwise(360)
    elif command == "go spin counter clockwise":
        return drone.rotate_counter_clockwise(360)
    elif command in ["go flip front", "go flipfront"]: 
        return drone.flip('f')
    elif command in ["go flip back", "go flipback"]:
        return drone.flip('b')

    elif command == "go stop":
        print("Landing...")
        drone.land()
        time.sleep(3)

    return True

if __name__ == "__main__":
    while True:
        command = getVoiceInput()
        if command:
            if not executeCommand(command):
                break
        else:
            print("No valid command detected.")