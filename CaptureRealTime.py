import cv2 
import numpy as np

import os

import PLCController
from PLCController import PLC

import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation


segmentor = SelfiSegmentation()
newest_image_path =""

class IMG_Processing():
    def __init__(self):
        pass

    def stackImages(scale,imgArray):
        rows = len(imgArray)
        cols = len(imgArray[0])
        rowsAvailable = isinstance(imgArray[0], list)
        width = imgArray[0][0].shape[1]
        height = imgArray[0][0].shape[0]
        if rowsAvailable:
            for x in range ( 0, rows):
                for y in range(0, cols):
                    if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                        imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                    else:
                        imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                    if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
            imageBlank = np.zeros((height, width, 3), np.uint8)
            hor = [imageBlank]*rows
            hor_con = [imageBlank]*rows
            for x in range(0, rows):
                hor[x] = np.hstack(imgArray[x])
            ver = np.vstack(hor)
        else:
            for x in range(0, rows):
                if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                    imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
                else:
                    imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
                if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
            hor= np.hstack(imgArray)
            ver = hor
        return ver



    # def getcoutours(frame_gray,frame_countour):
    #     contours,hierachy = cv2.findContours(frame_gray,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #     for cnt in contours:
    #         area = cv2.contourArea(cnt)
    #         print(area)
    #         areaMin = cv2.getTrackbarPos("Area","Parameters")
    #         if area > areaMin: # nho cau hinh lai
    #             cv2.drawContours(frame_countour,cnt,-1,(255,0,255),7) # 255,0,255 : mau tim
    #             peri = cv2.arcLength(cnt,True)
    #             approx = cv2.approxPolyDP(cnt,0.02*peri,True)
    #             x,y,w,h = cv2.boundingRect(approx)
    #             cv2.rectangle(frame_countour,(x,y),(x+w,y+h),(0,255,0),5) # 0,255,0 : mau xanh la cay
    #             cv2.putText(frame_countour,"Area: "+ str(int(area)),(x+w+40,y+65),cv2.FONT_HERSHEY_COMPLEX,0.7,
    #                         (0,255,0),2)

class capture_img():
    def __init__(self) :
        pass
    
 
    def capture(byte, bit, datatype):
        global video
        global newest_image_path
        sensor=PLC.ReadMemory(byte,bit,datatype)
        ret,frame = video.read()
        print(f"sensor:{sensor}")
        if sensor == True:
            global count
            count += 1
            folder = "/home/pi/Mechatronics_Project/Mechatronics-Project/Image_Original/"
            if not os.path.exists(folder):
                os.makedirs(folder)
            # global img
            # frame = img.copy()
            newest_image_path =folder +"sample No."+str(count) +".JPG"
            cv2.imwrite(newest_image_path, frame)
            print('capture success......................')
            # time.sleep(1)
    

    def removeBG():
        global newest_image_path
        output_image_dir = "Project_Push_Git\Image_RMGB"
        if not os.path.exists(output_image_dir):
            os.makedirs(output_image_dir)

        img = cv2.imread(newest_image_path)
        # Perform background removal
        img_out = segmentor.removeBG(img,cutThreshold=0.85)  # Adjust threshold as needed
        # Get the filename (without extension) from the input image path
        filename = os.path.splitext(os.path.basename(newest_image_path))[0]
        # Save the processed image to the output directory
        output_path = os.path.join(output_image_dir, f"{filename}.jpg")
        cv2.imwrite(output_path, img_out)

############################ TRACKBAR #########################################

def empty(a):
    pass
cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters",640,240)
cv2.createTrackbar("Thershold1","Parameters",100,255,empty)
cv2.createTrackbar("Thershold2","Parameters",60,255,empty)
cv2.createTrackbar("Area","Parameters",5000,30000,empty)

##################################################################################



video = cv2.VideoCapture(0)
count =0

############# set Frame image #####################
framewidth = 640
frameheight = 480
video.set(3,framewidth)
video.set(4,frameheight)
####################################################
while True: 
    ret,img = video.read()
    imgContour = img.copy()
    imgblur = cv2.GaussianBlur(img,(7,7),1)   
    gray = cv2.cvtColor(imgblur, cv2.COLOR_BGR2GRAY)

    threshold1 = cv2.getTrackbarPos("Thershold1","Parameters")
    threshold2 = cv2.getTrackbarPos("Thershold2","Parameters")

    imgCany = cv2.Canny(gray,threshold1,threshold2)
    # Adapte threshold img no need Detect thresh Manual
    output_adapthresh = cv2.adaptiveThreshold (gray,255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,51, 0)  #51
    # Create the array 3x3 vailue 1
    # kernel = np.ones((3, 3), np.uint8)
    # Dilation the object 
    # imgDil = cv2.dilate(output_adapthresh,kernel,iterations=2)  #imgCany
    # opening = cv2.morphologyEx(imgDil,cv2.MORPH_OPEN,kernel, iterations=2)
    IMG_Processing.getcoutours(output_adapthresh,imgContour)
    # Show image 
    imgstack = IMG_Processing.stackImages(0.8,([img,gray],
                                [output_adapthresh,imgCany]))


    cv2.imshow("Result Camera",imgstack)

    # capture_img.capture(0,0,S7WLBit)
    capture_img.removeBG()


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video.release
cv2.destroyAllWindows()
# # while (True):
# #     print(PLC.ReadMemory(0,0,S7WLBit))



