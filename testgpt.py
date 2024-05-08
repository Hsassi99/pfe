import requests
import cv2
import numpy as np

# Replace with the actual IP address of your Raspberry Pi and port of your Flask app
pi_ip = "192.168.178.88"
port = 5000  # Replace with the port used in your Flask app

def display_stream():
  """
  Function to display the stream from the Flask app on the Raspberry Pi.
  """
  stream_url = f"http://{pi_ip}:{port}"
  try:
    response = requests.get(stream_url)
    response.raise_for_status()  # Raise an exception for non-2xx status codes

    while True:
      bytes_ = response.raw.read(1024)
      if not bytes_:
        break
      frame = cv2.imdecode(np.frombuffer(bytes_, np.uint8), cv2.IMREAD_COLOR)
      if frame is None:
        continue
      cv2.imshow('Stream', frame)
      if cv2.waitKey(1) == ord('q'):
        break

  except requests.exceptions.RequestException as e:
    print(f"Error accessing stream: {e}")

  cv2.destroyAllWindows()

if __name__ == "__main__":
  display_stream()
