from datetime import timedelta
from collections import defaultdict

class HighlightGenerator:
    def __init__(self):
        self.event_weights = {
            'goal': 1.0,
            'dunk': 0.9,
            'wicket': 0.8,
            'cheer': 0.7
        }
        
    def generate_highlights(self, detections, duration):
        # Process detections and generate highlight segments
        highlights = []
        current_highlight = None
        for detection in detections:
            if detection['confidence'] > 0.8:
                if current_highlight is None:
                    current_highlight = {
                        'start': detection['timestamp'],
                        'end': detection['timestamp'],
                        'score': 0
                    }
                else:
                    current_highlight['end'] = detection['timestamp']
                current_highlight['score'] += self.event_weights.get(detection['event'], 0)
            else:
                if current_highlight and current_highlight['score'] > 1.0:
                    highlights.append(current_highlight)
                current_highlight = None
        return highlights 