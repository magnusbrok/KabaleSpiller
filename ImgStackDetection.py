import cv2
import imutils
import numpy as np
import os

import Cards
from DTO.cardDTO import CardDTO

section_names = ["drawStack", "lastDraw", "1. Base stack", "2. base stack", "3. Base stack", "4. Base stack",
                 "1. tower", "2. tower", "3. tower", "4. tower", "5. tower", "6. tower", "7. tower"]
IMG_size = 1600
def main():

    cardDTO = CardDTO(value="", suit="")

    # Load the train rank and suit images
    path = os.path.dirname(os.path.abspath(__file__))
    train_ranks = Cards.load_ranks(path + '/Card_Imgs/')
    train_suits = Cards.load_suits(path + '/Card_Imgs/')

    cardPath = 'Training-Imgs/kabale_1.jpg'

    print_img = cv2.imread(cardPath)
    print_frame = imutils.resize(print_img, IMG_size, IMG_size)

    image = cv2.imread(cardPath, cv2.IMREAD_GRAYSCALE)
    frame = imutils.resize(image, IMG_size, IMG_size)

    # cv2.imshow('frame-grayed', frame)

    # Standard prerpoccesing of input
    dilate = Cards.preprocess_imageOLD(frame)

    # contours, hierarchy = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    Cards.draw_board(print_frame)
    cv2.imshow("printframe", print_frame)
    #cv2.imshow('Dialated', dilate)

    sections = Cards.cutout_board_sections(dilate)
    print_sections = Cards.cutout_board_sections(print_frame)
    cards = []
    section_counter = 0
    for i in range(0, 13):
        section = sections[i]
        print_section = print_sections[i]
        print_only = imutils.resize(print_section, 200, 140)

        contours, hierarchy = cv2.findContours(section, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


        cnts_sort = []
        index_sort = sorted(range(len(contours)), key=lambda i: cv2.contourArea(contours[i]), reverse=True)
        # Fill empty lists with sorted contour and sorted hierarchy. Now,
        # the indices of the contour list still correspond with those of
        # the hierarchy list. The hierarchy array can be used to check if
        # the contours have parents or not.
        for j in index_sort:
            cnts_sort.append(contours[j])


        #print(len(cnts_sort))

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

            print_warp = imutils.resize(warp, 240, 140)
            print_warp = imutils.resize(warp, 240, 140)

            # cv2.imshow(str(i) + "warp", print_warp)
            edge_h = h  #  represents the bottom part of the first card
            edge_w = 50
            corner_h = 160
            edges = print_warp[0: edge_h, 5:edge_w]

            #cv2.imshow(str(i), edges)

            edges = imutils.resize(edges, 55)

            edges_processed = Cards.preprocces_image(edges)
            cv2.imshow(str(i), edges_processed)
            contours, hierarchy = cv2.findContours(edges_processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            filtered_contours = []
            for cnt in contours:
                area = cv2.contourArea(cnt)
                #print(cv2.contourArea(cnt))
                if area >= 200:
                    print(str(i) + "cnt Area = " + str(area))
                    filtered_contours.append(cnt)
                    x, y, w, h = cv2.boundingRect(cnt)
                    cv2.rectangle(edges, (x, y), (x + w, y + h), (0, 255, 0), 2)
            #cv2.drawContours(edges, filtered_contours, -1, (255, 0, 0), 2)
            cv2.imshow(str(i) + "Edges", edges)
            gray_section = cv2.cvtColor(edges, cv2.COLOR_BGR2GRAY)
            kernel = np.ones((2, 2), np.uint8)
            dilate = cv2.erode(gray_section, kernel, iterations=1)





            cards = []
            cardsArray = []

            j = 2
            cards_found = 0
            print("=======================")
            while j < len(filtered_contours)-1:
                cards.append(Cards.preprocess_stack_card(filtered_contours[j+1], filtered_contours[j], dilate))

                cards[cards_found].best_rank_match, cards[cards_found].best_suit_match, cards[cards_found]\
                    .rank_diff, cards[cards_found].suit_diff = Cards.match_card(
                    cards[cards_found], train_ranks, train_suits)

                #print("RESULTS for: " + str(i))
                print(cards[cards_found])
                cardDTO.suit = cards[cards_found].best_suit_match
                cardDTO.value = cards[cards_found].best_rank_match
                cardsArray.append(cardDTO())
                #print(cards[cards_found].best_rank_match, cards[cards_found].best_suit_match)
                #print(cards[cards_found].rank_diff, cards[cards_found].suit_diff)
                j += 2
                cards_found += 1
                print("============================")
        else:
            print("RESULTS for: " + str(i))
            print("NO contours aka no cards biutch")
            #print(cards[cards_found].best_rank_match, cards[cards_found].best_suit_match)
            #print(cards[cards_found].rank_diff, cards[cards_found].suit_diff)
            #j += 2
            #cards_found += 1
            print("============================")





    cv2.waitKey(0)
    cv2.destroyAllWindows()


main()

