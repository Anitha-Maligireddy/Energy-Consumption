import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page Configuration
st.set_page_config(page_title="Energy Dashboard", layout="wide", page_icon="⚡")

# Custom CSS for modern look
st.markdown("""
    <style>
    .block-container {padding-top: 2rem;}
    h1, h2, h3 {color: #2E86C1;}
    .stMetric {background-color: #F2F3F4; border-radius: 10px; padding: 10px;}
    </style>
""", unsafe_allow_html=True)

# --- File Upload ---
st.title("⚡ Energy Dashboard for Housing Complex")
uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Sidebar Filters
    region = st.sidebar.selectbox("Select Region", ["All"] + sorted(df["Region"].unique().tolist()))
    if region != "All":
        df = df[df["Region"] == region]

    # Tabs for different sections
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "📈 Visualizations", "💡 Recommendations"])

    with tab1:
        st.subheader("Household Energy Consumption Overview")
        st.dataframe(df.head(), use_container_width=True)

        # Metrics in columns
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Average Monthly Consumption (kWh)", f"{df['Monthly_Energy_Consumption_kWh'].mean():.2f}")
        with col2:
            st.metric("Total Energy Consumption (kWh)", f"{df['Monthly_Energy_Consumption_kWh'].sum():.0f}")

    with tab2:
        st.subheader("Income vs Energy Consumption")
        fig1, ax1 = plt.subplots(figsize=(7, 5))
        sns.scatterplot(data=df, x="Monthly_Income_INR", y="Monthly_Energy_Consumption_kWh",
                        hue="Region", palette="viridis", s=100, alpha=0.7, ax=ax1)
        ax1.set_title("Income vs Energy Consumption")
        st.pyplot(fig1)

        # Appliance Contribution
        st.subheader("Appliance-wise Count vs Energy Consumption")
        appliances = ["Appliance_AC", "Appliance_Fan", "Appliance_Light", "Fridge", "Washing_Machine", "EV_Charging"]
        selected_appliance = st.selectbox("Select Appliance", appliances)
        fig2, ax2 = plt.subplots(figsize=(7, 5))
        sns.barplot(x=df[selected_appliance], y=df["Monthly_Energy_Consumption_kWh"], palette="coolwarm", ax=ax2)
        ax2.set_xlabel(f"No. of {selected_appliance.replace('_', ' ')}")
        ax2.set_ylabel("Energy Consumption (kWh)")
        st.pyplot(fig2)

    with tab3:
        st.subheader("Smart Recommendations")
        recommendations = []
        for _, row in df.iterrows():
            if row["Monthly_Energy_Consumption_kWh"] > 250:
                msg = f"Household ID {row['Household_ID']} - High usage! Recommend switching to solar and LED bulbs."
                recommendations.append(msg)
                st.warning(msg)
            elif row["EV_Charging"] == 1:
                msg = f"Household ID {row['Household_ID']} - Consider installing a separate EV meter for optimal billing."
                recommendations.append(msg)
                st.info(msg)

        if recommendations:
            st.download_button("Download Recommendations", "\n".join(recommendations), "recommendations.txt")

else:
    st.info("👆 Please upload a file to see the dashboard.")

