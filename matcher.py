from frame_minipulations import getROI
from contour_matching import determine_best_contours_for_frame

TEMPLATE_FRAME = 0
TEMPLATE_ID = 1

HITS_SIMILARITY = 0
HITS_ID = 1
HITS_TEMPLATE = 2

def matchFrameToTemplates(frame, templates_with_ids, matcher):
    hits = []
    for idx, template_with_id in enumerate(templates_with_ids):
        template = template_with_id[TEMPLATE_FRAME]
        hit, similarity = matcher(frame, template)
        if hit:
            id = template_with_id[TEMPLATE_ID]
            print(f'Hit on {id} with similarity of {similarity}')
            hits.append((similarity, id, template))

    if len(hits) > 0:
        similarities = [similarity for similarity, name, template in hits]
        best_similarity_index = similarities.index(min(similarities))
        cow_id = hits[best_similarity_index][HITS_ID]

        # Show cow that matched, but is hard linked to contour_matching
        # determine_best_contours_for_frame(getROI(hits[best_similarity_index][2]), 'Best hit template', show_frame=True)
        print('Best hit on ID: ', cow_id)
        return cow_id
    else:
        print('No hit')
        return None
