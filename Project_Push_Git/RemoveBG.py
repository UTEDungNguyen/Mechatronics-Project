import cv2
import os
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation


# Remove background to detect object image Custom folder
# Initialize the SelfiSegmentation module
segmentor = SelfiSegmentation()
input_image_dir = "Image_Original"
output_image_dir = "Image_RMGB"

# Create the output directory if it doesn't exist
if not os.path.exists(output_image_dir):
    os.makedirs(output_image_dir)

list_path=[]
while True:
    files = os.listdir(input_image_dir)
    for file in files:
        file_path =os.path.join(input_image_dir,file)
        list_path.append(file_path)
        newest_file = max(list_path, key = os.path.getmtime)
    # Process each image in the directory
    # for img_path in image_files:
        # Read the image
        img = cv2.imread(newest_file)
        # Perform background removal
        img_out = segmentor.removeBG(img,cutThreshold=0.85)  # Adjust threshold as needed
        # Get the filename (without extension) from the input image path
        filename = os.path.splitext(os.path.basename(newest_file))[0]
        # Save the processed image to the output directory
        output_path = os.path.join(output_image_dir, f"{filename}_processed.jpg")
        cv2.imwrite(output_path, img_out)