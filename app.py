import streamlit as st
import PyPDF2
import os
from groq import Groq

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# App title
st.title("🎯 AI Resume Analyzer")
st.write("Upload your resume and get instant honest feedback!")

# PDF upload button
uploaded_file = st.file_uploader("Upload Resume (PDF only)", type="pdf")

if uploaded_file:
    # Extract text from the PDF
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    resume_text = ""
    for page in pdf_reader.pages:
        resume_text += page.extract_text()

    st.success("Resume uploaded successfully! ✅")

    # Analyze button
    if st.button("Analyze My Resume 🔍"):
        with st.spinner("Analyzing your resume..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{
                    "role": "user",
                    "content": f"""You are a senior hiring manager at a top AI company.
                    Analyze this resume and give feedback on:
                    1. What's strong 💪
                    2. What's weak ⚠️
                    3. What's missing ❌
                    4. Top 3 improvements to make immediately 🚀
                    
                    Resume: {resume_text}"""
                }]
            )
        
        st.markdown(response.choices[0].message.content)