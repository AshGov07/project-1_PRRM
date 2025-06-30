# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import speech_recognition as sr

# # Load the dataset
# @st.cache_data
# def load_data():
#     return pd.read_excel("Sample_Banned_Herbal_Ingredients_USA_Canada_.xlsx")

# df = load_data()

# st.set_page_config(page_title="Herbal Regulatory Compliance", layout="wide")
# st.title("🌿 Herbal Ingredients Regulatory Compliance Dashboard")
# st.markdown("""
# Choose a country to explore banned or restricted herbal ingredients.  
# Visualizations show data insights and global presence.
# """)

# # Sidebar voice input
# st.sidebar.markdown("🎙️ **Voice Search for Country**")
# use_voice = st.sidebar.button("🎙️ Speak")

# # Default dropdown
# selected_country = st.selectbox("🌎 Select a Country", sorted(df['Country'].dropna().unique()))

# # Override with voice input if triggered
# # Override with voice input if triggered
# if use_voice:
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         with st.spinner("🎙️ Listening for country name..."):
#             try:
#                 audio = recognizer.listen(source, timeout=5)
#                 voice_query = recognizer.recognize_google(audio).strip().upper()
#                 country_match = df['Country'][df['Country'].str.upper() == voice_query]
#                 if not country_match.empty:
#                     selected_country = country_match.iloc[0]
#                     st.success(f"✅ Detected Country: {selected_country}")
#                 else:
#                     st.warning(f"⚠️ '{voice_query}' is not a valid country in the data.")
#             except sr.UnknownValueError:
#                 st.error("❌ Couldn’t understand the input.")
#             except sr.RequestError as e:
#                 st.error(f"❌ Voice recognition error: {e}")
#             except sr.WaitTimeoutError:
#                 st.error("⌛ Listening timed out. Try again.")

# # Filter data
# filtered_df = df[df['Country'] == selected_country]

# # Data Table
# st.markdown(f"### 📋 Regulatory Data for {selected_country}")
# st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)

# # Charts section
# st.markdown("## 📊 Interactive Charts")
# col1, col2 = st.columns(2)

# with col1:
#     reg_counts = pd.DataFrame({
#         'Category': ['Prohibited to Import', 'Banned', 'Cannot be Grown'],
#         'Count': [
#             filtered_df['Prohibited to Import'].str.lower().eq("yes").sum(),
#             filtered_df['Banned'].str.lower().eq("yes").sum(),
#             filtered_df['Cannot be Grown'].str.lower().eq("yes").sum()
#         ]
#     })
#     bar_chart = px.bar(reg_counts, x='Category', y='Count', color='Category',
#                        title=f"🚫 Regulatory Action Counts in {selected_country}")
#     st.plotly_chart(bar_chart, use_container_width=True)

# with col2:
#     pie_chart = px.pie(reg_counts, names='Category', values='Count',
#                        title=f"🍰 Proportion of Herbal Regulation in {selected_country}")
#     st.plotly_chart(pie_chart, use_container_width=True)

# # Geo Map
# st.markdown("## 🗺️ Geographic View of Herbal Bans")
# map_data = df.copy()
# map_data["lat"] = map_data["Country"].map({"USA": 37.0902, "Canada": 56.1304})
# map_data["lon"] = map_data["Country"].map({"USA": -95.7129, "Canada": -106.3468})
# map_counts = map_data.groupby(["Country", "lat", "lon"]).size().reset_index(name='Count')

# geo_fig = px.scatter_geo(map_counts,
#                          lat="lat", lon="lon",
#                          text="Country", size="Count",
#                          projection="natural earth",
#                          title="🌐 Global Locations of Herbal Regulatory Actions")
# st.plotly_chart(geo_fig, use_container_width=True)

# # Citations
# with st.expander("🔗 View Sources / Citations"):
#     for _, row in filtered_df.iterrows():
#         if pd.notna(row["Citations"]):
#             st.markdown(f"**{row['Ingredient Name']}**: [Link]({row['Citations']})")

# # Download button
# st.download_button(
#     label="📥 Download Country Data as CSV",
#     data=filtered_df.to_csv(index=False),
#     file_name=f"{selected_country}_Herbal_Regulations.csv",
#     mime='text/csv'
# )




import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import whisper
import av
import tempfile
import numpy as np
import soundfile as sf

# Load dataset
@st.cache_data
def load_data():
    return pd.read_excel("Sample_Banned_Herbal_Ingredients_USA_Canada_.xlsx")

df = load_data()
st.set_page_config(page_title="Herbal Regulatory Compliance", layout="wide")
st.title("🌿 Herbal Ingredients Regulatory Compliance Dashboard")
st.markdown("Choose a country to explore banned or restricted herbal ingredients. Visualizations show data insights and global presence.")

# Whisper ASR model
@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()

# Audio processing
class AudioProcessor:
    def __init__(self):
        self.frames = []

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        audio = frame.to_ndarray().flatten()
        self.frames.append(audio)
        return frame

    def get_transcription(self):
        if not self.frames:
            return None
        audio_data = np.concatenate(self.frames).astype(np.float32) / 32768.0
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
            sf.write(tmpfile.name, audio_data, 16000)
            result = model.transcribe(tmpfile.name)
            return result["text"]

processor = AudioProcessor()

# UI: Dropdown and mic input
countries = sorted(df['Country'].dropna().unique())
selected_country = st.selectbox("🌎 Select a Country", countries)

with st.sidebar:
    st.markdown("🎙️ **Say the Country Name**")
    ctx = webrtc_streamer(
        key="speech",
        mode=WebRtcMode.SENDONLY,
        in_audio=True,
        audio_receiver_size=512,
        async_processing=True
    )

    if ctx.audio_receiver:
        st.info("🎧 Listening… Speak clearly")
        audio_frames = ctx.audio_receiver.get_frames(timeout=2)
        for frame in audio_frames:
            processor.recv(frame)

        if st.button("📝 Transcribe Voice"):
            transcript = processor.get_transcription()
            if transcript:
                st.success(f"🗣️ You said: `{transcript}`")
                match = df['Country'][df['Country'].str.upper() == transcript.strip().upper()]
                if not match.empty:
                    selected_country = match.iloc[0]
                    st.success(f"📍 Matched Country: {selected_country}")
                else:
                    st.warning("🔍 Couldn’t match that to a country.")
            else:
                st.error("❌ No audio was captured.")

# Filter data
filtered_df = df[df['Country'] == selected_country]

# Data table
st.markdown(f"### 📋 Regulatory Data for {selected_country}")
st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)

# Charts
st.markdown("## 📊 Interactive Charts")
col1, col2 = st.columns(2)

with col1:
    reg_counts = pd.DataFrame({
        'Category': ['Prohibited to Import', 'Banned', 'Cannot be Grown'],
        'Count': [
            filtered_df['Prohibited to Import'].str.lower().eq("yes").sum(),
            filtered_df['Banned'].str.lower().eq("yes").sum(),
            filtered_df['Cannot be Grown'].str.lower().eq("yes").sum()
        ]
    })
    bar_chart = px.bar(reg_counts, x='Category', y='Count', color='Category',
                       title=f"🚫 Regulatory Action Counts in {selected_country}")
    st.plotly_chart(bar_chart, use_container_width=True)

with col2:
    pie_chart = px.pie(reg_counts, names='Category', values='Count',
                       title=f"🍰 Proportion of Herbal Regulation in {selected_country}")
    st.plotly_chart(pie_chart, use_container_width=True)

# Map
st.markdown("## 🗺️ Geographic View of Herbal Bans")
map_data = df.copy()
map_data["lat"] = map_data["Country"].map({"USA": 37.0902, "Canada": 56.1304})
map_data["lon"] = map_data["Country"].map({"USA": -95.7129, "Canada": -106.3468})
map_counts = map_data.groupby(["Country", "lat", "lon"]).size().reset_index(name='Count')

geo_fig = px.scatter_geo(
    map_counts,
    lat="lat", lon="lon",
    text="Country", size="Count",
    projection="natural earth",
    title="🌐 Global Locations of Herbal Regulatory Actions"
)
st.plotly_chart(geo_fig, use_container_width=True)

# Citations
with st.expander("🔗 View Sources / Citations"):
    for _, row in filtered_df.iterrows():
        if pd.notna(row["Citations"]):
            st.markdown(f"**{row['Ingredient Name']}**: [Link]({row['Citations']})")

# Download
st.download_button(
    label="📥 Download Country Data as CSV",
    data=filtered_df.to_csv(index=False),
    file_name=f"{selected_country}_Herbal_Regulations.csv",
    mime='text/csv'
)
