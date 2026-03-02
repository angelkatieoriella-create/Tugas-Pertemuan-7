import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard Nilai Siswa", layout="wide")

st.title("📊 Dashboard Interaktif Nilai 50 Siswa")

# =========================
# Upload File CSV
# =========================
uploaded_file = st.file_uploader("Upload File CSV Data Siswa", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Ambil semua kolom nilai (anggap kolom pertama adalah Nama)
    nilai_columns = df.columns[1:]

    # Hitung rata-rata tiap siswa
    df["Rata-rata"] = df[nilai_columns].mean(axis=1)

    # =========================
    # Statistik Utama
    # =========================
    st.subheader("📌 Statistik Nilai")

    rata_kelas = df["Rata-rata"].mean()
    nilai_max = df["Rata-rata"].max()
    nilai_min = df["Rata-rata"].min()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Jumlah Siswa", len(df))
    col2.metric("Rata-rata Kelas", round(rata_kelas, 2))
    col3.metric("Nilai Tertinggi", round(nilai_max, 2))
    col4.metric("Nilai Terendah", round(nilai_min, 2))

    # =========================
    # Slider Batas Skor
    # =========================
    st.subheader("🎯 Pengaturan Kategori Nilai")

    batas = st.slider("Tentukan Batas Nilai Tinggi", 50, 100, 75)

    df["Kategori"] = df["Rata-rata"].apply(
        lambda x: "Tinggi" if x >= batas else "Rendah"
    )

    # =========================
    # Grafik Rata-rata per Siswa
    # =========================
    st.subheader("📈 Grafik Rata-rata Setiap Siswa")

    fig1, ax1 = plt.subplots()
    ax1.plot(df["Rata-rata"])
    ax1.set_xlabel("Urutan Siswa")
    ax1.set_ylabel("Rata-rata Nilai")
    ax1.set_title("Rata-rata Nilai 50 Siswa")
    st.pyplot(fig1)

    # =========================
    # Grafik Distribusi Nilai
    # =========================
    st.subheader("📊 Distribusi Nilai Siswa")

    fig2, ax2 = plt.subplots()
    ax2.hist(df["Rata-rata"], bins=10)
    ax2.set_xlabel("Nilai")
    ax2.set_ylabel("Jumlah Siswa")
    st.pyplot(fig2)

    # =========================
    # Grafik Tinggi vs Rendah
    # =========================
    st.subheader("📊 Perbandingan Skor Tinggi dan Rendah")

    kategori_count = df["Kategori"].value_counts()

    fig3, ax3 = plt.subplots()
    ax3.bar(kategori_count.index, kategori_count.values)
    ax3.set_xlabel("Kategori")
    ax3.set_ylabel("Jumlah Siswa")
    st.pyplot(fig3)

    # =========================
    # Top 5 Nilai Tertinggi
    # =========================
    st.subheader("🏆 Top 5 Siswa dengan Rata-rata Tertinggi")

    top5 = df.sort_values(by="Rata-rata", ascending=False).head(5)
    st.dataframe(top5)

    # =========================
    # Tampilkan Data Lengkap
    # =========================
    st.subheader("📋 Data Lengkap Siswa")
    st.dataframe(df)

else:
    st.info("Silakan upload file CSV berisi data 50 siswa.")