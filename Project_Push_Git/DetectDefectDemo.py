import cv2
import numpy as np

def empty(a):
    pass
cv2.namedWindow("Tracking")
cv2.resizeWindow("Tracking",640,240)
cv2.createTrackbar("LH", "Tracking", 97, 255, empty) # 97
cv2.createTrackbar("LS", "Tracking", 0, 255, empty)
cv2.createTrackbar("LV", "Tracking", 0, 255, empty)
cv2.createTrackbar("UH", "Tracking", 106, 255, empty)
cv2.createTrackbar("US", "Tracking", 174, 255, empty)
cv2.createTrackbar("UV", "Tracking", 255, 255, empty)

def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: 
                    imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        hor_con = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2: 
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver

def sharpen_image_laplacian(image):
    laplacian = cv2.Laplacian(image, cv2.CV_64F)
    sharpened_image = np.uint8(np.clip(image - 0.3*laplacian, 0, 255))
    return sharpened_image  # Return the sharpened image

def getcoutours(img, imgContour):
    #_,contours, hierachy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours, hierachy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # cv2.RETR_EXTERNAL
    for cnt in contours:
        area = cv2.contourArea(cnt)
        selected_contour = max(contours, key=lambda x: cv2.contourArea(x))
        print("Area of defect",area)
        areaMin = 3000 # Config area
        if area > areaMin:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 255),5)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02* peri, True)  # 0.009
            x, y, w, h = cv2.boundingRect(approx)
            cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 5)
            # cv2.putText(imgContour, "Area: " + str(int(area)), (x + w + 40, y + 65), cv2.FONT_HERSHEY_COMPLEX, 0.7,
            #             (0, 255, 0), 2)
while True:
    image = cv2.imread("D:\DATN\Mechatronics-Project\Project_Push_Git\Image\sample No.6.JPG")
    sharpened_image = sharpen_image_laplacian(image)
    rgb_img = cv2.cvtColor(sharpened_image, cv2.COLOR_BGR2RGB)

    # Convert BGR to HSV 
    HSV_img = cv2.cvtColor(rgb_img,cv2.COLOR_BGR2HSV)

    # Set range for red color and  
    l_h = cv2.getTrackbarPos("LH", "Tracking")
    l_s = cv2.getTrackbarPos("LS", "Tracking")
    l_v = cv2.getTrackbarPos("LV", "Tracking")

    u_h = cv2.getTrackbarPos("UH", "Tracking")
    u_s = cv2.getTrackbarPos("US", "Tracking")
    u_v = cv2.getTrackbarPos("UV", "Tracking")

    l_b = np.array([l_h, l_s, l_v])
    u_b = np.array([u_h, u_s, u_v])

    mask = cv2.inRange(HSV_img, l_b, u_b)

    # Morphological and Dilate
    kernel = np.ones((5,5),np.uint8)
    mask_morpho = cv2.morphologyEx(mask, cv2.MORPH_OPEN,kernel)

    mask_dilate = cv2.dilate(mask_morpho, kernel,iterations=2)
    res = cv2.bitwise_and(image,image, mask=mask_dilate)

    # Warming threshold needed apdative 
    # Detecting contours in image
    thresh, output_threshold = cv2.threshold(res,105, 255, 1, cv2.THRESH_BINARY)
    gray_image = cv2.cvtColor(output_threshold, cv2.COLOR_BGR2GRAY)
    bitwise_img = cv2.bitwise_not(gray_image)

    # Detecting contours in image
    getcoutours(bitwise_img,image)

    imgstack = stackImages(0.8, ([image,output_threshold,bitwise_img], [mask_dilate,mask,res]))
    
    #cv2.imshow("Image Origin",image)
    #cv2.imshow("output_morphology",output_morphology)
    #cv2.imshow("gray",gray_image)
    #cv2.imshow("thresh",output_threshold)
    #cv2.imshow("HSV image",bitwise_img)
    #cv2.imshow("mask dilate", mask_dilate)
    #cv2.imshow("res", res)
    cv2.imshow("Imag stack",imgstack)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break
cv2.destroyAllWindows()