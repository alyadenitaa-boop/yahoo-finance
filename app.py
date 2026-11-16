
import streamlit as st
import yfinance as yf
import plotly.express as px

st.set_page_config(
    page_title="Yahoo Finance Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Yahoo Finance Dashboard")
st.write("Aplikasi pemantauan harga saham menggunakan Yahoo Finance.")

# Pilihan saham
daftar_saham = {
    "BBCA - Bank Central Asia": "BBCA.JK",
    "BBRI - Bank Rakyat Indonesia": "BBRI.JK",
    "BMRI - Bank Mandiri": "BMRI.JK",
    "TLKM - Telkom Indonesia": "TLKM.JK",
    "ASII - Astra International": "ASII.JK",
    "AAPL - Apple Inc": "AAPL"
}

pilihan = st.sidebar.selectbox(
    "Pilih Saham",
    list(daftar_saham.keys())
)

ticker = daftar_saham[pilihan]

periode = st.sidebar.selectbox(
    "Pilih Periode",
    ["1mo", "3mo", "6mo", "1y", "2y", "5y"]
)

if st.sidebar.button("Tampilkan Data"):
    st.cache_data.clear()

try:
    saham = yf.Ticker(ticker)
    data = saham.history(period=periode)

    if data.empty:
        st.error("Data saham tidak tersedia.")
    else:
        harga_terakhir = data["Close"].iloc[-1]
        harga_sebelumnya = data["Close"].iloc[-2] if len(data) > 1 else harga_terakhir
        perubahan = harga_terakhir - harga_sebelumnya

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Harga Terakhir",
            f"{harga_terakhir:,.2f}"
        )

        col2.metric(
            "Perubahan Harga",
            f"{perubahan:,.2f}"
        )

        col3.metric(
            "Volume Terakhir",
            f"{data['Volume'].iloc[-1]:,.0f}"
        )

        st.subheader("Grafik Pergerakan Harga Saham")

        grafik = px.line(
            data,
            x=data.index,
            y="Close",
            title=f"Pergerakan Harga {ticker}",
            labels={
                "Date": "Tanggal",
                "Close": "Harga Penutupan"
            }
        )

        st.plotly_chart(grafik, use_container_width=True)

        st.subheader("Data Historis Saham")
        st.dataframe(data, use_container_width=True)

except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")
