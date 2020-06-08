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

    cardPath = 'Training-Imgs/kabale_1.jpg'
    #cardPath = 'Training-Imgs/2_card.jpg'

    img_size = 1600

    print_img = cv2.imread(cardPath)
    print_frame = imutils.resize(print_img, img_size, img_size)

    image = cv2.imread(cardPath, cv2.IMREAD_GRAYSCALE)
    frame = imutils.resize(image, img_size, img_size)

    # cv2.imshow('frame-grayed', frame)

    # Standard prerpoccesing of input
    dilate = Cards.preprocess_imageOLD(frame)

    # contours, hierarchy = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    Cards.draw_board(print_frame)
    cv2.imshow("printframe", print_frame)
    cv2.imshow('Dialated', dilate)

    sections = Cards.cutout_board_sections(dilate)
    print_sections = Cards.cutout_board_sections(print_frame)
    cards = []
    section_counter = 0
    for i in range(0, 6):
        section = sections[i]
        printable_section = print_sections[i]
        contours, hierarchy = cv2.findContours(section, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        print(len(contours))

        if len(contours) != 0:
            cnt = contours[0]

            gray_section = cv2.cvtColor(printable_section, cv2.COLOR_BGR2GRAY)

            cards.append(Cards.preprocess_card(cnt, gray_section))
            # cv2.imshow("testsection", sections[testSection])

            # Find the best rank and suit match for the card.
            cards[i].best_rank_match, cards[i].best_suit_match, cards[i].rank_diff, cards[
                i].suit_diff = Cards.match_card(
                cards[i], train_ranks, train_suits)

            found_card = cards[i]
            print(found_card.best_rank_match + found_card.best_suit_match)
            try:
                cv2.imshow(str(section_counter)+ "rank", found_card.rank_img)
                cv2.imshow(str(section_counter)+ "card suit", found_card.suit_img)
            except:
                print("no card found")



            section_counter += 1

    cv2.waitKey(0)
    cv2.destroyAllWindows()


main()

