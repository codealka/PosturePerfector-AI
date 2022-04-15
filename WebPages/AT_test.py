import streamlit as st
import cv2


def app():

    @st.cache(allow_output_mutation=True)
    def load_camera():
        CAMERA_FLAG = 0
        camera = cv2.VideoCapture(CAMERA_FLAG)
        return camera

    camera = load_camera()