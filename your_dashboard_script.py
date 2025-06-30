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

# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import requests
# from bs4 import BeautifulSoup
# import time

# # --- Config ---
# FDA_ALERT_PAGES = {
#     "54-12": "https://www.accessdata.fda.gov/cms_ia/importalert_143.html",
#     "54-14": "https://www.accessdata.fda.gov/cms_ia/importalert_741.html",
#     "66-66": "https://www.accessdata.fda.gov/cms_ia/importalert_202.html"
# }
# CANADA_COUNTRIES = {"Canada"}

# @st.cache_data
# def load_data():
#     return pd.read_excel("Sample_Banned_Herbal_Ingredients_USA_Canada_.xlsx")

# @st.cache_data
# def parse_fda_alert(url, ingredient):
#     resp = requests.get(url, headers={"User-Agent":"Mozilla/5.0"})
#     soup = BeautifulSoup(resp.text, "html.parser")
#     text = soup.get_text().lower()
#     return text.count(ingredient.lower())

# @st.cache_data
# def enrich_data(df):
#     counts = {ing: 0 for ing in df["Ingredient Name"]}
#     for name in counts:
#         total = 0
#         for page in FDA_ALERT_PAGES.values():
#             total += parse_fda_alert(page, name)
#             time.sleep(0.5)
#         counts[name] = total
#     df["Import_Alert_Count"] = df["Ingredient Name"].map(counts)
#     df["CFIA_Check_Required"] = df["Country"].isin(CANADA_COUNTRIES)
#     return df

# # --- Main ---
# df = enrich_data(load_data())

# st.set_page_config(page_title="Herbal Regulatory Compliance", layout="wide")
# st.title("🌿 Herbal Regulatory Compliance Dashboard with Import Insights")

# selected = st.selectbox("Select a Country", sorted(df['Country'].dropna().unique()))
# filtered = df[df['Country'] == selected].reset_index(drop=True)

# st.markdown(f"### 📋 Data for {selected}")
# st.dataframe(filtered, use_container_width=True)

# # -- Import Alerts Visualization --
# st.markdown("### 📈 FDA Import Alert Mentions")
# st.dataframe(filtered[["Ingredient Name", "Import_Alert_Count"]], use_container_width=True)
# fig = px.bar(filtered, x="Ingredient Name", y="Import_Alert_Count",
#              title=f"FDA Import Alert Mentions — {selected}")
# st.plotly_chart(fig, use_container_width=True)

# # -- CFIA Flag --
# if selected == "Canada":
#     st.markdown("### 🇨🇦 CFIA Import Requirement Flags")
#     st.table(filtered[["Ingredient Name", "CFIA_Check_Required"]])

# # -- Download Updated File --
# csv = filtered.to_csv(index=False)
# st.download_button("📥 Download Updated Data", csv,
#                    f"{selected}_Herbal_Regulations_Updated.csv", "text/csv")
