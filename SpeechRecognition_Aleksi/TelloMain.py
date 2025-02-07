from djitellopy import tello
import time
import TelloInput as ti
import cv2

global img

def getKeyboardInput():
    # LeftRight, FrontBack, UpDown, YawVelocity
    lr, fb, ud, yv = 0,0,0,0
    speed = 80
    liftSpeed = 80
    moveSpeed = 85
    rotationSpeed = 100

    # Left-Rigth
    if ti.getKey("LEFT"): lr = -speed
    elif ti.getKey("RIGHT"): lr = speed

    # Front-Back
    if ti.getKey("UP"): fb = moveSpeed
    elif ti.getKey("DOWN"): fb = -moveSpeed

    # Up-Down
    if ti.getKey("w"): ud = liftSpeed
    elif ti.getKey("s"): ud = -liftSpeed

    # Rotation
    if ti.getKey("d"): yv = rotationSpeed
    elif ti.getKey("a"): yv = -rotationSpeed

    # Landing
    if ti.getKey("q"): Drone.land(); time.sleep(3)
    elif ti.getKey("e"): Drone.takeoff()

    # Screen Shots
    if ti.getKey("z"):
        cv2.imwrite(f"tellopy/Resources/Images/{time.time()}.jpg", img)
        time.sleep(0.3)
    
    return [lr, fb, ud, yv] # Return given value

ti.init()

# Connects to the drone
Drone = tello.Tello()
Drone.connect()

print(Drone.get_Battery())

Drone.streamon()

while True:
    # Get the return value and store it on variable
    keyValues = getKeyboardInput()
    # Control the drone
    Drone.send_rc_control(keyValues[0],keyValues[1],
                          keyValues[2],keyValues[3])
    # Get image from drone cam
    img = Drone.get_frame_read().frame
    img = cv2.resize(img, (1080, 720))
    # Show frame
    cv2.imshow("DroneCapture", img)
    cv2.waitKey(1)