import cv2
import time
import PoseModule as pm
import math

camera = 1 # camera used ( 0 = native camera , 1 = added webcam)


def Shouldertilt(y1,y2):

    PD = ((y1 - y2)/y2)*100 # percentage difference
    if PD > 5:
        return 0
    if PD < -5:
        return 1

    # 1 -> Spine curved rightwards (
    # 0 -> spine curved leftwards )

def halfwaypoint(tuple1,tuple2):
    # each tuple has 4 entries id,x,y,z

    half = [(tuple1[0]+tuple2[0])/2,
            (tuple1[1]+tuple2[1])/2,
            (tuple1[2]+tuple2[2])/2,
            (tuple1[3]+tuple2[3])/2]

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
    Chest = halfwaypoint(lmList[11],lmList[12])
    nose = lmList[0]
    NCVD =  Chest[2] - nose[2] #Nose to chest vertical distance
    NCVD_benchmark = NCVD




    return NCVD_benchmark














#main code

Benchamrk = Calibrate_picture()
cap = cv2.VideoCapture(camera)
pTime = 0  # previous time
detector = pm.poseDetector()


while True:
    success, img = cap.read()
    img = detector.findPose(img)
    lmList = detector.findPosition(img)


    cTime = time.time()  # current time
    fps = 1 / (cTime - pTime)
    pTime = cTime  # updating previous time
    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)







    # to track specific points we can look at lmlist['point index']

    #Nose
    Nose = lmList[0]

    #Chest
    Chest = halfwaypoint(lmList[11],lmList[12])



    # Nose to chest:
    VD = Chest[2] - Nose[2] #vertical distance nose to chest ( real time)
    Nose_Chest_distance = Benchamrk      # calibrated Nose to chest distance

    if VD < Nose_Chest_distance:
        angle = (math.acos(VD/Nose_Chest_distance))*180/math.pi
        cv2.putText(img,'Head forward tilt in Degrees: ' + str(int(angle)), (70, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)



    # Head Side to side tilt:
    Chest_x = Chest[1]
    Nose_x = Nose[1]
    OFF_centre_d = Nose_x - Chest_x # if d > 0 then right tilt , if d < 0 then left tilt
    angle1 = math.asin(OFF_centre_d/VD)*180/math.pi
    cv2.putText(img, 'Off centre head angle: ' + str(int(angle1)), (70, 200), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)


    # shoulders tilt:
    y1 = lmList[11][2] #left shoulder y position
    y2 = lmList[12][2] #right shoulder y position
    ST = Shouldertilt(y1,y2)

    if ST == 0:
        cv2.putText(img, 'Spine Curved Leftwards' , (70, 150), cv2.FONT_HERSHEY_PLAIN, 3,(0, 255, 0), 3)
    elif ST == 1:
        cv2.putText(img, 'Spine Curved Rightwards', (70, 150), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)











    cv2.imshow('Image', img)
    cv2.waitKey(1)  # 1ms delay