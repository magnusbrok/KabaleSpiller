import cv2
import imutils
import numpy as np
import os

import Cards


def main():

    cap = cv2.VideoCapture(1)
    #cap = cv2.VideoCapture('http://192.168.1.135:4905/video')

    while True:
        ret, frame = cap.read()
        frame = cv2.rotate(frame, cv2.ROTATE_180) # Only relevant for Magnus
        frame = imutils.resize(frame, 1600)
        cv2.imshow("test", frame)
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        dilate = Cards.preprocces_image(frame)

        contours, hierarchy = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cv2.imshow('Dialated', dilate)

        #pre_proc = Cards.preprocess_image(frame)

        Cards.draw_board(frame)



        # Draw all contours
        temp_contours = []

        for cnt in contours:
            area = cv2.contourArea(cnt)
            print(cv2.contourArea(cnt))
            if area >= 750:
                temp_contours.append(cnt)

        cv2.drawContours(frame, temp_contours, -1, (0, 255, 0), 3)

        cv2.imshow('Contours', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


main()
