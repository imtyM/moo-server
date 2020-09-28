import cv2
import os
import numpy as np


import cv2

# Opens the Video file
cap = cv2.VideoCapture('Saved cows/Cow1/test.mp4')
i = 0
save = 0

template_supports = []
while (cap.isOpened()):
    ret, frame = cap.read()
    frame = cv2.resize(frame,(640,480),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('Saved cows/Cow1/Cow1_temp0.jpg', 0)
    template = cv2.resize(template,(640,480),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)

    template1 = cv2.imread('Saved cows/Cow1/Cow1_temp2.jpg', 0)
    template1 = cv2.resize(template1, (640, 480), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)

    template2 = cv2.imread('Saved cows/Cow1/Cow1_temp3.jpg', 0)
    template2 = cv2.resize(template2, (640, 480), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
    ##template2 = cv2.imread('Saved cows/test3.jpg', 0)
    ##template3 = cv2.imread('Saved cows/test4.jpg', 0)
    ##template4 = cv2.imread('Saved cows/test5.jpg', 0)
    ##template5 = cv2.imread('Saved cows/test6.jpg', 0)qqqq

    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    res1 = cv2.matchTemplate(img_gray, template1, cv2.TM_CCOEFF_NORMED)
    res2 = cv2.matchTemplate(img_gray, template2, cv2.TM_CCOEFF_NORMED)
    ##res3 = cv2.matchTemplate(img_gray, template3, cv2.TM_CCOEFF_NORMED)
    #res4 = cv2.matchTemplate(img_gray, template4, cv2.TM_CCOEFF_NORMED)
    ##res5 = cv2.matchTemplate(img_gray, template5, cv2.TM_CCOEFF_NORMED)

    threshold = 0.7
    loc = np.where(res >= threshold or res1 >= threshold or res2>= threshold)## or res3>= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 25)

    cv2.imshow('Detected', frame)

    if cv2.waitKey(1) & 0xFF == ord('c'):
        cv2.imwrite('Saved cows/Cow1/Cow1_extra'+str(save)+'.jpg', frame)
        save+=1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.waitKey(0)
cap.release()
cv2.destroyAllWindows()