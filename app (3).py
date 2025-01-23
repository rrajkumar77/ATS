import streamlit as st
import google.generativeai as genai
import os
import fitz  # PyMuPDF
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the Google API key from environment variables
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("Google API Key not found. Please make sure it is set in the environment.")
else:
    genai.configure(api_key=api_key)

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro')
    try:
        response = model.generate_content([input, pdf_content, prompt])
        return response.text
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return ""

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Read the PDF file
        document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        # Initialize a list to hold the text of each page
        text_parts = []

        # Iterate over the pages of the PDF to extract the text
        for page in document:
            text_parts.append(page.get_text())

        # Concatenate the list into a single string with a space in between each part
        pdf_text_content = " ".join(text_parts)
        return pdf_text_content
    else:
        st.error("No file uploaded!")
        return None

## Streamlit App
st.set_page_config(page_title="Resume Expert")

st.header("JobFit Analyzer")
st.subheader('This Application helps you in your Resume Review with help of GEMINI AI [LLM]')
input_text = st.text_input("Job Description: ", key="input")
uploaded_file = st
