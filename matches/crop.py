import os
import cv2

#dir with images
dir_name = "../test_dataset_1/vid220706_230729-opencv/"
dir = os.listdir(dir_name)

i = 1
# Load Images
for name_img in dir:
    print(f"--> Crop {i} image")
    # name_img = "frame0:00:15.00.jpg"
    img = cv2.imread(dir_name + name_img)

    # Prepare crop area
    width, height = 320, 320
    x, y = 0, 30

    # Crop image to specified area using slicing
    crop_img = img[y:y+height, 0:width]
    cv2.imwrite(f'imgs/crop_imgs/crop_{name_img}', crop_img)

    i += 1
