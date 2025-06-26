
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Z-Score Calculator", layout="centered")

st.title("📊 Z-Score Calculator App")
st.write("This app calculates the general Z-Score based on total Volume or Delta Volume data.")

option = st.sidebar.radio("Choose Data Input Method", ["Upload CSV", "Enter Manually"])

data = []

if option == "Upload CSV":
    uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Uploaded Data:", df)
        if df.shape[1] == 1:
            data = df.iloc[:, 0].tolist()
        else:
            col = st.selectbox("Select column to use", df.columns)
            data = df[col].tolist()

elif option == "Enter Manually":
    user_input = st.sidebar.text_area("Enter comma-separated values (e.g. 1234,5678,-2345):")
    if user_input:
        try:
            data = [float(i.strip()) for i in user_input.split(",")]
        except:
            st.error("Please enter valid numeric data.")

if data:
    mean_val = np.mean(data)
    std_val = np.std(data)
    current_val = data[-1]  # use last value to compare

    z_score = (current_val - mean_val) / std_val if std_val != 0 else 0

    st.subheader("📈 Results")
    st.write(f"**Mean (μ):** {mean_val:.2f}")
    st.write(f"**Standard Deviation (σ):** {std_val:.2f}")
    st.write(f"**Z-Score (Last Value vs Mean):** {z_score:.2f}")

    if abs(z_score) < 0.5:
        st.info("🔹 Value is close to the mean (normal range).")
    elif z_score >= 0.5:
        st.success("🔼 Value is above average.")
    elif z_score <= -0.5:
        st.warning("🔽 Value is below average.")
