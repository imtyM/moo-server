from frame_minipulations import *
import cv2

class CompareImage(object):
    # @staticmethod
    # def get_image_difference(image_1, image_2):
        # first_image_hist = cv2.calcHist([image_1], [0], None, [256], [0, 256])
        # second_image_hist = cv2.calcHist([image_2], [0], None, [256], [0, 256])

        # img_hist_diff = cv2.compareHist(first_image_hist, second_image_hist, cv2.HISTCMP_BHATTACHARYYA)
        # img_template_probability_match = cv2.matchTemplate(first_image_hist, second_image_hist, cv2.TM_CCOEFF_NORMED)[0][0]
        # img_template_diff = 1 - img_template_probability_match

        # # taking only 10% of histogram diff, since it's less accurate than template method
        # commutative_image_diff = (img_hist_diff / 10) + img_template_diff
        # return commutative_image_diff

    @staticmethod
    def get_image_difference(image_1, image_2):
        img_template_probability_match = cv2.matchTemplate(image_1, image_2, cv2.TM_CCOEFF_NORMED)[0][0]
        img_template_diff = 1 - img_template_probability_match

        return img_template_diff

def templateMatching(frame):
    processedFrame = grayScaleFrame(frame)
    cv2.imshow('processedFrame', processedFrame)
    templates = loadImagesFromFolder('./pictures')
    processedTemplates = [grayScaleFrame(template) for template in templates]

    # templateMatcheCoeffs = [cv2.matchTemplate(processedFrame, template, cv2.TM_CCOEFF_NORMED) for template in processedTemplates]

    bestVal = 1000
    bestTemplate = None
    for template in processedTemplates:
        val = CompareImage.get_image_difference(processedFrame, template)
        if val < bestVal:
            bestVal = val
            bestTemplate = template
    print(bestVal)

    if bestVal < 0.35 and bestTemplate is not None:
        print('Best match?')
        cv2.imshow('Best match', bestTemplate)
