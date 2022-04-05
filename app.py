import streamlit as st
import cv2
import av
from streamlit_webrtc import webrtc_streamer
import time
import PoseModule as pm
import math

camera = 1 # camera used ( 0 = native camera , 1 = added webcam)
st.title("Posture Correction app")
st.write("Hello , World")










#main code
detector = pm.poseDetector()
pTime = 0  # previous time


class VideoProcessor:

    #the main function
    def recv(self, frame):

        img = frame.to_ndarray(format="bgr24")
        img = detector.findPose(img)
        lmList = detector.findPosition(img)

        return av.VideoFrame.from_ndarray(img, format="bgr24")














webrtc_streamer(key="example", video_processor_factory=VideoProcessor)