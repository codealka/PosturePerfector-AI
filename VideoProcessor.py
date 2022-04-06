import streamlit as st
import cv2
import av
from streamlit_webrtc import webrtc_streamer
import time
import PoseModule as pm
import math

detector = pm.poseDetector()

class VideoProcessor:
    def recv(self, frame): # what user sees
        self.img = frame.to_ndarray(format='bgr24')
        self.img = detector.findPose(self.img)

        return av.VideoFrame.from_ndarray(self.img, format('bgr24'))

    def Analysis(self,img):
        lmList = detector.findPosition(self.img)

        return lmList

webrtc_streamer(key='key', video_processor_factory=VideoProcessor)
