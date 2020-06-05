import cv2
import imutils
import numpy as np
import os

import Cards

section_names = ["drawStack", "lastDraw", "1. Base stack", "2. base stack", "3. Base stack", "4. Base stack",
                 "1. tower", "2. tower", "3. tower", "4. tower", "5. tower", "6. tower", "7. tower"]

def main():
    cardPath = 'Training-Imgs/kabale_1.jpg'
    #cardPath = 'Training-Imgs/2_card.jpg'

    print_img = cv2.imread(cardPath)
    print_frame = imutils.resize(print_img, 640, 640)

    image = cv2.imread(cardPath, cv2.IMREAD_GRAYSCALE)
    frame = imutils.resize(image, 640, 640)

    #cv2.imshow('frame-grayed', frame)

    # Standard prerpoccesing of input
    dilate = Cards.preprocces_image(frame)

    # contours, hierarchy = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    Cards.draw_board(print_frame)
    cv2.imshow("printframe", print_frame)
    #cv2.imshow('Dialated', dilate)

    sections = Cards.cutout_board_sections(dilate)
    print_sections = Cards.cutout_board_sections(print_frame)
    temp_contours = []
    section_counter = 0
    for i in range(0, 6):
        section = sections[i]
        contours, hierarchy = cv2.findContours(section, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        print(len(contours))

        if len(contours) != 0:
            cnt = contours[0]
            print(cv2.contourArea(cnt))
            temp_contours.append(cnt)
            card = cnt

            # Approximate the corner points of the card
            peri = cv2.arcLength(card, True)
            approx = cv2.approxPolyDP(card, 0.01 * peri, True)
            pts = np.float32(approx)

            x, y, w, h = cv2.boundingRect(card)

            # Flatten the card and convert it to 200x300
            warp = Cards.flattener(print_sections[i], pts, w, h)
            #cv2.drawContours(warp, cnt, -1, (0, 255, 0), 3)
            cv2.imshow(section_names[section_counter], warp)
            section_counter += 1

    #for i in range(6, 13):
        #do something with building stacks



    #cv2.drawContours(print_frame, temp_contours, -1, (0, 255, 0), 3)
    #cv2.imshow("tefawfwaf", print_frame)

    print("number of contours %d -> "%len(temp_contours))

    cv2.waitKey(0)
    cv2.destroyAllWindows()

main()

