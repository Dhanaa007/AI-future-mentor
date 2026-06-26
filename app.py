import streamlit as st
import requests
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

API_KEY = st.secrets["GEMINI_API_KEY"]

st.title("🚀 AI Future Me Mentor")
name = st.text_input("Name")
goal = st.text_input("Goal")
skills = st.text_input("Skills")
challenge = st.text_area("Challenge")
age = st.number_input("Age", 10, 100)

def get_ai_response(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(url, json=payload)
    return response.json()["candidates"][0]["content"]["parts"][0]["text"]

def create_pdf(text):
    path = "/tmp/roadmap.pdf"          # ✅ writable on Streamlit Cloud
    doc = SimpleDocTemplate(path)
    styles = getSampleStyleSheet()
    story = [Paragraph(text.replace("\n", "<br/>"), styles["Normal"])]
    doc.build(story)
    return path

if st.button("Generate Roadmap"):
    prompt = f"""You are an AI career mentor.
Name: {name}
Goal: {goal}
Skills: {skills}
Challenge: {challenge}
Age: {age}
Give:
- Career roadmap
- 30-day plan
- Skills to learn"""

    with st.spinner("Generating..."):
        result = get_ai_response(prompt)

    st.success("Done!")
    st.write(result)

    pdf_path = create_pdf(result)
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()
    st.download_button("Download PDF", pdf_bytes, file_name="roadmap.pdf")  # ✅