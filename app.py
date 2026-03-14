import streamlit as st
from groq import Groq
import os

# --- AUTHENTICATION ---
groq_key = st.secrets.get("GROQ_API_KEY")
if groq_key:
    client = Groq(api_key=groq_key)

# --- THE "ELITE NEON SHARD" INTERFACE ---
st.set_page_config(page_title="AutoIntel Elite", page_icon="🏎️", layout="wide")

st.markdown("""
    <style>
    /* COMPLEX DYNAMIC BACKGROUND: Green, Cyan, and Red Shards */
    .stApp {
        background-color: #000000;
        background-image: 
            url("https://www.transparenttextures.com/patterns/carbon-fibre.png"),
            linear-gradient(135deg, rgba(0, 255, 0, 0.07) 0%, transparent 25%),
            linear-gradient(225deg, rgba(0, 255, 255, 0.07) 0%, transparent 25%),
            linear-gradient(45deg, rgba(255, 0, 0, 0.05) 0%, transparent 25%);
        background-attachment: fixed;
    }

    /* Vibrant Multi-Neon Title */
    @keyframes neonPulse {
        0% { text-shadow: 0 0 10px #00ff00; }
        50% { text-shadow: 0 0 20px #00ffff, 0 0 40px #ff0000; }
        100% { text-shadow: 0 0 10px #00ff00; }
    }
    .main-title {
        font-size: 85px !important;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(to right, #00ff00, #00ffff, #ff0000);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: neonPulse 3s infinite;
        letter-spacing: -4px;
        margin-top: -20px;
    }

    /* Complex Glassmorphism Card */
    .glass-panel {
        background: rgba(10, 10, 10, 0.85);
        border: 1px solid rgba(0, 255, 255, 0.3);
        border-top: 3px solid #ff0000;
        border-bottom: 3px solid #00ff00;
        border-radius: 30px;
        padding: 40px;
        backdrop-filter: blur(20px);
        box-shadow: 0 0 50px rgba(255, 0, 0, 0.1);
    }

    /* High-Tech Action Button */
    .stButton>button {
        background: linear-gradient(90deg, #1a1a1a, #000000) !important;
        color: #00ffff !important;
        border: 2px solid #00ffff !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        font-size: 20px !important;
        width: 100% !important;
        height: 65px !important;
        transition: 0.4s;
    }
    .stButton>button:hover {
        background: #00ffff !important;
        color: #000 !important;
        box-shadow: 0 0 40px #00ffff;
        transform: scale(1.02);
    }

    /* Digital Result Box */
    .result-display {
        background: #ffffff;
        color: #000000;
        font-size: 70px;
        font-weight: 900;
        text-align: center;
        border-radius: 15px;
        padding: 20px;
        border-left: 12px solid #00ff00;
        border-right: 12px solid #ff0000;
        margin-top: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'home'

# --- PAGE: HOME ---
if st.session_state.page == 'home':
    st.markdown('<div style="height:60px;"></div>', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">AUTO INTELLIGENCE</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,3,1])
    with col2:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        # Verified Bugatti Link
        st.image("https://images.unsplash.com/photo-1614162692292-7ac56d7f7f1e?auto=format&fit=crop&q=80&w=1200")
        if st.button("🏁 ACCESS QUANTUM ENGINE"):
            st.session_state.page = 'engine'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE: ENGINE ---
else:
    if st.button("⬅️ TERMINATE LINK"):
        st.session_state.page = 'home'
        st.rerun()

    st.markdown('<h1 class="main-title" style="font-size:45px !important;">QUANTUM TERMINAL</h1>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        with st.form("valuation_form"):
            c1, c2 = st.columns(2)
            with c1:
                make = st.text_input("MANUFACTURER")
                model_name = st.text_input("MODEL LINE")
                year = st.number_input("YEAR", 1920, 2027, 2024)
            with c2:
                trim = st.text_input("SPECIFICATION")
                miles = st.number_input("TOTAL MILEAGE", value=0)
                submit = st.form_submit_button("🔥 EXECUTE MARKET SCAN")
        st.markdown('</div>', unsafe_allow_html=True)

    if submit:
        if not (make and model_name):
            st.warning("⚠️ CRITICAL: Missing identification strings.")
        else:
            with st.spinner("AI scanning reality for vehicle existence..."):
                try:
                    prompt = (
                        f"Professional US Auto Expert: Check {year} {make} {model_name} {trim}. "
                        "1. If REALITY CHECK: If car is FAKE, reply 'ERR: NON-EXISTENT MODEL.' "
                        "2. If YEAR ERROR: If car year is wrong (e.g. 2025 for a 2021 car), reply 'ERR: PRODUCTION MISMATCH. Latest was [Year]. Price for that model: PRICE: [Price] REASON: [Why].' "
                        "3. If REAL: Reply 'PRICE: $[number] REASON: [justification]'. USE US PRICES ONLY."
                    )
                    chat_completion = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model="llama-3.3-70b-versatile",
                    )
                    response = chat_completion.choices[0].message.content

                    if "ERR:" in response:
                        st.error(response)
                    elif "PRICE:" in response:
                        parts = response.split("REASON:")
                        price = parts[0].replace("PRICE:", "").strip()
                        reason = parts[1].strip() if len(parts) > 1 else ""

                        st.markdown(f'<div class="result-display">{price}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="glass-panel"><b>DATA_DUMP:</b><br>{reason}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Engine connection failed: {e}")
