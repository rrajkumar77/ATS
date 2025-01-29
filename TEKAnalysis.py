import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
import docx
import pandas as pd
import fitz
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
            document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            text_parts = [page.get_text() for page in document]
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
st.set_page_config(page_title="JobFit Analyzer")

st.header("JobFit Analyzer")
st.subheader('Evaluate the Resume Against the Job Description')

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

submit1 = st.button("Technical Recruiter Analysis")
submit2 = st.button("Account Manager Analysis")
submit3 = st.button("Domain Expert Analysis")
submit4 = st.button("Technical Manager Analysis")
submit5 = st.button("Compare Resume with JD")
submit6 = st.button("Answer My Query")

input_promp = st.text_input("Queries: Feel Free to Ask here")

input_prompts = {
    "Technical Recruiter Analysis": """
    Role: Experienced Technical Human Resource Manager with expertise in technical evaluations and Recruitment
    Task: Review the provided resume against the job description.
    Objective: Evaluate whether the candidate's profile aligns with the role.
    Instructions:
    Provide a professional evaluation of the candidate's profile.
    Highlight the strengths and weaknesses of the applicant concerning the specified job requirements.
    """,
    "Account Manager Analysis": """
    Role: Experienced Technical Human Resource Manager with expertise in technical evaluations
    Task: Scrutinize the provided resume in light of the job description.
    Objective: Evaluate the candidate's suitability for the role from an HR perspective.
    """,
    "Domain Expert Analysis": """
    Role: Skilled ATS (Applicant Tracking System) scanner with expertise in domain and ATS functionality
    Task: Evaluate the provided resume against the job description.
    Objective: Assess the compatibility of the resume with the job description from a Domain Expert perspective.
    Instructions:
    - Calculate the match percentage between the resume and job description, provide a percentage number and explanation.
    - Identify any missing keywords in the resume relevant to the job description.
    """,
    "Technical Manager Analysis": """
    Role: Skilled ATS scanner with deep understanding of technology and technical skills
    Task: Evaluate the provided resume against the job description.
    Objective: Assess the compatibility of the resume with the job description from a Technical Expert perspective.
    Instructions:
    - Calculate match percentage and provide an explanation.
    - Identify missing keywords or skills.
    - Create a table with top 5 skills, years of experience required vs. candidate experience, and relevant projects.
    """
}

if submit1:
    selected_prompt = input_prompts["Technical Recruiter Analysis"]
elif submit2:
    selected_prompt = input_prompts["Account Manager Analysis"]
elif submit3:
    selected_prompt = input_prompts["Domain Expert Analysis"]
elif submit4:
    selected_prompt = input_prompts["Technical Manager Analysis"]
else:
    selected_prompt = None

if selected_prompt:
    if uploaded_file is not None and jd_file is not None:
        response = get_gemini_response(selected_prompt, doc_content, jd_content)
        st.subheader(selected_prompt.split("\n")[0])
        st.write(response)
    else:
        st.write("Please upload both a resume and a job description to proceed.")

if submit5:
    if uploaded_file is not None and jd_file is not None:
        input_prompt5 = """
        Compare the given resume with the job description and list the matching and missing skills.
        Provide an overall compatibility score and suggest areas for improvement.
        """
        response = get_gemini_response(input_prompt5, doc_content, jd_content)
        st.subheader("Comparison Result")
        st.write(response)
    else:
        st.write("Please upload both a resume and a job description to proceed.")

if submit6:
    if uploaded_file is not None:
        response = get_gemini_response(input_promp, doc_content, "")
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a document to proceed.")
