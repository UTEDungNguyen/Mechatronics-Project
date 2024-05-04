import cv2
import numpy as np

# Đọc ảnh đầu vào
image = cv2.imread('durian_test_2.jpg')

# Đọc ảnh của trái sầu riêng (template)
template = cv2.imread('durian_matching.png')

# Thực hiện template matching
result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

# Tìm vị trí tối ưu của trái sầu riêng trong ảnh
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
# Lấy kích thước của template
template_height, template_width = template.shape[:2]

# Tìm tọa độ của góc trên cùng bên trái và góc dưới cùng bên phải của đối tượng được phát hiện
top_left = max_loc
bottom_right = (top_left[0] + template_width, top_left[1] + template_height)

# Vẽ hình chữ nhật xung quanh đối tượng được phát hiện
cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)

# Lưu ảnh kết quả
cv2.imwrite('detected_mangosteen.jpg', image)

# Hiển thị ảnh kết quả
cv2.imshow('Detected Mangosteen', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
