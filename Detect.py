import cv2
import numpy as np
from PIL import Image,ImageTk,ImageOps


############ 
def classification(imageDurian):
    frame = cv2.cvtColor(np.array(imageDurian), cv2.COLOR_BGR2GRAY)
    frame = cv2.medianBlur(frame, 3)
    _, thresh = cv2.threshold(frame, 60, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    max_area = 0
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        dem = np.sum(thresh[y:y+h, x:x+w] == 255)
        if dem > max_area:
            max_area = dem
            area = max_area * (1369 / 4260) * (851 / 2810) * 0.01

    return area <= 2

# Example usage:
# Assuming you have a Bitmap object called ImageDurian
# result = classification(ImageDurian)

def to_bitmap_image_two(imshow):
    frame = cv2.cvtColor(np.array(imshow), cv2.COLOR_BGR2GRAY)
    frame = cv2.medianBlur(frame, 3)
    _, thresh = cv2.threshold(frame, 110, 255, cv2.THRESH_BINARY)

    x1, y1 = 0, 0
    for i in range(50, thresh.shape[1]):
        for j in range(50, thresh.shape[0]):
            if thresh[j, i] == 0:
                x1 = i
                y1 = j
                break
        if x1 != 0:
            break

    x2, y2 = 0, 0
    for i in range(thresh.shape[1] - 20, -1, -1):
        for j in range(50, thresh.shape[0]):
            if thresh[j, i] == 0:
                x2 = i
                y2 = j
                break
        if x2 != 0:
            break

    x3, y3 = 0, 0
    for i in range(20, thresh.shape[0]):
        for j in range(20, thresh.shape[1]):
            if thresh[i, j] == 0:
                x3 = j
                y3 = i
                break
        if x3 != 0:
            break

    x4, y4 = 0, 0
    for i in range(thresh.shape[0] - 50, -1, -1):
        for j in range(20, thresh.shape[1]):
            if thresh[i, j] == 0:
                x4 = j
                y4 = i
                break
        if x4 != 0:
            break

    length = x2 - x1
    height = y4 - y3

    cv2.rectangle(thresh, (x1, y3), (x1 + length, y3 + height), (0, 0, 0), 4, 0)

    pil_image = Image.fromarray(frame)
    bitmap_image = ImageTk.PhotoImage(pil_image)
    return bitmap_image

# Mark:
# Assuming you have a Bitmap object called imshow
# bitmap_image = to_bitmap_image_two(imshow)

def to_bitmap_image_two1(hienthisau):
    src_copy = cv2.cvtColor(np.array(hienthisau), cv2.COLOR_BGR2GRAY)
    src_copy = cv2.medianBlur(src_copy, 3)
    _, src_copy = cv2.threshold(src_copy, 150, 255, cv2.THRESH_BINARY)

    x1, y1 = 0, 0
    for i in range(80, src_copy.shape[1]):
        for j in range(0, src_copy.shape[0]):
            if src_copy[j, i] == 0:
                x1 = i
                y1 = j
                break
        if x1 != 0:
            break

    x2, y2 = 0, 0
    for i in range(src_copy.shape[1] - 50, -1, -1):
        for j in range(100, src_copy.shape[0]):
            if src_copy[j, i] == 0:
                x2 = i
                y2 = j
                break
        if x2 != 0:
            break

    x3, y3 = 0, 0
    for i in range(50, src_copy.shape[0]):
        for j in range(50, src_copy.shape[1]):
            if src_copy[i, j] == 0:
                x3 = j
                y3 = i
                break
        if x3 != 0:
            break

    x4, y4 = 0, 0
    for i in range(src_copy.shape[0] - 150, -1, -1):
        for j in range(50, src_copy.shape[1]):
            if src_copy[i, j] == 0:
                x4 = j
                y4 = i
                break
        if x4 != 0:
            break

    for i in range(y4, src_copy.shape[0]):
        for j in range(src_copy.shape[1]):
            src_copy[i, j] = 255

    height = y4 - y3

    cv2.rectangle(src_copy, (0, y3), (639, y3 + height), (0, 0, 0), 4, 0)

    pil_image = Image.fromarray(src_copy)
    bitmap_image = ImageTk.PhotoImage(pil_image)
    return bitmap_image

# Example usage:
# Assuming you have a Bitmap object called hienthisau
# bitmap_image = to_bitmap_image_two1(hienthisau)

def detect_contours(imshow):
    src_copy = cv2.cvtColor(np.array(imshow), cv2.COLOR_BGR2GRAY)
    src_copy = cv2.medianBlur(src_copy, 3)
    _, src_copy = cv2.threshold(src_copy, 60, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(src_copy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    contour_index = 0
    if len(contours) > 0:
        while contour_index >= 0:
            contour = contours[contour_index]
            bounding_rect = cv2.boundingRect(contour)
            cv2.rectangle(src_copy, (bounding_rect[0], bounding_rect[1]),
                          (bounding_rect[0] + bounding_rect[2], bounding_rect[1] + bounding_rect[3]),
                          (255, 255, 255), 2)
            contour_index = contour_index + 1
    else:
        pass

    img_pil = Image.fromarray(src_copy)
    img_pil = ImageOps.grayscale(img_pil)
    img_pil = ImageOps.invert(img_pil)
    img = np.array(img_pil)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    _, img_encoded = cv2.imencode('.png', img)
    show_image = Image.open(img_encoded.tobytes())
    return show_image

def mat_to_bitmap(src_hinh):
    hinh = cv2.cvtColor(src_hinh, cv2.COLOR_BGR2RGB)
    return hinh

def get_height(imshow3):
    frame = cv2.cvtColor(np.array(imshow3), cv2.COLOR_BGR2GRAY)
    frame = cv2.medianBlur(frame, 3)
    _, src_copy = cv2.threshold(frame, 150, 255, cv2.THRESH_BINARY)

    x3, y3 = 0, 0
    for i in range(50, frame.shape[0]):
        for j in range(50, frame.shape[1]):
            if frame[i, j] == 0:
                x3 = j
                y3 = i
                break
        if x3 != 0:
            break

    x4, y4 = 0, 0
    for i in range(frame.shape[0] - 150, -1, -1):
        for j in range(50, frame.shape[1]):
            if src_copy[i, j] == 0:
                x4 = j
                y4 = i
                break
        if x4 != 0:
            break

    height = y4 - y3
    return height

def get_length(imshow2):
    frame = cv2.cvtColor(np.array(imshow2), cv2.COLOR_BGR2GRAY)
    frame = cv2.medianBlur(frame, 3)
    _, thresh = cv2.threshold(frame, 110, 255, cv2.THRESH_BINARY)

    x1, y1 = 0, 0
    for i in range(50, thresh.shape[1]):
        for j in range(50, thresh.shape[0]):
            if frame[j, i] == 0:
                x1 = i
                y1 = j
                break
        if x1 != 0:
            break

    x2, y2 = 0, 0
    for i in range(thresh.shape[1] - 20, -1, -1):
        for j in range(50, thresh.shape[0]):
            if thresh[j, i] == 0:
                x2 = i
                y2 = j
                break
        if x2 != 0:
            break

    x3, y3 = 0, 0
    for i in range(20, thresh.shape[0]):
        for j in range(20, thresh.shape[1]):
            if thresh[i, j] == 0:
                x3 = j
                y3 = i
                break
        if x3 != 0:
            break

    x4, y4 = 0, 0
    for i in range(thresh.shape[0] - 50, -1, -1):
        for j in range(20, thresh.shape[1]):
            if thresh[i, j] == 0:
                x4 = j
                y4 = i
                break
        if x4 != 0:
            break

    length_x = x2 - x1
    length_y = y4 - y3
    return (length_x, length_y)

def dem_contours(imageDurian):
    src_copy = cv2.cvtColor(imageDurian, cv2.COLOR_BGR2GRAY)
    src_copy = cv2.medianBlur(src_copy, 3)
    _, src_copy = cv2.threshold(src_copy, 60, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(src_copy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    contour_index = 0
    dem = 0
    max_count = 0

    if len(contours) > 0:
        while contour_index >= 0:
            contour = contours[contour_index]
            bounding_rect = cv2.boundingRect(contour)
            rong = bounding_rect[3]
            dai = bounding_rect[2]

            for l in range(bounding_rect[1], bounding_rect[1] + rong):
                for w in range(bounding_rect[0], bounding_rect[0] + dai):
                    color = src_copy[l, w]
                    if color == 255:
                        dem += 1

            if max_count < dem:
                max_count = dem

            dem = 0
            contour_index = contour_index + 1

    else:
        pass

    area = max_count * (1.0 * 1369 / 4260) * (1.0 * 851 / 2810) * 0.01
    area = round(area, 3)
    return area
