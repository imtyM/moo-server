import cv2

__input = './1.mp4'
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
        print('Showing frame ', frame_counter)
        cv2.imshow('original', frame)
        ch = cv2.waitKey(1)
        if ch == 27 or ch == ord('q') or ch == ord('Q'):
            break



