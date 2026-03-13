import streamlit as st
import pandas as pd
import joblib
import time

# --- 1. SETTINGS & STYLING ---
st.set_page_config(page_title="AutoPredict AI Pro", page_icon="🏎️", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at top right, #051937, #000000);
        color: #f0f0f0;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border-radius: 25px;
        padding: 50px;
        text-align: center;
        margin: auto;
        max-width: 900px;
    }
    .ink-title {
        background: -webkit-linear-gradient(#00d2ff, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 70px !important;
    }
    .start-btn > button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%) !important;
        color: white !important;
        font-size: 24px !important;
        padding: 20px 50px !important;
        border-radius: 50px !important;
        border: none !important;
        transition: 0.4s !important;
        font-weight: bold !important;
    }
    .start-btn > button:hover {
        transform: scale(1.1);
        box-shadow: 0 0 30px #00d2ff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE FOR NAVIGATION ---
if 'started' not in st.session_state:
    st.session_state.started = False

def start_app():
    st.session_state.started = True

# --- 3. LANDING PAGE (What the user sees first) ---
if not st.session_state.started:
    st.markdown('<div style="height: 10vh;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h1 class="ink-title">AutoPredict AI</h1>', unsafe_allow_html=True)
    st.markdown("## The Future of Car Valuation is Here.")
    st.write("""
        Using neural regression trained on millions of US agency records, 
        our AI provides real-time market accuracy for any vehicle. 
        Forget guesswork—get the exact price you deserve.
    """)
    st.write("✨ **80+ US Agency Brands** | 📊 **Live Market Logic** | ⚡ **Instant Results**")
    st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)
    
    # Large Interactive Button
    st.markdown('<div class="start-btn">', unsafe_allow_html=True)
    st.button("Start Estimating!", on_click=start_app)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. THE MAIN ESTIMATOR PAGE ---
else:
    # --- LOAD ASSETS ---
    @st.cache_resource
    def load_assets():
        m = joblib.load('car_price_model.pkl')
        e = joblib.load('encoder.joblib')
        s = joblib.load('scaler.joblib')
        return m, e, s

    model, encoder, scaler = load_assets()
    if 'history' not in st.session_state: st.session_state.history = []

    # UI HEADER
    st.markdown('<h1 class="ink-title" style="font-size: 40px !important;">🏎️ VALUATION ENGINE</h1>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="glass-card" style="text-align: left; padding: 30px; max-width: 100%;">', unsafe_allow_html=True)
        
        # MASTER LIST
        us_brands = sorted(["Acura", "Audi", "BMW", "Cadillac", "Chevrolet", "Ford", "Honda", "Hyundai", "Jeep", "Kia", "Lexus", "Mercedes-Benz", "Nissan", "Porsche", "RAM", "Tesla", "Toyota", "Volkswagen", "Volvo", "Ferrari", "Lamborghini", "Land Rover", "Mazda", "Subaru", "GMC", "Dodge"])

        with st.form("main_form"):
            c1, c2 = st.columns(2)
            with c1:
                make = st.selectbox("Brand Agency", options=["Choose the car..."] + us_brands)
                year = st.number_input("Model Year", 1990, 2027, value=None, placeholder="YYYY")
                miles = st.number_input("Total Miles Driven", min_value=0, value=None, placeholder="e.g. 25000")
            with c2:
                model_name = st.text_input("Car Model", placeholder="e.g. Mustang, Civic...")
                trans = st.radio("Transmission", ["Automatic", "Manual"], horizontal=True)
                cond = st.select_slider("Condition", options=["Fair", "Good", "Excellent", "New"], value="Good")
            
            submitted = st.form_submit_button("GENERATE ESTIMATE")

        if submitted:
            if make == "Choose the car..." or not model_name or year is None or miles is None:
                st.warning("Please fill all fields.")
            else:
                input_df = pd.DataFrame([[year, make, model_name, "Base", "Sedan", trans, 3.0, miles]], columns=["year", "make", "model", "trim", "body", "transmission", "condition", "odometer"])
                input_df[["make", "model", "trim", "body", "transmission"]] = encoder.transform(input_df[["make", "model", "trim", "body", "transmission"]].astype(str).apply(lambda x: x.str.capitalize()))
                price = model.predict(scaler.transform(input_df))[0]
                st.balloons()
                st.markdown(f"<h1 style='color: #00d2ff;'>Estimate: ${price:,.2f}</h1>", unsafe_allow_html=True)
                st.session_state.history.insert(0, {"Car": f"{year} {make}", "Price": f"${price:,.2f}"})
        st.markdown('</div>', unsafe_allow_html=True)

    # HISTORY SECTION
    if st.session_state.history:
        st.markdown('<div class="glass-card" style="max-width: 100%; margin-top: 20px;">', unsafe_allow_html=True)
        st.subheader("📋 Recent Estimations")
        st.table(pd.DataFrame(st.session_state.history))
        st.markdown('</div>', unsafe_allow_html=True)
