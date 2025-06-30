# import streamlit as st
# import pandas as pd
# import plotly.express as px

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

# # Country dropdown
# selected_country = st.selectbox("🌎 Select a Country", sorted(df['Country'].dropna().unique()))

# # Filter data
# filtered_df = df[df['Country'] == selected_country]

# # Data Table
# st.markdown(f"### 📋 Regulatory Data for {selected_country}")
# st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)

# # Charts section
# st.markdown("## 📊 Interactive Charts")

# # Count charts
# col1, col2 = st.columns(2)

# with col1:
#     # Count of ingredients by regulation type
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

# # Geo Map (limited to USA and Canada for now)
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

# # Download
# st.download_button(
#     label="📥 Download Country Data as CSV",
#     data=filtered_df.to_csv(index=False),
#     file_name=f"{selected_country}_Herbal_Regulations.csv",
#     mime='text/csv'
# )


import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

@st.cache_data
def load_data():
    return pd.read_excel("Sample_Banned_Herbal_Ingredients_USA_Canada_.xlsx")

@st.cache_data
def get_import_alert_count(ingredient):
    queries = ["Import Alert 66-41", "Import Alert 54-18", "dietary supplement import alert herbal"]
    total = 0
    headers = {"User-Agent": "Mozilla/5.0"}
    for q in queries:
        url = f"https://www.google.com/search?q={quote_plus(q + ' ' + ingredient)}"
        r = requests.get(url, headers=headers)
        total += r.text.lower().count(ingredient.lower())
    return total

@st.cache_data
def enrich_data(df):
    df["Import_Alert_Count"] = df["Ingredient Name"].apply(get_import_alert_count)
    return df

df = enrich_data(load_data())

st.set_page_config(page_title="Herbal Regulatory Compliance", layout="wide")
st.title("🌿 Herbal Ingredients Regulatory Compliance Dashboard")
st.markdown("Choose a country to explore banned herbal ingredients and their FDA import alert history.")

selected = st.selectbox("🌎 Select a Country", sorted(df['Country'].dropna().unique()))
filtered = df[df['Country'] == selected].reset_index(drop=True)

st.markdown(f"### 📋 Regulatory Data for {selected}")
st.dataframe(filtered, use_container_width=True)

# Import alert counts
st.markdown("### 🛃 FDA Import Alert Mentions")
st.dataframe(filtered[["Ingredient Name", "Import_Alert_Count"]], use_container_width=True)
fig = px.bar(filtered, x="Ingredient Name", y="Import_Alert_Count",
             title=f"Import Alert Mention Count in {selected}")
st.plotly_chart(fig, use_container_width=True)

# Download updated dataset
st.download_button(
    label="📥 Download Updated Data (CSV)",
    data=filtered.to_csv(index=False),
    file_name=f"{selected}_Herbal_Regulations_Updated.csv",
    mime='text/csv'
)
# Optional: Show sources
with st.expander("🔗 View Sources / Citations"):
    for i, row in filtered.iterrows():
        if pd.notna(row["Citations"]):
            st.markdown(f"**{row['Ingredient Name']}**: [Link]({row['Citations']})")
