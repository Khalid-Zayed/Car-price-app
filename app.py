import streamlit as st
from groq import Groq

# --- AUTHENTICATION ---
groq_key = st.secrets.get("GROQ_API_KEY")
if groq_key:
    client = Groq(api_key=groq_key)

# --- PAGE CONFIG ---
st.set_page_config(page_title="Run&Drive | Institutional Analytics", layout="wide")

# --- STYLING: SYMMETRICAL CARDS & HIGH VISIBILITY ---
st.markdown("""
    <style>
    .hero-container {
        text-align: center;
        padding: 50px 0;
        background: #000;
        color: white;
        border-radius: 0 0 40px 40px;
    }
    
    [data-testid="stForm"] {
        background-color: #ffffff !important;
        border-radius: 20px !important;
        padding: 40px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05) !important;
    }
    
    label {
        color: #32cd32 !important; 
        font-weight: 700 !important;
    }

    /* FIXED SYMMETRY: Both cards now share the exact same height and layout */
    .stat-card {
        background: white;
        padding: 40px 20px;
        border-radius: 15px;
        border-bottom: 8px solid #32cd32;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        text-align: center;
        height: 250px; /* Locked height for perfect symmetry */
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    /* FIXED TRANSPARENCY: Force solid lime green color */
    .price-text {
        color: #32cd32 !important;
        opacity: 1 !important;
        font-size: 3.8rem;
        font-weight: 900;
        margin: 0;
    }

    header {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 1. WELCOME HERO SECTION ---
st.markdown("""
    <div class="hero-container">
        <h1 style='font-size: 4rem; margin-bottom: 10px;'>Run&Drive</h1>
        <p style='font-size: 1.5rem; color: #888;'>Premium Automotive Market Intelligence</p>
    </div>
    """, unsafe_allow_html=True)

# Cool car image for the header
st.image("https://images.unsplash.com/photo-1544636331-e26879cd4d9b?auto=format&fit=crop&q=80&w=2070", 
         use_column_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- 2. THE TERMINAL (FORM) ---
col_left, col_mid, col_right = st.columns([1, 2, 1])

with col_mid:
    with st.form("main_engine"):
        st.markdown("### Search Network")
        brand = st.text_input("Brand", placeholder="e.g. Porsche")
        model = st.text_input("Model", placeholder="e.g. 911 GT3")
        year = st.number_input("Year", min_value=1990, max_value=2026, value=2024)
        miles = st.number_input("Mileage", value=2500)
        trim = st.text_input("Trim/Spec", placeholder="e.g. Weissach Package")
        submit = st.form_submit_button("Execute Market Scan")

# --- 3. DYNAMIC RESULTS ---
if submit:
    if not (brand and model):
        st.warning("Please enter car details.")
    else:
        with st.spinner("Analyzing market data..."):
            try:
                prompt = (
                    f"Analyze a {year} {brand} {model} {trim} with {miles} miles. "
                    "Return exactly: PRICE: [value] | TREND: [status] | "
                    "SPECS: [Engine]/[Horsepower]/[0-60 Time]/[Top Speed]"
                )
                
                res = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile"
                ).choices[0].message.content
                
                price = res.split("PRICE:")[1].split("|")[0].strip()
                trend = res.split("TREND:")[1].split("|")[0].strip()
                specs = res.split("SPECS:")[1].strip().split("/")

                st.markdown("---")
                st.markdown(f"<h1 style='text-align:center;'>{year} {brand} {model}</h1>", unsafe_allow_html=True)
                
                c1, c2 = st.columns(2)
                with c1:
                    # High-visibility solid price card
                    st.markdown(f"""
                        <div class="stat-card">
                            <small style="color:gray; font-weight:bold; letter-spacing:1px;">ESTIMATED MARKET PRICE</small>
                            <h1 class="price-text">{price}</h1>
                        </div>
                    """, unsafe_allow_html=True)
                
                with c2:
                    # Symmetrical Trend Card
                    st.markdown(f"""
                        <div class="stat-card">
                            <small style="color:gray; font-weight:bold; letter-spacing:1px;">SALES TRENDS</small>
                            <h1 style="color:#000; margin:0; font-size: 3.2rem;">{trend}</h1>
                            <p style="color:#32cd32; margin-top:10px; font-weight:bold;">Status: Active</p>
                        </div>
                    """, unsafe_allow_html=True)

                st.markdown("### 🏎️ Technical Specifications")
                s1, s2, s3, s4 = st.columns(4)
                s1.metric("Engine", specs[0])
                s2.metric("Power", specs[1])
                s3.metric("0-60 MPH", specs[2])
                s4.metric("Top Speed", specs[3])

            except Exception as e:
                st.error("Connection failed. Please try again.")

st.markdown("<br><p style='text-align:center; color:gray;'>© 2026 Run&Drive Institutional Analytics</p>", unsafe_allow_html=True)
