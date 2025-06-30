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
import streamlit.components.v1 as components

# Load the dataset
@st.cache_data
def load_data():
    return pd.read_excel("Sample_Banned_Herbal_Ingredients_USA_Canada_.xlsx")

df = load_data()

# Set up Streamlit UI
st.set_page_config(page_title="Herbal Regulatory Compliance", layout="wide")
st.title("🌿 Herbal Ingredients Regulatory Compliance Dashboard")
st.markdown("""
Choose a country to explore banned or restricted herbal ingredients.  
Visualizations show data insights and global presence.
""")

# Sidebar: Voice input + text box
with st.sidebar:
    st.markdown("🎙️ **Voice Search for Country**")
    spoken_country = st.text_input("Detected voice input", "", key="voice_text")

    components.html(
        """
        <script>
        const button = document.createElement("button");
        button.innerText = "🎙️ Speak";
        button.style = "font-size:16px;margin-top:10px;";
        document.body.appendChild(button);

        const output = document.createElement("p");
        output.style = "font-weight:bold;margin-top:8px;";
        document.body.appendChild(output);

        button.onclick = function() {
            if (!('webkitSpeechRecognition' in window)) {
                output.innerText = "Speech recognition not supported.";
                return;
            }

            const recognition = new webkitSpeechRecognition();
            recognition.lang = "en-US";
            recognition.continuous = false;
            recognition.interimResults = false;

            recognition.onstart = () => {
                output.innerText = "🎧 Listening…";
            };

            recognition.onerror = (e) => {
                output.innerText = "❌ Error: " + e.error;
            };

            recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                output.innerText = "🗣️ You said: " + transcript;
                const inputBox = window.parent.document.querySelectorAll('input[data-testid="stTextInput"]')[0];
                const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
                nativeInputValueSetter.call(inputBox, transcript);
                inputBox.dispatchEvent(new Event('input', { bubbles: true }));
            };

            recognition.start();
        };
        </script>
        """,
        height=120
    )

# Dropdown (default selection)
selected_country = st.selectbox("🌎 Select a Country", sorted(df['Country'].dropna().unique()))

# Override dropdown with voice match
if spoken_country:
    match = df['Country'][df['Country'].str.upper() == spoken_country.strip().upper()]
    if not match.empty:
        selected_country = match.iloc[0]
        st.sidebar.success(f"📍 Voice matched: {selected_country}")
    else:
        st.sidebar.warning("❌ Couldn’t match voice input to a country.")

# Filter data
filtered_df = df[df['Country'] == selected_country]

# Display Data
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

# Geographic Visualization
st.markdown("## 🗺️ Geographic View of Herbal Bans")
map_data = df.copy()
map_data["lat"] = map_data["Country"].map({"USA": 37.0902, "Canada": 56.1304})
map_data["lon"] = map_data["Country"].map({"USA": -95.7129, "Canada": -106.3468})
map_counts = map_data.groupby(["Country", "lat", "lon"]).size().reset_index(name='Count')

geo_fig = px.scatter_geo(map_counts,
                         lat="lat", lon="lon",
                         text="Country", size="Count",
                         projection="natural earth",
                         title="🌐 Global Locations of Herbal Regulatory Actions")
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
