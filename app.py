import streamlit as st
import google.generativeai as genai
import os

# --- API SETUP ---
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# --- ADVANCED UI & ANIMATIONS ---
st.set_page_config(page_title="AutoIntelligence Pro", page_icon="🏎️", layout="wide")

st.markdown("""
    <style>
    /* Background & Global Font */
    .stApp {
        background: radial-gradient(circle at center, #1a0505 0%, #000000 100%);
        color: #ffffff;
    }

    /* Vibrant Red Title Animation */
    @keyframes glow {
        from { text-shadow: 0 0 10px #ff0000, 0 0 20px #ff0000; }
        to { text-shadow: 0 0 20px #ff4d4d, 0 0 30px #ff4d4d; }
    }
    
    .main-title {
        font-size: 70px !important;
        font-weight: 900;
        text-align: center;
        color: #ff0000;
        animation: glow 1.5s ease-in-out infinite alternate;
        letter-spacing: -2px;
    }

    /* Professional Glass Cards with Red Border */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px;
        padding: 40px;
        border: 1px solid rgba(255, 0, 0, 0.2);
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease, border 0.3s ease;
    }
    .glass-card:hover {
        transform: translateY(-5px);
        border: 1px solid rgba(255, 0, 0, 0.6);
    }

    /* Red Vibrant Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #ff0000 0%, #990000 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 15px 30px !important;
        font-weight: bold !important;
        font-size: 18px !important;
        transition: 0.4s !important;
        width: 100% !important;
    }
    .stButton>button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 0 25px rgba(255, 0, 0, 0.8) !important;
    }

    /* Price Display Styling */
    .price-box {
        background: #ff0000;
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-size: 55px;
        font-weight: 900;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(255, 0, 0, 0.4);
    }

    /* Transitions for inputs */
    input {
        background-color: rgba(255,255,255,0.05) !important;
        border-color: rgba(255,0,0,0.3) !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'home'

# --- PAGE: HOME ---
if st.session_state.page == 'home':
    st.markdown('<div style="height:100px;"></div>', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">AUTO INTELLIGENCE</h1>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:1.2rem; opacity:0.8;'>Elite Valuation Powered by Gemini AI</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.image("https://images.unsplash.com/photo-1544636331-e26879cd4d9b?q=80&w=1000&auto=format&fit=crop")
        if st.button("🏁 START ESTIMATING"):
            st.session_state.page = 'engine'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE: VALUATION ENGINE ---
else:
    if st.button("⬅️ EXIT ENGINE"):
        st.session_state.page = 'home'
        st.rerun()

    st.markdown('<h1 class="main-title" style="font-size:40px !important;">VALUATION ENGINE</h1>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        with st.form("main_form"):
            c1, c2 = st.columns(2)
            with c1:
                make = st.text_input("MANUFACTURER", placeholder="e.g. Porsche, Tesla, Toyota")
                model_name = st.text_input("MODEL", placeholder="e.g. 911 GT3, Model S, Supra")
                year = st.number_input("YEAR", 1950, 2027, 2023)
            with c2:
                trim = st.text_input("TRIM / SPECIFICATION", placeholder="e.g. Turbo S, Plaid, Premium")
                miles = st.number_input("MILEAGE", value=15000)
                submit = st.form_submit_button("🔥 ANALYZE MARKET VALUE")
        st.markdown('</div>', unsafe_allow_html=True)

    if submit:
        if not api_key:
            st.error("SYSTEM ERROR: Gemini API Key Missing.")
        elif not (make and model_name):
            st.warning("FIELD ERROR: Manufacturer and Model are required.")
        else:
            with st.spinner("QUANTUM ENGINE ANALYZING MARKET DATA..."):
                try:
                    ai_model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = (f"Act as a professional high-end car appraiser in 2026. "
                              f"For a {year} {make} {model_name} {trim} with {miles} miles, "
                              f"provide the fair market value as a number first, "
                              f"followed by a short, technical market justification. "
                              f"Format: PRICE: [number] REASON: [text]")
                    
                    response = ai_model.generate_content(prompt).text
                    price_part = response.split("REASON:")[0].replace("PRICE:", "").strip()
                    reason_part = response.split("REASON:")[1].strip()

                    clean_price = "".join(filter(str.isdigit, price_part))
                    formatted_price = f"{int(clean_price):,}"

                    st.markdown(f'<div class="price-box">${formatted_price}</div>', unsafe_allow_html=True)
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.subheader("🏎️ MARKET INSIGHT")
                    st.write(reason_part)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error("Engine failure. Please check details and try again.")
