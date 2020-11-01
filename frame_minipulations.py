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
def getROI(frame):
    # dim = (640, 480)
    # scaled = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    # lowX = 123
    # highX = 919
    # lowY = 185
    # highY = 570
    lowX = 50
    highX = 1000
    lowY = 50
    highY = 460
    cropped = frame[lowY:highY, lowX: highX]
    return cropped
    # print('shape', frame.shape)
    # # converting from BGR to HSV color space
    # hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    # # Range for lower red
    # lower_red = np.array([0,120,70])
    # upper_red = np.array([10,200,200])
    # mask1 = cv2.inRange(hsv, lower_red, upper_red)

    # # Range for upper range
    # lower_red = np.array([170,120,70])
    # upper_red = np.array([180,200,200])
    # mask2 = cv2.inRange(hsv,lower_red,upper_red)
    # cv2.imshow('mask1', mask1)
    # cv2.imshow('mask2', mask2)


    # # Generating the final mask to detect red color
    # mask1 = mask1 + mask2

    # cv2.imshow('mask', mask1)


    # return ''

def grayScaleFrame(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def BgrToHsv(frame, low_H, low_S, low_V, high_H, high_S, high_V):
    frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    return cv2.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))
