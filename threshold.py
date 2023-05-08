import cv2
import numpy as np

img = cv2.imread('pics/pic2.jpg', cv2.IMREAD_GRAYSCALE)
kernel = np.ones((5, 5), np.uint8)
thresh1 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)

erode_img = cv2.erode(thresh1, kernel)
cv2.imwrite('pics/erode_thresh.jpg', erode_img)
cv2.waitKey(0)