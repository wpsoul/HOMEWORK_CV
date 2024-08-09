from djitellopy import Tello
import cv2
import time
import os
from datetime import datetime
from ultralytics import YOLO


model = YOLO("YOLO/yolov8s.pt")

def detect_objects(frame, model):
    results = model(frame)
    return results

def draw_labels(frame, results):
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            confidence = box.conf[0]
            class_id = int(box.cls[0])
            label = model.names[class_id]
            color = (0, 255, 0)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, f"{label} {confidence:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return frame

def tello_move(tello):
    # Take off
    tello.takeoff()
    time.sleep(1)

    # Move up by 1 meter
    tello.move_up(100)
    time.sleep(1)

    # Move forward by 1 meter
    tello.move_forward(100)
    time.sleep(1)

    # Move back by 1 meter
    tello.move_back(100)
    time.sleep(1)

    # Land
    tello.land()

def main():

    # Create a Tello object
    tello = Tello()

    # Connect to the Tello drone
    tello.connect()

    # Print the battery level
    battery = tello.get_battery()
    print(f"Battery level: {battery}%")

    # Get current date for folder name
    current_date = datetime.now().strftime("%Y-%m-%d")
    if not os.path.exists(f'{current_date}'):
        os.makedirs(f'{current_date}')

    # Start video stream
    tello.streamon()

    # Initialize the video writer
    frame_read = tello.get_frame_read()
    time.sleep(2)
    frame = frame_read.frame
    height, width, _ = frame.shape
    video = cv2.VideoWriter(f'{current_date}/drone.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 30.0, (width, height))
    
    print("Starting video capture. Press 'q' to quit.")

    while True:
        # Get the current frame from the drone
        frame = frame_read.frame

        #frame = cv2.resize(frame, (360, 240))

        results = detect_objects(frame, model)
        frame = draw_labels(frame, results)
        
        # Write the frame to the video file
        video.write(frame)
        
        # Display the frame (optional)
        cv2.imshow("Tello Video Stream", frame)
        
        # Check for 'q' key press to quit early
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Stop recording when the drone lands
        #if not tello.is_flying:
            #break

    video.release()  
    cv2.destroyAllWindows() 

    # Stop video stream
    tello.streamoff()


if __name__ == "__main__":
    main()