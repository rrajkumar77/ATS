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
    st.write(project_updates)
