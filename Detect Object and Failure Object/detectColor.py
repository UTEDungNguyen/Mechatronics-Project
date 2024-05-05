import cv2
import numpy as np
img1 = cv2.imread("Test1(2).png")
img = cv2.imread("Test1(2).png",cv2.IMREAD_GRAYSCALE)

gray = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
# Apply adaptive thresholding
ret,threshold = cv2.threshold(gray,120,255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
thresholded_image = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
kernel = np.ones((3, 3), np.uint8)
opening = cv2.morphologyEx(thresholded_image,cv2.MORPH_OPEN,kernel, iterations=2)
laplacian = cv2.Laplacian(img,cv2.CV_64F)
sobelx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)
sobely = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5)




# Show the thresholded image
cv2.imshow(" Image input",img1)
cv2.imshow("Threshold",threshold)
cv2.imshow("Thresholded Image", thresholded_image)
cv2.imshow("opening",opening)
cv2.imshow("Laplancian",laplacian)
cv2.waitKey(0)
cv2.destroyAllWindows()



