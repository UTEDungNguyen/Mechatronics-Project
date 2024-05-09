import cv2
import numpy as np

def get_length(imshow2):
    # Convert Bitmap to OpenCV Mat
    frame = cv2.cvtColor(np.array(imshow2), cv2.COLOR_BGR2GRAY)
    frame = cv2.medianBlur(frame, 3)

    # Thresholding
    _, thresh = cv2.threshold(frame, 110, 255, cv2.THRESH_BINARY)

    # Finding the first non-zero pixel from left
    x1, y1 = 0, 0
    for i in range(50, thresh.shape[1]):
        for j in range(50, thresh.shape[0]):
            if frame[j, i] == 0:
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

    # Calculate length
    length_x = x2 - x1
    length_y = y4 - y3
    return (length_x, length_y)

# Assuming you have a Bitmap object called imshow2
# length_x, length_y = get_length(imshow2)