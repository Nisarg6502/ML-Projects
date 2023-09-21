# Decription: This program uses OpenCV to track an object and draw on the screen with it

import cv2
import numpy as np

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)  # 3 is the id for width
cap.set(4, frameHeight)  # 4 is the id for height
# 10 is the id for brightness (0-100) 0 is dark, 100 is bright as hell (literally)
cap.set(10, 150)

myColors = [[0, 10, 84, 255, 110, 255], [6, 67, 102, 255, 117, 255]]
# myColors = [[0, 100, 100, 10, 255, 255],  # Lower range for red
#             [160, 100, 100, 179, 255, 255],  # Upper range for red
#             [90, 100, 100, 120, 255, 255]]  # Blue

myColorValues = [[0, 0, 255], [0, 255, 255]]  # BGR

myPoints = []  # [x, y, colorId]


def findColor(img, myColors, myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for color in myColors:
        lower = np.array([color[0], color[2], color[4]])
        upper = np.array([color[1], color[3], color[5]])
        mask = cv2.inRange(imgHSV, lower, upper)
        # mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        # cv2.imshow(str(color[0]), mask)
        x, y = getContours(mask)
        cv2.circle(imgResult, (x, y), 10, myColorValues[count], cv2.FILLED)
        if x != 0 and y != 0:
            newPoints.append([x, y, count])
        count += 1
    return newPoints


def getContours(img):
    # RETR_EXTERNAL retrieves only the extreme outer contours (leftmost and rightmost points) of the shape of the object in the image (image, contour retrieval mode, contour approximation method)
    contours, Hierarchy = cv2.findContours(
        img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # find the contours
    # loop through the contours and draw the contours on the image (image, contours, contour index, color, thickness)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)  # calculate the area of the contour
        # print(area)
        # draw the contours on the image if the area is greater than 500
        if area > 500:
            # cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            # calculate the perimeter of the contour
            peri = cv2.arcLength(cnt, True)
            # print(peri)

            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x + w // 2, y


def drawOnCanvas(myPoints, myColorValues):
    for points in myPoints:
        cv2.circle(imgResult, (points[0], points[1]),
                   10, myColorValues[points[2]], cv2.FILLED)


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgResult = img.copy()
    newPoints = findColor(img, myColors, myColorValues)
    if len(newPoints) != 0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints) != 0:
        drawOnCanvas(myPoints, myColorValues)
    cv2.imshow("Video", imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
