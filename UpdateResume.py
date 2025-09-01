import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini function to get a response
def get_gemini_response(input_text):
    """
    Generates a response from the Gemini 1.5-flash model.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(input_text)
    return response.text

# Function to convert PDF to text
def input_pdf_text(uploaded_file):
    """
    Extracts text from a PDF file.
    """
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Define the input prompt for the Gemini model
input_prompt = """
You are a senior-level career coach and professional resume writer specializing in executive roles (VP and Director) within the data and analytics domain. 
Your task is to provide a detailed, actionable plan for tailoring an existing resume to a specific job description.

**Job Description Analysis:**
Analyze the job description provided below. Identify and list the top 5-7 most critical responsibilities, required skills, and quantifiable success metrics. Pay special attention to keywords related to leadership, strategy, business impact, and cross-functional collaboration.

**Resume Analysis:**
Review the uploaded resume provided below. Identify the sections, experience, and achievements that are most relevant to the critical points you identified in the job description.

**Resume Revision & Output Generation:**
Based on your analysis, generate the following revised content. Your tone must be strategic, results-oriented, and professional, using language appropriate for a senior leadership position.

1.  **Revised Professional Summary:**
    Craft a new, concise professional summary (3-5 lines) that begins with a senior title (e.g., "Strategic Data & Analytics Leader...") and directly connects the applicant's experience to the key requirements of the job description. The summary should be a hook that demonstrates the candidate is a perfect fit.

2.  **Tailored Experience Bullet Points:**
    For each of the most relevant past roles listed in the resume, generate 3-5 new bullet points that are direct and measurable. These new bullet points should replace or augment the existing ones.
    Each bullet point should follow the "Action Verb + Accomplishment + Result (with a quantifiable metric)" formula.
    Ensure the results directly address the core responsibilities and skills from the job description. For example, if the job description mentions "driving business growth," ensure the bullet point includes a metric related to revenue or market share.
    Focus on accomplishments that demonstrate strategic leadership, team management, and the ability to drive business value through data.

**Evaluation Output:**
1.  **Match Percentage:**
    Calculate the match percentage between the resume and job description, providing a numerical score.

2.  **Match Explanation:**
    Explain the match, highlighting the strengths of the candidate's resume relative to the job description.

3.  **Missing Keywords/Skills:**
    Identify any missing keywords or skills from the resume that are present in the job description.

4.  **Skills Table:**
    Create a table that includes the top 5 skills, the required years of experience (from the JD), the candidate's years of experience (from the Resume), and the relevant projects they have worked on.

**Inputs:**
-   **Resume:** {resume_text}
-   **Job Description:** {jd_text}
"""

# Streamlit app
st.set_page_config(page_title="Resume Matcher", layout="wide")

st.title("Raj's Smart ATS")
st.markdown("### Improve Your Resume's ATS Score and Get Tailored Content")

# Input fields
with st.container():
    st.markdown("#### Paste the Job Description")
    jd_text = st.text_area("Job Description", height=250, key="jd_input")

    st.markdown("#### Upload Your Resume (PDF format)")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"], help="Please upload your resume in PDF format.", key="resume_uploader")

    submit_button = st.button("Check Your Score")

# Logic for processing
if submit_button:
    if uploaded_file is not None and jd_text:
        with st.spinner("Processing..."):
            try:
                resume_text = input_pdf_text(uploaded_file)
                prompt_with_data = input_prompt.format(resume_text=resume_text, jd_text=jd_text)
                response = get_gemini_response(prompt_with_data)
                st.markdown("---")
                st.subheader("Analysis and Tailored Content")
                st.write(response)
            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.info("Please ensure your PDF is not an image and the job description is pasted correctly.")
    else:
        st.warning("Please paste the job description and upload your resume to get started.")
