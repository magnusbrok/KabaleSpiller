import cv2
import pytesseract

# Installed location of Tesseract-OCR in my system
pytesseract.pytesseract.tesseract_cmd = '/usr/local/Cellar/tesseract/4.1.1/bin/tesseract'

# read image
img = cv2.imread('Training-Imgs/Text1.png')

# pytesseract only accepts RGB values, so we convert from openCV BGR to RGB
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Print text from image
print(pytesseract.image_to_string(img))

# Print bounding-boxes of each character
# print(pytesseract.image_to_boxes(img))

### Detecting characters
# Define information of size and images (h = height, w = width)
hImg, wImg,_ = img.shape

# Store all information in a list "boxes"
boxes = pytesseract.image_to_boxes(img)

for b in boxes.splitlines():

    # split each character based on the empty space between each element
    b = b.split(' ')
    print (b)

    # x = index[1] in list of boxes, y = index[2] etc.
    x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])

    # create rectangle with color red
    cv2.rectangle(img, (x, hImg-y), (w, hImg-h), (0, 0, 255), 3)

    # put text of image underneath box
    cv2.putText(img, b[0], (x, hImg-y + 25), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 2)

    cv2.imshow('Result', img)
    cv2.waitKey(0)