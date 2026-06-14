import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Care Transition Analytics", layout="wide")

st.title("Care Transition Efficiency & Placement Outcome Analytics")
st.write("Unified Mentor Project Dashboard")

# Load Dataset
df = pd.read_csv("HHS_Unaccompanied_Alien_Children_Program.csv")

# Data Cleaning
numeric_cols = [
    'Children apprehended and placed in CBP custody*',
    'Children in CBP custody',
    'Children transferred out of CBP custody',
    'Children in HHS Care',
    'Children discharged from HHS Care'
]

for col in numeric_cols:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace(',', '', regex=False)
    )
    df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.dropna()

# Date Conversion
df['Date'] = pd.to_datetime(df['Date'])

# KPI Calculations
df['Transfer_Efficiency'] = (
    df['Children transferred out of CBP custody']
    / df['Children in CBP custody']
)

df['Discharge_Effectiveness'] = (
    df['Children discharged from HHS Care']
    / df['Children in HHS Care']
)

df['Pipeline_Throughput'] = (
    df['Children discharged from HHS Care']
    / df['Children apprehended and placed in CBP custody*']
)

df['Backlog'] = (
    df['Children apprehended and placed in CBP custody*']
    - df['Children discharged from HHS Care']
)

# KPI Section
st.header("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Avg Transfer Efficiency",
    round(df['Transfer_Efficiency'].mean(), 2)
)

col2.metric(
    "Avg Discharge Effectiveness",
    round(df['Discharge_Effectiveness'].mean(), 2)
)

col3.metric(
    "Avg Pipeline Throughput",
    round(df['Pipeline_Throughput'].mean(), 2)
)

col4.metric(
    "Avg Backlog",
    round(df['Backlog'].mean(), 2)
)

# Dataset Preview
st.header("Dataset Preview")
st.dataframe(df.head())

# Transfer Efficiency Chart
st.header("Transfer Efficiency Trend")

fig, ax = plt.subplots(figsize=(10,5))
ax.plot(df['Date'], df['Transfer_Efficiency'])
ax.set_title("Transfer Efficiency Trend")
ax.set_xlabel("Date")
ax.set_ylabel("Efficiency")

st.pyplot(fig)

# Discharge Effectiveness Chart
st.header("Discharge Effectiveness Trend")

fig, ax = plt.subplots(figsize=(10,5))
ax.plot(df['Date'], df['Discharge_Effectiveness'])
ax.set_title("Discharge Effectiveness Trend")
ax.set_xlabel("Date")
ax.set_ylabel("Effectiveness")

st.pyplot(fig)

# Pipeline Throughput Chart
st.header("Pipeline Throughput Trend")

fig, ax = plt.subplots(figsize=(10,5))
ax.plot(df['Date'], df['Pipeline_Throughput'])
ax.set_title("Pipeline Throughput Trend")
ax.set_xlabel("Date")
ax.set_ylabel("Throughput")

st.pyplot(fig)

# Backlog Chart
st.header("Backlog Trend")

fig, ax = plt.subplots(figsize=(10,5))
ax.plot(df['Date'], df['Backlog'])
ax.set_title("Backlog Trend")
ax.set_xlabel("Date")
ax.set_ylabel("Backlog")

st.pyplot(fig)