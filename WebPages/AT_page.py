import streamlit as st
import cv2
import time
import PoseModule as pm
import math
from playsound import playsound
import matplotlib.pyplot as plt
import numpy as np

sounds = 'Sounds/DataScanner.wav'

def app():

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
    slouching = []





    st.subheader("Run the posture imaging system")
    duration = 0

    choice = st.empty()
    duration = choice.selectbox(
         'Run duration (minutes)',
         ('1','5','15','30'))
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


            if lmList == False: # can not detect position

                Nose_Chest_angle.append(60)
                Nose_Chest_angle.append(-30)

                OFF_centre_angle.append(50)
                OFF_centre_angle.append(-50)

                Spine_curvature.append(1)
                Spine_curvature.append(-1)

                slouching.append(1)
                slouching.append(0)

                col1, col2, col3, col4 = statbox.columns(4)
                col1.metric("Slouching", 'N/A')
                col2.metric('Head angle' , 'N/A')
                col3.metric('Neck Sideways Tilt', 'N/A')
                col4.metric('Spinal Curvature', 'N/A')



            else:


                # to track specific points we can look at lmlist['point index']

                #Slouching

                ShoulderWidth = Benchmark[1]
                ShoulderWidth_RT = lmList[12][1]-lmList[11][1]

                percent_increase = ((ShoulderWidth_RT-ShoulderWidth)/ShoulderWidth)*100

                if percent_increase > 5:
                    slouching.append(1)
                    col1, col2, col3, col4 = statbox.columns(4)
                    col1.metric("Slouching", 'Yes')
                    playsound(sounds)
                else:
                    slouching.append(0)
                    col1, col2, col3, col4 = statbox.columns(4)
                    col1.metric("Slouching", 'No')







                # Nose
                Nose = lmList[0]

                # Chest
                Chest = pm.halfwaypoint(lmList[11], lmList[12])

                # Nose to chest:
                VD = Chest[2] - Nose[2]  # vertical distance nose to chest ( real time)
                Nose_Chest_distance = Benchmark[0]  # calibrated Nose to chest distance

                Cutoff_forward = 60
                Cutoff_backward = -30

                if VD <= Nose_Chest_distance:
                    angle = (math.acos(VD / Nose_Chest_distance)) * 180 / math.pi
                    if angle > 30:
                        playsound(sounds)
                    if angle > Cutoff_forward:
                        Nose_Chest_angle.append(Cutoff_forward)
                        col1, col2, col3, col4 = statbox.columns(4)
                        col2.metric("Head angle", str(Cutoff_forward) + '°' + ':MAX')
                    else:
                        col1, col2, col3, col4 = statbox.columns(4)
                        Nose_Chest_angle.append(angle)
                        col2.metric("Head angle", str(int(angle)) + '°')

                else:
                    angle = -((math.acos(Nose_Chest_distance / VD)) * 180 / math.pi)
                    col1, col2, col3, col4 = statbox.columns(4)
                    col2.metric("Head angle", str(int(angle)) + '°')

                    if angle < -15:
                        playsound(sounds)

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

                if abs(angle1) > 10:
                    playsound(sounds)

                # shoulders tilt:
                y1 = lmList[11][2]  # left shoulder y position
                y2 = lmList[12][2]  # right shoulder y position
                ST = pm.Shouldertilt(y1, y2)
                Spine_curvature.append(ST)

                if ST == -1:
                    col1, col2, col3, col4 = statbox.columns(4)
                    col4.metric("Spinal Curvature", "L" )
                    playsound(sounds)
                elif ST == 1:
                    col1, col2, col3, col4 = statbox.columns(4)
                    col4.metric("Spinal Curvature", "R")
                    playsound(sounds)
                else:
                    col1, col2, col3, col4 = statbox.columns(4)
                    col4.metric("Spinal Curvature", "N")

            FRAME_WINDOW.image(img)
    else:

        tick_spacing = 30 # every 30 seconds

        # not to get divison error
        length = 60 # number of samples
        samplingRate = 1  # duration in seconds
        ticks = np.arange(0, length, tick_spacing * int(samplingRate))

        if len(Nose_Chest_angle)>0:

            length = len(Nose_Chest_angle) # number of samples
            samplingRate = length/duration # duration in seconds
            ticks = np.arange(0, length, tick_spacing*int(samplingRate))

            seconds = [0]

            for i in range(int(duration/tick_spacing)):
                seconds.append((i+1)*tick_spacing)

            print (len(ticks),len(seconds))

            fig1 = plt.figure()
            plt.title('Neck Forward Angle')
            plt.plot(Nose_Chest_angle, color = 'b')
            plt.xticks( ticks , seconds)
            plt.xlim(xmin=0)
            plt.axhline(y=15, color='g', linestyle='-',label='Upper Threshold')
            plt.axhline(y=-15, color='y', linestyle='-',label='Lower Threshold')
            plt.legend(['Real-time Angle', "Upper Limit", "Lower Limit"], loc="lower right")
            plt.xlabel('Time(s)')
            plt.ylabel('Head Angle (degrees)')
            st.pyplot(fig1)

            #neck off centre angle
            fig2 = plt.figure()
            plt.title('Head Off-Centre Angle')
            plt.plot(OFF_centre_angle, color = 'b')
            plt.xticks( ticks , seconds)
            plt.xlim(xmin=0)
            plt.axhline(y=10, color='g', linestyle='-',label='Upper Threshold')
            plt.axhline(y=-10, color='y', linestyle='-',label='Lower Threshold')
            plt.legend(['Real-time Angle',"Upper Limit", "Lower Limit"], loc="lower right")
            plt.xlabel('Time(s)')
            plt.ylabel('Neck off centre Angle (degrees)')
            st.pyplot(fig2)

            #Spine curvature
            fig3 = plt.figure()
            plt.title('Spinal Curvature')
            plt.plot(Spine_curvature, color = 'b')
            plt.xticks( ticks , seconds)
            plt.yticks([-1,0,1],['L','N','R'])
            plt.xlim(xmin=0)
            plt.xlabel('Time(s)')
            plt.ylabel('Spine curvature direction')
            st.pyplot(fig3)

            fig4 = plt.figure()
            plt.title('Slouching')
            plt.plot(Spine_curvature, color='b')
            plt.xticks(ticks, seconds)
            plt.yticks([0, 1], ['NO','YES'])
            plt.xlim(xmin=0)
            plt.xlabel('Time(s)')
            plt.ylabel('Slouching')
            st.pyplot(fig4)


