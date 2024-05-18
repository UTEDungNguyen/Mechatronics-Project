import cv2
import numpy as np
import math
import glob
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




class DetectObject:
    def ElipseContours(self, img, imgContour):
        contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
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
               
                center = ellipse[0]
                semi_majorAxis = (ellipse[1][0])/2
                semi_minorAxis = (ellipse[1][1])/2
                angle = ellipse[2]

                area_elipse = math.pi * semi_majorAxis * semi_minorAxis
                area_elipse = "{:.3f}".format(area_elipse)
                area_elipse = float(area_elipse)
                print("Area of the elipse classification (pixel):", area_elipse)

                result_sub = area_elipse - area
                result_percent = result_sub/area_elipse
                result_percent = "{:.3f}".format(result_percent)
                result_percent = float(result_percent)
                print("Area of substraction (pixel): ",result_percent)
                if (result_percent < 0.2): # 20% 
                    print("Durian meet standards")
                    meetStandard = True
                else:
                    print("Durian does not meet standards")
                    meetStandard = False
                cv2.ellipse(imgContour, ellipse, (0, 255, 0), 3)
                cv2.circle(imgContour,(cx,cy),7,(0,0,255),-1)
                cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 5)
                return meetStandard

    def getResultObject(self,path_image):
        # image = cv2.imread("/home/pi/Mechatronics_Project/Mechatronics-Project/Project Push Git/Result Remove Background/sample No.1.png")
        image = cv2.imread(path_image)
        # image = cv2.imread("/home/pi/Mechatronics_Project/Mechatronics-Project/Project_Push_Git/Result Remove Background/sample No.4_processed.jpg")
        # cv2.imshow('ajnsad', image)
        # image = cv2.imread("D:\DATN\Mechatronics-Project\Project Push Git\Image\sample No.17.JPG")
        image = cv2.resize(image,(400,300))

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Warming threshold needed apdative
        # Convert Binary Image using 3 method
        #thresh,  output_otsuthresh = cv2.threshold(gray,110, 255, cv2.THRESH_BINARY)    
        thresh, output_otsuthresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        #output_adapthresh = cv2.adaptiveThreshold (gray,255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,51, 0)  #51
        
        # Erosion image to detect Object Elipse for Durian 
        kernel = np.ones((3,3),np.uint8)
        
        output_erosion = cv2.erode(output_otsuthresh, kernel,iterations=2)
        output_dilate = cv2.dilate(output_otsuthresh, kernel,iterations=4)
        
        boder =  output_dilate - output_erosion 
        # Detect Contour and measure the area durian object 
        resultObject = self.ElipseContours(boder,image)
        # imgstack = stackImages(0.8, ([image,boder, output_otsuthresh], [output_erosion,output_morphology,output_dilate]))
        
        return resultObject



class DetectDefect:
    def sharpen_image_laplacian(self, image):
        laplacian = cv2.Laplacian(image, cv2.CV_64F)
        sharpened_image = np.uint8(np.clip(image - 0.3*laplacian, 0, 255))
        return sharpened_image

    def RectangleContours(self, img, imgContour):
        contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
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
                Defect = True
            else: Defect = False
        return Defect

    def getResultDefect(self, file_path):

        image = cv2.imread(file_path)
        sharpened_image = self.sharpen_image_laplacian(image)
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
        resultDefect=self.RectangleContours(bitwise_img,image)
        return resultDefect

        # imgstack = stackImages(0.8, ([image,output_threshold,bitwise_img], [mask_dilate,mask,res]))
        
        

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



if __name__ == "__main__":
    folder_IMG_RmBG = "Project_Push_Git\Image_RMGB"
    while True:
        # Define the pattern for image files (you can add more extensions if needed)
        image_pattern = os.path.join(folder_IMG_RmBG, '*.[pjPJ][npNP][gG]')

        # Get a list of all image files in the directory
        image_files = glob.glob(image_pattern)

        # Check if the list is empty
        if not image_files:
            pass

        else:
        # Use the max function with a lambda to find the file with the latest modification time
            newest_image = max(image_files, key=os.path.getmtime)

            imgToDetectObject = cv2.imread(newest_image)
            imgToDetectDefect = cv2.imread(newest_image)

            resultDefect=DetectDefect.getResultDefect(imgToDetectDefect)
            resultObject=DetectObject.getResultObject(imgToDetectObject)


            if resultObject == True & resultDefect == False:
                print("########################### Meet Standard ##############")

                ############################## push image to firebase storages #############################


                #############################################################################################

            else :
                print("########################### Not Meet Standard ##############")


