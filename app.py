import streamlit as st
import pandas as pd
import joblib
import time

# --- 1. PAGE SETUP & GLOWING UI ---
st.set_page_config(page_title="AutoPredict AI Pro", page_icon="🏎️", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at top right, #051937, #000000);
        color: #e0e0e0;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 25px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        color: white;
        border-radius: 50px;
        font-weight: bold;
        width: 100%;
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

try:
    model, encoder, scaler = load_assets()
except:
    st.error("Model files not found. Ensure .pkl and .joblib files are in the main GitHub folder.")
    st.stop()

if 'history' not in st.session_state:
    st.session_state.history = []

# --- SECTION 1: WELCOME ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<h1 class="ink-title">🏎️ USA CAR VALUATOR PRO</h1>', unsafe_allow_html=True)
st.write("### Real-Time Market Intelligence")
st.write("Search any make/model to get an instant US market valuation based on millions of records.")
st.markdown('</div>', unsafe_allow_html=True)

# --- SECTION 2: THE DYNAMIC FORM ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.subheader("🔍 Vehicle Analysis")

# Expanded US Car Brand List
all_brands = sorted([
    "Acura", "Alfa Romeo", "Aston Martin", "Audi", "Bentley", "BMW", "Buick", "Cadillac", 
    "Chevrolet", "Chrysler", "Dodge", "Ferrari", "Fiat", "Fisker", "Ford", "Genesis", 
    "GMC", "Honda", "Hummer", "Hyundai", "Infiniti", "Isuzu", "Jaguar", "Jeep", "Kia", 
    "Lamborghini", "Land Rover", "Lexus", "Lincoln", "Lotus", "Maserati", "Maybach", 
    "Mazda", "McLaren", "Mercedes-Benz", "Mercury", "MINI", "Mitsubishi", "Nissan", 
    "Oldsmobile", "Plymouth", "Pontiac", "Porsche", "RAM", "Rolls-Royce", "Saab", 
    "Saturn", "Scion", "Smart", "Subaru", "Suzuki", "Tesla", "Toyota", "Volkswagen", "Volvo"
])

with st.form("main_form"):
    c1, c2 = st.columns(2)
    with c1:
        # SEARCHABLE DROPDOWN WITH PLACEHOLDER
        make = st.selectbox("Car Brand", options=["Choose the brand"] + all_brands)
        # MANUAL NUMBER INPUT FOR YEAR
        year = st.number_input("Model Year", min_value=1990, max_value=2027, value=None, placeholder="Enter Year (e.g. 2022)")
        # MANUAL NUMBER INPUT FOR MILES
        mileage = st.number_input("Odometer (Total Miles)", min_value=0, value=None, placeholder="Type actual miles...")
        
    with c2:
        # EMPTY TEXT INPUT FOR MODEL
        model_name = st.text_input("Car Model", value="", placeholder="Type model (e.g. Mustang, Civic...)")
        # TRANSMISSION
        trans = st.radio("Transmission", ["Automatic", "Manual"], horizontal=True)
        # CONDITION
        cond = st.select_slider("Vehicle Condition", options=["Poor", "Fair", "Good", "Excellent", "Like New"], value="Good")

    cond_map = {"Poor": 1.0, "Fair": 2.0, "Good": 3.0, "Excellent": 4.0, "Like New": 5.0}
    
    st.write("---")
    submitted = st.form_submit_button("GET ESTIMATED PRICE")

if submitted:
    if make == "Choose the brand" or not model_name or year is None or mileage is None:
        st.warning("⚠️ Please fill in all fields to get an accurate estimate.")
    else:
        with st.spinner("Analyzing current US market data..."):
            # Model uses lowercase/capitalized logic based on your training
            input_df = pd.DataFrame([[year, make, model_name, "Base", "Sedan", trans, cond_map[cond], mileage]], 
                                    columns=["year", "make", "model", "trim", "body", "transmission", "condition", "odometer"])
            
            # Match training encoding
            cat_cols = ["make", "model", "trim", "body", "transmission"]
            input_df[cat_cols] = encoder.transform(input_df[cat_cols].astype(str).apply(lambda x: x.str.capitalize()))
            
            # Predict
            final_input = scaler.transform(input_df)
            price = model.predict(final_input)[0]
            time.sleep(1) 
            
            st.balloons()
            st.markdown(f"<h2 style='text-align: center; color: #00d2ff;'>Market Value: ${price:,.2f}</h2>", unsafe_allow_html=True)
            
            # Add to Session History
            st.session_state.history.insert(0, {"Year": year, "Brand": make, "Model": model_name, "Miles": f"{mileage:,}", "Price": f"${price:,.2f}"})

st.markdown('</div>', unsafe_allow_html=True)

# --- SECTION 3: RECENT VALUATIONS ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.subheader("📋 Recent Estimations")
if st.session_state.history:
    st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)
    if st.button("Clear History"):
        st.session_state.history = []
        st.rerun()
else:
    st.info("Your estimation history will appear here.")
st.markdown('</div>', unsafe_allow_html=True)
