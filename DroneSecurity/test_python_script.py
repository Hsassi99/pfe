import cv2
import socket
import pickle
import struct

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server on local computer
client_socket.connect(('20.19.81.88',12345))

# Capture video from the camera
cap = cv2.VideoCapture(0)  # 0 is the default camera

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            # Serialize frame
            data = pickle.dumps(frame)

            # Send data size of the data first
            message_size = struct.pack("L", len(data))  # L is unsigned long
            try:
                client_socket.sendall(message_size + data)
            except ConnectionResetError as e:
                print("Connection was reset unexpectedly:", e)

        else:
            break
except KeyboardInterrupt:
    pass
finally:
    cap.release()
    client_socket.close()
