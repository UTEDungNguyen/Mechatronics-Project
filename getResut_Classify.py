import cv2
import numpy as np
import math
import glob
import os
import time
import PLCController
from PLCController import PLC
import DBconfig
from DBconfig import firebase
from datetime import datetime
import qrcode
import snap7
from snap7.util import *
from snap7.types import *
import snap7.client as c
import pyrebase
import shutil
import serial
import threading


storage = firebase.storage()
database = firebase.database()

Mass_Out = 0
flag_object = False
flag_defect = False
flag_PLC = True
doneGetWeight = False
RL_getLoadcellValue = False

MeetStandardIMGProcessing = False

list_results =[]

ser = serial.Serial("/dev/ttyAMA0", 9600)
# Lấy ngày và giờ hiện tại
current_datetime = datetime.now()

# Định dạng ngày tháng
formatted_date = current_datetime.strftime("%Y-%m-%d")
formatted_hour = current_datetime.strftime("%H:%M:%S")
count = 0
list_Weights = []
def empty(a):
    pass
cv2.namedWindow("Tracking")
cv2.resizeWindow("Tracking",640,240)
cv2.createTrackbar("LH", "Tracking", 97, 255, empty) 
cv2.createTrackbar("LS", "Tracking", 0, 255, empty)
cv2.createTrackbar("LV", "Tracking", 0, 255, empty)
cv2.createTrackbar("UH", "Tracking", 106, 255, empty)
cv2.createTrackbar("US", "Tracking", 174, 255, empty)
cv2.createTrackbar("UV", "Tracking", 255, 255, empty)


class DetectObject:
    def ElipseContours(self, img, imgContour_Object):
        contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            selected_contour = max(contours, key=lambda x: cv2.contourArea(x))
            # Config area to detect object value 
            areaMin = 1000 

            if area > areaMin:
                cv2.drawContours(imgContour_Object, cnt, -1, (255, 0, 255), 7)
                M = cv2.moments(cnt)
                cx= int(M["m10"]/M["m00"])
                cy= int(M["m01"]/M["m00"])  
                
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02* peri, True) 
                x, y, w, h = cv2.boundingRect(approx)
                ellipse = cv2.fitEllipse(selected_contour)
               
                center = ellipse[0]
                semi_majorAxis = (ellipse[1][0])/2
                semi_minorAxis = (ellipse[1][1])/2
                angle = ellipse[2]

                area_elipse = math.pi * semi_majorAxis * semi_minorAxis
                area_elipse = "{:.3f}".format(area_elipse)
                area_elipse = float(area_elipse)
                result_sub = area_elipse - area
                result_percent = result_sub/area_elipse
                result_percent = "{:.3f}".format(result_percent)
                result_percent = float(result_percent)
                # print("Area of substraction (pixel): ",result_percent)
                if (result_percent < 0.2): # 20% 
                    # print("Durian meet standards")
                    meetStandard = True
                else:
                    meetStandard = False
                cv2.ellipse(imgContour_Object, ellipse, (0, 255, 0), 3)
                cv2.circle(imgContour_Object,(cx,cy),7,(0,0,255),-1)
                cv2.rectangle(imgContour_Object, (x, y), (x + w, y + h), (0, 255, 0), 5)

                print(f"\nGet result OBJECT DONE \n resultOBJECT:{meetStandard}\n")

                return meetStandard,imgContour_Object

    def getResultObject(self,image,folder_object):
        global flag_object
        global count
        image = cv2.resize(image,(400,300))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Warming threshold needed apdative
        thresh, output_otsuthresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        # Erosion image to detect Object Elipse for Durian 
        kernel = np.ones((3,3),np.uint8)
        output_erosion = cv2.erode(output_otsuthresh, kernel,iterations=2)
        output_dilate = cv2.dilate(output_otsuthresh, kernel,iterations=4)
        boder =  output_dilate - output_erosion 
        # Detect Contour and measure the area durian object 
        resultObject,img_processed_object = self.ElipseContours(boder,image)
        
        flag_object = True
        if not os.path.exists(folder_object):
            os.makedirs(folder_object)
        newest_image_path =folder_object +"ResultObject_NO"+str(count +1) +".JPG"
        cv2.imwrite(newest_image_path, img_processed_object)
        return resultObject,img_processed_object

class DetectDefect:
    def __init__(self):
        pass
    def sharpen_image_laplacian(self, image):
        laplacian = cv2.Laplacian(image, cv2.CV_64F)
        sharpened_image = np.uint8(np.clip(image - 0.3*laplacian, 0, 255))
        return sharpened_image

    def RectangleContours(self, img, imgContour_Defect):
        list_area = []
        contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            list_area.append(area)
            selected_contour = max(contours, key=lambda x: cv2.contourArea(x))

            # Config area to detect defect of durian
            areaMin = 500 
            if area > areaMin:
                cv2.drawContours(imgContour_Defect, cnt, -1, (255, 0, 255),5)
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.009* peri, True)  
                x, y, w, h = cv2.boundingRect(approx)
                cv2.rectangle(imgContour_Defect, (x, y), (x + w, y + h), (0, 255, 0), 5)


        S = sorted(list_area,key=None,reverse=True)
        if S[0]< areaMin : 
            Defect = False
        else : 
            Defect = True
        
        return Defect,imgContour_Defect
    def getResultDefect(self,image, folder_defect):
        global flag_defect
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

        # Detecting contours in image
        thresh, output_threshold = cv2.threshold(res,105, 255, 1, cv2.THRESH_BINARY)
        gray_image = cv2.cvtColor(output_threshold, cv2.COLOR_BGR2GRAY)
        bitwise_img = cv2.bitwise_not(gray_image)
        # Detecting contours in image
        resultDefect,img_processed_defect = self.RectangleContours(bitwise_img,image)
        print(f"\nGet result DEFECT DONE \n resultDefect:{resultDefect}\n")
        flag_defect = True
        if not os.path.exists(folder_defect):
            os.makedirs(folder_defect)
        newest_image_path =folder_defect +"ResultDefect_NO"+str(count +1) +".JPG"
        cv2.imwrite(newest_image_path, img_processed_defect)
        return resultDefect,img_processed_defect
    
#  Innovate class and cofig again
class PLCVal:
     
    def getWeightsSample(self):
        # global count
        global Mass_Out
        global doneGetWeight
        global flag_PLC
        global RL_getLoadcellValue
        Single_Sanple =PLC.ReadMemory(5,0,S7WLBit)
        Multi_Sample =PLC.ReadMemory(5,1,S7WLBit)
        RL_chan = PLC.ReadMemory(3,1,S7WLBit)
        RL_le = PLC.ReadMemory(3,2,S7WLBit)
        if (Single_Sanple == True and Multi_Sample == True) or (Single_Sanple == False and Multi_Sample == False):
            pass
        elif Single_Sanple == True and Multi_Sample == False:
            Mass_Out = PLC.ReadMemory(58,0,S7WLWord)
            list_Weights.append(Mass_Out)
        else:
            if RL_chan == True and RL_le == False:
                Mass_Out = PLC.ReadMemory(50,0,S7WLWord)  
                list_Weights.append(Mass_Out)
            
            elif RL_chan == False and RL_le == True:
                Mass_Out = PLC.ReadMemory(54,0,S7WLWord)
                list_Weights.append(Mass_Out)
           
        flag_PLC = False
        doneGetWeight = True
        
        print(f" DONE GET WEIGHT\n done het weight: {doneGetWeight} ")
       
        return Mass_Out

def qrConfig():
    global count
    # Data to encode
    data = "https://utedungnguyen.github.io/MP_Web_Display/?custom_param=Sample" + str(count)
    
    # Creating an instance of QRCode class
    qr = qrcode.QRCode(version = 1,
                    error_correction = qrcode.constants.ERROR_CORRECT_L,
                    box_size = 20,
                    border = 2)
    
    # Adding data to the instance 'qr'
    qr.add_data(data)
    
    qr.make(fit = True)
    img = qr.make_image(fill_color = 'black',
                        back_color = 'white')
    path_save_qr ="Image_QR/" + "QR_Sample" + str(count) +".png"
    img.save(path_save_qr)
    # print("Successsssssssssssssss")


def moveImage(image_path,path_folder):
    if not os.path.exists(path_folder):
        os.makedirs(path_folder)
    
    # Get the file name from the source path
    file_name = os.path.basename(image_path)
    
    # Create the full path for the destination file
    dest_path = os.path.join(path_folder, file_name)
    
    # Move the file
    shutil.move(image_path, dest_path)
    
data_receive = 0
signal_state = False
Classify_Sensor = False
stop_threads = False
    
def Classification():
    global list_results, Classify_Sensor
    global data_receive, signal_state
    if signal_state == False:
        Classify_Sensor = PLC.ReadMemory(5,2,S7WLBit)
    if Classify_Sensor == True and len(list_results) != 0:
        if list_results[0] == "Type_1":
            ser.write(b"R")
            del list_results[0]
        elif list_results[0] == "Type_2":
            ser.write(b"L")
            del list_results[0]   
        Classify_Sensor = False    
        signal_state = True

PLC_val = PLCVal()

count_img = 0
state = False
count = 0


def read_from_port(ser):
    global data_receive, signal_state, stop_threads
    while True:
        if ser.in_waiting > 0:
            data_receive = ser.read(ser.in_waiting)
            data_receive = data_receive.decode("utf-8")
            print(data_receive)
            if data_receive == "F" :
                signal_state = False
                data_receive = ""
                
            if data_receive == "H" :
                stop_threads = True
                data_receive = ""

# Tạo một luồng để đọc dữ liệu từ serial
thread = threading.Thread(target=read_from_port, args=(ser,))
thread.daemon = True
thread.start()

while True:
    if state == False:
        if count == 0:
            SampleWeight = 1900
        elif count == 1:
            SampleWeight = 1500

        else :
            state = True 
            SampleWeight = 0
    
    if SampleWeight >1800  and SampleWeight<5000 :
        list_results.append("Type_1")
        count += 1
        
        # time.sleep(5)

    elif (SampleWeight >1400  and SampleWeight <1800) or SampleWeight >5000 :
        list_results.append("Type_2")
        count += 1
        # time.sleep(5)
    print(f"count :{count}")
    print(list_results)
    Classification()
    while stop_threads:
        if (PLC.ReadMemory(5,3,S7WLBit) == True):
            ser.write(b"S")
            stop_threads = False   
    
    




                
        
                
        
       

        
