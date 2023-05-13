from PIL import Image
import numpy as np
import json
import matplotlib.pyplot as plt
import cv2
from pathlib import Path
import os


def crop_image(img_path, json_path, n):
    """
    :param img_path: picture path
    :param json_path: json with coordinates
    :param n: picture number
    :return: cropped image from the original image
    """
    values = []
    try:
        img = Image.open(img_path)
    except FileNotFoundError:
        print(f"file with {img_path} doesn't exist")
    with open(json_path, 'r') as json_1:
        data = json.load(json_1)
    sorted_data = dict(sorted(data[n].items()))
    for value in sorted_data.values():
        values.append(value)
    print(sorted_data)
    left = sorted_data['x1']
    right = sorted_data['x2']
    upper = sorted_data['y1']
    lower = sorted_data['y2']
    if right < left:
        left = sorted_data['x2']
        right = sorted_data['x1']
    if lower < upper:
        upper = sorted_data['y2']
        lower = sorted_data['y1']
    print(left, upper, right, lower)
    crop_img = img.crop((left, upper, right, lower))
    return crop_img


def multiple_crop(img_path, json_path):
    for i in range(0, 10):
        matrix = crop_image(img_path, json_path, i)
        matrix.save(f'crop_matrices/pic_8_matrix_{i}.jpg')


def show_hist(img_path, json_path, n):
    """
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


def erode_thresh(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    thresh = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 17, 17)
    # kernel = np.array([[0,1], [0,1]], dtype=np.uint8)
    kernel = np.ones((2, 2), np.uint8)
    erode_img = thresh # cv2.dilate(thresh, kernel)
    b = np.sum(erode_img, axis=0)
    plt.plot(b)
    plt.show()
    cv2.imwrite('thresholded/pic2_ones.jpg', erode_img)

def erode_for_all(dir_path):
    # kernel = np.ones((2,2), np.uint8)
    for filename in os.listdir(dir_path):
        #print(filename)
        new_file = cv2.imread(dir_path + '/' + filename, cv2.IMREAD_GRAYSCALE)
        #print(new_file)
        thresh = cv2.adaptiveThreshold(new_file, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 15)
        b = np.sum(thresh, axis=0)
        cv2.imwrite(f'thresholded/{filename}', thresh)


def morph(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 15)
    kernel = np.ones((1, 1), np.uint8)
    # kernel = np.array([[0, 1], [0, 1]], dtype=np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    cv2.imwrite('morph.jpg', opening)


def delete_black_dots(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    # бинаризация изображения
    _, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    print(cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # удаление мелких объектов
    kernel = np.ones((2, 2), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    # удаление вертикальных и горизонтальных линий
    kernel_h = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 1))
    kernel_v = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 3))
    img_h = cv2.morphologyEx(opening, cv2.MORPH_OPEN, kernel_h)
    img_v = cv2.morphologyEx(opening, cv2.MORPH_OPEN, kernel_v)
    result = img_v + img_h
    cv2.imwrite('result1.jpg', result)


def delete_for_all_pics(dir_path):
    for filename in os.listdir(dir_path):
        img = cv2.imread(dir_path + '/' + filename, cv2.IMREAD_GRAYSCALE)
        _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        kernel = np.ones((2,2), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
        kernel_h = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 1))
        kernel_v = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 3))
        img_h = cv2.morphologyEx(opening, cv2.MORPH_OPEN, kernel_h)
        img_v = cv2.morphologyEx(opening, cv2.MORPH_OPEN, kernel_v)
        result = img_v + img_h
        cv2.imwrite(f'dots_deleted_with_nine/{filename}', result)









