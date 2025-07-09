# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import quote_plus

# @st.cache_data
# def load_data():
#     return pd.read_excel("Sample_Banned_Herbal_Ingredients_USA_Canada_.xlsx")

# @st.cache_data
# def get_import_alert_count(ingredient):
#     queries = ["Import Alert 66-41", "Import Alert 54-18", "dietary supplement import alert herbal"]
#     total = 0
#     headers = {"User-Agent": "Mozilla/5.0"}
#     for q in queries:
#         url = f"https://www.google.com/search?q={quote_plus(q + ' ' + ingredient)}"
#         r = requests.get(url, headers=headers)
#         total += r.text.lower().count(ingredient.lower())
#     return total

# @st.cache_data
# def enrich_data(df):
#     df["Import_Alert_Count"] = df["Ingredient Name"].apply(get_import_alert_count)
#     return df

# df = enrich_data(load_data())

# st.set_page_config(page_title="Herbal Regulatory Compliance", layout="wide")
# st.title("🌿 Herbal Ingredients Regulatory Compliance Dashboard")
# st.markdown("Choose a country to explore banned herbal ingredients and their FDA import alert history.")

# selected = st.selectbox("🌎 Select a Country", sorted(df['Country'].dropna().unique()))
# filtered = df[df['Country'] == selected].reset_index(drop=True)

# st.markdown(f"### 📋 Regulatory Data for {selected}")
# st.dataframe(filtered, use_container_width=True)

# # Import alert counts
# st.markdown("### 🛃 FDA Import Alert Mentions")
# st.dataframe(filtered[["Ingredient Name", "Import_Alert_Count"]], use_container_width=True)
# fig = px.bar(filtered, x="Ingredient Name", y="Import_Alert_Count",
#              title=f"Import Alert Mention Count in {selected}")
# st.plotly_chart(fig, use_container_width=True)

# # Download updated dataset
# st.download_button(
#     label="📥 Download Updated Data (CSV)",
#     data=filtered.to_csv(index=False),
#     file_name=f"{selected}_Herbal_Regulations_Updated.csv",
#     mime='text/csv'
# )
# # Optional: Show sources
# with st.expander("🔗 View Sources / Citations"):
#     for i, row in filtered.iterrows():
#         if pd.notna(row["Citations"]):
#             st.markdown(f"**{row['Ingredient Name']}**: [Link]({row['Citations']})")

# # import streamlit as st
# # import pandas as pd
# # import plotly.express as px
# # import requests
# # from bs4 import BeautifulSoup
# # import time

# # # --- Config ---
# # FDA_ALERT_PAGES = {
# #     "54-12": "https://www.accessdata.fda.gov/cms_ia/importalert_143.html",
# #     "54-14": "https://www.accessdata.fda.gov/cms_ia/importalert_741.html",
# #     "66-66": "https://www.accessdata.fda.gov/cms_ia/importalert_202.html"
# # }
# # CANADA_COUNTRIES = {"Canada"}

# # @st.cache_data
# # def load_data():
# #     return pd.read_excel("Sample_Banned_Herbal_Ingredients_USA_Canada_.xlsx")

# # @st.cache_data
# # def parse_fda_alert(url, ingredient):
# #     resp = requests.get(url, headers={"User-Agent":"Mozilla/5.0"})
# #     soup = BeautifulSoup(resp.text, "html.parser")
# #     text = soup.get_text().lower()
# #     return text.count(ingredient.lower())

# # @st.cache_data
# # def enrich_data(df):
# #     counts = {ing: 0 for ing in df["Ingredient Name"]}
# #     for name in counts:
# #         total = 0
# #         for page in FDA_ALERT_PAGES.values():
# #             total += parse_fda_alert(page, name)
# #             time.sleep(0.5)
# #         counts[name] = total
# #     df["Import_Alert_Count"] = df["Ingredient Name"].map(counts)
# #     df["CFIA_Check_Required"] = df["Country"].isin(CANADA_COUNTRIES)
# #     return df

# # # --- Main ---
# # df = enrich_data(load_data())

# # st.set_page_config(page_title="Herbal Regulatory Compliance", layout="wide")
# # st.title("🌿 Herbal Regulatory Compliance Dashboard with Import Insights")

# # selected = st.selectbox("Select a Country", sorted(df['Country'].dropna().unique()))
# # filtered = df[df['Country'] == selected].reset_index(drop=True)

# # st.markdown(f"### 📋 Data for {selected}")
# # st.dataframe(filtered, use_container_width=True)

# # # -- Import Alerts Visualization --
# # st.markdown("### 📈 FDA Import Alert Mentions")
# # st.dataframe(filtered[["Ingredient Name", "Import_Alert_Count"]], use_container_width=True)
# # fig = px.bar(filtered, x="Ingredient Name", y="Import_Alert_Count",
# #              title=f"FDA Import Alert Mentions — {selected}")
# # st.plotly_chart(fig, use_container_width=True)

# # # -- CFIA Flag --
# # if selected == "Canada":
# #     st.markdown("### 🇨🇦 CFIA Import Requirement Flags")
# #     st.table(filtered[["Ingredient Name", "CFIA_Check_Required"]])

# # # -- Download Updated File --
# # csv = filtered.to_csv(index=False)
# # st.download_button("📥 Download Updated Data", csv,
# #                    f"{selected}_Herbal_Regulations_Updated.csv", "text/csv")




# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import re

# # Load data
# df = pd.read_excel("final_banned_herbal_ingredients_with_case_reports.xlsx")

# # Title and dropdown
# st.title("🌿 Banned Herbal Ingredients by Country")
# country = st.selectbox("Select a Country", sorted(df["Country"].unique()))

# # Filtered data
# filtered_df = df[df["Country"] == country]

# # Country Highlight Section
# st.markdown(f"### 🌍 {country} - Regulatory Overview")

# # Add country-specific regulatory information
# if country == "USA":
#     st.markdown("""
#     **FDA Regulatory Framework:**
#     - Herbal products are regulated as dietary supplements under DSHEA 1994
#     - Manufacturers don't need FDA approval before marketing
#     - FDA can only act after safety issues emerge
#     - Required to report serious adverse events
#     """)
# elif country == "Australia":
#     st.markdown("""
#     **TGA Regulatory Framework:**
#     - Herbal products regulated as medicines or listed supplements
#     - Requires pre-market assessment for higher-risk products
#     - Maintains the Australian Register of Therapeutic Goods (ARTG)
#     """)

# # Country flag visualization (using emoji as fallback)
# country_flags = {
#     "USA": "🇺🇸",
#     "Australia": "🇦🇺"
# }
# st.markdown(f"**Country Flag:** {country_flags.get(country, '')}")

# # Overview
# st.markdown(f"### Banned/Restricted Herbs in {country}")
# st.dataframe(filtered_df[["Herbal Ingredient", "Botanical Name", "Status", "Risk"]], 
#             use_container_width=True)

# # Case reports with enhanced display
# st.markdown("### 📄 Case Reports & Regulatory Actions")
# for _, row in filtered_df.iterrows():
#     with st.expander(f"{row['Herbal Ingredient']} ({row['Botanical Name']})"):
#         st.write(f"**Status:** {row['Status']} | **Risk:** {row['Risk']}")
        
#         # Parse case reports to extract number of incidents
#         case_text = str(row['Case Reports / Incidents'])
#         if "+" in case_text or "cases" in case_text.lower():
#             # Extract numbers from text like "140+ adverse events" or "6+ liver injury cases"
#             numbers = re.findall(r'\d+', case_text)
#             # Exclude numbers that are likely years (1900-2100)
#             numbers = [int(num) for num in numbers if not (1900 <= int(num) <= 2100)]
#             incident_count = max(numbers) if numbers else 1
#         else:
#             incident_count = 1
            
#         st.write(f"**Reported Incidents:** {incident_count}")
#         st.write(f"**Case Details:** {case_text}")
#         st.markdown(f"[Regulatory Source]({row['Source']})")

# # Enhanced Risk Distribution Chart
# st.markdown("### 📊 Risk Profile Analysis")
# risk_df = filtered_df.copy()

# # Extract numerical values from case reports with year exclusion
# def extract_incidents(text):
#     text = str(text)
#     if "+" in text or "cases" in text.lower():
#         numbers = re.findall(r'\d+', text)
#         # Exclude numbers that are likely years (1900-2100)
#         numbers = [int(num) for num in numbers if not (1900 <= int(num) <= 2100)]
#         return max(numbers) if numbers else 1
#     return 1

# risk_df['Incident Count'] = risk_df['Case Reports / Incidents'].apply(extract_incidents)

# # Group by risk category and sum incidents
# risk_analysis = risk_df.groupby('Risk')['Incident Count'].sum().reset_index()
# risk_analysis.columns = ['Risk Category', 'Total Reported Incidents']

# fig_risk = px.bar(risk_analysis, 
#                  x='Risk Category', 
#                  y='Total Reported Incidents',
#                  color='Risk Category',
#                  title=f'Total Reported Incidents by Risk Category in {country}',
#                  labels={'Total Reported Incidents': 'Number of Incidents'})
# st.plotly_chart(fig_risk, use_container_width=True)

# # Enforcement Frequency Chart (now shows actual incident counts)
# st.markdown("### 📈 Ingredient Enforcement History")
# ingredient_counts = risk_df.groupby('Herbal Ingredient')['Incident Count'].sum().reset_index()
# ingredient_counts.columns = ['Herbal Ingredient', 'Reported Incidents']

# fig_freq = px.bar(ingredient_counts, 
#                  x='Herbal Ingredient', 
#                  y='Reported Incidents',
#                  title=f'Reported Incidents by Ingredient in {country}',
#                  color='Reported Incidents')
# st.plotly_chart(fig_freq, use_container_width=True)

# # Additional Regulatory Context
# st.markdown("### ℹ️ Regulatory Insights")
# if country == "USA":
#     st.markdown("""
#     - The FDA maintains an Import Alert system for problematic herbal ingredients
#     - From 2023-2024, herbal supplement imports to the US showed a -33% growth rate
#     - Recent lawsuits target kratom manufacturers for adverse health effects
#     """)
# elif country == "Australia":
#     st.markdown("""
#     - TGA maintains a Schedule of banned substances in therapeutic goods
#     - Australia has seen increasing seizures of prohibited herbal products like black salve
#     """)

# # Data source attribution
# st.caption("Data sources: FDA Adverse Event Reporting System, TGA regulatory actions, and clinical case reports")



import streamlit as st
import pandas as pd
import plotly.express as px
import re
import google.generativeai as genai

# =====================
# PAGE CONFIGURATION
# =====================
st.set_page_config(page_title="Banned Herbal Ingredients", layout="wide")

# =====================
# GEMINI SETUP
# =====================
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
gemini_model = genai.GenerativeModel("gemini-2.5-flash")

# =====================
# LOAD DATA
# =====================
df = pd.read_excel("final_banned_herbal_ingredients_with_case_reports.xlsx")

# =====================
# SIDEBAR: COUNTRY SELECTION
# =====================
st.sidebar.title("🌐 Country Filter")
country = st.sidebar.selectbox("Select a Country", sorted(df["Country"].unique()))
filtered_df = df[df["Country"] == country]

# =====================
# HEADER
# =====================
st.title("🌿 Banned Herbal Ingredients Dashboard")
st.subheader(f"Regulatory Overview: {country}")

# Country-specific info
if country == "USA":
    st.markdown("""
    **🇺🇸 FDA Regulatory Framework:**
    - Herbal products regulated under DSHEA 1994
    - No FDA pre-approval needed
    - Must report serious adverse events
    """)
elif country == "Australia":
    st.markdown("""
    **🇦🇺 TGA Regulatory Framework:**
    - Listed or registered medicines
    - Risk-based pre-market assessment
    - Registered on ARTG
    """)

st.markdown(f"**Country Flag:** {'🇺🇸' if country == 'USA' else '🇦🇺'}")

# =====================
# BANNED HERBS TABLE
# =====================
st.markdown("### 🌱 Banned/Restricted Herbs")
st.dataframe(filtered_df[["Herbal Ingredient", "Botanical Name", "Status", "Risk"]],
             use_container_width=True)

# =====================
# CASE REPORTS SECTION
# =====================
st.markdown("### 📄 Case Reports & Regulatory Actions")

def extract_incident_count(text):
    text = str(text)
    numbers = re.findall(r'\d+', text)
    numbers = [int(n) for n in numbers if not (1900 <= int(n) <= 2100)]
    return max(numbers) if numbers else 1

for _, row in filtered_df.iterrows():
    with st.expander(f"{row['Herbal Ingredient']} ({row['Botanical Name']})"):
        st.write(f"**Status:** {row['Status']} | **Risk:** {row['Risk']}")
        case_text = str(row['Case Reports / Incidents'])
        incident_count = extract_incident_count(case_text)
        st.write(f"**Reported Incidents:** {incident_count}")
        st.write(f"**Details:** {case_text}")
        st.markdown(f"[Regulatory Source]({row['Source']})")

# =====================
# RISK PROFILE CHART
# =====================
st.markdown("### 📊 Risk Profile Analysis")
risk_df = filtered_df.copy()
risk_df["Incident Count"] = risk_df["Case Reports / Incidents"].apply(extract_incident_count)

risk_analysis = risk_df.groupby('Risk')['Incident Count'].sum().reset_index()
risk_analysis.columns = ['Risk Category', 'Total Reported Incidents']

fig_risk = px.bar(risk_analysis, 
                  x='Risk Category', y='Total Reported Incidents',
                  color='Risk Category',
                  title=f"Incidents by Risk in {country}")
st.plotly_chart(fig_risk, use_container_width=True)

# =====================
# ENFORCEMENT HISTORY
# =====================
st.markdown("### 📈 Ingredient Enforcement History")
ingredient_counts = risk_df.groupby('Herbal Ingredient')['Incident Count'].sum().reset_index()
ingredient_counts.columns = ['Herbal Ingredient', 'Reported Incidents']

fig_freq = px.bar(ingredient_counts, 
                  x='Herbal Ingredient', y='Reported Incidents',
                  title=f"Incidents per Ingredient in {country}",
                  color='Reported Incidents')
st.plotly_chart(fig_freq, use_container_width=True)

# =====================
# REGULATORY INSIGHTS
# =====================
st.markdown("### ℹ️ Regulatory Insights")
if country == "USA":
    st.markdown("""
    - FDA Import Alerts target banned ingredients
    - 2023–24: -33% growth in herbal supplement imports
    - Recent lawsuits on kratom health risks
    """)
elif country == "Australia":
    st.markdown("""
    - TGA bans black salve, yohimbe and more
    - Sharp increase in seizures of unlisted herbal imports
    """)

st.caption("Sources: FDA, TGA, Clinical case reports, WHO Herbal Regulation Database")

# =====================
# 🤖 GEMINI AI CHATBOT
# =====================
st.markdown("---")
st.markdown("### 🤖 Ask the Herbal Regulation AI Assistant")

if user_input := st.chat_input("Ask a question about regulations, ingredients, or risks..."):
    st.chat_message("user").write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Gemini is thinking..."):
            try:
                gemini_response = gemini_model.generate_content(f"""
                You are an expert assistant on banned herbal ingredients and global regulatory frameworks.
                Based on the following user query, give clear and concise information: "{user_input}"
                """)
                st.write(gemini_response.text)
            except Exception as e:
                st.error("Gemini failed. Please check your API key or connection.")
