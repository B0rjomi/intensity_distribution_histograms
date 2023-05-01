import cv2

img = cv2.imread('pics/pic2.jpg', cv2.IMREAD_GRAYSCALE)

ret, thresh1 = cv2.threshold(img, 130, 255, cv2.THRESH_BINARY)

cv2.imwrite('pics/pic2_threshold_130.jpg', thresh1)
cv2.waitKey(0)