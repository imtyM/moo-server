import cv2

from template_matching import templateMatching
from contour_matching import contourMatching
from frame_minipulations import BgrToHsv

videoFolder = './cow_data/'
fileName = '1.mp4'
__input = videoFolder + fileName
cap = cv2.VideoCapture(__input)

frame_counter = 0

if cap.isOpened() == False:
    print('Could not open file')


while True:
    ret, frame = cap.read()
    if not ret:
        print('no frame left')
        break
    else:
        frame_counter = frame_counter + 1
        if (frame_counter < 200):
            continue
        print('Showing frame ', frame_counter)
        # cv2.imshow('original', frame)
        template = cv2.imread('./pictures/Cow1.jpg')
        contourMatching(frame, template)
        # hsvFrame = BgrToHsv(frame)
        # templateMatching(frame)
        ch = cv2.waitKey(0)
        if ch == 27 or ch == ord('q') or ch == ord('Q'):
            break
