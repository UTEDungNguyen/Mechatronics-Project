import cv2

def dem_contours(imageDurian):
    # Convert Bitmap to Mat
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
