import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("❌ GOOGLE_API_KEY not set in your .env file.")
else:
    genai.configure(api_key=api_key)

# Get current month and previous month
current_date = datetime.now()
current_month = current_date.strftime("%B")  # Full month name
previous_month = datetime(current_date.year, current_date.month - 1 if current_date.month > 1 else 12, 1).strftime("%B")

# Format bullet points using Gemini with appropriate tense
def format_bullet_points(text, is_past_month):
    try:
        # Convert to string and handle NaN/None values
        if pd.isna(text) or text is None:
            return "No data available"
        
        # Ensure text is a string
        text_str = str(text)
        if text_str.strip() == "":
            return "No data available"
            
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        if is_past_month:
            prompt = f"""
            Summarize these completed tasks/achievements in 3-4 concise bullet points using past tense. 
            Format each bullet point with a • symbol.
            Keep each bullet point under 15 words if possible.
            Start each bullet point on a new line.
            Do not use any HTML tags.
            """
        else:
            prompt = f"""
            Summarize these planned tasks in 3-4 concise bullet points using STRICTLY future tense ONLY.
            Every bullet point MUST start with "Will" or a similar future-indicating phrase.
            Examples of correct formats:
            • Will deliver medical dashboard to production.
            • Will implement new features for client portal.
            • Planning to complete documentation review.
            
            Format each bullet point with a • symbol.
            Keep each bullet point under 15 words if possible.
            Start each bullet point on a new line.
            Do not use any HTML tags or past tense verbs.
            """
            
        response = model.generate_content([prompt + "\n\n" + text_str])
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="QBR Table Generator", layout="wide")
st.title("📊 QBR Project Table Generator")
st.subheader(f"Generate a table for PowerPoint presentations ({previous_month}/{current_month} Update)")

# Option to override automatic month detection
with st.expander("Month Settings (Optional)"):
    use_custom_months = st.checkbox("Override automatic month detection")
    if use_custom_months:
        col1, col2 = st.columns(2)
        with col1:
            previous_month = st.selectbox("Previous Month", [
                "January", "February", "March", "April", "May", "June", 
                "July", "August", "September", "October", "November", "December"
            ], index=["January", "February", "March", "April", "May", "June", 
                "July", "August", "September", "October", "November", "December"].index(previous_month))
        with col2:
            current_month = st.selectbox("Current Month", [
                "January", "February", "March", "April", "May", "June", 
                "July", "August", "September", "October", "November", "December"
            ], index=["January", "February", "March", "April", "May", "June", 
                "July", "August", "September", "October", "November", "December"].index(current_month))

uploaded_file = st.file_uploader("Upload the QBR CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File uploaded successfully!")
        
        # Check if required columns exist
        required_columns = ["Created By", "Acheivements_ValueAdds", "Plans_for_Current_Month"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            st.error(f"❌ Missing required columns: {', '.join(missing_columns)}")
        else:
            # Handle any NaN values in the dataframe
            df = df.fillna("")
            for col in required_columns:
                if df[col].dtype not in [str, object]:
                    df[col] = df[col].astype(str)
            
            # Process the data
            with st.spinner(f"Processing data and generating {previous_month}/{current_month} table..."):
                # Create a new dataframe for the table
                table_data = pd.DataFrame()
                
                # Convert 'Created By' column to string and add to table data
                df["Created By"] = df["Created By"].astype(str)
                table_data["Consultant"] = df["Created By"]
                
                # Process previous month tasks (achievements) - PAST TENSE
                st.info(f"Generating {previous_month} tasks summaries (past tense)...")
                progress_bar1 = st.progress(0)
                prev_month_tasks = []
                total_rows = len(df["Acheivements_ValueAdds"])
                
                for i, task in enumerate(df["Acheivements_ValueAdds"]):
                    task_bullets = format_bullet_points(task, is_past_month=True)
                    prev_month_tasks.append(task_bullets)
                    progress_bar1.progress((i + 1) / total_rows)
                
                table_data[f"Project/Main tasks ({previous_month})"] = prev_month_tasks
                
                # Process current month tasks (plans) - FUTURE TENSE
                st.info(f"Generating {current_month} tasks summaries (future tense)...")
                progress_bar2 = st.progress(0)
                curr_month_tasks = []
                
                for i, plan in enumerate(df["Plans_for_Current_Month"]):
                    plan_bullets = format_bullet_points(plan, is_past_month=False)
                    curr_month_tasks.append(plan_bullets)
                    progress_bar2.progress((i + 1) / total_rows)
                
                table_data[f"Project/Main tasks ({current_month})"] = curr_month_tasks
                
                # Display the table
                st.markdown("### Generated Table")
                st.dataframe(
                    table_data,
                    column_config={
                        "Consultant": st.column_config.TextColumn("Consultant", width="medium"),
                        f"Project/Main tasks ({previous_month})": st.column_config.TextColumn(f"Project/Main tasks ({previous_month})", width="large"),
                        f"Project/Main tasks ({current_month})": st.column_config.TextColumn(f"Project/Main tasks ({current_month})", width="large")
                    },
                    use_container_width=True,
                    hide_index=True
                )
                
                # Export to CSV option
                csv = table_data.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "Download Table as CSV",
                    csv,
                    f"qbr_table_{previous_month}_{current_month}.csv",
                    "text/csv",
                    key='download-csv'
                )
                
                # Instructions for PowerPoint
                st.info("""
                **How to add this to PowerPoint:**
                1. Select the table above and copy (Ctrl+C)
                2. In PowerPoint, paste (Ctrl+V) into your slide
                3. Alternatively, download the CSV and import it into PowerPoint
                """)
                
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
        st.error(f"Detailed error: {str(e)}")