import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.linear_model import LinearRegression
from scipy.stats import pearsonr
import io

st.set_page_config(page_title="Dashboard Nilai Siswa", layout="wide")

st.title("📊 Dashboard Analisis Data Siswa (Excel)")

# Upload file Excel
uploaded_file = st.file_uploader("Upload file Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, engine="openpyxl")
    df.columns = df.columns.str.strip()  # Hapus spasi ekstra

    st.subheader("📋 Data Awal")
    st.dataframe(df)

    # Ambil kolom numerik
    df_numeric = df.select_dtypes(include=np.number)
    if df_numeric.shape[1] == 0:
        st.error("Tidak ada kolom numerik untuk dianalisis.")
    else:
        # Tambahkan kolom rata-rata
        df["Rata-rata"] = df_numeric.mean(axis=1)

        # ==============================
        # 1-4 Statistik Umum
        # ==============================
        st.subheader("📌 Statistik Umum")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Jumlah Siswa", len(df))
        col2.metric("Rata-rata Kelas", round(df["Rata-rata"].mean(), 2))
        col3.metric("Nilai Tertinggi", round(df["Rata-rata"].max(), 2))
        col4.metric("Nilai Terendah", round(df["Rata-rata"].min(), 2))

        # ==============================
        # 5. Histogram Interaktif (Plotly)
        # ==============================
        st.subheader("📈 Distribusi Nilai")
        fig_hist = px.histogram(df, x="Rata-rata", nbins=10, title="Distribusi Nilai Siswa")
        st.plotly_chart(fig_hist)

        # ==============================
        # 6. Heatmap Korelasi (Seaborn)
        # ==============================
        st.subheader("🔥 Heatmap Korelasi (Hanya Warna)")
        # Ambil kolom numerik
        df_numeric = df.select_dtypes(include=np.number)
        corr = df_numeric.corr()
        fig, ax = plt.subplots(figsize=(8,6))  # ukuran lebih besar
        sns.heatmap(corr, annot=False, cmap="coolwarm", linewidths=0.5, ax=ax)
        plt.xticks(rotation=45)
        plt.yticks(rotation=0)
        st.pyplot(fig)

        # ==============================
        # 7. Analisis Regresi Linear
        # ==============================
        st.subheader("📊 Analisis Regresi Linear")
        if df_numeric.shape[1] >= 2:
            col_x = st.selectbox("Pilih Variabel X", df_numeric.columns)
            col_y = st.selectbox("Pilih Variabel Y", df_numeric.columns)

            if col_x != col_y:
                X = df[[col_x]]
                Y = df[col_y]

                model = LinearRegression()
                model.fit(X, Y)
                Y_pred = model.predict(X)

                r, p_value = pearsonr(df[col_x], df[col_y])
                r2 = model.score(X, Y)

                fig_reg = px.scatter(df, x=col_x, y=col_y, title="Scatter Plot + Regresi")
                fig_reg.add_scatter(x=df[col_x], y=Y_pred, mode='lines', name='Regresi')
                st.plotly_chart(fig_reg)

                st.write(f"Koefisien Korelasi (r): {r:.4f}")
                st.write(f"P-value: {p_value:.4f}")
                st.write(f"R²: {r2:.4f}")
                st.write(f"Persamaan: y = {model.intercept_:.2f} + {model.coef_[0]:.2f}x")
            else:
                st.warning("Pilih dua variabel yang berbeda untuk regresi.")

        # ==============================
        # 8. Top 5 & Bottom 5 Siswa
        # ==============================
        st.subheader("🏆 Top & Bottom 5 Siswa")
        top5 = df.sort_values(by="Rata-rata", ascending=False).head(5)
        bottom5 = df.sort_values(by="Rata-rata", ascending=True).head(5)

        st.write("Top 5 Nilai Tertinggi")
        st.dataframe(top5.iloc[:, [0, -1]])

        st.write("Top 5 Nilai Terendah")
        st.dataframe(bottom5.iloc[:, [0, -1]])

        # ==============================
        # Download Hasil Analisis
        # ==============================
        st.subheader("📥 Download Hasil Analisis")
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Hasil Analisis')
        st.download_button(
            label="Download ke Excel",
            data=output.getvalue(),
            file_name="hasil_analisis.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:

    st.info("Silakan upload file Excel (.xlsx) untuk memulai analisis.")
