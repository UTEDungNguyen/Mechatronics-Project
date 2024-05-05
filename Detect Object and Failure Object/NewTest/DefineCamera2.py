import cv2
import numpy as np
from PIL import Image

def to_bitmap_image_two1(hienthisau):
    # Convert Bitmap to OpenCV Mat
    src_copy = cv2.cvtColor(np.array(hienthisau), cv2.COLOR_BGR2GRAY)
    src_copy = cv2.medianBlur(src_copy, 3)

    # Thresholding
    _, src_copy = cv2.threshold(src_copy, 150, 255, cv2.THRESH_BINARY)

    # Finding the first non-zero pixel from left
    x1, y1 = 0, 0
    for i in range(80, src_copy.shape[1]):
        for j in range(0, src_copy.shape[0]):
            if src_copy[j, i] == 0:
                x1 = i
                y1 = j
                break
        if x1 != 0:
            break

    # Finding the first non-zero pixel from right
    x2, y2 = 0, 0
    for i in range(src_copy.shape[1] - 50, -1, -1):
        for j in range(100, src_copy.shape[0]):
            if src_copy[j, i] == 0:
                x2 = i
                y2 = j
                break
        if x2 != 0:
            break

    # Finding the first non-zero pixel from top
    x3, y3 = 0, 0
    for i in range(50, src_copy.shape[0]):
        for j in range(50, src_copy.shape[1]):
            if src_copy[i, j] == 0:
                x3 = j
                y3 = i
                break
        if x3 != 0:
            break

    # Finding the first non-zero pixel from bottom
    x4, y4 = 0, 0
    for i in range(src_copy.shape[0] - 150, -1, -1):
        for j in range(50, src_copy.shape[1]):
            if src_copy[i, j] == 0:
                x4 = j
                y4 = i
                break
        if x4 != 0:
            break

    # Eraser shadow
    for i in range(y4, src_copy.shape[0]):
        for j in range(src_copy.shape[1]):
            src_copy[i, j] = 255

    # Calculate height
    height = y4 - y3

    # Draw rectangle around the mango
    cv2.rectangle(src_copy,
                  (0, y3),
                  (639, y3 + height),
                  (0, 0, 0), 4, 0)

    # Convert the modified OpenCV Mat to Bitmap
    pil_image = Image.fromarray(src_copy)

    # Convert PIL image to BitmapImage
    bitmap_image = ImageTk.PhotoImage(pil_image)

    # Return the BitmapImage
    return bitmap_image

# Example usage:
# Assuming you have a Bitmap object called hienthisau
# bitmap_image = to_bitmap_image_two1(hienthisau)
