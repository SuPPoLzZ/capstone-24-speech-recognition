import time
import json
import pyaudio
import keyboard
from vosk import Model, KaldiRecognizer
import numpy as np
from djitellopy import tello
import drone_commands as dc
#import video_stream as vs

# Setup Vosk model and recognizer
model = Model("vosk/vosk-model-small-en-us-0.15")
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

# Function to preprocess audio (normalize the audio)
def preprocess_audio(data):
    audio_data = np.frombuffer(data, dtype=np.int16)
    audio_data = audio_data / np.max(np.abs(audio_data))  # Normalize
    return audio_data.tobytes()

# Function to get voice input and return movement values
def getVoiceInput():
    print("Press and hold 'Space' to talk...")
    while not keyboard.is_pressed('space'):  # Wait until spacebar is pressed
        time.sleep(0.1)  # Prevent high CPU usage

    print("Listening... (Speak!)")

    while keyboard.is_pressed('space'):
        data = mic.read(4096)

        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            command = result.get("text", "").strip().lower()
            break
    
    print("You said:", command if command else "No command detected.")
    return command

def checkCommand(command):
    command = valid_commands.get(command, getVoiceInput)
    return command()

def ExitNow():
    print("Exiting...")
    try:
        Drone.land()
        time.sleep(1)
    finally:
        Drone.end()
        mic.stop_stream()
        mic.close()