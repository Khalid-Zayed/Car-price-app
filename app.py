import streamlit as st
from groq import Groq
import json
import urllib.parse

# --- AUTHENTICATION ---
# Ensure you have "GROQ_API_KEY" in your Streamlit secrets
groq_key = st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=groq_key) if groq_key else None

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="CarFin Analytics", 
    page_icon="🚘", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- ADVANCED CSS (MATCHING UI REFERENCE) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* Global Theme Overrides */
    .stApp {
        background-color: #f8f9fa;
        color: #1a1d23;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Top Navigation */
    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 15px 30px;
        background-color: transparent;
    }
    .nav-brand { font-weight: 800; font-size: 22px; display: flex; align-items: center; gap: 8px; }
    .nav-central-capsule {
        background: white;
        padding: 8px 20px;
        border-radius: 50px;
        display: flex;
        gap: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    }

    /* Left Panel Styling */
    .car-header-section { margin-bottom: 30px; }
    .car-title { font-size: 34px; font-weight: 800; letter-spacing: -1px; margin: 0; color: #111827; }
    .car-subtitle { font-size: 15px; color: #6b7280; font-weight: 500; margin-top: 4px; }

    /* Image Container */
    .image-stage {
        height: 350px;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        margin: 20px 0;
    }
    .car-main-img {
        max-width: 90%;
        max-height: 320px;
        object-fit: contain;
        filter: drop-shadow(0 25px 15px rgba(0,0,0,0.1));
    }

    /* Specs & Pricing */
    .price-block { margin-bottom: 40px; }
    .label-tiny { font-size: 11px; text-transform: uppercase; color: #9ca3af; font-weight: 700; letter-spacing: 1px; }
    .value-large { font-size: 28px; font-weight: 800; color: #111827; }

    .spec-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 15px;
    }
    .spec-card {
        background: white;
        border: 1px solid #edf2f7;
        padding: 18px;
        border-radius: 16px;
        transition: transform 0.2s;
    }
    .spec-card:hover { transform: translateY(-3px); }
    .spec-icon { font-size: 20px; margin-bottom: 10px; }
    .spec-val { font-size: 14px; font-weight: 700; color: #1a202c; }
    .spec-lab { font-size: 11px; color: #718096; margin-top: 2px; }

    /* Right Search Panel */
    .search-container {
        background: white;
        padding: 30px;
        border-radius: 24px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.05);
        border: 1px solid #f1f5f9;
        height: 100%;
    }
    
    /* Interactive Yellow Elements */
    .stButton > button {
        background-color: #dcf836 !important;
        color: #000 !important;
        border: none !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        padding: 12px 20px !important;
        transition: all 0.3s !important;
    }
    .stButton > button:hover {
        background-color: #c9e62e !important;
        transform: scale(1.02);
    }

    /* Audio UI Component */
    .audio-bar {
        background: #dcf836;
        border-radius: 14px;
        padding: 15px;
        display: flex;
        align-items: center;
        gap: 12px;
        margin-top: 25px;
    }
    .wave-sim {
        flex-grow: 1;
        display: flex;
        align-items: center;
        gap: 3px;
        height: 20px;
    }
    .wave-bar { background: black; width: 3px; border-radius: 2px; }

    /* Analytics Bars */
    .stat-bar-bg { background: #f1f5f9; height: 8px; border-radius: 4px; margin-top: 10px; overflow: hidden; }
    .stat-bar-fill { background: #dcf836; height: 100%; border-radius: 4px; }

    </style>
""", unsafe_allow_html=True)

# --- DATA FETCHING ENGINE ---
def get_car_intelligence(make, model, year, trim, mileage):
    if not client:
        return {"error": "API Key missing"}
    
    # Prompting Llama to act as a structured data provider
    prompt = f"""
    Return JSON only. Estimate market data for: {year} {make} {model} {trim} with {mileage} miles.
    Values must be realistic for 2026 market.
    JSON keys: 
    "title", "subtitle", "price_val", "delivery_val", "mileage_display", "engine_desc", "fuel_desc", "color_name", 
    "rev_val", "rev_pct", "sales_trend", "market_status"
    """
    try:
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"}
        )
        res = json.loads(completion.choices[0].message.content)
        
        # Smart Image Logic: Heuristic for transparent car PNGs
        # Note: In a real app, you'd use a dedicated Image Search API here.
        clean_name = f"{make}-{model}-{year}".lower().replace(" ", "-")
        # We use a high-quality fallback that matches the requested car brand via placeholders
        res["img_url"] = f"https://www.pngall.com/wp-content/uploads/2/Porsche-911-PNG-Clipart.png" 
        if "audi" in make.lower():
            res["img_url"] = "https://www.pngall.com/wp-content/uploads/2/Audi-PNG-High-Quality-Image.png"
        elif "bmw" in make.lower():
            res["img_url"] = "https://www.pngall.com/wp-content/uploads/2/BMW-PNG-Transparent-HD-Photo.png"
            
        return res
    except Exception as e:
        return {"error": str(e)}

# --- SESSION STATE INITIALIZATION ---
if 'car_data' not in st.session_state:
    st.session_state.car_data = {
        "title": "Porsche 911 2024",
        "subtitle": "992 Generation, GT3 Trim",
        "price_val": "$ 174,000.00",
        "delivery_val": "$ 2,500.00",
        "mileage_display": "12,000 mi",
        "engine_desc": "4.0L Naturally Aspirated Flat-6",
        "fuel_desc": "15 MPG",
        "color_name": "Guard Red",
        "img_url": "https://www.pngall.com/wp-content/uploads/2/Porsche-911-PNG-Clipart.png",
        "rev_val": "$ 142,000",
        "rev_pct": "85%",
        "sales_trend": "+12.4%",
        "market_status": "Highly Active"
    }

# --- UI LAYOUT ---

# 1. Top Navigation
st.markdown(f"""
<div class="top-nav">
    <div class="nav-brand">⌘ CarFin</div>
    <div class="nav-central-capsule">
        <span>🏠</span><span>⚙️</span>
        <span style="background:black; color:white; padding:0 6px; border-radius:4px;">🔎</span>
        <span>📱</span><span>📋</span>
    </div>
    <div style="font-size:14px; font-weight:600;">👤 User Profile</div>
</div>
""", unsafe_allow_html=True)

main_col, side_col = st.columns([7, 3], gap="large")

with main_col:
    d = st.session_state.car_data
    
    # Header
    st.markdown(f"""
        <div class="car-header-section">
            <h1 class="car-title">{d['title']}</h1>
            <p class="car-subtitle">{d['subtitle']}</p>
        </div>
    """, unsafe_allow_html=True)

    # Car Image Stage
    st.markdown(f"""
        <div class="image-stage">
            <img src="{d['img_url']}" class="car-main-img">
        </div>
    """, unsafe_allow_html=True)

    # Pricing Row
    p1, p2, _ = st.columns([1.5, 1.5, 4])
    with p1:
        st.markdown(f'<p class="label-tiny">Market Price</p><p class="value-large">{d["price_val"]}</p>', unsafe_allow_html=True)
    with p2:
        st.markdown(f'<p class="label-tiny">Delivery</p><p class="value-large" style="font-size:20px; color:#6b7280;">{d["delivery_val"]}</p>', unsafe_allow_html=True)

    # Specs Grid
    st.markdown(f"""
    <div class="spec-grid">
        <div class="spec-card">
            <div class="spec-icon">⏱️</div>
            <div class="spec-val">{d['mileage_display']}</div>
            <div class="spec-lab">Mileage of the car</div>
        </div>
        <div class="spec-card">
            <div class="spec-icon">⚙️</div>
            <div class="spec-val">{d['engine_desc']}</div>
            <div class="spec-lab">The engine</div>
        </div>
        <div class="spec-card">
            <div class="spec-icon">⛽</div>
            <div class="spec-val">{d['fuel_desc']}</div>
            <div class="spec-lab">Fuel consumption</div>
        </div>
        <div class="spec-card">
            <div class="spec-icon">🎨</div>
            <div class="spec-val">{d['color_name']}</div>
            <div class="spec-lab">Factory Color</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Bottom Analytics Section
    st.markdown('<div style="margin-top:40px; border-bottom:1px solid #e2e8f0; display:flex; gap:20px; font-size:14px; font-weight:600; padding-bottom:10px;">'
                '<span style="color:black; border-bottom: 2px solid black; padding-bottom:8px;">Analytics</span>'
                '<span style="color:#a0aec0;">Delivery ✕</span>'
                '<span style="color:#a0aec0;">Car history ✕</span></div>', unsafe_allow_html=True)
    
    a1, a2, a3 = st.columns(3)
    with a1:
        st.markdown(f'<div style="background:white; padding:20px; border-radius:16px; margin-top:20px;">'
                    f'<p class="label-tiny">Revenue Breakdown</p><h3>{d["rev_val"]}</h3>'
                    f'<div class="stat-bar-bg"><div class="stat-bar-fill" style="width:{d["rev_pct"]};"></div></div></div>', unsafe_allow_html=True)
    with a2:
        st.markdown(f'<div style="background:white; padding:20px; border-radius:16px; margin-top:20px;">'
                    f'<p class="label-tiny">Sales Trends</p><h3>{d["sales_trend"]}</h3>'
                    f'<div class="stat-bar-bg"><div class="stat-bar-fill" style="width:60%;"></div></div></div>', unsafe_allow_html=True)
    with a3:
        st.markdown(f'<div style="background:white; padding:20px; border-radius:16px; margin-top:20px;">'
                    f'<p class="label-tiny">Market Volume</p><h3>{d["market_status"]}</h3>'
                    f'<div class="stat-bar-bg"><div class="stat-bar-fill" style="width:90%;"></div></div></div>', unsafe_allow_html=True)

with side_col:
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    st.markdown('<p style="font-weight: 700; font-size: 18px; margin-bottom: 20px;">🔍 Search Network</p>', unsafe_allow_html=True)
    
    with st.form("car_query"):
        st.markdown('<p style="font-size: 13px; color: #718096; line-height: 1.4;">'
                    '"Can you help me find the market value and specs for a specific vehicle?"</p>', unsafe_allow_html=True)
        
        f_make = st.text_input("Brand", value="Porsche", placeholder="e.g. BMW")
        f_model = st.text_input("Model", value="911", placeholder="e.g. M4")
        
        y_col, m_col = st.columns(2)
        f_year = y_col.number_input("Year", 2010, 2026, 2024)
        f_miles = m_col.number_input("Mileage", 0, 200000, 5000)
        
        f_trim = st.text_input("Trim / Spec", placeholder="e.g. Competition")
        
        search_btn = st.form_submit_button("Execute Market Scan", use_container_width=True)
        
        if search_btn:
            with st.spinner("Analyzing Market Data..."):
                results = get_car_intelligence(f_make, f_model, f_year, f_trim, f_miles)
                if "error" not in results:
                    st.session_state.car_data = results
                    st.rerun()
                else:
                    st.error("Connection to Neural Engine failed.")

    # Voice/Audio Widget
    st.markdown(f"""
        <div style="margin-top: 40px; display: flex; align-items: center; gap: 8px;">
            <div style="background: black; color: white; border-radius: 6px; padding: 2px 8px; font-size: 10px; font-weight: 700;">GPT-4o</div>
            <div style="color: #cbd5e0; font-size: 10px; font-weight: 700;">GPT-3.5</div>
        </div>
        <div class="audio-bar">
            <span style="font-size: 14px;">⏸️</span>
            <div class="wave-sim">
                <div class="wave-bar" style="height: 8px;"></div>
                <div class="wave-bar" style="height: 14px;"></div>
                <div class="wave-bar" style="height: 10px;"></div>
                <div class="wave-bar" style="height: 18px;"></div>
                <div class="wave-bar" style="height: 12px;"></div>
                <div class="wave-bar" style="height: 6px;"></div>
                <div class="wave-bar" style="height: 14px;"></div>
            </div>
            <span style="font-size: 12px; font-weight: 800;">00:14</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
