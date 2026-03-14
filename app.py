import streamlit as st
from groq import Groq
import os

# --- AUTHENTICATION ---
groq_key = st.secrets.get("GROQ_API_KEY")
if groq_key:
    client = Groq(api_key=groq_key)

# --- EXECUTIVE STEALTH UI ---
st.set_page_config(page_title="AutoIntelligence Pro", page_icon="🏎️", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #050505;
        background-image: 
            url("https://www.transparenttextures.com/patterns/carbon-fibre.png"),
            radial-gradient(circle at center, #1a0000 0%, #000000 100%);
    }

    .main-title {
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 65px !important;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, #00ff00, #00ffff, #ff0000);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -2px;
        margin-top: 10px;
    }

    .glass-card {
        background: rgba(30, 30, 30, 0.5);
        border-radius: 15px;
        padding: 30px;
        border: 1px solid rgba(0, 255, 0, 0.2);
        backdrop-filter: blur(10px);
    }
    
    .result-tag {
        font-size: 60px;
        font-weight: 900;
        color: #000000;
        background: #ffffff;
        text-align: center;
        border-radius: 8px;
        padding: 15px;
        margin-top: 25px;
        border-left: 10px solid #00ff00;
    }

    .stButton>button {
        background: linear-gradient(90deg, #ff0000, #800000) !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: bold !important;
        height: 55px !important;
        width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'home'

# --- PAGE: HOME ---
if st.session_state.page == 'home':
    st.markdown('<div style="height:50px;"></div>', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">Auto Intelligence Pro</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,3,1])
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        # Professional Hero Image
        st.image("https://images.unsplash.com/photo-1544636331-e26879cd4d9b?auto=format&fit=crop&q=80&w=1200")
        
        if st.button("🏁 Access Valuation Engine"):
            st.session_state.page = 'engine'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE: ENGINE TERMINAL ---
else:
    if st.button("⬅️ Disconnect Session"):
        st.session_state.page = 'home'
        st.rerun()

    st.markdown('<h1 class="main-title" style="font-size:40px !important;">Valuation Terminal</h1>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        with st.form("valuation_form"):
            c1, c2 = st.columns(2)
            with c1:
                make = st.text_input("Brand", value="", placeholder="e.g. Porsche")
                model_name = st.text_input("Model Line", value="", placeholder="e.g. 911 GT3")
                year = st.number_input("Production year", min_value=1950, max_value=2027, value=2024)
            with c2:
                trim = st.text_input("Trim / Specification", value="", placeholder="e.g. Weissach Pack")
                miles = st.number_input("Odometer reading (miles)", value=0)
                submit = st.form_submit_button("🔥 Execute Market Analysis")
        st.markdown('</div>', unsafe_allow_html=True)

    if submit:
        if not (make and model_name):
            st.warning("Please specify Brand and Model.")
        else:
            with st.spinner("Analyzing market stability..."):
                try:
                    # UPDATED PROMPT: Added logic to ignore micro-changes in mileage
                    prompt = (
                        f"Professional US Auto Market Expert: Provide a valuation for a {year} {make} {model_name} {trim} with {miles} miles. "
                        "RULES:\n"
                        f"1. MILEAGE LOGIC: Do NOT change the price for minor mileage differences (under 50 miles). A 4-mile difference should almost never change the price. Focus on major wear tiers.\n"
                        "2. FORMAT: Reply exactly with 'PRICE: [Amount]' then 'BRIEF: [Summary]'.\n"
                        "3. THE BRIEF: Provide a 3-sentence professional brief. Include current market demand, how the odometer affects this specific model's value, and a 12-month value forecast."
                    )
                    
                    chat_completion = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model="llama-3.3-70b-versatile",
                    )
                    response = chat_completion.choices[0].message.content

                    if "PRICE:" in response:
                        parts = response.split("BRIEF:")
                        price = parts[0].replace("PRICE:", "").strip()
                        brief = parts[1].strip() if len(parts) > 1 else "No brief available."

                        st.markdown(f'<div class="result-tag">{price}</div>', unsafe_allow_html=True)
                        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                        st.subheader("🏎️ Market Executive Brief")
                        st.write(brief)
                        st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Engine connection failed: {e}")

st.markdown('<p style="text-align:center; padding:20px; color:#333;">© 2026 Auto Intelligence | Professional Grade</p>', unsafe_allow_html=True)
