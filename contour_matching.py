import cv2
import numpy as np
from numpy.linalg import norm
import random as rng
from scipy.interpolate import splprep, splev

from frame_minipulations import BgrToHsv

AREA_THRESHOLD = 10
SHAPE_SIMILARITY_THRESHOLD = 0.25

def contourMatching(frame, template):
    frame_brightness = np.average(norm(frame, axis=2)) / np.sqrt(3)
    template_brightness = np.average(norm(template, axis=2)) / np.sqrt(3)
    # print('Frame brightness ', frame_brightness)
    # print('Template brightness ', template_brightness)

    frame_best_contours = determine_best_contours_for_frame(frame, 'frame', show_frame=True)
    template_best_contours = determine_best_contours_for_frame(template, 'template')
    return match_best_contours(frame_best_contours, template_best_contours)

def determine_best_contours_for_frame(frame, name, template=False, show_frame=False):
    frame_HSV = BgrToHsv(frame, 0, 0, 150, 255, 255, 255)
    morphed_frame = apply_morphological_transform(frame_HSV)
    frame_contours, _ = cv2.findContours(morphed_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    filtered_contours = filter_small_contours(frame_contours, template)
    # smoothened_contours = smoothen_contours(filtered_contours)
    if show_frame:
        frame_with_contours = draw_frame_with_contours(morphed_frame, filtered_contours)

        title = f'{name} contours'
        cv2.imshow(title, frame_with_contours)

    return filtered_contours

def apply_morphological_transform(frame):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,15))
    dilated = cv2.erode(frame, kernel)
    return dilated

def draw_frame_with_contours(frame, contours, name='Contours'):
    frame_copy = frame[:]
    cv2.drawContours(frame_copy, contours, -1, (180, 180, 180), 3)
    return frame_copy

def filter_small_contours(contours, template=False):
    if template:
        return sorted(contours, key=cv2.contourArea, reverse=True)[1:2]
    largest_contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    return [contour for contour in largest_contours if cv2.contourArea(contour) > 2000]

def match_best_contours(frame_contours, template_contours):
    contours_similarity = []
    for frame_contour in frame_contours:
        for template_contour in template_contours:
            contours_match, similarity = match_contours(frame_contour, template_contour)
            if contours_match:
                contours_similarity.append(similarity)

    similarities_exist = len(contours_similarity) > 0
    #TODO: Do weighted average here.
    # frame_similarity = np.average(contours_similarity)
    frame_similarity = np.min(contours_similarity or 0)
    if similarities_exist and frame_similarity <= SHAPE_SIMILARITY_THRESHOLD:
        return True, frame_similarity
    return False, 1

def match_contours(frame_contour, template_contour):
    if not areas_match(frame_contour, template_contour):
        return False, 1

    similarity = cv2.matchShapes(frame_contour,template_contour, 1, 0.0)

    if similarity <= SHAPE_SIMILARITY_THRESHOLD:
        return True, similarity
    return False, 1

def areas_match(frame_contour, template_contour):
    frame_contour_area = cv2.contourArea(frame_contour)
    template_contour_area = cv2.contourArea(template_contour)
    percentage_difference = abs(
        ( frame_contour_area - template_contour_area )/ frame_contour_area
    ) * 100

    if percentage_difference <= AREA_THRESHOLD:
        return True
    return False

def smoothen_contours(contours):
    smoothened = []
    for contour in contours:
        x,y = contour.T
        # Convert from numpy arrays to normal arrays
        x = x.tolist()[0]
        y = y.tolist()[0]
        # https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.interpolate.splprep.html
        tck, u = splprep([x,y], u=None, s=1.0, per=1)
        # https://docs.scipy.org/doc/numpy-1.10.1/reference/generated/numpy.linspace.html
        u_new = np.linspace(u.min(), u.max(), 25)
        # https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.interpolate.splev.html
        x_new, y_new = splev(u_new, tck, der=0)
        # Convert it back to numpy format for opencv to be able to display it
        res_array = [[[int(i[0]), int(i[1])]] for i in zip(x_new,y_new)]
        smoothened.append(np.asarray(res_array, dtype=np.int32))
    return smoothened

