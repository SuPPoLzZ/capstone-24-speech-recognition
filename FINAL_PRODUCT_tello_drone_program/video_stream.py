import cv2
import socket
import threading
import time

# Tello drone IP and port for video stream
TELLORCVID_IP = '192.168.10.1'
TELLORCVID_PORT = 11111

# Create a UDP socket to receive video stream
video_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
video_socket.bind(('0.0.0.0', 9000))  # Use port 9000 for receiving video data

def receive_video():
    while True:
        # Receive video data in chunks and display it
        data, _ = video_socket.recvfrom(65536)  # Receive UDP packet
        # Here, you need to decode the data (H.264 stream) for proper display
        # OpenCV cannot directly display raw H.264, so we need to process it
        frame = cv2.imdecode(data, cv2.IMREAD_COLOR)
        if frame is not None:
            cv2.imshow('Tello Video Stream', frame)

        # Exit when the user presses 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Close the socket and window
    video_socket.close()
    cv2.destroyAllWindows()

def start_video_stream():
    # Set up the video stream from the Tello drone
    tello_control_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tello_control_socket.sendto(b'command', (TELLORCVID_IP, 8889))  # Put Tello in command mode
    tello_control_socket.sendto(b'streamon', (TELLORCVID_IP, 8889))  # Start the video stream
    
    # Start a new thread to receive video
    video_thread = threading.Thread(target=receive_video)
    video_thread.start()

    # Give some time for the drone to start the stream
    time.sleep(2)

    try:
        # Keep running the stream until 'q' is pressed
        video_thread.join()
    except KeyboardInterrupt:
        print("Stream interrupted by user")

