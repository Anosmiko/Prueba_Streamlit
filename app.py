import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Dashboard de Ventas",
                    page_icon= ":bar_chart:",
                    layout="wide")

@st.cache_data
def get_data_from_excel():
    df = pd.read_excel("data/supermarkt_sales.xlsx",
                        engine="openpyxl",
                        sheet_name="Sales",
                        skiprows=3,
                        usecols="B:R",
                        nrows=1000)

    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df

df = get_data_from_excel()
# Barra

st.sidebar.header("Filtros:")

ciudad = st.sidebar.multiselect(
    "Seleccione Ciudad:",
    options= df["City"].unique(),
    default=df["City"].unique()
    )

tipo_cliente = st.sidebar.multiselect(
    "Seleccione Tipo de Cliente:",
    options= df["Customer_type"].unique(),
    default=df["Customer_type"].unique()
    )

genero = st.sidebar.multiselect(
    "Seleccione Genero:",
    options= df["Gender"].unique(),
    default=df["Gender"].unique()
    )

df_selection = df.query("City == @ciudad & Customer_type == @tipo_cliente & Gender == @genero")

# st.dataframe(df_selection)

# ---- MAINPAGE ----
st.title(":bar_chart: Dashboard de Ventas")
st.markdown("##")

#KPIS
ventas_totales = int(df_selection["Total"].sum())

avg_ratings = round(df_selection["Rating"].mean(), 1)
estrellas = ":star:" * int(round(avg_ratings, 0))

venta_media_transaccion = round(df_selection["Total"].mean(), 2)

left_left, left, middle, right = st.columns(4)
with left_left:
    st.subheader("Número de Ventas")
    st.subheader(f"{df_selection.shape[0]}") # comma en mil
with left:
    st.subheader("Ventas Totales:")
    st.subheader(f"{ventas_totales:,}$ USD") # comma en mil
with middle:
    st.subheader("Promedio Rating:")
    st.subheader(f"{avg_ratings}/10 {estrellas}") # comma en mil
with right:
    st.subheader("Promedio de Ventas por Transaccion:")
    st.subheader(f"USD $ {venta_media_transaccion:,}") # comma en mil

st.markdown("---")

# GRAFICOS

# Por linea
sales_by_product_line = (
    df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
)

fig_venta_productos = px.bar(sales_by_product_line,
                             x = "Total",
                             y = sales_by_product_line.index,
                             orientation="h",
                             title="<b> Ventas Por Linea <b>",
                             color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
                             template="plotly_white")

fig_venta_productos.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)))


# Por Hora
sales_by_product_hora = (
    df_selection.groupby(by=["hour"]).sum()[["Total"]]
)

fig_venta_horas = px.bar(sales_by_product_hora,
                             x = sales_by_product_hora.index,
                             y = "Total",
                             title="<b> Ventas Por Hora <b>",
                             color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
                             template="plotly_white")

fig_venta_horas.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(tickmode="linear")),
    yaxis=(dict(showgrid=False)))

plot_left, plot_right = st.columns(2)
plot_left.plotly_chart(fig_venta_productos, use_container_width=True)
plot_right.plotly_chart(fig_venta_horas, use_container_width=True)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

text = "Nicolas Coddou"
centered_text = f"<p><center>{text}</center><p>"
text = "2023"
centered_año = f"<p><center>{text}</center><p>"


st.markdown(centered_text, unsafe_allow_html=True)
st.markdown(centered_año, unsafe_allow_html=True)
