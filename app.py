import streamlit as st
from groq import Groq
import os

# --- AUTHENTICATION ---
groq_key = st.secrets.get("GROQ_API_KEY")
if groq_key:
    client = Groq(api_key=groq_key)

# --- CINEMATIC AUTOMOTIVE UI ---
st.set_page_config(page_title="Auto Intelligence | Excellence", page_icon="🏎️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;800&display=swap');

    .stApp {
        background-color: #000000;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }

    .hero-title {
        font-size: 72px !important;
        font-weight: 800;
        text-align: center;
        color: #ffffff;
        letter-spacing: -2px;
        margin-bottom: 0px;
        padding-top: 50px;
    }
    .hero-subtitle {
        text-align: center;
        color: #888;
        font-size: 20px;
        font-weight: 300;
        margin-bottom: 50px;
        letter-spacing: 1px;
    }

    .card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 0px;
        padding: 40px;
        backdrop-filter: blur(20px);
        margin-bottom: 25px;
    }

    .price-wrap {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 30px;
        margin: 40px 0;
    }
    .price-val {
        font-size: 85px;
        font-weight: 800;
        color: #ffffff;
    }
    .trend-tag {
        font-size: 18px;
        padding: 8px 16px;
        border: 1px solid rgba(255,255,255,0.2);
        font-weight: 600;
        letter-spacing: 1px;
    }

    .stButton>button {
        background-color: transparent !important;
        color: #ffffff !important;
        border: 1px solid #ffffff !important;
        border-radius: 0px !important;
        font-weight: 400 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        height: 60px !important;
        width: 100% !important;
    }
    .stButton>button:hover {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    input {
        background-color: #000 !important;
        border: 1px solid #333 !important;
        color: white !important;
        border-radius: 0px !important;
    }
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'home'

# --- PAGE: HOME ---
if st.session_state.page == 'home':
    st.markdown('<h1 class="hero-title">Automotive Excellence</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">High-fidelity market quantification for exclusive marques.</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,4,1])
    with col2:
        st.image("https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&q=80&w=2000")
        st.markdown('<div style="height:40px;"></div>', unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            if st.button("Initialize Terminal"):
                st.session_state.page = 'engine'
                st.rerun()

# --- PAGE: ENGINE ---
else:
    st.markdown('<div style="padding: 20px;"><h1 style="font-weight:800; letter-spacing:-1px;">VALUATION TERMINAL</h1></div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        with st.form("valuation_form"):
            c1, c2 = st.columns(2)
            with c1:
                make = st.text_input("MANUFACTURER", placeholder="e.g. Porsche")
                model_name = st.text_input("MODEL LINE", placeholder="e.g. 911 GT3")
                year = st.number_input("PRODUCTION YEAR", min_value=1950, max_value=2027, value=2024)
            with c2:
                trim = st.text_input("SPECIFICATION", placeholder="e.g. Touring")
                miles = st.number_input("ODOMETER (MILES)", value=0)
                st.markdown('<div style="height:28px;"></div>', unsafe_allow_html=True)
                submit = st.form_submit_button("EXECUTE ANALYSIS")
        st.markdown('</div>', unsafe_allow_html=True)

    if submit:
        with st.spinner("Analyzing market and technical specifications..."):
            try:
                # INTEGRATED SPEC SHEET PROMPT
                prompt = (
                    f"Expert Automotive Analyst: Value and spec a {year} {make} {model_name} {trim} with {miles} miles. "
                    "STRICT STABILITY RULES:\n"
                    "1. PRICE STABILITY: Only change price in 1,000-mile tiers. No changes for small gaps.\n"
                    "2. FORMAT: Respond exactly like this:\n"
                    "PRICE: $[amount] | TREND: [UP/DOWN] | BRIEF: [3 sentence summary]\n"
                    "SPECS: [Engine type] / [Horsepower] / [0-60 MPH] / [Drivetrain]"
                )
                
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile",
                )
                res = chat_completion.choices[0].message.content

                # Parsing
                price = res.split("|")[0].replace("PRICE:", "").strip()
                trend = "UP" if "TREND: UP" in res else "DOWN"
                brief = res.split("BRIEF:")[1].split("SPECS:")[0].strip()
                specs = res.split("SPECS:")[1].strip()

                st.markdown(f'''
                    <div class="price-wrap">
                        <div class="price-val">{price}</div>
                        <div class="trend-tag">{"▲" if trend == "UP" else "▼"} {trend} MARKET</div>
                    </div>
                ''', unsafe_allow_html=True)
                
                col_spec, col_brief = st.columns([1, 2])
                with col_spec:
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown('### Technical Specs')
                    for s in specs.split(" / "):
                        st.write(f"⁃ {s}")
                    st.markdown('</div>', unsafe_allow_html=True)
                with col_brief:
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown('### Executive Summary')
                    st.write(brief)
                    st.markdown('</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Analysis failed: {e}")

    if st.button("← TERMINATE SESSION"):
        st.session_state.page = 'home'
        st.rerun()

st.markdown('<p style="text-align:center; padding:60px; color:#333; font-size:11px; letter-spacing:3px;">© 2026 AUTO INTELLIGENCE | PRIVATE SECTOR PORTAL</p>', unsafe_allow_html=True)
