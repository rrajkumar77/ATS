import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
import fitz
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define analysis prompts
project_update_prompt = """
Role: Project Management Expert
Task: Review the provided document for project updates.
Objective: Extract and organize comprehensive project information.
Instructions:
Please provide a comprehensive project update in a clear and concise format. Include:
1. Employee Name
2. Project Details
   - Project Name
   - Project Description
3. Project Problem Statement
4. Resolution Strategy and Utilized Tools/Techniques
5. Outcome and Value Adds

Sequence by high value to the organisation and present in a well-structured format.
"""

technical_review_prompt = """
Role: Senior Technical Expert
Task: Review the provided document for technical analysis.
Objective: Evaluate technical aspects and implementation details.
Instructions:
1. Analyze technical specifications and implementation details
2. Identify key technologies and methodologies used
3. Evaluate technical challenges and solutions
4. Assess code quality and architecture (if applicable)
5. Provide recommendations for technical improvements
"""

business_analysis_prompt = """
Role: Business Analysis Expert
Task: Review the provided document for business insights.
Objective: Extract and analyze business-related information.
Instructions:
1. Identify key business requirements and objectives
2. Analyze stakeholder needs and expectations
3. Evaluate business processes and workflows
4. Assess impact on business operations
5. Provide recommendations for business optimization
"""

risk_assessment_prompt = """
Role: Risk Management Expert
Task: Review the provided document for risk analysis.
Objective: Identify and assess potential risks and mitigation strategies.
Instructions:
1. Identify potential risks and challenges
2. Assess impact and probability of risks
3. Evaluate existing mitigation strategies
4. Recommend additional risk management measures
5. Prioritize risks based on severity and impact
"""

def get_gemini_response(input_text, document_text):
    """Get response from Gemini model"""
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([input_text, document_text])
    return response.text

def process_document(uploaded_file):
    """Process uploaded document and extract text"""
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split(".")[-1].lower()
        
        if file_extension == "pdf":
            document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            text_parts = [page.get_text() for page in document]
            return " ".join(text_parts)
        elif file_extension in ["txt", "doc", "docx"]:
            return str(uploaded_file.read(), "utf-8")
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
    return None

def main():
    st.set_page_config(page_title="Document Analyzer Pro", layout="wide")
    
    st.title("📄 Document Analyzer Pro")
    st.write("Upload a document and choose your analysis type!")

    # File uploader
    uploaded_file = st.file_uploader(
        "Upload your document (PDF, TXT, DOC, DOCX)", 
        type=["pdf", "txt", "doc", "docx"]
    )

    if uploaded_file:
        try:
            document_content = process_document(uploaded_file)
            st.success("Document uploaded and processed successfully!")
            
            # Document preview
            with st.expander("Document Preview"):
                st.text(document_content[:500] + "...")
            
            # Analysis Options
            st.subheader("Choose Analysis Type")
            
            # Create two rows of columns for buttons
            col1, col2 = st.columns(2)
            col3, col4 = st.columns(2)
            
            with col1:
                if st.button("🎯 Project Update", use_container_width=True):
                    with st.spinner("Generating project update..."):
                        response = get_gemini_response(project_update_prompt, document_content)
                        st.subheader("Project Update Analysis")
                        st.markdown(response)
            
            with col2:
                if st.button("🔧 Technical Review", use_container_width=True):
                    with st.spinner("Performing technical review..."):
                        response = get_gemini_response(technical_review_prompt, document_content)
                        st.subheader("Technical Review")
                        st.markdown(response)
            
            with col3:
                if st.button("💼 Business Analysis", use_container_width=True):
                    with st.spinner("Performing business analysis..."):
                        response = get_gemini_response(business_analysis_prompt, document_content)
                        st.subheader("Business Analysis")
                        st.markdown(response)
            
            with col4:
                if st.button("⚠️ Risk Assessment", use_container_width=True):
                    with st.spinner("Performing risk assessment..."):
                        response = get_gemini_response(risk_assessment_prompt, document_content)
                        st.subheader("Risk Assessment")
                        st.markdown(response)
            
            # Custom Analysis Section
            st.subheader("Custom Analysis")
            user_prompt = st.text_area(
                "Enter your custom analysis prompt:",
                height=100,
                placeholder="Enter your specific questions or analysis requirements..."
            )

            if st.button("🔍 Analyze", type="primary"):
                if user_prompt:
                    with st.spinner("Analyzing document..."):
                        response = get_gemini_response(user_prompt, document_content)
                        st.subheader("Custom Analysis Results")
                        st.markdown(response)
                else:
                    st.warning("Please enter a prompt for analysis.")
                    
        except Exception as e:
            st.error(f"Error processing document: {str(e)}")
            
    else:
        st.info("Please upload a document to begin analysis.")

if __name__ == "__main__":
    main()