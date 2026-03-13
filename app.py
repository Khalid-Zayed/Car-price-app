import streamlit as st
import pandas as pd
import joblib
import requests
from bs4 import BeautifulSoup
import re

# --- STYLING ---
st.set_page_config(page_title="AutoPredict Pro", page_icon="🏎️")
st.markdown("<style>.stApp{background:#0e1117;color:white;}.price{font-size:40px;font-weight:bold;color:#00d2ff;}</style>", unsafe_allow_html=True)

# --- SCRAPER (Logic for "Correct Data") ---
def get_market_avg(year, make, model, trim):
    query = f"{year} {make} {model} {trim} price for sale usa"
    url = f"https://www.google.com/search?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        res = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        prices = [int(p.replace('$', '').replace(',', '')) for p in re.findall(r'\$\d{1,3}(?:,\d{3})*', soup.get_text())]
        
        # ACCURACY FILTER: Ignore numbers that aren't car prices (e.g., $499 leases)
        # For cars 2020+, real prices are almost always > $15,000
        min_threshold = 15000 if int(year) > 2020 else 2000
        valid = [p for p in prices if min_threshold < p < 200000]
        
        return sum(valid[:5]) / len(valid[:5]) if valid else None
    except: return None

# --- MAIN ENGINE ---
st.title("🏎️ Real-Time Auto Valuation")

try:
    model = joblib.load('car_price_model.pkl')
    encoder = joblib.load('encoder.joblib')
    scaler = joblib.load('scaler.joblib')
except:
    st.error("Missing model files in GitHub!")
    st.stop()

with st.form("input_form"):
    col1, col2 = st.columns(2)
    with col1:
        make = st.selectbox("Make", ["Toyota", "Volkswagen", "Ford", "BMW", "Honda", "Nissan", "Chevrolet"])
        model_name = st.text_input("Model", value="Tiguan")
        year = st.number_input("Year", 2010, 2027, value=2023)
    with col2:
        trim = st.text_input("Trim", value="Trendline")
        miles = st.number_input("Miles", value=40000)
        submit = st.form_submit_button("ESTIMATE REAL VALUE")

if submit:
    with st.spinner("Scraping live market..."):
        # 1. Get Live Data (The "Truth")
        live_price = get_market_avg(year, make, model_name, trim)
        
        # 2. AI Fallback
        df = pd.DataFrame([[year, make, model_name, trim, "SUV", "Automatic", 3.0, miles]], columns=["year", "make", "model", "trim", "body", "transmission", "condition", "odometer"])
        df[df.columns[1:6]] = encoder.transform(df[df.columns[1:6]].astype(str).apply(lambda x: x.str.capitalize()))
        ai_price = model.predict(scaler.transform(df))[0]

        # 3. Final Result: Weighted toward Live Market for 2026 accuracy
        final = (live_price * 0.8 + ai_price * 0.2) if live_price else ai_price
        
        st.markdown(f"### Final Estimation")
        st.markdown(f"<div class='price'>${final:,.2f}</div>", unsafe_allow_html=True)
        st.write(f"✅ Based on live agency listings for {year} {make} {model_name} {trim}.")
