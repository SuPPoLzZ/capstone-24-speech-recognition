from djitellopy import Tello
import time

Drone = Tello()
Drone.connect()

Drone.turn_motor_on()
time.sleep(5)
Drone.turn_motor_off()

print("Ending")
Drone.end()