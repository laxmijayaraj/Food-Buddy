import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# App UI
st.set_page_config(page_title="Food Buddy", page_icon="🥗")
st.title("🥗 Food Buddy")
st.caption("Your AI-powered workout & diet assistant")

# Load .env locally
load_dotenv()

# Get API key from Streamlit Cloud or local .env
API_KEY = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))

if not API_KEY:
    st.error("GEMINI_API_KEY is missing. Add it in Streamlit Cloud → Settings → Secrets.")
    st.stop()

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# User input
user_profile = st.text_area(
    "Tell me about you (goal, food preference, allergies, time for exercise, budget):",
    placeholder="Example: Lose weight, vegetarian, no gluten, 30 minutes workout, low budget"
)

if st.button("Create My Plan"):
    if user_profile.strip() == "":
        st.warning("Please enter your details.")
    else:
        with st.spinner("Food Buddy is creating your plan..."):
            prompt = f"""
You are Food Buddy, an AI fitness and nutrition coach for students.

Based on the following student profile, generate:
1. A 7-day workout plan
2. A 1-day meal plan (budget-friendly)
3. Health & safety tips

Student profile:
{user_profile}
"""
            response = model.generate_content(prompt)
            st.subheader("Your Personalized Plan")
            st.write(response.text)
