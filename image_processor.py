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
            fileName = 'tarp_2.mp4'
            __input = videoFolder + fileName
            self.cap = cv2.VideoCapture(__input)
            self.cap.set(1, 170)
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
                frame = getROI(frame)
                templates_with_ids = loadImagesFromFolder('./pictures')
                matchFrameToTemplates(frame, templates_with_ids, contourMatching)

                # hsvFrame = BgrToHsv(frame)
                # templateMatching(frame)
                ch = cv2.waitKey(0)
                if ch == 27 or ch == ord('q') or ch == ord('Q'):
                    break

    def detectCow(self, valid):
        if not valid:
            return None
        ret, frame = self.cap.read()
        if not ret:
            print('Something went wrong reading from the camera')
            return None

        frame = getROI(frame)
        ## XXX: this should be cached
        templates_with_ids = loadImagesFromFolder('./pictures')
        return matchFrameToTemplates(frame, templates_with_ids, contourMatching)




