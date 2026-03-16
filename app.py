import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import json

# --- 1. SETUP ---
groq_key = st.secrets.get("GROQ_API_KEY")
if not groq_key:
    st.error("API Key Missing: Please add GROQ_API_KEY to your Streamlit Secrets.")
    st.stop()

client_groq = Groq(api_key=groq_key)
st.set_page_config(page_title="Run&Drive AI", layout="centered")

# --- 2. CSS STYLING (FORCED VISIBILITY) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;900&display=swap');
    
    .stApp { background-color: #ffffff; color: #000000; }
    #MainMenu, footer, header, .stDeployButton, div[data-testid="stToolbar"] {visibility: hidden; display: none;}
    
    .main-title { font-family: 'Montserrat', sans-serif; font-size: 4rem; color: #000000 !important; text-align: center; margin-bottom: 0px; }
    .sub-title { font-family: 'Montserrat', sans-serif; font-size: 1rem; color: #32cd32 !important; text-align: center; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 40px; }
    
    /* Force Input Labels to Black */
    label, p, span, div, .stMarkdown { color: #000000 !important; font-weight: 700; }
    
    .stTextInput input, .stNumberInput input {
        color: #000000 !important;
        border: 1px solid #ddd !important;
        background-color: #ffffff !important;
    }

    /* --- 🔘 BUTTON STYLING (THE HOVER FIX) --- */
    div.stButton > button:first-child { 
        background-color: #000000 !important; /* Box stays black */
        color: #ffffff !important;           /* TEXT IS NOW FORCED WHITE */
        font-weight: 900 !important; 
        font-family: 'Montserrat', sans-serif !important;
        text-transform: uppercase !important;
        width: 100% !important; 
        border-radius: 12px !important; 
        height: 3.5rem !important; 
        border: 2px solid #000000 !important; 
        transition: all 0.3s ease-in-out !important;
        margin-top: 20px !important;
    }

    /* Hover State: Box turns Green, Text turns Black */
    div.stButton > button:first-child:hover { 
        background-color: #32cd32 !important; 
        color: #000000 !important;           /* TEXT TURNS BLACK ON HOVER */
        border: 2px solid #32cd32 !important;
    }

    /* Stats & Cards */
    .stat-card { background: #ffffff; padding: 25px; border-radius: 15px; border: 1px solid #eee; border-bottom: 5px solid #32cd32; text-align: center; margin-bottom: 20px; }
    .stat-card small { color: #000000 !important; font-weight: 800; text-transform: uppercase; font-size: 0.8rem; }
    .stat-card h1 { color: #000000 !important; margin: 5px 0; font-weight: 900; font-size: 2.8rem; }
    .stat-card h3 { color: #000000 !important; margin: 0; font-weight: 800; font-size: 1.2rem; }
    .green-text { color: #32cd32 !important; }
    .insight-box { background: #f9f9f9; padding: 20px; border-radius: 10px; border-left: 5px solid #32cd32; margin-top: 20px; color: #000 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SEARCH LOGIC ---
def search_market(query):
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=3)
            return "\n".join([f"{r['title']}: {r['body']}" for r in results]) if results else "No data."
    except: return "Live data sync unavailable."

# --- 4. THE VERTICAL FORM ---
st.markdown('<h1 class="main-title">Run&Drive</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Expert Market Intelligence</p>', unsafe_allow_html=True)

brand = st.text_input("Car Brand", placeholder="Maserati")
model = st.text_input("Car Model", placeholder="Ghibli")
trim = st.text_input("Trim / Version", placeholder="Trofeo") # Text removed as requested
year = st.number_input("Year of Manufacture", 1900, 2026, 2024)
miles = st.number_input("Current Odometer Reading (Miles)", min_value=0, value=0)

submit = st.button("RUN LIVE MARKET VALUATION")

# --- 5. ACCURACY ENGINE ---
if submit and brand and model:
    with st.spinner("Analyzing Global Sales Trends..."):
        full_name = f"{year} {brand} {model} {trim}"
        search_data = search_market(f"real price {full_name} {miles} miles 2026 USD")
        
        try:
            prompt = f"""
            Analyst: Act as a Senior Car Appraiser in 2026.
            Vehicle: {full_name} with {miles} miles.
            Data: {search_data}
            
            Return ONLY this JSON:
            {{
              "price": "[Value]",
              "trend": "[Status]",
              "specs": {{"engine": "[Type]", "hp": "[HP]", "zero_sixty": "[0-60]", "top": "[Speed]"}},
              "why": "[Brief explanation]"
            }}
            """
            
            response = client_groq.chat.completions.create(
                messages=[{"role":"user","content":prompt}],
                model="llama-3.3-70b-versatile",
                temperature=0.1
            ).choices[0].message.content

            data = json.loads(response)

            # Display
            st.markdown(f"<h2 style='text-align:center; color:black; margin-top:40px;'>{full_name}</h2>", unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            c1.markdown(f'<div class="stat-card"><small>VALUE</small><h1 class="green-text">{data["price"]}</h1></div>', unsafe_allow_html=True)
            c2.markdown(f'<div class="stat-card"><small>TREND</small><h1>{data["trend"]}</h1></div>', unsafe_allow_html=True)

            p1, p2, p3, p4 = st.columns(4)
            p1.markdown(f'<div class="stat-card"><small>ENGINE</small><h3>{data["specs"]["engine"]}</h3></div>', unsafe_allow_html=True)
            p2.markdown(f'<div class="stat-card"><small>POWER</small><h3>{data["specs"]["hp"]}</h3></div>', unsafe_allow_html=True)
            p3.markdown(f'<div class="stat-card"><small>0-60</small><h3>{data["specs"]["zero_sixty"]}</h3></div>', unsafe_allow_html=True)
            p4.markdown(f'<div class="stat-card"><small>TOP SPEED</small><h3>{data["specs"]["top"]}</h3></div>', unsafe_allow_html=True)

            st.markdown(f'<div class="insight-box"><b>Valuation Logic:</b> {data["why"]}</div>', unsafe_allow_html=True)

        except:
            st.error("Accuracy timeout. Check details and retry.")
