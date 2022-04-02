import cv2
import time
import PoseModule as pm

camera = 0 # camera used ( 0 = native camera , 1 = added webcam)

def halfwaypoint(tuple1,tuple2):
    # each tuple has 3 entries id,x,y

    half = [(tuple1[0]+tuple2[0])/2,
            (tuple1[1]+tuple2[1])/2,
            (tuple1[2]+tuple2[2])/2]

    return half


def Calibrate_picture():
    cam = cv2.VideoCapture(camera)
    cv2.namedWindow("Calibration")
    img_counter = 0

    while img_counter<1:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)

        if k % 256 == 32:
            # SPACE pressed
            img_name = "Calibrate.jpg"
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1

    cam.release()
    cv2.destroyAllWindows()





    #getting calibration data
    detector = pm.poseDetector()
    img = detector.findPose(frame)
    lmList = detector.findPosition(img)


#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
    halfShoulders = halfwaypoint(lmList[11],lmList[12])
    nose = lmList[0]
    NCVD =  halfShoulders[2] - nose[2] #Nose to chest vertical distance
    NCVD_benchmark = 0.75 *NCVD

# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------

    ShoulderWidth = lmList[11][1] - lmList[12][1]
    SW_benchmark = 1.06*ShoulderWidth
    print(ShoulderWidth)
    print(SW_benchmark)



    return NCVD_benchmark , SW_benchmark














#main code

Benchamrk = Calibrate_picture()




cap = cv2.VideoCapture(camera)
pTime = 0  # previous time
detector = pm.poseDetector()


while True:
    success, img = cap.read()
    img = detector.findPose(img)
    lmList = detector.findPosition(img)

    # to track specific points we can look at lmlist['point index']

    cTime = time.time()  # current time
    fps = 1 / (cTime - pTime)
    pTime = cTime  # updating previous time



    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    halfShoulders = halfwaypoint(lmList[11], lmList[12])
    VD = halfShoulders[2] - lmList[0][2] #vertical distance nose to chest
    ShoulderWidth = lmList[11][1] - lmList[12][1]

    if VD < Benchamrk[0]:
         cv2.putText(img, 'BAD POSTURE : neck too low', (70, 150), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
    if ShoulderWidth > Benchamrk[1]:
        cv2.putText(img, 'BAD POSTURE: Hunched over', (70, 200), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
    if (lmList[11][2] > 1.05*lmList[12][2]) or (lmList[12][2]>1.05*lmList[11][2]):
        cv2.putText(img, 'BAD POSTURE: Slanted Shoulders', (70, 250), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)

    cv2.imshow('Image', img)

    cv2.waitKey(1)  # 1ms delay


