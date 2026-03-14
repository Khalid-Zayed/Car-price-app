import streamlit as st
from groq import Groq
import os

# --- AUTHENTICATION ---
groq_key = st.secrets.get("GROQ_API_KEY")
if groq_key:
    client = Groq(api_key=groq_key)

# --- THE "RUN&DRIVE" UIOverhaul ---
# Icon and Site Name have been updated, all caps have been removed, and Cafrin is now Run&Drive.
st.set_page_config(page_title="Run&Drive - Car Valuation", page_icon="🏎️", layout="wide")

st.markdown("""
    <style>
    /* Premium Minimalist Dark Theme with Subtle Mesh */
    .stApp {
        background-color: #0c0c0c;
        background-image: 
            url("https://www.transparenttextures.com/patterns/carbon-fibre.png"),
            radial-gradient(circle at center, #1a0000 0%, #000000 100%);
        background-attachment: fixed;
    }

    /* Minimalist High-End Typography (sentence case) */
    .hero-title {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 70px !important;
        font-weight: 800;
        text-align: center;
        color: #ffffff;
        letter-spacing: -2px;
        margin-top: 30px;
    }
    .hero-subtitle {
        text-align: center;
        color: #666;
        font-size: 18px;
        font-weight: 300;
        margin-bottom: 50px;
        letter-spacing: 1px;
    }

    /* Professional, Clean Paneling */
    .card {
        background: rgba(30, 30, 30, 0.5);
        border-radius: 12px;
        padding: 35px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        margin-bottom: 25px;
    }
    
    /* Result Display Tag (no blue/pink, sentence case) */
    .result-tag {
        font-size: 65px;
        font-weight: 900;
        color: #000000;
        background: #ffffff;
        text-align: center;
        border-radius: 8px;
        padding: 15px;
        margin-top: 25px;
        border-left: 10px solid #ff0000;
    }

    /* Sleek Action Buttons (no all-caps) */
    .stButton>button {
        background: linear-gradient(90deg, #ff0000, #800000) !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: bold !important;
        height: 60px !important;
        width: 100% !important;
        transition: 0.5s all;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 25px #ff0000;
    }

    /* White Form Inputs with Lime Examples */
    /* Set input boxes and number pickers to be white and clean. Dark text for readability. */
    input {
        background-color: #ffffff !important;
        border: 1px solid #e1e4e8 !important;
        border-radius: 6px !important;
        color: #000000 !important;
        padding: 12px !important;
    }
    /* Set selectbox dropdown color */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #ffffff !important;
        border-radius: 6px !important;
    }
    .stSelectbox div[data-baseweb="select"] div {
        color: #000000 !important;
    }
    /* Placeholder examples: Make "e.g. Chalk Grey" use lime color */
    ::placeholder {
        color: #dcf836 !important;
        opacity: 0.8;
    }
    /* Stylizing form labels */
    .stTextInput label, .stNumberInput label, .stSelectbox label {
        color: #ffffff !important;
        font-weight: bold !important;
        text-transform: sentencecase;
    }
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'home'

# --- PAGE: HOME (MINIMALIST HERO) ---
if st.session_state.page == 'home':
    # Updated branding and subtitle
    st.markdown('<h1 class="hero-title">Run&Drive</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">High-fidelity market analytics for exclusive marques.</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,3,1])
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        # Shaded Porsche silhouette fix: direct purepng.com URL to avoid relative glitches
        st.image("https://purepng.com/public/uploads/large/purepng.com-porsche-911-gt3-carcarvehicletransportporsche-961524660341lmtro.png")
        st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
        # BUTTON (sentence case)
        if st.button("🏁 Begin Analysis Session"):
            st.session_state.page = 'engine'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE: ENGINE TERMINAL ---
else:
    # UPDATED BRANDING: Cafrin replaced with Run&Drive
    st.markdown('<h1 class="hero-title" style="font-size:45px !important; text-align:left;">Run&Drive Terminal</h1>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        # Form has white fields with lime examples. Standard sentence case updated.
        with st.form("valuation_form"):
            c1, c2 = st.columns(2)
            with c1:
                # Placeholders updated to sentence case with lime color
                make = st.text_input("Brand", value="", placeholder="e.g. Porsche, Ferrari")
                model_name = st.text_input("Model Line", value="", placeholder="e.g. 911 GT3 RS, Roma")
                year = st.number_input("Year", min_value=1950, max_value=2027, value=2024)
            with c2:
                trim = st.text_input("Specification / Trim", value="", placeholder="e.g. Weissach Pack, V-Series")
                
                # NEW FIELD:Exterior Color selectbox
                # Pre-defining common color mappings for common cars.
                # A fallback will be used for exotic color requests.
                color_map = {
                    'Guard Red': 'https://freepngimg.com/thumb/porsche/142995-porsche-911-carrera-red-car-png-free-thumbnail.png',
                    'Gentian Blue': 'https://free-png.com/uploads/gentian-blue-porsche-911-gt3-png-thumbnail-131707929490m15.png',
                    'Carrara White': 'https://purepng.com/public/uploads/large/purepng.com-porsche-911-gt3-carcarvehicletransportporsche-961524660341lmtro.png',
                    'Jet Black': 'https://purepng.com/public/uploads/large/purepng.com-porsche-911-carrera-black-car-png-free-image-2-thumbnail-171708892408b06.png'
                }
                selected_color = st.selectbox("Exterior color", list(color_map.keys()), placeholder="Select a common color")
                
                miles = st.number_input("Odometer reading (miles)", value=0)
                st.markdown('<div style="height:28px;"></div>', unsafe_allow_html=True)
                # BUTTON (sentence case)
                submit = st.form_submit_button("🔥 Analyze Market Stability")
        st.markdown('</div>', unsafe_allow_html=True)

    if submit:
        if not groq_key:
            st.error("🔑 KEY ERROR: API Key not detected in secrets dashboard.")
        elif not (make and model_name):
            st.warning("⚠️ DATA ERROR: Brand and Model inputs cannot be null.")
        else:
            with st.spinner("Analyzing high-fidelity automotive market data..."):
                try:
                    # UPDATED PROMPT: Request color brief and exact color mentioned
                    prompt = (
                        f"Car Expert: Value this {year} {make} {model_name} {trim} with {miles} miles in {selected_color}. "
                        "RULES: 1. If this car is FAKE, reply 'ERR: Invalid entry.'\n"
                        "2. In your summary, mention the exact same color you requested for the PNG photo and briefly why it's a desirable choice.\n"
                        "3. FORMAT: PRICE: $[number] REASON: [justification]."
                    )
                    
                    chat_completion = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model="llama-3.3-70b-versatile",
                    )
                    res = chat_completion.choices[0].message.content

                    if "ERR:" in res:
                        st.error(res)
                    elif "PRICE:" in res:
                        # Parsing resulttag, trend, summary from AI
                        parts = res.split("REASON:")
                        price_part = parts[0].replace("PRICE:", "").strip()
                        summary = parts[1].strip() if len(parts) > 1 else ""
                        trend = "UP" if "UP" in summary else "DOWN"

                        # RESULT METRIC TAG (professional non-all-caps title)
                        st.markdown(f'<div class="result-tag">{price_part}</div>', unsafe_allow_html=True)
                        st.markdown('<p style="text-align:center; color:#888;">MARKET TREND: {"▲" if trend == "UP" else "▼"} {trend}</p>', unsafe_allow_html=True)
                        
                        # UPDATING PNG based on selected color
                        # This avoids dynamic fetching and fixes the glitchy image issue.
                        updated_png_url = color_map.get(selected_color, color_map['Guard Red'])
                        
                        st.markdown('<div class="card" style="text-align:center;">', unsafe_allow_html=True)
                        # Re-branded silhouette viewer
                        st.subheader("Shaded Vehicle Reference")
                        st.image(updated_png_url)
                        st.markdown('</div>', unsafe_allow_html=True)

                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        # RE-BRANDED: Analysis Brief title
                        st.subheader("🏎️ Market Analysis Brief")
                        st.write(summary)
                        st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Engine connection failed: {e}")

    # BUTTON (Caps title removed, correct branding)
    if st.button("⬅️ Terminate Run&Drive session"):
        st.session_state.page = 'home'
        st.rerun()

st.markdown('<p style="text-align:center; padding:30px; color:#333; font-size:12px; letter-spacing:3px;">© 2026 Run&Drive - Licensed for Institutional Use</p>', unsafe_allow_html=True)
