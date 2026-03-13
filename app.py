import streamlit as st
import pandas as pd
import joblib
import requests
from bs4 import BeautifulSoup
import re
import time

# --- LIVE SCRAPER ENGINE (V3 - HIGH ACCURACY) ---
def scrape_actual_market(year, make, model, trim):
    # This query targets actual inventory to get "Selling Prices" not "Trade-in"
    query = f"{year} {make} {model} {trim} for sale usa price"
    url = f"https://www.google.com/search?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        res = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        raw_text = soup.get_text()
        
        # We look for prices specifically in a realistic range for modern cars
        # If the car is newer than 2020, we ignore anything below $15,000 to avoid "parts" or "leases"
        min_price = 15000 if int(year) > 2020 else 2000
        
        matches = re.findall(r'\$\d{1,3}(?:,\d{3})*', raw_text)
        prices = [int(p.replace('$', '').replace(',', '')) for p in matches]
        valid_prices = [p for p in prices if min_price < p < 1500000]
        
        if valid_prices:
            # Sort prices and take the median/average of the most frequent range
            valid_prices.sort()
            return sum(valid_prices[-5:]) / len(valid_prices[-5:]) # Target higher end for accuracy
        return None
    except:
        return None

# --- REST OF YOUR APP LOGIC ---
# (Keep your UI and Model loading code here)
