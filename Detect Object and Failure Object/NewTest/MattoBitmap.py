import cv2

def mat_to_bitmap(src_hinh):
    # Convert Mat to Bitmap
    hinh = cv2.cvtColor(src_hinh, cv2.COLOR_BGR2RGB)
    return hinh


