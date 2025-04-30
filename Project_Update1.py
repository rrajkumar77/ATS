import streamlit as st
import pandas as pd
from io import StringIO

def extract_project_updates(uploaded_file):
    df = pd.read_csv(uploaded_file, encoding='utf-8')
    st.write("Columns in the uploaded file:", df.columns)  # Print the column names to verify
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

# Streamlit App
st.set_page_config(page_title="Document Analyser")
st.header("Document Analyzer")
st.subheader('This Application helps you to Analyse any document uploaded')
uploaded_file = st.file_uploader("Upload your Document (CSV only)...", type=["csv"])
if uploaded_file is not None:
    st.write("Document Uploaded Successfully")
    project_updates = extract_project_updates(uploaded_file)
    st.subheader("Project Updates")
    for update in project_updates:
        st.markdown(update, unsafe_allow_html=True)
