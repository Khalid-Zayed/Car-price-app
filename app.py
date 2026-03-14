import streamlit as st
from groq import Groq
import os

# --- AUTHENTICATION ---
groq_key = st.secrets.get("GROQ_API_KEY")
if groq_key:
    client = Groq(api_key=groq_key)

# --- NEON STEALTH UI & COMPLEX LAYERING ---
st.set_page_config(page_title="AutoIntel Pro", page_icon="🏎️", layout="wide")

st.markdown("""
    <style>
    /* Dark Background with Carbon Mesh & Neon Highlights */
    .stApp {
        background: radial-gradient(circle at center, #1a0000 0%, #000000 100%),
                    url("https://www.transparenttextures.com/patterns/carbon-fibre.png");
        color: #ffffff;
    }

    /* Vibrant Multi-Color Animated Title */
    @keyframes neonPulse {
        0% { text-shadow: 0 0 10px #00ff00; }
        50% { text-shadow: 0 0 20px #00ffff, 0 0 40px #ff0000; }
        100% { text-shadow: 0 0 10px #00ff00; }
    }
    .main-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 80px !important;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #00ff00, #00ffff, #ff0000);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: neonPulse 3s infinite alternate;
        letter-spacing: -3px;
    }

    /* Complex Detailing for Input Containers (Terminal View) */
    .glass-card {
        background: rgba(40, 40, 40, 0.7);
        border-radius: 20px;
        padding: 35px;
        border: 2px solid #00ff00;
        backdrop-filter: blur(15px);
        box-shadow: 0 0 30px rgba(0, 255, 0, 0.2);
    }

    /* High-Performance Stealth Button */
    .stButton>button {
        background: linear-gradient(90deg, #ff0000 0%, #800000 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        height: 55px !important;
        transition: 0.5s;
    }
    .stButton>button:hover {
        transform: scale(1.02) translateY(-2px);
        box-shadow: 0 0 25px #ff0000;
    }

    /* Market Valuation Price Result */
    .result-box {
        background: #ffffff;
        color: #000000;
        font-size: 70px;
        font-weight: 900;
        text-align: center;
        border-radius: 12px;
        padding: 20px;
        margin: 25px 0;
        border-left: 10px solid #ff0000;
    }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION CONTROLLER ---
if 'page' not in st.session_state: st.session_state.page = 'home'

# --- PAGE: HOME (NO SCROLLING LAYOUT) ---
if st.session_state.page == 'home':
    st.markdown('<div style="height:40px;"></div>', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">AUTO INTELLIGENCE</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#888;">ELITE AUTO ANALYTICS</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        # Blacked-out Cadillac Escalade (Direct image URL)
        st.image("https://images.unsplash.com/photo-1626012480088-34823ca86e0f?auto=format&fit=crop&q=80&w=1200", 
                 caption="2026 CADILLAC ESCALADE V-SERIES")
        
        if st.button("🏁 ACCESS NEURAL ENGINE"):
            st.session_state.page = 'engine'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE: QUANTUM TERMINAL (INPUT ENGINE) ---
else:
    if st.button("⬅️ DISCONNECT SESSION"):
        st.session_state.page = 'home'
        st.rerun()

    st.markdown('<h1 class="main-title" style="font-size:45px !important;">QUANTUM TERMINAL</h1>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        # Professional blank form
        with st.form("valuation_form"):
            c1, c2 = st.columns(2)
            with c1:
                make = st.text_input("MANUFACTURER", value="", placeholder="e.g. Cadillac, Ford")
                model_name = st.text_input("MODEL LINE", value="", placeholder="e.g. Escalade, Mustang")
                year = st.number_input("PRODUCTION YEAR", min_value=1950, max_value=2027, value=2024)
            with c2:
                trim = st.text_input("SPEC / TRIM", value="", placeholder="e.g. V-Series, Raptor")
                miles = st.number_input("TOTAL MILEAGE", value=0)
                submit = st.form_submit_button("🔥 EXECUTE MARKET SCAN")
        st.markdown('</div>', unsafe_allow_html=True)

    if submit:
        if not groq_key:
            st.error("🔑 KEY ERROR: Ensure GROQ_API_KEY is in Streamlit Secrets.")
        elif not (make and model_name):
            st.warning("⚠️ DATA ERROR: Please specify Manufacturer and Model.")
        else:
            with st.spinner("SCANNING REAL-TIME AUTOMOTIVE MARKETS..."):
                try:
                    # UPDATED Llama 3 Prompt: Added "Strict Reality Check" logic
                    prompt = (
                        f"Expert Car Appraiser: Market price for {year} {make} {model_name} {trim} with {miles} miles. "
                        "RULES:\n"
                        "1. If this car is FAKE or doesn't exist, reply only: 'REALITY CHECK: This vehicle does not exist.'\n"
                        "2. If the user input a year that is impossible (e.g. 2025 for a 2021 car), reply: 'ERR: This model ended in [Last Year]. Price for that model is: PRICE: [Price] REASON: [Why].'\n"
                        "3. Otherwise, reply: PRICE: $[number] REASON: [justification]."
                    )
                    
                    chat_completion = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model="llama-3.3-70b-versatile",
                    )
                    response = chat_completion.choices[0].message.content

                    if "REALITY CHECK" in response or "ERR:" in response:
                        st.error(response)
                    elif "PRICE:" in response:
                        parts = response.split("REASON:")
                        price = parts[0].replace("PRICE:", "").strip()
                        reason = parts[1].strip() if len(parts) > 1 else ""

                        st.markdown(f'<div class="result-box">{price}</div>', unsafe_allow_html=True)
                        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                        st.subheader("🏎️ Market Insights")
                        st.write(reason)
                        st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Engine connection failed: {e}")

st.markdown('<p style="text-align:center; padding:20px; color:#444;">>> [QUANTUM_LINK_ENCRYPTED] <<</p>', unsafe_allow_html=True)
