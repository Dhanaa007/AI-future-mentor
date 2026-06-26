import streamlit as st
import google.generativeai as genai
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# ---------------- API CONFIG ----------------
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

# ---------------- SESSION STATE ----------------
if "reports" not in st.session_state:
    st.session_state.reports = []

# ---------------- PAGE SETUP ----------------
st.set_page_config(
    page_title="AI Future Me Mentor",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 AI Future Me Mentor")
st.subheader("Build your career roadmap with AI")

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
    doc = SimpleDocTemplate("Future_Roadmap.pdf")
    styles = getSampleStyleSheet()
    story = [Paragraph(text.replace("\n", "<br/>"), styles["Normal"])]
    doc.build(story)

# ---------------- BUTTON ----------------
if st.button("🚀 Generate Future Advice"):

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

Generate:
1. Future Vision
2. 30-Day Roadmap
3. Weekly Plan
4. Skills to Learn
5. Daily Routine
6. Mistakes to Avoid
7. Motivation
8. Certifications
9. Career Advice
"""

        response = model.generate_content(prompt)

    st.success("Your Roadmap is Ready!")

    st.write(response.text)

    st.session_state.reports.append(response.text)

    create_pdf(response.text)

    with open("Future_Roadmap.pdf", "rb") as pdf:
        st.download_button(
            "📄 Download PDF",
            pdf,
            file_name="Future_Roadmap.pdf",
            mime="application/pdf"
        )

# ---------------- REPORTS ----------------
st.divider()

st.subheader("📜 Previous Reports")

if st.session_state.reports:
    for i, r in enumerate(st.session_state.reports, 1):
        st.markdown(f"### Report {i}")
        st.write(r)
        st.divider()
else:
    st.write("No reports yet.")

# ---------------- FOOTER ----------------
st.caption("Made with ❤️ using Streamlit")