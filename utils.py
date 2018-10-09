import cv2
import sys
import numpy as np

def denoising(img, min_size = 300):
    """
    Denoise a binarized image. 
    :param img; Binarized image. 
    :return : Denoised image.
    """  
    connectivity = 10
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(img, connectivity, cv2.CV_32S)
    sizes = stats[1:, -1]
    nb_components = nb_components - 1
    img2 = np.zeros((output.shape), np.uint8)
    for i in range(0, nb_components):
        if sizes[i] >= min_size:
            img2[output == i + 1] = 255

    return img2

def deskew(img, color=True):
    """
    Calculate the angle between text in the image and the horizontal line and fix it.
    :param img; Gray scale image. 
    :return : Fixed image.
    """  
    gray = img.copy()
    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    except:
        pass

    if color:   
        bit = cv2.bitwise_not(gray.copy())
        thresh = cv2.threshold(bit, 0, 255 ,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    else:
        thresh = gray
    
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]

    print(cv2.minAreaRect(coords))
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

   
    return rotated