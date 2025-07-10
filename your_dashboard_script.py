# # import streamlit as st
# # import pandas as pd
# # import plotly.express as px
# # import re
# # import google.generativeai as genai

# # # =====================
# # # PAGE CONFIGURATION
# # # =====================
# # st.set_page_config(page_title="Banned Herbal Ingredients", layout="wide")

# # # =====================
# # # GEMINI SETUP
# # # =====================
# # genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
# # gemini_model = genai.GenerativeModel("gemini-2.5-flash")

# # # =====================
# # # LOAD DATA
# # # =====================
# # df = pd.read_excel("final_banned_herbal_ingredients_with_case_reports.xlsx")

# # # =====================
# # # SIDEBAR: COUNTRY SELECTION
# # # =====================
# # st.sidebar.title("🌐 Country Filter")
# # country = st.sidebar.selectbox("Select a Country", sorted(df["Country"].unique()))
# # filtered_df = df[df["Country"] == country]

# # # =====================
# # # HEADER
# # # =====================
# # st.title("🌿 Banned Herbal Ingredients Dashboard")
# # st.subheader(f"Regulatory Overview: {country}")

# # # Country-specific info
# # if country == "USA":
# #     st.markdown("""
# #     **🇺🇸 FDA Regulatory Framework:**
# #     - Herbal products regulated under DSHEA 1994
# #     - No FDA pre-approval needed
# #     - Must report serious adverse events
# #     """)
# # elif country == "Australia":
# #     st.markdown("""
# #     **🇦🇺 TGA Regulatory Framework:**
# #     - Listed or registered medicines
# #     - Risk-based pre-market assessment
# #     - Registered on ARTG
# #     """)

# # st.markdown(f"**Country Flag:** {'🇺🇸' if country == 'USA' else '🇦🇺'}")

# # # =====================
# # # BANNED HERBS TABLE
# # # =====================
# # st.markdown("### 🌱 Banned/Restricted Herbs")
# # st.dataframe(filtered_df[["Herbal Ingredient", "Botanical Name", "Status", "Risk"]],
# #              use_container_width=True,hide_index=True)

# # # =====================
# # # CASE REPORTS SECTION
# # # =====================
# # st.markdown("### 📄 Case Reports & Regulatory Actions")

# # def extract_incident_count(text):
# #     text = str(text)
# #     numbers = re.findall(r'\d+', text)
# #     numbers = [int(n) for n in numbers if not (1900 <= int(n) <= 2100)]
# #     return max(numbers) if numbers else 1

# # for _, row in filtered_df.iterrows():
# #     with st.expander(f"{row['Herbal Ingredient']} ({row['Botanical Name']})"):
# #         st.write(f"**Status:** {row['Status']} | **Risk:** {row['Risk']}")
# #         case_text = str(row['Case Reports / Incidents'])
# #         incident_count = extract_incident_count(case_text)
# #         st.write(f"**Reported Incidents:** {incident_count}")
# #         st.write(f"**Details:** {case_text}")
# #         st.markdown(f"[Regulatory Source]({row['Source']})")

# # # =====================
# # # RISK PROFILE CHART
# # # =====================
# # st.markdown("### 📊 Risk Profile Analysis")
# # risk_df = filtered_df.copy()
# # risk_df["Incident Count"] = risk_df["Case Reports / Incidents"].apply(extract_incident_count)

# # risk_analysis = risk_df.groupby('Risk')['Incident Count'].sum().reset_index()
# # risk_analysis.columns = ['Risk Category', 'Total Reported Incidents']

# # fig_risk = px.bar(risk_analysis, 
# #                   x='Risk Category', y='Total Reported Incidents',
# #                   color='Risk Category',
# #                   title=f"Incidents by Risk in {country}")
# # st.plotly_chart(fig_risk, use_container_width=True)

# # # =====================
# # # ENFORCEMENT HISTORY
# # # =====================
# # st.markdown("### 📈 Ingredient Enforcement History")
# # ingredient_counts = risk_df.groupby('Herbal Ingredient')['Incident Count'].sum().reset_index()
# # ingredient_counts.columns = ['Herbal Ingredient', 'Reported Incidents']

# # fig_freq = px.bar(ingredient_counts, 
# #                   x='Herbal Ingredient', y='Reported Incidents',
# #                   title=f"Incidents per Ingredient in {country}",
# #                   color='Reported Incidents')
# # st.plotly_chart(fig_freq, use_container_width=True)








# # st.caption("Sources: FDA, TGA, Clinical case reports, WHO Herbal Regulation Database")

# # # =====================
# # # 🤖 GEMINI AI CHATBOT
# # # =====================
# # st.markdown("---")
# # st.markdown("### 🤖 Ask the Herbal Regulation AI Assistant")

# # if user_input := st.chat_input("Ask a question about regulations, ingredients, or risks..."):
# #     st.chat_message("user").write(user_input)

# #     with st.chat_message("assistant"):
# #         with st.spinner("Searching"):
# #             try:
# #                 gemini_response = gemini_model.generate_content(f"""
# #                 You are an expert assistant on banned herbal ingredients and global regulatory frameworks.
# #                 Based on the following user query, give clear and concise information: "{user_input}"
# #                 """)
# #                 st.write(gemini_response.text)
# #             except Exception as e:
# #                 st.error("Gemini failed. Please check your API key or connection.")





# # =====================
# # COMBINED INGREDIENT-RISK INCIDENTS CHART
# # =====================
# st.markdown("### 📊 Incidents by Herbal Ingredient and Risk Category")

# # Prepare data: each ingredient with its risk and incident count
# risk_df = filtered_df.copy()
# risk_df['Incident Count'] = risk_df['Case Reports / Incidents'].apply(extract_incident_count)
# combined_df = risk_df.groupby(['Herbal Ingredient', 'Risk'])['Incident Count'].sum().reset_index()

# fig_combined = px.bar(
#     combined_df,
#     x='Herbal Ingredient',
#     y='Incident Count',
#     color='Risk',
#     barmode='group',
#     title=f"Total Reported Incidents by Herbal Ingredient and Risk in {country}",
#     labels={'Incident Count': 'Total Reported Incidents', 'Herbal Ingredient': 'Herbal Ingredient', 'Risk': 'Risk Category'}
# )

# fig_combined.update_layout(
#     xaxis={'categoryorder': 'total descending'},
#     xaxis_tickangle=-45,
#     bargap=0.02,
#     bargroupgap=0.05,
#     height=600,
#     font=dict(size=14),
#     legend_title_text='Risk Category',
#     title_font_size=20
# )

# fig_combined.update_traces(
#     hovertemplate='<b>%{x}</b><br>Incidents: %{y}<br>Risk: %{marker.color}<extra></extra>'
# )

# st.plotly_chart(fig_combined, use_container_width=True)






# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import re
# import google.generativeai as genai

# # =====================
# # PAGE CONFIGURATION
# # =====================
# st.set_page_config(page_title="Banned Herbal Ingredients", layout="wide")

# # =====================
# # GEMINI SETUP
# # =====================
# genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
# gemini_model = genai.GenerativeModel("gemini-2.5-flash")

# # =====================
# # LOAD DATA
# # =====================
# df = pd.read_excel("final_banned_herbal_ingredients_with_case_reports.xlsx")

# # Drop any serial number/index column if it exists
# if df.columns[0] in ['Unnamed: 0', 'Index', 'S.No', 'Sr No']:
#     df = df.drop(columns=df.columns[0])


# # =====================
# # SIDEBAR: COUNTRY SELECTION
# # =====================
# st.sidebar.title("🌐 Country Filter")
# country = st.sidebar.selectbox("Select a Country", sorted(df["Country"].unique()))
# filtered_df = df[df["Country"] == country]

# # =====================
# # HEADER
# # =====================
# st.title("🌿 Banned Herbal Ingredients Dashboard")
# st.subheader(f"Regulatory Overview: {country}")

# # Country-specific info
# if country == "USA":
#     st.markdown("""
#     **🇺🇸 FDA Regulatory Framework:**
#     - Herbal products regulated under DSHEA 1994
#     - No FDA pre-approval needed
#     - Must report serious adverse events
#     """)
# elif country == "Australia":
#     st.markdown("""
#     **🇦🇺 TGA Regulatory Framework:**
#     - Listed or registered medicines
#     - Risk-based pre-market assessment
#     - Registered on ARTG
#     """)

# st.markdown(f"**Country Flag:** {'🇺🇸' if country == 'USA' else '🇦🇺'}")

# # =====================
# # BANNED HERBS TABLE
# # =====================
# st.markdown("### 🌱 Banned/Restricted Herbs")
# st.dataframe(
#     filtered_df[["Herbal Ingredient", "Botanical Name", "Status", "Risk"]],
#     use_container_width=True,
#     hide_index=True
# )



# # =====================
# # CASE REPORTS SECTION
# # =====================
# st.markdown("### 📄 Case Reports & Regulatory Actions")

# def extract_incident_count(text):
#     text = str(text)
#     numbers = re.findall(r'\d+', text)
#     numbers = [int(n) for n in numbers if not (1900 <= int(n) <= 2100)]
#     return max(numbers) if numbers else 1

# for _, row in filtered_df.iterrows():
#     with st.expander(f"{row['Herbal Ingredient']} ({row['Botanical Name']})"):
#         st.write(f"**Status:** {row['Status']} | **Risk:** {row['Risk']}")
#         case_text = str(row['Case Reports / Incidents'])
#         incident_count = extract_incident_count(case_text)
#         st.write(f"**Reported Incidents:** {incident_count}")
#         st.write(f"**Details:** {case_text}")
#         st.markdown(f"[Regulatory Source]({row['Source']})")

# # =====================
# # COMBINED INGREDIENT-RISK INCIDENTS CHART
# # =====================
# st.markdown("### 📊 Incidents by Herbal Ingredient and Risk Category")

# # Prepare data: each ingredient with its risk and incident count
# risk_df = filtered_df.copy()
# risk_df['Incident Count'] = risk_df['Case Reports / Incidents'].apply(extract_incident_count)
# combined_df = risk_df.groupby(['Herbal Ingredient', 'Risk'])['Incident Count'].sum().reset_index()

# fig_combined = px.bar(
#     combined_df,
#     x='Herbal Ingredient',
#     y='Incident Count',
#     color='Risk',
#     barmode='group',
#     title=f"Total Reported Incidents by Herbal Ingredient and Risk in {country}",
#     labels={'Incident Count': 'Total Reported Incidents', 'Herbal Ingredient': 'Herbal Ingredient', 'Risk': 'Risk Category'}
# )

# fig_combined.update_layout(
#     xaxis={'categoryorder': 'total descending'},
#     xaxis_tickangle=-45,
#     bargap=0.02,
#     bargroupgap=0.05,
#     height=600,
#     font=dict(size=14),
#     legend_title_text='Risk Category',
#     title_font_size=20
# )

# fig_combined.update_traces(
#     hovertemplate='<b>%{x}</b><br>Incidents: %{y}<br>Risk: %{marker.color}<extra></extra>'
# )

# st.plotly_chart(fig_combined, use_container_width=True)


# # # =====================
# # # REGULATORY INSIGHTS
# # # =====================
# # st.markdown("### ℹ️ Regulatory Insights")
# # if country == "USA":
# #     st.markdown("""
# #     - FDA Import Alerts target banned ingredients
# #     - 2023–24: -33% growth in herbal supplement imports
# #     - Recent lawsuits on kratom health risks
# #     """)
# # elif country == "Australia":
# #     st.markdown("""
# #     - TGA bans black salve, yohimbe and more
# #     - Sharp increase in seizures of unlisted herbal imports
# #     """)

# st.caption("Sources: FDA, TGA, Clinical case reports, WHO Herbal Regulation Database")

# # =====================
# # 🤖 GEMINI AI CHATBOT
# # =====================
# st.markdown("---")
# st.markdown("### 🤖 Ask the Herbal Regulation AI Assistant")

# if user_input := st.chat_input("Ask a question about regulations, ingredients, or risks..."):
#     st.chat_message("user").write(user_input)

#     with st.chat_message("assistant"):
#         with st.spinner("thinking..."):
#             try:
#                 gemini_response = gemini_model.generate_content(f"""
#                 You are an expert assistant on banned herbal ingredients and global regulatory frameworks.
#                 Based on the following user query, give clear and concise information: "{user_input}"
#                 """)
#                 st.write(gemini_response.text)
#             except Exception as e:
#                 st.error("Gemini failed. Please check your API key or connection.")
#             try:
#                 gemini_response = gemini_model.generate_content(f"""
#                 You are an expert assistant on banned herbal ingredients and global regulatory frameworks.
#                 Based on the following user query, give clear and concise information: "{user_input}"
#                 """)
#                 st.write(gemini_response.text)
#             except Exception as e:
#                 st.error("Gemini failed. Please check your API key or connection.")


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

# Drop any serial number/index column if it exists
if df.columns[0] in ['Unnamed: 0', 'Index', 'S.No', 'Sr No']:
    df = df.drop(columns=df.columns[0])

# =====================
# SIDEBAR: COUNTRY SELECTION
# =====================
st.sidebar.title("🌐 Country Filter")
country = st.sidebar.selectbox("Select a Country", sorted(df["Country"].unique()))
filtered_df = df[df["Country"] == country]

# =====================
# 🤖 GEMINI AI CHATBOT (IN SIDEBAR)
# =====================
st.sidebar.markdown("---")
st.sidebar.subheader("🤖 Herbal AI Assistant")

with st.sidebar.form("chatbot_form", clear_on_submit=True):
    user_input = st.text_area("Ask about ingredients, regulations, or risks:", height=100)
    submitted = st.form_submit_button("Ask")

if submitted and user_input:
    st.sidebar.markdown("**You asked:**")
    st.sidebar.write(user_input)

    with st.spinner("Assistant is thinking..."):
        try:
            gemini_response = gemini_model.generate_content(f"""
            You are an expert assistant on banned herbal ingredients and global regulatory frameworks.
            Based on the following user query, give clear and concise information: "{user_input}"
            """)
            st.sidebar.markdown("🧠 **Assistant says:**")
            st.sidebar.write(gemini_response.text)
        except Exception as e:
            st.sidebar.error("⚠️ Assistant failed. Check your API key or internet.")

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
st.dataframe(
    filtered_df[["Herbal Ingredient", "Botanical Name", "Status", "Risk"]],
    use_container_width=True,
    hide_index=True
)

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
# COMBINED INGREDIENT-RISK INCIDENTS CHART
# =====================
st.markdown("### 📊 Incidents by Herbal Ingredient and Risk Category")

# Prepare data: each ingredient with its risk and incident count
risk_df = filtered_df.copy()
risk_df['Incident Count'] = risk_df['Case Reports / Incidents'].apply(extract_incident_count)
combined_df = risk_df.groupby(['Herbal Ingredient', 'Risk'])['Incident Count'].sum().reset_index()

fig_combined = px.bar(
    combined_df,
    x='Herbal Ingredient',
    y='Incident Count',
    color='Risk',
    barmode='group',
    title=f"Total Reported Incidents by Herbal Ingredient and Risk in {country}",
    labels={'Incident Count': 'Total Reported Incidents', 'Herbal Ingredient': 'Herbal Ingredient', 'Risk': 'Risk Category'}
)

fig_combined.update_layout(
    xaxis={'categoryorder': 'total descending'},
    xaxis_tickangle=-45,
    bargap=0.02,
    bargroupgap=0.05,
    height=600,
    font=dict(size=14),
    legend_title_text='Risk Category',
    title_font_size=20
)

fig_combined.update_traces(
    hovertemplate='<b>%{x}</b><br>Incidents: %{y}<br>Risk: %{marker.color}<extra></extra>'
)

st.plotly_chart(fig_combined, use_container_width=True)

# =====================
# FOOTER
# =====================
st.caption("Sources: FDA, TGA, Clinical case reports, WHO Herbal Regulation Database")
