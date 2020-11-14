import cv2
from image_processor import ImageProcessor
import warnings


warnings.filterwarnings('ignore')
image_processor = ImageProcessor(debug=True)
image_processor.debugLoop()
