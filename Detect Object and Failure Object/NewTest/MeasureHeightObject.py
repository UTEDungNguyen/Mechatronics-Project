import cv2
import numpy as np

# Measure Height
def get_height(imshow3):
    # Convert Bitmap to OpenCV Mat
    frame = cv2.cvtColor(np.array(imshow3), cv2.COLOR_BGR2GRAY)
    frame = cv2.medianBlur(frame, 3)

    # Thresholding
    _, src_copy = cv2.threshold(frame, 150, 255, cv2.THRESH_BINARY)

    # Finding the first non-zero pixel from top
    x3, y3 = 0, 0
    for i in range(50,frame.shape[0]):
        for j in range(50, frame.shape[1]):
            if frame[i, j] == 0:
                x3 = j
                y3 = i
                break
        if x3 != 0:
            break

    # Finding the first non-zero pixel from bottom
    x4, y4 = 0, 0
    for i in range(frame.shape[0] - 150, -1, -1):
        for j in range(50, frame.shape[1]):
            if src_copy[i, j] == 0:
                x4 = j
                y4 = i
                break
        if x4 != 0:
            break

    # Calculate height
    height = y4 - y3
    return height


# Assuming you have a Bitmap object called imshow3a
# height = get_height(imshow3)


