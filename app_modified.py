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


Nose_Chest_angle = []
OFF_centre_angle = []
Spine_curvature = []





st.subheader("Run the posture imaging system")

choice = st.empty()
duration = choice.selectbox(
     'Run duration (minutes)',
     ('1', '2','5'))
duration = 60*int(duration)
run_time = time.time() + duration


empty = st.empty()
run = empty.checkbox('Run')
FRAME_WINDOW = st.image([])
cap = cv2.VideoCapture(camera)
pTime = 0  # previous time


statbox = st.empty()
while run and time.time()<run_time:
        choice.empty()
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

        Cutoff_forward = 60
        Cutoff_backward = -30

        if VD <= Nose_Chest_distance:
            angle = (math.acos(VD / Nose_Chest_distance)) * 180 / math.pi
            col2.metric("Head angle", str(int(angle)) + '°')
            if angle > Cutoff_forward:
                Nose_Chest_angle.append(Cutoff_forward)
                col1, col2, col3, col4 = statbox.columns(4)
                col2.metric("Head angle", str(Cutoff_forward) + '°' + ':MAX')
            else:
                Nose_Chest_angle.append(angle)

        else:
            angle = -((math.acos(Nose_Chest_distance / VD)) * 180 / math.pi)
            col1, col2, col3, col4 = statbox.columns(4)
            col2.metric("Head angle", str(int(angle)) + '°')
            if angle < Cutoff_backward:
                Nose_Chest_angle.append(Cutoff_backward)
                col1, col2, col3, col4 = statbox.columns(4)
                col2.metric("Head angle", str(Cutoff_backward)+'°' + ':MAX')
            else:
                Nose_Chest_angle.append(angle)

        # Head Side to side tilt:
        Chest_x = Chest[1]
        Nose_x = Nose[1]
        OFF_centre_d = Nose_x - Chest_x  # if d > 0 then right tilt , if d < 0 then left tilt

        OFF_Centre_Cut_OFF = 50  # cut off value where the angle represnted will no longer be accurate due to awkward body position

        if abs(VD) > abs(OFF_centre_d):

            angle1 = int((math.asin(OFF_centre_d / VD) * 180 / math.pi))
            if angle1 > OFF_Centre_Cut_OFF:
                col1, col2, col3, col4 = statbox.columns(4)
                col3.metric("Neck Sideways Tilt", str(OFF_Centre_Cut_OFF)+'°' + ':MAX')
                OFF_centre_angle.append(OFF_Centre_Cut_OFF)
            elif angle1 < -OFF_Centre_Cut_OFF:
                col1, col2, col3, col4 = statbox.columns(4)
                col3.metric("Neck Sideways Tilt", str(-OFF_Centre_Cut_OFF) + '°' + ':MAX')
                OFF_centre_angle.append(-OFF_Centre_Cut_OFF)
            else:
                col1, col2, col3, col4 = statbox.columns(4)
                col3.metric("Neck Sideways Tilt", str(angle1) + '°' )
                OFF_centre_angle.append(angle1)


        # shoulders tilt:
        y1 = lmList[11][2]  # left shoulder y position
        y2 = lmList[12][2]  # right shoulder y position
        ST = pm.Shouldertilt(y1, y2)
        print(ST)
        Spine_curvature.append(ST)

        # if ST == -1:
        #     cv2.putText(img, 'Spine Curved Leftwards', (70, 150), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        # elif ST == 1:
        #     cv2.putText(img, 'Spine Curved Rightwards', (70, 150), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

        FRAME_WINDOW.image(img)



