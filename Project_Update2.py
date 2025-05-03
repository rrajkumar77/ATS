import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variable
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("❌ GOOGLE_API_KEY not found in .env file.")
else:
    genai.configure(api_key=api_key)

# === BRAND COLORS ===
BRAND_BG = "#F5F5F5"
BRAND_TITLE = "#012A52"
BRAND_TEXT = "#00798B"

# === Function to format summary output ===
def format_summary(title, summary_html):
    return f"""
    <div style="background-color:{BRAND_BG}; padding: 20px; border-radius: 12px; margin-bottom: 25px;">
        <h3 style="color:{BRAND_TITLE}; font-family:sans-serif;">{title}</h3>
        <div style="color:{BRAND_TEXT}; font-size: 16px; font-family:sans-serif;">{summary_html}</div>
    </div>
    """

# === Function to call Gemini API ===
def get_project_summary(text):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")  # ✅ correct model name
        prompt = (
            "Summarize the following employee QBR project inputs into 4-5 concise bullet points. "
            "Include project names, goals, achievements, and value delivered. Use <ul><li> HTML tags for output:\n\n"
        )
        response = model.generate_content(prompt + text)
        return response.text
    except Exception as e:
        return f"<p style='color:red;'>Error: {str(e)}</p>"

# === Streamlit UI ===
st.set_page_config(page_title="QBR Summary Generator", layout="centered")
st.title("📊 QBR Project Summary Generator")

uploaded_file = st.file_uploader("Upload the Pedro QBR CSV file", type=["csv"])

if uploaded_file is not None:
    with st.spinner("Processing..."):
        df = pd.read_csv(uploaded_file)

        # Convert date and extract Quarter
        df["Period_From"] = pd.to_datetime(df["Period_From"], errors="coerce")
        df["Quarter"] = df["Period_From"].dt.to_period("Q").astype(str)  # '2025Q1'

        # Group by employee and quarter
        grouped = df.groupby(["Created By", "Quarter"])

        for (employee_name, quarter), group_df in grouped:
            # Combine entries into one text
            text_chunks = []
            for _, row in group_df.iterrows():
                team_lead = row.get("Team_Lead", "")
                project_name = row.get("Project_Name", "")
                project_desc = row.get("Project_Description", "")
                achievements = row.get("Acheivements_ValueAdds", "")
                value_add = row.get("Value_Add", "")

                chunk = f"""
                Team Lead: {team_lead}
                Project Name: {project_name}
                Project Description: {project_desc}
                Achievements: {achievements}
                Value Add: {value_add}
                """
                text_chunks.append(chunk)

            combined_text = "\n\n".join(text_chunks)

            summary_html = get_project_summary(combined_text)
            section_title = f"{employee_name} - {quarter}"
            formatted_output = format_summary(section_title, summary_html)
            st.markdown(formatted_output, unsafe_allow_html=True)
