import cv2
import time
import PoseModule as pm


cap = cv2.VideoCapture(1)
pTime = 0  # previous time
detector = pm.poseDetector()

while True:
    success, img = cap.read()
    img = detector.findPose(img)
    lmList = detector.findPosition(img)
    print(lmList)

    # to track specific points we can look at lmlist['point index']

    cTime = time.time()  # current time
    fps = 1 / (cTime - pTime)
    pTime = cTime  # updating previous time

    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow('Image', img)

    cv2.waitKey(1)  # 1ms delay
