import cv2 as cv

__input = './cow_data/WIN_20200907_12_29_56_Pro.mp4'
cap = cv.VideoCapture(__input)

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
        print('Showing frame ', frame_counter)
        cv.imshow('', frame)
        cv.waitKey(0)
