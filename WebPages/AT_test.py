import streamlit as st
import cv2


def app():

    @st.cache(allow_output_mutation=True)
    def load_camera():

        CAMERA_FLAG = 1
        camera = cv2.VideoCapture(CAMERA_FLAG)

        return camera



    FRAME_WINDOW = st.image([])
    cap = load_camera()
    while True:
        _, img = cap.read()
        st.write('img')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        FRAME_WINDOW.image(img)
