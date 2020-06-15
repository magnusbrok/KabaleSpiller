import cv2
import imutils
import numpy as np
import os

from Detection import Cards
from DTO.buildingTowerDTO import BuildingTowerDTO
from DTO.cardDTO import CardDTO

section_names = ["drawStack", "lastDraw", "1. Base stack", "2. base stack", "3. Base stack", "4. Base stack",
                 "1. tower", "2. tower", "3. tower", "4. tower", "5. tower", "6. tower", "7. tower"]

def main():

    # Load the train rank and suit images
    path = os.path.dirname(os.path.abspath(__file__))
    train_ranks = Cards.load_ranks(path + '/Card_Imgs/')
    train_suits = Cards.load_suits(path + '/Card_Imgs/')

    cardPath = 'Training-Imgs/opencv_frame_4.png'
    cardPath = 'Training-Imgs/test_billeder.png'



    print_img = cv2.imread(cardPath)
    print_frame = imutils.resize(print_img, Cards.feed_width, Cards.feed_hight)

    image = cv2.imread(cardPath, cv2.IMREAD_GRAYSCALE)
    frame = imutils.resize(image, Cards.feed_width, Cards.feed_hight)

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
    buildingTowerArray = []
    base_stack_array = []
    section_counter = 0
    for i in range(6, 12):
        section = sections[i]
        print_section = print_sections[i]

        contours, hierarchy = cv2.findContours(section, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cnts_sort = Cards.sort_contours(contours)
        if len(cnts_sort) != 0:
            contour = cnts_sort[0]
            card = contour
            # Approximate the corner points of the card and flatten it
            peri = cv2.arcLength(card, True)
            approx = cv2.approxPolyDP(card, 0.01 * peri, True)
            pts = np.float32(approx)
            x, y, w, h = cv2.boundingRect(card)
            # Flatten the card and convert it to 200x300
            warp = Cards.flatten_stack(print_section, pts, w, h)


            #testImg = Cards.flatten_stack(image, 100, Cards.feed_width, Cards.feed_hight)
            #cv2.imshow("testeer", testImg)
            warp = imutils.resize(warp, 300)


            cv2.imshow(str(i) + "warp", warp)

            edge_h = h*2  #  represents the bottom part of the first card
            edge_w = 50
            edge_indent = 5
            edges = warp[0: edge_h, edge_indent:edge_w]

            warp = Cards.flatten_stack(print_section, pts, w, h)
            warp = imutils.resize(warp, 300)
            print_edges = warp[0: edge_h, edge_indent:edge_w]
            #edges = imutils.resize(edges, 75)
            #print_edges = imutils.resize(print_edges, 75)
            cv2.imshow("wdaw", print_edges)

            #cv2.imshow(str(i) + "normal", edges)

            #edges = imutils.resize(edges, 100)

            #cv2.imshow(str(i) + "rezises", edges)

            edges_processed = Cards.preprocces_image(edges)
            #cv2.imshow(str(i) + "processed", edges_processed)


            contours, hierarchy = cv2.findContours(edges_processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            filtered_contours = []
            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)
                area = w*h
                area = cv2.contourArea(cnt)
                #print(cv2.contourArea(cnt))
                if area >= 200:
                    print(str(i) + "cnt Area = " + str(area))
                    filtered_contours.append(cnt)
                    x, y, w, h = cv2.boundingRect(cnt)
                    cv2.rectangle(print_edges, (x, y), (x + w, y + h), (0, 255, 0), 1)
            #cv2.drawContours(edges, filtered_contours, -1, (255, 0, 0), 2)
            cv2.imshow(str(i) + "printimg", print_edges)


            gray_section = cv2.cvtColor(edges, cv2.COLOR_BGR2GRAY)
            #cv2.imshow("greaaa", gray_section)
            kernel = np.ones((2, 2), np.uint8)
            dilate = cv2.erode(gray_section, kernel, iterations=2)






            cards = []
            cardsArray = []



            j = 2
            cards_found = 0
            print("=======================")
            while j < len(filtered_contours)-1:
                cards.append(Cards.preprocess_stack_card(filtered_contours[j + 1], filtered_contours[j], dilate))

                cards[cards_found].best_rank_match, cards[cards_found].best_suit_match, cards[cards_found]\
                    .rank_diff, cards[cards_found].suit_diff = Cards.match_card(
                    cards[cards_found], train_ranks, train_suits)

                # print("RESULTS for: " + str(i))
                # print(cards[cards_found])
                cardDTO = CardDTO(value=cards[cards_found].best_rank_match, suit=cards[cards_found].best_suit_match)
                # cardDTO.suit = cards[cards_found].best_suit_match
                # cardDTO.value = cards[cards_found].best_rank_match
                cardsArray.append(cardDTO)

                if i == 1:
                    currentCard = cardDTO

                if 1 < i < 6:
                    base_stack_array.append(cardDTO)




                # print(cards[cards_found].best_rank_match, cards[cards_found].best_suit_match)
                print(cards[cards_found].rank_diff, cards[cards_found].suit_diff)
                print(cardsArray[cards_found].value, cardsArray[cards_found].suit)
                j += 2
                cards_found += 1
                print("============================")

            if 5 < i:
                # Tilføjer array af cardDTO objekter til buildingTowerDTO.faceUpCards, er ikke 100% sikker på dette
                # er den rigtige måde at gøre det på.
                # TODO: tilføj så vi ved om der er face down kort eller ej
                cardsArray = cardsArray[::-1]
                buildingTower = BuildingTowerDTO(faceDownCards=False, faceUpCards=cardsArray)
                buildingTowerArray.append(buildingTower)

        else:
            print("RESULTS for: " + str(i))
            print("NO contours aka no cards biutch")
            #print(cards[cards_found].best_rank_match, cards[cards_found].best_suit_match)
            #print(cards[cards_found].rank_diff, cards[cards_found].suit_diff)
            #j += 2
            #cards_found += 1
            print("============================")
    # TODO: implementer basestack og currentcard funktion





    cv2.waitKey(0)
    cv2.destroyAllWindows()

main()
