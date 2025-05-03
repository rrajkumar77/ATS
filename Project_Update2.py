import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load your .env with the Google API key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Configure Gemini
if not api_key:
    st.error("Missing GOOGLE_API_KEY in environment.")
else:
    genai.configure(api_key=api_key)

# Define the Gemini summarizer
def get_project_summary(text):
    try:
        model = genai.GenerativeModel('models/gemini-pro')  # Fully qualified path
        prompt = (
            "Summarize this employee's project experience in 4-5 concise bullet points using <ul><li> HTML tags. "
            "Include project name, responsibilities, achievements, value add, and technologies used:"
        )
        response = model.generate_content([prompt + "\n\n" + text])
        return response.text
    except Exception as e:
        return f"<p style='color:red;'>Error: {str(e)}</p>"

# Format HTML block with brand styling
def format_summary(employee_name, summary_html):
    return f"""
    <div style="background-color:#F5F5F5; padding: 20px; border-radius: 12px; margin-bottom: 25px;">
        <h3 style="color:#012A52; font-family:sans-serif;">Employee Name: {employee_name}</h3>
        <div style="color:#00798B; font-size: 16px; font-family:sans-serif;">{summary_html}</div>
    </div>
    """

# Streamlit layout
st.set_page_config(page_title="Project Summary Generator", layout="centered")
st.title("🔍 Project Summary Generator")
st.markdown("Upload a QBR CSV to generate project summaries in your brand format.")

# CSV uploader
uploaded_file = st.file_uploader("Upload QBR CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")

    st.write("📄 **Detected Columns:**", df.columns.tolist())

    for idx, row in df.iterrows():
        # Adjust column names based on your actual CSV
        employee_name = row.get("Employee Name", "N/A")
        lead_name = row.get("Lead Name", "")
        project_name = row.get("Project Name", "")
        project_description = row.get("Project Description", "")
        achievements = row.get("Achievements/Value Adds", "")
        value_add = row.get("Value Add", "")

        # Combine into one input
        full_text = f"""
        Employee Name: {employee_name}
        Lead Name: {lead_name}
        Project Name: {project_name}
        Project Description: {project_description}
        Achievements: {achievements}
        Value Add: {value_add}
        """

        summary_html = get_project_summary(full_text)
        summary_block = format_summary(employee_name, summary_html)
        st.markdown(summary_block, unsafe_allow_html=True)
