import streamlit as st
from groq import Groq
import urllib.parse

# --- 1. SETUP ---
groq_key = st.secrets.get("GROQ_API_KEY")
client_groq = Groq(api_key=groq_key)

st.set_page_config(page_title="Run&Drive AI", layout="wide")

# --- 2. CSS (STAYS THE SAME - LOOKS GOOD) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@900&display=swap');
    .stApp { background-color: #ffffff; }
    #MainMenu, footer, header, .stDeployButton, div[data-testid="stToolbar"] {visibility: hidden; display: none;}
    .main-title { font-family: 'Montserrat', sans-serif; font-size: 5rem; color: #000000 !important; text-align: center; margin-bottom: 10px; }
    label { color: #000000 !important; font-weight: 800 !important; text-transform: uppercase; }
    .stat-card { background: #ffffff; padding: 25px; border-radius: 15px; border: 1px solid #eeeeee; border-bottom: 5px solid #32cd32; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.05); margin-bottom: 20px; }
    .stat-card small { color: #444444 !important; font-weight: 800; text-transform: uppercase; display: block; margin-bottom: 10px; }
    .stat-card h1 { color: #000000 !important; margin: 0; font-weight: 900; }
    .spec-label { color: #32cd32 !important; font-weight: 800; font-size: 0.85rem; display: block; text-transform: uppercase; }
    .spec-value { color: #000000 !important; font-weight: 700; font-size: 1.2rem; display: block; }
    div.stButton > button:first-child { background-color: #32cd32 !important; color: white !important; font-weight: 900; height: 3em !important; width: 100% !important; border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. UI ---
st.markdown('<h1 class="main-title">Run&Drive</h1>', unsafe_allow_html=True)

with st.columns([1,2,1])[1]:
    brand = st.text_input("Brand")
    model = st.text_input("Model")
    year = st.number_input("Year", min_value=1900, max_value=2026, value=2024)
    miles = st.number_input("Current Mileage (Miles)", min_value=0, value=0)
    submit = st.button("RUN AI ANALYSIS")

# --- 4. THE ACCURACY ENGINE ---
if submit and brand and model:
    with st.spinner("Calculating Precision Value..."):
        try:
            # IMPROVED ACCURACY PROMPT
            prompt = f"""
            You are an expert car appraiser. Provide a precise market valuation for:
            Car: {year} {brand} {model}
            Mileage: {miles} miles
            
            RULES:
            1. If mileage is 0-100, the price MUST be the full MSRP (New Price).
            2. High mileage MUST decrease the price compared to 0 mileage.
            3. Accuracy is #1 priority.
            
            Format exactly: 
            PRICE: [The USD Value]
            TREND: [Bullish/Bearish/Stable]
            SPECS: [Engine Type]/[Horsepower]/[0-60 Time]/[Top Speed]
            """
            
            res = client_groq.chat.completions.create(
                messages=[{"role":"user","content":prompt}], 
                model="llama-3.3-70b-versatile",
                temperature=0.2 # Lower temperature = more factual/less creative
            ).choices[0].message.content
            
            # Parsing
            price = res.split("PRICE:")[1].split("TREND:")[0].strip()
            trend = res.split("TREND:")[1].split("SPECS:")[0].strip()
            specs_raw = res.split("SPECS:")[1].strip().split("/")
            while len(specs_raw) < 4: specs_raw.append("N/A")

            # --- DISPLAY RESULTS ---
            st.markdown(f'<h2 style="text-align:center; color:black; margin-top:30px;">{year} {brand} {model}</h2>', unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            c1.markdown(f'<div class="stat-card"><small>MARKET VALUATION</small><h1 style="color:#32cd32 !important;">{price}</h1></div>', unsafe_allow_html=True)
            c2.markdown(f'<div class="stat-card"><small>MARKET TREND</small><h1>{trend}</h1></div>', unsafe_allow_html=True)

            st.markdown("### Technical Specifications")
            sc1, sc2, sc3, sc4 = st.columns(4)
            sc1.markdown(f'<div class="stat-card"><span class="spec-label">Engine</span><span class="spec-value">{specs_raw[0]}</span></div>', unsafe_allow_html=True)
            sc2.markdown(f'<div class="stat-card"><span class="spec-label">Power</span><span class="spec-value">{specs_raw[1]}</span></div>', unsafe_allow_html=True)
            sc3.markdown(f'<div class="stat-card"><span class="spec-label">0-60 MPH</span><span class="spec-value">{specs_raw[2]}</span></div>', unsafe_allow_html=True)
            sc4.markdown(f'<div class="stat-card"><span class="spec-label">Top Speed</span><span class="spec-value">{specs_raw[3]}</span></div>', unsafe_allow_html=True)

        except Exception as e:
            st.error("Accuracy timeout. Please refine your car details.")
