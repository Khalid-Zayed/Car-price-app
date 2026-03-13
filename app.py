import streamlit as st
import pandas as pd
import joblib
import time

# --- 1. PAGE SETUP & GLOWING CSS ---
st.set_page_config(page_title="AI Car Valuator Pro", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    /* Vibrant Ink Background */
    .stApp {
        background: radial-gradient(circle at top right, #001f3f, #000000);
        color: #e0e0e0;
    }
    
    /* Glowing Glass Containers for Sections */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
    }
    
    /* Interactive Button Styling */
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
        color: #ffffff;
    }
    
    /* Custom Title Text */
    .ink-title {
        font-family: 'Inter', sans-serif;
        background: -webkit-linear-gradient(#00d2ff, #91eaff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 50px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ASSET LOADING ---
@st.cache_resource
def load_assets():
    # Note: Ensure these filenames match your GitHub exactly (lowercase, no spaces)
    m = joblib.load('car_price_model.pkl')
    e = joblib.load('encoder.joblib')
    s = joblib.load('scaler.joblib')
    return m, e, s

model, encoder, scaler = load_assets()

if 'history' not in st.session_state:
    st.session_state.history = []

# --- SECTION 1: WELCOME & VIBE ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<h1 class="ink-title">💎 AI CAR VALUATOR PRO</h1>', unsafe_allow_html=True)
st.write("### Precise Market Analysis powered by Neural Regression.")
st.write("This engine analyzes mileage, condition, and market trends to give you an instant valuation.")
st.markdown('</div>', unsafe_allow_html=True)

# --- SECTION 2: THE INTERACTIVE FORM ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.subheader("🏎️ Vehicle Specifications")

with st.form("main_form"):
    row1_col1, row1_col2, row1_col3 = st.columns(3)
    with row1_col1:
        make = st.selectbox("Manufacturer", ["Toyota", "Bmw", "Ford", "Mercedes-benz", "Honda", "Nissan", "Chevrolet"])
        year = st.number_input("Model Year", 2010, 2026, 2022)
    with row1_col2:
        model_name = st.text_input("Model Name", "Camry")
        trans = st.radio("Transmission", ["Automatic", "Manual"], horizontal=True)
    with row1_col3:
        mileage = st.number_input("Odometer (KM)", value=30000)
        cond = st.slider("Vehicle Condition", 1.0, 5.0, 4.0)

    # Simplified values for your model logic
    trim = "Base"
    body = "Sedan"

    st.write("")
    submitted = st.form_submit_button("CALCULATE VALUE")

if submitted:
    with st.spinner("🧠 AI is analyzing auction records..."):
        # Processing
        input_df = pd.DataFrame([[year, make, model_name, trim, body, trans, cond, mileage]], 
                                columns=["year", "make", "model", "trim", "body", "transmission", "condition", "odometer"])
        
        # Transformation
        cat_cols = ["make", "model", "trim", "body", "transmission"]
        input_df[cat_cols] = encoder.transform(input_df[cat_cols].astype(str).apply(lambda x: x.str.capitalize()))
        final_input = scaler.transform(input_df)
        
        # Prediction
        price = model.predict(final_input)[0]
        time.sleep(1.2) # Adding a dramatic pause
        
        st.balloons()
        st.markdown(f"<h2 style='text-align: center; color: #00d2ff;'>Market Estimate: ${price:,.2f}</h2>", unsafe_allow_html=True)
        
        # Add to History
        st.session_state.history.append({"Vehicle": f"{year} {make}", "Price": f"${price:,.2f}"})

st.markdown('</div>', unsafe_allow_html=True)

# --- SECTION 3: RECENT ESTIMATIONS ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.subheader("📋 Recent Estimations")
if st.session_state.history:
    # Reverse the history to show newest first
    hist_df = pd.DataFrame(st.session_state.history[::-1])
    st.dataframe(hist_df, use_container_width=True)
else:
    st.info("No estimates yet. Try the form above.")
st.markdown('</div>', unsafe_allow_html=True)
