import streamlit as st
import google.generativeai as genai
import os

# --- AUTHENTICATION ---
# Use the key you generated in Google AI Studio
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# --- UI & ANIMATIONS ---
st.set_page_config(page_title="AutoIntelligence Pro", page_icon="🏎️", layout="wide")
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #2a0000 0%, #000000 100%); color: white; }
    .main-title { font-size: 70px !important; font-weight: 900; text-align: center; color: #ff0000; text-shadow: 0 0 20px #ff0000; }
    .glass-card { background: rgba(255, 0, 0, 0.05); border-radius: 15px; padding: 30px; border: 1px solid #ff0000; backdrop-filter: blur(10px); }
    .price-tag { font-size: 60px; font-weight: 900; color: #ff0000; text-align: center; background: white; border-radius: 10px; padding: 10px; margin: 20px 0; }
    .stButton>button { background: linear-gradient(45deg, #ff0000, #660000) !important; color: white !important; font-weight: bold !important; width: 100% !important; height: 50px !important; border: none !important; }
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'home'

# --- PAGE: HOME ---
if st.session_state.page == 'home':
    st.markdown('<div style="height:100px;"></div>', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">AUTO INTELLIGENCE</h1>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.image("https://images.unsplash.com/photo-1544636331-e26879cd4d9b?auto=format&fit=crop&w=1000")
        if st.button("🏁 ENTER SYSTEM"):
            st.session_state.page = 'engine'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE: ENGINE ---
else:
    if st.button("⬅️ EXIT"):
        st.session_state.page = 'home'
        st.rerun()

    st.markdown('<h1 class="main-title" style="font-size:40px !important;">VALUATION ENGINE</h1>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        with st.form("valuation_form"):
            c1, c2 = st.columns(2)
            with c1:
                make = st.text_input("BRAND")
                model_name = st.text_input("MODEL")
                year = st.number_input("YEAR", 1950, 2027, 2023)
            with c2:
                trim = st.text_input("TRIM")
                miles = st.number_input("MILES", value=15000)
                submit = st.form_submit_button("🔥 ANALYZE MARKET VALUE")
        st.markdown('</div>', unsafe_allow_html=True)

    if submit:
        if not api_key:
            st.error("Authentication Error: Key not found.")
        elif not (make and model_name):
            st.warning("Please fill in Brand and Model.")
        else:
            with st.spinner("SCANNING MARKET DATA..."):
                try:
                    # Updated model name to 'gemini-pro' to fix your 404 error
                    model_ai = genai.GenerativeModel('gemini-pro')
                    prompt = f"Appraiser: Current market value for {year} {make} {model_name} {trim} with {miles} miles. Format: PRICE: [number] REASON: [justification]"
                    response = model_ai.generate_content(prompt).text
                    
                    price_val = response.split("REASON:")[0].replace("PRICE:", "").strip()
                    reason_val = response.split("REASON:")[1].strip()

                    st.markdown(f'<div class="price-tag">${int("".join(filter(str.isdigit, price_val))):,}</div>', unsafe_allow_html=True)
                    st.info(reason_val)
                except Exception as e:
                    st.error(f"Engine connection failed: {e}")
