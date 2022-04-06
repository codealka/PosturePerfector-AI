import streamlit as st
import cv2
import time
import PoseModule as pm
import math

st.title("Postural Imaging System for Back Pain Sufferers")

option = st.selectbox(
     'Video input medium',
     ('Device Native Camera', 'Additional Webcam'))

st.write('You selected:', option)

if option == 'Device Native Camera':
        camera = 0 # camera used ( 0 = native camera , 1 = added webcam)
else:
        camera = 1


#main code

st.subheader("Calibration is used to tailor the system for you")
Benchmark = pm.Calibrate_app(camera)
detector = pm.poseDetector()




st.subheader("Run the posture imaging system")
empty = st.empty()
run = empty.checkbox('Run')
FRAME_WINDOW = st.image([])
cap = cv2.VideoCapture(camera)
pTime = 0  # previous time


statbox = st.empty()
while run:
        empty.empty()
        _, img = cap.read()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = detector.findPose(img)
        lmList = detector.findPosition(img)

        cTime = time.time()  # current time
        fps = int( 1 / (cTime - pTime))
        pTime = cTime  # updating previous time

        col1, col2, col3, col4= statbox.columns(4)

        col1.metric("FPS", fps)


        # to track specific points we can look at lmlist['point index']

        # Nose
        Nose = lmList[0]

        # Chest
        Chest = pm.halfwaypoint(lmList[11], lmList[12])

        # Nose to chest:
        VD = Chest[2] - Nose[2]  # vertical distance nose to chest ( real time)
        Nose_Chest_distance = Benchmark  # calibrated Nose to chest distance

        if VD < Nose_Chest_distance:
            angle = (math.acos(VD / Nose_Chest_distance)) * 180 / math.pi
            col2.metric("Head angle", str(int(angle)) + '°')

            # if angle > 20:
            #

        else:
                col1, col2, col3 , col4 = statbox.columns(4)
                col2.metric("Head angle", 'GOOD')




        # Head Side to side tilt:
        Chest_x = Chest[1]
        Nose_x = Nose[1]
        OFF_centre_d = Nose_x - Chest_x  # if d > 0 then right tilt , if d < 0 then left tilt
        angle1 = math.asin(OFF_centre_d / VD) * 180 / math.pi

        if (angle1) > 10:
                col3.metric("Head sideways tilt", 'L'+ str(int(angle1)) + '°')
        elif (angle1) < -10:
                col3.metric("Head sideways tilt", 'R'+ str(int(abs(angle1))) + '°')
        else:
                col1, col2, col3, col4 = statbox.columns(4)
                col3.metric("Head sideways tilt", 'GOOD')

        # shoulders tilt:
        y1 = lmList[11][2]  # left shoulder y position
        y2 = lmList[12][2]  # right shoulder y position
        ST = pm.Shouldertilt(y1, y2)

        if ST == 0:
                col1, col2, col3,col4 = statbox.columns(4)
                col4.metric("Spine Curve", 'Left')
        elif ST == 1:
                col1, col2, col3, col4 = statbox.columns(4)
                col4.metric("Spine Curve", 'Right')
        else:
                col1, col2, col3, col4 = statbox.columns(4)
                col4.metric("Spine Curve", 'Centred')




        FRAME_WINDOW.image(img)




