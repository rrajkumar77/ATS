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
            "Employee Name": row['Created By'].replace(';', '.\n- '),
            "Lead Name": row['Team_Lead'].replace(';', '.\n- '),
            "Project Name": row['Project_Name'].replace(';', '.\n- '),
            "Project Description": row['Project_Description'].replace(';', '.\n- '),
            "Achievements/Value Adds": row['Acheivements_ValueAdds'].replace(';', '.\n- '),
            "Value Add": row['Value_Add'].replace(';', '.\n- ')
        }
        formatted_updates.append(formatted_update)
    formatted_df = pd.DataFrame(formatted_updates)
    return formatted_df

def generate_bullet_summary(row):
    """
    Generates a bullet-point summary for a project update row.
    """
    summary = (
        f"- **Lead Name:** {row['Lead Name']}\n"
        f"- **Project Name:** {row['Project Name']}\n"
        f"- **Project Description:** {row['Project Description']}\n"
        f"- **Achievements/Value Adds:** {row['Achievements/Value Adds']}\n"
        f"- **Value Add:** {row['Value Add']}\n"
    )
    return summary

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
**Lead Name:** {row['Lead Name']}

**Project Name:** {row['Project Name']}

**Project Description:** {row['Project Description']}

**Achievements/Value Adds:** {row['Achievements/Value Adds']}

**Value Add:** {row['Value Add']}
        """)
        # Add bullet-point summary for stakeholders
        st.markdown("**Summary for Stakeholders:**")
        st.markdown(generate_bullet_summary(row))

