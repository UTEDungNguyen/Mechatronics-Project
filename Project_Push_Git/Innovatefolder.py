import cv2
import numpy as np
import os
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation

# # demo and mapping Capture Realtime imgae
# import cv2
# import os
# import PLC  # Assuming PLC module is imported for ReadMemory function
# import cvzone
# from cvzone.SelfiSegmentationModule import SelfiSegmentation

# # Initialize the SelfiSegmentation module
# segmentor = SelfiSegmentation()

# # Set the directory to save the processed images
# output_image_dir = "Demo"
# # Create the output directory if it doesn't exist
# if not os.path.exists(output_image_dir):
#     os.makedirs(output_image_dir)

# # Initialize global variables
# video = cv2.VideoCapture(0)  # Initialize video capture from camera
# count = 0  # Initialize count for image naming

# def capture(byte, bit, datatype):
#     global video, count

#     # Read sensor value from PLC
#     sensor = PLC.ReadMemory(byte, bit, datatype)
#     print(f"sensor: {sensor}")

#     if sensor:
#         count += 1
#         folder = f"/home/pi/Mechatronics_Project/Mechatronics-Project/Image/Sample{count}"
#         if not os.path.exists(folder):
#             os.makedirs(folder)
        
#         # Capture frame from camera
#         ret, frame = video.read()
#         # Save captured image
#         img_path = f"{folder}/sample No.{count}.jpg"
#         cv2.imwrite(img_path, frame)
#         print('Capture success...')
        
#         # Process the image to remove background
#         img = cv2.imread(img_path)
#         img_out = segmentor.removeBG(img, cutThreshold=0.85)
        
#         # Save processed image
#         output_path = f"{folder}/sample No.{count}_processed.jpg"
#         cv2.imwrite(output_path, img_out)
#         print('Background removed and processed image saved.')

# # Example usage:
# capture(byte=1, bit=2, datatype="int")  # Replace with appropriate PLC memory parameters
####################################################################################################################
# Initialize the SelfiSegmentation module
segmentor = SelfiSegmentation()

# Set the directory containing folders with images
input_folder_dir = "/home/pi/Mechatronics_Project/Mechatronics-Project/Image"
# Set the directory to save the processed images
output_image_dir = "Demo"
# Create the output directory if it doesn't exist
if not os.path.exists(output_image_dir):
    os.makedirs(output_image_dir)

# Initialize global variables
video = cv2.VideoCapture(0)  # Initialize video capture from camera
count = 0  # Initialize count for image naming

def capture(byte, bit, datatype):
    global video, count

    # Read sensor value from PLC
    sensor = PLC.ReadMemory(byte, bit, datatype)
    print(f"sensor: {sensor}")

    if sensor:
        count += 1
        folder = os.path.join(input_folder_dir, f"Sample{count}")
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Capture frame from camera
        ret, frame = video.read()
        # Save captured image
        img_path = os.path.join(folder, f"sample No.{count}.jpg")
        cv2.imwrite(img_path, frame)
        print('Capture success...')
        
        # Process the image to remove background
        img = cv2.imread(img_path)
        img_out = segmentor.removeBG(img, cutThreshold=0.85)
        
        # Save processed image back into the same folder
        output_path = os.path.join(output_image_dir, f"sample No.{count}_processed.jpg")
        cv2.imwrite(output_path, img_out)
        print('Background removed and processed image saved.')

# Example usage:
capture(byte=1, bit=2, datatype="int")  # Replace with appropriate PLC memory parameters

