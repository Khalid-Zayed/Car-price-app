import streamlit as st
from groq import Groq

# --- AUTHENTICATION ---
groq_key = st.secrets.get("GROQ_API_KEY")
if groq_key:
    client = Groq(api_key=groq_key)

# --- PAGE CONFIG ---
st.set_page_config(page_title="Run&Drive | Institutional Analytics", layout="wide")

# --- STYLING: HIGH-READABILITY LIGHT THEME ---
# --- STYLING: LIGHT VIBRANT THEME & SECURITY LOCK ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@900&display=swap');

    /* 1. VIBRANT LIGHT BACKGROUND */
    .stApp {
        background-color: #ffffff;
    }
    
    /* 2. SECURITY: HIDE MENU & SOURCE CODE BUTTONS */
    #MainMenu {visibility: hidden;} 
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    div[data-testid="stToolbar"] {display: none;}

    /* 3. HERO TITLE: BOLD & READABLE */
    .header-container {
        text-align: center;
        padding: 50px 0 20px 0;
    }
    
    .main-title {
        font-family: 'Montserrat', sans-serif;
        font-size: 6rem;
        font-weight: 900;
        color: #000000 !important;
        margin-bottom: 0;
        letter-spacing: -3px;
        line-height: 1;
    }

    .sub-title {
        font-size: 1.4rem;
        color: #32cd32;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 5px;
    }
    
    /* 4. CARDS & INPUTS */
    [data-testid="stForm"] {
        background-color: #ffffff !important;
        border-radius: 20px !important;
        padding: 40px !important;
        box-shadow: 0 15px 40px rgba(0,0,0,0.06) !important;
        border: 1px solid #f0f0f0 !important;
    }
    
    label {
        color: #32cd32 !important; 
        font-weight: 700 !important;
    }

    .stat-card {
        background: #ffffff;
        padding: 40px 20px;
        border-radius: 15px;
        border-bottom: 8px solid #32cd32;
        text-align: center;
        height: 280px; 
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.04);
        border: 1px solid #f5f5f5;
    }

    .price-text {
        color: #32cd32 !important;
        font-size: 4rem !important;
        font-weight: 900 !important;
    }

    .trend-text {
        color: #000000;
        font-size: 3.2rem;
        font-weight: 800;
    }

    .spec-value {
        color: #1a1a1a;
        font-size: 1.7rem;
        font-weight: 700;
    }
    </style>
    """, unsafe_allow_html=True)
   

# --- 1. ENHANCED HERO SECTION ---
st.markdown("""
    <div class="header-container">
        <h1 class="main-title">Run&Drive</h1>
        <p class="sub-title">Automotive Excellence</p>
    </div>
    """, unsafe_allow_html=True)

# Cadillac Banner
st.image("https://cdn.dlron.us/static/dealer-27085/2024_Cadillac_Escalade/banner_2024_Cadillac_Escalade.jpg?v=ht3cO0GIsRU8HoPCdrCEsw==", use_column_width=True)

# --- 2. INPUT TERMINAL ---
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
                prompt = (
                    f"Institutional market analysis for {year} {brand} {model} {trim} with {miles} miles. "
                    "Return exactly: PRICE: [value] | TREND: [status] | SPECS: [Engine]/[HP]/[0-60]/[Top Speed]"
                )
                
                res = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile"
                ).choices[0].message.content
                
                price = res.split("PRICE:")[1].split("|")[0].strip()
                trend = res.split("TREND:")[1].split("|")[0].strip()
                specs = res.split("SPECS:")[1].strip().split("/")

                st.markdown(f"<h1 style='text-align:center; color:#000; margin-top:50px;'>{year} {brand} {model}</h1>", unsafe_allow_html=True)
                
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"""
                        <div class="stat-card">
                            <p style="color:#888; font-weight:bold;">ESTIMATED MARKET PRICE</p>
                            <p class="price-text">{price}</p>
                        </div>
                    """, unsafe_allow_html=True)
                with c2:
                    st.markdown(f"""
                        <div class="stat-card">
                            <p style="color:#888; font-weight:bold;">SALES TRENDS</p>
                            <p class="trend-text">{trend}</p>
                            <p style="color:#32cd32; font-weight:bold;">Market Status: Active</p>
                        </div>
                    """, unsafe_allow_html=True)

                st.markdown("<br><h2 style='color:#000; border-left: 5px solid #32cd32; padding-left:15px;'>Technical Specifications</h2>", unsafe_allow_html=True)
                s1, s2, s3, s4 = st.columns(4)
                labels = ["Engine", "Power", "0-60 MPH", "Top Speed"]
                for col, label, val in zip([s1, s2, s3, s4], labels, specs):
                    col.markdown(f"""
                        <div style="margin-top:20px; background: #ffffff; padding: 25px; border-radius: 12px; border: 1px solid #eee; box-shadow: 0 4px 15px rgba(0,0,0,0.02);">
                            <p class="spec-label">{label}</p>
                            <p class="spec-value">{val}</p>
                        </div>
                    """, unsafe_allow_html=True)

            except Exception as e:
                st.error("Engine failure.")

st.markdown("<br><br><p style='text-align:center; color:#888;'>© 2026 Run&Drive Institutional Analytics</p>", unsafe_allow_html=True)
