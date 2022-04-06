import streamlit as st
import cv2
import time
import PoseModule as pm
import math




camera = 1 # camera used ( 0 = native camera , 1 = added webcam)
st.title("Posture Correction app")


#main code
Benchmark = pm.Calibrate_app(camera)
detector = pm.poseDetector()



empty = st.empty()
run = empty.checkbox('Run')
FRAME_WINDOW = st.image([])
cap = cv2.VideoCapture(camera)
pTime = 0  # previous time

while run:
        empty.empty()

        _, img = cap.read()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = detector.findPose(img)
        lmList = detector.findPosition(img)

        cTime = time.time()  # current time
        fps = 1 / (cTime - pTime)
        pTime = cTime  # updating previous time
        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        # # to track specific points we can look at lmlist['point index']
        #
        # # Nose
        # Nose = lmList[0]
        #
        # # Chest
        # Chest = pm.halfwaypoint(lmList[11], lmList[12])
        #
        # # Nose to chest:
        # VD = Chest[2] - Nose[2]  # vertical distance nose to chest ( real time)
        # Nose_Chest_distance = Benchmark  # calibrated Nose to chest distance
        #
        # if VD < Nose_Chest_distance:
        #     angle = (math.acos(VD / Nose_Chest_distance)) * 180 / math.pi
        #
        #     if angle > 20:
        #         cv2.putText(img, 'Head forward tilt in Degrees: ' + str(int(angle)), (70, 100), cv2.FONT_HERSHEY_PLAIN,
        #                     3, (0, 0, 255), 3)
        #
        # # Head Side to side tilt:
        # Chest_x = Chest[1]
        # Nose_x = Nose[1]
        # OFF_centre_d = Nose_x - Chest_x  # if d > 0 then right tilt , if d < 0 then left tilt
        # angle1 = math.asin(OFF_centre_d / VD) * 180 / math.pi
        # if abs(angle1) > 10:
        #     cv2.putText(img, 'Off centre head angle: ' + str(int(angle1)), (70, 200), cv2.FONT_HERSHEY_PLAIN, 3,
        #                 (0, 255, 0), 3)
        #
        # # shoulders tilt:
        # y1 = lmList[11][2]  # left shoulder y position
        # y2 = lmList[12][2]  # right shoulder y position
        # ST = pm.Shouldertilt(y1, y2)
        #
        # if ST == 0:
        #     cv2.putText(img, 'Spine Curved Leftwards', (70, 150), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        # elif ST == 1:
        #     cv2.putText(img, 'Spine Curved Rightwards', (70, 150), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)


        FRAME_WINDOW.image(img)

else:

    st.write('Terminated')

