import streamlit as st
from cv_processor.page import cv_processor_page
from chatbot.page import chatbot_page
from pathlib import Path
from dotenv import load_dotenv
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Custom CSS
def add_custom_css():
    st.markdown(
        """
        <style>
        .stApp {
            font-family: 'Arial', sans-serif;
            background-color: #f4f5f7;
        }
        .header {
            font-size: 2em;
            margin-bottom: 20px;
        }
        .stButton>button {
            font-size: 1.2em;
            padding: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar():
    st.sidebar.title("Talent Acquisition Hub")
    st.sidebar.markdown("---")
    page = st.sidebar.radio(
        "Navigate",
        ["Upload Resumes", "Chat with the Assistant"],
        index=0
    )
    return page

# Main App Logic
def main():
    if "files_parsed" not in st.session_state:
        st.session_state["files_parsed"] = False

    add_custom_css()

    page = render_sidebar()

    if page == "Upload Resumes":
        cv_processor_page()
    elif page == "Chat with the Assistant":
        chatbot_page()

if __name__ == "__main__":
    main()
