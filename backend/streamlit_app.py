import streamlit as st
from models.yolo.object_detection import ObjectDetector
import cv2
import time

# Initialize the object detector
detector = ObjectDetector()

# Streamlit app
st.title("AI Sports Highlights Generator")

# Upload video file
uploaded_file = st.file_uploader("Upload a sports video", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    # Save the uploaded file temporarily
    with open("temp_video.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Process the video
    st.write("Processing video...")
    cap = cv2.VideoCapture("temp_video.mp4")
    
    # Create a placeholder for the video frame
    frame_placeholder = st.empty()
    
    # Initialize variables for highlight clipping
    highlight_frames = []
    highlight_start_time = None
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Detect objects in the frame
        detections = detector.detect_objects(frame)
        
        # Display the frame with detections
        for detection in detections:
            x1, y1, x2, y2 = detection['bbox']
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        # Display the frame in real-time
        frame_placeholder.image(frame, channels="BGR")
        
        # Check for highlights (e.g., when a ball is detected)
        if any(detection['class_id'] == 0 for detection in detections):  # Assuming class_id 0 is for the ball
            if highlight_start_time is None:
                highlight_start_time = time.time()
            highlight_frames.append(frame)
        elif highlight_start_time is not None:
            # Save the highlight clip
            highlight_duration = time.time() - highlight_start_time
            if highlight_duration >= 2:  # Minimum duration for a highlight clip
                highlight_filename = f"highlight_{int(time.time())}.mp4"
                out = cv2.VideoWriter(highlight_filename, cv2.VideoWriter_fourcc(*'mp4v'), 30, (frame.shape[1], frame.shape[0]))
                for highlight_frame in highlight_frames:
                    out.write(highlight_frame)
                out.release()
                st.write(f"Highlight saved: {highlight_filename}")
            highlight_frames = []
            highlight_start_time = None
        
        # Add a small delay to simulate real-time processing
        time.sleep(0.03)  # Adjust this value to control the frame rate
    
    cap.release()
    st.write("Processing complete!")