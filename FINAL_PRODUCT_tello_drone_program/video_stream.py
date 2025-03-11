import cv2
import socket
import numpy as np

def test_stream():
    # Tello drone connection
    Tello_ip = ('192.168.10.1', 8889)  # Tello command port
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Send command to Tello to start the video stream
    sock.sendto(b'command', Tello_ip)  # Ensure the Tello is in command mode
    sock.sendto(b'streamon', Tello_ip)  # Start video stream




def stream_tello_video():
    # Tello IP and Port for video stream
    Tello_IP = "0.0.0.0"
    VIDEO_PORT = 11112

    # Set up UDP socket to receive video stream
    video_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    video_socket.bind((Tello_IP, VIDEO_PORT))

    # Create OpenCV window
    cv2.namedWindow("Tello Stream", cv2.WINDOW_NORMAL)

    while True:
        # Receive video data from Tello
        frame, _ = video_socket.recvfrom(65536)
        
        # Decode the frame to a format OpenCV can display
        nparr = np.frombuffer(frame, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is not None:
            # Display the image in the OpenCV window
            cv2.imshow("Tello Stream", img)

        # Close the window if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources and close the window
    cv2.destroyAllWindows()
    video_socket.close()


if __name__ == "__main__":
    test_stream()
    stream_tello_video()


