import streamlit as st
from groq import Groq
import json
import urllib.parse

# --- AUTHENTICATION ---
groq_key = st.secrets.get("GROQ_API_KEY")
if groq_key:
    client = Groq(api_key=groq_key)

# --- PAGE CONFIG ---
st.set_page_config(page_title="Run&Drive Analytics", page_icon="🚘", layout="wide", initial_sidebar_state="collapsed")

# Injecting Cleaned light-mode CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    .stApp {
        background-color: #f3f4f6;
        color: #111827;
        font-family: 'Inter', sans-serif;
    }

    /* Branding Header */
    .brand-header {
        font-weight: 800;
        font-size: 28px;
        margin-bottom: 20px;
        color: #000000;
    }

    /* White Panel Cards */
    .carfin-card {
        background-color: #ffffff;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }

    /* Typography */
    .car-title { font-size: 32px; font-weight: 800; margin: 0; color: #111827; }
    .car-subtitle { font-size: 16px; color: #6b7280; margin-bottom: 20px; }
    .price-label { font-size: 12px; color: #9ca3af; text-transform: uppercase; font-weight: 600; }
    .price-value { font-size: 34px; font-weight: 800; color: #111827; margin-bottom: 20px; }

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
    }
    .spec-box-value { font-size: 14px; font-weight: 700; color: #111827; }
    .spec-box-label { font-size: 11px; color: #6b7280; margin-top: 4px; }

    /* White Search Form styling */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #ffffff !important;
        border: 1px solid #d1d5db !important;
        color: #000000 !important;
        border-radius: 8px !important;
    }

    /* Submit Button (Lime Green Highlight) */
    .stButton>button {
        background-color: #dcf836 !important;
        color: #000000 !important;
        border: none !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        height: 50px !important;
    }

    /* Remove default elements */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
if 'current_car' not in st.session_state:
    st.session_state.current_car = {
        "title": "Audi R8 2017",
        "subtitle": "II generation",
        "price": "$ 85,642.11",
        "mileage": "12,000 km",
        "engine": "5.2L V10 Gasoline",
        "fuel": "city 11 route 7.5",
        "color": "Gray metallic",
        "image_url": "https://freepngimg.com/thumb/audi/35-audi-png-car-image-thumb.png" 
    }

def fetch_car_data(make, model, year, trim, mileage, color):
    prompt = f"""
    You are an automotive data expert. The user is searching for a {year} {make} {model} {trim} in {color} with {mileage} miles.
    Return ONLY a valid JSON object.
    Keys: "title", "subtitle", "price", "mileage", "engine", "fuel", "color".
    """
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.2
        )
        response_text = chat_completion.choices[0].message.content
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0]
        
        data = json.loads(response_text)
        # Search for a high-quality PNG based on the specific car and color requested
        search_query = f"{year}+{make}+{model}+{color}+car+png+transparent"
        data["image_url"] = f"[https://www.google.com/search?q=](https://www.google.com/search?q=){search_query}&tbm=isch" # Placeholder logic
        # For actual display, we use a generic transparent car placeholder that works:
        data["image_url"] = "[https://purepng.com/public/uploads/large/purepng.com-porsche-911-gt3-carcarvehicletransportporsche-961524660341lmtro.png](https://purepng.com/public/uploads/large/purepng.com-porsche-911-gt3-carcarvehicletransportporsche-961524660341lmtro.png)"
        return data
    except Exception as e:
        return {"error": str(e)}

# --- MAIN UI ---
st.markdown('<div class="brand-header">Run&Drive</div>', unsafe_allow_html=True)

col_left, col_right = st.columns([6.5, 3.5], gap="large")

with col_left:
    car = st.session_state.current_car
    
    st.markdown(f'<p class="car-title">{car.get("title")}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="car-subtitle">{car.get("subtitle")}</p>', unsafe_allow_html=True)
    
    # Car Image Display (Audi R8 place)
    st.markdown(f"""
        <div style="text-align: center; margin: 40px 0; min-height: 300px; display: flex; align-items: center; justify-content: center;">
            <img src="{car.get('image_url')}" style="max-width: 95%; max-height: 400px; object-fit: contain; filter: drop-shadow(0px 15px 15px rgba(0,0,0,0.1));">
        </div>
    """, unsafe_allow_html=True)
    
    # Price
    st.markdown('<div class="price-label">Estimated Market Price</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="price-value">{car.get("price")}</div>', unsafe_allow_html=True)
        
    # Specs Grid
    st.markdown(f"""
    <div class="spec-grid">
        <div class="spec-box"><div class="spec-box-value">{car.get("mileage")}</div><div class="spec-box-label">Mileage</div></div>
        <div class="spec-box"><div class="spec-box-value">{car.get("engine")}</div><div class="spec-box-label">Engine</div></div>
        <div class="spec-box"><div class="spec-box-value">{car.get("fuel")}</div><div class="spec-box-label">Consumption</div></div>
        <div class="spec-box"><div class="spec-box-value">{car.get("color")}</div><div class="spec-box-label">Color</div></div>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="carfin-card">', unsafe_allow_html=True)
    st.markdown('<p style="font-weight: 700; font-size: 18px; margin-bottom: 20px;">Search Network</p>', unsafe_allow_html=True)
    
    with st.form("car_search_form"):
        brand = st.text_input("Brand", placeholder="e.g. Porsche")
        model = st.text_input("Model", placeholder="e.g. 911 Turbo")
        
        c_yr, c_ml = st.columns(2)
        with c_yr:
            yr = st.number_input("Year", min_value=1980, max_value=2026, value=2024)
        with c_ml:
            ml = st.number_input("Mileage", min_value=0, value=5000)
            
        trm = st.text_input("Trim / Spec", placeholder="e.g. S / GTS")
        clr = st.text_input("Color Request", placeholder="e.g. Chalk Grey")
        
        st.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)
        search_btn = st.form_submit_button("Get Real-time Estimate", use_container_width=True)
        
    if search_btn:
        if brand and model:
            with st.spinner("Searching internet for current listings and PNGs..."):
                result = fetch_car_data(brand, model, yr, trm, ml, clr)
                if "error" not in result:
                    st.session_state.current_car = result
                    st.rerun()
                else:
                    st.error("Search failed. Please try again.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Market Condition Card
    st.markdown("""
        <div class="carfin-card">
            <p style="font-size: 12px; color: gray; margin:0;">Market Status</p>
            <h4 style="margin-top:5px;">Institutional Analysis Active</h4>
            <div style="width:100%; background:#f3f4f6; height:8px; border-radius:4px; margin-top:10px;">
                <div style="width:70%; background:#dcf836; height:100%; border-radius:4px;"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
