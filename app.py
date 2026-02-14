import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Crypto Volatility Visualizer", layout="wide")

# --- CUSTOM CSS FOR DARK THEME ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR CONTROLS (Stage 6) ---
st.sidebar.header("🕹️ Control Panel")
pattern = st.sidebar.selectbox("Select Swing Pattern", ["Sine Wave (Stable)", "Random Walk (Volatile)", "Hybrid"])
amplitude = st.sidebar.slider("Swing Size (Amplitude)", 0.1, 10.0, 2.0)
frequency = st.sidebar.slider("Swing Speed (Frequency)", 0.01, 0.5, 0.1)
drift = st.sidebar.slider("Long-term Slope (Drift/Integral)", -5.0, 5.0, 0.5)

# --- DATA PREPARATION (Stage 4) ---
@st.cache_data
def load_and_clean_data():
    # Simulation of loading the CSV for the structure
    # In practice: df = pd.read_csv('your_crypto_data.csv')
    dates = pd.date_range(start="2024-01-01", periods=100, freq='D')
    data = {
        'Timestamp': dates,
        'Close': np.random.uniform(30000, 60000, size=100),
        'High': np.random.uniform(31000, 61000, size=100),
        'Low': np.random.uniform(29000, 59000, size=100),
        'Volume': np.random.randint(1000, 5000, size=100)
    }
    df = pd.DataFrame(data)
    # Cleaning: Ensure datetime and handle missing values
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df = df.fillna(method='ffill')
    return df

df = load_and_clean_data()

# --- MATHEMATICAL SIMULATION (The "Math for AI" Logic) ---
x = np.arange(len(df))
if pattern == "Sine Wave (Stable)":
    simulated_swing = amplitude * np.sin(frequency * x) + (drift * x/10)
elif pattern == "Random Walk (Volatile)":
    simulated_swing = np.cumsum(np.random.normal(drift/10, amplitude/5, len(df)))
else:
    simulated_swing = (amplitude * np.cos(frequency * x)) + np.cumsum(np.random.normal(0, 0.5, len(df)))

df['Simulated_Price'] = df['Close'].iloc[0] + (simulated_swing * 1000)

# --- VISUALIZATIONS (Stage 5) ---
st.title("₿ Crypto Volatility Visualizer")
st.write("Visualizing mathematical swings vs. real market data.")

col1, col2, col3 = st.columns(3)
col1.metric("Avg Drift", f"{drift}%")
col2.metric("Volatility Index", f"{amplitude}x")
col3.metric("Sample Size", f"{len(df)} Days")

# 1. Main Price Line Chart
fig_price = go.Figure()
fig_price.add_trace(go.Scatter(x=df['Timestamp'], y=df['Simulated_Price'], name="Simulated Price", line=dict(color='#00ffcc')))
fig_price.update_layout(template="plotly_dark", title="Simulated Price Over Time", xaxis_title="Date", yaxis_title="Price (USD)")
st.plotly_chart(fig_price, use_container_width=True)

# 2. High vs Low Comparison
fig_hl = go.Figure()
fig_hl.add_trace(go.Scatter(x=df['Timestamp'], y=df['High'], name="Market High", line=dict(color='green', dash='dot')))
fig_hl.add_trace(go.Scatter(x=df['Timestamp'], y=df['Low'], name="Market Low", line=dict(color='red', dash='dot')))
fig_hl.update_layout(template="plotly_dark", title="High vs Low Volatility Range")
st.plotly_chart(fig_hl, use_container_width=True)

# 3. Volume Bar Chart
fig_vol = go.Figure(data=[go.Bar(x=df['Timestamp'], y=df['Volume'], marker_color='orange')])
fig_vol.update_layout(template="plotly_dark", title="Trading Volume Analysis")
st.plotly_chart(fig_vol, use_container_width=True)

st.success("Analysis Complete: Stable vs Volatile regions identified.")
