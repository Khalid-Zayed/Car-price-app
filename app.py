import streamlit as st
import pandas as pd
import joblib
import time

# --- 1. PAGE SETUP & GLOWING UI ---
st.set_page_config(page_title="AutoPredict AI Pro", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at top right, #001f3f, #000000);
        color: #e0e0e0;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
    }
    .stButton>button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 50px;
        font-weight: bold;
        transition: all 0.3s ease-in-out;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 0 20px #00d2ff;
    }
    .ink-title {
        background: -webkit-linear-gradient(#00d2ff, #91eaff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 50px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOAD AI ASSETS ---
@st.cache_resource
def load_assets():
    m = joblib.load('car_price_model.pkl')
    e = joblib.load('encoder.joblib')
    s = joblib.load('scaler.joblib')
    return m, e, s

model, encoder, scaler = load_assets()

if 'history' not in st.session_state:
    st.session_state.history = []

# --- SECTION 1: WELCOME & VIBE ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<h1 class="ink-title">💎 AUTO-PREDICT AI PRO</h1>', unsafe_allow_html=True)
st.write("### The Gold Standard in 2026 Vehicle Valuation.")
st.write("Enter your vehicle details below to run our neural-network market analysis.")
st.markdown('</div>', unsafe_allow_html=True)

# --- SECTION 2: THE SEARCHABLE FORM ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.subheader("🏎️ Vehicle Specifications")

# Full List of 55+ Brands for "Search by itself" feel
all_brands = sorted([
    "Toyota", "Bmw", "Ford", "Mercedes-benz", "Honda", "Nissan", "Chevrolet", 
    "Audi", "Hyundai", "Kia", "Jeep", "Dodge", "Lexus", "Volkswagen", "Mazda", 
    "Gmc", "Infiniti", "Ram", "Subaru", "Chrysler", "Cadillac", "Acura", 
    "Buick", "Lincoln", "Volvo", "Mitsubishi", "Land rover", "Porsche", 
    "Jaguar", "Mini", "Gmc", "Pontiac", "Mercury", "Saturn", "Scion", 
    "Hummer", "Saab", "Suzuki", "Oldsmobile", "Isuzu", "Fiat", "Bentley", 
    "Maserati", "Aston martin", "Tesla", "Ferrari", "Lamborghini", "Rolls-royce"
])

with st.form("main_form"):
    c1, c2, c3 = st.columns(3)
    with c1:
        make = st.selectbox("Manufacturer", options=all_brands)
        year = st.slider("Model Year", 2010, 2026, 2022)
    with c2:
        model_name = st.text_input("Model Name (e.g., Civic, Mustang)", "Camry")
        trans = st.radio("Transmission", ["Automatic", "Manual"], horizontal=True)
    with c3:
        mileage = st.number_input("Odometer (KM)", value=45000)
        cond = st.select_slider("Condition", options=["Poor", "Fair", "Good", "Excellent", "New"], value="Good")

    # Map condition text to numbers for the AI
    cond_map = {"Poor": 1.0, "Fair": 2.0, "Good": 3.0, "Excellent": 4.0, "New": 5.0}
    
    # Placeholders for columns required by the model but not used in UI
    trim = "Base"
    body = "Sedan"

    submitted = st.form_submit_button("CALCULATE VALUE")

if submitted:
    with st.spinner("🧠 Scanning market databases..."):
        # Create input row
        input_df = pd.DataFrame([[year, make, model_name, trim, body, trans, cond_map[cond], mileage]], 
                                columns=["year", "make", "model", "trim", "body", "transmission", "condition", "odometer"])
        
        # Encoding (Handles unseen text safely)
        cat_cols = ["make", "model", "trim", "body", "transmission"]
        input_df[cat_cols] = encoder.transform(input_df[cat_cols].astype(str).apply(lambda x: x.str.capitalize()))
        
        # Scaling & Prediction
        final_input = scaler.transform(input_df)
        price = model.predict(final_input)[0]
        time.sleep(1.2) 
        
        st.balloons()
        st.markdown(f"<h2 style='text-align: center; color: #00d2ff;'>Market Estimate: ${price:,.2f}</h2>", unsafe_allow_html=True)
        
        # Add to Session History
        st.session_state.history.insert(0, {"Vehicle": f"{year} {make} {model_name}", "Price": f"${price:,.2f}"})

st.markdown('</div>', unsafe_allow_html=True)

# --- SECTION 3: INTERACTIVE HISTORY ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.subheader("📋 Recent Valuations")
if st.session_state.history:
    st.table(pd.DataFrame(st.session_state.history))
    if st.button("Clear History"):
        st.session_state.history = []
        st.rerun()
else:
    st.info("No valuations found. Run the engine to see history.")
st.markdown('</div>', unsafe_allow_html=True)
