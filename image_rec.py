import cv2
import os
import numpy as np

# Opens the Video file
cap = cv2.VideoCapture('./cow_data/6.mp4')
kernel = np.ones((10, 10),np.uint8)
template = cv2.imread('./hsv_ranged_images/Cow_1.jpg', 0)
frame_counter = 0

while (cap.isOpened()):
    ret, frame = cap.read()
    original = frame
    frame_counter = frame_counter + 1
    if frame_counter < 0:
        continue
    #
    #
    # frame = cv2.resize(frame,(640,480),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
    # img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # img_gray = cv2.bilateralFilter(img_gray,9,75,75)
    # img_gray = cv2.equalizeHist(img_gray)
    # edges = cv2.Canny(img_gray, 100, 200)
    #
    # template = cv2.imread('Cow data/cow5/Cow5.jpg', 0)
    # template = cv2.resize(template,(640,480),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
    # filter = cv2.bilateralFilter(template,9,75,75)
    # template = filter
    # # template1 = cv2.imread('Cow data/cow5/Cow5.jpg', 0)
    # # template1 = cv2.resize(template1, (640, 480), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
    #
    # # template2 = cv2.imread('Saved cows/Cow1/Cow1_temp3.jpg', 0)
    # # template2 = cv2.resize(template2, (640, 480), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
    # ##template2 = cv2.imread('Saved cows/test3.jpg', 0)
    # ##template3 = cv2.imread('Saved cows/test4.jpg', 0)
    # ##template4 = cv2.imread('Saved cows/test5.jpg', 0)
    # ##template5 = cv2.imread('Saved cows/test6.jpg', 0)qqqq
    #
    # w, h = template.shape[::-1]
    # res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    # #res1 = cv2.matchTemplate(img_gray, template1, cv2.TM_CCOEFF_NORMED)
    # #res2 = cv2.matchTemplate(img_gray, template2, cv2.TM_CCOEFF_NORMED)
    # ##res3 = cv2.matchTemplate(img_gray, template3, cv2.TM_CCOEFF_NORMED)
    # #res4 = cv2.matchTemplate(img_gray, template4, cv2.TM_CCOEFF_NORMED)
    # ##res5 = cv2.matchTemplate(img_gray, template5, cv2.TM_CCOEFF_NORMED)
    #
    # threshold = 0.7
    # loc = np.where(res >= threshold) #or res1 >= threshold)# or res2>= threshold)## or res3>= threshold)
    # for pt in zip(*loc[::-1]):
    #     cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 25)
    frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frame = cv2.inRange(frame, (0, 0, 190), (255, 255, 255))
    #frame = cv2.GaussianBlur(frame, (5,5),0)
    frame = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)
    frame = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernel)

    contours, hierachy = cv2.findContours(template, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)[1:]

    template_contours = sorted_contours[0]

    contours, hierachy = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

    smatch = 10
    for c in sorted_contours:
        match = cv2.matchShapes(template_contours,c,1,0.0)

        if match < smatch and cv2.contourArea(c)>10000:
            cnt = c
            smatch = match
            print(match)
            print(cv2.contourArea(c))
    cv2.drawContours(original, cnt, -1, (200,100,0), 3)
    cv2.imshow('Detected', original)
    cv2.imshow('Other', template)

    if cv2.waitKey(50) & 0xFF == ord('c'):
        cv2.imwrite('Saved cows/Cow1/Cow1_extra'+str(save)+'.jpg', frame)
        save+=1

    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

cv2.waitKey(0)
cap.release()
cv2.destroyAllWindows()
