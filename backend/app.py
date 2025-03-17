import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from api.routes import api

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')

@app.route('/')
def index():
    return 'AI Sports Highlights Generator'

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('highlights', exist_ok=True)
    print(sys.path)
    app.run(debug=True) 