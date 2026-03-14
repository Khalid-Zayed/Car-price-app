import streamlit as st
from groq import Groq
import os

# --- AUTHENTICATION ---
groq_key = st.secrets.get("GROQ_API_KEY")
if groq_key:
    client = Groq(api_key=groq_key)

# --- THE "CARFIN" DASHBOARD UI ---
st.set_page_config(page_title="CarFin Analytics Dashboard", page_icon="🏎️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;800&display=swap');

    /* Premium Minimalist Dark Theme */
    .stApp {
        background-color: #0c0d0f;
        color: #e0e2e7;
        font-family: 'Inter', sans-serif;
    }

    /* Minimalist High-End Typography */
    .dashboard-title {
        font-size: 38px !important;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -1px;
    }
    .metric-value {
        font-size: 55px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -3px;
    }

    /* Complex Analytics Cards */
    .analytics-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 25px;
        backdrop-filter: blur(10px);
    }
    .spec-item {
        border-bottom: 1px solid #1a1c21;
        padding: 12px 0;
        display: flex;
        justify-content: space-between;
        color: #9ea4b0;
    }
    .spec-val { color: #fff; font-weight: 600; }

    /* Search Input Overrides */
    input {
        background-color: #000 !important;
        border: 1px solid #282a31 !important;
        color: white !important;
    }
    
    /* Interactive Button */
    .stButton>button {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: bold !important;
        height: 50px !important;
        transition: 0.3s all;
    }
    .stButton>button:hover {
        background-color: #cccccc !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DASHBOARD HEADER ---
st.markdown('<div style="height:40px;"></div>', unsafe_allow_html=True)
c1, c2 = st.columns([8, 2])
with c1:
    st.markdown('<h1 class="dashboard-title">CarFin Analytics</h1>', unsafe_allow_html=True)
with c2:
    st.image("https://images.unsplash.com/photo-1544636331-e26879cd4d9b?auto=format&fit=crop&q=80&w=200", 
             width=180, caption="Profile Active")

st.markdown('<div style="height:30px;"></div>', unsafe_allow_html=True)

# --- MAIN DASHBOARD LAYOUT (analytics_form to simulate search) ---
col_main, col_search = st.columns([6, 4])

with col_main:
    with st.form("analytics_form"):
        # Direct Car Identification Input
        make = st.text_input("MANUFACTURER", value="", placeholder="e.g. Porsche")
        model_name = st.text_input("MODEL LINE", value="", placeholder="e.g. 911 GT3")
        year = st.number_input("PRODUCTION YEAR", min_value=1950, max_value=2027, value=2024)
        trim = st.text_input("SPECIFICATION", value="", placeholder="e.g. Touring Pack")
        miles = st.number_input("TOTAL MILES", value=0)
        
        # Action button mimics the "Can you help me find a reliable car..." search
        submit = st.form_submit_button("🔥 INITIATE AI MARKET SCAN")

with col_search:
    st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
    st.markdown("### Search Parameters")
    st.write("Current Focus: Reliable vehicles under $100,000 USD with good mileage.")
    st.write("Market Condition: Neutral Trend Detected.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="height:30px;"></div>', unsafe_allow_html=True)

if submit:
    if not (make and model_name):
        st.warning("Identification failed: Please enter Manufacturer and Model.")
    else:
        with st.spinner("Accessing technical spec and market history neural data..."):
            try:
                # INTEGRATED PROMPT: Requesting 0-60 Time, Specs, Price, and Validation.
                prompt = (
                    f"Market Analyst: Value and spec a {year} {make} {model_name} {trim} with {miles} miles. "
                    "RULES:\n"
                    "1. If this car is FAKE, reply 'ERR: This vehicle does not exist.'\n"
                    "2. Request 0-60 time, power output, drivetrain, and a professional market description.\n"
                    "3. If real, reply: PRICE: $[number] | DATA: [Power]/[0-60 MPH]/[Drivetrain] | SUMMARY: [Professional Description]."
                )
                
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile",
                )
                raw = chat_completion.choices[0].message.content

                if "ERR:" in raw:
                    st.error(raw)
                elif "PRICE:" in raw:
                    # Parsing new high-spec format
                    price = raw.split("|")[0].replace("PRICE:", "").strip()
                    data_points = raw.split("DATA:")[1].split("|")[0].strip().split("/")
                    summary = raw.split("SUMMARY:")[1].strip()

                    # Result Display mirroring the metrics in image_14.png
                    col_price, col_specs = st.columns([3, 2])
                    with col_price:
                        st.markdown('<div class="metric-value">Market Valuation</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="metric-value">{price}</div>', unsafe_allow_html=True)
                        
                        st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
                        st.markdown('### Executive Summary')
                        st.write(summary)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with col_specs:
                        # Technical spec fields instead of basic mileage
                        st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
                        st.markdown('### Institutional Technical Data')
                        spec_labels = ["Configuration", "Power Output", "Acceleration (0-60 MPH)", "Drive Type"]
                        for label, val in zip(spec_labels, [data_points[0]] + data_points[1:]):
                            st.markdown(f'<div class="spec-item">{label} <span class="spec-val">{val}</span></div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Analysis Failed: {e}")

# --- ANALYTICS FOOTER (Multi-Color Charts Area) ---
st.markdown('<div style="height:30px;"></div>', unsafe_allow_html=True)
col_chart1, col_chart2, col_chart3 = st.columns(3)

with col_chart1:
    st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
    st.markdown("### Revenue breakdown")
    # Simple bar chart component simulation
    st.image("https://images.unsplash.com/photo-1544197150-b99a580bb7a8?auto=format&fit=crop&q=80&w=300", 
             width=250, caption="2025 Market Volume (Institution View)")
    st.markdown('</div>', unsafe_allow_html=True)

with col_chart2:
    st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
    st.markdown("### Sales trends")
    # Live market ticker component simulation
    st.image("https://images.unsplash.com/photo-1611162618071-b39a2ec055fb?auto=format&fit=crop&q=80&w=300", 
             width=250, caption="Trending: Exotic values up 1.2%")
    st.markdown('</div>', unsafe_allow_html=True)

with col_chart3:
    st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
    st.markdown("### Market history")
    st.image("https://images.unsplash.com/photo-1603356033288-acfcb54801e6?auto=format&fit=crop&q=80&w=300", 
             width=250, caption="Data sync: active.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- live ticker and status ---
st.markdown('<p style="text-align:center; padding:30px; color:#222; font-family:monospace;">>> [CARFIN_LINK_ENCRYPTED] | SYSTEM V.3.2 // GREEN_CYAN_RED // AI_SCAN ACTIVE <<</p>', unsafe_allow_html=True)
