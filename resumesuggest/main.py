from email import message
import streamlit as st
import PyPDF2
import io
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Resume Suggest", page_icon="page", layout="centered", initial_sidebar_state="auto")

st.title("RESUME AI SUGGEST")
st.markdown("""Upload your resume and let AI suggest improvements.""")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

uploaded_file = st.file_uploader("Upload your resume", type=["pdf"])

job_role = st.text_input("Enter the job role")

analyze = st.button("Analyze Resume")

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    
    return uploaded_file.read().decode("utf-8")


if analyze and uploaded_file:
    try:
        file_content = extract_text_from_file(uploaded_file)
        if not file_content.strip():
            st.error("File Does Not Have Content")
            st.stop()

        prompt = f"""Please analyze the resume and suggest improvements for the job role of {job_role}. 
        
        Resume Content: 
        {file_content}
        
        """ 

        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create( 
            model="gpt-3.5-turbo",
            messages = [
                {"role": "system", "content": "You are a resume analysis assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature = 0.7,
            max_tokens = 1000,
        ) 
        st.markdown("### Analysis Result")
        st.markdown(response.choices[0].message.content)  
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}") 
            
        
