from djitellopy import tello
import time
import cv2

from vosk import Model, KaldiRecognizer
import pyaudio
import json
import os

global img # Global variable for image capture

# === VOICE_CONTROL_FUNCTION ===
def getVoiceInput():
    start_time = time.time()
    timeout = 3 # Waits for 5 seconds for an input

    print("Listening... (Speak!)")
    while time.time() - start_time < timeout:
        data = mic.read(4096)

        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            command = result.get("text", "").strip()
            print("You said:", command)

            # Movement variables: LeftRight, FrontBack, UpDown, YawVelocity
            lr, fb, ud, yv = 0,0,0,0
            speed = 20
            liftSpeed = 20
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
            elif command == "front flip" or "frontflip": Drone.flip('f') 
            elif command == "backflip" or "back flip": Drone.flip('b') 


            # Landing & Takeoff
            elif command == "land": 
                print("Landing...")
                Drone.Land()
                time.sleep(3)
            elif command == "take off":
                print("Taking off...")
                Drone.takeoff()

            # Capture image from drone camera
            elif command == "image":
                print("Capturing image...")
                img = Drone.get_frame_read().frame
                cv2.imwrite(f"Images/{time.time()}.jpg", img)
                time.sleep(0.3)

            return [lr, fb, ud, yv] # Return movement values
    
    print(f"No commands given in the last {timeout}s. No movement issued.")
    return [0,0,0,0] # Default: No command, no movement


# === SETUP_SPEECH_RECOGNITION ===
#model = Model("C:/Users/psemppa/Downloads/vosk-model-en-us-0.22")
model = Model(os.path.dirname(__file__)+"\Python_Packages\VoskModelSmall_en-us_0.15")
recognizer = KaldiRecognizer(model, 16000)
mic = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=16000, 
                             input=True, frames_per_buffer=4096)
mic.start_stream()

# === MATRIX PANEL ===
pattern = [
    0, 0, 0, 0, 0, 0, 0, 0,  # Row 1
    0, 0, 0, 0, 0, 0, 0, 0,  # Row 2
    0, 0, 0, 0, 0, 0, 0, 0,  # Row 3
    0, 0, 0, 0, 0, 0, 0, 0,  # Row 4
    0, 0, 0, 0, 0, 0, 0, 0,  # Row 5
    0, 0, 0, 0, 0, 0, 0, 0,  # Row 6
    0, 0, 0, 0, 0, 0, 0, 0,  # Row 7
    0, 0, 0, 0, 0, 0, 0, 0   # Row 8
    
]

# === MATRIX PANEL PATTERNS ===
X_pattern = [
    [1, 0, 0, 0, 0, 0, 0, 1],  # Row 1
    [0, 1, 0, 0, 0, 0, 1, 0],  # Row 2
    [0, 0, 1, 0, 0, 1, 0, 0],  # Row 3
    [0, 0, 0, 1, 1, 0, 0, 0],  # Row 4
    [0, 0, 0, 1, 1, 0, 0, 0],  # Row 5
    [0, 0, 1, 0, 0, 1, 0, 0],  # Row 6
    [0, 1, 0, 0, 0, 0, 1, 0],  # Row 7
    [1, 0, 0, 0, 0, 0, 0, 1]   # Row 8
]

O_pattern = [ 
    [0, 1, 1, 1, 1, 1, 1, 0],  # Row 1
    [1, 0, 0, 0, 0, 0, 0, 1],  # Row 2
    [1, 0, 0, 0, 0, 0, 0, 1],  # Row 3
    [1, 0, 0, 0, 0, 0, 0, 1],  # Row 4
    [1, 0, 0, 0, 0, 0, 0, 1],  # Row 5
    [1, 0, 0, 0, 0, 0, 0, 1],  # Row 6
    [1, 0, 0, 0, 0, 0, 0, 1],  # Row 7
    [0, 1, 1, 1, 1, 1, 1, 0]   # Row 8
]

# === MATRIX_PANEL_FUNCTIONS ===
def update_matrix(display_pattern):
    tello.set_matrix_pattern(display_pattern)


# === Drone_Connection ===
Drone = tello.Tello()
Drone.connect()
print(f"Battery: {Drone.get_battery()}%")

Drone.streamon()

# === MAIN_LOOP ===
while True:
    # Get the return value and store it on variable
    keyValues = getVoiceInput()

    # Get distance data from the drone
    distance = Drone.get_distance()
    print(f"Distance from object: {distance} cm")
    update_matrix(O_pattern)  # Update the matrix panel

    if distance < 20:  # If something is too close
        print("Obstacle detected! Moving back!")
        Drone.move_back(15)  # Move the drone back if the object is too close
        update_matrix(X_pattern)  # Update matrix to show 'X' pattern
    else:
        print("Path is clear")

    if keyValues == [None]:  # On 'Exit' command, stop the loop
        print("Exiting...")
        break

    # Drone control
    print(f"Values: {keyValues[0],keyValues[1],keyValues[2],keyValues[3]}")
    Drone.send_rc_control(keyValues[0],keyValues[1],keyValues[2],keyValues[3])
    # Get image from drone cam
    img = Drone.get_frame_read().frame
    img = cv2.resize(img, (1080, 720))
    # Show frame
    cv2.imshow("DroneCapture", img)
    cv2.waitKey(1)
    time.sleep(1)

# === CLEAN_UP ===
Drone.end()
mic.stop_stream()
mic.close()