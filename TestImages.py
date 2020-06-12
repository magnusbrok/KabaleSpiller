import cv2
import imutils
from Detection import Cards


# Used for checking image processing and find countours works on different card setups pr 17/04 everything works as
# intented
def main():
    card_location = 'Training-Imgs/'

    test_images = [card_location + "kabale_1.jpg", card_location + "kabale_2.jpg", card_location + "kabale_3.jpg",
                   card_location + "1_card.jpg", card_location + "2_card.jpg", card_location + "3_card.jpg",
                   card_location + "4_card.jpg", card_location + "2_stacked.jpg"]

    for path in test_images:

        print_img = cv2.imread(path)
        print_frame = imutils.resize(print_img, 640, 640)

        image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        frame = imutils.resize(image, 640, 640)

        # Standard prerpoccesing of input
        dilate = Cards.preprocces_image(frame)

        contours, hierarchy = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        temp_contours = []

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if 30000 >= area >= 1200:
                temp_contours.append(cnt)

        cv2.drawContours(print_frame, temp_contours, -1, (0, 255, 0), 3)

        cv2.imshow(path, print_frame)

        print(path + " number of contours %d -> " % len(temp_contours))

    cv2.waitKey(0)
    cv2.destroyAllWindows()

main()
