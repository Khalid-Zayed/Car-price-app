import streamlit as st
import google.generativeai as genai
import os

# --- API SETUP ---
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# --- STYLING ---
st.set_page_config(page_title="AutoIntelligence AI", page_icon="🏎️")
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .price-display { 
        background: linear-gradient(90deg, #00d2ff, #3a7bd5); 
        padding: 30px; border-radius: 15px; text-align: center; 
        font-size: 45px; font-weight: bold; margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'home'

# --- PAGE: HOME ---
if st.session_state.page == 'home':
    st.markdown("<h1 style='text-align:center; font-size:60px;'>🏎️ AutoIntelligence</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Unlimited AI-driven car valuation. Type any car, get a real price.</p>", unsafe_allow_html=True)
    st.write("---")
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&q=80&w=1000")
        if st.button("🚀 Estimate Now!", use_container_width=True):
            st.session_state.page = 'engine'
            st.rerun()

# --- PAGE: VALUATION ENGINE ---
else:
    if st.button("⬅️ Back to Home"):
        st.session_state.page = 'home'
        st.rerun()

    st.title("🔍 Universal Market Analysis")
    st.info("Since we use Gemini AI, you are not limited to a list. Type any car details below.")
    
    with st.form("main_form"):
        c1, c2 = st.columns(2)
        with c1:
            # CHANGED: Selectbox replaced with text_input for unlimited options
            make = st.text_input("Car Make / Brand", placeholder="e.g. Volkswagen, Ferrari, Lucid")
            model_name = st.text_input("Model Name", placeholder="e.g. Tiguan, 488, Air")
            year = st.number_input("Year", 1900, 2027, 2023)
        with c2:
            trim = st.text_input("Trim / Specs", placeholder="e.g. Trendline, AWD, Performance")
            miles = st.number_input("Odometer (Miles)", value=40000)
            submit = st.form_submit_button("RUN AI VALUATION")

    if submit:
        if not api_key:
            st.error("API Key missing! Check your Streamlit Secrets.")
        elif not (make and model_name):
            st.warning("Please enter at least the Make and Model.")
        else:
            with st.spinner(f"Gemini is analyzing the market for your {year} {make}..."):
                try:
                    ai_model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    # Unified prompt to get both price and reason in one go (saves time/quota)
                    prompt = (f"Act as a professional US car appraiser in 2026. "
                              f"For a {year} {make} {model_name} {trim} with {miles} miles, "
                              f"provide the fair market value as a number first, "
                              f"followed by a short 2-sentence justification. "
                              f"Format: PRICE: [number] REASON: [text]")
                    
                    response = ai_model.generate_content(prompt).text
                    
                    # Simple parsing of the response
                    price_part = response.split("REASON:")[0].replace("PRICE:", "").strip()
                    reason_part = response.split("REASON:")[1].strip()

                    # Clean the price string
                    clean_price = "".join(filter(str.isdigit, price_part))
                    formatted_price = f"{int(clean_price):,}"

                    st.markdown(f'<div class="price-display">${formatted_price}</div>', unsafe_allow_html=True)
                    st.subheader("🤖 AI Market Analysis")
                    st.success(reason_part)
                    
                except Exception as e:
                    st.error("Could not generate valuation. Please check the car details and try again.")
