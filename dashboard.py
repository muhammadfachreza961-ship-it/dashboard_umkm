import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard UMKM",
    layout="wide"
)

st.title("Dashboard Streamlit database")
st.write("Analisis data UMKM interaktif")

@st.cache_data
def load_data():
    df = pd.read_csv("clean_umkm_dataset.csv")
    return df

df = load_data()
st.sidebar.header("🔍 Filter Data")

cat_cols = df.select_dtypes(include='object').columns

filtered_df = df.copy()

for col in cat_cols:
    options = df[col].dropna().unique()
    selected = st.sidebar.multiselect(f"Pilih {col}", options)

    if selected:
        filtered_df = filtered_df[filtered_df[col].isin(selected)]

st.subheader("📌 Ringkasan")

col1, col2, col3 = st.columns(3)

col1.metric("Jumlah Data", len(filtered_df))
col2.metric("Jumlah Kolom", filtered_df.shape[1])
col3.metric("Missing Value", filtered_df.isnull().sum().sum())

st.subheader("📄 Data")

st.dataframe(filtered_df, use_container_width=True)

st.subheader("📊 Visualisasi")

num_cols = filtered_df.select_dtypes(include=['int64', 'float64']).columns

if len(num_cols) > 0:
    col_x = st.selectbox("Pilih X", num_cols)
    col_y = st.selectbox("Pilih Y", num_cols)

    chart_type = st.radio("Jenis Grafik", ["Scatter", "Line", "Bar"])

    if chart_type == "Scatter":
        fig = px.scatter(filtered_df, x=col_x, y=col_y)
    elif chart_type == "Line":
        fig = px.line(filtered_df, x=col_x, y=col_y)
    else:
        fig = px.bar(filtered_df, x=col_x, y=col_y)

    st.plotly_chart(fig, use_container_width=True)

st.subheader("📈 Distribusi Data")

if len(num_cols) > 0:
    selected_col = st.selectbox("Pilih kolom", num_cols)

    fig2 = px.histogram(filtered_df, x=selected_col, nbins=30)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
st.caption("Dibuat dengan Streamlit")