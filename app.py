import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import json
from datetime import datetime

# --- 1. SETUP ---
client_groq = Groq(api_key=st.secrets["GROQ_API_KEY"])
conn = st.connection("gsheets", type=GSheetsConnection)

st.set_page_config(page_title="Run&Drive Admin", layout="centered")

# --- 2. CSS (STAYS THE SAME) ---
st.markdown("""
    <style>
    /* All your custom CSS for the green button and focus goes here */
    div.stButton > button:first-child { background-color: #32cd32 !important; color: #000 !important; font-weight: 900 !important; }
    .stat-card { background: #ffffff; padding: 25px; border-radius: 15px; border-bottom: 5px solid #32cd32; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. THE UI ---
brand = st.text_input("Car Brand")
model = st.text_input("Car Model")
trim = st.text_input("Trim / Version (Optional)")
year = st.number_input("Year", min_value=1900, max_value=2026, value=2024)
miles = st.number_input("Miles", min_value=0, value=0)

if st.button("RUN LIVE VALUATION"): #
    with st.spinner("Processing..."):
        # 1. Clean the Trim
        clean_trim = trim.strip() if trim else ""
        full_name = f"{year} {brand} {model} {clean_trim}".strip().replace("  ", " ")
        
        try:
            # 2. AI VALUATION LOGIC
            prompt = f"Verify and value {full_name} at {miles} miles. Return JSON: {{'exists': true/false, 'price': 'USD', 'why': 'logic'}}"
            res = client_groq.chat.completions.create(
                messages=[{"role":"user","content":prompt}],
                model="llama-3.3-70b-versatile",
                temperature=0.1
            ).choices[0].message.content
            data = json.loads(res.strip())

            if not data.get("exists"):
                st.error("Invalid vehicle data.")
            else:
                # --- 3. THE FIX: SIMPLIFIED APPEND ---
                try:
                    log_entry = pd.DataFrame([{
                        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Brand": brand,
                        "Model": model,
                        "Trim": clean_trim,
                        "Year": year,
                        "Miles": miles,
                        "Price_Estimate": data["price"],
                        "AI_Logic": data["why"]
                    }])
                    
                    # This simple 'append' logic is less likely to fail than 'read-then-update'
                    conn.create(data=log_entry) 
                    st.toast("Admin Log Updated!")
                except:
                    st.warning("Result generated, but Admin Log sync failed.")

                # 4. SHOW RESULTS
                st.markdown(f"### {full_name}")
                st.markdown(f'<div class="stat-card"><h1>{data["price"]}</h1></div>', unsafe_allow_html=True)

        except Exception as e:
            st.error("Connection error. Please try again.")
