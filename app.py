import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS

# --- 1. SETUP ---
groq_key = st.secrets.get("GROQ_API_KEY")
client_groq = Groq(api_key=groq_key)

st.set_page_config(page_title="Run&Drive AI | Analysis", layout="centered")

# --- 2. THE CUSTOM STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;900&display=swap');
    
    /* Global Page Styling */
    .stApp { background-color: #ffffff; color: #000000; }
    #MainMenu, footer, header, .stDeployButton, div[data-testid="stToolbar"] {visibility: hidden; display: none;}
    
    /* Header Styles */
    .main-title { font-family: 'Montserrat', sans-serif; font-size: 4rem; color: #000000; text-align: center; margin-bottom: 0px; }
    .sub-title { font-family: 'Montserrat', sans-serif; font-size: 1rem; color: #32cd32; text-align: center; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 40px; }
    
    /* Force Black Text for all elements */
    label, p, span, div, .stMarkdown { color: #000000 !important; font-weight: 700; }
    .stTextInput input, .stNumberInput input { color: #000000 !important; border: 1px solid #ddd !important; background-color: #ffffff !important; }

    /* --- THE HOVER BUTTON MAGIC --- */
    div.stButton > button:first-child { 
        background-color: #000000 !important; /* Initial: Black box */
        color: #ffffff !important;           /* Initial: White text */
        font-weight: 900; 
        width: 100% !important; 
        border-radius: 8px !important; 
        height: 3.5rem; 
        border: 2px solid #000000 !important; 
        transition: all 0.3s ease; /* Smooth transition */
        margin-top: 20px;
    }

    div.stButton > button:first-child:hover { 
        background-color: #32cd32 !important; /* Hover: Green box */
        color: #000000 !important;           /* Hover: Black text */
        border: 2px solid #32cd32 !important;
    }

    /* Stat Cards & Insights */
    .stat-card { background: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #eee; border-bottom: 4px solid #32cd32; text-align: center; margin-bottom: 20px; }
    .stat-card small { color: #000000 !important; font-weight: 800; text-transform: uppercase; font-size: 0.75rem; }
    .stat-card h1 { color: #000000 !important; margin: 5px 0; font-weight: 900; font-size: 2.2rem; }
    .green-text { color: #32cd32 !important; }
    .insight-box { background: #f9f9f9; padding: 20px; border-radius: 10px; border-left: 5px solid #32cd32; margin-top: 20px; color: #000 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIC ---
def search_market(query):
    try:
        with DDGS() as ddgs:
            return "\n".join([f"{r['title']}: {r['body']}" for r in ddgs.text(query, max_results=3)])
    except: return "Live data unavailable."

# --- 4. THE VERTICAL FORM ---
st.markdown('<h1 class="main-title">Run&Drive</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Expert Market Intelligence</p>', unsafe_allow_html=True)

# Forms stacked one after another
brand = st.text_input("Car Brand", placeholder="Maserati")
model = st.text_input("Car Model", placeholder="Ghibli")
trim = st.text_input("Trim / Version", placeholder="Trofeo")
year = st.number_input("Year of Manufacture", 1900, 2026, 2024)
miles = st.number_input("Current Odometer (Miles)", min_value=0, value=0)

submit = st.button("RUN LIVE VALUATION")

# --- 5. EXECUTION ---
if submit and brand and model:
    with st.spinner("Analyzing Global Sales..."):
        full_name = f"{year} {brand} {model} {trim}"
        search_data = search_market(f"real price {full_name} {miles} miles 2026")
        
        try:
            prompt = f"""
            Analyst: Act as a Senior Car Appraiser. Use data: {search_data}
            Evaluate: {full_name} with {miles} miles.
            Format: PRICE: [Value] | TREND: [Status] | SPECS: [Eng]/[HP]/[0-60]/[Top] | WHY: [Why this price?]
            """
            
            response = client_groq.chat.completions.create(
                messages=[{"role":"user","content":prompt}],
                model="llama-3.3-70b-versatile",
                temperature=0.1
            ).choices[0].message.content

            # Simple parsing
            price = response.split("PRICE:")[1].split("|")[0].strip()
            trend = response.split("TREND:")[1].split("|")[0].strip()
            specs = response.split("SPECS:")[1].split("|")[0].strip().split("/")
            why = response.split("WHY:")[1].strip()

            # --- DISPLAY RESULTS ---
            st.markdown(f"<h2 style='text-align:center; color:black;'>{full_name}</h2>", unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            c1.markdown(f'<div class="stat-card"><small>MARKET VALUE</small><h1 class="green-text">{price}</h1></div>', unsafe_allow_html=True)
            c2.markdown(f'<div class="stat-card"><small>TREND</small><h1>{trend}</h1></div>', unsafe_allow_html=True)

            sc1, sc2, sc3, sc4 = st.columns(4)
            sc1.markdown(f'<div class="stat-card"><small>ENGINE</small><h3>{specs[0]}</h3></div>', unsafe_allow_html=True)
            sc2.markdown(f'<div class="stat-card"><small>POWER</small><h3>{specs[1]}</h3></div>', unsafe_allow_html=True)
            sc3.markdown(f'<div class="stat-card"><small>0-60</small><h3>{specs[2]}</h3></div>', unsafe_allow_html=True)
            sc4.markdown(f'<div class="stat-card"><small>TOP SPEED</small><h3>{specs[3]}</h3></div>', unsafe_allow_html=True)

            st.markdown(f'<div class="insight-box"><b>Valuation Logic:</b> {why}</div>', unsafe_allow_html=True)

        except:
            st.error("Accuracy timeout. Check details and retry.")
