import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Dargeçit Sınav Sorgulama", layout="centered")

st.title("🏆 Sınav Sonuç Sorgulama Sistemi")

# --- DİNAMİK SINIF SEÇİMİ ---
# 4'ten 12'ye kadar olan tüm sınıfları kontrol eder
mevcut_kademeler = []
for i in range(4, 13):
    if os.path.exists(f"sonuclar_{i}.xlsx"):
        mevcut_kademeler.append(f"{i}. Sınıf")

if not mevcut_kademeler:
    st.error("Sistemde yüklü sınav bulunamadı. Lütfen yöneticinizle iletişime geçin.")
    st.stop()

secilen_kademe_str = st.selectbox("Lütfen Sınıfınızı Seçiniz:", mevcut_kademeler)
secilen_kademe_no = secilen_kademe_str.split(".")[0]
aktif_dosya = f"sonuclar_{secilen_kademe_no}.xlsx"

# --- VERİ YÜKLEME ---
@st.cache_data
def veriyi_oku(dosya):
    df = pd.read_excel(dosya)
    # Öğrenci no temizliği (Baştaki sıfırlar ve float dönüşümü engelleme)
    df['Arama_No'] = df['Öğrenci No'].astype(str).str.lstrip('0').str.split('.').str[0]
    return df

df = veriyi_oku(aktif_dosya)

# --- SORGULAMA EKRANI ---
st.markdown("---")
tab1, tab2 = st.tabs(["👤 Öğrenci Girişi", "👨‍🏫 Kurumsal Raporlar"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        okul = st.selectbox("Okulunuz:", sorted(df['OKUL ADI'].unique()), key="ogr_okul")
    with col2:
        no = st.text_input("Okul Numaranız:", key="ogr_no").lstrip('0')
        
    if st.button("Sonucumu Getir"):
        sonuc = df[(df['OKUL ADI'] == okul) & (df['Arama_No'] == no)]
        if not sonuc.empty:
            ogr = sonuc.iloc[0]
            st.success(f"Merhaba {ogr['Ad']} {ogr['Soyad']}, sonucun hazır!")
            # Karne tasarımı buraya gelecek...
        else:
            st.error("Kayıt bulunamadı. Lütfen okulunuzu ve numaranızı kontrol edin.")

with tab2:
    st.subheader("Okul Müdürleri ve Öğretmenler İçin")
    sifre = st.text_input("Kurumsal Erişim Şifresi:", type="password")
    # İsterseniz buraya basit bir şifre (Örn: dargecit2026) koyabilirsiniz
    if sifre == "darder47": 
        kurum_okul = st.selectbox("Okul Seçiniz:", ["Tüm İlçe"] + sorted(df['OKUL ADI'].unique()))
        # Filtreleme ve Tablo gösterme kodları...
        st.write(f"{kurum_okul} listesi hazırlanıyor...")
    elif sifre != "":
        st.error("Hatalı Şifre!")