import cv2
import numpy as np
import os

class CompareImage(object):

    def __init__(self, image_1, image_2):
        self.minimum_commutative_image_diff = 1
        self.image_1 = image_1
        self.image_2 = image_2

    def compare_image(self):
        # image_1 = cv2.imread(self.image_1_path, 0)
        # image_2 = cv2.imread(self.image_2_path, 0)
        commutative_image_diff = self.get_image_difference(self.image_1, self.image_2)

        if commutative_image_diff < self.minimum_commutative_image_diff:
            return commutative_image_diff
        return 10000 # random failure value

    @staticmethod
    def get_image_difference(image_1, image_2):
        first_image_hist = cv2.calcHist([image_1], [0], None, [256], [0, 256])
        second_image_hist = cv2.calcHist([image_2], [0], None, [256], [0, 256])

        img_hist_diff = cv2.compareHist(first_image_hist, second_image_hist, cv2.HISTCMP_BHATTACHARYYA)
        img_template_probability_match = cv2.matchTemplate(first_image_hist, second_image_hist, cv2.TM_CCOEFF_NORMED)[0][0]
        img_template_diff = 1 - img_template_probability_match

        # taking only 10% of histogram diff, since it's less accurate than template method
        commutative_image_diff = (img_hist_diff / 10) + img_template_diff
        return commutative_image_diff

videoFolder = './cow_data/'
fileName = '1.mp4'
__input = videoFolder + fileName
cap = cv2.VideoCapture(__input)

frame_counter = 0

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

# Returns whether we should break or not - True = break, False - don't =-)
def showFrameWithQuit(frame, frameName = 'frame'):
    cv2.imshow(frameName, frame)
    ch = cv2.waitKey(0)
    if ch == 27 or ch == ord('q') or ch == ord('Q'):
        return True
    else:
        return False

def matchFrame(frame):
    processedFrame = grayScaleFrame(getROI(frame))
    cv2.imshow('processedFrame', processedFrame)
    templates = loadImagesFromFolder('./pictures')
    processedTemplates = [grayScaleFrame(template) for template in templates]

    # templateMatcheCoeffs = [cv2.matchTemplate(processedFrame, template, cv2.TM_CCOEFF_NORMED) for template in processedTemplates]

    for i, template in enumerate(processedTemplates):
        compareObject = CompareImage(processedFrame, template)
        val = compareObject.compare_image()
        if val < 0.65:
            print('value: ', val, ' Matched to: ', i)


def grayScaleFrame(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def loadImagesFromFolder(folder):
    return [cv2.imread(os.path.join(folder, filename)) for filename in os.listdir(folder) if cv2.imread(os.path.join(folder, filename)) is not None]


if cap.isOpened() == False:
    print('Could not open file')


while True:
    ret, frame = cap.read()
    if not ret:
        print('no frame left')
        break
    else:
        frame_counter = frame_counter + 1
        if (frame_counter < 240):
            continue
        print('Showing frame ', frame_counter)
        # cv2.imshow('original', frame)
        matchFrame(frame)
        ch = cv2.waitKey(0)
        if ch == 27 or ch == ord('q') or ch == ord('Q'):
            break

