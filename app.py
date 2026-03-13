import streamlit as st
import google.generativeai as genai
import os
import pandas as pd
import joblib

# --- 1. API SETUP ---
# Works for both local (.env) and Streamlit Cloud (Secrets)
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# --- 2. STYLING ---
st.set_page_config(page_title="AutoIntelligence AI", page_icon="🏎️")
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .price-display { 
        background: linear-gradient(90deg, #00d2ff, #3a7bd5); 
        padding: 30px; border-radius: 15px; text-align: center; 
        font-size: 45px; font-weight: bold; margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. NAVIGATION LOGIC ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- PAGE: HOME ---
if st.session_state.page == 'home':
    st.markdown("<h1 style='text-align:center; font-size:60px;'>🏎️ AutoIntelligence</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>The most accurate AI-driven car valuation tool in 2026.</p>", unsafe_allow_html=True)
    st.write("---")
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        # A nice placeholder image for the home screen
        st.image("https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&q=80&w=1000")
        if st.button("🚀 Estimate Now!", use_container_width=True):
            st.session_state.page = 'engine'
            st.rerun()

# --- PAGE: VALUATION ENGINE ---
else:
    if st.button("⬅️ Back to Home"):
        st.session_state.page = 'home'
        st.rerun()

    st.title("🔍 Deep Market Analysis")
    
    with st.form("main_form"):
        c1, c2 = st.columns(2)
        with c1:
            make = st.selectbox("Select Agency", ["Toyota", "Volkswagen", "BMW", "Ford", "Honda", "Tesla", "Mercedes-Benz", "Audi", "Nissan", "Chevrolet"])
            model_name = st.text_input("Model", placeholder="e.g. Tiguan")
            year = st.number_input("Year", 2010, 2027, 2023)
        with c2:
            trim = st.text_input("Trim Level", placeholder="e.g. Trendline, SE, GT")
            miles = st.number_input("Odometer (Miles)", value=40000)
            submit = st.form_submit_button("RUN AI VALUATION")

    if submit:
        if not api_key:
            st.error("API Key missing! Please add GEMINI_API_KEY to Streamlit Secrets.")
        elif not model_name or not trim:
            st.warning("Please enter the Model and Trim for an accurate search.")
        else:
            with st.spinner("Gemini AI is analyzing current market listings..."):
                try:
                    # 1. Ask Gemini for the numeric price
                    ai_model = genai.GenerativeModel('gemini-1.5-flash')
                    price_prompt = f"As a professional US auto appraiser, provide ONLY the estimated current market price (as a plain number, no symbols or text) for a {year} {make} {model_name} {trim} with {miles} miles. Use 2026 market data."
                    price_response = ai_model.generate_content(price_prompt).text.strip()
                    
                    # 2. Ask Gemini for the justification
                    desc_prompt = f"In exactly two sentences, explain why a {year} {make} {model_name} {trim} with {miles} miles is priced at ${price_response} in today's market."
                    desc_response = ai_model.generate_content(desc_prompt).text

                    # Clean the price string in case Gemini adds a '$' or ','
                    clean_price = "".join(filter(str.isdigit, price_response))
                    formatted_price = f"{int(clean_price):,}"

                    st.markdown(f'<div class="price-display">${formatted_price}</div>', unsafe_allow_html=True)
                    st.subheader("🤖 AI Market Justification")
                    st.info(desc_response)
                except Exception as e:
                    st.error(f"Analysis failed: {e}")
