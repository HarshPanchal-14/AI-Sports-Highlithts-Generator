from flask import Blueprint, request, jsonify
from api.processing import process_video

api = Blueprint('api', __name__)

@api.route('/upload', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    try:
        result = process_video(file)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500 