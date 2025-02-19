# ### Author: Matiur Rahman Minar ###
# ### EMCOM Lab, SeoulTech, 2021 ###
# ### Task: Generating binary mask/silhouette/segmentation ###
# ### especially for clothing image ###
# ### Focused method: Binary thresholding ###


# import os
# import cv2
# import numpy as np
# from PIL import Image

# # helper function
# def cloth_masking(im_path, save_path):
#     img = cv2.imread(im_path, 0)
#     img1 = Image.open(im_path).convert('RGB')
#     lo = 250
#     hi = 255

#     # ret,thresh1 = cv2.threshold(img, lo, hi,cv2.THRESH_BINARY)
#     ret,th_bin = cv2.threshold(img, lo, hi, cv2.THRESH_BINARY_INV)
#     # ret,thresh3 = cv2.threshold(img, lo, hi,cv2.THRESH_TRUNC)
#     # ret,thresh4 = cv2.threshold(img, lo, hi,cv2.THRESH_TOZERO)
#     # ret,thresh5 = cv2.threshold(img, lo, hi,cv2.THRESH_TOZERO_INV)
#     # ret, thresh3 = cv2.threshold(img, lo, hi, cv2.THRESH_OTSU+cv2.THRESH_BINARY)
#     # th_otsu = cv2.bitwise_not(thresh3)
#     # thresh4 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
#     # th_mean = cv2.bitwise_not(thresh4)
#     # thresh5 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
#     # th_gauss = cv2.bitwise_not(thresh5)

#     # Filling operation:
#     # Copy the thresholded image.
#     im_floodfill = th_bin.copy()
#     # Mask used to flood filling.
#     # Notice the size needs to be 2 pixels than the image.
#     h, w = th_bin.shape[:2]
#     mask = np.zeros((h+2, w+2), np.uint8)
#     # Floodfill from point (0, 0)
#     cv2.floodFill(im_floodfill, mask, (0,0), 255);
#     # Invert floodfilled image
#     im_floodfill_inv = cv2.bitwise_not(im_floodfill)
#     # Combine the two images to get the foreground.
#     th_filled = th_bin | im_floodfill_inv

#     # Morphology operation:
#     kernel = np.ones((2,2),np.uint8)

#     # opening for salt noise removal
#     th_opened = cv2.morphologyEx(th_filled, cv2.MORPH_OPEN, kernel)

#     # closing for pepper noise removal (not needed it seems)
#     # th_closed = cv2.morphologyEx(th_opened, cv2.MORPH_CLOSE, kernel)

#     # erosion for thinning out boundary
#     kernel = np.ones((3,3),np.uint8)
#     th_eroded = cv2.erode(th_opened,kernel,iterations=1)

#     # save result
#     print("Saving ", save_path)
#     cv2.imwrite(save_path, th_eroded)
    
#     return True

import os
import cv2
import numpy as np
from PIL import Image

# Helper function
def cloth_masking(im_path, save_path):
    img = cv2.imread(im_path, 0)  # Read image in grayscale
    img1 = Image.open(im_path).convert('RGB')
    
    # Use Otsu's method to determine the optimal threshold value
    ret, th_bin = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Filling operation
    im_floodfill = th_bin.copy()
    h, w = th_bin.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
    cv2.floodFill(im_floodfill, mask, (0, 0), 255)
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)
    th_filled = th_bin | im_floodfill_inv

    # Morphology operation
    kernel = np.ones((2, 2), np.uint8)
    th_opened = cv2.morphologyEx(th_filled, cv2.MORPH_OPEN, kernel)
    kernel = np.ones((3, 3), np.uint8)
    th_eroded = cv2.erode(th_opened, kernel, iterations=1)

    # Save result
    print("Saving", save_path)
    cv2.imwrite(save_path, th_eroded)
    
    return True
    
