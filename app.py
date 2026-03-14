import streamlit as st
from groq import Groq

# --- AUTHENTICATION ---
groq_key = st.secrets.get("GROQ_API_KEY")
if groq_key:
    client = Groq(api_key=groq_key)

# --- PAGE CONFIG ---
st.set_page_config(page_title="Run&Drive | Institutional Analytics", layout="wide")

# --- STYLING: PREMIUM DARK THEME & SYMMETRICAL CARDS ---
st.markdown("""
    <style>
    /* Dark Theme Background */
    .stApp {
        background-color: #0b0d10;
    }
    
    .hero-container {
        text-align: center;
        padding: 60px 0;
        background: #000;
        color: white;
        border-radius: 0 0 40px 40px;
    }
    
    /* Search Terminal Styling: White Form with Lime Text */
    [data-testid="stForm"] {
        background-color: #ffffff !important;
        border-radius: 20px !important;
        padding: 40px !important;
        box-shadow: 0 15px 35px rgba(0,0,0,0.3) !important;
    }
    
    label {
        color: #32cd32 !important; 
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }

    /* CARD SYMMETRY FIX: Forced height and flex alignment */
    .stat-card {
        background: #ffffff;
        padding: 40px 20px;
        border-radius: 15px;
        border-bottom: 8px solid #32cd32;
        text-align: center;
        height: 280px; /* Locked height for identical sizing */
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin-top: 20px;
    }

    /* SOLID PRICE VISIBILITY: High-contrast lime green */
    .price-text {
        color: #32cd32 !important;
        opacity: 1 !important;
        font-size: 3.8rem !important;
        font-weight: 900 !important;
        margin: 0 !important;
        line-height: 1 !important;
    }

    .trend-text {
        color: #000000;
        font-size: 3.2rem;
        font-weight: 800;
        margin: 0;
    }

    .spec-label {
        color: #32cd32;
        font-size: 0.9rem;
        font-weight: bold;
        text-transform: uppercase;
        margin-bottom: 5px;
    }

    .spec-value {
        color: #ffffff;
        font-size: 1.8rem;
        font-weight: 600;
    }

    header {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 1. HERO SECTION ---
st.markdown("""
    <div class="hero-container">
        <h1 style='font-size: 4.5rem; margin-bottom: 0;'>Run&Drive</h1>
        <p style='font-size: 1.4rem; color: #32cd32; font-weight: bold;'>AUTOMOTIVE EXCELLENCE</p>
    </div>
    """, unsafe_allow_html=True)

# Main branding image
st.image("https://cdn.dlron.us/static/dealer-27085/2024_Cadillac_Escalade/banner_2024_Cadillac_Escalade.jpg?v=ht3cO0GIsRU8HoPCdrCEsw==", use_column_width=True)

# --- 2. THE TERMINAL (INPUT FORM) ---
st.markdown("<br>", unsafe_allow_html=True)
col_l, col_mid, col_r = st.columns([1, 2, 1])

with col_mid:
    with st.form("main_engine"):
        st.markdown("<h3 style='color:#000; text-align:center;'>Market Analysis Terminal</h3>", unsafe_allow_html=True)
        brand = st.text_input("Car Brand", placeholder="e.g. Volkswagen")
        model = st.text_input("Model Line", placeholder="e.g. Tiguan")
        year = st.number_input("Production Year", min_value=1990, max_value=2026, value=2024)
        miles = st.number_input("Current Mileage", value=5000)
        trim = st.text_input("Specific Trim", placeholder="e.g. R-Line")
        submit = st.form_submit_button("Execute Market Scan")

# --- 3. DYNAMIC RESULTS ---
if submit:
    if not (brand and model):
        st.warning("Please provide vehicle details.")
    else:
        with st.spinner("Analyzing Institutional Data..."):
            try:
                # Optimized prompt for more accurate prices and specs
                prompt = (
                    f"Perform an institutional market analysis for a {year} {brand} {model} {trim} with {miles} miles. "
                    "Be highly accurate with performance specs and current auction pricing. "
                    "Return exactly this format: PRICE: [value] | TREND: [status] | "
                    "SPECS: [Engine Type]/[Horsepower]/[0-60 MPH]/[Top Speed]"
                )
                
                res = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile"
                ).choices[0].message.content
                
                # Parsing the AI response
                price = res.split("PRICE:")[1].split("|")[0].strip()
                trend = res.split("TREND:")[1].split("|")[0].strip()
                specs = res.split("SPECS:")[1].strip().split("/")

                # Display Results Header
                st.markdown(f"<h1 style='text-align:center; color:white; margin-top:50px;'>{year} {brand} {model}</h1>", unsafe_allow_html=True)
                
                # Symmetrical Sizing for Price and Trend Cards
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"""
                        <div class="stat-card">
                            <p style="color:#888; font-weight:bold; margin-bottom:10px;">ESTIMATED MARKET PRICE</p>
                            <p class="price-text">{price}</p>
                        </div>
                    """, unsafe_allow_html=True)
                with c2:
                    st.markdown(f"""
                        <div class="stat-card">
                            <p style="color:#888; font-weight:bold; margin-bottom:10px;">SALES TRENDS</p>
                            <p class="trend-text">{trend}</p>
                            <p style="color:#32cd32; font-weight:bold; margin-top:10px;">Market Status: Active</p>
                        </div>
                    """, unsafe_allow_html=True)

                # Technical Specifications Section
                st.markdown("<br><h2 style='color:white; border-left: 5px solid #32cd32; padding-left:15px;'>Technical Specifications</h2>", unsafe_allow_html=True)
                s1, s2, s3, s4 = st.columns(4)
                
                labels = ["Engine", "Power", "0-60 MPH", "Top Speed"]
                for col, label, val in zip([s1, s2, s3, s4], labels, specs):
                    col.markdown(f"""
                        <div style="margin-top:20px; background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px;">
                            <p class="spec-label">{label}</p>
                            <p class="spec-value">{val}</p>
                        </div>
                    """, unsafe_allow_html=True)

            except Exception as e:
                st.error("Engine failure. Please ensure your API key is correct and try again.")

# Footer
st.markdown("<br><br><p style='text-align:center; color:#444;'>© 2026 Run&Drive Institutional Analytics</p>", unsafe_allow_html=True)
