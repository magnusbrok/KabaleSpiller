############## Playing Card Detector Functions ###############
#
# Original Author: Evan Juras
# Date: 9/5/17
# Edited by Magnus Brok and Anders Brandt 26/06/20
# Description: Functions and classes for CardDetection.py that perform
# various steps of the card detection algorithm
#


# Import necessary packages
import json
import imutils
import numpy as np
import cv2
from Socket.Client_socket import Socket
from DTO.SolitaireDTO import SolitaireEncoder
### Constants ###

# Videofeed dimensions
feed_width = 1600
feed_height = 1200
# constants used for defining sections of the gameboard
top_section_h = int(feed_height * 0.175)
top_section_c_w = int(feed_width / 6)
bot_section_h = feed_height
bot_section_c_w = int(feed_width / 7)

# Adaptive threshold levels
BKG_THRESH = 60
CARD_THRESH = 30

# Width and height of card corner, where rank and suit are
CORNER_WIDTH = 55
CORNER_HEIGHT = 140

# rank dimension
rank_y_offset = 20
rank_y_endpoint = 250
rank_x_offset = 0
rank_x_endpoint = 190

# suit dimensions
suit_y_offset = rank_y_endpoint + 1
suit_y_endpoint = 600
suit_x_offset = 0
suit_x_endpoint = rank_x_endpoint

# Dimensions of rank train images
RANK_WIDTH = 70
RANK_HEIGHT = 125

# Dimensions of suit train images
SUIT_WIDTH = 70
SUIT_HEIGHT = 100

RANK_DIFF_MAX = 2500
SUIT_DIFF_MAX = 2400

CARD_MAX_AREA = 120000
CARD_MIN_AREA = 25000

font = cv2.FONT_HERSHEY_SIMPLEX

def preprocces_image(image):
    # cv2.imshow('Card class recieved image', image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # cv2.imshow("image", image)
    image = gray
    blur = cv2.GaussianBlur(image, (5, 5), 0)
    # cv2.imshow("blur", blur)

    edges = cv2.Canny(blur, 120, 200)
    # cv2.imshow("edges", edges)

    kernel = np.ones((2, 2), np.uint8)
    dilate = cv2.dilate(edges, kernel, iterations=2)
    # cv2.imshow("dilate", dilate)

    return dilate


### Structures to hold query card and train card information ###
# Author: Evan Juras
class Query_card:
    """Structure to store information about query cards in the camera image."""

    def __init__(self):
        self.contour = []  # Contour of card
        self.rank_contour = []
        self.suit_contour = []
        self.width, self.height = 0, 0  # Width and height of card
        self.corner_pts = []  # Corner points of card
        self.center = []  # Center point of card
        self.warp = []  # 200x300, flattened, grayed, blurred image
        self.rank_img = []  # Thresholded, sized image of card's rank
        self.suit_img = []  # Thresholded, sized image of card's suit
        self.best_rank_match = "U"  # Best matched rank
        self.best_suit_match = "U"  # Best matched suit
        self.rank_diff = 0  # Difference between rank image and best matched train rank image
        self.suit_diff = 0  # Difference between suit image and best matched train suit image

# Author: Evan Juras
class Train_ranks:
    """Structure to store information about train rank images."""

    def __init__(self):
        self.img = []  # Thresholded, sized rank image loaded from hard drive
        self.name = "Placeholder"

# Author: Evan Juras
class Train_suits:
    """Structure to store information about train suit images."""

    def __init__(self):
        self.img = []  # Thresholded, sized suit image loaded from hard drive
        self.name = "Placeholder"


### Functions ###
# Author: Evan Juras
def load_ranks(filepath):
    """Loads rank images from directory specified by filepath. Stores
    them in a list of Train_ranks objects."""

    train_ranks = []
    newranks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    i = 0

    for Rank in ['Ace', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
                 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King']:
        train_ranks.append(Train_ranks())
        train_ranks[i].name = newranks[i]
        filename = Rank + '.jpg'
        train_ranks[i].img = cv2.imread(filepath + filename, cv2.IMREAD_GRAYSCALE)
        i = i + 1

    return train_ranks

# Author: Evan Juras
def load_suits(filepath):
    """Loads suit images from directory specified by filepath. Stores
    them in a list of Train_suits objects."""

    train_suits = []
    i = 0

    for Suit in ['S', 'D', 'C', 'H']:
        train_suits.append(Train_suits())
        train_suits[i].name = Suit
        filename = Suit + '.jpg'
        train_suits[i].img = cv2.imread(filepath + filename, cv2.IMREAD_GRAYSCALE)
        i = i + 1

    return train_suits

# Author: Evan Juras
def preprocess_imageOLD(image):
    """Returns a grayed, blurred, and adaptively thresholded camera image."""

    # gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    gray = image
    blur = cv2.GaussianBlur(gray, (9, 9), 0)

    # The best threshold level depends on the ambient lighting conditions.
    # For bright lighting, a high threshold must be used to isolate the cards
    # from the background. For dim lighting, a low threshold must be used.
    # To make the card detector independent of lighting conditions, the
    # following adaptive threshold method is used.
    #
    # A background pixel in the center top of the image is sampled to determine
    # its intensity. The adaptive threshold is set at 50 (THRESH_ADDER) higher
    # than that. This allows the threshold to adapt to the lighting conditions.
    img_w, img_h = np.shape(image)[:2]
    bkg_level = gray[int(img_h / 100)][int(img_w / 2)]
    thresh_level = bkg_level + BKG_THRESH

    retval, thresh = cv2.threshold(blur, 160, 255, cv2.THRESH_BINARY)
    #thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                            #   cv2.THRESH_BINARY, 11, 2)

    return thresh
# Author: Evan Juras
def preprocess_card(contour, image):
    """Uses contour to find information about the query card. Isolates rank
    and suit images from the card."""

    # Initialize new Query_card object
    qCard = Query_card()

    qCard.contour = contour

    #cv2.imshow("recieved img", image)

    # Find perimeter of card and use it to approximate corner points
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.01 * peri, True)
    pts = np.float32(approx)
    qCard.corner_pts = pts

    # Find width and height of card's bounding rectangle
    x, y, w, h = cv2.boundingRect(contour)
    qCard.width, qCard.height = w, h

    # Find center point of card by taking x and y average of the four corners.
    average = np.sum(pts, axis=0) / len(pts)
    cent_x = int(average[0][0])
    cent_y = int(average[0][1])
    qCard.center = [cent_x, cent_y]

    try:
        # Warp card into 200x300 flattened image using perspective transform
        qCard.warp = flattener(image, pts, w, h)
        #cv2.imshow("r_warp", qCard.warp)
    except:
        return qCard
    # Grab corner of warped card image and do a 4x zoom
    Qcorner = qCard.warp[0:CORNER_HEIGHT, 0:CORNER_WIDTH]
    Qcorner_zoom = cv2.resize(Qcorner, (0, 0), fx=4, fy=4)

    # Sample known white pixel intensity to determine good threshold level
    white_level = Qcorner_zoom[15, int((CORNER_WIDTH * 4) / 2)]
    thresh_level = white_level - CARD_THRESH
    if (thresh_level <= 0):
        thresh_level = 1
    retval, query_thresh = cv2.threshold(Qcorner_zoom, thresh_level, 255, cv2.THRESH_BINARY_INV)

    # Split in to top and bottom half (top shows rank, bottom shows suit)
    Qrank = query_thresh[rank_y_offset:rank_y_endpoint, rank_x_offset:rank_x_endpoint]
    #cv2.imshow("Qrank", Qrank)
    Qsuit = query_thresh[suit_y_offset:suit_y_endpoint, suit_x_offset:suit_x_endpoint]
    #cv2.imshow("QSuit", Qsuit)

    # Find rank contour and bounding rectangle, isolate and find largest contour
    Qrank_cnts, hier = cv2.findContours(Qrank, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    Qrank_cnts = sorted(Qrank_cnts, key=cv2.contourArea, reverse=True)

    # Find bounding rectangle for largest contour, use it to resize query rank
    # image to match dimensions of the train rank image
    if len(Qrank_cnts) != 0:
        x1, y1, w1, h1 = cv2.boundingRect(Qrank_cnts[0])
        Qrank_roi = Qrank[y1:y1 + h1, x1:x1 + w1]
        Qrank_sized = cv2.resize(Qrank_roi, (RANK_WIDTH, RANK_HEIGHT), 0, 0)
        qCard.rank_img = Qrank_sized
        #cv2.imshow("rankfound", Qrank_sized)

    # Find suit contour and bounding rectangle, isolate and find largest contour
    Qsuit_cnts, hier = cv2.findContours(Qsuit, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    Qsuit_cnts = sorted(Qsuit_cnts, key=cv2.contourArea, reverse=True)

    # Find bounding rectangle for largest contour, use it to resize query suit
    # image to match dimensions of the train suit image
    if len(Qsuit_cnts) != 0:
        x2, y2, w2, h2 = cv2.boundingRect(Qsuit_cnts[0])
        Qsuit_roi = Qsuit[y2:y2 + h2, x2:x2 + w2]
        Qsuit_sized = cv2.resize(Qsuit_roi, (SUIT_WIDTH, SUIT_HEIGHT), 0, 0)
        qCard.suit_img = Qsuit_sized
        #cv2.imshow("suitfound", Qsuit_sized)

    return qCard

# Author: Evan Juras
def match_card(qCard, train_ranks, train_suits):
    """Finds best rank and suit matches for the query card. Differences
    the query card rank and suit images with the train rank and suit images.
    The best match is the rank or suit image that has the least difference."""

    best_rank_match_diff = 10000
    best_suit_match_diff = 10000
    best_rank_match_name = "U"
    best_suit_match_name = "U"
    i = 0

    # If no contours were found in query card in preprocess_card function,
    # the img size is zero, so skip the differencing process
    # (card will be left as Unknown)
    if (len(qCard.rank_img) != 0) and (len(qCard.suit_img) != 0):

        # Difference the query card rank image from each of the train rank images,
        # and store the result with the least difference
        for Trank in train_ranks:

            diff_img = cv2.absdiff(qCard.rank_img, Trank.img)
            rank_diff = int(np.sum(diff_img) / 255)

            if rank_diff < best_rank_match_diff:
                best_rank_diff_img = diff_img
                best_rank_match_diff = rank_diff
                best_rank_name = Trank.name

        # Same process with suit images
        for Tsuit in train_suits:

            diff_img = cv2.absdiff(qCard.suit_img, Tsuit.img)
            suit_diff = int(np.sum(diff_img) / 255)

            if suit_diff < best_suit_match_diff:
                best_suit_diff_img = diff_img
                best_suit_match_diff = suit_diff
                best_suit_name = Tsuit.name

    # Combine best rank match and best suit match to get query card's identity.
    # If the best matches have too high of a difference value, card identity
    # is still Unknown
    if (best_rank_match_diff < RANK_DIFF_MAX):
        best_rank_match_name = best_rank_name

    if (best_suit_match_diff < SUIT_DIFF_MAX):
        best_suit_match_name = best_suit_name

    # Return the identiy of the card and the quality of the suit and rank match
    return best_rank_match_name, best_suit_match_name, best_rank_match_diff, best_suit_match_diff

# Author: Evan Juras
def flattener(image, pts, w, h):
    """Flattens an image of a card into a top-down 200x300 perspective.
    Returns the flattened, re-sized, grayed image.
    See www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/"""
    temp_rect = np.zeros((4, 2), dtype="float32")

    s = np.sum(pts, axis=2)

    tl = pts[np.argmin(s)]
    br = pts[np.argmax(s)]

    diff = np.diff(pts, axis=-1)
    tr = pts[np.argmin(diff)]
    bl = pts[np.argmax(diff)]

    # Need to create an array listing points in order of
    # [top left, top right, bottom right, bottom left]
    # before doing the perspective transform

    if w <= 0.8 * h:  # If card is vertically oriented
        temp_rect[0] = tl
        temp_rect[1] = tr
        temp_rect[2] = br
        temp_rect[3] = bl

    if w >= 1.2 * h:  # If card is horizontally oriented
        temp_rect[0] = bl
        temp_rect[1] = tl
        temp_rect[2] = tr
        temp_rect[3] = br

    # If the card is 'diamond' oriented, a different algorithm
    # has to be used to identify which point is top left, top right
    # bottom left, and bottom right.

    if w > 0.8 * h and w < 1.2 * h:  # If card is diamond oriented
        # If furthest left point is higher than furthest right point,
        # card is tilted to the left.
        if pts[1][0][1] <= pts[3][0][1]:
            # If card is titled to the left, approxPolyDP returns points
            # in this order: top right, top left, bottom left, bottom right
            temp_rect[0] = pts[1][0]  # Top left
            temp_rect[1] = pts[0][0]  # Top right
            temp_rect[2] = pts[3][0]  # Bottom right
            temp_rect[3] = pts[2][0]  # Bottom left

        # If furthest left point is lower than furthest right point,
        # card is tilted to the right
        if pts[1][0][1] > pts[3][0][1]:
            # If card is titled to the right, approxPolyDP returns points
            # in this order: top left, bottom left, bottom right, top right
            temp_rect[0] = pts[0][0]  # Top left
            temp_rect[1] = pts[3][0]  # Top right
            temp_rect[2] = pts[2][0]  # Bottom right
            temp_rect[3] = pts[1][0]  # Bottom left

    maxWidth = 200
    maxHeight = 300

    # Create destination array, calculate perspective transform matrix,
    # and warp card image
    dst = np.array([[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]], np.float32)
    M = cv2.getPerspectiveTransform(temp_rect, dst)
    warp = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    # warp = cv2.cvtColor(warp,cv2.COLOR_BGR2GRAY)

    return warp
# Author: Magnus Brok
def draw_board(frame):
    # Top of the board
    cv2.line(frame, (0, top_section_h), (feed_width, top_section_h), (255, 0, 0), 3)

    # The 6 sections of top board
    for x in range(1, 6):
        cv2.line(frame, (top_section_c_w * x, 0), (top_section_c_w * x, top_section_h), (255, 0, 0), 3)
    # The bottom 7 cardstacks
    for x in range(1, 8):
        cv2.line(frame, (bot_section_c_w * x, top_section_h), (bot_section_c_w * x, bot_section_h), (255, 0, 0), 3)

# Author: Magnus Brok
def cutout_board_sections(frame):
    sections = []
    section_number = 1
    for x in range(0, 6):
        image = frame[0: int(top_section_h), int(top_section_c_w) * x:int(top_section_c_w) * (x + 1)]
        sections.append(imutils.resize(image, 600, 480))

    for x in range(0, 7):
        image = frame[top_section_h:bot_section_h, bot_section_c_w * x:bot_section_c_w * (x + 1)]
        sections.append(image)

    # for i in range(0, len(sections)):
    # contours, heir = cv2.findContours(sections[i], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(sections[i], contours, 0, (255, 255, 255), 3)
    # cv2.imshow(str(i), sections[i])

    return sections

# Author: Anders Brandt
def send_game(solitaire):
    data = json.dumps(solitaire, cls=SolitaireEncoder)
    socket = Socket("localhost", 8080)
    socket.send(data)
    socket.receive()
