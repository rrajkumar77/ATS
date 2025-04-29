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
    formatted_response = format_response(response.text)
    return formatted_response

def format_response(response_text):
    lines = response_text.split('\n')
    if len(lines) < 8:
        raise ValueError("Response text does not contain enough information.")
    
    emp_name = lines[0].split(':')[1].strip() if ':' in lines[0] else "N/A"
    project_details = lines[1].split(':')[1].strip() if ':' in lines[1] else "N/A"
    project_name = lines[2].split(':')[1].strip() if ':' in lines[2] else "N/A"
    project_description = lines[3].split(':')[1].strip() if ':' in lines[3] else "N/A"
    team_details = lines[4].split(':')[1].strip() if ':' in lines[4] else "N/A"
    project_problem_statement = lines[5].split(':')[1].strip() if ':' in lines[5] else "N/A"
    resolution_strategy = lines[6].split(':')[1].strip() if ':' in lines[6] else "N/A"
    outcome_value_adds = lines[7].split(':')[1].strip() if ':' in lines[7] else "N/A"

    formatted_response = f"""
    - **Employee Name**: {emp_name}
    - **Project Details**: {project_details}
    - **Project Name**: {project_name}
    - **Project Description**: {project_description}
    - **Team Details**: {team_details}
    - **Project Problem Statement**: {project_problem_statement}
    - **Resolution Strategy and Utilized Tools/Techniques**: {resolution_strategy}
    - **Outcome and Value Adds**: {outcome_value_adds}
    """
    return formatted_response

def input_doc_setup(uploaded_file):
    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            # Read the PDF file
            document = pdf.PdfFileReader(uploaded_file)
            text_parts = []
            for page_num in range(document.getNumPages()):
                page = document.getPage(page_num)
                text_parts.append(page.extract_text())
            doc_text_content = " ".join(text_parts)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            # Read the DOCX file
            document = docx.Document(uploaded_file)
            text_parts = [para.text for para in document.paragraphs]
            doc_text_content = " ".join(text_parts)
        elif uploaded_file.type == "text/plain":
            # Read the TXT file
            doc_text_content = uploaded_file.read().decode("utf-8")
        elif uploaded_file.type == "text/csv":
            # Read the CSV file
            try:
                text_parts = []
                csv_reader = csv.reader(StringIO(uploaded_file.getvalue().decode("utf-8")))
                for row in csv_reader:
                    text_parts.append(", ".join(row))
                doc_text_content = "\n".join(text_parts)
            except csv.Error as e:
                raise ValueError(f"CSV file reading error: {e}")
        else:
            raise ValueError("Unsupported file type")
        return doc_text_content
    else:
        raise FileNotFoundError("No file uploaded")

def extract_project_updates(file_path):
    df = pd.read_csv(file_path)
    columns = ['Created By', 'Team_Lead', 'Project_Name', 'Project_Description', 'Acheivements_ValueAdds', 'Value_Add']
    project_updates = df[columns]
    
    formatted_updates = []
    for index, row in project_updates.iterrows():
        formatted_update = f"""
        - **Employee Name**: {row['Created By']}
        - **Lead Name**: {row['Team_Lead']}
        - **Project Name**: {row['Project_Name']}
        - **Project Description**: {row['Project_Description']}
        - **Achievements/Value Adds**: {row['Acheivements_ValueAdds']}
        - **Value Add**: {row['Value_Add']}
        """
        formatted_updates.append(formatted_update)
    
    return formatted_updates

## Streamlit App

st.set_page_config(page_title="Document Analyser")

st.header("Document Analyzer")
st.subheader('This Application helps you to Analyse any document uploaded')
uploaded_file = st.file_uploader("Upload your Document (PDF, DOCX, CSV, or TXT)...", type=["pdf", "docx", "txt", "csv"])
doc_content = ""

if uploaded_file is not None:
    st.write("Document Uploaded Successfully")

submit1 = st.button("Consultant Project Update")

input_promp = st.text_input("Queries: Feel Free to Ask here")

submit4 = st.button("Answer My Query")

input_prompt1 = """
Based on the transcript uploaded, please provide a comprehensive project update including:
- Employee Name
- Project Details
- Project Name
- Project Description
- Team Details
- Project Problem Statement
- Resolution Strategy and Utilized Tools/Techniques
- Outcome and Value Adds

Please ensure the response is clear and concise, and presented in bullet points.
"""

if submit1:
    if uploaded_file is not None:
        doc_content = input_doc_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, doc_content, "")
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a document to proceed.")

if submit4:
    if uploaded_file is not None:
        doc_content = input_doc_setup(uploaded_file)
        response = get_gemini_response(input_promp, doc_content, "")
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a document to proceed.")

if uploaded_file is not None and uploaded_file.type == "text/csv":
    file_path = uploaded_file.name
    project_updates = extract_project_updates(file_path)
    st.subheader("Project Updates")
    for update in project_updates:
        st.write(update)
