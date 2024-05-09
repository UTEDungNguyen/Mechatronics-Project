import cv2
import numpy as np

def classification(imgageDurian):
    # Convert Bitmap to OpenCV Mat
    img = cv2.cvtColor(imgageDurian, cv2.COLOR_BGR2GRAY)
    frame = cv2.medianBlur(img, 3)

    # Thresholding
    _, thresh = cv2.threshold(frame,150, 255, cv2.THRESH_BINARY_INV)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    max_area = 0
    for contour in contours:
        # Calculate bounding rectangle
        x, y, w, h = cv2.boundingRect(contour)
        
        # Count white pixels within the bounding rectangle
        dem = np.sum(thresh[y:y+h, x:x+w] == 255)

        # Update max area and calculate the real area
        if dem > max_area:
            max_area = dem
            area = max_area * (1369 / 4260) * (851 / 2810) * 0.01
    
        cv2.imshow('thresh',thresh)
    return area 

# Example usage:
# Assuming you have a Bitmap object called ImageDurian
# result = classification(Durian)

imgageDurian =cv2.imread('testhu.jpg')
# Get the size of the image
width,height,channel = imgageDurian.shape
# Print the size
print("Image width:", width)
print("Image height:", height)
imgageDurian = cv2.resize(imgageDurian,(400,500))
cv2.imshow("Image",imgageDurian)
while True:
    result = classification(imgageDurian)
    print(f'AREA = {result}')
    

    # cv2.imshow("Result",result)
    if cv2.waitKey(0) == ord('q'):
        break
