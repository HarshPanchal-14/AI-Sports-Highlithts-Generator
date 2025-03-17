from ultralytics import YOLO
import cv2
import os
import subprocess

class ObjectDetector:
    def __init__(self, model_path='yolov8n.pt'):
        self.model = YOLO(model_path)
        
    def detect_objects(self, frame):
        results = self.model(frame)
        detections = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])
                detections.append({
                    'bbox': [x1, y1, x2, y2],
                    'confidence': confidence,
                    'class_id': class_id
                })
        return detections 

def check_project_structure():
    required_files = [
        'backend/app.py',
        'backend/requirements.txt',
        'frontend/src/app/app.module.ts',
        'frontend/package.json'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        return f"Missing files: {missing_files}"
    else:
        return "Project structure looks good!"

def install_backend_dependencies():
    try:
        requirements_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'requirements.txt')
        subprocess.run(['pip', 'install', '-r', requirements_path], check=True)
        return "Backend dependencies installed successfully!"
    except subprocess.CalledProcessError as e:
        return f"Error installing backend dependencies: {e}"

def install_frontend_dependencies():
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'frontend', 'frontend-app')
    if os.path.exists(frontend_path):
        try:
            subprocess.run(['npm', 'install'], cwd=frontend_path, check=True)
        except FileNotFoundError:
            print("npm not found. Please ensure Node.js is installed.")
    else:
        print(f"Frontend directory not found at {frontend_path}")

def run_frontend():
    try:
        frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'frontend', 'frontend-app')
        subprocess.Popen(['ng', 'serve'], cwd=frontend_path)
        return "Frontend server is running!"
    except Exception as e:
        return f"Error running frontend server: {e}"

check_project_structure()
install_backend_dependencies()
install_frontend_dependencies()
run_frontend()