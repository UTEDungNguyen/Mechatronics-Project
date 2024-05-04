import cv2
import numpy as np
from PIL import Image,ImageTk 

cap = cv2.VideoCapture(0) # 0: Config camera in Laptop

while True: 
    # Read Camera in Laptop and Capture Image continute
    _,frame = cap.read()
    hsv_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) # Convert RGB to HSV 
    
    # Set up Red Colour
    low_red = np.array([161, 155, 84])  # ngưỡng min Red
    high_red = np.array([179, 255, 255])  # ngưỡng max Red 
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)  #tạo mặt nạ phân tách kênh red có gtri từ ngưỡng min 2 max
    red = cv2.bitwise_and(frame, frame, mask=red_mask) #loại bỏ các màu k mong muốn và chuyển chúng thành màu đen,chỉ giữ lại màu đỏ
    (contours,hierarchy)=cv2.findContours(red_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        #contour tìm 1 đối tượng trắng trên nền đen, chú ý việc đặt ngưỡng cv2.RETR_TREE, chain: là method of contour
        #redmask gtri anh nhị phan,retr_tree tìm all đường biên gần nhất
        # chain approx là pp chỉ trả về 1 điểm cụ thể, từ đó nhận diện đường bao phù hợp nhất
    for piv, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            #contourArea có thể tính toán diện tích đường bao
            if(area>300):
                #tác dụng khữ nhiễu đói với vật có kt nhỏ hơn 300 và không tạo khug với những vật đó
                x,y,w,h = cv2.boundingRect(contour)
                #boundingRect vẽ hình CN xung quanh ảnh nhị phân
                if(w > 120) and (h>120):  
                    img = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),1)
                    #cv2.rectanle()  được sử dụng để vẽ 1 hình chữ nhật trên 1 hình ảnh bất kì nào
                    # đó với tọa độ bắt đầu là (x,y) và tọa độ kết thúc (x+w, y+h) tiếp đó là chọn màu kẻ viền(0, 0, 255) và độ rộng đưởng kẻ(1).
                    cv2.putText(frame,"Red",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,255))   
                    #v2.putText có chức năng của cú pháp là tạo ra 1 văn bản trên hình ảnh đã cho với văn bản cần ghi là “Red color”, phông chữ 
                    # tùy chọn ( cv2.FONT_HERSHAY_SIMPLEX ), độ rộng nét chữ (0.7) và màu chữ (0, 0, 255).
    
    #Set up Blue Colour
    low_blue = np.array([94, 80, 2])
    high_blue = np.array([126, 255, 255])
    blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue)
    blue = cv2.bitwise_and(frame, frame, mask=blue_mask)
    (contours,hierarchy)=cv2.findContours(blue_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for piv, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area>300):
            x,y,w,h = cv2.boundingRect(contour)
            if(w > 150) and (h>150):  
                img = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),1)
                cv2.putText(frame,"Blue",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,255))

    # Set up Green Colour
    low_green = np.array([25, 52, 72])
    high_green = np.array([102, 255, 255])
    green_mask = cv2.inRange(hsv_frame, low_green, high_green)
    green = cv2.bitwise_and(frame, frame, mask=green_mask)
    (contours,hierarchy)=cv2.findContours(green_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for piv, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area>300):
                x,y,w,h = cv2.boundingRect(contour)
                if(w > 150) and (h>150):  
                    img = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),1)
                    cv2.putText(frame,"Green",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,255))


    # Set up Yellow Colour
    low_yellow = np.array([0, 57, 167])
    high_yellow = np.array([124, 255, 255])
    yellow_mask = cv2.inRange(hsv_frame, low_yellow, high_yellow)
    yellow = cv2.bitwise_and(frame, frame, mask=yellow_mask)
    (contours,hierarchy)=cv2.findContours(yellow_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for piv, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area>300):         
                x,y,w,h = cv2.boundingRect(contour)
                if(w > 150) and (h>150):  
                    img = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),1)
                    cv2.putText(frame,"Yellow",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,255))

    # Create Results
    low = np.array([0, 42, 0])
    high = np.array([179, 255, 255])
    mask = cv2.inRange(hsv_frame, low, high)
    result = cv2.bitwise_and(frame, frame, mask=mask)  # nhận diện
    
    cv2.imshow("Video",frame) # Image from Camera Input
    #cv2.imshow("Red",red)     # Detect Red channel
    #cv2.imshow("Blue",blue)   # Detect Blue channel
    #cv2.imshow("Green",green) # Detect Green channel
    #cv2.imshow("Yellow",yellow) # Detect Yellow channel
    cv2.imshow("Mask",mask) 
    cv2.imshow("Results",result) # Detect Results Output


    if cv2.waitKey(1)== ord('q'):
        break 
cv2.destroyAllWindows()




