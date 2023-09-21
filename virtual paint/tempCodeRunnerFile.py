def getContours(img):
#     # RETR_EXTERNAL retrieves only the extreme outer contours (leftmost and rightmost points) of the shape of the object in the image (image, contour retrieval mode, contour approximation method)
#     contours, Hierarchy = cv2.findContours(
#         img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # find the contours
#     # loop through the contours and draw the contours on the image (image, contours, contour index, color, thickness)
#     for cnt in contours:
#         area = cv2.contourArea(cnt)  # calculate the area of the contour
#         print(area)
#         # draw the contours on the image if the area is greater than 500
#         if area > 500:
#             cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
#             # calculate the perimeter of the contour
#             peri = cv2.arcLength(cnt, True)
#             print(peri)

#             approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
#             print(len(approx))

#             objCor = len(approx)  # number of corners of the contour
#             x, y, w, h = cv2.boundingRect(approx)
