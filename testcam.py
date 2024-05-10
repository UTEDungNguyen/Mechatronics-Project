import cv2 
import numpy as np

file_path =r'Result Remove Background/img_processed.jpg'
img = cv2.imread(file_path)
cv2.imshow('ajha',img)


cv2.waitKey(0)
cv2.destroyAllWindows()