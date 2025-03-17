import streamlit as st
import cv2
import time
import os
from models.yolo.object_detection import ObjectDetector

# Cache the model to avoid reloading on every Streamlit rerun
@st.cache_resource
def load_detector():
    model_path = "backend/models/yolo/best.pt"  # Adjust path as per your repo structure
    if not os.path.exists(model_path):
        st.error(f"Model file not found at {model_path}. Please check your repo!")
        st.stop()
    return ObjectDetector(model_path)

# Load YOLO detector
detector = load_detector()

# Streamlit App UI
st.title("🏅 AI Sports Highlights Generator")

uploaded_file = st.file_uploader("🎥 Upload a sports video", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    with open("temp_video.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("Video uploaded successfully! Starting processing...")

    cap = cv2.VideoCapture("temp_video.mp4")
    frame_placeholder = st.empty()
    highlight_frames = []
    highlight_start_time = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        detections = detector.detect_objects(frame)

        # Draw detections on frame
        for detection in detections:
            x1, y1, x2, y2 = detection['bbox']
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Stream frame to Streamlit
        frame_placeholder.image(frame, channels="BGR")

        # Highlight logic (e.g., ball detected)
        if any(detection['class_id'] == 0 for detection in detections):
            if highlight_start_time is None:
                highlight_start_time = time.time()
            highlight_frames.append(frame)
        elif highlight_start_time is not None:
            highlight_duration = time.time() - highlight_start_time
            if highlight_duration >= 2:
                highlight_filename = f"highlight_{int(time.time())}.mp4"
                out = cv2.VideoWriter(highlight_filename, cv2.VideoWriter_fourcc(*'mp4v'), 30, (frame.shape[1], frame.shape[0]))
                for highlight_frame in highlight_frames:
                    out.write(highlight_frame)
                out.release()
                st.success(f"🎯 Highlight saved: {highlight_filename}")
            highlight_frames = []
            highlight_start_time = None

        time.sleep(0.03)  # Simulate near real-time

    cap.release()
    st.info("✅ Processing complete!")

