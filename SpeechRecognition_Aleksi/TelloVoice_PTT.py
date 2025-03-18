from djitellopy import tello
import time
import keyboard

from vosk import Model, KaldiRecognizer
import pyaudio
import json

#global img # Global variable for image capture

# ===!!! THIS IS THE NEWEST UNMODIFIED VERSION OF THE WORKING CODE !!!===

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

    # Movement variables: LeftRight, FrontBack, UpDown, YawVelocity
    lr, fb, ud, yv = 0,0,0,0
    speed, liftSpeed, moveSpeed, rotationSpeed = 25, 25, 25, 50

    if command == "exit":
        return [None] # Signal to exit the program

    # Directional commands
    if command == "left": lr = -speed; print(lr)
    elif command == "right": lr = speed; print(lr)
    elif command == "forward": fb = moveSpeed; print(fb)
    elif command == "back": fb = -moveSpeed; print(fb)
    elif command == "up": ud = liftSpeed; print(ud)
    elif command == "down": ud = -liftSpeed; print(ud)
    elif command == "turn left": yv = rotationSpeed; print(yv)
    elif command == "turn right": yv = -rotationSpeed; print(yv)
    
    # Special commands
    elif command == "spin": cw = 360; print(cw)
    elif command == "spin counter clockwise": ccw = -360; print(ccw)
    elif command == "front flip": print("Frontflip"); Drone.flip_forward()
    elif command == "backflip": print("Backflip"); Drone.flip_back()

    # Landing & Takeoff
    elif command == "land": 
        print("Landing...")
        Drone.land()
        time.sleep(3)
    elif command == "take off":
        print("Taking off...")
        Drone.takeoff()

    elif command in ["test", "best"]:
        Drone.turn_motor_on()
        time.sleep(10)
        Drone.turn_motor_off()
        print("Test done")
    
    else:
        lr, fb, ud, yv = 0,0,0,0

    return [lr, fb, ud, yv] # Return movement values


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

# === MAIN_LOOP ===
while True:
    # Get the return value and store it on variable
    keyValues = getVoiceInput()
    
    if keyboard.is_pressed('k'):
        Drone.land()
        time.sleep(1)
        Drone.end()
        break

    if keyValues == [None]: # On 'Exit' command, stop the loop
        print("Exiting...")
        Drone.land()
        time.sleep(1)
        Drone.end()
        break

    # Drone control
    print(f"Values: {keyValues[0],keyValues[1],keyValues[2],keyValues[3]}")
    Drone.send_rc_control(keyValues[0],keyValues[1],keyValues[2],keyValues[3])
    
    time.sleep(1)
            
# === CLEAN_UP ===
Drone.end()
mic.stop_stream()
mic.close()