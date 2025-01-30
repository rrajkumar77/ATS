import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
load_dotenv()
import fitz 

import google.generativeai as genai

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([input, pdf_content, prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Read the PDF file
        document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        # Initialize a list to hold the text of each page
        text_parts = []

        # Iterate over the pages of the PDF to extract the text
        for page in document:
            text_parts.append(page.get_text())

        # Concatenate the list into a single string with a space in between each part
        pdf_text_content = " ".join(text_parts)
        return pdf_text_content
    else:
        raise FileNotFoundError("No file uploaded")

def extract_skills_from_resume(pdf_content):
    # Placeholder function to extract skills from resume content
    # You can implement a more sophisticated extraction logic here
    skills = ["Python", "Machine Learning", "Data Analysis", "Project Management"]
    return skills

## Streamlit App

st.set_page_config(page_title="Resume Expert")

st.header("JobFit Analyzer")
st.subheader('This Application helps you to evaluate the Resume Review with the Job Description')
input_text = st.text_input("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your Resume(PDF)...", type=["pdf"])
pdf_content = ""

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

top_skills = st.text_input("Top Skills Required for the Job (comma-separated):")

submit1 = st.button("Technical Recruiter Analysis")
submit2 = st.button("Technical Questions")
submit3 = st.button("Domain Expert Analysis")
submit4 = st.button("Technical Manager Analysis")
submit5 = st.button("Answer My Query")
submit6 = st.button("Skill Analysis")
submit7 = st.button("JD Summarization")

input_promp = st.text_input("Queries: Feel Free to Ask here")

input_prompt1 = """
Role: Experienced Technical Human Resource Manager with expertise in technical evaluations and Recruitement
Task: Review the provided resume against the job description.
Objective: Evaluate whether the candidate's profile aligns with the role.
Instructions:
Provide the match percentage between the resume and job description
Provide a professional evaluation of the candidate's profile.
Highlight the strengths and weaknesses of the applicant concerning the specified job requirements.
"""

input_prompt2 = """
Can you share some technical questions to evaluate the candidate based on the above JD and Resume uploaded
Have the questions in sequence order from project start to finish.
Classify questions from JD and Resume 
also provide answers so the recruiter can validate 
"""

input_prompt3 = """
Role: Skilled ATS (Applicant Tracking System) scanner with expertise in domain and ATS functionality
Task: Evaluate the provided resume against the job description.
Objective: Assess the compatibility of the resume with the job description from a Domain Expert perspective. (Eg: Business Analyst(BA), Functional Manger or Project Manager)
Instructions:
Calculating the match percentage between the resume and job description, provide a percentage number and explanation.
Identify any missing keywords in the resume relevant to the job description.
Your evaluation should be thorough, precise, and objective. It should ensure that the most qualified candidates are accurately identified based on their resume content concerning the job criteria.
"""
input_prompt4 = """
Role: Skilled ATS (Applicant Tracking System) scanner with a deep understanding of the technology and Technical skills mentioned in the job description and ATS functionality
Task: Evaluate the provided resume against the job description.
Objective: Assess the compatibility of the resume with the job description from a Technical Expert perspective.
Instructions:
1. Calculate the match percentage between the resume and job description, provide a percentage number 
2. Explain the match and the gap
3. Identify missing keywords or skills from the resume compared to the job description.
4. Create a table that includes the top 5 skills, the required years of experience (JD), the candidate's years of experience (Resume), and the relevant projects with the year they have worked on.
5. Share final thoughts on the candidate's suitability for the role.
"""
input_prompt5 = """
Role: AI Assistant
Task: Summarize the provided job description.
Objective: Provide a concise summary of the job description.
Instructions:
Summarize the key responsibilities, required skills, and qualifications mentioned in the job description.
"""
input_prompt6 = """
Role: Skill Analyst
Task: Perform a Skill Analysis
Objective: Analyze the provided job description (JD) and resume to determine the match status of skills.
Instructions:
Input: top_skills, input_text
Process: For each skill in the job description, check if it is present in the resume.
Output:
Skill: The skill being analyzed.
Match Status: "Yes" if the skill is present in the resume, otherwise "No".
Relevant Projects: List of relevant projects from the resume (e.g., "Project A, Project B").
Years of Experience: Total years of experience related to the skill (e.g., "3 years").
"""
if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("Technical Recruiter Analysis")
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")

elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("Account Manager Analysis")
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("Domain Expert Analysis")
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")

elif submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt4, pdf_content, input_text)
        st.subheader("Technical Manager Analysis")
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")

elif submit5:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_promp5, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")
        
elif submit6:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_promp6, pdf_content, input_text)
        st.subheader("Top Skill Analysis")
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")

elif submit7:
    if input_text:
        response = get_gemini_response(input_prompt5, "", input_text)
        st.subheader("Job Description Summary")
        st.write(response)
    else:
        st.write("Please enter a Job Description to proceed.")
