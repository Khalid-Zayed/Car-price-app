import streamlit as st
from groq import Groq
import os

# --- AUTHENTICATION ---
groq_key = st.secrets.get("GROQ_API_KEY")
if groq_key:
    client = Groq(api_key=groq_key)

# --- NEON STEALTH UI ---
st.set_page_config(page_title="AutoIntelligence Pro", page_icon="⬛", layout="wide")

st.markdown("""
    <style>
    /* Dark Carbon & Red Gradient */
    .stApp {
        background: radial-gradient(circle at top right, #1a1a1a, #000000);
        color: #ffffff;
    }

    /* Animated Title */
    @keyframes glow { 0% { text-shadow: 0 0 10px #ff0000; } 100% { text-shadow: 0 0 30px #ff0000, 0 0 10px #ffffff; } }
    .main-title {
        font-size: 70px !important;
        font-weight: 900;
        text-align: center;
        color: #ff0000;
        animation: glow 2s infinite alternate;
        letter-spacing: -2px;
        margin-bottom: 5px;
    }

    /* Glassmorphism Cards with Red Border */
    .glass-card {
        background: rgba(40, 40, 40, 0.6);
        border-radius: 20px;
        padding: 35px;
        border: 1px solid rgba(255, 0, 0, 0.3);
        backdrop-filter: blur(15px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    /* Stealth Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #ff0000 0%, #800000 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-size: 20px !important;
        font-weight: bold !important;
        height: 60px !important;
        transition: 0.5s ease;
    }
    .stButton>button:hover { transform: translateY(-3px); box-shadow: 0 0 25px #ff0000; }

    /* Price Box */
    .price-box {
        background: #ffffff;
        color: #000000;
        font-size: 65px;
        font-weight: 900;
        text-align: center;
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        border-left: 10px solid #ff0000;
    }
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'home'

# --- PAGE: HOME ---
if st.session_state.page == 'home':
    st.markdown('<div style="height:50px;"></div>', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">AUTO INTELLIGENCE</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#888;">THE ULTIMATE CAR VALUATION SYSTEM</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,3,1])
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        # Black Cadillac Escalade-V Front View
        st.image("https://images.unsplash.com/photo-1626012480088-34823ca86e0f?auto=format&fit=crop&q=80&w=1200", caption="2026 ESCALADE-V STEALTH EDITION")
        if st.button("🏁 ACCESS ENGINE"):
            st.session_state.page = 'engine'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE: VALUATION ENGINE ---
else:
    if st.button("⬅️ DISCONNECT"):
        st.session_state.page = 'home'
        st.rerun()

    st.markdown('<h1 class="main-title" style="font-size:40px !important;">VALUATION ENGINE</h1>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        with st.form("valuation_form"):
            c1, c2 = st.columns(2)
            with c1:
                make = st.text_input("BRAND", placeholder="e.g. Cadillac, Ford")
                model_name = st.text_input("MODEL", placeholder="e.g. Escalade, Mustang")
                year = st.number_input("YEAR", 1900, 2027, 2024)
            with c2:
                trim = st.text_input("TRIM / SPEC", placeholder="e.g. V-Series, Raptor")
                miles = st.number_input("MILES", value=0)
                submit = st.form_submit_button("🔥 ANALYZE MARKET")
        st.markdown('</div>', unsafe_allow_html=True)

    if submit:
        if not groq_key:
            st.error("Authentication Error: API Key Missing.")
        elif not (make and model_name):
            st.warning("Data Required: Please enter car details.")
        else:
            with st.spinner("AI ANALYZING MARKET EXISTENCE & PRICING..."):
                try:
                    # UPDATED PROMPT: Added strict logic for non-existent cars and year checking
                    prompt = (
                        f"You are a professional US car market expert. User wants a valuation for: {year} {make} {model_name} {trim} with {miles} miles. "
                        "RULES:\n"
                        "1. If this car model is FAKE or doesn't exist in real life, reply ONLY: 'REALITY CHECK: This car does not exist in the real world.'\n"
                        "2. If the user input a year that is impossible (e.g. 2025 for a car that ended in 2021), reply: 'UPDATE: The latest year for this car is [Latest Year]. Here is the price for that model instead: PRICE: [Price] REASON: [Explain why].'\n"
                        "3. If the car is real (ignore minor spelling mistakes), give the valuation. Format: PRICE: $[number] REASON: [justification].\n"
                        "4. Focus on the AMERICAN market only."
                    )
                    
                    chat_completion = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model="llama-3.3-70b-versatile",
                    )
                    response = chat_completion.choices[0].message.content

                    if "REALITY CHECK" in response:
                        st.error(response)
                    elif "UPDATE:" in response:
                        st.info(response)
                    elif "PRICE:" in response:
                        parts = response.split("REASON:")
                        price = parts[0].replace("PRICE:", "").strip()
                        reason = parts[1].strip() if len(parts) > 1 else ""

                        st.markdown(f'<div class="price-box">{price}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="glass-card"><b>MARKET ANALYSIS:</b><br>{reason}</div>', unsafe_allow_html=True)
                    else:
                        st.write(response)
                except Exception as e:
                    st.error(f"Engine connection failed: {e}")

st.markdown('<p style="text-align:center; padding:20px; color:#444;">© 2026 AUTO INTELLIGENCE | ENCRYPTED LINK ACTIVE</p>', unsafe_allow_html=True)
