
import cv2
import numpy as np
import imutils

# Đọc ảnh và chuyển đổi sang ảnh grayscale
image = cv2.imread('Mechatronics-Project\image\sr.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Áp dụng GaussianBlur để giảm nhiễu
blurred = cv2.GaussianBlur(gray, (5,5), 0)
# Áp dụng GaussianBlur để giảm nhiễu và làm mịn ảnh


# Sử dụng phương pháp Canny để phát hiện biên
edges = cv2.Canny(blurred, 105,110)

kernel = np.ones((5, 5), np.uint8)
morphological_image = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)


dilated = cv2.dilate(morphological_image, None, iterations=2)
# # # Tìm contours trong ảnh
# _, img_binary = cv2.threshold( morphological_image,255, cv2.THRESH_BINARY_INV)
contours = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts =imutils.grab_contours(contours)
img_result = image.copy()
countContours = 0
num=0
for cnt in cnts:
    num+=1
    c_area = cv2.contourArea(cnt)
    print(f'area {num}= {c_area}')
    countContours += 1
    if c_area>450:
         cv2.drawContours(img_result,[cnt], -1, (0,255,0) , 2)
    else: pass


# markers = np.zeros_like(image)
markers = cv2.connectedComponents(morphological_image)[1]

# Đánh số mỗi vùng cần tách trên mask
marker_id = 1
for c in contours: 
    cv2.drawContours(markers, [cnt], -1, (marker_id), -1)
    marker_id += 1
# markers = np.int32(markers)
new_img=cv2.imread('Mechatronics-Project\image\sr.png')
print("Type of image:", image.dtype)
print("Shape of image:", image.shape)
# Áp dụng Watershed để tách vùng
cv2.watershed(new_img, markers)
# In đánh dấu trên ảnh gốc
image[markers == -1] = [0, 0, 255]  # Đánh dấu các vùng tách bằng màu đỏ

markers_display = cv2.convertScaleAbs(markers)

    

# Hiển thị ảnh gốc và ảnh với contours
cv2.imshow('Original Image', image)
cv2.imshow('Mophol Image', morphological_image)
cv2.imshow('Image with Contours', img_result)
cv2.imshow('Image ', edges)
cv2.imshow('Watershed Segmentation', markers_display)


# Hiển thị ảnh
# cv2.imshow('Image with Corners', img_result)
cv2.waitKey(0)
cv2.destroyAllWindows()
# Trong đoạn mã trên:





