import sys
import os
import tempfile

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from services.document_formatter import format_docx, format_pdf

import streamlit as st
import requests
import os

from dotenv import load_dotenv


# =========================================================
# CONFIGURATION
# =========================================================

load_dotenv()

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)


# =========================================================
# CUSTOM WEBSITE STYLE
# =========================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background-color: #f5f7fb;
    }

    /* Main content width */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* Main title */
    .main-title {
        font-size: 42px;
        font-weight: 700;
        color: #172554;
        margin-bottom: 20px;
        margin-top: 30px;
    }

    /* Subtitle */
    .subtitle {
        font-size: 17px;
        color: #64748b;
        margin-top: 5px;
        margin-bottom: 30px;
    }

    /* Section heading */
    .section-title {
        font-size: 23px;
        font-weight: 650;
        color: #1e293b;
        margin-top: 25px;
        margin-bottom: 12px;
    }

    /* Input labels */
    label {
        color: #334155 !important;
        font-weight: 600 !important;
    }

    /* Text areas and select boxes */
    div[data-baseweb="select"] > div,
    textarea,
    input {
        border-radius: 10px !important;
    }

    /* Generate button */
    div.stButton > button {
        width: 100%;
        height: 48px;
        border-radius: 10px;
        background-color: #2563eb;
        color: white;
        font-size: 16px;
        font-weight: 600;
        border: none;
        transition: 0.2s;
    }

    div.stButton > button:hover {
        background-color: #1d4ed8;
        color: white;
    }

    /* Download buttons */
    div.stDownloadButton > button {
        width: 100%;
        height: 45px;
        border-radius: 9px;
        font-weight: 600;
        border: 1px solid #cbd5e1;
        background-color: white;
        color: #1e3a8a;
    }

    div.stDownloadButton > button:hover {
        border-color: #2563eb;
        color: #2563eb;
    }

    /* Success message */
    div[data-testid="stAlert"] {
        border-radius: 10px;
    }

    /* Card */
    .card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 15px rgba(15, 23, 42, 0.05);
        margin-bottom: 25px;
    }

    /* Small information text */
    .info-text {
        color: #64748b;
        font-size: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">⚖️LegalEase</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-Powered Legal Document Generator'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# DOCUMENT INPUT SECTION
# =========================================================

st.markdown(
    '<div class="card">',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">Create Your Legal Document</div>',
    unsafe_allow_html=True
)

document_type = st.selectbox(
    "Document Type",
    [
        "Employment Contract",
        "Lease Agreement",
        "Non-Disclosure Agreement"
    ]
)

parties = st.text_area(
    "Parties",
    placeholder="Enter the names/details of the parties"
)

terms = st.text_area(
    "Key Terms",
    placeholder="Enter the key terms separated by semicolons"
)

effective_date = st.date_input(
    "Effective Date"
)

st.markdown(
    '<div class="info-text">'
    'Provide the required information and let LegalEase generate your document.'
    '</div>',
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)


# =========================================================
# GENERATE BUTTON
# =========================================================

if st.button("✨ Generate Document"):

    data = {
        "document_type": document_type,
        "parties": parties,
        "terms": terms,
        "effective_date": str(effective_date)
    }

    try:

        response = requests.post(
            f"{BACKEND_URL}/generate",
            json=data
        )

        if response.status_code == 200:

            result = response.json()

            st.session_state["generated_text"] = result[
                "generated_text"
            ]

            st.success(
                "Document generated successfully!"
            )

        else:

            st.error(
                f"Error: {response.text}"
            )

    except Exception as error:

        st.error(
            f"Unable to connect to the backend: {error}"
        )


st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# DOCUMENT PREVIEW
# =========================================================

if "generated_text" in st.session_state:

    st.markdown(
        '<div class="section-title">📄 Document Preview</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    edited_text = st.text_area(
        "Edit Document",
        value=st.session_state["generated_text"],
        height=500
    )

    st.session_state["generated_text"] = edited_text

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


    # =====================================================
    # DOWNLOAD SECTION
    # =====================================================

    st.markdown(
        '<div class="section-title">⬇️ Download Document</div>',
        unsafe_allow_html=True
    )

    # TXT
    st.download_button(
        label="Download TXT",
        data=edited_text,
        file_name="legal_document.txt",
        mime="text/plain"
    )


    # DOCX
    docx_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".docx"
    )

    format_docx(
        edited_text,
        docx_file.name
    )

    with open(docx_file.name, "rb") as file:

        st.download_button(
            label="Download DOCX",
            data=file,
            file_name="legal_document.docx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            )
        )


    # PDF
    pdf_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    )

    format_pdf(
        edited_text,
        pdf_file.name
    )

    with open(pdf_file.name, "rb") as file:

        st.download_button(
            label="Download PDF",
            data=file,
            file_name="legal_document.pdf",
            mime="application/pdf"
        )


