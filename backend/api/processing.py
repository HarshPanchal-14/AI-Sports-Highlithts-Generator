from models.yolo.object_detection import ObjectDetector
from models.action_recognition.event_detector import EventDetector
from models.audio_analysis.crowd_noise import CrowdNoiseAnalyzer
from models.highlight_model import HighlightGenerator
from video_processing.frame_extraction import extract_frames
from video_processing.highlight_extraction import extract_highlights
import tempfile
import os

def process_video(video_file):
    # Save video to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
        video_path = tmp.name
        video_file.save(video_path)
    
    try:
        # Initialize models
        object_detector = ObjectDetector()
        event_detector = EventDetector('model.pth')
        noise_analyzer = CrowdNoiseAnalyzer()
        highlight_generator = HighlightGenerator()
        
        # Process video
        frames = extract_frames(video_path)
        detections = []
        for frame in frames:
            objects = object_detector.detect_objects(frame)
            events = event_detector.detect_events(frame)
            detections.append({
                'objects': objects,
                'events': events
            })
        
        # Generate highlights
        highlights = highlight_generator.generate_highlights(detections, len(frames))
        
        # Extract highlights
        output_path = extract_highlights(video_path, highlights)
        
        return {
            'status': 'success',
            'highlight_path': output_path
        }
    finally:
        os.remove(video_path)