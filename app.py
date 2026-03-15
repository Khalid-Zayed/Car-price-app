import streamlit as st
from groq import Groq
import urllib.parse

# --- 1. SETUP ---
groq_key = st.secrets.get("GROQ_API_KEY")
client_groq = Groq(api_key=groq_key)

st.set_page_config(page_title="Run&Drive AI", layout="wide")

# --- 2. THE ULTIMATE VISIBILITY CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@900&display=swap');
    
    /* Global Background */
    .stApp { background-color: #ffffff; }
    
    /* Hide Streamlit Junk */
    #MainMenu, footer, header, .stDeployButton, div[data-testid="stToolbar"] {visibility: hidden; display: none;}

    /* Main Title */
    .main-title {
        font-family: 'Montserrat', sans-serif;
        font-size: 5rem;
        color: #000000 !important;
        text-align: center;
        margin-bottom: 10px;
    }

    /* Force all Input Labels to be Black */
    label {
        color: #000000 !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
    }

    /* Stat Cards */
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
    
    /* Visible Text inside Cards */
    .stat-card small { 
        color: #444444 !important; 
        font-weight: 800; 
        text-transform: uppercase; 
        display: block; 
        margin-bottom: 10px; 
    }
    
    .stat-card h1, .stat-card h2 { 
        color: #000000 !important; 
        margin: 0; 
    }

    .spec-label { color: #32cd32 !important; font-weight: 800; font-size: 0.85rem; display: block; text-transform: uppercase; }
    .spec-value { color: #000000 !important; font-weight: 700; font-size: 1.2rem; display: block; }

    .section-header h2 { color: #000000 !important; font-weight: 900; }
    
    .share-btn {
        display: inline-block;
        padding: 12px 25px;
        margin: 5px;
        border-radius: 30px;
        color: white !important;
        text-decoration: none;
        font-weight: bold;
    }
    .tw-btn { background-color: #000000; }
    .wa-btn { background-color: #25D366; }

    .disclaimer { text-align: center; color: #666666 !important; font-size: 0.75rem; margin-top: 50px; padding: 20px; border-top: 1px solid #eeeeee; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. UI ---
st.markdown('<h1 class="main-title">Run&Drive</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#32cd32; font-weight:800; letter-spacing:3px; margin-top:-20px;">INSTITUTIONAL AI ANALYTICS</p>', unsafe_allow_html=True)

# I wrapped the inputs in a clean container to make the questions stand out
with st.container():
    with st.columns([1,2,1])[1]:
        brand = st.text_input("What is the Car Brand?", placeholder="e.g. Mercedes")
        model = st.text_input("What is the Car Model?", placeholder="e.g. G-Wagon")
        year = st.number_input("What is the Manufacturing Year?", min_value=1900, max_value=2026, value=2024)
        
        # Center the button
        if st.button("RUN AI ANALYSIS", use_container_width=True):
            if brand and model:
                with st.spinner("Synchronizing Engine Data..."):
                    try:
                        prompt = f"Analyze {year} {brand} {model}. Format exactly: PRICE: [val] | TREND: [status] | SPECS: [Engine]/[Power]/[0-60]/[Top Speed]"
                        res = client_groq.chat.completions.create(messages=[{"role":"user","content":prompt}], model="llama-3.3-70b-versatile").choices[0].message.content
                        
                        price = res.split("PRICE:")[1].split("|")[0].strip()
                        trend = res.split("TREND:")[1].split("|")[0].strip()
                        specs_raw = res.split("SPECS:")[1].strip().split("/")
                        while len(specs_raw) < 4: specs_raw.append("N/A")

                        st.markdown(f'<h2 style="text-align:center; color:black; margin-top:30px;">{year} {brand} {model}</h2>', unsafe_allow_html=True)
                        
                        c1, c2 = st.columns(2)
                        c1.markdown(f'<div class="stat-card"><small>ESTIMATED PRICE</small><h1 style="color:#32cd32 !important;">{price}</h1></div>', unsafe_allow_html=True)
                        c2.markdown(f'<div class="stat-card"><small>MARKET TREND</small><h1>{trend}</h1></div>', unsafe_allow_html=True)

                        st.markdown('<div class="section-header"><h2>Technical Specifications</h2></div>', unsafe_allow_html=True)
                        sc1, sc2, sc3, sc4 = st.columns(4)
                        sc1.markdown(f'<div class="stat-card"><span class="spec-label">Engine</span><span class="spec-value">{specs_raw[0]}</span></div>', unsafe_allow_html=True)
                        sc2.markdown(f'<div class="stat-card"><span class="spec-label">Power</span><span class="spec-value">{specs_raw[1]}</span></div>', unsafe_allow_html=True)
                        sc3.markdown(f'<div class="stat-card"><span class="spec-label">0-60 MPH</span><span class="spec-value">{specs_raw[2]}</span></div>', unsafe_allow_html=True)
                        sc4.markdown(f'<div class="stat-card"><span class="spec-label">Top Speed</span><span class="spec-value">{specs_raw[3]}</span></div>', unsafe_allow_html=True)

                        # SHARE
                        share_text = f"Check out the AI analysis for the {year} {brand} {model} on Run&Drive!"
                        encoded_text = urllib.parse.quote(share_text)
                        st.markdown(f'''
                            <div style="text-align:center; margin-top:30px;">
                                <a href="https://twitter.com/intent/tweet?text={encoded_text}" target="_blank" class="share-btn tw-btn">Share on X</a>
                                <a href="https://wa.me/?text={encoded_text}" target="_blank" class="share-btn wa-btn">Share on WhatsApp</a>
                            </div>
                        ''', unsafe_allow_html=True)

                        st.markdown('<div class="disclaimer">DISCLAIMER: This is an AI-generated estimate based on market patterns. Verify data before purchasing.</div>', unsafe_allow_html=True)

                    except Exception as e:
                        st.error("Engine failed to parse data. Try a more common car name.")
            else:
                st.warning("Please fill in both Brand and Model.")
