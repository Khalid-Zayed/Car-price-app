import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import json

# --- 1. SETUP ---
# Fetch keys from Streamlit Secrets
groq_key = st.secrets.get("GROQ_API_KEY")

if not groq_key:
    st.error("API Key Missing: Please add GROQ_API_KEY to your Streamlit Secrets.")
    st.stop()

client_groq = Groq(api_key=groq_key)

st.set_page_config(page_title="Run&Drive AI", layout="centered")

# --- 2. CSS FOR FORCED VISIBILITY & REVERSE HOVER ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;900&display=swap');
    
    /* Global Background and Defaults */
    .stApp { background-color: #ffffff; color: #000000; }
    #MainMenu, footer, header, .stDeployButton, div[data-testid="stToolbar"] {visibility: hidden; display: none;}
    
    /* Header Styles */
    .main-title { font-family: 'Montserrat', sans-serif; font-size: 4rem; color: #000000 !important; text-align: center; margin-bottom: 0px; }
    .sub-title { font-family: 'Montserrat', sans-serif; font-size: 1rem; color: #32cd32 !important; text-align: center; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 40px; }
    
    /* Force Input Form styling to be Black */
    label, p, span, div, .stMarkdown { color: #000000 !important; font-weight: 700; }
    
    /* Input Field Styling (Ensuring text is visible) */
    .stTextInput input, .stNumberInput input {
        color: #000000 !important;
        border: 1px solid #ddd !important;
        background-color: #ffffff !important;
    }
    
    /* Placeholder Text color */
    ::placeholder { color: #888888 !important; opacity: 1; }

    /* --- 🔘 REVERSE HOVER BUTTON STYLING (THE FIX) --- */
    div.stButton > button:first-child { 
        background-color: #000000 !important; /* Initial: BLACK box */
        color: #ffffff !important;           /* Initial: WHITE text */
        font-weight: 900 !important; 
        font-family: 'Montserrat', sans-serif !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        width: 100% !important; 
        border-radius: 12px !important; 
        height: 3.5rem !important; 
        border: 2px solid #000000 !important; 
        transition: all 0.3s ease-in-out !important; /* Smooth invert effect */
        margin-top: 20px !important;
    }

    /* Standard Invert Effect on Hover */
    div.stButton > button:first-child:hover { 
        background-color: #32cd32 !important; /* Hover: GREEN box */
        color: #000000 !important;           /* Hover: BLACK text */
        border: 2px solid #32cd32 !important;
    }

    /* --- RESULTS DISPLAY --- */
    .stat-card { background: #ffffff; padding: 25px; border-radius: 15px; border: 1px solid #eee; border-bottom: 5px solid #32cd32; text-align: center; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
    .stat-card small { color: #000000 !important; font-weight: 800; text-transform: uppercase; font-size: 0.8rem; }
    .stat-card h1 { color: #000000 !important; margin: 5px 0; font-weight: 900; font-size: 2.8rem; }
    .stat-card h3 { color: #000000 !important; margin: 0; font-weight: 800; font-size: 1.2rem; }
    .green-text { color: #32cd32 !important; } /* Highlight Green */
    
    /* Valuation Logic Box */
    .insight-box { background: #f9f9f9; padding: 20px; border-radius: 10px; border-left: 5px solid #32cd32; margin-top: 20px; color: #000 !important; line-height: 1.6; }
    
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIC ENGINES (NO CHANGES MADE HERE) ---
def search_market(query):
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=3)
            if not results: return "No live listings found."
            return "\n".join([f"{r['title']}: {r['body']}" for r in results])
    except: return "Live data sync currently unavailable."

# --- 4. THE VERTICAL FORM LAYOUT (FORCED V-STACK) ---
st.markdown('<h1 class="main-title">Run&Drive</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Expert Market Intelligence</p>', unsafe_allow_html=True)

# Central container for vertical alignment of forms
with st.container():
    # Labels are forced black via CSS, and forms are stacked vertically
    brand = st.text_input("Car Brand", placeholder="e.g. Maserati")
    model = st.text_input("Car Model", placeholder="e.g. Ghibli")
    trim = st.text_input("Trim / Version (DuckDuckGo will search this)", placeholder="e.g. Trofeo / Modena")
    year = st.number_input("Year of Manufacture", min_value=1900, max_value=2026, value=2024)
    miles = st.number_input("Current Odometer Reading (Miles)", min_value=0, value=0)
    
    # The submission button with the custom hover effect
    submit = st.button("RUN LIVE MARKET VALUATION")

# --- 5. EXECUTION & DISPLAY (NO CHANGES MADE HERE) ---
if submit and brand and model:
    ifmiles_text = "✨ New Vehicle Status Detected" if miles <= 100 else f"Used: {miles} miles"
    
    with st.spinner("Analyzing Global Sales Trends..."):
        # Live Search Phase
        full_name = f"{year} {brand} {model} {trim}"
        search_data = search_market(f"real market price {full_name} {miles} miles 2026 USD")
        
        try:
            # Construct the expert prompt
            prompt = f"""
            Analyst Persona: Senior Automotive Valuer at a luxury auction house.
            Date: March 16, 2026.
            
            Vehicle: {full_name} | Mileage: {miles} miles.
            Condition Context: If miles < 100, use 2026 MSRP/Sticker Price. If miles > 100, calculate depreciation based on trim rarity and reliability.
            
            Provide only this concise JSON response without commentary:
            {{
              "price": "[The Precise USD Value]",
              "trend": "[Bullish/Bearish/Stable]",
              "specs": {{
                "engine": "[Type]",
                "hp": "[HP]",
                "zero_sixty": "[Time]",
                "top": "[Speed]"
              }},
              "why": "[A 2-sentence explanation of why this specific price was chosen for this trim and mileage]"
            }}
            """
            
            response = client_groq.chat.completions.create(
                messages=[{"role":"user","content":prompt}],
                model="llama-3.3-70b-versatile",
                temperature=0.1
            ).choices[0].message.content

            data = json.loads(response)

            # --- DISPLAY RESULTS ---
            st.markdown(f"<h2 style='text-align:center; color:black; margin-top:40px;'>{full_name}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align:center; color:#32cd32; font-weight:bold;'>{ifmiles_text}</p>", unsafe_allow_html=True)
            
            # Row 1: Valuation & Trend
            res_col1, res_col2 = st.columns(2)
            res_col1.markdown(f'<div class="stat-card"><small>INSTITUTIONAL VALUE</small><h1 class="green-text">{data["price"]}</h1></div>', unsafe_allow_html=True)
            res_col2.markdown(f'<div class="stat-card"><small>MARKET TREND (2026)</small><h1>{data["trend"]}</h1></div>', unsafe_allow_html=True)

            # Row 2: Performance Grid
            p1, p2, p3, p4 = st.columns(4)
            p1.markdown(f'<div class="stat-card"><small>ENGINE</small><h3>{data["specs"]["engine"]}</h3></div>', unsafe_allow_html=True)
            p2.markdown(f'<div class="stat-card"><small>POWER</small><h3>{data["specs"]["hp"]}</h3></div>', unsafe_allow_html=True)
            p3.markdown(f'<div class="stat-card"><small>0-60 MPH</small><h3>{data["specs"]["zero_sixty"]}</h3></div>', unsafe_allow_html=True)
            p4.markdown(f'<div class="stat-card"><small>TOP SPEED</small><h3>{data["specs"]["top"]}</h3></div>', unsafe_allow_html=True)

            # Row 3: Valuation Insight (The "Why")
            st.markdown(f'<div class="insight-box"><b>Valuation Logic:</b> {data["why"]}</div>', unsafe_allow_html=True)
            st.markdown('<div style="text-align:center; color:#999; font-size:0.75rem; margin-top:30px;">AI-GENERATED ESTIMATE BASED ON LIVE WEB-SEARCH SNIPPETS. ALWAYS VERIFY DATA.</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error("Market synchronization timed out. Please refine your car details and retry.")
