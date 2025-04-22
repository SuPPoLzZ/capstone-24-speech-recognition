import os
import cv2
import time
from djitellopy import tello

# Ensure output directory exists
os.makedirs("videos", exist_ok=True)
frame = ""

def TakeDroneVideo():
    Drone = tello.Tello()
    Drone.connect()
    Drone.streamon()

    # Delay for start
    time.sleep(2)

    frame = Drone.get_frame_read().frame

    TARGET_FPS = 120.0
    fourcc = cv2.VideoWriter_fourcc(*"mp4v") # mp4v OR XVID
    out = cv2.VideoWriter("videos/tello_video.mp4", fourcc, TARGET_FPS, (960, 720))

    if not out.isOpened():
        print("Error: VideoWriter failed to open!")
        Drone.streamoff()
        return
    else:
        print("VideoWriter is working.")

    frame_count = 0

    while True:
        frame = Drone.get_frame_read().frame
        if frame is None:
            print("Error: No frames recieved!")
            continue

        # frame = cv2.resize(frame, (640, 480))
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

        out.write(frame)  # Save frame to file
        cv2.imshow("Tello Video Stream", frame)
        frame_count += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print(f"✅ Video saved with {frame_count} frames")
    out.release()  # Stop the recording
    Drone.streamoff()
    cv2.destroyAllWindows()