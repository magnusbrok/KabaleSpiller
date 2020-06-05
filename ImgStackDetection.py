import cv2
import imutils
import numpy as np
import os

import Cards

section_names = ["drawStack", "lastDraw", "1. Base stack", "2. base stack", "3. Base stack", "4. Base stack",
                 "1. tower", "2. tower", "3. tower", "4. tower", "5. tower", "6. tower", "7. tower"]

def main():

    # Load the train rank and suit images
    path = os.path.dirname(os.path.abspath(__file__))
    train_ranks = Cards.load_ranks(path + '/Card_Imgs/')
    train_suits = Cards.load_suits(path + '/Card_Imgs/')

    cardPath = 'Training-Imgs/kabale_2.jpg'

    print_img = cv2.imread(cardPath)
    print_frame = imutils.resize(print_img, 1800, 1800)

    image = cv2.imread(cardPath, cv2.IMREAD_GRAYSCALE)
    frame = imutils.resize(image, 1800, 1800)

    # cv2.imshow('frame-grayed', frame)

    # Standard prerpoccesing of input
    dilate = Cards.preprocess_imageOLD(frame)

    # contours, hierarchy = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cv2.imshow("printframe", print_frame)
    #cv2.imshow('Dialated', dilate)

    sections = Cards.cutout_board_sections(dilate)
    print_sections = Cards.cutout_board_sections(print_frame)
    cards = []
    section_counter = 0
    for i in range(12, 13):
        section = sections[i]
        print_section = print_sections[i]
        print_only = imutils.resize(print_section, 200, 140)
        #cv2.imshow(str(i), print_only)

        contours, hierarchy = cv2.findContours(section, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cnts_sort = []
        index_sort = sorted(range(len(contours)), key=lambda i: cv2.contourArea(contours[i]), reverse=True)
        # Fill empty lists with sorted contour and sorted hierarchy. Now,
        # the indices of the contour list still correspond with those of
        # the hierarchy list. The hierarchy array can be used to check if
        # the contours have parents or not.
        for j in index_sort:
            cnts_sort.append(contours[j])


        print(len(cnts_sort))

        if len(cnts_sort) != 0:
            contour = cnts_sort[0]
            card = contour

            # Approximate the corner points of the card
            peri = cv2.arcLength(card, True)
            approx = cv2.approxPolyDP(card, 0.01 * peri, True)
            pts = np.float32(approx)

            x, y, w, h = cv2.boundingRect(card)
            gray_section = cv2.cvtColor(print_section, cv2.COLOR_BGR2GRAY)

            # Flatten the card and convert it to 200x300
            warp = Cards.flatten_stack(print_sections[i], pts, w, h)

            print_warp = imutils.resize(warp, 200, 140)
            #cv2.imshow(str(i) + "warp", print_warp)
            edge_h = h-440 # 420 represents the bottom part of the first card
            edge_w = 80
            corner_h = 160
            edges = warp[0: edge_h, 0:edge_w]

            print(edge_h)
            print_edges = imutils.resize(edges, 60, 60)

            cv2.imshow(str(i) + "edge of warp", print_edges)

            i = 1
            while i*corner_h < edge_h:
                if i == 1:
                    corner = edges[edge_h-corner_h:edge_h, 0:edge_w]
                else:
                    corner = edges[edge_h - corner_h*i:edge_h-corner_h*(i-1), 0:edge_w]

                cv2.imshow(str(i)+"corner", corner)
                #above = edges[0:200, 0:80]
                #cv2.imshow("above corner", above)
                i += 1



    cv2.waitKey(0)
    cv2.destroyAllWindows()


main()

