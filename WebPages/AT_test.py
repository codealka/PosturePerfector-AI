import streamlit as st
import cv2


def app():

    @st.cache(allow_output_mutation=True)
    def load_camera():

        CAMERA_FLAG = 1
        camera = cv2.VideoCapture(CAMERA_FLAG)

        return camera

    FRAME_WINDOW = st.image([])
    while True:
        cap = load_camera()
        _, img = cap.read()

        FRAME_WINDOW.image(img)
