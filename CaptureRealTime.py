import cv2 
import numpy as np

import os
import snap7
from snap7.util import *
from snap7.types import *
import snap7.client as c

import PLCController
from PLCController import PLC

import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation


segmentor = SelfiSegmentation()
newest_image_path =""

count_capture =0
count_Remove =0

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
            global count_capture
            global count_Remove
            count_Remove = count_capture

            print(f'count_capture: {count_capture}')
            print(f'count_remove: {count_Remove}')
            count_capture += 1
            count_Remove +=1
            folder = "/home/pi/Mechatronics_Project/Mechatronics-Project/Image_Original/"
            if not os.path.exists(folder):
                os.makedirs(folder)
            newest_image_path =folder +"sampleNo"+str(count_capture) +".JPG"
            cv2.imwrite(newest_image_path, frame)
            print('capture success......................')

    def removeBG():
        global newest_image_path
        output_image_dir = "/home/pi/Mechatronics_Project/Mechatronics-Project/Image_RMBG"
        if not os.path.exists(output_image_dir):
            os.makedirs(output_image_dir)

        img = cv2.imread(newest_image_path)
        # Perform background removal
        img_out = segmentor.removeBG(img,cutThreshold=0.8)  # Adjust threshold as needed
        # Get the filename (without extension) from the input image path
        filename = os.path.splitext(os.path.basename(newest_image_path))[0]
        # Save the processed image to the output directory
        output_path = os.path.join(output_image_dir, f"{filename}.jpg")
        cv2.imwrite(output_path, img_out)

############################ CAPTURE #########################################

video = cv2.VideoCapture(0)

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

    threshold1 = 100
    threshold2 = 60
    imgCany = cv2.Canny(gray,threshold1,threshold2)

    # Adapte threshold img no need Detect thresh Manual
    output_adapthresh = cv2.adaptiveThreshold (gray,255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,51, 0) 

    # Show image 
    imgstack = IMG_Processing.stackImages(0.8,([img,gray],
                                [output_adapthresh,imgCany]))
    cv2.imshow("Result Camera",imgstack)

    capture_img.capture(3,6,S7WLBit)
   
    file_path = os.listdir("Image_Original")

    if not file_path or newest_image_path =="":
        print('##################################################')
        pass
    else:
        if count_Remove == count_capture:
                capture_img.removeBG()
                count_Remove += 1
                print(f'count_remove_while:{count_Remove}')
        else: pass      
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video.release
cv2.destroyAllWindows()




