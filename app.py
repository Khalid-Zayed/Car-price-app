import streamlit as st
from groq import Groq
import os

# --- AUTHENTICATION ---
groq_key = st.secrets.get("GROQ_API_KEY")
if groq_key:
    client = Groq(api_key=groq_key)

# --- ULTRA-LUXURY CUSTOM CSS ---
st.set_page_config(page_title="AutoIntel Elite", page_icon="⬛", layout="wide")

st.markdown("""
    <style>
    /* Layered Background: Carbon Fiber Texture + Shards */
    .stApp {
        background-color: #050505;
        background-image: 
            radial-gradient(circle at 20% 30%, rgba(255, 0, 0, 0.05) 0%, transparent 40%),
            radial-gradient(circle at 80% 70%, rgba(255, 0, 0, 0.05) 0%, transparent 40%),
            url("https://www.transparenttextures.com/patterns/carbon-fibre.png");
        color: #ffffff;
    }

    /* Complex Neon Title */
    @keyframes neonPulse {
        from { text-shadow: 0 0 5px #ff0000, 0 0 10px #ff0000; }
        to { text-shadow: 0 0 20px #ff0000, 0 0 30px #ff0000, 0 0 5px #ffffff; }
    }
    .hero-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 85px !important;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(to bottom, #ffffff 30%, #ff0000 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: neonPulse 2s infinite alternate;
        letter-spacing: -5px;
        margin-bottom: 0px;
    }

    /* The "Complex" Card: Glassmorphism + Ruby Shards */
    .luxury-card {
        background: rgba(15, 15, 15, 0.85);
        border: 2px solid rgba(255, 0, 0, 0.4);
        border-radius: 25px;
        padding: 40px;
        backdrop-filter: blur(25px);
        box-shadow: 0 0 50px rgba(255, 0, 0, 0.15), inset 0 0 20px rgba(255, 0, 0, 0.05);
        position: relative;
        overflow: hidden;
    }
    
    /* Decorative Shard Elements */
    .luxury-card::before {
        content: ""; position: absolute; top: -50px; right: -50px; width: 100px; height: 100px;
        background: #ff0000; filter: blur(60px); opacity: 0.3;
    }

    /* Interactive Stealth Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #1a1a1a 0%, #330000 100%) !important;
        border: 1px solid #ff0000 !important;
        color: #ff0000 !important;
        font-weight: 900 !important;
        letter-spacing: 2px;
        text-transform: uppercase;
        border-radius: 5px !important;
        height: 65px !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .stButton>button:hover {
        background: #ff0000 !important;
        color: white !important;
        box-shadow: 0 0 40px #ff0000;
        transform: scale(1.03);
    }

    /* Price Display: Gold-Standard Polish */
    .price-display {
        font-size: 80px;
        font-weight: 900;
        color: #000000;
        background: linear-gradient(90deg, #ff0000, #ff6666);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 15px 35px rgba(255, 0, 0, 0.4);
        margin: 30px 0;
    }

    /* Cyber Ticker */
    @keyframes scroll { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    .ticker-bar {
        background: rgba(255, 0, 0, 0.1);
        border-top: 1px solid #ff0000;
        position: fixed; bottom: 0; left: 0; width: 100%; padding: 10px;
        overflow: hidden; white-space: nowrap; font-family: monospace;
    }
    .ticker-content { display: inline-block; animation: scroll 30s linear infinite; color: #ff4d4d; }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION LOGIC ---
if 'page' not in st.session_state: st.session_state.page = 'home'

# --- PAGE: HOME (LUXURY ENTRANCE) ---
if st.session_state.page == 'home':
    st.markdown('<div style="height:40px;"></div>', unsafe_allow_html=True)
    st.markdown('<h1 class="hero-title">AUTO INTELLIGENCE</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#ff4d4d; font-weight:bold; letter-spacing:5px;">ELITE MARKET QUANTIFICATION</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,4,1])
    with col2:
        st.markdown('<div class="luxury-card">', unsafe_allow_html=True)
        # 2026 Black Cadillac Escalade-V (Stealth Grill)
        st.image("https://images.unsplash.com/photo-1626012480088-34823ca86e0f?q=80&w=2070&auto=format&fit=crop", 
                 caption="2026 CADILLAC ESCALADE-V STEALTH")
        if st.button("🏁 INITIALIZE NEURAL ENGINE"):
            st.session_state.page = 'engine'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE: VALUATION ENGINE ---
else:
    if st.button("⬅️ TERMINATE SESSION"):
        st.session_state.page = 'home'
        st.rerun()

    st.markdown('<h1 class="hero-title" style="font-size:45px !important;">ENGINE TERMINAL</h1>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="luxury-card">', unsafe_allow_html=True)
        with st.form("elite_form"):
            c1, c2 = st.columns(2)
            with c1:
                make = st.text_input("MANUFACTURER")
                model_name = st.text_input("MODEL LINE")
                year = st.number_input("PRODUCTION YEAR", 1920, 2027, 2024)
            with c2:
                trim = st.text_input("TRIM / SPECIFICATION")
                miles = st.number_input("ODOMETER (MILES)", value=0)
                submit = st.form_submit_button("🔥 EXECUTE VALUATION")
        st.markdown('</div>', unsafe_allow_html=True)

    if submit:
        if not (make and model_name):
            st.warning("⚠️ CRITICAL ERROR: Incomplete vehicle data detected.")
        else:
            with st.spinner("Neural networks calculating market delta..."):
                try:
                    prompt = (
                        f"Expert Appraisal Engine: Check if {year} {make} {model_name} {trim} exists. "
                        "1. If FAKE/IMPOSSIBLE: Reply 'STATUS: INVALID MODEL. This vehicle does not exist in our reality.' "
                        "2. If YEAR MISMATCH (e.g. 2025 for a 2021 car): Reply 'STATUS: YEAR DISCREPANCY. Production for this model ceased in [Year]. Valuation for the final production year is: PRICE: [Price] REASON: [Why].' "
                        "3. If REAL: Reply 'PRICE: $[number] REASON: [justification]'. Use AMERICAN MARKET prices."
                    )
                    
                    chat_completion = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model="llama-3.3-70b-versatile",
                    )
                    response = chat_completion.choices[0].message.content

                    if "INVALID" in response or "DISCREPANCY" in response:
                        st.error(response)
                    elif "PRICE:" in response:
                        parts = response.split("REASON:")
                        price = parts[0].replace("PRICE:", "").strip()
                        reason = parts[1].strip() if len(parts) > 1 else ""

                        st.markdown(f'<div class="price-display">{price}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="luxury-card"><b>TECHNICAL JUSTIFICATION:</b><br>{reason}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Neural connection failure: {e}")

# --- CYBER TICKER ---
st.markdown("""
    <div class="ticker-bar">
        <div class="ticker-content">
            // LIVE_MARKET_UPDATE: Exotic resale values up 4.2% // SYSTEM_STATUS: Llama-3.3 Active // TRENDING: 2026 Escalade-V Stealth demand increasing // DATA_SYNC: Complete //
        </div>
    </div>
    """, unsafe_allow_html=True)
