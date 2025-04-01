import cv2
import time
from djitellopy import Tello

tello = Tello()
tello.connect()
tello.streamon()

# Delay for start
time.sleep(2)

# Define the video writer
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter("C:/Users/Aleksandra/Desktop/tello_video.mp4", fourcc, 30.0, (960, 720))

if not out.isOpened():
    print("Error: VideoWriter failed to open!")
else:
    print("VideoWriter is working.")

frame_count = 0

while True:
    frame = tello.get_frame_read().frame

    if frame is None:
        print("Error: No frames recieved!")
        continue

    # frame = cv2.resize(frame, (640, 480))
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

    out.write(frame)  # Save frame to file
    frame_count += 1
    cv2.imshow("Tello Video Stream", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print(f"✅ Video saved with {frame_count} frames")

tello.streamoff()
out.release()  # Stop recording
cv2.destroyAllWindows()