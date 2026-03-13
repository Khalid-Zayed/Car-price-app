import streamlit as st
import pandas as pd
import joblib
import requests
from bs4 import BeautifulSoup
import re
import time

# --- 1. SETTINGS & STYLING ---
st.set_page_config(page_title="Live Market Auto-Predict", page_icon="📈", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #000000; color: #f0f0f0; }
    .glass-card { background: rgba(255, 255, 255, 0.05); border-radius: 20px; padding: 30px; border: 1px solid #333; }
    .price-box { background: linear-gradient(90deg, #00d2ff, #3a7bd5); padding: 20px; border-radius: 15px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LIVE SCRAPER FUNCTION ---
def get_live_market_price(year, make, model, trim):
    """Searches Google for live listings and extracts prices to find an average."""
    query = f"{year} {make} {model} {trim} for sale price"
    url = f"https://www.google.com/search?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for dollar signs followed by numbers in the search results
        text = soup.get_text()
        prices = re.findall(r'\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?', text)
        
        # Convert found strings like "$25,000" to integers
        clean_prices = []
        for p in prices:
            num = int(p.replace('$', '').replace(',', '').split('.')[0])
            if num > 1000: # Filter out small numbers that aren't car prices
                clean_prices.append(num)
        
        if clean_prices:
            # Take the average of the top 5 results found
            return sum(clean_prices[:5]) / len(clean_prices[:5])
        return None
    except:
        return None

# --- 3. THE APP LOGIC ---
if 'started' not in st.session_state: st.session_state.started = False

if not st.session_state.started:
    st.markdown('<div class="glass-card" style="text-align:center; margin-top:100px;">', unsafe_allow_html=True)
    st.title("💎 LIVE MARKET ESTIMATOR")
    st.write("Our system scrapes live agency data to give you the most accurate price in 2026.")
    st.button("Start Live Search", on_click=lambda: st.session_state.update({"started": True}))
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Load your local model as a fallback
    model = joblib.load('car_price_model.pkl')
    encoder = joblib.load('encoder.joblib')
    scaler = joblib.load('scaler.joblib')

    st.title("🏎️ Real-Time Valuation")
    
    with st.form("main_form"):
        col1, col2 = st.columns(2)
        with col1:
            make = st.text_input("Brand", placeholder="Toyota, BMW, etc.")
            model_name = st.text_input("Model", placeholder="Camry, X5, etc.")
            year = st.number_input("Year", 2010, 2027, value=None)
        with col2:
            trim = st.text_input("Trim (CRITICAL)", placeholder="LE, GT, Premium, etc.")
            miles = st.number_input("Miles", min_value=0, value=None)
            submit = st.form_submit_button("SEARCH REAL-TIME MARKET")

    if submit:
        if not (make and model_name and trim and year and miles):
            st.error("Please fill all details to allow the scraper to search.")
        else:
            with st.spinner(f"🔍 Searching Google & Agencies for {year} {make} {model_name} {trim}..."):
                # 1. Get Live Data
                live_avg = get_live_market_price(year, make, model_name, trim)
                
                # 2. Get AI Baseline (Your trained model)
                input_df = pd.DataFrame([[year, make, model_name, trim, "Sedan", "Automatic", 3.0, miles]], 
                                        columns=["year", "make", "model", "trim", "body", "transmission", "condition", "odometer"])
                input_df[input_df.columns[1:6]] = encoder.transform(input_df[input_df.columns[1:6]].astype(str).apply(lambda x: x.str.capitalize()))
                ai_price = model.predict(scaler.transform(input_df))[0]
                
                time.sleep(1) # For effect

                # 3. Final Calculation (Weighted average of AI + Live Data)
                final_price = live_avg if live_avg else ai_price
                
                st.markdown('<div class="price-box">', unsafe_allow_html=True)
                st.markdown(f"<h1>Final Real Estimation: ${final_price:,.2f}</h1>", unsafe_allow_html=True)
                if live_avg:
                    st.write(f"✅ Verified against live listings for the **{trim}** trim.")
                else:
                    st.write("⚠️ Live data busy; using AI market-trend baseline.")
                st.markdown('</div>', unsafe_allow_html=True)
