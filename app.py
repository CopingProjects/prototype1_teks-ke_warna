import streamlit as st
from warna_utils import buat_visualisasi

st.set_page_config(page_title="Teks ke Warna", layout="wide")

st.title("🎨 Teks ke Warna - Prototype 1")
st.write("Masukkan teks di bawah ini, lalu lihat hasil visualisasinya berdasarkan frekuensi huruf dan tanda baca.")

teks = st.text_area("Masukkan teks:", height=200)

if st.button("Tampilkan Visualisasi"):
    if teks.strip():
        fig = buat_visualisasi(teks)
        st.pyplot(fig)
    else:
        st.warning("Tolong masukkan teks terlebih dahulu.")