import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import cv2
import numpy as np
import pyrebase 
import serial
import time
import argparse
import pandas as pd
import numpy as np
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt
import schedule
import threading



#HSV color
lower_green = (30, 127, 31)
upper_green = (241, 255, 255)
lower_yellow=(20,132,52) #(18,77,80)
upper_yellow = (34,255, 252)

def camera_thread():
    # Open the default camera
    #cap = cv2.VideoCapture(0)
    #roi = [160, 90, 340, 333]
    while True:
        global frame
        global image
        global string
        ret, frame = cap.read()
        frame = frame[int(roi[1]):int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])]
        image=cv2.resize(frame,(300,300))
        print("mode_auto: ",mode_auto)
        print("mode",mode)
        print(string)
        #if mode_auto==0 & mode ==1 :
          #  frame=cv2.putText(image,string,(20,20),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2, cv2.LINE_AA)      
        cv2.imshow("Webcam", frame)
        cv2.imwrite("/var/www/image/image.jpg", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

#===============================Helper function for detect==============================#
def extract_bg(image):
    kernel = np.ones((3, 3), np.uint8)
    gray=cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    gray=cv2.GaussianBlur(gray,(3,3),0)
    _, binary_image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV)
    binary_image = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel)
    return binary_image

def convert_to_binary(image):
    kernel = np.ones((3, 3), np.uint8)
    gray=cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    gray=cv2.GaussianBlur(gray,(3,3),0)
    _, binary_image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
    binary_image = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel)
    return binary_image

def hsv_color(image,lower_threshold,upper_threshold):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_image, lower_threshold,upper_threshold)
    result = cv2.bitwise_and(image, image, mask=mask)
    return result
def extract_yellow_mask(image,lower_yellow,upper_yellow,show=False):
    image_yellow=hsv_color(image,lower_yellow,upper_yellow)
    image_green=hsv_color(image,lower_green,upper_green)
    b_img_yellow=convert_to_binary(image_yellow)
    b_img_green=convert_to_binary(image_green)
    # # Find the intersection mask using bitwise AND
    intersection = cv2.bitwise_and(b_img_green,b_img_yellow)
    # Find the non-intersection mask of mask1 using bitwise NOT
    non_intersection_mask1 = cv2.bitwise_not(b_img_yellow)
    # Combine the non-intersection mask of mask1 with mask2 using bitwise OR
    subtracted_mask = cv2.bitwise_or(non_intersection_mask1, b_img_green)
    # Invert the mask to change the background to white
    inverted_mask = cv2.bitwise_not(subtracted_mask)
    return b_img_green,b_img_yellow,inverted_mask

def min_max_norm(image):
    a_min, a_max = image.min(), image.max()
    return (image-a_min)/(a_max - a_min) 

def cvt2heatmap(gray):
    heatmap = cv2.applyColorMap(np.uint8(gray), cv2.COLORMAP_JET)
    return heatmap
    
#===================================Hàm chuyển từ pixel sang diện tích=============================================#

#Chiều rộng thực tế - đơn vị(cm)
image_width_cm =10
#Chiều cao thực tế - đơn vị(cm)
image_height_cm =10
#Hàm chuyển từ pixel sang cm^2
def convert_pixels_to_cm2(mask,nonzero_pixels,image_width_cm,image_height_cm ):
    # Get image resolution
    height, width = mask.shape[:2]

    # Calculate physical size of a single pixel
    # pixel_size_cm = region_size_cm / max(height, width)
    # Calculate pixel resolution
    pixel_resolution_x = image_width_cm / width
    pixel_resolution_y = image_height_cm / height
    # Calculate the conversion factor
    conversion_factor = pixel_resolution_x * pixel_resolution_y
    # Convert nonzero pixels to square centimeters
    area_cm2 = nonzero_pixels *conversion_factor #(pixel_size_cm ** 2)

    return area_cm2

#AUTO_DETECT
pos_auto_array = [1,2,3,4,5,6,13,12,11,10,9,8,7,14,15,16,17,18,19]
#pos_auto_array = [1,2,3]
def auto_detect():
    global mode_auto
    mode_auto=1
    mode =0
    #List lưu diện tích
    plant_areas=[]
    print("time up")
    for value in pos_auto_array: 
        pos_auto = value
        print(pos_auto)
        data_trans = str(pos_auto)
        ser.write(data_trans.encode())
        mode = 0
        if ser.in_waiting>=0:
            data_rec = ser.readline().decode('utf-8').rstrip()
        # Xử lý dữ liệu nhận được
        pos_auto_arduino = int(data_rec)
        if pos_auto_arduino == pos_auto:
            mode = 1
        if mode == 1:
            count =0
            print(pos_auto)
            while count <=7:
                # ret, frame = cap.read()
                # frame = frame[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
                # image=cv2.resize(frame,(300,300))
                
                all_scores_mean_norm=[]
                b_img_green,b_img_yellow,inverted_mask=extract_yellow_mask(image,lower_yellow,upper_yellow)
                t1=time.time()
                anomaly_map_resized_blur = gaussian_filter(inverted_mask, sigma=4)
                anomaly_map_resized_blur[0][0] = 1.

                #Find index of pixel values(Abnormality region)
                anomaly_threshold_index = anomaly_map_resized_blur[anomaly_map_resized_blur >75] #75
                #Pixel <75 will be assigned to be zero
                anomaly_map_resized_blur[anomaly_map_resized_blur < 75] = 0 #75
                #Area of anomaly region
                anomaly_threshold_area = anomaly_threshold_index.size
                anomaly_threshold_area = anomaly_threshold_area / float(anomaly_map_resized_blur.size) * 100
                # all_scores_mean_norm.append(anomaly_threshold_area)
                # score=np.mean(all_scores_mean_norm)
                if anomaly_threshold_area > 0.5:
                    string='abnormal'
                else:
                    string='normal'
                print(string)
                db.reference(f'state_plant/plant{pos_auto}').set(string)    
                 #========================Add thêm tính diện tích (firebase_v1.py)=======================#
                # Đếm số pixel của vùng lá màu xanh và vàng
                non_pix_g,non_pix_y=cv2.countNonZero(b_img_green),cv2.countNonZero(b_img_yellow)
                #Tính tổng số pixel của cả 2 vùng
                plant_size=non_pix_g+non_pix_g
                # Chuyển từ giá trị pixel sang cm^2()
                pixel_2cm=convert_pixels_to_cm2(inverted_mask,plant_size,image_width_cm,image_height_cm )
                #Add vào danh sách
                
                #In ra diện tích nếu cần
                
                count += 1
            #plant_areas[pos_auto-1] = pixel_2cm
            plant_areas.append(pixel_2cm)
            print(plant_areas)
            cv2.imwrite(f"/var/www/image/image{pos_auto}.jpg", frame)  
            storage.child(f"plant{pos_auto}.jpg").put(f"/var/www/image/image{pos_auto}.jpg")
    ser.write(str(0).encode())
    pos_ref.set(0)
    ser.write(str(0).encode())
    #Tim ra so tuan tuoi
    threshold_area = np.mean(plant_areas)
    if (threshold_area < 20):
        print('dieu chinh cho tuan 1')
        plant_stage_ref.set(0)
    elif (threshold_area > 20):
        print('dieu chinh cho tuan 2')
        plant_stage_ref.set(1)
    pos_current = 0
    pos_arduino = 0
    mode_auto =0



#================================================================================#
configure_keys="/home/pi/Desktop/codeFinal/esp-firebase-f07dc-firebase-adminsdk-upc95-413e263545.json"
# service='https://esp-firebase-f07dc-default-rtdb.firebaseio.com//'

#================START===================
# Start measuring the inference time
cred = credentials.Certificate(configure_keys)
firebase_admin.initialize_app(cred, {

    'databaseURL': 'https://esp-firebase-f07dc-default-rtdb.firebaseio.com/'

})
# Reference to the Firebase database node you want to update
pos_ref=db.reference('Position/pos') 
hour_run_auto_ref = db.reference('/Timer_auto_detect/hour')
min_run_auto_ref = db.reference('/Timer_auto_detect/min')
plant_stage_ref = db.reference('/grown_up')

#upload ảnh
config= {
    "apiKey": "AIzaSyBA6yTZp555yZFXkCDMw93GQqe_7A58N_0",
    "authDomain": "esp-firebase-f07dc.firebaseapp.com",
    "databaseURL": "https://esp-firebase-f07dc-default-rtdb.firebaseio.com",
    "projectId": "esp-firebase-f07dc",
    "storageBucket": "esp-firebase-f07dc.appspot.com",
    "messagingSenderId": "313931083002",
    "appId": "1:313931083002:web:de4674ef289e2a66972d43",
    "serviveAccount": "/home/pi/Desktop/codeFinal/esp-firebase-f07dc-firebase-adminsdk-upc95-55f97253b4.json"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()



hour_auto_fb = hour_run_auto_ref.get()
min_auto_fb = min_run_auto_ref.get()
if int(hour_auto_fb)<10:
    hour_auto = "0"+str(hour_auto_fb)
else:
    hour_auto = str(hour_auto_fb)
if int(min_auto_fb)<10:
    min_auto = "0"+str(min_auto_fb)
else:
    min_auto = str(min_auto_fb)
time_auto = hour_auto + ":" + min_auto

schedule.every().day.at(time_auto).do(auto_detect)
#khoi tao uart
ser = serial.Serial('/dev/serial0', 115200)

pos_current = 0
pos_arduino = 0
mode = 0
mode_auto =0
frame = None
image = None
string = None
# Open the default camera
roi = [160, 90, 340, 333]
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
frame = frame[int(roi[1]):int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])]
image=cv2.resize(frame,(300,300))


camera_thread = threading.Thread(target=camera_thread)
camera_thread.start()



while True:
    # ret, frame = cap.read()
    # frame = frame[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
    
    
    pos_fb=pos_ref.get()
    #get timer run auto_detect from fb
    hour_auto_fb = hour_run_auto_ref.get()
    min_auto_fb = min_run_auto_ref.get()
    if int(hour_auto_fb)<10:
        hour_auto = "0"+str(hour_auto_fb)
    else:
        hour_auto = str(hour_auto_fb)
    if int(min_auto_fb)<10:
        min_auto = "0"+str(min_auto_fb)
    else:
        min_auto = str(min_auto_fb)
    time_auto_fb = hour_auto + ":" + min_auto
    print(time_auto)
    if time_auto != time_auto_fb:
    #function timer run auto
        schedule.every().day.at(time_auto_fb).do(auto_detect)
        time_auto = time_auto_fb
    schedule.run_pending()
    if pos_current != pos_fb :
        mode = 0
        pos_current = pos_fb
        print(pos_current)
        data_trans = str(pos_current)
        ser.write(data_trans.encode())
    if ser.in_waiting > 0:
        data_rec = ser.readline().decode('utf-8').rstrip()
    # Xử lý dữ liệu nhận được
        pos_arduino = int(data_rec)
   

        print(pos_arduino) 
    if pos_arduino == pos_current:
        mode = 1
        
    if mode == 1 :
        all_scores_mean_norm=[]
        inverted_mask=extract_yellow_mask(image,lower_yellow,upper_yellow)
        anomaly_map_resized_blur = gaussian_filter(inverted_mask, sigma=4)
        anomaly_map_resized_blur[0][0] = 1.
        
        
        #Find index of pixel values(Abnormality region)
        anomaly_threshold_index = anomaly_map_resized_blur[anomaly_map_resized_blur >75] #75
        #Pixel <75 will be assigned to be zero
        anomaly_map_resized_blur[anomaly_map_resized_blur < 75] = 0 #75
        #Area of anomaly region
        anomaly_threshold_area = anomaly_threshold_index.size
        anomaly_threshold_area = anomaly_threshold_area / float(anomaly_map_resized_blur.size) * 100
        # all_scores_mean_norm.append(anomaly_threshold_area)
        # score=np.mean(all_scores_mean_norm)
        if anomaly_threshold_area > 0.5:
            string='abnormal'
        else:
            string='normal'
        frame=cv2.putText(image,string,(20,10),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2, cv2.LINE_AA)
        print(string)
        db.reference(f'state_plant/plant{pos_current}').set(string)
    
    
    #cv2.imshow("Webcam", frame)
    

# Dừng luồng
camera_thread.join()
ser.close()

    








