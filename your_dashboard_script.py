import streamlit as st
import pandas as pd
import plotly.express as px
import io
import whisper  # or use any STT engine/API

# Load data
@st.cache_data
def load_data():
    return pd.read_excel("Sample_Banned_Herbal_Ingredients_USA_Canada_.xlsx")
df = load_data()

st.set_page_config(...)

st.title("Herbal Regulatory Compliance Dashboard with Voice 🎙️")
st.markdown("Speak or type a country name to filter the data.")

# Audio-based input
audio_bytes = st.audio_input("🎤 Tap to speak the country")
selected_country = None

if audio_bytes:
    with st.spinner("🔍 Transcribing…"):
        model = whisper.load_model("base")
        result = model.transcribe(io.BytesIO(audio_bytes), language="en")
        country_guess = result["text"].strip().title()
        if country_guess in df['Country'].unique():
            selected_country = country_guess
            st.success(f"Heard: **{country_guess}**")
        else:
            st.error(f"🔴 Heard '{country_guess}', but that country isn't in the data.")

# Fallback text input
if not selected_country:
    selected_country = st.selectbox("Or type/select a country", sorted(df['Country'].unique()))

filtered = df[df['Country'] == selected_country]

# Display table & charts as before…
...
