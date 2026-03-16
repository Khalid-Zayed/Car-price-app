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
st.set_page_config(page_title="Run&Drive AI | Market Pro", layout="centered")

# --- 2. CSS: FOCUS HIGHLIGHTS, GREEN BUTTON & VERTICAL FORMS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;900&display=swap');
    
    .stApp { background-color: #ffffff; color: #000000; }
    #MainMenu, footer, header, .stDeployButton, div[data-testid="stToolbar"] {visibility: hidden; display: none;}
    
    .main-title { font-family: 'Montserrat', sans-serif; font-size: 4rem; color: #000000 !important; text-align: center; margin-bottom: 0px; }
    .sub-title { font-family: 'Montserrat', sans-serif; font-size: 1rem; color: #32cd32 !important; text-align: center; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 40px; }
    
    label, p, span, div, .stMarkdown { color: #000000 !important; font-weight: 700; }
    
    /* Input Fields & Focus Animation */
    .stTextInput input, .stNumberInput input {
        color: #000000 !important;
        background-color: #ffffff !important;
        border: 2px solid #eeeeee !important; 
        border-radius: 8px !important;
        caret-color: #000000 !important; 
        transition: all 0.3s ease;
    }
    
    .stTextInput input:focus, .stNumberInput input:focus, div[data-baseweb="input"]:focus-within {
        border: 2px solid #32cd32 !important; 
        box-shadow: 0 0 10px rgba(50, 205, 50, 0.4) !important; 
        outline: none !important;
        background-color: #fafafa !important;
    }

    ::placeholder { color: #aaaaaa !important; opacity: 1; }

    /* --- 🔘 THE BUTTON: PERMANENT GREEN + HOVER POP --- */
    div.stButton > button:first-child { 
        background-color: #32cd32 !important; 
        color: #000000 !important;           
        font-weight: 900 !important; 
        font-family: 'Montserrat', sans-serif !important;
        text-transform: uppercase !important;
        width: 100% !important; 
        border-radius: 12px !important; 
        height: 4rem !important; 
        border: none !important; 
        transition: transform 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.2s ease !important;
        margin-top: 20px !important;
    }

    div.stButton > button:first-child:hover { 
        transform: scale(1.03) !important; 
        box-shadow: 0 12px 24px rgba(50, 205, 50, 0.3) !important; 
        background-color: #32cd32 !important; 
        color: #000000 !important;           
    }

    /* Cards & Result UI */
    .stat-card { background: #ffffff; padding: 25px; border-radius: 15px; border: 1px solid #eee; border-bottom: 5px solid #32cd32; text-align: center; margin-bottom: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.03); }
    .stat-card small { color: #000000 !important; font-weight: 800; text-transform: uppercase; font-size: 0.8rem; }
    .stat-card h1 { color: #000000 !important; margin: 5px 0; font-weight: 900; font-size: 2.8rem; }
    .stat-card h3 { color: #000000 !important; margin: 0; font-weight: 800; font-size: 1.2rem; }
    .green-text { color: #32cd32 !important; }
    .insight-box { background: #f9f9f9; padding: 20px; border-radius: 10px; border-left: 5px solid #32cd32; margin-top: 20px; color: #000 !important; line-height: 1.6; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SEARCH LOGIC ---
def deep_market_search(query):
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=6)
            return "\n".join([f"{r['title']}: {r['body']}" for r in results]) if results else "No data."
    except:
        return "Live data sync offline."

# --- 4. THE UI FORM (CLEANED) ---
st.markdown('<h1 class="main-title">Run&Drive</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Live Market Analysis</p>', unsafe_allow_html=True)

with st.container():
    # Removed specific SF90 example text
    brand = st.text_input("Car Brand", placeholder="e.g. Maserati")
    model = st.text_input("Car Model", placeholder="e.g. Ghibli")
    trim = st.text_input("Trim / Version", placeholder="e.g. Trofeo")
    year = st.number_input("Year of Manufacture", min_value=1900, max_value=2026, value=2024)
    # Default mileage set to 0 as requested
    miles = st.number_input("Current Odometer Reading (Miles)", min_value=0, value=0)
    
    submit = st.button("RUN DEEP MARKET ANALYSIS")

# --- 5. EXECUTION ENGINE ---
if submit and brand and model:
    with st.spinner("Analyzing Global Market Tiers..."):
        full_name = f"{year} {brand} {model} {trim}"
        search_query = f"{full_name} MSRP original price AND used market value {miles} miles price"
        search_data = deep_market_search(search_query)
        
        try:
            prompt = f"""
            Role: Strict Automotive Appraiser.
            Task: Value a {full_name} with {miles} miles using this data:
            {search_data}
            
            Rules:
            1. Use factory MSRP as a baseline if specific used listings aren't found.
            2. Apply logic: higher mileage = lower price; lower mileage = higher price.
            3. For "hp", provide numbers only (e.g., "580").
            
            Return strictly as JSON:
            {{
              "price": "[Final USD Price]",
              "trend": "[Status]",
              "specs": {{"engine": "[Type]", "hp": "[Numbers]", "zero_sixty": "[Time]", "top": "[Speed]"}},
              "why": "[Explanation of how {miles} miles affected the final valuation.]"
            }}
            """
            
            response = client_groq.chat.completions.create(
                messages=[{"role":"user","content":prompt}],
                model="llama-3.3-70b-versatile",
                temperature=0.1
            ).choices[0].message.content

            clean_json = response.replace('```json', '').replace('```', '').strip()
            data = json.loads(clean_json)

            # --- HP DISPLAY FIX ---
            raw_hp = str(data["specs"]["hp"]).upper().replace("HP", "").strip()
            formatted_hp = f"{raw_hp} HP"

            # --- DISPLAY RESULTS ---
            st.markdown(f"<h2 style='text-align:center; color:black; margin-top:40px;'>{full_name}</h2>", unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            c1.markdown(f'<div class="stat-card"><small>ESTIMATED VALUE</small><h1 class="green-text">{data["price"]}</h1></div>', unsafe_allow_html=True)
            c2.markdown(f'<div class="stat-card"><small>MARKET TREND</small><h1>{data["trend"]}</h1></div>', unsafe_allow_html=True)

            p1, p2, p3, p4 = st.columns(4)
            p1.markdown(f'<div class="stat-card"><small>ENGINE</small><h3>{data["specs"]["engine"]}</h3></div>', unsafe_allow_html=True)
            p2.markdown(f'<div class="stat-card"><small>POWER</small><h3>{formatted_hp}</h3></div>', unsafe_allow_html=True)
            p3.markdown(f'<div class="stat-card"><small>0-60 MPH</small><h3>{data["specs"]["zero_sixty"]}</h3></div>', unsafe_allow_html=True)
            p4.markdown(f'<div class="stat-card"><small>TOP SPEED</small><h3>{data["specs"]["top"]}</h3></div>', unsafe_allow_html=True)

            st.markdown(f'<div class="insight-box"><b>Valuation Logic:</b> {data["why"]}</div>', unsafe_allow_html=True)

        except:
            st.error("Market data sync error. Please try again.")
