import cv2
import numpy as np
import math
import os
import imutils
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation


# Remove background to detect object image Custom folder
# Initialize the SelfiSegmentation module
segmentor = SelfiSegmentation()

# # Set the directory containing images and the directory to save the processed images
# class capture_img():
#     def __init__(self) :
#         pass
    
 
#     def capture(byte, bit, datatype):
#         global video
#         sensor=PLC.ReadMemory(byte,bit,datatype)
#         ret,frame = video.read()
#         print(f"sensor:{sensor}")
#         if sensor == True:
#             global count
#             count += 1
#             folder = "/home/pi/Mechatronics_Project/Mechatronics-Project/Image/Sample" + str(count)
#             if not os.path.exists(folder):
#                 os.makedirs(folder)
#             # global img
#             # frame = img.copy()
#             cv2.imwrite(folder +"/"+"sample No."+str(count) +".JPG", frame)
#             print('capture success......................')
#             # time.sleep(1)
count = 3
for n in range(count):
    count +=1
print(count)
# input_image_dir = "Image1"+"/"+ "Sample"+str(count)
input_image_dir = "Image1"+"/"+ "Sample"+ str(count)
# output_image_dir = "Result_Remove_Background1"+"/"+"Sample"+str(count)
output_image_dir = "Result_Remove_Background1"+"/"+"Sample"+ str(count)

# Create the output directory if it doesn't exist
if not os.path.exists(output_image_dir):
    os.makedirs(output_image_dir)

# List all image files in the directory
image_files = [os.path.join(input_image_dir, filename) for filename in os.listdir(input_image_dir) 
               if filename.endswith(('.JPG', '.png', '.jpeg','.jpg'))]

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