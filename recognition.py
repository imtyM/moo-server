import cv2
import numpy as np

videoFolder = './videos/'
fileName = '2.mp4'
__input = videoFolder + fileName
cap = cv2.VideoCapture(__input)

frame_counter = 0

if cap.isOpened() == False:
    print('Could not open file')

# function to detect the ROI for the cow.
# We need a range of RGB values for the color of the corners - In our case it's red
# The function will interrogate the frame, detect the left most, right most, top most and bottom most pixels,
# anything within that range will be kept, the rest cropped out
# @input - RGB frame
# @return - cropped RGB image only with ROI.
def getROI(frame):
    lowX = 34
    highX = 1250
    lowY = 91
    highY = 542
    cropped = frame[lowY:highY, lowX: highX]
    cv2.imshow('cropped', cropped)
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

while True:
    ret, frame = cap.read()
    if not ret:
        print('no frame left')
        break
    else:
        frame_counter = frame_counter + 1
        print('Showing frame ', frame_counter)
        cv2.imshow('original', frame)
        getROI(frame)
        ch = cv2.waitKey(0)
        if ch == 27 or ch == ord('q') or ch == ord('Q'):
            break



