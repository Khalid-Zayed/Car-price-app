import streamlit as st
from groq import Groq
import os

# --- AUTHENTICATION ---
groq_key = st.secrets.get("GROQ_API_KEY")
if groq_key:
    client = Groq(api_key=groq_key)

# --- THE "AUTOMOTIVE EXCELLENCE" UIOverhaul ---
st.set_page_config(page_title="AutoIntelligence Pro", page_icon="🏎️", layout="wide")

st.markdown("""
    <style>
    /* Premium Executive Dark Mode */
    .stApp {
        background-color: #050505;
        background-image: 
            url("https://www.transparenttextures.com/patterns/carbon-fibre.png"),
            radial-gradient(circle at center, #1a0000 0%, #000000 100%);
        background-attachment: fixed;
    }

    /* Minimalist High-End Typography */
    .hero-title {
        font-family: 'Inter', -apple-system, sans-serif;
        font-size: 75px !important;
        font-weight: 800;
        text-align: center;
        color: #ffffff;
        letter-spacing: -2px;
        margin-top: 20px;
    }
    .hero-subtitle {
        text-align: center;
        color: #666;
        font-size: 18px;
        font-weight: 300;
        margin-bottom: 50px;
        letter-spacing: 1px;
    }

    /* Complex Detailing for Feature Paragraphs */
    .feature-text {
        color: #999;
        font-size: 15px;
        max-width: 600px;
        margin: 0 auto;
        padding: 20px;
        text-align: center;
        line-height: 1.8;
    }

    /* Pro Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 30px;
        backdrop-filter: blur(20px);
    }
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
    }

    /* Sleek Action Buttons */
    .stButton>button {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 4px !important;
        font-weight: bold !important;
        height: 55px !important;
        width: 100% !important;
    }
    .stButton>button:hover {
        background-color: #cccccc !important;
    }

    /* Terminal Fields: Pro Spacing */
    input {
        border-radius: 4px !important;
    }
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'home'

# --- PAGE: HOME (SINGLE VIEW - NO SCROLL) ---
if st.session_state.page == 'home':
    st.markdown('<div style="height:60px;"></div>', unsafe_allow_html=True)
    st.markdown('<h1 class="hero-title">Auto Intelligence</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Elite Automotive Market Analytics</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        # CDN Cadillac Escalade (Verified reliable link)
        st.image("https://images.unsplash.com/photo-1626012480088-34823ca86e0f?auto=format&fit=crop&q=80&w=1200", 
                 caption="2026 CADILLAC ESCALADE V-SERIES")
        st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
        if st.button("🏁 ACCESS QUANTUM ENGINE"):
            st.session_state.page = 'engine'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE: ENGINE TERMINAL (INPUT & REPORT) ---
else:
    if st.button("⬅️ DISCONNECT SESSION"):
        st.session_state.page = 'home'
        st.rerun()

    st.markdown('<h1 class="hero-title" style="font-size:45px !important; text-align:left;">QUANTUM TERMINAL</h1>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        with st.form("valuation_form"):
            c1, c2 = st.columns(2)
            with c1:
                make = st.text_input("Brand", value="", placeholder="e.g. Cadillac")
                model_name = st.text_input("Model", value="", placeholder="e.g. Escalade")
                year = st.number_input("Year", min_value=1950, max_value=2027, value=2024)
            with c2:
                trim = st.text_input("Spec/Trim", value="", placeholder="e.g. V-Series")
                miles = st.number_input("Mileage", value=0)
                submit = st.form_submit_button("🔥 EXECUTE MARKET SCAN")
        st.markdown('</div>', unsafe_allow_html=True)

    if submit:
        if not (make and model_name):
            st.warning("⚠️ CRITICAL: Data entry fields cannot be null.")
        else:
            with st.spinner("AI analyzing global market trends..."):
                try:
                    # UPDATED Prompt: Detects if car exists OR year is impossible.
                    prompt = (
                        f"Car Expert: Value this {year} {make} {model_name} {trim} with {miles} miles. "
                        "STRICT RULE 1: If car is FAKE, reply 'ERR: This vehicle does not exist.' "
                        "STRICT RULE 2: If year is IMPOSSIBLE (e.g. 2025 for a 2021 car), reply 'ERR: Latest was [Year]. Price for that model: PRICE: [Price] REASON: [Why].' "
                        "Otherwise, reply PRICE: $[number] REASON: [justification]."
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
                        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                        st.subheader("🏎️ Market Analysis Brief")
                        st.write(reason)
                        st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Engine connection failed: {e}")

st.markdown('<p style="text-align:center; padding:30px; color:#222; font-family:monospace;">>> [QUANTUM_LINK_ACTIVE] <<</p>', unsafe_allow_html=True)
