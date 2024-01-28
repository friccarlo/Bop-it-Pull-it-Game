from roboflow import Roboflow
import numpy as np
VERSION = 1
import cv2
rf = Roboflow(api_key="aZDfnapGThmiaVxQJBHV")
project = rf.workspace().project("bopitmerged")
model = project.version(VERSION).model

cap = cv2.VideoCapture(0)

frame_skip = 25  # Process every 5th frame
frame_count = 0
target_resolution = (640, 640)  # Target resolution for model input

try:
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % frame_skip != 0:
            continue

        # Resize frame to the resolution expected by the model
        resized_frame = cv2.resize(frame, target_resolution)

        # Perform inference on the resized frame
        prediction = model.predict(resized_frame, confidence=40, overlap=30).json()

        # Draw bounding boxes and display class names
        for det in prediction['predictions']:
            x_scale = frame.shape[1] / target_resolution[0]
            y_scale = frame.shape[0] / target_resolution[1]

            x1 = int((det['x'] - det['width'] / 2) * x_scale)
            y1 = int((det['y'] - det['height'] / 2) * y_scale)
            x2 = x1 + int(det['width'] * x_scale)
            y2 = y1 + int(det['height'] * y_scale)

            # Draw rectangle and label for each detection
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f"{det['class']} ({det['confidence']:.2f})"
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # Display the resulting frame
        cv2.imshow('Frame', cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))


        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # When everything done, release the capture
    cap.release()
    # Allow time for windows to close
    cv2.waitKey(1)
    # Destroy all OpenCV windows
    cv2.destroyAllWindows()