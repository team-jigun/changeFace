from win10toast import ToastNotifier
from cv2 import cv2
import numpy as np
import random

text = "Found. your face!"

# Image of face to replace
overlayFace = cv2.imread('duck.png', -1)

changingFace = False

# secretCode Active whether
secretCode = 0

# random box list, weight
randomBox = []
weight = 50

# Initialization variables 
init = 0

# select Webcam
cap = cv2.VideoCapture(0)

width = 640
height = 480

toaster = ToastNotifier()
toaster.show_toast('', f'width : {width}, height : {height}', duration=10)

cap.set(3, width) # 너비 (width)
cap.set(4, height) # 높이 (height)

print('width : %d, height : %d' % (cap.get(3), cap.get(4)))

xml = 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(xml)

while(True) :
    if secretCode >= 4 :
        changingFace = True

    # cap.read() 함수는 재생되는 비디오의 한 프레임씩 읽습니다.
    # 비디오 프레임을 제대로 읽었다면 ret 값이 True가 되고, 실패하면 False가 됩니다.
    # 필요한 경우, ret 값을 체크하여 비디오 프레임을 제대로 읽었는지 확인할 수 있습니다.

    # 읽은 프레임은 frame에 할답됩니다.
    ret, frame = cap.read()

    # Left and right symmetry
    frame = cv2.flip(frame, 1) 

    # 예측을 하기 위해 grayscale로 조정
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 

    faces = face_cascade.detectMultiScale(gray, 1.05, 5)
    if len(faces) is not 0 :
        print(f'Number of faces detected : {str(len(faces))}')

    if len(faces) :
        for (x, y, w, h) in faces :

            z = (x + int(w / 2), y + int(h / 2))

            for ranX, ranY, ranCenX, ranCenY in randomBox :
                centerX, centerY = center

                if ranCenX == centerX and ranCenY == ranCenY :
                    randomBox.remove((ranX, ranY, ranCenX, ranCenY))

                print(f'centerX : {centerX}, centerY : {centerY} \nranCenX : {ranCenX}, ranCenY : {ranCenY}')

            # x -= int(w / 2)
            # y -= int(h / 2)
            # w *= 2
            # h *= 2

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (155, 155, 0), 2)
            

            if changingFace :    
                changeFace = cv2.resize(overlayFace, dsize=(h, w), interpolation=cv2.INTER_LINEAR)
                y1, y2 = y, y + changeFace.shape[0]
                x1, x2 = x, x + changeFace.shape[1]

                overlayAlpha = changeFace[:, :, 3] / 255.0
                imgAlpha = 1.0 - overlayAlpha

                for c in range(0, 3) :
                    frame[y1:y2, x1:x2, c] = (overlayAlpha * changeFace[:, :, c] + imgAlpha * frame[y1:y2, x1:x2, c])
            
    for x, y, t, e in randomBox :
        cv2.rectangle(frame, (x, y), (x + weight, y + weight), (255, 0, 0), -1)

    cv2.imshow("result" , frame)

    k = cv2.waitKey(30) & 0xff

    # Esc 키를 누르면 종료
    if k == 27 :
        break

    # secretCode {
    if k == 49 :
        print("test")
        if secretCode is 0 :
            secretCode = 1

    if k == 48 :
        if secretCode >= 1 :
            secretCode += 1
    # }

    # init {
    if k == ord('b') :
        if init is 0 :
            init += 1

    if k == ord('o') :
        print(init)
        if init is 1 :
            init += 1

    if k == ord('x') :
        if init is 2 :
            changingFace = False
            init = 0
            secretCode = 0
    # }

    if k == ord(' ') :
        randomNumX = random.randrange(0, width)
        randomNumY = random.randrange(0, height)

        randomBox.insert(len(randomBox), (randomNumX, randomNumY, randomNumX + int(weight / 2), randomNumY + int(weight / 2)))

    

cap.release()
cap.destroyWindow()