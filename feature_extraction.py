import cv2

# Đọc ảnh đối tượng trái sầu riêng
template = cv2.imread('durian_matching.png', cv2.IMREAD_GRAYSCALE)

# Lấy kích thước ban đầu của ảnh
original_height_template, original_width_template = template.shape[:2]      

# Tính kích thước mới (1/2 kích thước ban đầu)
new_height_template = int(original_height_template / 2)
new_width_template = int(original_width_template / 2)

# Resize ảnh
resized_image_template = cv2.resize(template, (new_width_template, new_height_template))

# Đọc ảnh đầu vào
image = cv2.imread('durian_matching.png', cv2.IMREAD_GRAYSCALE)

# Lấy kích thước ban đầu của ảnh
original_height, original_width = image.shape[:2]

# Tính kích thước mới (1/2 kích thước ban đầu)
new_height = int(original_height / 2)
new_width = int(original_width / 2)

# Resize ảnh
resized_image = cv2.resize(image, (new_width, new_height))

# Tạo một bộ trình phát hiện SIFT
sift = cv2.SIFT_create()

# Tìm các điểm đặc trưng và các vector mô tả của đối tượng      
keypoints_template, descriptors_template = sift.detectAndCompute(resized_image_template, None)
keypoints_image, descriptors_image = sift.detectAndCompute(resized_image, None)

# Tạo bộ matcher để so khớp các điểm đặc trưng
matcher = cv2.BFMatcher()

# Tìm các điểm đặc trưng tương đối giữa đối tượng và ảnh
matches = matcher.knnMatch(descriptors_template, descriptors_image, k=2)    

# Sắp xếp các kết quả theo thứ tự tăng dần về khoảng cách   
# matches = sorted(matches, key=lambda x: x.distance)    

# Lọc các kết quả tốt nhất
good_matches = []
for m, n in matches:
    if m.distance < 0.75 * n.distance:
        good_matches.append(m)

# In ra số lượng đặc trưng tìm thấy khớp
print("Số lượng đặc trưng tìm thấy khớp: ", len(good_matches))

# Kiểm tra xem số lượng đặc trưng khớp có đủ lớn để xác định trái sầu riêng hay không
if len(good_matches) > 50:  # Tùy chỉnh ngưỡng này tùy theo hình ảnh cụ thể
    print("Trái sầu riêng được tìm thấy!")
else:
    print("Không tìm thấy trái sầu riêng.")

# Vẽ các điểm đặc trưng được so khớp lên ảnh    
result = cv2.drawMatches(resized_image_template, keypoints_template, resized_image, keypoints_image, good_matches, None)

# Hiển thị ảnh kết quả với các điểm đặc trưng
cv2.imshow('Feature Matching Result', result)   
cv2.waitKey(0)
cv2.destroyAllWindows()
