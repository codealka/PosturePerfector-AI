import streamlit as st
import cv2


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

    vf = cv2.VideoCapture(1)

    stframe = st.empty()

    while vf.isOpened():
        ret, frame = vf.read()
        # if frame is read correctly ret is True
        if not ret:
            st.write("not")
            print("Can't receive frame (stream end?). Exiting ...")
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        stframe.image(gray)