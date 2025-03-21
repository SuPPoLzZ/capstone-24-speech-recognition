from djitellopy import tello
import time
import keyboard
import TelloDroneCommands as tc

from vosk import Model, KaldiRecognizer
import pyaudio
import json

# ===!!! THIS IS THE NEWEST UNMODIFIED VERSION OF THE WORKING CODE !!!===

# === SETUP_SPEECH_RECOGNITION ===
model = Model("vosk/vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)
mic = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=16000, 
                             input=True, frames_per_buffer=4096)
mic.start_stream()

# === DRONE_CONNECTION ===
Drone = tello.Tello()
Drone.connect()
print(f"Battery: {Drone.get_battery()}%")
Drone.streamon()

# === DRONE_CONTROL_DICTIONARY ===
valid_commands = {
    "go left": tc.go_left,
    "go right": tc.go_right,
    "go forward": tc.go_forward,
    "go back": tc.go_back,
    "go up": tc.go_up,
    "go down": tc.go_down,
    "rotate left": tc.rotate_left,
    "rotate right": tc.rotate_right,
    "spin clockwise": tc.spin_clockwise,
    "spin counter": tc.spin_counter,
    "do front flip": tc.frontflip,
    "do backflip": tc.backflip,
    "go land": tc.LandingSequence,
    "take off": tc.Takingoff,
    "go test": tc.Testing,
    "go best": tc.Testing
}


# === VOICE_CONTROL_FUNCTION ===
def getVoiceInput():
    print("Press and hold 'Space' to talk...")
    while not keyboard.is_pressed('space'):  # Wait until spacebar is pressed
        time.sleep(0.1)  # Prevent high CPU usage

    print("Listening...")

    while keyboard.is_pressed('space'):
        data = mic.read(4096)

        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            command = result.get("text", "").strip()
            break
    
    print("You said:", command if command else "No command detected.")
    return command

# === CHECH_THE_COMMANDS ===
def CheckForCommand(command):
    command = valid_commands.get(command, getVoiceInput)
    return command()

# === EMERGENCY_EXIT ===
def ExitNow():
    print("Exiting...")
    Drone.land()
    time.sleep(1)
    Drone.end()

# === MAIN_LOOP ===
while not keyboard.is_pressed('k'):
    # Get the return value and store it on variable
    command = getVoiceInput()
    if command == "exit":
        ExitNow()
        break

    # Drone control
    movement = CheckForCommand(command)
    print(f"Movement: {movement}")
    time.sleep(1)
            
# === CLEAN_UP ===
try:
    ExitNow()
finally:
    Drone.end()
    mic.stop_stream()
    mic.close()