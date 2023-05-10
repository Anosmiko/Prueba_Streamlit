import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Dashboard de Ventas",
                    page_icon= ":bar_chart:",
                    layout="wide")

df = pd.read_excel("supermarkt_sales.xlsx",
                    engine="openpyxl",
                    sheet_name="Sales",
                    skiprows=3,
                    usecols="B:R",
                    nrows=1000)

st.dataframe(df)

# Barra
st.sidebar.header("Filtros:")
coudad = st.sidebar.multiselect(
    "Seleccione Ciudad:",
    options= df["City"].unique(),
    default=df["City"].unique()
    )