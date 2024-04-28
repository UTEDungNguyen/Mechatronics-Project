from rembg import remove 
from PIL import Image
import cv2
import numpy as np
import imutils


print('Done remove background')

def sharpen_image_laplacian(image):
    laplacian = cv2.Laplacian(image, cv2.CV_64F)
    sharpened_image = np.uint8(np.clip(image - 0.3*laplacian, 0, 255))
    return sharpened_image  # Return the sharpened image

img1 = cv2.imread('image\img_4.jpg')
# img_reszie = cv2.resize(img1, (200, 300))
# cv2.imwrite('img_4.png', img_reszie, [cv2.IMWRITE_PNG_COMPRESSION, 0])

inp = r'image\\img_4.jpg'
out = r'image\\img_rmbg.png'

input_img = Image.open(inp)
output = remove(input_img)
output.save(out)

print('Done remove background')

img = cv2.imread(out)
img = cv2.resize(img,(400,500))


gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Thresholding
_, thresh = cv2.threshold(gray,150,255, cv2.THRESH_BINARY)


cv2.imshow('threshold_img', thresh)

# overlay_img = cv2.bitwise_and(img, img, mask=thresh)

# cv2.imshow('overlay_img', overlay_img)
# remove_noise:
kernel = np.ones((3, 3), np.uint8)

sure_bg = cv2.dilate(thresh,kernel, iterations=5)

cv2.imshow('sure_bg',sure_bg)


# # processImage = Img
#  Code chay dc chua toi uu 
contours = cv2.findContours(sure_bg.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
cnts =imutils.grab_contours(contours)
print(f'cnts:{cnts}')
# print(f"cnts[0][9]: {cnts[0][9]}")

convex_hulls = []
img_result = img.copy()

# Calculate convex hulls for each contour
for contour in cnts:
    c_area = cv2.contourArea(contour)
    print(c_area)
    if c_area >=250 and c_area <10000:
        # cv2.drawContours(img_result,[contour], -1, (0,255,0) , 2)
        convex_hull_1= cv2.convexHull(points=contour, clockwise=
                                     False)
        # convex_hull_2= cv2.convexHull(points=convex_hull_1, clockwise=
        #                              False)
        convex_hulls.append(convex_hull_1)

    # print(f'convex_hull: {convex_hull}')
# Draw lines to connect convex hulls
for i in range(len(convex_hulls) - 1):
    cv2.drawContours(img_result, [convex_hulls[i], convex_hulls[i+1]], -1, (0, 255, 0), 2)

# Display the result
cv2.imshow('Connected Contours', img_result)



# # cv2.imshow('shapern_img', sharpen_img)
# # cv2.imshow("img", img_reszie)
# cv2.imshow("dilate",sure_bg)
# cv2.imshow("Thresh", thresh)
# # cv2.imshow("Opening",opening)
# #cv2.imshow("processImage",processImage)
cv2.waitKey(0)
cv2.destroyAllWindows()
