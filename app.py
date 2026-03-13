import streamlit as st
from groq import Groq
import os

# --- AUTHENTICATION ---
# Ensure you have GROQ_API_KEY in your Streamlit Secrets
groq_key = st.secrets.get("GROQ_API_KEY")
if groq_key:
    client = Groq(api_key=groq_key)

# --- VIBRANT RED INTERACTIVE UI ---
st.set_page_config(page_title="AutoIntelligence Pro", page_icon="🏎️", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at center, #2a0000 0%, #000000 100%);
        color: #ffffff;
    }
    @keyframes pulse { 0% { opacity: 0.8; } 100% { opacity: 1; text-shadow: 0 0 30px #ff0000; } }
    .main-title {
        font-size: 75px !important;
        font-weight: 900;
        text-align: center;
        color: #ff0000;
        animation: pulse 1.5s infinite alternate;
        letter-spacing: -3px;
    }
    .glass-card {
        background: rgba(255, 0, 0, 0.05);
        border-radius: 15px;
        padding: 30px;
        border: 1px solid #ff0000;
        backdrop-filter: blur(10px);
    }
    .stButton>button {
        background: linear-gradient(45deg, #ff0000, #660000) !important;
        color: white !important;
        font-weight: bold !important;
        width: 100% !important;
        height: 55px !important;
        border: none !important;
    }
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
        st.image("https://images.unsplash.com/photo-1544636331-e26879cd4d9b?auto=format&fit=crop&w=1000")
        if st.button("🏁 ENTER SYSTEM"):
            st.session_state.page = 'engine'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE: VALUATION ENGINE ---
else:
    if st.button("⬅️ LOGOUT"):
        st.session_state.page = 'home'
        st.rerun()

    st.markdown('<h1 class="main-title" style="font-size:45px !important;">VALUATION ENGINE</h1>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        with st.form("main_form"):
            c1, c2 = st.columns(2)
            with c1:
                make = st.text_input("BRAND", value="")
                model_name = st.text_input("MODEL", value="")
                year = st.number_input("YEAR", min_value=1950, max_value=2027, value=2024)
            with c2:
                trim = st.text_input("TRIM / SPEC", value="")
                miles = st.number_input("MILEAGE", value=0)
                submit = st.form_submit_button("🔥 ANALYZE MARKET VALUE")
        st.markdown('</div>', unsafe_allow_html=True)

    if submit:
        if not groq_key:
            st.error("🔑 KEY ERROR: Ensure GROQ_API_KEY is in Streamlit Secrets.")
        elif not (make and model_name):
            st.warning("⚠️ DATA ERROR: Brand and Model cannot be blank.")
        else:
            with st.spinner("SCANNING REAL-TIME DATA..."):
                try:
                    # Using the latest supported Groq model
                    chat_completion = client.chat.completions.create(
                        messages=[{
                            "role": "user",
                            "content": f"Provide current market value for {year} {make} {model_name} {trim} with {miles} miles. Format: PRICE: [number] REASON: [justification]"
                        }],
                        model="llama-3.3-70b-versatile",
                    )
                    response = chat_completion.choices[0].message.content
                    
                    if "REASON:" in response:
                        price_val = response.split("REASON:")[0].replace("PRICE:", "").strip()
                        reason_val = response.split("REASON:")[1].strip()
                        clean_p = "".join(filter(str.isdigit, price_val))
                        
                        st.markdown(f'<div class="price-tag">${int(clean_p):,}</div>', unsafe_allow_html=True)
                        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                        st.subheader("🏎️ Market Insight")
                        st.write(reason_val)
                        st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Engine connection failed: {e}")
