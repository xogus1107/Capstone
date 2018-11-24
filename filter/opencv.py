import numpy as np
import cv2


img = cv2.imread('face.png')
blur = cv2.GaussianBlur(img,(5,5),0)
#blur = cv2.bilateralFilter(img,9,75,75)
#blur = cv2.blur(img,(7,7))
#blur = cv2.medianBlur(img,9)

cv2.imshow('Original', img)
cv2.imshow('Result', blur)
cv2.imwrite('gaussian.jpg',blur)
cv2.waitKey(0)
cv2.destroyAllWindows()