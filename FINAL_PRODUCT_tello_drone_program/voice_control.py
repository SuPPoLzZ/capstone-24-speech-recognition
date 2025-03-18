import time
import json
import pyaudio
import keyboard
from vosk import Model, KaldiRecognizer
import numpy as np
from djitellopy import Tello
import video_stream as vs

# Setup Vosk model and recognizer
model = Model("vosk/vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)

# Microphone setup
mic = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=16000, 
                             input=True, frames_per_buffer=4096)
mic.start_stream()

# Define valid commands for the drone
valid_commands = {
    "test": "Perform a diagnostic test",
    "best": "Alternative to test",
    "exit": "Exit the program",
    "left": "Move drone left",
    "right": "Move drone right",
    "forward": "Move drone forward",
    "back": "Move drone back",
    "up": "Move drone up",
    "down": "Move drone down",
    "turn left": "Turn drone left",
    "turn right": "Turn drone right",
    "spin": "Spin the drone 360 degrees",
    "spin counter clockwise": "Spin the drone 360 degrees counter clockwise",
    "front flip": "Make the drone perform a front flip",
    "backflip": "Make the drone perform a back flip",
    "stop": "Land the drone"
}

# Function to preprocess audio (normalize the audio)
def preprocess_audio(data):
    audio_data = np.frombuffer(data, dtype=np.int16)
    audio_data = audio_data / np.max(np.abs(audio_data))  # Normalize
    return audio_data.tobytes()

# Function to get voice input and return movement values
def getVoiceInput():
    print("Press and hold 'Space' to talk...")

    lr, fb, ud, yv = 0, 0, 0, 0  # Initialize movement variables
    speed = 20
    liftSpeed = 20
    moveSpeed = 25
    rotationSpeed = 50

    while True:
        keyboard.wait('space')
        print("Listening... (Speak!)")

        while keyboard.is_pressed('space'):
            data = mic.read(4096)

            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                command = result.get("text", "").strip().lower()
                print(f"You said: {command}")

                # Handle recognized commands
                if command in valid_commands:
                    # Command to exit the program
                    if command == "exit":
                        return [None]  # Exit the program

                    # Test command (Run diagnostics)
                    if command == "best":
                        print("Hello World!")
                        """
                        vs.start_video_stream()
                        print(f"Temperature: {Tello.get_temperature()}")
                        print(f"Battery: {Tello.get_battery()}")
                        Tello.turn_motor_on()
                        time.sleep(5)
                        Tello.turn_motor_off()
                        print("Test complete.")
                        Tello.end()
                        """

                    # Directional movement commands
                    elif command == "left": lr = -speed
                    elif command == "right": lr = speed
                    elif command == "forward": fb = moveSpeed
                    elif command == "back": fb = -moveSpeed
                    elif command == "up": ud = liftSpeed
                    elif command == "down": ud = -liftSpeed
                    elif command == "turn left": yv = rotationSpeed
                    elif command == "turn right": yv = -rotationSpeed

                    # Special commands (spin, flips)
                    elif command == "spin": yv = 360
                    elif command == "spin counter clockwise": yv = -360
                    elif command in ["front flip", "frontflip"]: Tello.flip('f')
                    elif command in ["backflip", "back flip"]: Tello.flip('b')

                    # Stop the drone (land)
                    elif command == "stop":
                        print("Landing...")
                        Tello.land()
                        time.sleep(3)

                else:
                    print(f"Unrecognized command: '{command}'")

                return [lr, fb, ud, yv]

        print(f"No commands given. No movement issued.")
        return [0, 0, 0, 0]  # Default: No command, no movement