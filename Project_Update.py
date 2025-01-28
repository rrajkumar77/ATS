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

def get_gemini_response(input_text, document_text):
    """Get response from Gemini model"""
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([input_text, document_text])
    return response.text

def process_document(uploaded_file):
    """Process uploaded document and extract text"""
    if uploaded_file is not None:
        # Get file extension
        file_extension = uploaded_file.name.split(".")[-1].lower()
        
        if file_extension == "pdf":
            # Process PDF
            document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            text_parts = [page.get_text() for page in document]
            return " ".join(text_parts)
        elif file_extension in ["txt", "doc", "docx"]:
            # Process text files
            return str(uploaded_file.read(), "utf-8")
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
    return None

def main():
    st.set_page_config(page_title="Document Analyzer")
    
    st.title("📄 Document Analyzer")
    st.write("Upload a document and analyze its content!")

    # File uploader
    uploaded_file = st.file_uploader(
        "Upload your document (PDF, TXT, DOC, DOCX)", 
        type=["pdf", "txt", "doc", "docx"]
    )

    # Document content placeholder
    document_content = None

    if uploaded_file:
        try:
            document_content = process_document(uploaded_file)
            st.success("Document uploaded and processed successfully!")
            
            # Show document preview
            with st.expander("Document Preview"):
                st.text(document_content[:500] + "...")
            
            # Create columns for buttons
            col1, col2 = st.columns(2)
            
            # Project Update Button
            project_update_prompt = """
            Please provide a comprehensive project update in a clear and concise format. Analyze the document and extract/organize the following details:

            1. Employee Name
            2. Project Details:
               - Project Name
               - Project Description
            3. Project Problem Statement
            4. Resolution Strategy and Utilized Tools/Techniques
            5. Outcome and Value Adds

            Please present this information in a well-structured format, sequenced by high value to the organization. 
            Format the output using markdown tables for better readability.
            """
            
            with col1:
                if st.button("🎯 Project Update", type="primary"):
                    with st.spinner("Generating project update..."):
                        response = get_gemini_response(project_update_prompt, document_content)
                        st.subheader("Project Update Analysis")
                        st.markdown(response)
            
            # Custom Analysis Section
            with col2:
                if st.button("🔍 Custom Analysis", type="primary"):
                    st.session_state.show_custom = True

            if st.session_state.get('show_custom', False):
                # User prompt input
                user_prompt = st.text_area(
                    "Enter your question or analysis prompt:",
                    height=100,
                    placeholder="Example: Summarize the main points of this document\n"
                              "Or: What are the key findings in this document?\n"
                              "Or: Extract all dates mentioned in this document"
                )

                # Analysis button
                if st.button("Analyze", type="primary"):
                    if user_prompt:
                        with st.spinner("Analyzing document..."):
                            response = get_gemini_response(user_prompt, document_content)
                            st.subheader("Analysis Results")
                            st.write(response)
                    else:
                        st.warning("Please enter a prompt for analysis.")
                    
        except Exception as e:
            st.error(f"Error processing document: {str(e)}")
            
    else:
        st.info("Please upload a document to begin analysis.")

if __name__ == "__main__":
    main()