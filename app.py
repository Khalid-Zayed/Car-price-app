import streamlit as st
import google.generativeai as genai
import os

# --- AUTHENTICATION ---
# Ensure your key AIzaSyBkIQ2bkm7i0nh0LNxQa_YLiZkFBtuHCjY is in Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# --- VIBRANT RED UI & ANIMATIONS ---
st.set_page_config(page_title="AutoIntelligence Pro", page_icon="🏎️", layout="wide")

st.markdown("""
    <style>
    /* Dark Background with Red Highlights */
    .stApp {
        background: radial-gradient(circle at center, #2a0000 0%, #000000 100%);
        color: #ffffff;
    }

    /* Red Pulsing Title */
    @keyframes pulse { 0% { opacity: 0.8; } 100% { opacity: 1; text-shadow: 0 0 30px #ff0000; } }
    .main-title {
        font-size: 75px !important;
        font-weight: 900;
        text-align: center;
        color: #ff0000;
        animation: pulse 1.5s infinite alternate;
        letter-spacing: -3px;
    }

    /* Red Shard Glass Cards */
    .glass-card {
        background: rgba(255, 0, 0, 0.05);
        border-radius: 15px;
        padding: 30px;
        border: 1px solid #ff0000;
        backdrop-filter: blur(10px);
        transition: 0.3s ease;
    }
    .glass-card:hover {
        background: rgba(255, 0, 0, 0.1);
        box-shadow: 0 0 40px rgba(255, 0, 0, 0.3);
    }

    /* Professional Red Buttons */
    .stButton>button {
        background: linear-gradient(45deg, #ff0000, #660000) !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 18px !important;
        width: 100% !important;
        height: 55px !important;
        border: none !important;
        border-radius: 8px !important;
        transition: 0.4s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 20px #ff0000; }

    /* Price Result Styling */
    .price-tag {
        font-size: 70px;
        font-weight: 900;
        color: #ff0000;
        text-align: center;
        background: white;
        border-radius: 12px;
        padding: 15px;
        margin: 25px 0;
    }
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'home'

# --- PAGE: HOME ---
if st.session_state.page == 'home':
    st.markdown('<div style="height:80px;"></div>', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">AUTO INTELLIGENCE</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.image("https://images.unsplash.com/photo-1544636331-e26879cd4d9b?auto=format&fit=crop&q=80&w=1000")
        if st.button("🏁 ENTER SYSTEM"):
            st.session_state.page = 'engine'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE: VALUATION ENGINE ---
else:
    if st.button("⬅️ EXIT"):
        st.session_state.page = 'home'
        st.rerun()

    st.markdown('<h1 class="main-title" style="font-size:45px !important;">VALUATION ENGINE</h1>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        with st.form("main_form"):
            c1, c2 = st.columns(2)
            with c1:
                make = st.text_input("BRAND")
                model_name = st.text_input("MODEL")
                year = st.number_input("YEAR", 1950, 2027, 2023)
            with c2:
                trim = st.text_input("TRIM / EDITION")
                miles = st.number_input("MILES", value=10000)
                submit = st.form_submit_button("🔥 ANALYZE MARKET VALUE")
        st.markdown('</div>', unsafe_allow_html=True)

    if submit:
        if not api_key:
            st.error("Engine failure: API Key not found in Secrets.")
        elif not (make and model_name):
            st.warning("Please fill in Brand and Model to continue.")
        else:
            with st.spinner("SCANNING GLOBAL AUTOMOTIVE DATA..."):
                try:
                    # Using gemini-1.5-flash which is stable
                    model_ai = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = (f"Market Expert: Current price for {year} {make} {model_name} {trim} with {miles} miles. "
                              f"Format: PRICE: [number] REASON: [technical justification]")
                    
                    response = model_ai.generate_content(prompt).text
                    
                    price_val = response.split("REASON:")[0].replace("PRICE:", "").strip()
                    reason_val = response.split("REASON:")[1].strip()

                    # Format and display price
                    clean_p = "".join(filter(str.isdigit, price_val))
                    st.markdown(f'<div class="price-tag">${int(clean_p):,}</div>', unsafe_allow_html=True)
                    
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.subheader("🏎️ Market Analysis")
                    st.write(reason_val)
                    st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Engine connection failed: {e}")
