import streamlit as st
from WebPages import AT_page , ML_Page, Thesis_Page, GoodPosture_page

def navigation():
    try:
        path = st.experimental_get_query_params()['p'][0]
    except Exception as e:
        st.error('Please use the main app.')
        return None
    return path


if navigation() == "home":
    AT_page.app()

elif navigation() == "Thesis":
    Thesis_Page.app()

elif navigation() == "ML":
    ML_Page.app()

elif navigation() == "Good Posture":
    GoodPosture_page.app()


elif navigation() == "logs":
    st.title('View all of the logs')
    st.write('Here you may view all of the logs.')


elif navigation() == "verify":
    st.title('Data verification is started...')
    st.write('Please stand by....')


elif navigation() == "config":
    st.title('Configuration of the app.')
    st.write('Here you can configure the application')
