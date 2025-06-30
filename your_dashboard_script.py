import streamlit as st
import pandas as pd
import plotly.express as px
import speech_recognition as sr
from io import BytesIO

# Load the dataset
@st.cache_data
def load_data():
    data = {
        'Ingredient Name': ['Acorus calamus', 'Aloe (botanical non-tea)', 'Aristolochic Acid', 
                           'Belladonna', 'Cannabis', 'Chaparral', 'Comfrey', 'Ephedrine alkaloids',
                           'Kava', 'Kratom', 'Sassafras', 'Yohimbe'],
        'Prohibited to Import': ['Contextual', 'IA 99-45', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 
                               'Yes', 'Restricted', 'Yes', 'Yes', 'Restricted'],
        'Banned': ['Restricted', 'Conditionally', 'Yes', 'Restricted', 'Schedule I', 'Discouraged',
                  'Yes', 'Yes', 'Warnings', 'Unapproved', 'Yes', 'Discouraged'],
        'Cannot be Grown': ['No', 'No', 'Discouraged', 'No', 'Yes', 'No', 'No', 'No', 
                           'No', 'Varies', 'No', 'No'],
        'Citations': ['https://ods.od.nih.gov/factsheets/List_of_Botanicals/',
                    'https://www.accessdata.fda.gov/cms_ia/importalert_147.html',
                    'https://www.fda.gov/food/metals-and-your-food/aristolochic-acid-herbal-products',
                    'https://www.fda.gov/news-events/press-announcements/fda-asks-homeopathic-manufacturer-withdraw-belladonna-containing-products',
                    'https://www.dea.gov/drug-information/csa',
                    'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5922762/',
                    'https://ods.od.nih.gov/factsheets/Comfrey-HealthProfessional/',
                    'https://www.fda.gov/food/dietary-supplements/information-select-dietary-supplement-ingredients-and-other-substances',
                    'https://www.fda.gov/consumers/consumer-updates/kava-kava-linked-severe-liver-injury',
                    'https://www.fda.gov/news-events/public-health-focus/fda-and-kratom',
                    'https://www.fda.gov/food/food-additives-petitions/sassafras',
                    'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4118946/'],
        'Country': ['USA', 'USA', 'USA', 'USA', 'USA', 'USA', 'USA', 'USA', 'USA', 'USA', 'USA', 'USA'],
        'Case Reports (USA)': ['2011: FDA warnings', '2002: Import alerts', '2001: Kidney failure cases',
                              '2017: Infant seizures', '2018: CBD warnings', '1992: Liver toxicity',
                              '2001: Oral ban', '2004: 16,000+ adverse events', '2002: Liver failure',
                              '2016: Product seizures', '1976: Flavoring ban', '2013: Heart risk warnings'],
        'Case Reports (Canada)': ['None found', 'None found', '2012: Recalls', '2019: Recalls',
                                 '2019: THC limits', 'None found', '2006: Topical restrictions',
                                 '2003: Stroke reports', '2002: Health advisory', '2016: Addiction advisory',
                                 'None found', '2015: Adulteration recalls']
    }
    return pd.DataFrame(data)

df = load_data()

# App configuration
st.set_page_config(page_title="Herbal Regulatory Compliance", layout="wide")
st.title("🌿 Herbal Ingredients Regulatory Compliance Dashboard")
st.markdown("""
Choose a country to explore banned or restricted herbal ingredients.  
Visualizations show data insights and global presence.
""")

# Sidebar voice input
st.sidebar.markdown("🎙️ **Voice Search for Country**")
use_voice = st.sidebar.button("🎙️ Speak")

# Default dropdown
selected_country = st.selectbox("🌎 Select a Country", sorted(df['Country'].dropna().unique()))

# Voice input handling
if use_voice:
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            with st.spinner("🎙️ Listening for country name..."):
                audio = recognizer.listen(source, timeout=5)
                voice_query = recognizer.recognize_google(audio).strip().upper()
                country_match = df['Country'][df['Country'].str.upper() == voice_query]
                if not country_match.empty:
                    selected_country = country_match.iloc[0]
                    st.success(f"✅ Detected Country: {selected_country}")
                else:
                    st.warning(f"⚠️ '{voice_query}' is not a valid country in the data.")
    except sr.UnknownValueError:
        st.error("❌ Couldn't understand the input.")
    except sr.RequestError as e:
        st.error(f"❌ Voice recognition error: {e}")
    except sr.WaitTimeoutError:
        st.error("⌛ Listening timed out. Try again.")
    except Exception as e:
        st.error(f"❌ Error: {e}")

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
                         hover_name="Country",
                         size="Count",
                         projection="natural earth",
                         title="🌐 Global Locations of Herbal Regulatory Actions")
st.plotly_chart(geo_fig, use_container_width=True)

# Citations
with st.expander("🔗 View Sources / Citations"):
    for _, row in filtered_df.iterrows():
        if pd.notna(row["Citations"]):
            st.markdown(f"**{row['Ingredient Name']}**: [Link]({row['Citations']})")

# Download button
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Country Data as CSV",
    data=csv,
    file_name=f"{selected_country}_Herbal_Regulations.csv",
    mime='text/csv'
)
