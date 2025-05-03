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

# Gemini AI summary generation
def get_project_summary(text):
    model = genai.GenerativeModel('gemini-pro')
    prompt = (
        "Please summarize the following project in 4-5 concise bullet points. "
        "Include the project name, responsibilities, technologies used, achievements, and business value. "
        "Format the response using HTML <ul><li> tags for each bullet point:"
    )
    try:
        response = model.generate_content([prompt, text])
        return response.text
    except Exception as e:
        return f"<p style='color:red;'>Error: {str(e)}</p>"

# HTML formatting for display
def format_summary(employee_name, summary_html):
    return f"""
    <div style="background-color:#F5F5F5; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h3 style="color:#012A52;">Employee Name: {employee_name}</h3>
        <div style="color:#00798B; font-size: 16px;">{summary_html}</div>
    </div>
    """

# Streamlit UI
st.set_page_config(page_title="Project Summary Generator")
st.header("QBR Project Summary Generator")
st.subheader("Upload your QBR CSV to generate summaries")

uploaded_csv = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_csv is not None:
    df = pd.read_csv(uploaded_csv)
    st.success("CSV uploaded successfully!")

    # Show column names so we can confirm structure
    st.write("Detected Columns:", df.columns.tolist())

    # Loop through each record and process
    for index, row in df.iterrows():
        # Adjust these keys if your CSV uses different column names
        employee_name = row.get("Employee Name", "").strip()
        lead_name = row.get("Lead Name", "").strip()
        project_name = row.get("Project Name", "").strip()
        project_desc = row.get("Project Description", "").strip()
        achievements = row.get("Achievements/Value Adds", "").strip()
        value_add = row.get("Value Add", "").strip()

        # Combine all fields into one prompt input
        input_text = f"""
        Employee Name: {employee_name}
        Lead Name: {lead_name}
        Project Name: {project_name}
        Project Description: {project_desc}
        Achievements: {achievements}
        Value Add: {value_add}
        """

        summary_html = get_project_summary(input_text)
        formatted_block = format_summary(employee_name, summary_html)
        st.markdown(formatted_block, unsafe_allow_html=True)
