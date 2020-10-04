import cv2
import numpy as np
import random as rng

from frame_minipulations import BgrToHsv

AREA_THRESHOLD = 15
SHAPE_SIMILARITY_THRESHOLD = 0.2

def contourMatching(frame, template):
    frame_best_contours = determine_best_contours_for_frame(frame, 'frame')
    template_best_contours = determine_best_contours_for_frame(template, 'template', True)
    match_best_contours(frame_best_contours, template_best_contours)

def determine_best_contours_for_frame(frame, name, template=False):
    frame_HSV = BgrToHsv(frame, 0, 0, 140, 255, 255, 255)
    # cv2.imshow(name, frame_HSV)
    # morphed_frame = apply_morphological_transform(frame_HSV)
    frame_contours, _ = cv2.findContours(frame_HSV, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    filtered_contours = filter_small_contours(frame_contours, template)
    frame_with_contours = draw_frame_with_contours(frame, filtered_contours)

    title = f'{name} contours'
    cv2.imshow(title, frame_with_contours)

    return filtered_contours

def apply_morphological_transform(frame):
    kernel = np.ones((10, 10),np.uint8)
    open_frame = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)
    close_frame = cv2.morphologyEx(open_frame, cv2.MORPH_CLOSE, kernel)
    return close_frame

def draw_frame_with_contours(frame, contours, name='Contours'):
    frame_copy = frame[:]
    for idx, countour in enumerate(contours):
        color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
        cv2.drawContours(frame_copy, contours, idx, color, 3)
    return frame_copy

def filter_small_contours(contours, template=False):
    if template:
        return sorted(contours, key=cv2.contourArea, reverse=True)[0:1]
    return sorted(contours, key=cv2.contourArea, reverse=True)[:5]

def match_best_contours(frame_contours, template_contours):
    contours_similarity = []
    for frame_contour in frame_contours:
        for template_contour in template_contours:
            contours_match, similarity = match_contours(frame_contour, template_contour)
            if contours_match:
                contours_similarity.append(similarity)
    print(contours_similarity)
    # do something

def match_contours(frame_contour, template_contour):
    if not areas_match(frame_contour, template_contour):
        return False, 1

    similarity = cv2.matchShapes(frame_contour,template_contour, 1, 0.0)

    print('Areas match with similarity of: ', similarity)
    if similarity <= SHAPE_SIMILARITY_THRESHOLD:
        return True, similarity
    return False, 1

def areas_match(frame_contour, template_contour):
    frame_contour_area = cv2.contourArea(frame_contour)
    template_contour_area = cv2.contourArea(template_contour)
    percentage_difference = abs(
        ( frame_contour_area - template_contour_area )/ frame_contour_area
    ) * 100

    print('Area percentage difference: ', percentage_difference)
    if percentage_difference <= AREA_THRESHOLD:
        return True
    return False
