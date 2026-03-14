import streamlit as st
from groq import Groq

# --- AUTHENTICATION ---
groq_key = st.secrets.get("GROQ_API_KEY")
if groq_key:
    client = Groq(api_key=groq_key)

# --- PAGE CONFIG ---
st.set_page_config(page_title="Run&Drive | Institutional Analytics", layout="wide")

# --- STYLING: PREMIUM DARK THEME & LOCKED SYMMETRY ---
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
    
    /* Search Terminal Styling */
    [data-testid="stForm"] {
        background-color: #161a1d !important;
        border: 1px solid #2d3436 !important;
        border-radius: 20px !important;
        padding: 40px !important;
    }
    
    label {
        color: #32cd32 !important; 
        font-weight: 700 !important;
    }

    /* CARD SYMMETRY FIX: Explicit height and Flexbox alignment */
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

    /* SOLID PRICE VISIBILITY: High contrast lime */
    .price-text {
        color: #32cd32 !important;
        font-size: 4rem !important;
        font-weight: 900 !important;
        margin: 0 !important;
        line-height: 1 !important;
    }

    .trend-text {
        color: #000000;
        font-size: 3.5rem;
        font-weight: 800;
        margin: 0;
    }

    .spec-label {
        color: #32cd32;
        font-size: 0.9rem;
        font-weight: bold;
        text-transform: uppercase;
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

st.image("https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&q=80&w=2070", use_column_width=True)

# --- 2. THE TERMINAL ---
col_left, col_mid, col_right = st.columns([1, 2, 1])

with col_mid:
    with st.form("main_engine"):
        st.markdown("<h3 style='color:white;'>Market Analysis Terminal</h3>", unsafe_allow_html=True)
        brand = st.text_input("Brand", placeholder="e.g. Porsche")
        model = st.text_input("Model", placeholder="e.g. 911 GT3")
        year = st.number_input("Year", min_value=1990, max_value=2026, value=2024)
        miles = st.number_input("Mileage", value=2500)
        trim = st.text_input("Trim", placeholder="e.g. RS Package")
        submit = st.form_submit_button("Execute Market Scan")

# --- 3. DYNAMIC RESULTS ---
if submit:
    if not (brand and model):
        st.warning("Please provide details.")
    else:
        with st.spinner("Analyzing Intelligence..."):
            try:
                prompt = (
                    f"Analyze {year} {brand} {model} {trim} with {miles} miles. "
                    "Return exactly: PRICE: [value] | TREND: [status] | "
                    "SPECS: [Engine]/[Power]/[0-60 Time]/[Top Speed]"
                )
                res = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile"
                ).choices[0].message.content
                
                price = res.split("PRICE:")[1].split("|")[0].strip()
                trend = res.split("TREND:")[1].split("|")[0].strip()
                specs = res.split("SPECS:")[1].strip().split("/")

                st.markdown(f"<h1 style='text-align:center; color:white; margin-top:50px;'>{year} {brand} {model}</h1>", unsafe_allow_html=True)
                
                # Symmetrical Card Layout
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

                # Premium Technical Specs Section
                st.markdown("<br><h2 style='color:white; border-left: 5px solid #32cd32; padding-left:15px;'>Technical Specifications</h2>", unsafe_allow_html=True)
                s1, s2, s3, s4 = st.columns(4)
                
                for col, label, val in zip([s1, s2, s3, s4], ["Engine", "Power", "0-60 MPH", "Top Speed"], specs):
                    col.markdown(f"""
                        <div style="margin-top:20px;">
                            <p class="spec-label">{label}</p>
                            <p class="spec-value">{val}</p>
                        </div>
                    """, unsafe_allow_html=True)

            except Exception as e:
                st.error("Engine failure. Please retry.")

st.markdown("<br><br><p style='text-align:center; color:#444;'>© 2026 Run&Drive Institutional Analytics</p>", unsafe_allow_html=True)
