import streamlit as st
import streamlit_option_menu as OM
from WebPages import AT_page, Thesis_Page,GoodPosture_page,ML_Page, AT_test


with st.sidebar:
    selected = OM.option_menu(
        menu_title = '',
        options = ['Home','AT Posture Correction','Good Posture','ML','Thesis','AT_test'],
        icons = ['house-fill','play-circle-fill','activity','cpu-fill','file-earmark-text-fill','play-circle-fill'],
        menu_icon = 'menu-button-wide-fill',
        default_index = 0
    )

if selected == 'Home':
        st.title('Overview')

        st.write("<web app still in progress>")

if selected == 'AT Posture Correction':
    AT_page.app()
if selected == 'Good Posture':
    GoodPosture_page.app()
if selected == 'ML':
    ML_Page.app()
if selected == 'Thesis':
    Thesis_Page.app()
if selected == 'AT_test':
    AT_test.app()
