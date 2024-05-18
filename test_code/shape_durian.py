
 
import cv2
import imutils
import numpy as np
import os



folder_img ='Test_code\image_sample'

width = 500
high =500

# file_img = r'D:\\DO_AN_CDT\\source_dung\\Mechatronics-Project\\sample_4.jpg'



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


list_img = os.listdir(folder_img)
for img in list_img:
    link_img = os.path.join(folder_img,img)
    img = cv2.imread(link_img)


    img_scale = cv2.resize(img,(high,width))

    gray_img = cv2.cvtColor(img_scale, cv2.COLOR_RGB2GRAY)

# seg_img = phan_doan_bang_cat_nguong(gray_img, otsu(gray_img))


# cv2.imshow('hahaha', seg_img)
# image = cv2.imread(present_path)

    thresh = otsu(gray_img) 
    _, img_binary = cv2.threshold(gray_img, thresh,255, cv2.THRESH_BINARY_INV)
    contours = cv2.findContours(img_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts =imutils.grab_contours(contours)
    img_result = img_scale.copy()
    # countContours = 0   
    for cnt in cnts:
        # countContours+=1 
        area = cv2.contourArea(cnt)
        print(f'############################{area}')
        if area > 6000:
            cv2.drawContours(img_result,[cnt], -1, (0,255,0) , 2)

            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(img_result,(x,y),(x+w,y+h),(255,0,0),2)
            print(x,y,w,h)
        else: pass

    cv2.imshow('a', img_result)
    # cnts =imutils.grab_contours(contours)


    # new_img = img_binary[495:5,0:296]/
    cv2.imshow('f',img_binary)
    # cv2.imshow('d',seg_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()