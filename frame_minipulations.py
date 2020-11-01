import cv2
import os

max_value = 255
max_value_H = 360//2
low_H = 0
low_S = 0
low_V = 0
high_H = max_value_H
high_S = max_value
high_V = max_value
window_capture_name = 'original'
window_detection_name = 'Object Detection'
low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'
high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'

def loadImagesFromFolder(folder):
    return [(cv2.imread(os.path.join(folder, filename)), filename) for filename in os.listdir(folder) if cv2.imread(os.path.join(folder, filename)) is not None]

# function to detect the ROI for the cow.
# We need a range of RGB values for the color of the corners - In our case it's red
# The function will interrogate the frame, detect the left most, right most, top most and bottom most pixels,
# anything within that range will be kept, the rest cropped out
# @input - RGB frame
# @return - cropped RGB image only with ROI.
def getROI(frame, lowX=0, highX=720, lowY=0, highY=1280):
    # scaled = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    cropped = frame[lowY:highY, lowX: highX]
    return cropped

def scale_to_360(frame):
    return cv2.resize(frame, (256, 144), interpolation=cv2.INTER_AREA)

def grayScaleFrame(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def BgrToHsv(frame, low_H, low_S, low_V, high_H, high_S, high_V):
    frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    return cv2.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))
