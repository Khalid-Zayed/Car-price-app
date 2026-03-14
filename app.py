import streamlit as st
from groq import Groq
import json
import urllib.parse

# --- AUTHENTICATION ---
groq_key = st.secrets.get("GROQ_API_KEY")
if groq_key:
    client = Groq(api_key=groq_key)

# --- PAGE CONFIG & LIGHT MODE UI ---
st.set_page_config(page_title="CarFin Analytics", page_icon="🚘", layout="wide", initial_sidebar_state="collapsed")

# Injecting complex CSS to mirror the light-mode CarFin UI
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* Global Light Theme */
    .stApp {
        background-color: #f3f4f6; /* Light gray background */
        color: #111827;
        font-family: 'Inter', sans-serif;
    }

    /* Top Navigation Bar Simulation */
    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 20px;
        background-color: #f3f4f6;
        margin-bottom: 20px;
    }
    .nav-icons {
        display: flex;
        gap: 15px;
        background: white;
        padding: 8px 15px;
        border-radius: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    /* White Panel Cards */
    .carfin-card {
        background-color: #ffffff;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }

    /* Left Side Typography */
    .car-title { font-size: 28px; font-weight: 800; margin: 0; padding: 0; color: #111827; }
    .car-subtitle { font-size: 14px; color: #6b7280; margin-top: -5px; margin-bottom: 20px; }
    
    /* Price Display */
    .price-label { font-size: 12px; color: #9ca3af; text-transform: uppercase; font-weight: 600; }
    .price-value { font-size: 28px; font-weight: 800; color: #111827; margin-bottom: 20px; }
    
    /* Highlight Yellow (from reference image) */
    .highlight-yellow {
        background-color: #dcf836;
        padding: 12px;
        border-radius: 12px;
        font-weight: 600;
        text-align: center;
        margin-bottom: 15px;
    }

    /* Specs Grid */
    .spec-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 15px;
        margin-top: 20px;
    }
    .spec-box {
        background: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 15px;
        text-align: left;
    }
    .spec-box-value { font-size: 14px; font-weight: 700; color: #111827; }
    .spec-box-label { font-size: 11px; color: #6b7280; margin-top: 4px; }

    /* Right Side Search/Chat Panel */
    .search-panel {
        background-color: #ffffff;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
        height: 100%;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
# Default to the Audi R8 view from your image if no search has occurred
if 'current_car' not in st.session_state:
    st.session_state.current_car = {
        "title": "Audi R8 2017",
        "subtitle": "II generation",
        "price": "$ 85,642.11",
        "delivery": "$ 10,874.42",
        "mileage": "12,000 km",
        "engine": "2 liters Gasoline",
        "fuel": "city 11 route 7.5",
        "color": "Gray metallic",
        # Using a reliable transparent car placeholder for the default state
        "image_url": "https://freepngimg.com/thumb/audi/35-audi-png-car-image-thumb.png" 
    }

def fetch_car_data(make, model, year, trim, mileage):
    """Hits the Groq API to estimate stats and format them as JSON"""
    prompt = f"""
    You are an automotive data API. The user is querying a {year} {make} {model} {trim} with {mileage} miles.
    Return ONLY a valid JSON object with realistic estimated data for this specific car. Do not add markdown blocks or conversational text.
    
    Required JSON keys:
    "title": "{make} {model} {year}"
    "subtitle": "Generation or Trim info"
    "price": "Estimated price formatted like '$ 45,000.00'"
    "delivery": "Random delivery fee formatted like '$ 1,200.00'"
    "mileage": "The requested mileage formatted with 'mi' or 'km'"
    "engine": "Engine specs (e.g., '3.0L V6 Turbo')"
    "fuel": "Estimated MPG or L/100km"
    "color": "A typical factory color for this car"
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.2
        )
        response_text = chat_completion.choices[0].message.content
        # Strip potential markdown formatting if Llama disobeys
        if response_text.startswith("```json"):
            response_text = response_text[7:-3]
        
        data = json.loads(response_text)
        
        # --- IMAGE FETCHING LOGIC ---
        # Since we can't easily scrape a perfect transparent PNG dynamically, 
        # we generate a reliable search query URL or use a generic fallback.
        # In a production app, replace this with a Google Custom Search API call.
        query = urllib.parse.quote(f"{make} {model} png transparent")
        data["image_url"] = f"[https://purepng.com/public/uploads/large/purepng.com-porsche-911-gt3-carcarvehicletransportporsche-961524660341lmtro.png](https://purepng.com/public/uploads/large/purepng.com-porsche-911-gt3-carcarvehicletransportporsche-961524660341lmtro.png)" # Using a high-quality transparent fallback for demonstration
        
        return data
    except Exception as e:
        return {"error": str(e)}

# --- TOP NAVIGATION ---
st.markdown("""
<div class="top-nav">
    <div style="font-weight: 800; font-size: 20px;">⌘ CarFin</div>
    <div class="nav-icons">
        <span>🏠</span> <span>⚙️</span> <span style="background: black; color: white; border-radius: 5px; padding: 0 5px;">🔎</span> <span>📱</span> <span>📋</span>
    </div>
    <div>👤 User Profile</div>
</div>
""", unsafe_allow_html=True)

# --- MAIN LAYOUT ---
col_left, col_right = st.columns([6.5, 3.5], gap="large")

with col_left:
    car = st.session_state.current_car
    
    # Header
    st.markdown(f'<p class="car-title">{car.get("title", "Unknown Car")}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="car-subtitle">{car.get("subtitle", "Details unavailable")}</p>', unsafe_allow_html=True)
    
    # Car Image
    # Using mix-blend-mode just in case the image fetched isn't perfectly transparent
    st.markdown(f"""
        <div style="text-align: center; margin: 40px 0; min-height: 250px; display: flex; align-items: center; justify-content: center;">
            <img src="{car.get('image_url')}" style="max-width: 90%; max-height: 350px; object-fit: contain; mix-blend-mode: multiply; filter: drop-shadow(0px 20px 10px rgba(0,0,0,0.2));">
        </div>
    """, unsafe_allow_html=True)
    
    # Price Row
    c1, c2, c3 = st.columns([1.5, 1.5, 4])
    with c1:
        st.markdown('<div class="price-label">Price</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="price-value">{car.get("price", "$0.00")}</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="price-label">Delivery</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="price-value" style="font-size: 20px; padding-top: 8px;">{car.get("delivery", "$0.00")}</div>', unsafe_allow_html=True)
        
    # Specs Grid
    st.markdown(f"""
    <div class="spec-grid">
        <div class="spec-box">
            <div>⏱️</div>
            <div class="spec-box-value">{car.get("mileage", "N/A")}</div>
            <div class="spec-box-label">Mileage of the car</div>
        </div>
        <div class="spec-box">
            <div>⚙️</div>
            <div class="spec-box-value">{car.get("engine", "N/A")}</div>
            <div class="spec-box-label">The engine</div>
        </div>
        <div class="spec-box">
            <div>⛽</div>
            <div class="spec-box-value">{car.get("fuel", "N/A")}</div>
            <div class="spec-box-label">Fuel consumption</div>
        </div>
        <div class="spec-box">
            <div>🎨</div>
            <div class="spec-box-value">{car.get("color", "N/A")}</div>
            <div class="spec-box-label">Color</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)
    
    # Bottom Analytics Tabs
    st.markdown("""
    <div style="display: flex; gap: 10px; margin-bottom: 15px;">
        <div style="padding: 5px 15px; border-bottom: 2px solid black; font-weight: 600; font-size: 14px;">Analytics</div>
        <div style="padding: 5px 15px; color: gray; font-size: 14px;">Delivery ✕</div>
        <div style="padding: 5px 15px; color: gray; font-size: 14px;">Car history ✕</div>
    </div>
    """, unsafe_allow_html=True)
    
    ac1, ac2, ac3 = st.columns(3)
    with ac1:
        st.markdown('<div class="carfin-card"><p style="font-size: 12px; color: gray; margin:0;">Revenue breakdown</p><h4 style="margin-top:0;">$ 42,914</h4><div style="width:100%; background:#f3f4f6; height:20px; border-radius:10px;"><div style="width:85%; background:#dcf836; height:100%; border-radius:10px;"></div></div></div>', unsafe_allow_html=True)
    with ac2:
        st.markdown('<div class="carfin-card"><p style="font-size: 12px; color: gray; margin:0;">Sales trends</p><h4 style="margin-top:0;">+14.2%</h4><div style="height: 20px; background: linear-gradient(90deg, #f3f4f6 50%, #dcf836 50%); border-radius: 5px;"></div></div>', unsafe_allow_html=True)
    with ac3:
        st.markdown('<div class="carfin-card"><p style="font-size: 12px; color: gray; margin:0;">Market volume</p><h4 style="margin-top:0;">Active</h4><div style="height: 20px; background: #dcf836; border-radius: 5px; width: 60%;"></div></div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="search-panel">', unsafe_allow_html=True)
    
    st.markdown('<p style="font-weight: 600; margin-bottom: 20px;">🔍 Search for a car</p>', unsafe_allow_html=True)
    
    # The Chat/Input Form
    with st.form("car_search_form"):
        st.markdown('<p style="font-size: 14px; color: gray; margin-bottom: 5px;">"Can you help me find the market value and specs for..."</p>', unsafe_allow_html=True)
        
        make = st.text_input("Brand", placeholder="e.g. Porsche")
        model_name = st.text_input("Model", placeholder="e.g. 911")
        
        c_year, c_miles = st.columns(2)
        with c_year:
            year = st.number_input("Year", min_value=1950, max_value=2026, value=2024)
        with c_miles:
            miles = st.number_input("Mileage", min_value=0, value=12000)
            
        trim = st.text_input("Trim/Spec", placeholder="e.g. GT3 RS")
        
        st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
        
        # Style the submit button to match the yellow theme
        submit = st.form_submit_button("Search Network", use_container_width=True)
        
    if submit:
        if not make or not model_name:
            st.warning("Please enter at least a Brand and Model.")
        else:
            with st.spinner("AI scanning web for specs and imagery..."):
                new_data = fetch_car_data(make, model_name, year, trim, miles)
                
                if "error" in new_data:
                    st.error(f"Failed to fetch data: {new_data['error']}")
                else:
                    st.session_state.current_car = new_data
                    st.rerun()
                    
    # Audio Wave Graphic Simulation
    st.markdown("""
        <div style="margin-top: 30px; display: flex; align-items: center; gap: 10px;">
            <div style="background: black; color: white; border-radius: 20px; padding: 5px 15px; font-size: 12px;">GPT-4o</div>
            <div style="color: gray; font-size: 12px;">GPT-3.5</div>
        </div>
        <div style="background: #dcf836; border-radius: 12px; padding: 15px; margin-top: 15px; display: flex; align-items: center; justify-content: center; gap: 5px;">
            <span>⏸️</span>
            <div style="flex-grow: 1; height: 10px; background: rgba(0,0,0,0.1); border-radius: 5px; display:flex; gap:2px; overflow:hidden;">
                <div style="width:2px; height:8px; background:black;"></div>
                <div style="width:2px; height:12px; background:black;"></div>
                <div style="width:2px; height:6px; background:black;"></div>
                <div style="width:2px; height:10px; background:black;"></div>
                <div style="width:2px; height:4px; background:black;"></div>
                <div style="width:2px; height:10px; background:black;"></div>
            </div>
            <span style="font-size: 12px; font-weight: 600;">00:14</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
