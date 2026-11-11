import joblib
import pandas as pd
import streamlit as st

fitur = ["ALLSKY_SFC_SW_DWN", "T2M", "RH2M", "WS10M"]
model = joblib.load("model_latihan.joblib")
batas = pd.read_csv("batas.csv", index_col=0)

st.title("Latihan: Estimasi Daya PLTS Atap")
st.caption(
    "Model latihan dari data simulasi satu titik di Denpasar, "
    "tahun 2020 sampai 2022. Bukan hasil penelitian."
)

radiasi = st.number_input("Radiasi matahari (ALLSKY_SFC_SW_DWN)", value=5.5, format="%.4f")
suhu = st.number_input("Suhu udara (T2M)", value=25.5, format="%.2f")
kelembapan = st.number_input("Kelembapan relatif (RH2M)", value=84.6, format="%.2f")
angin = st.number_input("Kecepatan angin (WS10M)", value=2.3, format="%.2f")

if st.button("Hitung estimasi"):
    nilai = [radiasi, suhu, kelembapan, angin]
    data = pd.DataFrame([nilai], columns=fitur)
    hasil = float(model.predict(data)[0])
    st.metric("Estimasi daya_listrik (hasil simulasi)", f"{hasil:.2f}")

    di_luar = []
    for nama, angka in zip(fitur, nilai):
        if angka < batas.loc["min", nama] or angka > batas.loc["max", nama]:
            di_luar.append(nama)

    if di_luar:
        st.warning(", ".join(di_luar) + " di luar rentang data latih. Hasil tidak dapat diandalkan.")
    else:
        st.success("Semua masukan berada dalam rentang data latih.")
