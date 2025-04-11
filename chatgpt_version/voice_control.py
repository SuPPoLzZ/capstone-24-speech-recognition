import time
import json
import pyaudio
import keyboard
from vosk import Model, KaldiRecognizer
from djitellopy import tello
import drone_commands as dc
from difflib import SequenceMatcher

# === Config === #
MODEL_PATH = "vosk/vosk-model-small-en-us-0.15"
THRESHOLD = 0.7
CHUNK = 4096
RATE = 16000

# === Initialize === #
model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, RATE)

# Setup microphone stream
mic = pyaudio.PyAudio().open(
    format=pyaudio.paInt16,
    channels=1,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK
)
mic.start_stream()

Drone = tello.Tello()

# === Valid Voice Commands === #
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

# === Voice Input === #
def GetVoiceInput():
    print("\n▶ Press 'Space' to speak, 'k' to exit")
    
    while True:
        if keyboard.is_pressed('k'):
            print("Exit key pressed.")
            return "exit"
        elif keyboard.is_pressed('space'):
            break
        time.sleep(0.1)

    print("🎤 Listening...")
    spoken_text = ""

    while keyboard.is_pressed('space'):
        try:
            data = mic.read(CHUNK, exception_on_overflow=False)
        except IOError:
            continue

        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            spoken_text = result.get("text", "").strip().lower()
            break

    if not spoken_text:
        print("⚠ No command detected.")
    else:
        print(f"🗣 You said: '{spoken_text}'")

    return spoken_text or None

# === Fuzzy Match to Valid Commands === #
def CheckCommand(given_command):
    if not given_command:
        return None

    highest_similarity = 0
    best_match = None

    for command in valid_commands:
        similarity = SequenceMatcher(None, given_command, command).ratio()
        print(f"🧠 Similarity with '{command}': {similarity:.2f}")
        
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = command

    if highest_similarity >= THRESHOLD:
        print(f"✅ Matched: '{best_match}' (Score: {highest_similarity:.2f})")
        return valid_commands[best_match]
    
    print("❌ No valid match above threshold.")
    return None

# === Run Verified Command === #
def RunCommand(verified_command):
    if callable(verified_command):
        verified_command()

# === Exit and Cleanup === #
def ExitNow():
    print("🛑 Exiting and landing drone...")
    try:
        Drone.land()
        time.sleep(1)
        Drone.end()
    except Exception as e:
        print("⚠ Drone landing failed or already landed:", e)
    finally:
        mic.stop_stream()
        mic.close()
