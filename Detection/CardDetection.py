import cv2
import imutils
import os

import numpy as np
from pip._vendor.distlib.compat import raw_input

from Detection import Cards
from DTO.SolitaireDTO import SolitaireDTO
from DTO.buildingTowerDTO import BuildingTowerDTO
from DTO.cardDTO import CardDTO
from Socket import Client_socket


def main():

    # Load the train rank and suit images
    path = os.path.dirname(os.path.abspath(__file__))
    train_ranks = Cards.load_ranks(path + '/Card_Imgs/')
    train_suits = Cards.load_suits(path + '/Card_Imgs/')

    cap = cv2.VideoCapture(1)
    #cap = cv2.VideoCapture('http://192.168.1.135:4905/video')

    while True:
        while True:
            ret, frame = cap.read()

            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # float
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float

            print_frame = frame[20:height, 650:width - 650]
            save_frame = frame[20:height, 650:width - 650]

            image = cv2.resize(print_frame, (Cards.feed_width, Cards.feed_hight))
            frame = cv2.resize(save_frame, (Cards.feed_width, Cards.feed_hight))

            Cards.draw_board(frame)
            cv2.imshow("print frame", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("p"):
                break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        dilate = Cards.preprocess_imageOLD(gray)

        #cv2.imshow("dilate", dilate)

        sections = Cards.cutout_board_sections(dilate)
        print_sections = Cards.cutout_board_sections(frame)
        qcards = []
        tower_card_array = []
        buildingTowerArray = []
        base_stack_array = []
        cards_found = 0
        section_counter = 0

        for i in range(0, 13):
            section = sections[i]
            #cv2.imshow(str(i) + "section", section)
            printable_section = print_sections[i]
            contours, hierarchy = cv2.findContours(section, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

            #print(len(contours))

            if len(contours) != 0:
                cnt = contours[0]

                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.01 * peri, True)
                pts = np.float32(approx)
                corner_pts = pts

                # Find width and height of card's bounding rectangle
                x, y, w, h = cv2.boundingRect(cnt)

#                warp = Cards.flattener(printable_section, pts, w, h)

                #   cv2.imshow(str(i)+"warp", warp)

                gray_section = cv2.cvtColor(printable_section, cv2.COLOR_BGR2GRAY)
                # cv2.imshow(str(i)+ "gray", gray_section)
                qcards.append(Cards.preprocess_card(cnt, gray_section))
                # cv2.imshow("testsection", sections[testSection])

                # Find the best rank and suit match for the card.
                qcards[cards_found].best_rank_match, qcards[cards_found].best_suit_match, qcards[cards_found].rank_diff, \
                qcards[
                    cards_found].suit_diff = Cards.match_card(
                    qcards[cards_found], train_ranks, train_suits)

                cardDTO = CardDTO(value=qcards[cards_found].best_rank_match, suit=qcards[cards_found].best_suit_match)



                if i == 1:
                    currentCard = cardDTO

                if 1 < i < 6:
                    base_stack_array.append(cardDTO)

                if 5 < i:
                    tower_card_array = []
                    if cardDTO.suit != "U" and cardDTO.value != "U":
                        tower_card_array.append(cardDTO)
                    buildingTower = BuildingTowerDTO(faceDownCards=False, faceUpCards=tower_card_array)
                    buildingTowerArray.append(buildingTower)

                found_card = qcards[cards_found]
              #  print("============================")
              #  print("RESULTS for: " + str(i))
              #  print(str(found_card.best_rank_match) + str(found_card.best_suit_match))
              #  print("Rank diff: " + str(found_card.rank_diff) + " Suit Diff: " + str(found_card.suit_diff))
                #try:
                    #cv2.imshow(str(section_counter) + "rank", found_card.rank_img)
                    #cv2.imshow(str(section_counter) + "card suit", found_card.suit_img)
                #except:
                   # print("no card found")

                cards_found += 1

            if len(contours) == 0:

                if i == 1:
                    currentCard = None
                if 5 < i:
                    tower_card_array = []
                    buildingTower = BuildingTowerDTO(faceDownCards=False, faceUpCards=tower_card_array)
                    buildingTowerArray.append(buildingTower)
               # print("============================")
               # print("RESULTS for: " + str(i))
               # print("no card found")
            section_counter += 1

        solitaire = SolitaireDTO(baseStack=base_stack_array, currentCard=currentCard, towers=buildingTowerArray)
        top_row_string = "CurrCard: "
        if currentCard != None:
            top_row_string += str(currentCard.value)
            top_row_string += str(currentCard.suit)
            top_row_string += " |  "
        else:
            top_row_string += "XX"
            top_row_string += " |  "
        for i in range(0, 4):
            if len(base_stack_array) > i:
                cardDTO = base_stack_array[i]
                top_row_string += str(cardDTO.value)
                top_row_string += str(cardDTO.suit)
                top_row_string += "   "
            else:
                top_row_string += "XX"
                top_row_string += "   "

        tower_string = ""
        for tower in buildingTowerArray:
            cardDTO = CardDTO
            if len(tower.faceUpCards) > 0:
                cardDTO = tower.faceUpCards[0]
                tower_string += str(cardDTO.value)
                tower_string += str(cardDTO.suit)
                tower_string += "   "
            else:
                tower_string += "XX"
                tower_string += "   "
        print("========  RESULTS OF SCAN ========")
        print(top_row_string)
        print(tower_string)

        print()

        input_char = input("Was the scan correct? [Y/N]")
        input_char = input_char.lower()
        if input_char == "y":
            Cards.send_game(solitaire)
        if input_char == "n":
            print("Tryk p for at tage et nyt billedet")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


main()
