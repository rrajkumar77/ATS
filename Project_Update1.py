import streamlit as st
import pandas as pd
import os
from io import StringIO
from dotenv import load_dotenv
load_dotenv()

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, doc_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, doc_content, prompt])
    return response.text

def format_response(response_text):
    lines = response_text.split('\n')
    formatted_response = f"""
    **Employee Name**: {lines[0].split(':')[1].strip()}
    **Lead Name**: {lines[1].split(':')[1].strip()}
    **Project Name**: {lines[2].split(':')[1].strip()}
    **Project Description**: {lines[3].split(':')[1].strip()}
    **Achievements/Value Adds**:
    - {lines[4].split(':')[1].strip().replace(';', '\n- ')}
    **Value Add**:
    - {lines[5].split(':')[1].strip().replace(';', '\n- ')}
    """
    return formatted_response

def extract_project_updates(uploaded_file):
    df = pd.read_csv(uploaded_file)
    columns = ['Created By', 'Team_Lead', 'Project_Name', 'Project_Description', 'Acheivements_ValueAdds', 'Value_Add']
    project_updates = df[columns]
    
    formatted_updates = []
    for index, row in project_updates.iterrows():
        input_prompt = f"""
        Employee Name: {row['Created By']}
        Lead Name: {row['Team_Lead']}
        Project Name: {row['Project_Name']}
        Project Description: {row['Project_Description']}
        Achievements/Value Adds: {row['Acheivements_ValueAdds']}
        Value Add: {row['Value_Add']}
        """
        response = get_gemini_response(input_prompt, "", "")
        formatted_update = format_response(response)
        formatted_updates.append(formatted_update)
    
    return formatted_updates

## Streamlit App

st.set_page_config(page_title="Document Analyser")

st.header("Document Analyzer")
st.subheader('This Application helps you to Analyse any document uploaded')
uploaded_file = st.file_uploader("Upload your Document (CSV only)...", type=["csv"])

if uploaded_file is not None:
    st.write("Document Uploaded Successfully")
    project_updates = extract_project_updates(uploaded_file)
    st.subheader("Project Updates")
    for update in project_updates:
        st.write(update)
