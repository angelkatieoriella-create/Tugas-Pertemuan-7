import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import altair as alt
from sklearn.linear_model import LinearRegression
from scipy.stats import pearsonr
import io

st.set_page_config(page_title="Dashboard Nilai Siswa (Excel)", layout="wide")

st.title("📊 Dashboard Analisis Data 50 Siswa (Excel)")

# ==============================
# Upload File Excel SAJA
# ==============================
uploaded_file = st.file_uploader("Upload File Excel (.xlsx)", type=["xlsx"])

if uploaded_file is not None:

    df = pd.read_excel(uploaded_file, engine="openpyxl")

    st.subheader("📋 Data Awal")
    st.dataframe(df)

    # Ambil kolom nilai (selain kolom pertama = Nama)
    nilai_columns = df.columns[1:]
    df["Rata-rata"] = df[nilai_columns].mean(axis=1)

    # ==============================
    # 1–4 Informasi Utama
    # ==============================
    st.subheader("📌 Informasi Utama")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Jumlah Siswa", len(df))
    col2.metric("Rata-rata Kelas", round(df["Rata-rata"].mean(), 2))
    col3.metric("Nilai Tertinggi", round(df["Rata-rata"].max(), 2))
    col4.metric("Nilai Terendah", round(df["Rata-rata"].min(), 2))

    # ==============================
    # 5. Histogram Interaktif
    # ==============================
    st.subheader("📈 Distribusi Nilai")
    fig_hist = px.histogram(df, x="Rata-rata", nbins=10)
    st.plotly_chart(fig_hist)

    # ==============================
    # 6. Heatmap Korelasi
    # ==============================
    st.subheader("🔥 Heatmap Korelasi")

    corr = df[nilai_columns].corr()

    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

    # ==============================
    # 7. Regresi Linear
    # ==============================
    st.subheader("📊 Analisis Regresi Linear")

    col_x = st.selectbox("Pilih Variabel X", nilai_columns)
    col_y = st.selectbox("Pilih Variabel Y", nilai_columns)

    if col_x != col_y:
        X = df[[col_x]]
        Y = df[col_y]

        model = LinearRegression()
        model.fit(X, Y)
        Y_pred = model.predict(X)

        r, p_value = pearsonr(df[col_x], df[col_y])
        r2 = model.score(X, Y)

        fig_reg = px.scatter(df, x=col_x, y=col_y)
        fig_reg.add_scatter(x=df[col_x], y=Y_pred, mode='lines', name='Regresi')
        st.plotly_chart(fig_reg)

        st.write(f"Koefisien Korelasi (r): {r:.4f}")
        st.write(f"P-value: {p_value:.4f}")
        st.write(f"R²: {r2:.4f}")
        st.write(f"Persamaan: y = {model.intercept_:.2f} + {model.coef_[0]:.2f}x")

    # ==============================
    # 8. Top & Bottom 5
    # ==============================
    st.subheader("🏆 Top 5 & Bottom 5")

    top5 = df.sort_values("Rata-rata", ascending=False).head(5)
    bottom5 = df.sort_values("Rata-rata", ascending=True).head(5)

    st.write("Top 5 Nilai Tertinggi")
    st.dataframe(top5[["Nama", "Rata-rata"]])

    st.write("Top 5 Nilai Terendah")
    st.dataframe(bottom5[["Nama", "Rata-rata"]])

    # ==============================
    # Download Hasil
    # ==============================
    st.subheader("📥 Download Hasil Analisis")

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Hasil Analisis')

    st.download_button(
        label="Download Hasil ke Excel",
        data=output.getvalue(),
        file_name="hasil_analisis.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

else:
    st.info("Silakan upload file Excel (.xlsx) berisi data 50 siswa.")