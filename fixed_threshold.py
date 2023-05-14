import cv2
import numpy as np
import os


def delete_black_dots(img_path):
    """
    функция применяет метод threshold к обрезанной матрице так, что выходное изображение содержит меньше помех
    в виде мелких черных точек
    :param img_path: cropped matrix path
    :return: thresholded image
    """
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    # бинаризация изображения
    _, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    print(cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # удаление мелких объектов
    kernel = np.ones((2, 2), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    # удаление вертикальных и горизонтальных линий
    kernel_h = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 1)) # не нужно
    kernel_v = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 3)) # не нужно
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