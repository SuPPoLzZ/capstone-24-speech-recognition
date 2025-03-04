from djitellopy import Tello
import cv2
import time

# Initialize and connect to the Tello drone
drone = Tello()
drone.connect()


# Print battery level
print(f"Battery: {drone.get_battery()}%")

drone.send_command_with_return("command")

drone.query_sdk_version()
print(f"Temp: {drone.get_temperature()}")

#drone.turn_motor_on()
#drone.reboot()

"""
drone.streamon()

frame = drone.get_frame_read().frame

cv2.imshow("cap", frame)
imageFile = f"tello_frame_cap{time.time()}.jpg"
cv2.imwrite(imageFile, frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
drone.streamoff()
"""
while True:
# Takeoff
    drone.takeoff()
    drone.land()
"""
time.sleep(2)

# Move forward
drone.move_forward(50)
time.sleep(2)

# Move backward
drone.move_back(50)
time.sleep(2)

# Move left
drone.move_left(50)
time.sleep(2)

# Move right
drone.move_right(50)
time.sleep(2)


# Land the drone
    drone.land()

# Disconnect
drone.end()
"""