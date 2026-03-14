import streamlit as st
from groq import Groq

# --- AUTHENTICATION ---
groq_key = st.secrets.get("GROQ_API_KEY")
if groq_key:
    client = Groq(api_key=groq_key)

# --- UI CONFIGURATION ---
st.set_page_config(page_title="Run&Drive", layout="wide")

st.markdown("""
    <style>
    /* Light Theme 'Fin' Style */
    .stApp {
        background-color: #f8f9fa;
        color: #1a1a1a;
    }
    
    /* Global Casing: Sentence Case */
    h1, h2, h3, p, label {
        text-transform: none !important;
    }

    /* Form Container: White with Lime Question Text */
    [data-testid="stForm"] {
        background-color: #ffffff !important;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #e0e0e0;
    }
    
    /* Questions in Lime */
    .stTextInput label, .stNumberInput label, .stSelectbox label {
        color: #32cd32 !important; 
        font-weight: 600 !important;
    }

    /* Analytics Card Styling */
    .stat-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        border-bottom: 5px solid #32cd32;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    /* Branding Header */
    .brand-header {
        font-size: 24px;
        font-weight: 800;
        color: #000;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LAYOUT: RUN&DRIVE TERMINAL ---
st.markdown('<div class="brand-header">🏎️ Run&Drive</div>', unsafe_allow_html=True)

col_main, col_sidebar = st.columns([2, 1])

with col_sidebar:
    # White form with lime text questions
    with st.form("search_network"):
        st.markdown("**Search Network**")
        make = st.text_input("What is the car brand?", placeholder="e.g. Porsche")
        model = st.text_input("What is the model line?", placeholder="e.g. 911")
        year = st.number_input("What is the production year?", min_value=1960, max_value=2026, value=2024)
        miles = st.number_input("What is the current mileage?", value=0)
        trim = st.text_input("What is the specific trim?", placeholder="e.g. GT3")
        submit = st.form_submit_button("Execute Market Scan")

# --- LOGIC & RESULTS ---
if submit:
    if not (make and model):
        st.warning("Please provide both Brand and Model.")
    else:
        with st.spinner("Analyzing..."):
            # Simulation of AI valuation logic
            val_price = "$174,000.00"
            trend_val = "+12.4%"
            
            with col_main:
                # Top section: Header & Image
                st.title(f"{make} {model} {year}")
                st.caption(f"{trim} Generation")
                
                # Image handling: Shifted to avoid glitchy gaps
                # Using a reliable placeholder for the visual layout
                st.image("https://purepng.com/public/uploads/large/purepng.com-porsche-911-gt3-carcarvehicletransportporsche-961524660341lmtro.png", width=500)
                
                # Analytics Row: Renamed & Filtered
                st.markdown("---")
                a1, a2 = st.columns(2)
                
                with a1:
                    # Relabeled Revenue -> Estimated Market Price
                    st.markdown(f"""
                        <div class="stat-card">
                            <small style="color:gray;">Estimated market price</small>
                            <h2>{val_price}</h2>
                        </div>
                    """, unsafe_allow_html=True)
                
                with a2:
                    # Kept Sales Trends
                    st.markdown(f"""
                        <div class="stat-card">
                            <small style="color:gray;">Sales trends</small>
                            <h2 style="color:#32cd32;">{trend_val}</h2>
                            <small>Market is Active</small>
                        </div>
                    """, unsafe_allow_html=True)

else:
    with col_main:
        # Initial empty state
        st.info("Enter vehicle details in the search network to begin analysis.")
