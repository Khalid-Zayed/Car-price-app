import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS

# --- 1. SETUP ---
groq_key = st.secrets.get("GROQ_API_KEY")
client_groq = Groq(api_key=groq_key)

st.set_page_config(page_title="Run&Drive AI | Market Analyst", layout="wide")

# --- 2. ENHANCED CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;900&display=swap');
    .stApp { background-color: #ffffff; }
    #MainMenu, footer, header, .stDeployButton, div[data-testid="stToolbar"] {visibility: hidden; display: none;}
    
    .main-title { font-family: 'Montserrat', sans-serif; font-size: 4rem; color: #000000; text-align: center; margin-bottom: 5px; }
    .sub-title { font-family: 'Montserrat', sans-serif; font-size: 1rem; color: #32cd32; text-align: center; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 30px; }
    
    .stat-card { background: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #eee; border-bottom: 4px solid #32cd32; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.03); }
    .stat-card small { color: #666; font-weight: 800; text-transform: uppercase; font-size: 0.7rem; }
    .stat-card h1 { color: #000; margin: 5px 0; font-weight: 900; font-size: 2.2rem; }
    
    .insight-box { background: #f9f9f9; padding: 25px; border-radius: 15px; border-left: 5px solid #32cd32; margin-top: 20px; }
    .insight-title { font-weight: 900; text-transform: uppercase; color: #000; margin-bottom: 10px; display: block; }
    .insight-text { color: #444; line-height: 1.6; font-size: 0.95rem; }

    div.stButton > button:first-child { background-color: #000 !important; color: white !important; font-weight: 900; width: 100% !important; border-radius: 8px !important; border: none; height: 3.5rem; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HELPER FUNCTIONS ---
def search_market(query):
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=3)]
            return "\n".join([f"{r['title']}: {r['body']}" for r in results])
    except: return "No live data found."

# --- 4. UI LAYOUT ---
st.markdown('<h1 class="main-title">Run&Drive</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Live Market Intelligence 2026</p>', unsafe_allow_html=True)

with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        brand = st.text_input("Brand", placeholder="e.g. Maserati")
        year = st.number_input("Year", 1900, 2026, 2024)
    with col2:
        model = st.text_input("Model", placeholder="e.g. Ghibli")
        trim = st.text_input("Trim / Version", placeholder="e.g. Trofeo / Modena")
    with col3:
        miles = st.number_input("Mileage", min_value=0, value=0)
        submit = st.button("ANALYZE MARKET VALUE")

# --- 5. EXECUTION ---
if submit and brand and model:
    with st.spinner("Accessing Global Market Data..."):
        # Live Search with Trim
        full_name = f"{year} {brand} {model} {trim}"
        search_data = search_market(f"current price {full_name} {miles} miles 2026")
        
        try:
            prompt = f"""
            Act as a Professional Car Appraiser. Use this search data: {search_data}
            Evaluate: {full_name} with {miles} miles.
            
            Return ONLY this format:
            PRICE: [Value]
            TREND: [Bullish/Bearish/Stable]
            SPECS: [Engine]/[HP]/[0-60]/[Top Speed]
            WHY: [2-sentence explanation of why this price was chosen based on mileage and trim rarity]
            """
            
            response = client_groq.chat.completions.create(
                messages=[{"role":"user","content":prompt}],
                model="llama-3.3-70b-versatile",
                temperature=0.1
            ).choices[0].message.content

            # Data Parsing
            price = response.split("PRICE:")[1].split("TREND:")[0].strip()
            trend = response.split("TREND:")[1].split("SPECS:")[0].strip()
            specs = response.split("SPECS:")[1].split("WHY:")[0].strip().split("/")
            why = response.split("WHY:")[1].strip()

            # --- DISPLAY RESULTS ---
            st.markdown(f"<h2 style='text-align:center; margin-top:40px;'>{full_name}</h2>", unsafe_allow_html=True)
            
            res_col1, res_col2 = st.columns(2)
            res_col1.markdown(f'<div class="stat-card"><small>ESTIMATED VALUE</small><h1 style="color:#32cd32;">{price}</h1></div>', unsafe_allow_html=True)
            res_col2.markdown(f'<div class="stat-card"><small>MARKET TREND</small><h1>{trend}</h1></div>', unsafe_allow_html=True)

            # Performance Row
            st.write("")
            p1, p2, p3, p4 = st.columns(4)
            p1.markdown(f'<div class="stat-card"><small>ENGINE</small><h3>{specs[0]}</h3></div>', unsafe_allow_html=True)
            p2.markdown(f'<div class="stat-card"><small>POWER</small><h3>{specs[1]}</h3></div>', unsafe_allow_html=True)
            p3.markdown(f'<div class="stat-card"><small>0-60</small><h3>{specs[2]}</h3></div>', unsafe_allow_html=True)
            p4.markdown(f'<div class="stat-card"><small>TOP SPEED</small><h3>{specs[3]}</h3></div>', unsafe_allow_html=True)

            # WHY Section
            st.markdown(f"""
                <div class="insight-box">
                    <span class="insight-title">🔍 Valuation Insight</span>
                    <p class="insight-text">{why}</p>
                </div>
            """, unsafe_allow_html=True)

        except:
            st.error("Market data timeout. Please try again.")
