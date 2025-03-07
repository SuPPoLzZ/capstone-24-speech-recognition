# voice_control.py

import time
import json
import pyaudio
from vosk import Model, KaldiRecognizer
import numpy as np
from main import Drone

# Setup Vosk model and recognizer
model = Model("vosk/vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)
mic = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=16000, 
                             input=True, frames_per_buffer=4096)
mic.start_stream()


def preprocess_audio(data):
    # Convert audio data to numpy array
    audio_data = np.frombuffer(data, dtype=np.int16)
    # Apply normalization
    audio_data = audio_data / np.max(np.abs(audio_data))
    # Convert back to bytes
    return audio_data.tobytes()

def getVoiceInput():
    start_time = time.time()
    timeout = 5  # Wait for 5 seconds for an input

    print("Listening... (Speak!)")
    while time.time() - start_time < timeout:
        data = mic.read(4096)

        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            command = result.get("text", "").strip()
            print("You said:", command)

            # Initialize movement variables
            lr, fb, ud, yv = 0, 0, 0, 0
            speed = 20
            liftSpeed = 20
            moveSpeed = 25
            rotationSpeed = 50

            # Handle directional commands
            if command == "exit":
                return [None]  # Signal to exit the program
            
            # Test commands
            #if command == "best":
                print(f"Temp: {Drone.get_temperature()}")
                print(f"Battery: {Drone.get_battery()}")
                Drone.turn_motor_on()
                time.sleep(5)
                Drone.turn_motor_off()
                print("Test complete.")
                Drone.end()

            # Directional commands
            if command == "left": lr = -speed
            elif command == "right": lr = speed
            elif command == "forward": fb = moveSpeed
            elif command == "back": fb = -moveSpeed
            elif command == "up": ud = liftSpeed
            elif command == "down": ud = -liftSpeed
            elif command == "turn left": yv = rotationSpeed
            elif command == "turn right": yv = -rotationSpeed

            # Special commands
            elif command == "spin": yv = 360
            elif command == "spin counter clockwise": yv = -360
            elif command in ["front flip", "frontflip"]: Drone.flip('f')
            elif command in ["backflip", "back flip"]: Drone.flip('b')

            # Emergency stop
            if command == "best":
                print("Taking off...")
                Drone.takeoff()
            
            if command == "stop":
                print("Landing...")
                Drone.Land()
                time.sleep(3)

            return [lr, fb, ud, yv]

    print(f"No commands given in the last {timeout}s. No movement issued.")
    return [0, 0, 0, 0]  # Default: No command, no movement
