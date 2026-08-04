import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Business & Automation Simplifier", page_icon="⚡")
st.title("⚡ Unlimited Business & Tech Simplifier")
st.write("Verify your student email, paste any business jargon or n8n code, and get a simple breakdown!")

# 1. Configured Google Sheets CSV Endpoint
GOOGLE_SHEET_CSV_URL = "https://google.com"
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

@st.cache_data(ttl=60)
def get_authorized_emails():
    try:
        df = pd.read_csv(GOOGLE_SHEET_CSV_URL)
        return set(df['Email'].astype(str).str.lower().str.strip())
    except Exception as e:
        st.error("System Error: Unable to verify student database configuration.")
        return set()

student_email = st.text_input("Registered Course Email:", placeholder="student@example.com").strip().lower()
student_input = st.text_area("Paste your business jargon, corporate buzzwords, or n8n code here:", height=200, placeholder="Example: ARR, B2B, Webhook, or raw node JSON...")

if st.button("Verify & Simplify Layout", type="primary"):
    authorized_students = get_authorized_emails()
    
    if not student_email:
        st.error("🔒 Please enter your registered course email to access this tool.")
    elif student_email not in authorized_students:
        st.error("❌ Access Denied. This email is not registered in our student database.")
    elif not student_input.strip():
        st.warning("Please paste some text or code first!")
    else:
        with st.spinner("Analyzing and simplifying..."):
            try:
                url = f"https://googleapis.com{GEMINI_API_KEY}"
                
                # High school targeted translation instruction prompt
                instruction = (
                    "You are an elite Business & Automation Mentor speaking directly to high school students. "
                    "Your objective is to take complex business jargon, corporate buzzwords, tech slang, or n8n workflow logic "
                    "and explain it using simple English, high school vocabulary, and highly relatable everyday analogies "
                    "(like gaming, sports, social media, school projects, or part-time jobs).\n\n"
                    "CRITICAL STYLE RULES:\n"
                    "- Ban all corporate fluff. Do not use words like 'synergy', 'leveraging', or 'optimization' without translating them first.\n"
                    "- Break down concepts step-by-step using bullet points and bold visual anchors.\n"
                    "- Use a friendly, encouraging, and peer-like tone—never sound like a rigid textbook.\n\n"
                    f"Here is the term or code the student needs broken down: {student_input}"
                )
                
                payload = {
                    "contents": [{
                        "parts": [{
                            "text": instruction
                        }]
                    }]
                }
                
                response = requests.post(url, json=payload)
                if response.status_code == 200:
                    result_json = response.json()
                    ai_explanation = result_json['candidates']['content']['parts']['text']
                    st.success("Analysis Complete!")
                    st.markdown("### 📋 Plain English Breakdown")
                    st.markdown(ai_explanation)
                else:
                    st.error("The AI engine is temporarily busy. Please try clicking the button again.")
            except Exception as e:
                st.error(f"Could not reach the processing engine: {e}")
