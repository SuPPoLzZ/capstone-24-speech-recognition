import time
import json
import pyaudio
from vosk import Model, KaldiRecognizer

# Vosk model path
MODEL_PATH = "vosk/vosk-model-small-en-us-0.15"

# Setup Vosk model and recognizer
model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, 16000)

# Microphone setup
mic = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=16000, 
                             input=True, frames_per_buffer=4096)
mic.start_stream()

valid_commands = {
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

if __name__ == "__main__":
    getVoiceInput()