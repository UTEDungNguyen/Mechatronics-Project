import cv2
import numpy as np
import math
from PIL import Image
import imutils
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import os


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

# Remove background to detect object image
# Initialize the SelfiSegmentation module
segmentor = SelfiSegmentation()
# Set the directory containing images and the directory to save the processed images
input_image_dir = "Image"
output_image_dir = "Result_Remove_Background"
# List all image files in the directory
image_files = [os.path.join(input_image_dir, filename) for filename in os.listdir(input_image_dir) if filename.endswith(('.JPG', '.png', '.jpeg','.jpg'))]

# Ensure there are images in the directory
if not image_files:
    print("No images found in the directory.")
else:
    # Process each image in the directory
    for img_path in image_files:
        # Read the image
        img = cv2.imread(img_path)
        # Perform background removal
        img_out = segmentor.removeBG(img,cutThreshold=0.85)  # Adjust threshold as needed
        # Get the filename (without extension) from the input image path
        filename = os.path.splitext(os.path.basename(img_path))[0]

        # Save the processed image to the output directory
        output_path = os.path.join(output_image_dir, f"{filename}_processed.jpg")
        cv2.imwrite(output_path, img_out)

# Create the output directory if it doesn't exist
if not os.path.exists(output_image_dir):
    os.makedirs(output_image_dir)

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

def getcoutours_ObjectDetect(img, imgContour):
    #_,contours, hierachy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours, hierachy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # cv2.RETR_EXTERNAL
    for cnt in contours:
        area = cv2.contourArea(cnt)
        selected_contour = max(contours, key=lambda x: cv2.contourArea(x))
        areaMin = 1000 # Config area
        if area > areaMin: 
            print("Area of object durian (pixel): ",area) 
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 7)
            M = cv2.moments(cnt)
            cx= int(M["m10"]/M["m00"])
            cy= int(M["m01"]/M["m00"])  
            
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02* peri, True) # 0.02
            x, y, w, h = cv2.boundingRect(approx)
            ellipse = cv2.fitEllipse(selected_contour)
           
            # Unpack the array into separate variables
            center = ellipse[0]
            semi_majorAxis = (ellipse[1][0])/2
            semi_minorAxis = (ellipse[1][1])/2
            angle = ellipse[2]

            # Caculate the elipse for classification durian
            area_elipse =math.pi * semi_majorAxis * semi_minorAxis
            area_elipse = "{:.3f}".format(area_elipse)
            area_elipse = float(area_elipse)
            print("Area of the elipse classification (pixel):", area_elipse)
            # Classification Durian 
            result_sub = area_elipse - area
            # Convert the result of sub to perentage
            result_percent = result_sub/area_elipse
            result_percent = "{:.3f}".format(result_percent)
            result_percent = float(result_percent)
            print("Area of substraction (pixel): ",result_percent)
            if (result_percent < 0.2) : # 20% 
                 print("Durian meet standards")
            else:
                print("Durian does not meet standards")
            
            # Draw the elipse classification and object 
            cv2.ellipse(img_detect_object, ellipse, (0, 255, 0), 3)
            cv2.circle(img_detect_object,(cx,cy),7,(0,0,255),-1)
            cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 5)
        
def sharpen_image_laplacian(image):
    laplacian = cv2.Laplacian(image, cv2.CV_64F)
    sharpened_image = np.uint8(np.clip(image - 0.3*laplacian, 0, 255))
    return sharpened_image  # Return the sharpened image

def getcoutours_DefectDetect(img, imgContour):
    #_,contours, hierachy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours, hierachy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # cv2.RETR_EXTERNAL
    for cnt in contours:
        area = cv2.contourArea(cnt)
        selected_contour = max(contours, key=lambda x: cv2.contourArea(x))
        areaMin = 3000 # Config area
        if area > areaMin:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 255),5)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.009* peri, True)  # 0.009
            x, y, w, h = cv2.boundingRect(approx)
            cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 5)

while True:
    image = cv2.imread("D:\DATN\Mechatronics-Project\Project_Push_Git\Result_Remove_Background\sample No.16_processed.jpg")
    image = cv2.resize(image,(400,300))
    # Divide input from image and processing in the Detect_Object class and Detect_Defect
    img_detect_object = image.copy()
    img_detect_defect = image.copy()

    # Classification the Object Detect Durian
    gray = cv2.cvtColor(img_detect_object, cv2.COLOR_BGR2GRAY)
    # Warming threshold needed apdative
    # Convert Binary Image using method threshold
    thresh, output_otsuthresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # Erosion image to detect Object Elipse for Durian 
    kernel = np.ones((3,3),np.uint8)
    output_morphology = cv2.morphologyEx(output_otsuthresh, cv2.MORPH_OPEN,kernel)
    output_erosion = cv2.erode(output_otsuthresh, kernel,iterations=2)
    output_dilate = cv2.dilate(output_otsuthresh, kernel,iterations=4)
    boder =  output_dilate - output_erosion
    # Detect Contour and measure the area durian object 
    getcoutours_ObjectDetect(boder,img_detect_object)


    # Detect Defect of Object in the surface
    sharpened_image = sharpen_image_laplacian(img_detect_defect)
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
    # Detect Contour of Defect in the surface 
    getcoutours_DefectDetect(bitwise_img,img_detect_defect)

    imgstack = stackImages(0.8, ([img_detect_object,img_detect_defect,bitwise_img], [mask,mask_dilate,res]))
    cv2.imshow("Result Image", imgstack)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break
cv2.destroyAllWindows()