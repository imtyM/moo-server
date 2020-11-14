import cv2
import numpy as np
from numpy.linalg import norm
from scipy.interpolate import splprep, splev

from frame_minipulations import BgrToHsv

AREA_THRESHOLD = 20
SHAPE_SIMILARITY_THRESHOLD = 0.25

def contourMatching(frame, template):
    # frame_brightness = np.average(norm(frame, axis=2)) / np.sqrt(3)
    # template_brightness = np.average(norm(template, axis=2)) / np.sqrt(3)
    # print('Frame brightness ', frame_brightness)
    # print('Template brightness ', template_brightness)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        sys.exit(1)

    frame_best_contours = determine_best_contours_for_frame(frame, 'frame', show_frame=True)
    template_best_contours = determine_best_contours_for_frame(template, 'template', template=False, show_frame=False)

    hits, similarity, matching_frame_contour, matching_template_contour = match_best_contours(frame_best_contours, template_best_contours)
    # if matching_frame_contour is not None:
        # hull = cv2.convexHull(matching_frame_contour)
        # matching_frame_with_contour = draw_frame_with_contours(frame, [ matching_frame_contour ])
        # matching_template_with_contour = draw_frame_with_contours(template, [ matching_template_contour ])
        # cv2.imshow('matching frame contour', matching_frame_with_contour)
        # cv2.imshow('matching template contour', matching_template_with_contour)
    return hits, similarity

def determine_best_contours_for_frame(frame, name, template=False, show_frame=False):
    if show_frame and template:
        cv2.imshow('Normal template', frame)
    frame_HSV = BgrToHsv(frame, 0, 0, 180, 255, 255, 255)
    if show_frame and template:
        cv2.imshow('HSV transform', frame_HSV)
    morphed_frame = apply_morphological_transform(frame_HSV)
    if show_frame and template:
        cv2.imshow('morpho transform', morphed_frame)
    frame_contours, _ = cv2.findContours(morphed_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    filtered_contours = filter_small_contours(frame_contours, template)
    smoothened_contours = smoothen_contours(filtered_contours)
    if show_frame:
        frame_with_contours = draw_frame_with_contours(morphed_frame, smoothened_contours)

        title = f'{name} contours'
        cv2.imshow(title, frame_with_contours)

    return smoothened_contours

def apply_morphological_transform(frame):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    dilated = cv2.erode(frame, kernel)
    return dilated

def draw_frame_with_contours(frame, contours, name='Contours'):
    frame_copy = frame[:]
    cv2.drawContours(frame_copy, contours, -1, (180, 180, 180), 3)
    return frame_copy

def filter_small_contours(contours, template=False):
    largest_contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    return [contour for contour in largest_contours if cv2.contourArea(contour) > 2000]

def match_best_contours(frame_contours, template_contours):
    contours_with_similarity = []
    for frame_contour in frame_contours:
        for template_contour in template_contours:
            contours_match, similarity = match_contours(frame_contour, template_contour)
            if contours_match:
                contours_with_similarity.append((similarity, frame_contour, template_contour))

    similarities_exist = len(contours_with_similarity) > 0
    #TODO: Do weighted average here.
    # frame_similarity = np.average(contours_similarity)
    similarities = [similarity for similarity, fc, tc in contours_with_similarity]
    frame_similarity = np.min(similarities or 0)
    if similarities_exist and frame_similarity <= SHAPE_SIMILARITY_THRESHOLD:
        index_of_matching_contour = similarities.index(frame_similarity)
        matching_frame_contour = contours_with_similarity[index_of_matching_contour][1]
        matching_template_contour = contours_with_similarity[index_of_matching_contour][2]
        return True, frame_similarity, matching_frame_contour, matching_template_contour
    return False, 1, None, None

def match_contours(frame_contour, template_contour):
    if not areas_match(frame_contour, template_contour):
        return False, 1

    # hull_frame_contour = cv2.convexHull(frame_contour)
    # hull_template_contour = cv2.convexHull(template_contour)
    hull_frame_contour = frame_contour
    hull_template_contour = template_contour
    similarity = cv2.matchShapes(hull_template_contour,hull_frame_contour, 3, 0.0)

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

# # NOTE: This is really really expensive, need an alt
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

