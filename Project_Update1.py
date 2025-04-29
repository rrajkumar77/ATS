import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
import docx
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, doc_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, doc_content, prompt])
    return response.text

def input_doc_setup(uploaded_file):
    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            # Read the PDF file
            document = pdf.PdfFileReader(uploaded_file)
            text_parts = []
            for page_num in range(document.getNumPages()):
                page = document.getPage(page_num)
                text_parts.append(page.extract_text())
            doc_text_content = " ".join(text_parts)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            # Read the DOCX file
            document = docx.Document(uploaded_file)
            text_parts = [para.text for para in document.paragraphs]
            doc_text_content = " ".join(text_parts)
        elif uploaded_file.type == "text/plain":
            # Read the TXT file
            doc_text_content = uploaded_file.read().decode("utf-8")
        else:
            raise ValueError("Unsupported file type")
        return doc_text_content
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit App

st.set_page_config(page_title="Document Analyser")

st.header("Document Analyzer")
st.subheader('This Application helps you to Analyse any document uploaded')
uploaded_file = st.file_uploader("Upload your Document (PDF, DOCX, CSV, or TXT)...", type=["pdf", "docx", "txt", "CSV"])
doc_content = ""

if uploaded_file is not None:
    st.write("Document Uploaded Successfully")

submit1 = st.button("Consultant Project Update")

input_promp = st.text_input("Queries: Feel Free to Ask here")

submit4 = st.button("Answer My Query")

input_prompt1 = """
Based on the transcript uploaded, please provide a comprehensive project update. 
"""

if submit1:
    if uploaded_file is not None:
        doc_content = input_doc_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, doc_content, "")
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a document to proceed.")

if submit4:
    if uploaded_file is not None:
        doc_content = input_doc_setup(uploaded_file)
        response = get_gemini_response(input_promp, doc_content, "")
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a document to proceed.")
