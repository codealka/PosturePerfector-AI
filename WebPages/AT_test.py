import streamlit as st
import cv2


def app():

    @st.cache()
    def load_camera():
        CAMERA_FLAG = 1
        camera = cv2.VideoCapture(CAMERA_FLAG)
        return camera

    camera = load_camera()