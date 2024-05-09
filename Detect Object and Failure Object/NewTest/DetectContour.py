import cv2
import numpy as np
from PIL import Image, ImageOps

def detect_contours(imshow):
    # Convert Bitmap to Mat
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

    # Convert Mat back to BitmapImage
    img_pil = Image.fromarray(src_copy)
    img_pil = ImageOps.grayscale(img_pil)
    img_pil = ImageOps.invert(img_pil)
    img = np.array(img_pil)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    _, img_encoded = cv2.imencode('.png', img)
    show_image = Image.open(img_encoded.tobytes())
    return show_image
