from djitellopy import tello
import time
import keyboard

from vosk import Model, KaldiRecognizer
import pyaudio
import json

global img # Global variable for image capture

# ===!!! THIS IS THE NEWEST UNMODIFIED VERSION OF THE WORKING CODE !!!===

# === VOICE_CONTROL_FUNCTION ===
def getVoiceInput():
    print("Press and hold 'Space' to talk...")

    while True:
        keyboard.wait('space')
        print("Listening...")

        while keyboard.is_pressed('space'):
            data = mic.read(4096)

            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                command = result.get("text", "").strip()
                print("You said:", command)

                # Movement variables: LeftRight, FrontBack, UpDown, YawVelocity
                lr, fb, ud, yv = 0,0,0,0
                speed = 25
                liftSpeed = 25
                moveSpeed = 25
                rotationSpeed = 50

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
                elif command == "front flip": Drone.flip_forward() 
                elif command == "backflip": Drone.flip_back() 

                # Landing & Takeoff
                elif command == "land": 
                    print("Landing...")
                    Drone.land()
                    time.sleep(3)
                elif command == "take off":
                    print("Taking off...")
                    Drone.takeoff()

                return [lr, fb, ud, yv] # Return movement values
    
        print(f"No valid commands given. No movement issued.")
        return [0,0,0,0] # Default: No command, no movement


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