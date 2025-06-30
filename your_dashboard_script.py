import streamlit as st
import pandas as pd
import plotly.express as px
from stt_component import stt  # streamlit-stt component

# Load the dataset
@st.cache_data
def load_data():
    return pd.read_excel("Sample_Banned_Herbal_Ingredients_USA_Canada_.xlsx")

df = load_data()

st.set_page_config(page_title="Herbal Regulatory Compliance", layout="wide")
st.title("🌿 Herbal Ingredients Regulatory Compliance Dashboard")
st.markdown("""
Choose a country to explore banned or restricted herbal ingredients.  
You can use **voice input** or dropdown to select a country.
""")

# Get available countries
available_countries = sorted(df['Country'].dropna().unique())

# Voice input component
st.sidebar.markdown("🎙️ **Voice Input**")
spoken_country = stt(language="en")  # Returns text or None

# Determine selected_country
default_country = available_countries[0]
if spoken_country:
    formatted = spoken_country.strip().title()
    if formatted in available_countries:
        default_country = formatted
        st.sidebar.success(f"✅ Detected: {formatted}")
    else:
        st.sidebar.warning(f"⚠️ '{spoken_country}' not recognized in dataset.")

# Dropdown selection
selected_country = st.selectbox("🌎 Select a Country", available_countries,
                                index=available_countries.index(default_country))

# Filter data
filtered_df = df[df['Country'] == selected_country]

# Data Table
st.markdown(f"### 📋 Regulatory Data for {selected_country}")
st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)

# Charts section
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

# Geo Map
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

# Download button
st.download_button(
    label="📥 Download Country Data as CSV",
    data=filtered_df.to_csv(index=False),
    file_name=f"{selected_country}_Herbal_Regulations.csv",
    mime='text/csv'
)
