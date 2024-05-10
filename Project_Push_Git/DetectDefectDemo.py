# import cv2
# import numpy as np
# from PIL import Image,ImageTk 

# cap = cv2.VideoCapture(0) # 0: Config camera in Laptop
# def stackImages(scale,imgArray):
#     rows = len(imgArray)
#     cols = len(imgArray[0])
#     rowsAvailable = isinstance(imgArray[0], list)
#     width = imgArray[0][0].shape[1]
#     height = imgArray[0][0].shape[0]
#     if rowsAvailable:
#         for x in range ( 0, rows):
#             for y in range(0, cols):
#                 if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
#                     imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
#                 else:
#                     imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
#                 if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
#         imageBlank = np.zeros((height, width, 3), np.uint8)
#         hor = [imageBlank]*rows
#         hor_con = [imageBlank]*rows
#         for x in range(0, rows):
#             hor[x] = np.hstack(imgArray[x])
#         ver = np.vstack(hor)
#     else:
#         for x in range(0, rows):
#             if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
#                 imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
#             else:
#                 imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
#             if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
#         hor= np.hstack(imgArray)
#         ver = hor
#     return ver

# while True: 
#     # Read Camera in Laptop and Capture Image continute
#     _,frame = cap.read()
#     hsv_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) # Convert RGB to HSV 
    
#     # Set up Red Colour
#     low_red = np.array([161, 155, 84])  # ngưỡng min Red
#     high_red = np.array([179, 255, 255])  # ngưỡng max Red 
#     red_mask = cv2.inRange(hsv_frame, low_red, high_red)  #tạo mặt nạ phân tách kênh red có gtri từ ngưỡng min 2 max
#     red = cv2.bitwise_and(frame, frame, mask=red_mask) #loại bỏ các màu k mong muốn và chuyển chúng thành màu đen,chỉ giữ lại màu đỏ
#     (contours,hierarchy)=cv2.findContours(red_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#         #contour tìm 1 đối tượng trắng trên nền đen, chú ý việc đặt ngưỡng cv2.RETR_TREE, chain: là method of contour
#         #redmask gtri anh nhị phan,retr_tree tìm all đường biên gần nhất
#         # chain approx là pp chỉ trả về 1 điểm cụ thể, từ đó nhận diện đường bao phù hợp nhất
#     for piv, contour in enumerate(contours):
#             area = cv2.contourArea(contour)
#             #contourArea có thể tính toán diện tích đường bao
#             if(area>300):
#                 #tác dụng khữ nhiễu đói với vật có kt nhỏ hơn 300 và không tạo khug với những vật đó
#                 x,y,w,h = cv2.boundingRect(contour)
#                 #boundingRect vẽ hình CN xung quanh ảnh nhị phân
#                 if(w > 120) and (h>120):  
#                     img = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),1)
#                     #cv2.rectanle()  được sử dụng để vẽ 1 hình chữ nhật trên 1 hình ảnh bất kì nào
#                     # đó với tọa độ bắt đầu là (x,y) và tọa độ kết thúc (x+w, y+h) tiếp đó là chọn màu kẻ viền(0, 0, 255) và độ rộng đưởng kẻ(1).
#                     cv2.putText(frame,"Red",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,255))   
#                     #v2.putText có chức năng của cú pháp là tạo ra 1 văn bản trên hình ảnh đã cho với văn bản cần ghi là “Red color”, phông chữ 
#                     # tùy chọn ( cv2.FONT_HERSHAY_SIMPLEX ), độ rộng nét chữ (0.7) và màu chữ (0, 0, 255).
    
#     #Set up Blue Colour
#     low_blue = np.array([94, 80, 2])
#     high_blue = np.array([126, 255, 255])
#     blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue)
#     blue = cv2.bitwise_and(frame, frame, mask=blue_mask)
#     (contours,hierarchy)=cv2.findContours(blue_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#     for piv, contour in enumerate(contours):
#         area = cv2.contourArea(contour)
#         if(area>300):
#             x,y,w,h = cv2.boundingRect(contour)
#             if(w > 150) and (h>150):  
#                 img = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),1)
#                 cv2.putText(frame,"Blue",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,255))

#     # Set up Green Colour
#     low_green = np.array([25, 52, 72])
#     high_green = np.array([102, 255, 255])
#     green_mask = cv2.inRange(hsv_frame, low_green, high_green)
#     green = cv2.bitwise_and(frame, frame, mask=green_mask)
#     (contours,hierarchy)=cv2.findContours(green_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#     for piv, contour in enumerate(contours):
#             area = cv2.contourArea(contour)
#             if(area>300):
#                 x,y,w,h = cv2.boundingRect(contour)
#                 if(w > 150) and (h>150):  
#                     img = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),1)
#                     cv2.putText(frame,"Green",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,255))


#     # Set up Yellow Colour
#     low_yellow = np.array([0, 57, 167])
#     high_yellow = np.array([124, 255, 255])
#     yellow_mask = cv2.inRange(hsv_frame, low_yellow, high_yellow)
#     yellow = cv2.bitwise_and(frame, frame, mask=yellow_mask)
#     (contours,hierarchy)=cv2.findContours(yellow_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#     for piv, contour in enumerate(contours):
#             area = cv2.contourArea(contour)
#             if(area>300):         
#                 x,y,w,h = cv2.boundingRect(contour)
#                 if(w > 150) and (h>150):  
#                     img = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),1)
#                     cv2.putText(frame,"Yellow",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,255))

#     # Create Results
#     low = np.array([0, 42, 0])
#     high = np.array([179, 255, 255])
#     mask = cv2.inRange(hsv_frame, low, high)
#     result = cv2.bitwise_and(frame, frame, mask=mask)  # nhận diện
#     imgStack = stackImages(0.8,([frame,hsv_frame,],[mask,result]))

#     #cv2.imshow("Video",frame) # Image from Camera Input
#     #cv2.imshow("Red",red)     # Detect Red channel
#     #cv2.imshow("Blue",blue)   # Detect Blue channel
#     #cv2.imshow("Green",green) # Detect Green channel
#     #cv2.imshow("Yellow",yellow) # Detect Yellow channel
#     #cv2.imshow("Mask",mask) 
#     #cv2.imshow("Results",result) # Detect Results Output
#     cv2.imshow("Image Stack",imgStack)

#     if cv2.waitKey(1)== ord('q'):
#         break 
# cv2.destroyAllWindows()

# organizing imports

import cv2
import numpy as np
import imutils
segmented = []
# path to input image is specified and
# image is loaded with imread command
image1 = cv2.imread("testhu.jpg")
image1 = cv2.resize(image1,(400,300))
blue, green, red = cv2.split(image1)
# cv2.cvtColor is applied over the
# image input with applied parameters
# to convert the image in grayscale

img = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)

# applying  thresholding

thresh1 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C ,
										cv2.THRESH_BINARY, 9, 18)

contours1, hierarchy1 = cv2.findContours(thresh1, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
# cnts =imutils.grab_contours(contours1)
# img_result = image1.copy()
# countContours = 0
# for cnt in contours1:
#     c_area = cv2.contourArea(cnt)
#     print(c_area)
#     if c_area >=100 and c_area <3000:
#         countContours += 1
#         cv2.drawContours(img_result,[cnt], -1, (0,255,0) , 2)
#     if c_area < 100 and c_area >400:
#         countContours += 1
#         cv2.drawContours(img_result,[cnt], -1, (0,255,0) , 2)
# draw contours on the original image
13
image_contour_blue = img.copy()
cv2.drawContours(image1, contours=contours1, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
# see the results
cv2.imshow('Contour detection using blue channels only', image1)
cv2.waitKey(0)
cv2.imshow('Contour detection using blue channels only', blue)
cv2.waitKey(0)
cv2.imshow('Contour detection using green channels only', green)
cv2.waitKey(0)
cv2.imshow('Contour detection using red channels only', red)
cv2.waitKey(0)

# the window showing output images
# with the corresponding thresholding
# techniques applied to the input image
cv2.imshow('Adaptive Mean', thresh1)
# cv2.imshow('Adaptive Gaussian', thresh2)

# De-allocate any associated memory usage
if cv2.waitKey(0) & 0xff == 27:
	cv2.destroyAllWindows()


