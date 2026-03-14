import streamlit as st
from groq import Groq

# --- AUTHENTICATION ---
# Ensure your GROQ_API_KEY is set in the Streamlit Secrets tab
groq_key = st.secrets.get("GROQ_API_KEY")
if groq_key:
    client = Groq(api_key=groq_key)

# --- PAGE CONFIG ---
st.set_page_config(page_title="Run&Drive | Institutional Analytics", layout="wide")

# --- STYLING: WHITE FORM & LIME TEXT ---
st.markdown("""
    <style>
    /* Hero Section Styling */
    .hero-container {
        text-align: center;
        padding: 50px 0;
        background: #000;
        color: white;
        border-radius: 0 0 40px 40px;
    }
    
    /* Form Customization: White Background */
    [data-testid="stForm"] {
        background-color: #ffffff !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 20px !important;
        padding: 40px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05) !important;
    }
    
    /* Lime Text for Questions */
    label {
        color: #32cd32 !important; 
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        text-transform: none !important; /* Sentence case */
    }

    /* Analytics Card */
    .stat-card {
        background: white;
        padding: 30px;
        border-radius: 15px;
        border-bottom: 8px solid #32cd32;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        text-align: center;
    }

    /* Price highlight - makes the price pop in lime */
    .price-display {
        color: #32cd32;
        font-size: 3.5rem;
        font-weight: 900;
        margin: 0;
    }

    /* Remove extra Streamlit UI */
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 1. WELCOME HERO SECTION ---
st.markdown("""
    <div class="hero-container">
        <h1 style='font-size: 4.5rem; margin-bottom: 10px; font-weight: 900;'>Run&Drive</h1>
        <p style='font-size: 1.4rem; color: #666;'>Institutional Market Intelligence & Spec Analysis</p>
    </div>
    """, unsafe_allow_html=True)

# High-quality automotive hero image
st.image("https://images.unsplash.com/photo-1614162692292-7ac56d7f7f1e?auto=format&fit=crop&q=80&w=2070", 
         use_column_width=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# --- 2. THE TERMINAL (FORM) ---
st.markdown("<h2 style='text-align:center;'>Market Analysis Terminal</h2>", unsafe_allow_html=True)

# Centering the form
col_left, col_mid, col_right = st.columns([1, 2, 1])

with col_mid:
    with st.form("main_engine"):
        st.markdown("### Search Network")
        brand = st.text_input("What is the car brand?", placeholder="e.g. Porsche")
        model = st.text_input("What is the model line?", placeholder="e.g. 911 GT3")
        year = st.number_input("What is the production year?", min_value=1990, max_value=2026, value=2024)
        miles = st.number_input("What is the current mileage?", value=2500)
        trim = st.text_input("What is the specific trim?", placeholder="e.g. RS Package")
        
        submit = st.form_submit_button("Execute Market Scan")

# --- 3. DYNAMIC RESULTS & SPECS ---
if submit:
    if not (brand and model):
        st.warning("Please enter car details to begin.")
    else:
        with st.spinner("Analyzing high-fidelity data..."):
            try:
                # Real-time AI valuation and specs
                prompt = (
                    f"Analyze a {year} {brand} {model} {trim} with {miles} miles. "
                    "Return exactly: PRICE: [value] | TREND: [status] | "
                    "SPECS: [Engine]/[Power]/[0-60 Time]/[Top Speed]"
                )
                
                res = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile"
                ).choices[0].message.content
                
                # Parsing
                price_val = res.split("PRICE:")[1].split("|")[0].strip()
                trend_val = res.split("TREND:")[1].split("|")[0].strip()
                specs = res.split("SPECS:")[1].strip().split("/")

                # Display Results
                st.markdown("---")
                st.markdown(f"<h1 style='text-align:center;'>{year} {brand} {model}</h1>", unsafe_allow_html=True)
                
                c1, c2 = st.columns(2)
                with c1:
                    # Relabeled and color-coded Price
                    st.markdown(f"""
                        <div class="stat-card">
                            <small style="color:gray;">ESTIMATED MARKET PRICE</small>
                            <p class="price-display">{price_val}</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                with c2:
                    # Sales Trends Card
                    st.markdown(f"""
                        <div class="stat-card">
                            <small style="color:gray;">SALES TRENDS</small>
                            <h1 style="color:#000; margin:0; font-size: 3rem;">{trend_val}</h1>
                            <p style="color:#32cd32; font-weight:bold; margin:0;">Status: Active</p>
                        </div>
                    """, unsafe_allow_html=True)

                # TECHNICAL SPECS SECTION
                st.markdown("<br>### 🏎️ Technical Specifications", unsafe_allow_html=True)
                s1, s2, s3, s4 = st.columns(4)
                s1.metric("Engine", specs[0])
                s2.metric("Power", specs[1])
                s3.metric("0-60 MPH", specs[2])
                s4.metric("Top Speed", specs[3])

            except Exception as e:
                st.error("Terminal connection failed. Check your API key or input details.")

# Footer
st.markdown("<br><br><p style='text-align:center; color:gray;'>© 2026 Run&Drive Institutional Analytics</p>", unsafe_allow_html=True)
