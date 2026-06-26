import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# ---------------- LOAD ENV ----------------
load_dotenv()

# ---------------- API ----------------
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ---------------- SESSION MEMORY ----------------
if "reports" not in st.session_state:
    st.session_state.reports = []

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Future Me Mentor",
    page_icon="🚀",
    layout="centered"
)

# ---------------- SIDEBAR ----------------
st.sidebar.title("Menu")
page = st.sidebar.radio("Go to", ["Home", "Reports"])

# ---------------- PDF FUNCTION ----------------
def create_pdf(text):
    doc = SimpleDocTemplate("Future_Roadmap.pdf")
    styles = getSampleStyleSheet()
    story = [Paragraph(text.replace("\n", "<br/>"), styles["Normal"])]
    doc.build(story)

# ================= HOME PAGE =================
if page == "Home":

    st.title("🚀 AI Future Me Mentor")
    st.subheader("Turn your dreams into a practical roadmap")

    st.write("Fill in your details and get your AI career plan")

    st.divider()

    # ---------------- INPUTS ----------------
    name = st.text_input("Enter your Name")
    goal = st.text_input("What is your biggest Goal?")
    skills = st.text_input("What skills do you already have?")
    challenge = st.text_area("What is your biggest challenge?")
    age = st.number_input("🎂 Enter your Age", min_value=10, max_value=100)
    education = st.selectbox("🎓 Current Education", ["School", "Diploma", "B.E/B.Tech", "B.Sc", "M.E/M.Tech", "Other"])
    dream_company = st.text_input("🏢 Dream Company")
    study_hours = st.slider("📚 Study Hours per Day", 1, 12, 2)
    skill_level = st.selectbox("⭐ Current Skill Level", ["Beginner", "Intermediate", "Advanced"])
    three_year_goal = st.text_area("Where do you see yourself in 3 years?")

    st.divider()

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

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

        st.success("Your AI Roadmap is Ready!")

        st.markdown("## Your AI Mentor Says")
        st.write(response.text)

        # SAVE REPORT
        st.session_state.reports.append(response.text)

        # CREATE PDF
        create_pdf(response.text)

        with open("Future_Roadmap.pdf", "rb") as pdf:
            st.download_button(
                "📄 Download My Roadmap",
                pdf,
                file_name="Future_Roadmap.pdf",
                mime="application/pdf"
            )

# ================= REPORTS PAGE =================
if page == "Reports":

    st.title("📜 Previous Reports")

    if len(st.session_state.reports) == 0:
        st.write("No reports yet.")
    else:
        for i, r in enumerate(st.session_state.reports, 1):
            st.markdown(f"### Report {i}")
            st.write(r)
            st.divider()

# ---------------- FOOTER ----------------
st.caption("Made with ❤️ using Streamlit")