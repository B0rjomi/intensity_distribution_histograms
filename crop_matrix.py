from PIL import Image
import numpy as np
import json
import matplotlib.pyplot as plt


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
    #plt.switch_backend('agg') необходимо снять комментарий с этой строки чтобы гистограмма корректно сохранялась
    crop = crop_image(img_path, json_path, n)
    crop.convert('L')
    img_arr = np.array(crop)
    contrast = img_arr.std(axis=1)
    plt.hist(contrast.flatten(), bins=256, range=(0, 256), fc='k', ec='k')
    plt.show()
    #plt.savefig(f'hist_1.png')


def show_multiple(img_path, json_path):
    """

    :param img_path: picture path
    :param json_path: json coordinates path
    :return: returns intensity distribution histogram for all cropped matrices from the original image
    """
    #plt.switch_backend('agg') необходимо снять комментарий с этой строки чтобы гистограмма корректно сохранялась
    for i in range(0, 10):
        crop = crop_image(img_path, json_path, i)
        crop.convert('L')
        img_arr = np.array(crop)
        contrast = img_arr.std(axis=1)
        plt.hist(contrast.flatten(), bins=256, range=(0, 256), fc='k', ec='k')
        plt.show()
        #plt.savefig(f'histograms/pic_8_hist_{i}.png')












