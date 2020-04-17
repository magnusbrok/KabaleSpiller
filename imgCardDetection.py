import cv2
import imutils
import numpy as np
import os



def main():
    cardPath = 'Training-Imgs/kabale_1.jpg'

    printImg = cv2.imread(cardPath)
    printFrame = imutils.resize(printImg, 640, 640)

    image = cv2.imread(cardPath, cv2.IMREAD_GRAYSCALE)

    frame = imutils.resize(image, 640, 640)

    cv2.imshow('frame-grayed', frame)

    blur = cv2.GaussianBlur(frame, (9, 9), 0)

    edges = cv2.Canny(blur, 50, 150, True)

    cv2.imshow('edges', edges)

    kernel = np.ones((5, 5), np.uint8)
    dilate = cv2.dilate(edges, kernel, iterations=1)

    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cv2.imshow('Dialated', dilate)


    temp_contours = []

    for cnt in contours:
        area = cv2.contourArea(cnt)
        print(cv2.contourArea(cnt))
        if (area <= 30000 and area >= 1200):
            temp_contours.append(cnt)

    cv2.drawContours(printFrame, temp_contours, -1, (0, 255, 0), 3)

    cv2.imshow('Contours', printFrame)

    print("numberf of contoyurs %d -> "%len(temp_contours))




    cv2.waitKey(0)
    cv2.destroyAllWindows()



main()
