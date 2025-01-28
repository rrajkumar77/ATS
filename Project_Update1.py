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
    model = genai.GenerativeModel('gemini-pro')
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

st.set_page_config(page_title="Resume Expert")

st.header("JobFit Analyzer")
st.subheader('This Application helps you to evaluate the Resume Review with the Job Description')
input_text = st.text_input("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your Resume (PDF, DOCX, or TXT)...", type=["pdf", "docx", "txt"])
doc_content = ""

if uploaded_file is not None:
    st.write("Document Uploaded Successfully")

submit1 = st.button("Consultant Project Update")

input_prompt1 = """
Based on the transcript uploaded, Please provide a comprehensive project update in a clear and concise format. 
The update should include the following details if available in a table format:
    1. Employee Name 
    2. Project Details
        a. Project Name
        b. Project Description
        c. Team details
    3. Project Problem Statement
    4. Resolution Strategy and Utilized Tools/Techniques
    5. Outcome and Value Adds
Sequence by high value to the organization.
"""

if submit1:
    if uploaded_file is not None:
        doc_content = input_doc_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, doc_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a document to proceed.")
