import streamlit as st
import pandas as pd
import io
import ast
import os

# --- KURUMSAL SAYFA AYARLARI ---
st.set_page_config(page_title="1. Dargeçit Matematik Olimpiyatı Sonuç Portalı", layout="wide", page_icon="🥇")

# --- PROFESYONEL CSS ---
st.markdown("""
    <style>
    :root {
        --meb-kirmizi: #E30A17;
        --koyu-siyah: #111827;
        --acik-gri: #f3f4f6;
    }
    .main { background-color: var(--acik-gri); }
    .header-banner { 
        background-color: white; padding: 20px; border-bottom: 4px solid var(--meb-kirmizi); 
        border-radius: 10px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); text-align: center; 
    }
    .header-banner h1 { color: var(--koyu-siyah); font-weight: 800; font-size: 28px; margin-bottom: 5px; }
    .header-banner h3 { color: var(--meb-kirmizi); font-weight: 600; font-size: 16px; margin-top: 0; }
    .stButton>button { background-color: var(--koyu-siyah); color: white; border-radius: 8px; font-weight: bold; border:none; }
    .stButton>button:hover { background-color: var(--meb-kirmizi); color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- ÜST BANNER ---
st.markdown("""
    <div class="header-banner">
        <h1>🥇 1. DARGEÇİT MATEMATİK OLİMPİYATI</h1>
        <h3>1. Aşama Sınav Sonuç ve Analiz Portalı</h3>
    </div>
""", unsafe_allow_html=True)

# --- VERİ OKUMA ---
@st.cache_data
def veriyi_oku(dosya_adi):
    if not os.path.exists(dosya_adi): return None
    df = pd.read_excel(dosya_adi)
    # Baştaki sıfırları temizleyip güvenli arama no oluşturma
    df['Arama_No'] = df['Öğrenci No'].astype(str).str.lstrip('0').str.split('.').str[0]
    # Otomatik en yüksek puandan en düşüğe sıralama
    df = df.sort_values(by=['Puan', 'Net'], ascending=[False, False]).reset_index(drop=True)
    return df

siniflar = [f"{i}. Sınıf" for i in range(4, 13)]
secilen_sinif = st.sidebar.selectbox("Kategori Seçiniz:", siniflar, index=3)
dosya_adi = f"sonuclar_{secilen_sinif.split('.')[0]}.xlsx"

df = veriyi_oku(dosya_adi)

if df is None:
    st.warning(f"⚠️ {secilen_sinif} verileri henüz sisteme yüklenmedi.")
else:
    tab1, tab2 = st.tabs(["👤 Bireysel Sonuç Öğrenme", "🏫 Kurum ve Öğretmen Paneli (Toplu Liste)"])

    # =========================================================
    # 1. BİREYSEL KARNE EKRANI
    # =========================================================
    with tab1:
        st.markdown("### 🔍 Öğrenci Sonuç Sorgulama")
        c1, c2 = st.columns(2)
        with c1: okul_secim = st.selectbox("Okulunuz:", sorted(df['OKUL ADI'].unique()))
        with c2: no_secim = st.text_input("Öğrenci Numaranız (Örn: 35 veya 250035):").lstrip('0')

        if st.button("Sonucumu Getir", type="primary"):
            sonuc = df[(df['OKUL ADI'] == okul_secim) & (df['Arama_No'] == no_secim)]
            if not sonuc.empty:
                st.balloons()
                ogr = sonuc.iloc[0]
                
                # Yorum Algoritması
                p = ogr['Puan']
                if p >= 85: yorum = "🌟 Üstün Başarı! Olimpiyat standartlarında harika bir analitik zekaya sahipsin. 2. Aşamada başarılar!"
                elif p >= 65: yorum = "👍 Çok İyi! Birkaç küçük dikkat hatası dışında hedefine çok yakınsın."
                elif p >= 40: yorum = "📚 Başarılı bir temel. Düzenli soru çözümü ile netlerini hızla zirveye taşıyabilirsin."
                else: yorum = "💪 Asla pes etme! Bu sınav senin için harika bir tecrübe oldu, çalışmaya devam."

                st.markdown(f"""
                <div style="background:white; padding:30px; border-radius:15px; border-top:5px solid var(--meb-kirmizi); box-shadow:0 10px 25px rgba(0,0,0,0.1);">
                    <h2 style="color:var(--koyu-siyah); margin:0;">{ogr['Ad']} {ogr['Soyad']}</h2>
                    <p style="color:#555; font-size:16px;">{ogr['OKUL ADI']} - {ogr['Sınıf']}/{ogr['Şube']} | İlçe Sırası: <b>{ogr['İlçe Sırası']}</b> | Okul Sırası: <b>{ogr['Okul Sırası']}</b></p>
                    <hr>
                    <div style="display:flex; justify-content:space-around; text-align:center; margin:20px 0;">
                        <div><p style="color:#666; margin:0;">Doğru</p><h3 style="color:#059669; margin:0;">{ogr['Doğru']}</h3></div>
                        <div><p style="color:#666; margin:0;">Yanlış</p><h3 style="color:#E30A17; margin:0;">{ogr['Yanlış']}</h3></div>
                        <div><p style="color:#666; margin:0;">Boş</p><h3 style="color:#6b7280; margin:0;">{ogr['Boş']}</h3></div>
                        <div><p style="color:#666; margin:0;">Net</p><h3 style="color:#2563eb; margin:0;">{ogr['Net']}</h3></div>
                        <div><p style="color:#666; margin:0;">Puan</p><h2 style="color:var(--koyu-siyah); margin:0;">{ogr['Puan']}</h2></div>
                    </div>
                    <div style="background:#fef2f2; padding:15px; border-radius:8px; border-left:4px solid var(--meb-kirmizi); margin-top:20px;">
                        <p style="margin:0; color:var(--koyu-siyah);"><b>Analiz Notu:</b> {yorum}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("Kayıt bulunamadı. Lütfen okulunuzu ve numaranızı kontrol edin.")

    # =========================================================
    # 2. KURUMSAL PANEL VE IŞIK HIZINDA PDF AKTARIMI
    # =========================================================
    with tab2:
        sifre = st.text_input("🔐 Öğretmen/İdareci Şifresi:", type="password")
        if sifre == "darder47":
            st.success("Giriş Başarılı.")
            kurum = st.selectbox("Raporlanacak Okul:", ["Tüm İlçe Listesi"] + sorted(df['OKUL ADI'].unique()))
            
            f_df = df if kurum == "Tüm İlçe Listesi" else df[df['OKUL ADI'] == kurum]

            # Arayüzde Tablo Gösterimi
            st.dataframe(f_df[['İlçe Sırası', 'Okul Sırası', 'OKUL ADI', 'Sınıf', 'Şube', 'Öğrenci No', 'Ad', 'Soyad', 'Doğru', 'Yanlış', 'Net', 'Puan']], use_container_width=True)

            colA, colB, colC = st.columns(3)
            
            # Excel İndir
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                f_df.to_excel(writer, index=False)
            colA.download_button("📊 Excel İndir", data=buffer.getvalue(), file_name=f"{kurum}_sonuclar.xlsx", use_container_width=True)
            
            # CSV İndir
            csv_data = f_df.to_csv(index=False).encode('utf-8-sig')
            colB.download_button("📑 CSV İndir", data=csv_data, file_name=f"{kurum}_sonuclar.csv", use_container_width=True)
            
            # GÜNCEL, BÜYÜK YAZILI VE ÖĞRENCİ NUMARALI PDF ŞABLONU
            html_sablon = """
            <html><head><meta charset="utf-8"><style>
                @page { size: A4; margin: 10mm; }
                body { font-family: 'Segoe UI', Arial, sans-serif; background: white; font-size: 13px; margin: 0; color: #111827; }
                .karne { border: 2px solid #111827; border-radius: 12px; padding: 20px; margin-bottom: 25px; width: 48%; float: left; margin-right: 2%; box-sizing: border-box; page-break-inside: avoid; }
                .baslik { color: #E30A17; text-align: center; font-weight: 900; font-size: 16px; border-bottom: 3px solid #eee; padding-bottom: 8px; margin-bottom: 12px; }
                .kimlik { display: flex; justify-content: space-between; font-weight: bold; margin-bottom: 10px; font-size: 14px; }
                .siralama { text-align: center; background: #111827; color: white; padding: 8px; border-radius: 6px; margin-bottom: 15px; font-size: 12px; font-weight: bold; }
                .analiz-tablo { width: 100%; border-collapse: collapse; text-align: center; margin-bottom: 15px; font-size: 14px; }
                .analiz-tablo th { background: #f3f4f6; border: 1px solid #ccc; padding: 6px; color: #111827; }
                .analiz-tablo td { border: 1px solid #ccc; padding: 8px; font-weight: bold; font-size: 15px; }
                .optik-tablo { width: 100%; border-collapse: collapse; text-align: center; font-size: 12px; }
                .optik-tablo td, .optik-tablo th { border: 1px solid #ccc; padding: 5px; }
                .optik-tablo th { background: #e5e7eb; }
                .dogru { background-color: #dcfce7; color: #059669; font-weight: 900; }
                .yanlis { background-color: #fee2e2; color: #E30A17; font-weight: 900; font-size: 13px; }
                .bos { color: #9ca3af; font-weight: bold; }
                .yorum { margin-top: 15px; padding: 10px; background: #fef2f2; border-left: 4px solid #E30A17; font-size: 12px; font-style: italic; font-weight: 600; line-height: 1.4; }
            </style></head><body>
            """
            
            for index, row in f_df.iterrows():
                try:
                    ogr_cevap = ast.literal_eval(row['Ogrenci_Cevap_Listesi']) if isinstance(row['Ogrenci_Cevap_Listesi'], str) else []
                    dogru_cevap = ast.literal_eval(row['Cevap_Anahtari_Listesi']) if isinstance(row['Cevap_Anahtari_Listesi'], str) else []
                except:
                    ogr_cevap = list(row.get('Ogrenci_Cevap_Listesi', ''))
                    dogru_cevap = list(row.get('Cevap_Anahtari_Listesi', ''))

                soru_th, key_td, stu_td = "", "", ""
                
                for i in range(len(dogru_cevap)):
                    soru_th += f"<th>{i+1}</th>"
                    anahtar_cvp = dogru_cevap[i]
                    key_td += f"<td>{anahtar_cvp}</td>"
                    ogr_cvp = ogr_cevap[i] if i < len(ogr_cevap) else '-'
                    
                    if ogr_cvp == anahtar_cvp and ogr_cvp != '-':
                        stu_td += f"<td class='dogru'>{ogr_cvp}</td>" 
                    elif ogr_cvp != anahtar_cvp and ogr_cvp != '-':
                        stu_td += f"<td class='yanlis'>{ogr_cvp}</td>" 
                    else:
                        stu_td += f"<td class='bos'>-</td>"

                p = row['Puan']
                if p >= 85: yr = "🌟 Üstün Başarı! Olimpiyat standartlarında harika bir analitik zekaya sahipsin. 2. Aşamada başarılar!"
                elif p >= 65: yr = "👍 Çok İyi! Birkaç küçük dikkat hatası dışında hedefine çok yakınsın."
                elif p >= 40: yr = "📚 Başarılı bir temel. Düzenli soru çözümü ile netlerini artırabilirsin."
                else: yr = "💪 Bu sınav harika bir tecrübe oldu, eksiklerini kapatarak yola devam et."

                html_sablon += f"""
                <div class="karne">
                    <div class="baslik">1. DARGEÇİT MATEMATİK OLİMPİYATI</div>
                    <div class="kimlik">
                        <span>{row['Ad']} {row['Soyad']}</span>
                        <span style="color:#E30A17;">Öğr. No: {row.get('Öğrenci No', '-')}</span>
                    </div>
                    <div class="kimlik" style="font-size: 12px; color: #555; margin-bottom:12px;">
                        <span>{row['OKUL ADI']}</span>
                        <span>Sınıf: {row['Sınıf']}/{row['Şube']}</span>
                    </div>
                    <div class="siralama">İlçe Sırası: {row['İlçe Sırası']} &nbsp;|&nbsp; Okul Sırası: {row['Okul Sırası']}</div>
                    
                    <table class="analiz-tablo">
                        <tr><th>Doğru</th><th>Yanlış</th><th>Boş</th><th>Net</th><th>Puan</th></tr>
                        <tr>
                            <td style="color:#059669;">{row['Doğru']}</td>
                            <td style="color:#E30A17;">{row['Yanlış']}</td>
                            <td style="color:#6b7280;">{row['Boş']}</td>
                            <td style="color:#2563eb;">{row['Net']}</td>
                            <td style="font-size:16px; color:#111827; background:#fef08a;">{row['Puan']}</td>
                        </tr>
                    </table>

                    <table class="optik-tablo">
                        <tr><td>Soru</td>{soru_th}</tr>
                        <tr><td>Cevap</td>{key_td}</tr>
                        <tr><td>Öğrenci</td>{stu_td}</tr>
                    </table>
                    
                    <div class="yorum">{yr}</div>
                </div>
                """
                if (index + 1) % 2 == 0: html_sablon += "<div style='clear: both;'></div>"
                if (index + 1) % 6 == 0: html_sablon += "<div style='page-break-after: always; clear: both;'></div>"

            html_sablon += "</body></html>"
            
            st.markdown("""<style> div[data-testid="stDownloadButton"] button { background-color: #E30A17; color: white; font-weight: bold; width:100%; border-radius: 8px;} </style>""", unsafe_allow_html=True)
            colC.download_button("🖨️ PDF Karneleri Al (Hızlı Çıktı)", data=html_sablon, file_name=f"{kurum}_Karneler.html", mime="text/html")
