import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
import docx
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, doc_content, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([input, doc_content, prompt])
    return response.text

def input_doc_setup(uploaded_file):
    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            document = pdf.PdfReader(uploaded_file)
            text_parts = [page.extract_text() for page in document.pages if page.extract_text()]
            doc_text_content = " ".join(text_parts)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            document = docx.Document(uploaded_file)
            text_parts = [para.text for para in document.paragraphs]
            doc_text_content = " ".join(text_parts)
        elif uploaded_file.type == "text/plain":
            doc_text_content = uploaded_file.read().decode("utf-8")
        else:
            raise ValueError("Unsupported file type")
        return doc_text_content
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit App
st.set_page_config(page_title="Resume Expert")

st.header("Document Analyzer")
st.subheader('Analyze your resume and match required skills')

uploaded_file = st.file_uploader("Upload your Resume (PDF, DOCX, or TXT)...", type=["pdf", "docx", "txt"])
jd_file = st.file_uploader("Upload Job Description (PDF, DOCX, or TXT)...", type=["pdf", "docx", "txt"])
user_skills = st.text_area("Enter Top Required Skills (comma-separated)", "Python, Data Analysis, Machine Learning")

doc_content = ""
jd_content = ""
if uploaded_file is not None:
    st.write("Resume Uploaded Successfully")
    doc_content = input_doc_setup(uploaded_file)
if jd_file is not None:
    st.write("Job Description Uploaded Successfully")
    jd_content = input_doc_setup(jd_file)
    
skill_list = [skill.strip().lower() for skill in user_skills.split(",")]

submit1 = st.button("Consultant Project Update")
submit2 = st.button("Analyze Resume")
submit4 = st.button("Compare Resume with JD")
input_promp = st.text_input("Queries: Feel Free to Ask here")
submit3 = st.button("Answer My Query")

input_prompt1 = """
Based on the transcript uploaded, please provide a comprehensive project update.
"""

if submit1:
    if uploaded_file is not None:
        response = get_gemini_response(input_prompt1, doc_content, "")
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a document to proceed.")

if submit2:
    if uploaded_file is not None and user_skills:
        matching_skills = {skill: skill in doc_content.lower() for skill in skill_list}
        
        input_prompt2 = f"""
        Extract the relevant projects and years of experience for each of the following skills: {', '.join(skill_list)} 
        from the resume.
        """
        
        response = get_gemini_response(input_prompt2, doc_content, "")
        project_experience = response.split('\n')  # Assumes AI provides structured output
        
        results = []
        for skill in skill_list:
            matched = "✔" if matching_skills[skill] else "✖"
            relevant_projects = next((proj for proj in project_experience if skill in proj.lower()), "No relevant experience found")
            results.append([skill, matched, relevant_projects])
        
        df = pd.DataFrame(results, columns=["Skill", "Matched", "Relevant Projects & Experience"])
        
        st.subheader("Skill Match Results")
        st.dataframe(df)
    else:
        st.write("Please upload a resume and enter required skills to proceed.")

if submit4:
    if uploaded_file is not None and jd_file is not None:
        input_prompt3 = """
        Compare the given resume with the job description and list the matching and missing skills.
        Provide an overall compatibility score and suggest areas for improvement.
        """
        response = get_gemini_response(input_prompt3, doc_content, jd_content)
        st.subheader("Comparison Result")
        st.write(response)
    else:
        st.write("Please upload both a resume and a job description to proceed.")

if submit3:
    if uploaded_file is not None:
        response = get_gemini_response(input_promp, doc_content, "")
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a document to proceed.")
