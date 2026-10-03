"""LegalEase Streamlit user interface."""
import os

import requests
import streamlit as st
from dotenv import load_dotenv

from exports import to_docx, to_pdf, to_txt

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")

st.set_page_config(page_title="LegalEase", page_icon="⚖️", layout="wide")
st.title("⚖️ LegalEase")
st.caption("AI-assisted legal document drafting for educational use")
st.warning(
    "This tool creates a starting draft, not legal advice. AI can make mistakes. "
    "Do not enter highly confidential information. Have a qualified lawyer review "
    "the document before signing or relying on it."
)

with st.form("document_form"):
    left, right = st.columns(2)
    with left:
        document_type = st.selectbox("Document type", [
            "Non-Disclosure Agreement (NDA)",
            "Employment Agreement",
            "Residential Lease Agreement",
            "Freelance Services Agreement",
        ])
        parties = st.text_area(
            "Parties and roles",
            placeholder="Example: ABC Technologies Pvt Ltd (Employer); Priya Kumar (Employee)",
            height=110,
        )
        effective_date = st.text_input("Effective date", placeholder="DD Month YYYY")
    with right:
        jurisdiction = st.text_input("Jurisdiction", value="India")
        terms_input = st.text_area(
            "Key terms (one per line)",
            placeholder="Salary/payment details\nConfidentiality obligations\nTermination notice period",
            height=175,
        )
    submitted = st.form_submit_button("Generate document", type="primary")

if submitted:
    terms = [line.strip(" \t-•") for line in terms_input.splitlines() if line.strip(" \t-•")]
    if not parties.strip() or not effective_date.strip() or not terms:
        st.error("Enter the parties, effective date, and at least one key term.")
    else:
        payload = {
            "document_type": document_type,
            "parties": parties.strip(),
            "effective_date": effective_date.strip(),
            "jurisdiction": jurisdiction.strip() or "India",
            "terms": terms,
        }
        try:
            with st.spinner("Preparing your draft..."):
                response = requests.post(f"{BACKEND_URL}/generate", json=payload, timeout=120)
            response.raise_for_status()
            result = response.json()
            st.session_state["document_text"] = result["document_text"]
            st.session_state["generator"] = result["generator"]
        except requests.RequestException as exc:
            st.error(f"Could not reach the backend at {BACKEND_URL}. Start the API server and retry. Details: {exc}")

if st.session_state.get("document_text"):
    st.subheader("Editable preview")
    st.caption(f"Generated using: {st.session_state.get('generator', 'unknown')}")
    edited_text = st.text_area(
        "Review and edit the draft before downloading",
        value=st.session_state["document_text"],
        height=480,
        key="editable_document",
    )
    st.download_button("Download TXT", to_txt(edited_text), "legalease_draft.txt", "text/plain")
    col_docx, col_pdf = st.columns(2)
    with col_docx:
        st.download_button(
            "Download DOCX", to_docx(edited_text), "legalease_draft.docx",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
    with col_pdf:
        st.download_button("Download PDF", to_pdf(edited_text), "legalease_draft.pdf", "application/pdf")

with st.expander("About this student project"):
    st.write(
        "LegalEase demonstrates a Streamlit frontend, FastAPI REST backend, optional "
        "Gemini text generation, editable output, and TXT/DOCX/PDF export. The app does "
        "not store submitted documents. When Gemini is enabled, prompt data is sent to "
        "Google's API; use non-confidential sample data for demonstrations."
    )
