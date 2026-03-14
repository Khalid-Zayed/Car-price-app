import streamlit as st
from groq import Groq
import os

# --- AUTHENTICATION ---
# Ensure you have GROQ_API_KEY saved in Streamlit Secrets
groq_key = st.secrets.get("GROQ_API_KEY")
if groq_key:
    client = Groq(api_key=groq_key)

# --- EXECUTIVE STEALTH UI & LAYERING ---
st.set_page_config(page_title="AutoIntelligence Pro", page_icon="🏎️", layout="wide")

st.markdown("""
    <style>
    /* Clean Dark Gradient Background with Carbon Mesh */
    .stApp {
        background-color: #050505;
        background-image: 
            url("https://www.transparenttextures.com/patterns/carbon-fibre.png"),
            radial-gradient(circle at center, #1a0000 0%, #000000 100%);
    }

    /* Refined Animated Case Title */
    @keyframes subtleGlow {
        0% { text-shadow: 0 0 10px #00ff00; }
        100% { text-shadow: 0 0 20px #00ffff, 0 0 40px #ff0000; }
    }
    .main-title {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 70px !important;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, #00ff00, #00ffff, #ff0000);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: subtleGlow 4s infinite alternate;
        letter-spacing: -2px;
        margin-top: 10px;
    }

    /* Professional, Thin Input Containers */
    .glass-card {
        background: rgba(40, 40, 40, 0.4);
        border-radius: 12px;
        padding: 30px;
        border: 1px solid rgba(0, 255, 0, 0.2);
        backdrop-filter: blur(15px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    /* Result Box Styling */
    .result-tag {
        font-size: 65px;
        font-weight: 900;
        color: #000000;
        background: #ffffff;
        text-align: center;
        border-radius: 8px;
        padding: 15px;
        margin-top: 30px;
        border-left: 10px solid #ff0000;
    }

    /* Refined Button */
    .stButton>button {
        background: linear-gradient(90deg, #ff0000, #800000) !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: bold !important;
        font-size: 18px !important;
        width: 100% !important;
        height: 60px !important;
        transition: 0.5s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 25px #ff0000; }
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'home'

# --- PAGE: HOME ---
if st.session_state.page == 'home':
    st.markdown('<div style="height:60px;"></div>', unsafe_allow_html=True)
    # Corrected capitalization
    st.markdown('<h1 class="main-title">Auto Intelligence Pro</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#888;">Executive market quantification for the discerning collector.</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,3,1])
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        # Dirty Porsche 911 GT3 in snow landscape
        st.image("https://images.unsplash.com/photo-1544636331-e26879cd4d9b?auto=format&fit=crop&q=80&w=1200")
        
        # Action button (Caps removed)
        if st.button("🏁 Access Valuation Engine"):
            st.session_state.page = 'engine'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE: ENGINE TERMINAL ---
else:
    # Action button (Caps removed)
    if st.button("⬅️ Disconnect Session"):
        st.session_state.page = 'home'
        st.rerun()

    st.markdown('<h1 class="main-title" style="font-size:45px !important;">Valuation Terminal</h1>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        # Form has blank fields for professional input
        with st.form("valuation_form"):
            c1, c2 = st.columns(2)
            with c1:
                make = st.text_input("Brand", value="", placeholder="e.g. Porsche, Ferrari")
                model_name = st.text_input("Model Line", value="", placeholder="e.g. 911 GT3 RS, Roma")
                year = st.number_input("Year", min_value=1950, max_value=2027, value=2024)
            with c2:
                trim = st.text_input("Specification / Trim", value="", placeholder="e.g. Weissach, Carbon")
                miles = st.number_input("Odometer (Miles)", value=0)
                submit = st.form_submit_button("🔥 Execute Market Analysis")
        st.markdown('</div>', unsafe_allow_html=True)

    if submit:
        if not groq_key:
            st.error("Engine failure: API Key not detected in Streamlit Secrets.")
        elif not (make and model_name):
            st.warning("Data mismatch: Brand and Model inputs cannot be null.")
        else:
            with st.spinner("AI scanning real-time automotive markets..."):
                try:
                    # UPDATED Prompt: Detects if the model exists OR if the user's year is impossible.
                    prompt = (
                        f"Professional car appraiser: valuation for {year} {make} {model_name} {trim} with {miles} miles. "
                        "RULES:\n"
                        "1. If this car is FAKE and doesn't exist, reply exactly: 'REALITY CHECK: This model does not exist.'\n"
                        "2. If the model is real but that YEAR is impossible (e.g. 2025 for a car that ended in 2021), reply: 'UPDATE: The latest year for this car is [Latest Year]. Price for that model is: PRICE: [Price] REASON: [Why].'\n"
                        "3. Otherwise, reply PRICE: $[number] REASON: [justification]."
                    )
                    
                    chat_completion = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model="llama-3.3-70b-versatile",
                    )
                    response = chat_completion.choices[0].message.content

                    if "REALITY CHECK" in response or "UPDATE:" in response:
                        st.error(response)
                    elif "PRICE:" in response:
                        parts = response.split("REASON:")
                        price = parts[0].replace("PRICE:", "").strip()
                        reason = parts[1].strip() if len(parts) > 1 else ""

                        st.markdown(f'<div class="result-tag">{price}</div>', unsafe_allow_html=True)
                        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                        st.subheader("🏎️ Market Insights")
                        st.write(reason)
                        st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Engine connection failed: {e}")

st.markdown('<p style="text-align:center; padding:20px; color:#333;">© 2026 Auto Intelligence | Proprietary Algorithms Active</p>', unsafe_allow_html=True)
