import streamlit as st
from groq import Groq
import os

# --- AUTHENTICATION ---
groq_key = st.secrets.get("GROQ_API_KEY")
if groq_key:
    client = Groq(api_key=groq_key)

# --- ULTRA-VIBRANT CYBER-SHARD UI ---
st.set_page_config(page_title="AutoIntel Cyber", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    /* Layered Background: Dark Grid + Multi-Color Neon Shards */
    .stApp {
        background-color: #000000;
        background-image: 
            radial-gradient(circle at 10% 20%, rgba(0, 255, 0, 0.1) 0%, transparent 30%),
            radial-gradient(circle at 90% 80%, rgba(0, 255, 255, 0.1) 0%, transparent 30%),
            radial-gradient(circle at 50% 50%, rgba(255, 0, 0, 0.05) 0%, transparent 40%),
            url("https://www.transparenttextures.com/patterns/carbon-fibre.png");
        color: #ffffff;
    }

    /* Animated Cyber Title */
    @keyframes cyberGlow {
        0% { text-shadow: 0 0 10px #00ff00, 0 0 20px #00ffff; }
        50% { text-shadow: 0 0 20px #ff0000, 0 0 30px #ff0000; }
        100% { text-shadow: 0 0 10px #00ff00, 0 0 20px #00ffff; }
    }
    .main-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 80px !important;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #00ff00, #00ffff, #ff0000);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: cyberGlow 4s infinite;
        letter-spacing: -4px;
    }

    /* Complex Card: Glassmorphism + Tri-Neon Borders */
    .cyber-card {
        background: rgba(10, 10, 10, 0.9);
        border: 1px solid rgba(0, 255, 255, 0.3);
        border-radius: 20px;
        padding: 35px;
        backdrop-filter: blur(15px);
        box-shadow: 
            -10px -10px 30px rgba(0, 255, 0, 0.05), 
            10px 10px 30px rgba(0, 255, 255, 0.05),
            inset 0 0 20px rgba(255, 0, 0, 0.1);
        position: relative;
    }

    /* Buttons: Multi-Neon Gradient */
    .stButton>button {
        background: linear-gradient(45deg, #00ff00, #00ffff) !important;
        color: #000 !important;
        font-weight: 900 !important;
        border: none !important;
        height: 60px !important;
        border-radius: 5px !important;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.4);
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: #ff0000 !important;
        color: white !important;
        box-shadow: 0 0 30px #ff0000;
        transform: translateY(-2px);
    }

    /* Valuation Output */
    .valuation-box {
        font-size: 60px;
        font-weight: 900;
        text-align: center;
        padding: 20px;
        border-radius: 12px;
        background: #ffffff;
        color: #000000;
        border-left: 10px solid #00ff00;
        border-right: 10px solid #ff0000;
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'home'

# --- PAGE: HOME (BUGATTI RE-ENTRY) ---
if st.session_state.page == 'home':
    st.markdown('<h1 class="main-title">AUTO INTELLIGENCE</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#00ffff; font-family:monospace;">SYST_LOG: NEURAL_VALUATION_ACTIVE</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,4,1])
    with col2:
        st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
        # Re-inserted Bugatti Image (Verified reliable URL)
        st.image("https://images.unsplash.com/photo-1614162692292-7ac56d7f7f1e?auto=format&fit=crop&q=80&w=2000", caption="AUTO_INTEL_SYSTEM_ENTRY")
        if st.button("🏁 EXECUTE SYSTEM INITIALIZATION"):
            st.session_state.page = 'engine'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE: ENGINE TERMINAL ---
else:
    if st.button("⬅️ DISCONNECT_SESSION"):
        st.session_state.page = 'home'
        st.rerun()

    st.markdown('<h1 class="main-title" style="font-size:45px !important;">VALUATION ENGINE</h1>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
        with st.form("valuation_form"):
            c1, c2 = st.columns(2)
            with c1:
                make = st.text_input("BRAND (e.g., Ferrari, Toyota)", value="")
                model_name = st.text_input("MODEL (e.g., Roma, Supra)", value="")
                year = st.number_input("PRODUCTION YEAR", 1920, 2027, 2024)
            with c2:
                trim = st.text_input("SPEC/TRIM (e.g., V8, TRD)", value="")
                miles = st.number_input("TOTAL MILES", value=0)
                submit = st.form_submit_button("🔥 INITIATE AI MARKET SCAN")
        st.markdown('</div>', unsafe_allow_html=True)

    if submit:
        if not (make and model_name):
            st.warning("⚠️ DATA_ENTRY_NULL: Please provide car identification.")
        else:
            with st.spinner("AI ANALYZING MARKET EXISTENCE..."):
                try:
                    prompt = (
                        f"Car expert analysis for: {year} {make} {model_name} {trim} with {miles} miles. "
                        "RULES: "
                        "1. If FAKE/IMPOSSIBLE: Reply 'STATUS: INVALID_VEHICLE. This model is not a production vehicle.' "
                        "2. If YEAR MISMATCH (e.g. 2025 for a 2021 car): Reply 'STATUS: OUT_OF_SYNC. Latest model was [Year]. Valuation for that model is: PRICE: [Price] REASON: [Why].' "
                        "3. If REAL: Reply 'PRICE: $[number] REASON: [justification]'. USE AMERICAN PRICES."
                    )
                    
                    chat_completion = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model="llama-3.3-70b-versatile",
                    )
                    response = chat_completion.choices[0].message.content

                    if "INVALID_VEHICLE" in response or "OUT_OF_SYNC" in response:
                        st.error(response)
                    elif "PRICE:" in response:
                        parts = response.split("REASON:")
                        price = parts[0].replace("PRICE:", "").strip()
                        reason = parts[1].strip() if len(parts) > 1 else ""

                        st.markdown(f'<div class="valuation-box">{price}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="cyber-card"><b>DATA SUMMARY:</b><br>{reason}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Neural connection error: {e}")

st.markdown('<p style="text-align:center; padding:30px; color:#333; font-family:monospace;">>> [SYSTEM_V.3.1_GREEN_CYAN_RED_ENABLED] <<</p>', unsafe_allow_html=True)
