from PIL import Image
import cv2
import matplotlib.pyplot as plt
import numpy as np

img = Image.open('crop_matrices/pic_1_matrix_1.jpg')

img_array = np.array(img)

# вычисление контрастности пикселов
contrast = img_array.std(axis=0)
bins_sum = img_array.sum(axis=0)

# определение границ бинов
# bins = np.histogram_bin_edges(contrast, bins='auto')


print(len(img_array.sum(axis=0)))
print(len(contrast))