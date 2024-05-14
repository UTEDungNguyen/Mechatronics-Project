import cv2
import numpy as np
import os
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation

# Initialize the SelfiSegmentation module
segmentor = SelfiSegmentation()

# Set the directory containing images and the directory to save the processed images
input_image_dir = "Image"
output_image_dir = "Result_Remove_Background"
# Create the output directory if it doesn't exist
if not os.path.exists(output_image_dir):
    os.makedirs(output_image_dir)

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



# # demo and mapping Capture Realtime imgae
# import cv2
# import os
# import PLC  # Assuming PLC module is imported for ReadMemory function
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
