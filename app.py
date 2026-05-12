import streamlit as st
import pandas as pd
import io

# Sayfa Ayarları
st.set_page_config(page_title="1. Dargeçit Matematik Olimpiyatı", layout="wide", page_icon="📐")

# --- PROFESYONEL CSS TASARIMI ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stHeader { background-color: #ffffff; padding: 20px; border-bottom: 3px solid #1e3a8a; border-radius: 10px; margin-bottom: 20px; }
    .result-card { background: white; padding: 25px; border-radius: 15px; border-left: 10px solid #1e3a8a; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
    .metric-val { font-size: 24px; font-weight: bold; color: #1e3a8a; }
    .metric-label { font-size: 14px; color: #666; }
    .badge { padding: 5px 10px; border-radius: 5px; color: white; font-weight: bold; }
    .badge-success { background-color: #10b981; }
    .badge-info { background-color: #3b82f6; }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ OKUMA (Hızlandırılmış Caching) ---
@st.cache_data
def veriyi_oku(dosya_adi):
    if not os.path.exists(dosya_adi): return None
    df = pd.read_excel(dosya_adi)
    df['Arama_No'] = df['Öğrenci No'].astype(str).str.lstrip('0').str.split('.').str[0]
    return df

# --- ÜST BANNER ---
st.markdown("""
    <div class="stHeader">
        <h1 style='text-align: center; color: #1e3a8a; margin:0;'>🥇 1. DARGEÇİT MATEMATİK OLİMPİYATLARI</h1>
        <p style='text-align: center; color: #555; font-size: 18px;'>1. Aşama Sınav Sonuç Sorgulama Sistemi</p>
    </div>
    """, unsafe_allow_html=True)

# Sınıf Seçimi
siniflar = [f"{i}. Sınıf" for i in range(4, 13)]
secilen_sinif_str = st.sidebar.selectbox("📐 Sınav Kategorisi Seçiniz:", siniflar, index=3)
secilen_no = secilen_sinif_str.split(".")[0]
aktif_dosya = f"sonuclar_{secilen_no}.xlsx"

import os
df = veriyi_oku(aktif_dosya)

if df is None:
    st.info(f"ℹ️ {secilen_sinif_str} kategorisine ait sonuçlar henüz sisteme yüklenmemiştir.")
else:
    tab1, tab2 = st.tabs(["👤 Öğrenci Sorgulama", "🏫 Müdür & Kurum Paneli"])

    with tab1:
        st.markdown("### 🔍 Sonucunu Öğren")
        c1, c2 = st.columns(2)
        with c1:
            okul = st.selectbox("Okulunuzu Seçin:", sorted(df['OKUL ADI'].unique()))
        with c2:
            ogr_no = st.text_input("Öğrenci Numarası (Örn: 35 veya 250035):").lstrip('0')

        if st.button("Sınav Sonucunu Göster", type="primary"):
            sonuc = df[(df['OKUL ADI'] == okul) & (df['Arama_No'] == ogr_no)]
            if not sonuc.empty:
                st.balloons()
                o = sonuc.iloc[0]
                
                # ÖĞRENCİ KARNE KARTI
                st.markdown(f"""
                <div class="result-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <h2 style='margin:0;'>{o['Ad']} {o['Soyad']}</h2>
                            <p style='color:#666;'>{o['OKUL ADI']} - {o['Sınıf']}/{o['Şube']}</p>
                        </div>
                        <div style='text-align:right;'>
                            <span class="badge badge-info">İlçe Sırası: {o['İlçe Sırası']}</span><br>
                            <span class="badge badge-success" style="margin-top:5px;">Okul Sırası: {o['Okul Sırası']}</span>
                        </div>
                    </div>
                    <hr>
                    <div style="display: flex; justify-content: space-around; text-align:center;">
                        <div><div class="metric-label">Doğru</div><div class="metric-val">{o['Doğru']}</div></div>
                        <div><div class="metric-label">Yanlış</div><div class="metric-val">{o['Yanlış']}</div></div>
                        <div><div class="metric-label">Net</div><div class="metric-val" style="color:#2563eb;">{o['Net']}</div></div>
                        <div><div class="metric-label">Puan</div><div class="metric-val" style="color:#059669; font-size:32px;">{o['Puan']}</div></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # YORUM KARNESİ
                p = o['Puan']
                if p >= 80: yorum = "Mükemmel! Matematiksel yeteneğin ilçe standartlarının üzerinde."
                elif p >= 60: yorum = "Çok iyi. Birkaç dikkatsizlik dışında harika bir performans."
                elif p >= 40: yorum = "Başarılı. Eksik konularını tamamlayarak daha iyi olabilirsin."
                else: yorum = "Bu bir başlangıç. Bir sonraki olimpiyatta daha iyi olacağına inanıyoruz."
                
                st.info(f"📝 **Öğrenci Analiz Notu:** {yorum}")
            else:
                st.error("❌ Kayıt bulunamadı. Lütfen bilgilerinizi kontrol ediniz.")

    with tab2:
        sifre = st.text_input("🔐 Kurum Şifresi:", type="password")
        if sifre == "darder47":
            st.success("Yetki Onaylandı. Listeler Hazırlanıyor...")
            # Burada listelemeyi sadece okul bazlı yaparak hızı artırıyoruz
            kurum_okul = st.selectbox("Görüntülenecek Kurum:", ["Tüm İlçe"] + sorted(df['OKUL ADI'].unique()))
            
            f_df = df if kurum_okul == "Tüm İlçe" else df[df['OKUL ADI'] == kurum_okul]
            st.dataframe(f_df[['İlçe Sırası', 'Okul Sırası', 'OKUL ADI', 'Sınıf', 'Şube', 'Ad', 'Soyad', 'Net', 'Puan']], use_container_width=True)
            
            # TOPLU PDF BUTONU (Sadece burada PDF kodu çalışacak, bu yüzden ana ekran yavaşlamayacak)
            if st.button("📥 Toplu Karneleri PDF Aktar (Yazdır)"):
                st.write("PDF Dosyanız Arka Planda Hazırlanıyor, Lütfen Bekleyin...")
                # PDF oluşturma fonksiyonu buraya çağrılacak