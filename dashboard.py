<import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ----------------------------
# Title and Introduction
# ----------------------------
st.set_page_config(page_title="Permian Basin Well Dashboard", layout="wide")
st.title("🛢️ Permian Basin Horizontal Well Dashboard")
st.markdown("This dashboard compares top-ranked synthetic horizontal wells in the Permian Basin to real-world operator benchmarks from Pioneer, EOG, and Diamondback.")

# ----------------------------
# Synthetic Data (Top 10 Proposed Wells)
# ----------------------------
future_wells = pd.DataFrame({
    'X': [24855, 16239, 18890, 4308, 1657, 11930, 25186, 32146, 29163, 32146],
    'Y': [31151, 6959, 1988, 20878, 18890, 31483, 24855, 19552, 6959, 14913],
    'Porosity': [0.1715, 0.1361, 0.1320, 0.1089, 0.1015, 0.1236, 0.0956, 0.1281, 0.1338, 0.1290],
    'Permeability': [2.65, 1.56, 1.44, 1.39, 1.41, 1.31, 1.33, 1.24, 1.23, 1.20],
    'Lateral_Length_ft': [7787, 7521, 9507, 7837, 9757, 8386, 7559, 8958, 9569, 8476]
})

# Upgrade to Gen4 standard (≥9500 ft)
future_wells['Lateral_Length_ft'] = future_wells['Lateral_Length_ft'].apply(lambda x: max(x, 9500))

# Calculate EUR
EUR_SCALE = 0.45
future_wells['EUR_MBO'] = future_wells['Porosity'] * np.sqrt(future_wells['Permeability']) * future_wells['Lateral_Length_ft'] * EUR_SCALE

# ----------------------------
# Real Operator Benchmarks
# ----------------------------
operator_data = pd.DataFrame({
    'Source': ['Pioneer', 'EOG', 'Diamondback'],
    'Basin': ['Midland', 'Delaware', 'Midland'],
    'Avg_Lateral_Length_ft': [10000, 9500, 9800],
    'EUR_MBO_per_Well': [1100, 875, 950],
    'Completion_Type': ['Gen4', 'Gen3+', 'Gen4']
})

# Synthetic Summary
synthetic_summary = pd.DataFrame({
    'Source': ['Synthetic'],
    'Basin': ['Permian'],
    'Avg_Lateral_Length_ft': [future_wells['Lateral_Length_ft'].mean()],
    'EUR_MBO_per_Well': [future_wells['EUR_MBO'].mean()],
    'Completion_Type': ['Gen4 (Upgraded)']
})

comparison_df = pd.concat([operator_data, synthetic_summary], ignore_index=True)

# ----------------------------
# Section 1: Table of Synthetic Wells
# ----------------------------
st.subheader("📊 Top-Ranked Synthetic Horizontal Wells")
st.dataframe(future_wells[['X', 'Y', 'Porosity', 'Permeability', 'Lateral_Length_ft', 'EUR_MBO']].sort_values(by='EUR_MBO', ascending=False))

# ----------------------------
# Section 2: Real vs. Synthetic Comparison
# ----------------------------
st.subheader("🏭 Real vs. Synthetic Well Comparison")
st.dataframe(comparison_df)

# ----------------------------
# Section 3: EUR vs. Lateral Length Plot
# ----------------------------
st.subheader("📈 EUR vs. Lateral Length Comparison")
fig, ax = plt.subplots()
sns.scatterplot(data=comparison_df,
                x='Avg_Lateral_Length_ft',
                y='EUR_MBO_per_Well',
                hue='Source',
                style='Basin',
                s=200, ax=ax)
ax.set_xlabel("Avg Lateral Length (ft)")
ax.set_ylabel("EUR (MBO)")
ax.set_title("EUR vs. Lateral Length")
st.pyplot(fig)

st.markdown("---")
st.caption("Built with ❤️ using Streamlit. Data represents synthetic modeling and public benchmarks.")
PASTE THE FULL STREAMLIT CODE HERE>
