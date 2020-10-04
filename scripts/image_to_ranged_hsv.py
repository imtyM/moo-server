import cv2
from frame_minipulations import *

images = loadImagesFromFolder('./pictures')
hsv_ranged_images = [BgrToHsv(image, 0, 0, 190, 255, 255, 255) for image in images]

for idx, image in enumerate(hsv_ranged_images):
    path = f"./hsv_ranged_images/Cow_{idx}.jpg"
    print(path)
    cv2.imwrite(path, image)
