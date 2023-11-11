# import cv2
# import numpy as np

# # Đọc ảnh đầu vào
# file_hinh='C:\\Users\\havie\\Desktop\\DO_AN_CDT\\source_code\\main\\durian.jpg'
# image = cv2.imread(file_hinh)

# # Định nghĩa các điểm của vùng bạn muốn cắt (4 điểm)
# points = np.array([[100, 100],  # Góc trên cùng bên trái
#                    [300, 100],  # Góc trên cùng bên phải
#                    [300, 300],  # Góc dưới cùng bên phải
#                    [100, 300]], dtype=np.float32)  # Góc dưới cùng bên trái

# # Xác định các điểm mới sau khi cắt (4 điểm)
# new_points = np.array([[0, 0],  # Góc trên cùng bên trái
#                        [200, 0],  # Góc trên cùng bên phải
#                        [200, 200],  # Góc dưới cùng bên phải
#                        [0, 200]], dtype=np.float32)  # Góc dưới cùng bên trái

# # Tính ma trận biến đổi affine
# matrix = cv2.getPerspectiveTransform(points, new_points)

# # Thực hiện biến đổi ảnh
# result = cv2.warpPerspective(image, matrix, (200, 200))

# # Lưu ảnh kết quả
# local_file ='C:\\Users\\havie\\Desktop\\DO_AN_CDT\\source_code\\main'
# cv2.imwrite(local_file + '\\per_trans.jpg', result)

# # Hiển thị ảnh kết quả
# cv2.imshow(local_file + '\\per_trans.jpg', result)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
import cv2
import numpy as np
import imutils
def otsu(img):
    hist = cv2.calcHist([img],[0],None,[256],[0,255]) # tính histogram của ảnh

    hist_norm = hist.ravel()
    phuong_sai_t = 0 
    M,N = img.shape
 

    for nguong in range(256):
        Tong_gt_xam_A = 0  
        Tong_gt_xam_B = 0  
        Tong_pixel_A = 0  
        Tong_pixel_B = 1   
     

        for x in range (0,256):
            if x >= nguong:
               Tong_pixel_A += hist_norm[x]
               Tong_gt_xam_A += x*(hist_norm[x]/M*N)
            else:
                Tong_pixel_B += hist_norm[x]
                Tong_gt_xam_B += x*(hist_norm[x]/M*N)
        
        mG = Tong_gt_xam_A + Tong_gt_xam_B  # cuong do trung binh cua anh

        P1 =Tong_pixel_A/(M*N)  # tong xac suat tich luy
        P2 =Tong_pixel_B/(M*N)

        m1 = Tong_gt_xam_A/P1   # gtri cuong do trung binh cua pixel
        m2 = Tong_gt_xam_B/P2     
        phuong_sai = P1*((m1-mG)**2)+P2*((m2-mG)**2) 
       


        if (phuong_sai > phuong_sai_t):
            phuong_sai_t = phuong_sai
            nguong_toi_uu = nguong  



    print("Ngưỡng tìm được", nguong_toi_uu)
    return nguong_toi_uu



def phan_doan_bang_cat_nguong(img, nguong):
    img_phan_doan = np.zeros_like(img)
    m, n = img.shape
    for i in range(m):
        for j in range(n):
            if (img[i,j] < nguong):
                img_phan_doan[i,j] = 0
            else:
                img_phan_doan[i,j] = 225 
    return img_phan_doan
# Đọc ảnh và chuyển đổi sang ảnh grayscale
image = cv2.imread('main\\image\\1.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Áp dụng GaussianBlur để giảm nhiễu
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

nguong_toi_uu= otsu(blurred)

# Sử dụng hàm Canny để phát hiện các biên
edges = phan_doan_bang_cat_nguong(blurred, nguong_toi_uu)

# # Tìm contours trong ảnh
_, img_binary = cv2.threshold(gray, nguong_toi_uu,255, cv2.THRESH_BINARY_INV)
contours = cv2.findContours(img_binary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts =imutils.grab_contours(contours)
img_result = image.copy()
countContours = 0
for cnt in cnts:
    c_area = cv2.contourArea(cnt)

    countContours += 1
    cv2.drawContours(img_result,[cnt], -1, (0,255,0) , 2)

# contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# # Chọn contour lớn nhất
# largest_contour = max(contours, key=cv2.contourArea)

# # Ưu tiên đơn giản hóa contour để giảm số lượng điểm
# epsilon = 0.04 * cv2.arcLength(largest_contour, True)
# approx = cv2.approxPolyDP(largest_contour, epsilon, True)

# # Lặp qua các điểm của contour và vẽ đường và góc
# for point in approx:
#     x, y = point.ravel()
#     cv2.circle(image, (x, y), 5, (0, 255, 0), -1)  # vẽ đường tròn tại mỗi điểm
#     cv2.putText(image, f'({x}, {y})', (x + 10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

# Hiển thị ảnh
cv2.imshow('Image with Corners', img_result)
cv2.imshow('Image ', edges)
cv2.waitKey(0)
cv2.destroyAllWindows()
# Trong đoạn mã trên:

# Sử dụng hàm cv2.findContours để tìm contours trong ảnh.
# Chọn contour lớn nhất (hoặc bạn có thể chọn contour khác tùy thuộc vào ứng dụng cụ thể của bạn).
# Ưu tiên đơn giản hóa contour để giảm số lượng điểm.
# Lặp qua các điểm của contour và vẽ đường và góc tại mỗi điểm.
# Vui lòng thay đổi đường dẫn đến ảnh và điều chỉnh các tham số nếu cần thiết dựa trên ảnh cụ thể của bạn.





