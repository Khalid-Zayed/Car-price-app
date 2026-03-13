import streamlit as st
import pandas as pd
import joblib
import time

# --- 1. THE "INK" DESIGN SYSTEM ---
st.set_page_config(page_title="Global Auto Valuator Pro", page_icon="🌐", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at top right, #051937, #000000);
        color: #e0e0e0;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 25px;
        padding: 40px;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .stButton>button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        color: white;
        border-radius: 12px;
        font-weight: bold;
        height: 3em;
        transition: 0.3s;
        border: none;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 15px #00d2ff;
    }
    .ink-title {
        background: -webkit-linear-gradient(#00d2ff, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 60px !important;
        letter-spacing: -1px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ASSET LOADING ---
@st.cache_resource
def load_assets():
    # Ensure these names match your GitHub files exactly
    m = joblib.load('car_price_model.pkl')
    e = joblib.load('encoder.joblib')
    s = joblib.load('scaler.joblib')
    return m, e, s

try:
    model, encoder, scaler = load_assets()
except Exception as e:
    st.error(f"Error: Could not find model files. Please check GitHub. Details: {e}")
    st.stop()

if 'history' not in st.session_state:
    st.session_state.history = []

# --- SECTION 1: HEADER ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<h1 class="ink-title">🌐 GLOBAL AUTO VALUATOR</h1>', unsafe_allow_html=True)
st.write("### Professional Grade Valuation for all US-Agency Vehicles.")
st.write("Enter details precisely for the most accurate AI-driven market estimate.")
st.markdown('</div>', unsafe_allow_html=True)

# --- SECTION 2: THE FORM (EMPTY ON OPEN) ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.subheader("📝 Vehicle Details")

# Master list of all brands available in US agencies (Domestic & Imported)
us_market_brands = sorted([
    "Acura", "Alfa Romeo", "Aston Martin", "Audi", "Bentley", "BMW", "Bugatti", "Buick", 
    "Cadillac", "Chevrolet", "Chrysler", "Dodge", "Ferrari", "Fiat", "Fisker", "Ford", 
    "Genesis", "GMC", "Honda", "Hummer", "Hyundai", "Infiniti", "Isuzu", "Jaguar", 
    "Jeep", "Karma", "Kia", "Koenigsegg", "Lamborghini", "Land Rover", "Lexus", 
    "Lincoln", "Lotus", "Lucid", "Maserati", "Maybach", "Mazda", "McLaren", 
    "Mercedes-Benz", "Mercury", "MINI", "Mitsubishi", "Nissan", "Oldsmobile", 
    "Pagani", "Plymouth", "Polestar", "Pontiac", "Porsche", "RAM", "Rivian", 
    "Rolls-Royce", "Saab", "Saturn", "Scion", "Smart", "Subaru", "Suzuki", 
    "Tesla", "Toyota", "Volkswagen", "Volvo"
])

with st.form("valuation_engine"):
    col1, col2 = st.columns(2)
    
    with col1:
        # Defaults to placeholder
        make = st.selectbox("Brand / Agency", options=["Choose the car..."] + us_market_brands)
        # Empty text input for specific model
        model_name = st.text_input("Car Model", value="", placeholder="e.g. S-Class, Mustang, Land Cruiser")
        # Empty number input for Year
        year = st.number_input("Manufacturing Year", min_value=1980, max_value=2027, value=None, placeholder="YYYY")

    with col2:
        # Empty number input for Miles
        miles = st.number_input("Odometer (Total Miles Walked)", min_value=0, value=None, placeholder="e.g. 15000")
        # Transmission toggle
        trans = st.radio("Transmission Type", ["Automatic", "Manual"], horizontal=True)
        # Condition slider
        cond = st.select_slider("Vehicle Condition", options=["Wrecked", "Fair", "Good", "Excellent", "Brand New"], value="Good")

    cond_map = {"Wrecked": 1.0, "Fair": 2.0, "Good": 3.0, "Excellent": 4.0, "Brand New": 5.0}
    
    st.write("---")
    submit = st.form_submit_button("GENERATE ACCURATE ESTIMATE")

if submit:
    if make == "Choose the car..." or not model_name or year is None or miles is None:
        st.warning("🚨 Please complete all fields before generating an estimate.")
    else:
        with st.spinner("AI analyzing millions of US transaction records..."):
            # Prepare data
            input_df = pd.DataFrame([[year, make, model_name, "Base", "Sedan", trans, cond_map[cond], miles]], 
                                    columns=["year", "make", "model", "trim", "body", "transmission", "condition", "odometer"])
            
            # Match Training Logic (Capitalization is key for accuracy!)
            cat_cols = ["make", "model", "trim", "body", "transmission"]
            input_df[cat_cols] = encoder.transform(input_df[cat_cols].astype(str).apply(lambda x: x.str.capitalize()))
            
            # Neural Prediction
            final_input = scaler.transform(input_df)
            prediction = model.predict(final_input)[0]
            time.sleep(1.5) 
            
            st.balloons()
            st.markdown(f"<h1 style='text-align: center; color: #00d2ff;'>Market Value: ${prediction:,.2f}</h1>", unsafe_allow_html=True)
            
            # Record keeping
            st.session_state.history.insert(0, {
                "Vehicle": f"{year} {make} {model_name}", 
                "Miles": f"{miles:,}", 
                "Condition": cond,
                "Price": f"${prediction:,.2f}"
            })

st.markdown('</div>', unsafe_allow_html=True)

# --- SECTION 3: HISTORY ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.subheader("📋 Valuation History")
if st.session_state.history:
    st.table(pd.DataFrame(st.session_state.history))
    if st.button("Clear Records"):
        st.session_state.history = []
        st.rerun()
else:
    st.info("Estimations will be listed here after you click the button above.")
st.markdown('</div>', unsafe_allow_html=True)
