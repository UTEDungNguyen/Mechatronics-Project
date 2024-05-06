import cv2 
import numpy as np
import imutils
import cv2
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours


# Initialize camera 
# intialize distance from camera to the object , which in case is 24cm
Know_distance = 24.0
# intialize the known object width, which in this case, the piece of is 12cm 
known_width = 11.0


def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: 
                    imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        hor_con = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2: 
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver

def getcoutours(img, imgContour):
    contours, hierachy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # for cnt in contours:
    #     area = cv2.contourArea(cnt)
    #     print(area)
    #     areaMin = cv2.getTrackbarPos("Area", "Parameters")
    #     if area > areaMin:  
    #         cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 7)  
    #         peri = cv2.arcLength(cnt, True)
    #         approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
    #         x, y, w, h = cv2.boundingRect(approx)
    #         cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 5)  
    #         cv2.putText(imgContour, "Area: " + str(int(area)), (x + w + 40, y + 65), cv2.FONT_HERSHEY_COMPLEX, 0.7,
    #                     (0, 255, 0), 2)

    # Loop through each contour.
    for cnt in contours: 
        area = cv2.contourArea(cnt)
        print(area)
        areaMin = cv2.getTrackbarPos("Area", "Parameters")
        # If the contour's area is less than 100, skip to the next contour.
        if cv2.contourArea(cnt) < 100:
            continue
        if area > areaMin:  
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 7)  
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
            cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 5)  
            cv2.putText(imgContour, "Area: " + str(int(area)), (x + w + 40, y + 65), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                        (0, 255, 0), 2)

    
            

# Define and distance caculation
def distance_to_camera(know_width, focal_length, per_width):
    return (know_width * focal_length) / per_width

# Size measurement
def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


def find_markers(image):
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(5,5),0)
    output_adapthresh = cv2.adaptiveThreshold (gray,255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,51, 0)  #51
    # find contour 
    cnts = cv2.findContours(output_adapthresh.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts,key=cv2.contourArea)
    return cv2.minAreaRect(c)

# Load the image from disk
img = cv2.imread("images/mui3.png")
markers = find_markers(img)
focallength = (markers[1][0]*Know_distance)/known_width
object_width_mm = 11
img = cv2.resize(img,(300,400))
# Check if the image is loaded successfully
if img is None:
    print("Error: Unable to load image.")
    exit()

framewidth = 640
frameheight = 480

def empty(a):
    pass

cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters", 640, 240)
cv2.createTrackbar("Area", "Parameters", 5000, 30000, empty)
while True:
    pixelsPerMetric = None
    imgContour = img.copy()
    # Filter Image and Pre Processing Image
    imgblur = cv2.GaussianBlur(img, (7, 7), 1)
    gray = cv2.cvtColor(imgblur, cv2.COLOR_BGR2GRAY)
    # Adapte threshold img no need Detect thresh Manual
    output_adapthresh = cv2.adaptiveThreshold (gray,255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,51, 0)  #51
    kernel = np.ones((3, 3), np.uint8)
    getcoutours(output_adapthresh , imgContour)
    imgstack = stackImages(0.8, ([img, gray, imgContour], [output_adapthresh, imgContour, gray]))

    cv2.imshow("Result Image", imgstack)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
