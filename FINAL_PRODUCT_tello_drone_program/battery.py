import djitellopy as tello
import time

# Create a Tello object
Drone = tello.Tello()

# Connect to the Tello drone
while True:
    Drone.connect()
    print(f"TEMP: {Drone.get_temperature()} C'")
    print(f"Battery: {Drone.get_battery()}%")
    time.sleep(60)
