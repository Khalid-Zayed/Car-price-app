import streamlit as st
from groq import Groq
import urllib.parse

# --- 1. SETUP ---
groq_key = st.secrets.get("GROQ_API_KEY")
client_groq = Groq(api_key=groq_key)

st.set_page_config(page_title="Run&Drive AI", layout="wide")

# --- 2. CSS FOR VISIBILITY & STYLE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@900&display=swap');
    .stApp { background-color: #ffffff; }
    #MainMenu, footer, header, .stDeployButton, div[data-testid="stToolbar"] {visibility: hidden; display: none;}

    .main-title {
        font-family: 'Montserrat', sans-serif;
        font-size: 5rem;
        color: #000000 !important;
        text-align: center;
        margin-bottom: 10px;
    }

    /* Force all Labels to be Black and Visible */
    label {
        color: #000000 !important;
        font-weight: 800 !important;
        font-size: 1rem !important;
        text-transform: uppercase;
    }

    .stat-card {
        background: #ffffff;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #eeeeee;
        border-bottom: 5px solid #32cd32;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    
    .stat-card small { color: #444444 !important; font-weight: 800; text-transform: uppercase; display: block; margin-bottom: 10px; }
    .stat-card h1 { color: #000000 !important; margin: 0; font-weight: 900; }
    .spec-label { color: #32cd32 !important; font-weight: 800; font-size: 0.85rem; display: block; text-transform: uppercase; }
    .spec-value { color: #000000 !important; font-weight: 700; font-size: 1.2rem; display: block; }

    /* Green Analysis Button */
    div.stButton > button:first-child {
        background-color: #32cd32 !important;
        color: white !important;
        font-weight: 900 !important;
        border: none !important;
        height: 3em !important;
        width: 100% !important;
        border-radius: 10px !important;
    }

    .section-header h2 { color: #000000 !important; font-weight: 900; border-left: 5px solid #32cd32; padding-left: 15px; }
    .share-btn { display: inline-block; padding: 12px 25px; margin: 5px; border-radius: 30px; color: white !important; text-decoration: none; font-weight: bold; }
    .tw-btn { background-color: #000000; }
    .wa-btn { background-color: #25D366; }
    .disclaimer { text-align: center; color: #666666 !important; font-size: 0.75rem; margin-top: 50px; padding: 20px; border-top: 1px solid #eeeeee; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. UI LAYOUT ---
st.markdown('<h1 class="main-title">Run&Drive</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#32cd32; font-weight:800; letter-spacing:3px; margin-top:-20px;">INSTITUTIONAL AI ANALYTICS</p>', unsafe_allow_html=True)

with st.columns([1,2,1])[1]:
    brand = st.text_input("Brand", placeholder="e.g. Mercedes")
    model = st.text_input("Model", placeholder="e.g. G-Wagon")
    year = st.number_input("Year", min_value=1900, max_value=2026, value=2024)
    miles = st.number_input("Current Mileage (Miles)", min_value=0, value=0)
    
    submit = st.button("RUN AI ANALYSIS")

# --- 4. ENGINE LOGIC ---
if submit and brand and model:
    # MILEAGE LOGIC: If miles <= 100, we force Gemini to treat it as "Brand New"
    condition = "Brand New / Unused" if miles <= 100 else f"Used with {miles} miles"
    
    with st.spinner("Analyzing Market Value..."):
        try:
            prompt = f"Analyze a {year} {brand} {model} in {condition} condition. Format exactly: PRICE: [val] | TREND: [status] | SPECS: [Engine]/[Power]/[0-60]/[Top Speed]"
            
            res = client_groq.chat.completions.create(
                messages=[{"role":"user","content":prompt}], 
                model="llama-3.3-70b-versatile"
            ).choices[0].message.content
            
            price = res.split("PRICE:")[1].split("|")[0].strip()
            trend = res.split("TREND:")[1].split("|")[0].strip()
            specs_raw = res.split("SPECS:")[1].strip().split("/")
            while len(specs_raw) < 4: specs_raw.append("N/A")

            # --- DISPLAY ---
            st.markdown(f'<h2 style="text-align:center; color:black; margin-top:30px;">{year} {brand} {model}</h2>', unsafe_allow_html=True)
            if miles <= 100:
                st.markdown('<p style="text-align:center; color:#32cd32; font-weight:bold;">✨ NEW VEHICLE STATUS DETECTED</p>', unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            c1.markdown(f'<div class="stat-card"><small>MARKET VALUATION ({condition})</small><h1 style="color:#32cd32 !important;">{price}</h1></div>', unsafe_allow_html=True)
            c2.markdown(f'<div class="stat-card"><small>MARKET TREND</small><h1>{trend}</h1></div>', unsafe_allow_html=True)

            st.markdown('<div class="section-header"><h2>Technical Specifications</h2></div>', unsafe_allow_html=True)
            sc1, sc2, sc3, sc4 = st.columns(4)
            sc1.markdown(f'<div class="stat-card"><span class="spec-label">Engine</span><span class="spec-value">{specs_raw[0]}</span></div>', unsafe_allow_html=True)
            sc2.markdown(f'<div class="stat-card"><span class="spec-label">Power</span><span class="spec-value">{specs_raw[1]}</span></div>', unsafe_allow_html=True)
            sc3.markdown(f'<div class="stat-card"><span class="spec-label">0-60 MPH</span><span class="spec-value">{specs_raw[2]}</span></div>', unsafe_allow_html=True)
            sc4.markdown(f'<div class="stat-card"><span class="spec-label">Top Speed</span><span class="spec-value">{specs_raw[3]}</span></div>', unsafe_allow_html=True)

            # SHARE BUTTONS
            share_text = f"Check out the AI analysis for the {year} {brand} {model} on Run&Drive!"
            encoded_text = urllib.parse.quote(share_text)
            st.markdown(f'''
                <div style="text-align:center; margin-top:30px;">
                    <a href="https://twitter.com/intent/tweet?text={encoded_text}" target="_blank" class="share-btn tw-btn">Share on X</a>
                    <a href="https://wa.me/?text={encoded_text}" target="_blank" class="share-btn wa-btn">Share on WhatsApp</a>
                </div>
            ''', unsafe_allow_html=True)

            st.markdown('<div class="disclaimer">DISCLAIMER: This is an AI-generated estimate. Run&Drive is not liable for pricing fluctuations.</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error("System Error: AI could not fetch data. Please check car details.")
