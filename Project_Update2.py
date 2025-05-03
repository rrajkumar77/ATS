import numpy as np

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded!")

    # Convert Period_From to datetime and extract Quarter
    df["Period_From"] = pd.to_datetime(df["Period_From"], errors="coerce")
    df["Quarter"] = df["Period_From"].dt.to_period("Q").astype(str)  # e.g., '2025Q1'

    # Group by employee and quarter
    grouped = df.groupby(["Created By", "Quarter"])

    for (employee_name, quarter), group_df in grouped:
        # Combine text fields across the grouped rows
        text_chunks = []
        for _, row in group_df.iterrows():
            project_name = row.get("Project_Name", "")
            project_desc = row.get("Project_Description", "")
            achievements = row.get("Acheivements_ValueAdds", "")
            value_add = row.get("Value_Add", "")
            team_lead = row.get("Team_Lead", "")
            
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
