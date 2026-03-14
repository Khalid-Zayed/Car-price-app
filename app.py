import streamlit as st
from groq import Groq
import os

# --- AUTHENTICATION ---
groq_key = st.secrets.get("GROQ_API_KEY")
if groq_key:
    client = Groq(api_key=groq_key)

# --- PROFESSIONAL EXECUTIVE UI ---
st.set_page_config(page_title="AutoIntelligence Pro", page_icon="🏎️", layout="wide")

st.markdown("""
    <style>
    /* Premium Executive Dark Mode */
    .stApp {
        background-color: #0a0a0a;
        color: #e0e0e0;
        font-family: 'Inter', -apple-system, sans-serif;
    }

    /* Minimalist High-End Title */
    .hero-title {
        font-size: 58px !important;
        font-weight: 700;
        text-align: center;
        color: #ffffff;
        letter-spacing: -1.5px;
        margin-bottom: 5px;
    }
    .hero-subtitle {
        text-align: center;
        color: #666;
        font-size: 18px;
        margin-bottom: 40px;
    }

    /* Professional Glassmorphism Cards */
    .card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 30px;
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
    }

    /* Clean Valuation Display */
    .price-display {
        font-size: 72px;
        font-weight: 800;
        color: #ffffff;
        text-align: center;
        margin: 20px 0;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 20px;
    }
    .trend-indicator {
        font-size: 24px;
        padding: 5px 12px;
        border-radius: 6px;
        font-weight: 600;
    }

    /* Sleek Action Button */
    .stButton>button {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 4px !important;
        font-weight: 600 !important;
        height: 50px !important;
        width: 100% !important;
        transition: 0.3s all;
    }
    .stButton>button:hover {
        background-color: #cccccc !important;
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'home'

# --- PAGE: HOME (MINIMALIST HERO) ---
if st.session_state.page == 'home':
    st.markdown('<div style="height:80px;"></div>', unsafe_allow_html=True)
    st.markdown('<h1 class="hero-title">Auto Intelligence Pro</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Institutional grade automotive valuation and market analytics.</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        # High-res Porsche Image
        st.image("https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&q=80&w=1200")
        st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
        if st.button("Begin Valuation"):
            st.session_state.page = 'engine'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE: ENGINE (CLEAN DASHBOARD) ---
else:
    col_a, col_b = st.columns([8, 2])
    with col_b:
        if st.button("End Session"):
            st.session_state.page = 'home'
            st.rerun()

    st.markdown('<h1 class="hero-title" style="font-size:32px !important; text-align:left;">Valuation Terminal</h1>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        with st.form("valuation_form"):
            c1, c2 = st.columns(2)
            with c1:
                make = st.text_input("Brand", value="", placeholder="e.g. Porsche")
                model_name = st.text_input("Model", value="", placeholder="e.g. 911 GT3")
                year = st.number_input("Year", min_value=1950, max_value=2027, value=2024)
            with c2:
                trim = st.text_input("Trim specification", value="", placeholder="e.g. Touring")
                miles = st.number_input("Odometer (miles)", value=0)
                submit = st.form_submit_button("Analyze Market")
        st.markdown('</div>', unsafe_allow_html=True)

    if submit:
        if not (make and model_name):
            st.warning("Input required: Please specify the vehicle brand and model.")
        else:
            with st.spinner("Accessing institutional market data..."):
                try:
                    # UPDATED STABILITY PROMPT
                    prompt = (
                        f"Expert Automotive Analyst: Value a {year} {make} {model_name} {trim} with {miles} miles. "
                        "STRICT STABILITY RULES:\n"
                        "1. PRICE STABILITY: Only change the price for every 1,000 miles. A difference of 100 miles must not change the price.\n"
                        "2. TREND: Decide if this specific model is currently 'Appreciating' or 'Depreciating' in the US market.\n"
                        "3. FORMAT: 'PRICE: $[amount]' | 'TREND: [UP/DOWN]' | 'BRIEF: [3 professional sentences on rarity, mileage tier, and outlook]'"
                    )
                    
                    chat_completion = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model="llama-3.3-70b-versatile",
                    )
                    response = chat_completion.choices[0].message.content

                    if "PRICE:" in response:
                        # Parsing logic
                        price = response.split("|")[0].replace("PRICE:", "").strip()
                        trend_dir = "UP" if "TREND: UP" in response else "DOWN"
                        brief = response.split("BRIEF:")[1].strip()

                        trend_color = "#00ff00" if trend_dir == "UP" else "#ff4b4b"
                        trend_arrow = "▲" if trend_dir == "UP" else "▼"

                        st.markdown(f'''
                            <div class="price-display">
                                {price}
                                <span class="trend-indicator" style="background: {trend_color}22; color: {trend_color};">
                                    {trend_arrow} {trend_dir}
                                </span>
                            </div>
                        ''', unsafe_allow_html=True)
                        
                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        st.markdown('### Executive Market Brief')
                        st.write(brief)
                        st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Engine connection failed: {e}")

st.markdown('<p style="text-align:center; padding:40px; color:#444; font-size:12px;">© 2026 Auto Intelligence | Licensed for Institutional Use</p>', unsafe_allow_html=True)
