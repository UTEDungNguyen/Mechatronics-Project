import cv2
import numpy as np
from PIL import Image,ImageTk

def to_bitmap_image_two(imshow):
    # Convert Bitmap to OpenCV Mat
    frame = cv2.cvtColor(np.array(imshow), cv2.COLOR_BGR2GRAY)
    frame= cv2.medianBlur(frame, 3)

    # Thresholding
    _, thresh = cv2.threshold(frame, 110, 255, cv2.THRESH_BINARY)

    # Finding the first non-zero pixel from left
    x1, y1 = 0, 0
    for i in range(50, thresh.shape[1]):
        for j in range(50, thresh.shape[0]):
            if thresh[j, i] == 0:
                x1 = i
                y1 = j
                break
        if x1 != 0:
            break

    # Finding the first non-zero pixel from right
    x2, y2 = 0, 0
    for i in range(thresh.shape[1] - 20, -1, -1):
        for j in range(50, thresh.shape[0]):
            if thresh[j, i] == 0:
                x2 = i
                y2 = j
                break
        if x2 != 0:
            break

    # Finding the first non-zero pixel from top
    x3, y3 = 0, 0
    for i in range(20, thresh.shape[0]):
        for j in range(20, thresh.shape[1]):
            if thresh[i, j] == 0:
                x3 = j
                y3 = i
                break
        if x3 != 0:
            break

    # Finding the first non-zero pixel from bottom
    x4, y4 = 0, 0
    for i in range(thresh.shape[0] - 50, -1, -1):
        for j in range(20, thresh.shape[1]):
            if thresh[i, j] == 0:
                x4 = j
                y4 = i
                break
        if x4 != 0:
            break

    # Calculate length and height
    length = x2 - x1
    height = y4 - y3

    # Draw rectangle around the durian
    cv2.rectangle(thresh,
                  (x1, y3),
                  (x1 + length, y3 + height),
                  (0, 0, 0), 4, 0)

    # Convert the modified OpenCV Mat to Bitmap
    pil_image = Image.fromarray(frame)

    # Convert PIL image to BitmapImage
    bitmap_image = ImageTk.PhotoImage(pil_image)

    # Return the BitmapImage
    return bitmap_image

# Mark:
# Assuming you have a Bitmap object called imshow
# bitmap_image = to_bitmap_image_two(imshow)
