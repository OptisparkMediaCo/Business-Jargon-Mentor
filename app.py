import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="n8n Workflow Simplifier", page_icon="⚡")
st.title("⚡ Unlimited n8n Workflow Simplifier")
st.write("Verify your student status, paste your n8n logic, and get instant explanations.")

# Paste your published Google Sheet CSV URL here
GOOGLE_SHEET_CSV_URL = "PASTE_YOUR_PUBLIC_GOOGLE_SHEET_CSV_URL_HERE"
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
student_input = st.text_area("Paste your n8n code/concept here:", height=200, placeholder="Example: {{ $json.body.id }} or paste raw node JSON...")

if st.button("Verify & Simplify Layout", type="primary"):
    authorized_students = get_authorized_emails()
    
    if not student_email:
        st.error("🔒 Please enter your registered course email to access this tool.")
    elif student_email not in authorized_students:
        st.error("❌ Access Denied. This email is not registered in our student database.")
    elif not student_input.strip():
        st.warning("Please paste some n8n text or code first!")
    else:
        with st.spinner("Analyzing your n8n setup..."):
            try:
                url = f"https://googleapis.com{GEMINI_API_KEY}"
                payload = {
                    "contents": [{
                        "parts": [{
                            "text": f"You are an expert n8n course assistant. Translate complex n8n workflows, expressions, or raw JSON code into beginner-friendly layman terms. Use clean markdown formatting, bold markers, and bullet points. Here is the n8n data: {student_input}"
                        }]
                    }]
                }
                response = requests.post(url, json=payload)
                if response.status_code == 200:
                    result_json = response.json()
                    ai_explanation = result_json['candidates'][0]['content']['parts'][0]['text']
                    st.success("Analysis Complete!")
                    st.markdown("### 📋 Plain English Breakdown")
                    st.markdown(ai_explanation)
                else:
                    st.error("The AI engine is temporarily busy. Please try clicking the button again.")
            except Exception as e:
                st.error(f"Could not reach the processing engine: {e}")
