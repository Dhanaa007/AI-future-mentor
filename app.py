import streamlit as st
from google import genai
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# ---------------- API (STREAMLIT SECRETS) ----------------
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# ---------------- PAGE ----------------
st.set_page_config(
    page_title="AI Future Me Mentor",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 AI Future Me Mentor")
st.subheader("Build your personalized career roadmap with AI")

st.divider()

# ---------------- INPUTS ----------------
name = st.text_input("Enter your Name")
goal = st.text_input("What is your biggest Goal?")
skills = st.text_input("Skills you already have")
challenge = st.text_area("Biggest Challenge")
age = st.number_input("Age", 10, 100)
education = st.selectbox("Education", ["School", "Diploma", "B.Tech", "B.Sc", "M.Tech", "Other"])
dream_company = st.text_input("Dream Company")
study_hours = st.slider("Study Hours per day", 1, 12, 2)
skill_level = st.selectbox("Skill Level", ["Beginner", "Intermediate", "Advanced"])
three_year_goal = st.text_area("Where do you see yourself in 3 years?")

st.divider()

# ---------------- PDF FUNCTION ----------------
def create_pdf(text):
    doc = SimpleDocTemplate("roadmap.pdf")
    styles = getSampleStyleSheet()
    story = [Paragraph(text.replace("\n", "<br/>"), styles["Normal"])]
    doc.build(story)

# ---------------- BUTTON ----------------
if st.button("🚀 Generate Roadmap"):

    with st.spinner("AI is thinking..."):

        prompt = f"""
You are an AI Career Mentor.

Name: {name}
Goal: {goal}
Skills: {skills}
Challenge: {challenge}
Age: {age}
Education: {education}
Dream Company: {dream_company}
Study Hours: {study_hours}
Skill Level: {skill_level}
3-Year Goal: {three_year_goal}

Give:
1. Career Vision
2. 30-Day Plan
3. Weekly Study Plan
4. Skills to Learn
5. Daily Routine
6. Mistakes to Avoid
7. Motivation
8. Certifications
9. Career Advice
"""

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

    st.success("Generated Successfully!")

    st.write(response.text)

    create_pdf(response.text)

    with open("roadmap.pdf", "rb") as f:
        st.download_button(
            "📄 Download PDF",
            f,
            file_name="roadmap.pdf",
            mime="application/pdf"
        )