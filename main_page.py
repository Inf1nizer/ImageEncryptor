import streamlit as st
from rsa_page import show_rsa_page
from aes_page import show_aes_page
from des_page import show_des_page
from blowfish_page import show_blowfish_page

st.set_page_config(layout="wide")

# Initialize session state for page navigation
if "page" not in st.session_state:
    st.session_state.page = "main"


def navigate(page_name):
    st.session_state.page = page_name


# Display main content based on the current page
if st.session_state.page == "main":
    st.title("IMAGE ENCRYPTION APPLICATION")
    st.caption(
        "This web application is designed to offer seamless image encryption with a simple and interactive interface. Users can upload an image, and the app quickly encrypts it using advanced cryptographic algorithms. The time taken to complete the encryption is displayed in real-time, giving users insights into the process's efficiency. Once encrypted, the file is ready for secure download, ensuring complete data confidentiality. Built for speed and security, the application leverages modern encryption standards while maintaining an intuitive user experience. A perfect blend of performance and ease-of-use for anyone looking to protect their digital assets."
    )

    col1, col2, col3, col4 = st.columns(4, gap="large")

    with col1:
        st.header("RSA")
        if st.button("Go to RSA"):
            navigate("rsa")  # Navigate to RSA page

    with col2:
        st.header("DES")
        if st.button("Go to DES"):
            navigate("des")  # Navigate to DES page

    with col3:
        st.header("AES")
        if st.button("Go to AES"):
            navigate("aes")  # Navigate to AES page

    with col4:
        st.header("BF")
        if st.button("Go to Blowfish"):
            navigate("blowfish")  # Navigate to SHA page


elif st.session_state.page == "rsa":
    show_rsa_page()
elif st.session_state.page == "aes":
    show_aes_page()
elif st.session_state.page == "des":
    show_des_page()
elif st.session_state.page == "blowfish":
    show_blowfish_page()
