import streamlit as st
import pandas as pd
from io import StringIO

def extract_project_updates(uploaded_file):
    df = pd.read_csv(uploaded_file)
    columns = ['Created By', 'Team_Lead', 'Project_Name', 'Project_Description', 'Acheivements_ValueAdds', 'Value_Add']
    project_updates = df[columns]
    
    formatted_updates = []
    for index, row in project_updates.iterrows():
        formatted_update = {
            "Employee Name": row['Created By'],
            "Lead Name": row['Team_Lead'],
            "Project Name": row['Project_Name'],
            "Project Description": row['Project_Description'],
            "Achievements/Value Adds": row['Acheivements_ValueAdds'].replace(';', '.\n- '),
            "Value Add": row['Value_Add'].replace(';', '.\n- ')
        }
        formatted_updates.append(formatted_update)
    
    formatted_df = pd.DataFrame(formatted_updates)
    return formatted_df

## Streamlit App

st.set_page_config(page_title="Document Analyser")

st.header("Document Analyzer")
st.subheader('This Application helps you to Analyse any document uploaded')
uploaded_file = st.file_uploader("Upload your Document (CSV only)...", type=["csv"])

if uploaded_file is not None:
    st.write("Document Uploaded Successfully")
    project_updates = extract_project_updates(uploaded_file)
    st.subheader("Project Updates")
    
    for index, row in project_updates.iterrows():
        st.markdown(f"""
        <div style="background-color:#f0f0f5; padding:10px; border-radius:5px; margin-bottom:10px;">
            <h3 style="color:#C6DC00;">Employee Name: {row['Employee Name']}</h3>
            <p><strong style="color:#F8971D;">Lead Name:</strong> {row['Lead Name']}</p>
            <p><strong style="color:#F8971D;">Project Name:</strong> {row['Project Name']}</p>
            <p><strong style="color:#F8971D;">Project Description:</strong> {row['Project Description']}</p>
            <p><strong style="color:#F8971D;">Achievements/Value Adds:</strong></p>
            <ul style="color:#F8971D;">
                {row['Achievements/Value Adds']}
            </ul>
            <p><strong style="color:#FF5733;">Value Add:</strong></p>
            <ul style="color:#F8971D;">
                {row['Value Add']}
            </ul>
        </div>
        """, unsafe_allow_html=True)
