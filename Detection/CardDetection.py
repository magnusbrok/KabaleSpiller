import cv2

from Detection import Cards


def main():

    cap = cv2.VideoCapture(1)
    #cap = cv2.VideoCapture('http://192.168.1.135:4905/video')

    while True:
        ret, frame = cap.read()

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # float
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float

        print_frame = frame[20:height, 650:width - 650]
        save_frame = frame[20:height, 650:width - 650]

        print_frame = cv2.resize(print_frame, (Cards.feed_width, Cards.feed_hight))
        save_frame = cv2.resize(save_frame, (Cards.feed_width, Cards.feed_hight))

        cv2.imshow("print frame", print_frame)

        gray = cv2.cvtColor(print_frame, cv2.COLOR_BGR2GRAY)


        dilate = Cards.preprocces_image(print_frame)

        contours, hierarchy = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cv2.imshow('Dialated', dilate)

        #pre_proc = Cards.preprocess_image(frame)

        Cards.draw_board(print_frame)



        # Draw all contours
        temp_contours = []

        for cnt in contours:
            area = cv2.contourArea(cnt)
            #print(cv2.contourArea(cnt))
            if area >= 750:
                temp_contours.append(cnt)

        cv2.drawContours(print_frame, temp_contours, -1, (0, 255, 0), 3)

        cv2.imshow('Contours', print_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


main()
