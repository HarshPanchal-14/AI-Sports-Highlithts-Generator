import streamlit as st
from models.yolo.object_detection import ObjectDetector
import cv2
import time
import os

# Initialize the object detector
detector = ObjectDetector()

# Streamlit app
st.title("🏟️ AI Sports Highlights Generator")

# Upload video file
uploaded_file = st.file_uploader("📹 Upload a sports video", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    with open("temp_video.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("Video uploaded successfully!")

    if st.button("🚀 Start Processing"):
        cap = cv2.VideoCapture("temp_video.mp4")
        frame_placeholder = st.empty()

        highlight_frames = []
        highlight_start_time = None
        saved_highlights = []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Resize frame for Streamlit display
            resized_frame = cv2.resize(frame, (640, 360))

            # Detect objects
            detections = detector.detect_objects(resized_frame)

            # Draw bounding boxes
            for detection in detections:
                x1, y1, x2, y2 = detection['bbox']
                cv2.rectangle(resized_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Streamlit image display
            frame_placeholder.image(resized_frame, channels="BGR")

            # Check for highlights
            if any(detection['class_id'] == 0 for detection in detections):  # assuming ball = class 0
                if highlight_start_time is None:
                    highlight_start_time = time.time()
                highlight_frames.append(frame)
            elif highlight_start_time is not None:
                highlight_duration = time.time() - highlight_start_time
                if highlight_duration >= 2:
                    highlight_filename = f"highlight_{int(time.time())}.mp4"
                    out = cv2.VideoWriter(highlight_filename, cv2.VideoWriter_fourcc(*'mp4v'), 30, (frame.shape[1], frame.shape[0]))
                    for hf in highlight_frames:
                        out.write(hf)
                    out.release()
                    saved_highlights.append(highlight_filename)
                    st.success(f"✅ Highlight saved: {highlight_filename}")
                highlight_frames = []
                highlight_start_time = None

            time.sleep(0.03)  # simulate real-time

        cap.release()
        st.success("🎉 Video processing complete!")

        # Offer downloads
        for hl in saved_highlights:
            with open(hl, "rb") as f:
                st.download_button(label=f"⬇️ Download {hl}", data=f, file_name=hl)

