import time
import json
import pyaudio
import keyboard
from vosk import Model, KaldiRecognizer
from djitellopy import tello
import drone_commands as dc
from difflib import SequenceMatcher

Model_Path = "vosk/vosk-model-small-en-us-0.15"
Threshold = 0.7

# Setup Vosk model and recognizer
model = Model(Model_Path)
recognizer = KaldiRecognizer(model, 16000)

# Microphone setup
mic = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=16000, 
                             input=True, frames_per_buffer=4096)
mic.start_stream()

Drone = tello.Tello()

# Define valid commands for the drone
valid_commands = {
    "go left": dc.Go_left,
    "go right": dc.Go_right,
    "go forward": dc.Go_forward,
    "go back": dc.Go_back,
    "go up": dc.Go_up,
    "go down": dc.Go_down,
    "rotate left": dc.Rotate_left,
    "rotate right": dc.Rotate_right,
    "spin clockwise": dc.Spin_clockwise,
    "spin counter": dc.Spin_counter,
    "do front flip": dc.Frontflip,
    "do backflip": dc.Backflip,
    "go land": dc.LandingSequence,
    "take off": dc.Takingoff,
    "go test": dc.Testing,
    "go best": dc.Testing,
    
    "exit": "Exit the program"
}

# Function to get voice input and return movement values
def getVoiceInput():
    print("Press and hold 'Space' to talk...")
    command = ""
    while not keyboard.is_pressed('space'):  # Wait until spacebar is pressed
        time.sleep(0.1)  # Prevent high CPU usage

    print("Listening... (Speak!)")

    while keyboard.is_pressed('space'):
        data = mic.read(4096)
        #data = mic.read(1400)

        if len(data) == 0:
            continue

        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            command = result.get("text", "").strip().lower()
            if command == None:
                continue
            else:
                break
    
    print("You said:", command if command else "No command detected.")
    return command

def checkCommand(given_command):
    # Compare given command with valid commands using similarity
    highest_similarity = 0
    best_match = None

    # Loop through valid commands & calculate similarity
    for command in valid_commands:
        matcher = SequenceMatcher(None, given_command, command)
        similarity = matcher.ratio()
        print(f"Similarity with '{command}': {similarity}")

        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = command
            
    # If similarity goes over threshold, return best match
    if highest_similarity <= Threshold:
        print("No valid command detected with enough similarity.")
        return None
    else:
        print(f"Command '{best_match}' detected with similarity {highest_similarity}")
        executed_command = valid_commands.get(best_match, None)
        return executed_command()

def ExitNow():
    print("Exiting...")
    try:
        Drone.land()
        time.sleep(1)
    finally:
        Drone.end()
        mic.stop_stream()
        mic.close()