
import streamlit as st
from PIL import Image
import pytesseract
import re
import random

st.set_page_config(page_title="777Joya Aviator Predictor", layout="centered")

st.title("✈️ 777Joya Aviator Predictor (Web Version)")

uploaded_file = st.file_uploader("Upload a screenshot of the Aviator game", type=["jpg", "jpeg", "png"])

def extract_multipliers_from_image(image):
    try:
        text = pytesseract.image_to_string(image)
        matches = re.findall(r"\d+\.\d+x", text)
        multipliers = [float(m.replace('x', '')) for m in matches]
        return multipliers
    except Exception as e:
        st.error(f"OCR failed: {e}")
        return []

def predict_next_multiplier(history):
    if not history:
        return round(random.uniform(1.0, 3.0), 2)
    last = history[-1]
    if last < 1.5:
        return round(random.uniform(2.0, 5.0), 2)
    elif last < 3.0:
        return round(random.uniform(1.0, 2.0), 2)
    else:
        return round(random.uniform(1.0, 1.5), 2)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Screenshot", use_column_width=True)

    with st.spinner("Extracting multipliers..."):
        multipliers = extract_multipliers_from_image(image)

    if multipliers:
        st.success(f"Found {len(multipliers)} multipliers: {multipliers[-5:]}")
        prediction = predict_next_multiplier(multipliers)
        st.markdown(f"### 🔮 Predicted Next Multiplier: **{prediction}x**")
    else:
        st.warning("No valid multipliers found in the image.")
else:
    st.info("Please upload a screenshot to begin.")
