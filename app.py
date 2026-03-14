import streamlit as st
from groq import Groq
import os

# --- AUTHENTICATION ---
groq_key = st.secrets.get("GROQ_API_KEY")
if groq_key:
    client = Groq(api_key=groq_key)

# --- IMMERSIVE CINEMATIC UI ---
st.set_page_config(page_title="Auto Intelligence | Excellence", page_icon="🏎️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;800&display=swap');

    /* Full-Bleed Dark Theme */
    .stApp {
        background-color: #000000;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }

    /* Cinematic Hero Layout */
    .hero-container {
        padding-top: 80px;
        text-align: center;
        background: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,1) 100%);
    }
    .hero-title {
        font-size: 82px !important;
        font-weight: 800;
        letter-spacing: -3px;
        color: #ffffff;
        margin-bottom: 0px;
    }
    .hero-subtitle {
        color: #666;
        font-size: 18px;
        font-weight: 300;
        letter-spacing: 4px;
        text-transform: uppercase;
        margin-bottom: 60px;
    }

    /* High-Contrast Action Terminal */
    .terminal-card {
        background: #080808;
        border: 1px solid #1a1a1a;
        padding: 50px;
        margin-top: -20px;
    }

    /* Executive Price Metric */
    .metric-value {
        font-size: 100px;
        font-weight: 800;
        letter-spacing: -4px;
        text-align: center;
        margin-top: 40px;
    }
    .metric-label {
        color: #444;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-align: center;
        font-size: 14px;
    }

    /* Minimalist Technical Table */
    .spec-item {
        border-bottom: 1px solid #111;
        padding: 15px 0;
        display: flex;
        justify-content: space-between;
        color: #888;
    }
    .spec-val { color: #fff; font-weight: 600; }

    /* Stealth Form Inputs */
    input {
        background-color: #000 !important;
        border: 1px solid #222 !important;
        border-radius: 0px !important;
        color: white !important;
        padding: 12px !important;
    }
    .stButton>button {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 0px !important;
        font-weight: 700 !important;
        letter-spacing: 1px;
        height: 55px !important;
    }
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'home'

# --- PAGE: HOME (SHADED EXCELLENCE) ---
if st.session_state.page == 'home':
    st.markdown('<div class="hero-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="hero-title">Automotive Excellence</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Institutional Valuation Portal</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,5,1])
    with col2:
        # Shaded vehicle silhouette matching your reference
        st.image("https://images.unsplash.com/photo-1614162692292-7ac56d7f7f1e?auto=format&fit=crop&q=80&w=2000", use_container_width=True)
        st.markdown('<div style="height:50px;"></div>', unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns([1,1,1])
        with c2:
            if st.button("ENTER TERMINAL"):
                st.session_state.page = 'engine'
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE: ENGINE (THE DASHBOARD) ---
else:
    st.markdown('<div style="padding: 40px 0;"><h2 style="font-weight:800; letter-spacing:-1px; text-align:center;">MARKET ANALYSIS TERMINAL</h2></div>', unsafe_allow_html=True)
    
    col_main1, col_main2, col_main3 = st.columns([1,6,1])
    with col_main2:
        st.markdown('<div class="terminal-card">', unsafe_allow_html=True)
        with st.form("valuation_form"):
            c1, c2 = st.columns(2)
            with c1:
                make = st.text_input("MANUFACTURER", placeholder="e.g. Porsche")
                model_name = st.text_input("MODEL LINE", placeholder="e.g. 911 GT3")
                year = st.number_input("PRODUCTION YEAR", min_value=1950, max_value=2027, value=2024)
            with c2:
                trim = st.text_input("SPECIFICATION", placeholder="e.g. RS")
                miles = st.number_input("ODOMETER (MILES)", value=0)
                st.markdown('<div style="height:28px;"></div>', unsafe_allow_html=True)
                submit = st.form_submit_button("GENERATE REPORT")
        st.markdown('</div>', unsafe_allow_html=True)

        if submit:
            with st.spinner("Executing high-fidelity analysis..."):
                try:
                    # Model: Llama-3.3-70b-versatile for high precision
                    prompt = (
                        f"Professional Valuation: {year} {make} {model_name} {trim} with {miles} miles. "
                        "RULES: 1. Price is stable in 1,000-mile blocks. 2. Use institutional language.\n"
                        "FORMAT: PRICE: $[amount] | TREND: [UP/DOWN] | SUMMARY: [3 professional sentences]\n"
                        "DATA: [Engine] / [Horsepower] / [0-60 Time] / [Drive Type]"
                    )
                    
                    chat_completion = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model="llama-3.3-70b-versatile",
                    )
                    raw = chat_completion.choices[0].message.content

                    # Parsing for the new high-end layout
                    price = raw.split("|")[0].replace("PRICE:", "").strip()
                    trend = "UP" if "TREND: UP" in raw else "DOWN"
                    summary = raw.split("SUMMARY:")[1].split("DATA:")[0].strip()
                    data_points = raw.split("DATA:")[1].strip().split(" / ")

                    # Large Metric Display
                    st.markdown(f'<div class="metric-label">Estimated Market Value (USD)</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-value">{price}</div>', unsafe_allow_html=True)
                    st.markdown(f'<p style="text-align:center; color:#888;">MARKET DIRECTION: {"▲" if trend == "UP" else "▼"} {trend}</p>', unsafe_allow_html=True)
                    
                    st.markdown('<div style="height:50px;"></div>', unsafe_allow_html=True)
                    
                    # Split Detailed View
                    col_left, col_right = st.columns(2)
                    with col_left:
                        st.markdown('<h4 style="color:#666; font-size:12px; letter-spacing:2px;">TECHNICAL DATA</h4>', unsafe_allow_html=True)
                        labels = ["Engine Configuration", "Power Output", "Acceleration (0-60)", "Drivetrain"]
                        for label, val in zip(labels, data_points):
                            st.markdown(f'<div class="spec-item">{label} <span class="spec-val">{val}</span></div>', unsafe_allow_html=True)
                    
                    with col_right:
                        st.markdown('<h4 style="color:#666; font-size:12px; letter-spacing:2px;">EXECUTIVE SUMMARY</h4>', unsafe_allow_html=True)
                        st.write(summary)

                except Exception as e:
                    st.error(f"Analysis engine timeout: {e}")

    st.markdown('<div style="height:100px;"></div>', unsafe_allow_html=True)
    if st.button("TERMINATE SESSION"):
        st.session_state.page = 'home'
        st.rerun()

st.markdown('<p style="text-align:center; padding:60px; color:#222; font-size:10px; letter-spacing:5px;">© 2026 AUTO INTELLIGENCE | ENCRYPTED CHANNEL</p>', unsafe_allow_html=True)
