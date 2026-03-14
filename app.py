import streamlit as st
from groq import Groq
import os

# --- AUTHENTICATION ---
groq_key = st.secrets.get("GROQ_API_KEY")
if groq_key:
    client = Groq(api_key=groq_key)

# --- EXECUTIVE STEALTH UI ---
st.set_page_config(page_title="AutoIntelligence Pro", page_icon="🏎️", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #050505;
        background-image: 
            url("https://www.transparenttextures.com/patterns/carbon-fibre.png"),
            radial-gradient(circle at center, #1a0000 0%, #000000 100%);
    }

    .main-title {
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 65px !important;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, #00ff00, #00ffff, #ff0000);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -2px;
        margin-top: 10px;
    }

    .glass-card {
        background: rgba(30, 30, 30, 0.5);
        border-radius: 15px;
        padding: 30px;
        border: 1px solid rgba(0, 255, 0, 0.2);
        backdrop-filter: blur(10px);
    }
    
    .result-tag {
        font-size: 60px;
        font-weight: 900;
        color: #000000;
        background: #ffffff;
        text-align: center;
        border-radius: 8px;
        padding: 15px;
        margin-top: 25px;
        border-left: 10px solid #00ff00;
    }

    .stButton>button {
        background: linear-gradient(90deg, #ff0000, #800000) !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: bold !important;
        height: 55px !important;
        width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'home'

# --- PAGE: HOME ---
if st.session_state.page == 'home':
    st.markdown('<div style="height:50px;"></div>', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">Auto Intelligence Pro</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,3,1])
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        # Reliable Hero Image (Porsche 911)
        st.image("https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&q=80&w=1200")
        
        if st.button("🏁 Access Valuation Engine"):
            st.session_state.page = 'engine'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE: ENGINE ---
else:
    if st.button("⬅️ Disconnect Session"):
        st.session_state.page = 'home'
        st.rerun()

    st.markdown('<h1 class="main-title" style="font-size:40px !important;">Valuation Terminal</h1>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        with st.form("valuation_form"):
            c1, c2 = st.columns(2)
            with c1:
                make = st.text_input("Brand", value="", placeholder="e.g. Porsche")
                model_name = st.text_input("Model", value="", placeholder="e.g. 911 Turbo")
                year = st.number_input("Year", min_value=1960, max_value=2027, value=2024)
            with c2:
                trim = st.text_input("Trim / Spec", value="", placeholder="e.g. S, Heritage Edition")
                miles = st.number_input("Mileage", value=0)
                submit = st.form_submit_button("🔥 Analyze Market Value")
        st.markdown('</div>', unsafe_allow_html=True)

    if submit:
        if not (make and model_name):
            st.warning("Please enter car details.")
        else:
            with st.spinner("Analyzing market data..."):
                try:
                    # PROMPT: Explicit instructions for brief and mileage scaling
                    prompt = (
                        f"Provide a market valuation for a {year} {make} {model_name} {trim} with {miles} miles. "
                        "FORMAT YOUR RESPONSE EXACTLY LIKE THIS:\n"
                        "PRICE: [Price in USD]\n"
                        "BRIEF: [A 3-sentence professional summary of this specific car's rarity, "
                        "how the mileage of {miles} specifically affected this price, and its resale outlook.]"
                    )
                    
                    chat_completion = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model="llama-3.3-70b-versatile",
                    )
                    response = chat_completion.choices[0].message.content

                    if "PRICE:" in response:
                        parts = response.split("BRIEF:")
                        price = parts[0].replace("PRICE:", "").strip()
                        brief = parts[1].strip() if len(parts) > 1 else "Analysis complete."

                        st.markdown(f'<div class="result-tag">{price}</div>', unsafe_allow_html=True)
                        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                        st.subheader("Professional Brief")
                        st.write(brief)
                        st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Engine connection failed: {e}")

st.markdown('<p style="text-align:center; padding:20px; color:#333;">© 2026 Auto Intelligence | Professional Grade</p>', unsafe_allow_html=True)
