import cv2

video_capture = cv2.VideoCapture(0)
    
while True: 
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2G    RAY)z

    # Hiển thị khung kết quả                       
    cv2.imshow('Video', frame)                                                                                                                                                                                              

    if cv2.waitKey(1) & 0xFF == ord('q'):   
        break

# Sau khi thực hiện thành công thì giải phóng ảnh
video_capture.release()
cv2.destroyAllWindows()
