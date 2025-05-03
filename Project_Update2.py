import streamlit as st
import google.generativeai as genai
import os
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("Google API Key not found.")
else:
    genai.configure(api_key=api_key)

# Gemini interaction
def get_project_summary(text):
    model = genai.GenerativeModel('gemini-pro')
    prompt = "Summarize this project in a professional tone with key details, achievements, and value adds:"
    try:
        response = model.generate_content([prompt, text])
        return response.text
    except Exception as e:
        return f"Error generating summary: {str(e)}"

# Styled HTML output using your brand colors
def format_summary(employee_name, lead_name, project_name, project_desc, achievements, value_add):
    return f"""
    <div style="background-color:#F5F5F5; padding: 20px; border-radius: 10px;">
        <h3 style="color:#012A52;">Employee Name: {employee_name}</h3>
        <p><strong style="color:#CDDC00;">Lead Name:</strong> {lead_name}</p>
        <p><strong style="color:#009CDE;">Project Name:</strong> {project_name}</p>
        <p><strong style="color:#00798B;">Project Description:</strong> {project_desc}</p>
        <p><strong style="color:#009CDE;">Achievements/Value Adds:</strong><br>{achievements}</p>
        <p><strong style="color:#F8971D;">Value Add:</strong><br>{value_add}</p>
    </div>
    <br>
    """

# Streamlit UI
st.set_page_config(page_title="Project Summary Generator")
st.header("QBR Project Summary Generator")
st.subheader("Upload your QBR data in CSV format to get formatted summaries")

uploaded_csv = st.file_uploader("Upload QBR CSV", type=["csv"])

if uploaded_csv is not None:
    df = pd.read_csv(uploaded_csv)

    for index, row in df.iterrows():
        combined_text = f"""
        Employee Name: {row.get('Employee Name', '')}
        Lead Name: {row.get('Lead Name', '')}
        Project Name: {row.get('Project Name', '')}
        Project Description: {row.get('Project Description', '')}
        Achievements/Value Adds: {row.get('Achievements/Value Adds', '')}
        Value Add: {row.get('Value Add', '')}
        """

        summary = get_project_summary(combined_text)

        formatted_html = format_summary(
            employee_name=row.get('Employee Name', 'N/A'),
            lead_name=row.get('Lead Name', 'N/A'),
            project_name=row.get('Project Name', 'N/A'),
            project_desc=row.get('Project Description', 'N/A'),
            achievements=row.get('Achievements/Value Adds', 'N/A'),
            value_add=row.get('Value Add', 'N/A')
        )

        st.markdown(formatted_html, unsafe_allow_html=True)
