import cv2
from Detection import Cards

cap = cv2.VideoCapture(1)


cv2.namedWindow("test")
#cam = cv2.VideoCapture('http://192.168.1.135:4905/video')



img_counter = 0

while True:
    ret, frame = cap.read()
    #cv2.imshow("org img" , frame)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # float
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) # float

    print_frame = frame[20:height, 650:width-650]
    save_frame = frame[20:height, 650:width-650]

    print_frame = cv2.resize(print_frame, (Cards.feed_width, Cards.feed_height))
    save_frame = cv2.resize(save_frame, (Cards.feed_width, Cards.feed_height))




    if not ret:
        print("failed to grab frame")
        break

    Cards.draw_board(print_frame)
    cv2.imshow("test", print_frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, save_frame)
        print("{} written!".format(img_name))
        img_counter += 1

cap.release()

cv2.destroyAllWindows()