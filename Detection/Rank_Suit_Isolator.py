### Takes a card picture and creates a top-down 200x300 flattened image
### of it. Isolates the suit and rank and saves the isolated images.
### Runs through A - K ranks and then the 4 suits.

# Import necessary packages
import cv2
import numpy as np
from Detection import Cards
import os

img_path = os.path.dirname(os.path.abspath(__file__)) + '/Card_Imgs/'

IM_WIDTH = 1280
IM_HEIGHT = 720

RANK_WIDTH = 70
RANK_HEIGHT = 125

SUIT_WIDTH = 70
SUIT_HEIGHT = 100

cap = cv2.VideoCapture(1)
#cap = cv2.VideoCapture('http://192.168.1.135:4905/video')

# Use counter variable to switch from isolating Rank to isolating Suit
i = 1

for Name in ['Ace','Two','Three','Four','Five','Six','Seven','Eight',
             'Nine','Ten','Jack','Queen','King','Spades','Diamonds',
             'Clubs','Hearts']:

    filename = Name + '.jpg'

    print('Press "p" to take a picture of ' + filename)
    
    


# Press 'p' to take a picture
    while True:

        ret, frame = cap.read()

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # float
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float

        print_frame = frame[20:int(height/2), 650*2:width - 650*2]
        save_frame = frame[20:int(height/2), 650*2:width - 650*2]

        image = cv2.resize(print_frame, (Cards.feed_width, Cards.feed_hight))
        frame = cv2.resize(save_frame, (Cards.feed_width, Cards.feed_hight))

        cv2.imshow("Card",frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("p"):
            image = frame
            break

    # Pre-process image
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    retval, thresh = cv2.threshold(blur,100,255,cv2.THRESH_BINARY)



    # Find contours and sort them by size
    cnts,hier = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea,reverse=True)

    # Assume largest contour is the card. If there are no contours, print an error
    flag = 0
    image2 = image.copy()

    if len(cnts) == 0:
        print('No contours found!')
        quit()

    card = cnts[0]

    # Approximate the corner points of the card
    peri = cv2.arcLength(card,True)
    approx = cv2.approxPolyDP(card,0.01*peri,True)
    pts = np.float32(approx)

    x,y,w,h = cv2.boundingRect(card)

    # Flatten the card and convert it to 200x300
    warp = Cards.flattener(image, pts, w, h)
    cv2.imshow("warp", warp)

    # Grab corner of card image, zoom, and threshold
    corner = warp[0:Cards.CORNER_HEIGHT, 0:Cards.CORNER_WIDTH]
    #corner_gray = cv2.cvtColor(corner,cv2.COLOR_BGR2GRAY)
    corner_zoom = cv2.resize(corner, (0,0), fx=4, fy=4)
    gray_corner = cv2.cvtColor(corner_zoom,cv2.COLOR_BGR2GRAY)
    corner_blur = cv2.GaussianBlur(gray_corner,(5,5),0)
    retval, corner_thresh = cv2.threshold(corner_blur, 155, 255, cv2. THRESH_BINARY_INV)
    cv2.imshow("corner", corner_zoom)


    # Isolate suit or rank
    if i <= 13: # Isolate rank
        rank = corner_thresh[Cards.rank_y_offset:Cards.rank_y_endpoint,
               Cards.rank_x_offset:Cards.rank_x_endpoint]
        # Grabs portion of image that shows rank
        cv2.imshow("rank", rank)

        rank_cnts, hier = cv2.findContours(rank, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        rank_cnts = sorted(rank_cnts, key=cv2.contourArea,reverse=True)
        x,y,w,h = cv2.boundingRect(rank_cnts[0])
        rank_roi = rank[y:y+h, x:x+w]
        rank_sized = cv2.resize(rank_roi, (RANK_WIDTH, RANK_HEIGHT), 0, 0)
        final_img = rank_sized
        #cv2.imshow("fianl", final_img)

    if i > 13: # Isolate suit
        suit = corner_thresh[Cards.suit_y_offset:Cards.suit_y_endpoint,
               Cards.suit_x_offset:Cards.rank_y_endpoint] # Grabs portion of image that shows suit
        cv2.imshow("suit", suit)
       
        suit_cnts, hier = cv2.findContours(suit, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        suit_cnts = sorted(suit_cnts, key=cv2.contourArea,reverse=True)
        x,y,w,h = cv2.boundingRect(suit_cnts[0])
        suit_roi = suit[y:y+h, x:x+w]
        suit_sized = cv2.resize(suit_roi, (SUIT_WIDTH, SUIT_HEIGHT), 0, 0)
        final_img = suit_sized

    cv2.imshow("Image",final_img)

    # Save image
    print('Press "c" to continue.')
    key = cv2.waitKey(0) & 0xFF
    if key == ord('c'):
        cv2.imwrite(img_path+filename,final_img)

    i = i + 1

cv2.destroyAllWindows()
