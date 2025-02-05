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
Task: Evaluate the provided resume against the given job description.  
Objective: Assess the compatibility of the resume with the job description.
1. Keyword Optimization
"Extract the top 10 industry-specific keywords from this job description."
"Analyze my resume and suggest missing keywords relevant to this [industry/role]."
"Compare my resume to this job posting and identify gaps in required skills and keywords."
2. Formatting & Structure
"Review my resume for ATS formatting issues and suggest improvements."
"Ensure my resume is ATS-friendly by removing any problematic design elements."
"Convert my resume into a simple, ATS-compatible format using standard fonts and bullet points."
3. Action-Oriented Content
"Rewrite my bullet points to be more action-driven using strong verbs."
"Improve my resume summary to be more concise and impactful."
"Quantify my achievements in this resume by adding metrics where applicable."
4. Section Optimization
"Rearrange my resume sections to highlight the most relevant experience first."
"Optimize my work experience section to align with ATS best practices."
"Ensure my education and certifications are formatted correctly for ATS parsing."
5. General ATS Compliance Check
"Check my resume against common ATS rejection issues and suggest fixes."
"Ensure my resume uses a standard file format (e.g., .docx, .pdf) that works with ATS."
"Validate that my resume uses standard section headings (e.g., 'Work Experience' instead of 'Professional Journey')."
6. ATS compliant resume
" Based on the above adjust resume to meet ATS best practices by using standard fonts, bullet points, and section headings. 
Rewrite my bullet points using strong action verbs and quantify my achievements where applicable. 
Optimize my resume summary to clearly highlight my value proposition in a concise, impactful way. 
Finally, validate that my resume is saved in a compatible format (e.g., .docx or .pdf) and check for any ATS rejection issues to ensure it passes screening successfully."
7. Cover Letter Drafting: Write a compelling cover letter that effectively demonstrates how the skills listed in the resume align with the job requirements.  
8. Skills Comparison Table: Create a table listing the skills required in the job description and how the candidate’s skills align with them.  
"""

'''
input_prompt6 = """
Role: Skilled ATS (Applicant Tracking System) scanner with expertise in domain-specific ATS functionality.  
Task: Evaluate the provided resume against the given job description.  
Objective: Assess the compatibility of the resume with the job description from a Human Resource manager's perspective.  
Instructions:  
1. Keyword Analysis: Identify missing keywords in the resume that are relevant to the job description.  
2. Skill Enhancement: Provide recommendations for improving the candidate’s skillset based on the job requirements.  
3. Development Areas: Identify areas where the candidate needs further development to better match the role.  
4. Cover Letter Drafting: Write a compelling cover letter that effectively demonstrates how the skills listed in the resume align with the job requirements.  
5. Skills Comparison Table: Create a table that lists the skills required in the job description alongside how the candidate’s skills align with them.  
6. Resume Optimization: Modify and enhance the resume to ensure it aligns with the job description, optimizing it for Applicant Tracking System (ATS) compatibility while maintaining a professional format.  
Output Format:  
- A detailed list of missing keywords.  
- Specific skill enhancement recommendations.  
- A concise analysis of areas requiring improvement.  
- A professionally written cover letter.  
- A structured comparison table matching job description skills with resume skills.  
- An ATS-optimized version of the resume.  
"""
'''

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
