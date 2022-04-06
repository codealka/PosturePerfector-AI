import streamlit as st
import cv2
import av
from streamlit_webrtc import webrtc_streamer
import time
import PoseModule as pm
import math

camera = 1 # camera used ( 0 = native camera , 1 = added webcam)










st.title("Posture Correction app")







#main code
detector = pm.poseDetector()



run = st.checkbox('Run')
FRAME_WINDOW = st.image([])
cap = cv2.VideoCapture(camera)
pTime = 0  # previous time

while run:

        _, img = cap.read()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        img = detector.findPose(img)
        lmList = detector.findPosition(img)
        FRAME_WINDOW.image(img)


        cTime = time.time()  # current time
        fps = int( 1 / (cTime - pTime) )
        pTime = cTime  # updating previous tim

else:

    st.write('Terminated')
