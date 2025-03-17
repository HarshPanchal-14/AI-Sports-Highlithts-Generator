from .routes import api

# Import the process_video function from the processing module
from .processing import process_video

__all__ = ['api', 'process_video']  # Updated to include process_video  # Defines what is accessible when using `from api import *`