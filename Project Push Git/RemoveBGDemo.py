# from rembg import remove
# from PIL import Image
# import os

# for i in os.listdir(r'D:\DATN\Detect Object and Failure Object\Project Push Git\Image'):
#     j = i.rsplit('.', maxsplit=1)[0]
#     input_path = r'D:\DATN\Detect Object and Failure Object\Project Push Git\Image\\' + i
#     output_path = r'D:\DATN\Detect Object and Failure Object\Project Push Git\Result Remove Background\\' + j + ".png"
#     input = Image.open(input_path)
#     output = remove(input)
#     output.save(output_path)

import cv2
import numpy as np
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import os

# Initialize the SelfiSegmentation module
segmentor = SelfiSegmentation()


# Set the directory containing images and the directory to save the processed images
input_image_dir = "image"
output_image_dir = "Result Remove Background"

# Create the output directory if it doesn't exist
if not os.path.exists(output_image_dir):
    os.makedirs(output_image_dir)

# List all image files in the directory
image_files = [os.path.join(input_image_dir, filename) for filename in os.listdir(input_image_dir) if filename.endswith(('.JPG', '.png', '.jpeg'))]

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

        
       
# def sharpen_image_laplacian(image):
#     laplacian = cv2.Laplacian(image, cv2.CV_64F)
#     sharpened_image = np.uint8(np.clip(image - 0.3*laplacian, 0, 255))
#     return sharpened_image  # Return the sharpened image


while True:
    #img = img_out.copy()
    img = cv2.imread(r'Result Remove Background\sample No.14_processed.jpg')
    # sharpened_image = sharpen_image_laplacian(img)
    # img = sharpened_image.copy()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    thresh, output_otsuthresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    output_adapthresh = cv2.adaptiveThreshold (gray,255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,51, 0)  #51
    
    
    # Display the original and processed images
    cv2.imshow("Original Image", img)
    cv2.imshow("Background Removed Image", img_out)
    
    cv2.imshow("Gray image",gray)
    cv2.imshow("Thresh image",output_adapthresh)
 # Wait for a key press to proceed to the next image or exit
    key = cv2.waitKey(0)

    # If 'q' is pressed, exit
    if key == ord('q'):
        break
# Close all windows
cv2.destroyAllWindows()
