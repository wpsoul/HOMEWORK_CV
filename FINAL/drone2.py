from djitellopy import Tello
import cv2
import time
import os
from datetime import datetime
import subprocess

def main():

    # Create a Tello object
    tello = Tello()

    # Connect to the Tello drone
    tello.connect()

    # Print the battery level
    battery = tello.get_battery()
    print(f"Battery level: {battery}%")

    # Start video stream
    tello.streamon()

    # Get current date for folder name
    current_date = datetime.now().strftime("%Y-%m-%d")
    if not os.path.exists(current_date):
        os.makedirs(current_date)

    # Video capture setup
    cap = tello.get_frame_read()
    video_filename = os.path.join(current_date, 'tello_video.avi')
    video_writer = cv2.VideoWriter(video_filename, cv2.VideoWriter_fourcc(*'XVID'), 30, (960, 720))

    # Start recording video
    recording = True


    # Capture video frames during flight
    start_time = time.time()
    while recording and (time.time() - start_time) < 30:  # Record for 30 seconds or until the flight ends
        frame = cap.frame
        if frame is not None:
            video_writer.write(frame)
        time.sleep(1 / 30)  # To match the 30 FPS rate

    # Stop recording video
    recording = False

    # Release video writer
    video_writer.release()

    # Stop video stream
    tello.streamoff()

    # End the connection
    tello.end()

if __name__ == "__main__":
    main()