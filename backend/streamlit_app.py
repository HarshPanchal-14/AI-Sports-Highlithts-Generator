import streamlit as st
from models.yolo.object_detection import ObjectDetector
import cv2
import time
import os

# Initialize the object detector
detector = ObjectDetector()

# Streamlit app
st.title("⚽ AI Sports Highlights Generator")

# Upload video file
uploaded_file = st.file_uploader("🎥 Upload a sports video", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    # Save the uploaded file temporarily
    temp_video_path = "/tmp/temp_video.mp4"
    with open(temp_video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Open video with OpenCV
    cap = cv2.VideoCapture(temp_video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30  # Default to 30 FPS if not detected
    
    # Streamlit placeholders
    frame_placeholder = st.empty()
    progress_bar = st.progress(0)
    st.write("🚀 Processing video...")

    # Variables for highlights
    highlight_frames = []
    highlight_start_time = None
    highlight_files = []
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    current_frame = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        current_frame += 1
        
        # Object detection
        detections = detector.detect_objects(frame)
        
        # Draw detections
        for detection in detections:
            x1, y1, x2, y2 = detection['bbox']
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        # Resize for Streamlit display
        frame_display = cv2.resize(frame, (640, 360))
        frame_placeholder.image(frame_display, channels="BGR")
        
        # Highlight logic (detecting "ball" as class_id 0)
        if any(d['class_id'] == 0 for d in detections):
            if highlight_start_time is None:
                highlight_start_time = time.time()
            highlight_frames.append(frame)
        elif highlight_start_time is not None:
            highlight_duration = time.time() - highlight_start_time
            if highlight_duration >= 2:  # Save if duration >= 2 sec
                highlight_filename = f"/tmp/highlight_{int(time.time())}.mp4"
                out = cv2.VideoWriter(highlight_filename, cv2.VideoWriter_fourcc(*'mp4v'), int(fps), (frame.shape[1], frame.shape[0]))
                for h_frame in highlight_frames:
                    out.write(h_frame)
                out.release()
                highlight_files.append(highlight_filename)
                st.success(f"Highlight saved: {os.path.basename(highlight_filename)}")
            highlight_frames = []
            highlight_start_time = None
        
        # Progress update
        progress_bar.progress(min(current_frame / total_frames, 1.0))
        
        # Control frame rate
        time.sleep(1 / fps)
    
    cap.release()
    progress_bar.empty()
    st.success("✅ Processing complete!")

    # Download buttons for saved highlights
    if highlight_files:
        st.subheader("🎯 Download Highlights")
        for file in highlight_files:
            with open(file, "rb") as vid_file:
                st.download_button(
                    label=f"Download {os.path.basename(file)}",
                    data=vid_file,
                    file_name=os.path.basename(file),
                    mime="video/mp4"
                )
    else:
        st.warning("No highlights detected.")
