import json
import pyaudio
from vosk import Model, KaldiRecognizer
from difflib import SequenceMatcher

# Vosk model path
MODEL_PATH = "vosk/vosk-model-small-en-us-0.15"
THRESHOLD = 0.7  # Similarity threshold

# Setup Vosk model and recognizer
model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, 16000)

# Microphone setup
mic = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=16000, 
                                input=True, frames_per_buffer=4096)
mic.start_stream()

valid_commands = {
    "go exit": "Exit the program",
    "go test": "Performing diagnostics",
    "go left": "Move drone left",
    "go right": "Move drone right",
    "go forward": "Move drone forward",
    "go back": "Move drone back",
    "go up": "Move drone up",
    "go take off": "Take off the drone",
    "go land": "Land the drone",
    "go down": "Move drone down",
    "go turn left": "Turn drone left",
    "go turn right": "Turn drone right",
    "go spin clock": "Spin the drone 360 degrees",
    "go spin back": "Spin the drone 360 degrees counter clockwise",
    "go flip front": "Make the drone perform a front flip",
    "go flip back": "Make the drone perform a back flip",
    "go stop": "Land the drone"
}

def getVoiceInput():
    print("Listening... (Speak!)")
    while True:
        #data = mic.read(4096)
        data = mic.read(1400)
        if len(data) == 0:
            continue

        if recognizer.AcceptWaveform(data):
            result_str = recognizer.Result()
            result = json.loads(result_str)

            if "text" in result:
                recognized_text = result["text"].strip().lower()
                print(f"Recognized text: {recognized_text}")

                # Compare recognized text with valid commands using similarity
                highest_similarity = 0
                best_match = None

                # Loop through valid commands and calculate similarity
                for command in valid_commands:
                    matcher = SequenceMatcher(None, recognized_text, command)
                    similarity = matcher.ratio()
                    print(f"Similarity with '{command}': {similarity}")

                    if similarity > highest_similarity:
                        highest_similarity = similarity
                        best_match = command

                # If similarity exceeds the threshold, return the best match
                if highest_similarity <= THRESHOLD:
                    print("No valid command detected with sufficient similarity.")
                    return None
        
                else:
                    print(f"Command '{best_match}' detected with similarity {highest_similarity}")
                    return best_match

if __name__ == "__main__":
    while True:
        getVoiceInput()