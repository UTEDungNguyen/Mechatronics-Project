import cv2
import numpy as np

# Đọc ảnh đầu vào
image = cv2.imread('durian_test.jpg')

# Định nghĩa các điểm của vùng bạn muốn cắt (4 điểm)
points = np.array([[100, 100],  # Góc trên cùng bên trái
                   [300, 100],  # Góc trên cùng bên phải
                   [300, 300],  # Góc dưới cùng bên phải
                   [100, 300]], dtype=np.float32)  # Góc dưới cùng bên trái

# Xác định các điểm mới sau khi cắt (4 điểm)
new_points = np.array([[0, 0],  # Góc trên cùng bên trái
                       [200, 0],  # Góc trên cùng bên phải
                       [200, 200],  # Góc dưới cùng bên phải
                       [0, 200]], dtype=np.float32)  # Góc dưới cùng bên trái

# Tính ma trận biến đổi affine
matrix = cv2.getPerspectiveTransform(points, new_points)

# Thực hiện biến đổi ảnh
result = cv2.warpPerspective(image, matrix, (200, 200))

# # Lưu ảnh kết quả
# cv2.imwrite('cropped_image_affine.jpg', result)   

# Hiển thị ảnh kết quả
cv2.imshow('original_durian', image)
cv2.imshow('Cropped Image (Affine)', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
