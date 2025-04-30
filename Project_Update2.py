import streamlit as st
import pandas as pd
from io import StringIO
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# Get the Google API key from environment variables
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("Google API Key not found. Please make sure it is set in the environment.")
else:
    genai.configure(api_key=api_key)

def get_gemini_response(input, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    try:
        response = model.generate_content([input, prompt])
        return response.text
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return ""

def extract_project_updates(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)
        if df.empty:
            st.error("The uploaded CSV file is empty. Please upload a valid file.")
            return []
    except pd.errors.EmptyDataError:
        st.error("The uploaded CSV file is empty. Please upload a valid file.")
        return []
    
    columns = ['Created By', 'Team_Lead', 'Project_Name', 'Project_Description', 'Acheivements_ValueAdds', 'Value_Add']
    project_updates = df[columns]
    
    formatted_updates = []
    for index, row in project_updates.iterrows():
        formatted_update = f"""
        <div style="background-color:#F6F5F5; padding:10px; border-radius:5px; margin-bottom:10px;">
            <h3 style="color:#021A2A;">Employee Name: {row['Created By']}</h3>
            <p><strong style="color:#CDDC00;">Lead Name:</strong> {row['Team_Lead']}</p>
            <p><strong style="color:#007698;">Project Name:</strong> {row['Project_Name']}</p>
            <p><strong style="color:#0095D3;">Project Description:</strong> {row['Project_Description']}</p>
            <p><strong style="color:#44D7F4;">Achievements/Value Adds:</strong></p>
            <ul style="color:#333;">
                <li>{row['Acheivements_ValueAdds'].replace(';', '.</li>\n<li>')}</li>
            </ul>
            <p><strong style="color:#F9671D;">Value Add:</strong></p>
            <ul style="color:#333;">
                <li>{row['Value_Add'].replace(';', '.</li>\n<li>')}</li>
            </ul>
        </div>
        """
        formatted_updates.append(formatted_update)
    
    return formatted_updates

def concise_project_update(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)
        if df.empty:
            st.error("The uploaded CSV file is empty. Please upload a valid file.")
            return []
    except pd.errors.EmptyDataError:
        st.error("The uploaded CSV file is empty. Please upload a valid file.")
        return []
    
    columns = ['Created By', 'Team_Lead', 'Project_Name', 'Project_Description', 'Acheivements_ValueAdds', 'Value_Add']
    project_updates = df[columns]
    
    concise_updates = []
    for index, row in project_updates.iterrows():
        concise_update = f"""
        <div style="background-color:#F6F5F5; padding:10px; border-radius:5px; margin-bottom:10px;">
            <h3 style="color:#021A2A;">Employee Name: {row['Created By']}</h3>
            <p><strong style="color:#CDDC00;">Lead Name:</strong> {row['Team_Lead']}</p>
            <p><strong style="color:#007698;">Project Name:</strong> {row['Project_Name']}</p>
            <p><strong style="color:#0095D3;">Project Description:</strong> {row['Project_Description']}</p>
            <p><strong style="color:#44D7F4;">Achievements/Value Adds:</strong></p>
            <ul style="color:#333;">
                <li>{row['Acheivements_ValueAdds'].replace(';', '.</li>\n<li>')}</li>
            </ul>
            <p><strong style="color:#F9671D;">Value Add:</strong></p>
            <ul style="color:#333;">
                <li>{row['Value_Add'].replace(';', '.</li>\n<li>')}</li>
            </ul>
            <p><strong style="color:#007698;">Concise Insights:</strong></p>
            <ul style="color:#333;">
                <li>Project Name: {row['Project_Name']}</li>
                <li>Lead Name: {row['Team_Lead']}</li>
                <li>Key Achievements: {row['Acheivements_ValueAdds'].replace(';', ', ')}</li>
                <li>Value Adds: {row['Value_Add'].replace(';', ', ')}</li>
            </ul>
        </div>
        """
        concise_updates.append(concise_update)
    
    return concise_updates

## Streamlit App
st.set_page_config(page_title="Document Analyser")
st.header("Document Analyzer")
st.subheader('This Application helps you to Analyse any document uploaded')
uploaded_file = st.file_uploader("Upload your Document (CSV only)...", type=["csv"])

# Input prompt for generating concise insights
input_prompt = st.text_input("Prompt: ", key="input_prompt")

if uploaded_file is not None:
    st.write("Document Uploaded Successfully")
    project_updates = extract_project_updates(uploaded_file)
    concise_updates = concise_project_update(uploaded_file)
    st.subheader("Project Updates")
    for update in project_updates:
        st.markdown(update, unsafe_allow_html=True)
    st.subheader("Concise Project Updates")
    for update in concise_updates:
        st.markdown(update, unsafe_allow_html=True)

if st.button("Generate Insights"):
    if uploaded_file is not None:
        concise_updates = concise_project_update(uploaded_file)
        if concise_updates:
            response = get_gemini_response(input_prompt, concise_updates)
            st.subheader("Generated Insights")
            st.write(response)
        else:
            st.write("Please upload a valid CSV file to proceed.")
