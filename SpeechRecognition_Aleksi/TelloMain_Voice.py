from djitellopy import tello
import time
#import TelloInput as ti
import cv2

from vosk import Model, KaldiRecognizer
import pyaudio
import json

global img

def getVoiceInput():
    
    # LeftRight, FrontBack, UpDown, YawVelocity
    lr, fb, ud, yv = 0,0,0,0
    speed = 80
    liftSpeed = 80
    moveSpeed = 85
    rotationSpeed = 100
    data = mic.read(4096)

    if recognizer.AcceptWaveform(data):
        result = json.loads(recognizer.Result())
        print("You said:", result["text"])
        
        if result["text"] == "":
            result["text"] = "[no_speech]"
        elif result["text"] == "exit":
            global isRunning
            isRunning = False
            exit()
        
        # Left-Rigth
        if result["text"] == "left": lr = -speed; print(lr)
        elif result["text"] == "right": lr = speed; print(lr)

        # Front-Back
        if result["text"] == "forward": fb = moveSpeed; print(fb)
        elif result["text"] == "back": fb = -moveSpeed; print(fb)

        # Up-Down
        if result["text"] == "up": ud = liftSpeed; print(ud)
        elif result["text"] == "down": ud = -liftSpeed; print(ud)

        # Rotation
        if result["text"] == "turn left": yv = rotationSpeed; print(yv)
        elif result["text"] == " turn right": yv = -rotationSpeed; print(yv)

        # Landing
        if result["text"] == "land": Drone.land(); print("Landing..."); time.sleep(3)
        elif result["text"] == "take off": Drone.takeoff(); print("Taking off...")

        # Screen Shots
        if result["text"] == "image":
            print("Capturing image...")
            cv2.imwrite(f"tellopy/Resources/Images/{time.time()}.jpg", img)
            time.sleep(0.3)
    
        return [lr, fb, ud, yv] # Return given value

# ti.init()

model = Model("Python_Packages/VoskModelSmall_en-us_0.15")
recognizer = KaldiRecognizer(model, 16000)
isRunning = True
mic = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=16000, 
                             input=True, frames_per_buffer=4096)
mic.start_stream()
print("Listening... (Speak!)")


# Connects to the drone
Drone = tello.Tello()
Drone.connect()

print(Drone.get_Battery())

Drone.streamon()

while isRunning:
    # Get the return value and store it on variable
    keyValues = getVoiceInput()
    # Control the drone
    Drone.send_rc_control(keyValues[0],keyValues[1],
                          keyValues[2],keyValues[3])
    # Get image from drone cam
    img = Drone.get_frame_read().frame
    img = cv2.resize(img, (1080, 720))
    # Show frame
    cv2.imshow("DroneCapture", img)
    cv2.waitKey(1)