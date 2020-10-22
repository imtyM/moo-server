import cv2

from contour_matching import contourMatching, determine_best_contours_for_frame
from frame_minipulations import BgrToHsv, loadImagesFromFolder, getROI
from matcher import matchFrameToTemplates

class ImageProcessor():
    def __init__(self, debug=False):
        self.cap = None
        self.setupImageProcessing(debug=debug)

    def setupImageProcessing(self, debug=False):
        print('=========================\n')
        print('Setting up image processor')
        if debug:
            videoFolder = './videos/'
            fileName = '1.mp4'
            __input = videoFolder + fileName
            self.cap = cv2.VideoCapture(__input)
        else:
            self.cap = cv2.VideoCapture(0)

        if self.cap is None or not self.cap.isOpened():
            print('Trouble setting up the image processor. Does your pc even have a video input?😕\n ImageProcessor NOT setup.🖕\n\n')
            return

        print ('Image processor setup complete.👌\n\n')

    def debugLoop(self):
        frame_counter = 0
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print('no frame left')
                break
            else:
                frame_counter = frame_counter + 1
                if (frame_counter < 260):
                    continue
                frame = getROI(frame)
                templates_with_ids = loadImagesFromFolder('./pictures')
                matchFrameToTemplates(frame, templates_with_ids, contourMatching)

                # hsvFrame = BgrToHsv(frame)
                # templateMatching(frame)
                ch = cv2.waitKey(0)
                if ch == 27 or ch == ord('q') or ch == ord('Q'):
                    break

