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

## Streamlit App

st.set_page_config(page_title="Resume Expert")

st.header("JobFit Analyzer")
st.subheader('This Application helps you to evaluate the Resume Review with the Job Description')
input_text = st.text_input("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your Resume(PDF)...", type=["pdf"])
pdf_content = ""

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
submit2 = st.button("Overall Evaluation, Strengths, Weaknesses, Areas for Improvement, Advice for Enhancing Skills")
submit3 = st.button("Identify Missing Keywords and provide recommendation")
submit4 = st.button("Percentage match")
input_prompt = st.text_input("Queries: Feel Free to Ask here")
submit5 = st.button("Answer My Query")
submit6 = st.button("Update Resume")

input_prompt1 = """
Role: Experienced Technical Human Resource Manager with expertise in technical evaluations
Task: Review the provided resume against the job description.
Objective: Evaluate whether the candidate's profile aligns with the role.
Instructions:
Provide a professional evaluation of the candidate's profile.
Highlight the strengths and weaknesses of the applicant concerning the specified job requirements.
"""

input_prompt2 = """
Role: Experienced Technical Human Resource Manager with expertise in technical evaluations
Task: Scrutinize the provided resume in light of the job description.
Objective: Evaluate the candidate's suitability for the role from an HR perspective.
Instructions:
Share insights on the candidate's suitability for the role.
Highlight the strengths and weaknesses of the applicant concerning the job requirements.
Identify areas where improvement is needed.
Offer advice on enhancing the candidate's skills.
"""

input_prompt3 = """
Role: Skilled ATS (Applicant Tracking System) scanner with expertise in domain and ATS functionality
Task: Evaluate the provided resume against the job description.
Objective: Assess the compatibility of the resume with the role from a Human Resource manager's perspective.
Instructions:
Identify any missing keywords in the resume relevant to the job description.
Provide recommendations for enhancing the candidate's skills.
Identify areas where further development is needed.
"""
input_prompt4 = """
Role: Skilled ATS (Applicant Tracking System) scanner with a deep understanding of the technology mentioned in the job description and ATS functionality
Task: Evaluate the provided resume against the job description.
Objective: Assess the compatibility of the resume with the job description.
Instructions:
Provide the percentage that matches the resume with the job description.
List the missing keywords.
Share final thoughts on the candidate's suitability for the role.
"""

input_prompt6 = """
Role: Skilled ATS (Applicant Tracking System) scanner with expertise in domain-specific ATS functionality.  
Task: Rewrite and optimize the provided resume against the given job description.  
1. Write a cover letter
2. Create a Skills Comparison Table 
3. Optimise Resume
Objective:
1. Cover Letter: Write a compelling cover letter that effectively demonstrates how the skills listed in the resume align with the job requirements.  
2. Skills Comparison Table: "Create a Skills Comparison Table that directly matches the key Job Description Skills with my own skills and experience from my resume. 
Clearly demonstrate how my past projects and experience align with each required skill to showcase me as the best fit for the role.
The table should be structured as follows:
Job Description Skills	|| My Skills & Experience
[Skill from JD]	|| [My relevant experience showcasing this skill]
[Skill from JD]	|| [My relevant experience showcasing this skill]
Ensure that my responses use strong action verbs, highlight quantifiable achievements, and reflect real impact-driven experiences from my past projects. 
The goal is to give recruiters full confidence that I am the right fit for the job."
3. Optimise Resume: 
"Compare my resume against this job description and optimize it for a perfect match with ATS compliance. 
Extract the top 10 industry-specific keywords from the JD and identify any missing or underutilized keywords in my resume. 
Ensure my resume highlights the most relevant skills, experience, and qualifications from the JD to align closely with the employer’s requirements.
Optimize formatting and structure to follow ATS best practices by using standard fonts, clear bullet points, and proper section headings. Remove any design elements that may hinder ATS readability.
Enhance my work experience section by rewriting bullet points with strong action verbs and adding quantifiable metrics to demonstrate impact. Improve my summary to be concise, compelling, and aligned with the JD’s core expectations.
Validate that my resume follows standard ATS-friendly section headings (e.g., 'Work Experience' instead of 'Professional Journey') and is saved in a compatible format (.docx or .pdf) to avoid parsing errors. Finally, perform a comprehensive ATS compliance check to identify and fix any issues that could prevent my resume from passing the ATS screening process."
Finally, validate that my resume is saved in a compatible format (e.g., .docx or .pdf) and check for any ATS rejection issues to ensure it passes screening successfully."
"""


if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")

elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")

elif submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt4, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")

elif submit5:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")
elif submit6:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt6, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")
