import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def dilate_thresh(img_path):
    """
    применяет к вырезанной матрице функцию adaptive threshold c фиксированными параметрами
    :param img_path: cropped matrix path
    :return: thresholded picture
    """
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    thresh = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 17, 17)
    # kernel = np.array([[0,1], [0,1]], dtype=np.uint8)
    kernel = np.ones((2, 2), np.uint8)
    erode_img = thresh # cv2.dilate(thresh, kernel)
    b = np.sum(erode_img, axis=0)
    plt.plot(b)
    plt.show()
    cv2.imwrite('thresholded/pic2_ones.jpg', erode_img)

def dilate_for_all(dir_path):
    """
    применяет ко всем вырезанным матрицам в каталоге adaptive threshold
    :param dir_path:
    :return:
    """
    # kernel = np.ones((2,2), np.uint8)
    for filename in os.listdir(dir_path):
        #print(filename)
        new_file = cv2.imread(dir_path + '/' + filename, cv2.IMREAD_GRAYSCALE)
        #print(new_file)
        thresh = cv2.adaptiveThreshold(new_file, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 15)
        b = np.sum(thresh, axis=0)
        cv2.imwrite(f'thresholded/{filename}', thresh)