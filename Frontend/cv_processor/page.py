import streamlit as st
from cv_processor.api import APIClient
import os

def cv_processor_page():
    st.header("📂 Upload Resumes")
    st.write("Upload resumes in PDF format for processing.")

    # File uploader
    uploaded_files = st.file_uploader(
        "Choose PDF files (you can upload multiple files)", 
        type=["pdf"], 
        accept_multiple_files=True
    )

    if uploaded_files:
        st.info(f"{len(uploaded_files)} file(s) selected for upload.")

        if st.button("Upload Resumes", use_container_width=True):
            with st.spinner("Uploading and processing files..."):
                API_BASE_URL = f"{os.getenv('BACKEND_URL')}/retriever"
                api_client = APIClient(api_base_url=API_BASE_URL)

                response = api_client.upload_pdfs(uploaded_files)

            if response["success"]:
                st.session_state.files_parsed = True
                st.session_state.collection_name = response["data"]["collection_name"]  # Store collection name
                st.success("Files processed successfully. You can now chat with the assistant.")
            else:
                st.error(response["error"])
                if "details" in response:
                    st.text(response["details"])
