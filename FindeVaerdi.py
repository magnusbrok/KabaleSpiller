import cv2
import imutils
import numpy as np
import os
import pytesseract
import Cards

# Installed location of Tesseract-OCR in my system
pytesseract.pytesseract.tesseract_cmd = '/usr/local/Cellar/tesseract/4.1.1/bin/tesseract'

cardPath = 'Training-Imgs/4_card.jpg'

#cardPath = 'Training-Imgs/2_card.jpg'

print_img = cv2.imread(cardPath)
print_frame = imutils.resize(print_img, 640, 640)

image = cv2.imread(cardPath, cv2.IMREAD_GRAYSCALE)
frame = imutils.resize(image, 640, 640)

#cv2.imshow('frame-grayed', frame)

# Standard preproccesing of input
dilate = Cards.preprocces_image(frame)

contours, hierarchy = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#cv2.imshow('Dialated', dilate)


temp_contours = []

for cnt in contours:
    area = cv2.contourArea(cnt)
    print(cv2.contourArea(cnt))
    if (area <= 30000 and area >= 1200):
        temp_contours.append(cnt)

        card = cnt

        # Approximate the corner points of the card
        peri = cv2.arcLength(card, True)
        approx = cv2.approxPolyDP(card, 0.01 * peri, True)
        pts = np.float32(approx)

        x, y, w, h = cv2.boundingRect(card)

        # Flatten the card and convert it to 200x300
        warp = Cards.flattener(frame, pts, w, h)

        #cv2.imshow(str(area), warp)

        # Print text from image
        print(pytesseract.image_to_string(warp))

        # Print bounding-boxes of each character
        print(pytesseract.image_to_boxes(warp))

        ### Detecting characters
        # Define information of size and images (h = height, w = width)
        hImg, wImg = warp.shape

        # Store all information in a list "boxes"
        boxes = pytesseract.image_to_boxes(warp)

        for b in boxes.splitlines():
            # split each character based on the empty space between each element
            b = b.split(' ')
            print(b)

            # x = index[1] in list of boxes, y = index[2] etc.
            x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])

            # create rectangle with color red
            cv2.rectangle(warp, (x, hImg - y), (w, hImg - h), (0, 0, 255), 3)

            # put text of image underneath box
            cv2.putText(warp, b[0], (x, hImg - y + 25), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 2)

            cv2.imshow(str(b), warp)


cv2.drawContours(print_frame, temp_contours, -1, (0, 255, 0), 3)

#cv2.imshow('Contours', print_frame)

print("number of contours %d -> "%len(temp_contours))

cv2.waitKey(0)
cv2.destroyAllWindows()