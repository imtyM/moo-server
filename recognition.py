import cv2

from template_matching import templateMatching
from contour_matching import contourMatching, determine_best_contours_for_frame
from frame_minipulations import BgrToHsv, loadImagesFromFolder, getROI

videoFolder = './videos/'
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
        if (frame_counter < 260):
            continue
        frame = getROI(frame)
        templates_with_ids = loadImagesFromFolder('./pictures')

        hits = []
        for idx, template_with_id in enumerate(templates_with_ids):
            template = template_with_id[0]
            hit, similarity = contourMatching(frame, getROI(template))
            if hit:
                id = template_with_id[1]
                print(f'Hit on {id} with similarity of {similarity}')
                hits.append((similarity, id, template))

        if len(hits) > 0:
            similarities = [similarity for similarity, name, template in hits]
            best_similarity_index = similarities.index(min(similarities))
            determine_best_contours_for_frame(getROI(hits[best_similarity_index][2]), 'Best hit template', show_frame=True)
            print('Best hit on ID: ', hits[best_similarity_index][1])
        else:
            print('No hit')
        # hsvFrame = BgrToHsv(frame)
        # templateMatching(frame)
        ch = cv2.waitKey(0)
        if ch == 27 or ch == ord('q') or ch == ord('Q'):
            break
