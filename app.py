import streamlit as st
import requests

API_KEY = st.secrets["GROQ_API_KEY"]

st.title("🚀 AI Future Me Mentor")
name = st.text_input("Name")
goal = st.text_input("Goal")
skills = st.text_input("Skills")
challenge = st.text_area("Challenge")
age = st.number_input("Age", 10, 100)

def get_ai_response(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]

if st.button("Generate Roadmap"):
    if not name or not goal:
        st.warning("Please fill in Name and Goal!")
        st.stop()

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

    st.download_button(
        "Download as TXT",
        result,
        file_name="roadmap.txt",
        mime="text/plain"
    )