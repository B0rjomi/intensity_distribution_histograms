import matplotlib.pyplot as plt
import numpy as np
from crop import *


def show_hist(img_path, json_path, n):
    """
    функция строит гистограмму распределения интенсивности пикселей по изображению вырезанной матрицы
    :param img_path: picture path
    :param json_path: json with coordinates
    :param n: picture number
    :return: intensity distribution histogram

    """
    plt.switch_backend('agg') #необходимо снять комментарий с этой строки чтобы гистограмма корректно сохранялась
    crop = crop_image(img_path, json_path, n)
    crop.convert('L')
    img_arr = np.array(crop)
    #ret, crop_thresh = cv2.threshold(img_arr, 130, 255, cv2.THRESH_BINARY)
    b = np.sum(crop, axis=0)
    print(b[:,0].shape)
    print(b[:,0])
    plt.plot(b[:,0])#, bins=b[:,0].shape[0], fc='k', ec='k')
    plt.show()
    plt.savefig(f'hist_1_non_thresh.png')


def show_multiple(img_path, json_path):
    """

    :param img_path: picture path
    :param json_path: json coordinates path
    :return: returns intensity distribution histogram for all cropped matrices from the original image
    """
    plt.switch_backend('agg') # необходимо снять комментарий с этой строки чтобы гистограмма корректно сохранялась
    for i in range(0, 10):
        crop = crop_image(img_path, json_path, i)
        crop.convert('L')
        img_arr = np.array(crop)
        contrast = img_arr.std(axis=0)
        plt.hist(contrast.flatten(), bins=len(contrast), range=(0, 256), fc='k', ec='k')
        plt.show()
        plt.savefig(f'histograms_with_axis_0/pic_8_hist_{i}.png')