import streamlit as st
import google.generativeai as genai
import os

# --- SILENT API SETUP ---
# This checks both your local .env and the Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

# ... (Keep your existing CSS and Home Page code here) ...

# --- UPDATE THE SUBMIT LOGIC ---
if submit:
    if not api_key:
        st.error("🔑 CONFIG ERROR: API Key not found in Secrets. Please add GEMINI_API_KEY.")
    elif not (make and model_name):
        st.warning("FIELD ERROR: Manufacturer and Model are required.")
    else:
        with st.spinner("QUANTUM ENGINE ANALYZING..."):
            try:
                # Using the most stable model version
                ai_model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = (f"Act as a professional car appraiser. "
                          f"For a {year} {make} {model_name} {trim} with {miles} miles, "
                          f"provide the market value as a number first, "
                          f"followed by a short technical justification. "
                          f"Format: PRICE: [number] REASON: [text]")
                
                response = ai_model.generate_content(prompt).text
                
                # Parsing logic
                if "REASON:" in response:
                    price_part = response.split("REASON:")[0].replace("PRICE:", "").strip()
                    reason_part = response.split("REASON:")[1].strip()
                    
                    clean_price = "".join(filter(str.isdigit, price_part))
                    formatted_price = f"{int(clean_price):,}"

                    st.markdown(f'<div class="price-box">${formatted_price}</div>', unsafe_allow_html=True)
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.subheader("🏎️ MARKET INSIGHT")
                    st.write(reason_part)
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.error("Engine returned invalid data format. Try again.")

            except Exception as e:
                # This line is key: it tells you the ACTUAL error
                st.error(f"ENGINE ERROR: {str(e)}")
