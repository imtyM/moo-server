import cv2 as cv

cap = cv.VideoCapture('./cow_data/WIN_20200907_12_29_56_Pro.mp4')

if cap.isOpened() == False:
    print('Could not open file')
while True:
    ret, frame = cap.read()
    if not ret:
        print('no frame left')
        break
    else:
        cv.imshow('', frame)
