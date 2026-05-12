import streamlit as st
import pandas as pd
import io
import os
import glob
import plotly.express as px

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Dargeçit Olimpiyat Analiz Merkezi", layout="wide", page_icon="📈")

# --- KRİSTAL NETLİĞİNDE KURUMSAL CSS ---
st.markdown("""
    <style>
    :root {
        --meb-red: #E30A17;
        --navy: #111827;
        --light-gray: #f8fafc;
    }
    .main { background-color: var(--light-gray); }
    * { -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }

    .header-box {
        background: white; padding: 25px; border-bottom: 6px solid var(--meb-red);
        border-radius: 12px; margin-bottom: 30px; text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }
    .header-box h1 { color: var(--navy); font-weight: 900; font-size: 32px; margin: 0; letter-spacing: -0.5px; }
    .header-box h3 { color: var(--meb-red); font-weight: 800; font-size: 18px; margin-top: 5px; text-transform: uppercase; }
    
    .metric-card {
        background: white; border-radius: 10px; padding: 20px; text-align: center;
        border: 1px solid #e2e8f0; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .metric-card h2 { margin: 0; color: var(--navy); font-size: 36px; font-weight: 900; }
    .metric-card p { margin: 0; color: #64748b; font-size: 14px; font-weight: bold; text-transform: uppercase; }
    
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] { height: 50px; background: white; border-radius: 8px 8px 0 0; font-weight: bold; border: 1px solid #ddd; }
    .stTabs [aria-selected="true"] { background: var(--navy) !important; color: white !important; border-bottom: 4px solid var(--meb-red); }
    </style>
    """, unsafe_allow_html=True)

# --- BANNER ---
st.markdown("""
    <div class="header-box">
        <h1>📈 T.C. DARGEÇİT KAYMAKAMLIĞI</h1>
        <h3>İlçe Milli Eğitim Müdürlüğü - Sınav Analiz ve İstatistik Merkezi</h3>
    </div>
""", unsafe_allow_html=True)

# --- TÜM VERİLERİ TOPLAMA MOTORU (Öğrenci isimleri silinir, sadece istatistik alınır) ---
@st.cache_data
def tum_verileri_yukle():
    dosyalar = glob.glob("sonuclar_*.xlsx")
    df_list = []
    for d in dosyalar:
        try:
            temp_df = pd.read_excel(d)
            # Analiz için gerekli sütunları filtrele, kişisel verileri at
            if set(['OKUL ADI', 'Sınıf', 'Şube', 'Puan', 'Net']).issubset(temp_df.columns):
                # Öğrenci adı, soyadı, no gibi alanları siliyoruz (Güvenlik)
                clean_df = temp_df[['OKUL ADI', 'Sınıf', 'Şube', 'Doğru', 'Yanlış', 'Boş', 'Net', 'Puan']].copy()
                df_list.append(clean_df)
        except: pass
    if df_list:
        return pd.concat(df_list, ignore_index=True)
    return None

df_genel = tum_verileri_yukle()

if df_genel is None or df_genel.empty:
    st.error("⚠️ Sistemde istatistiği çıkarılacak sonuç dosyası (sonuclar_*.xlsx) bulunamadı.")
else:
    # Veri Temizliği ve Düzenleme
    df_genel['Sınıf'] = df_genel['Sınıf'].astype(str).str.replace('.0', '', regex=False)
    df_genel['Şube'] = df_genel['Şube'].astype(str).str.strip().str.upper()
    df_genel['Sınıf_Şube'] = df_genel['Sınıf'] + "/" + df_genel['Şube']
    
    # Üst İstatistik Kartları
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f"<div class='metric-card'><p>Sınava Giren Toplam Öğrenci</p><h2>{len(df_genel)}</h2></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='metric-card'><p>Katılım Sağlayan Okul Sayısı</p><h2>{df_genel['OKUL ADI'].nunique()}</h2></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='metric-card'><p>İlçe Geneli Puan Ortalaması</p><h2 style='color:#059669;'>{df_genel['Puan'].mean():.2f}</h2></div>", unsafe_allow_html=True)
    with c4: st.markdown(f"<div class='metric-card'><p>İlçe Geneli Net Ortalaması</p><h2 style='color:#2563eb;'>{df_genel['Net'].mean():.2f}</h2></div>", unsafe_allow_html=True)
    
    st.write("")
    tab1, tab2, tab3 = st.tabs(["🏆 İLÇE GENELİ OKUL BAŞARI SIRALAMASI", "📊 SINIF VE ŞUBE (ÖĞRETMEN) ANALİZLERİ", "🖨️ KURUMSAL RAPOR ÇIKTISI (PDF)"])

    # =========================================================
    # TAB 1: İLÇE GENELİ OKUL KARŞILAŞTIRMASI
    # =========================================================
    with tab1:
        st.subheader("🏢 Okulların Genel Matematik Performansı")
        st.markdown("Aşağıdaki grafik ve tablo, okulların tüm sınıflar bazındaki **Puan Ortalamasına** göre sıralamasını göstermektedir.")
        
        # Okul Bazlı Ortalama Hesaplama
        df_okul = df_genel.groupby('OKUL ADI').agg(
            Öğrenci_Sayısı=('Puan', 'count'),
            Ortalama_Net=('Net', 'mean'),
            Ortalama_Puan=('Puan', 'mean')
        ).reset_index().sort_values(by='Ortalama_Puan', ascending=True) # Grafik için ascending
        
        # Grafik
        fig = px.bar(df_okul, x='Ortalama_Puan', y='OKUL ADI', orientation='h', 
                     text=df_okul['Ortalama_Puan'].apply(lambda x: f"{x:.2f}"),
                     color='Ortalama_Puan', color_continuous_scale='Reds',
                     title="İlçe Geneli Okul Başarı Sıralaması (Puan Ortalaması)")
        fig.update_layout(height=600, showlegend=False, xaxis_title="Puan Ortalaması", yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)
        
        # Tablo
        df_okul_tablo = df_okul.sort_values(by='Ortalama_Puan', ascending=False).reset_index(drop=True)
        df_okul_tablo.index += 1
        st.dataframe(df_okul_tablo.style.format({"Ortalama_Net": "{:.2f}", "Ortalama_Puan": "{:.2f}"}), use_container_width=True)

    # =========================================================
    # TAB 2: ŞUBE VE ÖĞRETMEN ANALİZİ (REKABET ALANI)
    # =========================================================
    with tab2:
        st.subheader("📉 Sınıf ve Şube Bazlı Başarı İncelemesi")
        st.info("Bu bölüm, aynı okuldaki veya farklı okullardaki şubeleri kıyaslayarak hangi sınıfın/öğretmenin daha başarılı olduğunu tespit etmenizi sağlar.")
        
        secilen_kademe = st.selectbox("İncelenecek Sınıf Kademesini Seçin:", sorted(df_genel['Sınıf'].unique(), key=lambda x: str(x)))
        df_kademe = df_genel[df_genel['Sınıf'] == secilen_kademe]
        
        c_an1, c_an2 = st.columns(2)
        
        with c_an1:
            st.markdown(f"**{secilen_kademe}. Sınıflar Okul Sıralaması**")
            df_kad_okul = df_kademe.groupby('OKUL ADI')['Puan'].mean().reset_index().sort_values(by='Puan', ascending=False)
            fig2 = px.bar(df_kad_okul, x='OKUL ADI', y='Puan', text=df_kad_okul['Puan'].apply(lambda x: f"{x:.2f}"), color='Puan', color_continuous_scale='Blues')
            fig2.update_layout(xaxis_tickangle=-45, xaxis_title="", yaxis_title="Ortalama Puan")
            st.plotly_chart(fig2, use_container_width=True)
            
        with c_an2:
            st.markdown(f"**{secilen_kademe}. Sınıflar İçi Şube (Öğretmen) Rekabeti**")
            df_sube = df_kademe.groupby(['OKUL ADI', 'Şube']).agg(Ogrenci=('Puan', 'count'), Puan_Ort=('Puan', 'mean')).reset_index()
            # Sadece 5'ten fazla öğrencisi olan şubeleri al ki istatistik doğru olsun
            df_sube = df_sube[df_sube['Ogrenci'] >= 3].sort_values(by='Puan_Ort', ascending=False).head(15) # En iyi 15 şube
            df_sube['Okul_Sube'] = df_sube['OKUL ADI'] + " - " + df_sube['Şube']
            
            fig3 = px.bar(df_sube, x='Puan_Ort', y='Okul_Sube', orientation='h', text=df_sube['Puan_Ort'].apply(lambda x: f"{x:.2f}"), color='Puan_Ort', color_continuous_scale='Teal')
            fig3.update_layout(yaxis={'categoryorder':'total ascending'}, xaxis_title="Ortalama Puan", yaxis_title="")
            st.plotly_chart(fig3, use_container_width=True)

    # =========================================================
    # TAB 3: RESMİ KURUMSAL RAPOR (KAYMAYAN PDF ÇIKTISI)
    # =========================================================
    with tab2:
        pass # Sekme düzeni için
        
    with tab3:
        st.subheader("🖨️ İlçe Milli Eğitim Değerlendirme Raporu")
        st.write("Okulların ortalamalarını içeren bu resmi rapor, A4 kağıdına tam oturacak ve kayma yapmayacak şekilde tasarlanmıştır. 'Raporu Al' butonuna tıklayıp tarayıcıda Ctrl+P ile yazdırabilirsiniz.")
        
        # Rapor için Data Hazırlığı (Genel Sıralama)
        rapor_df = df_genel.groupby('OKUL ADI').agg(
            Ogr_Sayisi=('Puan', 'count'),
            Ort_Dogru=('Doğru', 'mean'),
            Ort_Yanlis=('Yanlış', 'mean'),
            Ort_Net=('Net', 'mean'),
            Ort_Puan=('Puan', 'mean')
        ).reset_index().sort_values(by='Ort_Puan', ascending=False)
        rapor_df.index += 1
        
        rapor_html = """
        <html><head><meta charset="utf-8"><style>
            @page { size: A4 portrait; margin: 15mm; }
            * { box-sizing: border-box; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
            body { font-family: 'Segoe UI', Arial, sans-serif; background: white; margin: 0; padding: 0; color: #111827; }
            
            .rapor-konteyner { width: 100%; }
            .baslik-alan { text-align: center; border-bottom: 5px solid #111827; padding-bottom: 15px; margin-bottom: 25px; }
            .baslik-alan h1 { margin: 0; font-size: 24px; font-weight: 900; text-transform: uppercase; }
            .baslik-alan h2 { margin: 8px 0 0 0; color: #E30A17; font-size: 16px; font-weight: bold; }
            
            .info-kutu { display: flex; justify-content: space-between; background: #f8fafc; padding: 15px; border-radius: 8px; border: 1px solid #e2e8f0; margin-bottom: 25px; font-weight: bold; font-size: 14px; }
            
            /* Sayfa kırılmasını (kaymayı) engelleyen tablo yapısı */
            .rapor-tablo { width: 100%; border-collapse: collapse; text-align: center; font-size: 13px; page-break-inside: auto; }
            .rapor-tablo tr { page-break-inside: avoid; page-break-after: auto; }
            .rapor-tablo th { background-color: #111827; color: white; padding: 12px 8px; font-weight: bold; border: 1px solid #111827; }
            .rapor-tablo td { padding: 10px 8px; border: 1px solid #cbd5e1; font-weight: 600; color: #334155; }
            .rapor-tablo tr:nth-child(even) { background-color: #f8fafc; }
            .rapor-tablo tr:hover { background-color: #f1f5f9; }
            
            .puan-hucre { background-color: #fef2f2 !important; color: #E30A17 !important; font-size: 15px; font-weight: 900 !important; }
            
            .alt-bilgi { margin-top: 30px; font-size: 11px; color: #64748b; text-align: center; border-top: 1px solid #e2e8f0; padding-top: 10px; }
        </style></head><body>
        <div class="rapor-konteyner">
            <div class="baslik-alan">
                <h1>T.C. DARGEÇİT KAYMAKAMLIĞI</h1>
                <h2>1. MATEMATİK OLİMPİYATI - İLÇE GENELİ DEĞERLENDİRME RAPORU</h2>
            </div>
        """
        
        rapor_html += f"""
            <div class="info-kutu">
                <span>Katılımcı Okul Sayısı: {df_genel['OKUL ADI'].nunique()}</span>
                <span>Sınava Giren Toplam Öğrenci: {len(df_genel)}</span>
                <span>İlçe Puan Ortalaması: {df_genel['Puan'].mean():.2f}</span>
            </div>
            
            <table class="rapor-tablo">
                <thead>
                    <tr>
                        <th style="width: 5%;">Sıra</th>
                        <th style="text-align: left; width: 35%;">Kurum Adı</th>
                        <th style="width: 15%;">Öğrenci Sayısı</th>
                        <th style="width: 15%;">Ort. Doğru</th>
                        <th style="width: 15%;">Ort. Net</th>
                        <th style="width: 15%;">Puan Ortalaması</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for sira, (idx, row) in enumerate(rapor_df.iterrows(), 1):
            rapor_html += f"""
                    <tr>
                        <td>{sira}</td>
                        <td style="text-align: left; font-weight: 800; color: #0f172a;">{row.name}</td>
                        <td>{int(row['Ogr_Sayisi'])}</td>
                        <td>{row['Ort_Dogru']:.1f}</td>
                        <td>{row['Ort_Net']:.2f}</td>
                        <td class="puan-hucre">{row['Ort_Puan']:.2f}</td>
                    </tr>
            """
            
        rapor_html += """
                </tbody>
            </table>
            
            <div class="alt-bilgi">
                Bu belge Dargeçit İlçe Milli Eğitim Müdürlüğü Sınav Analiz Sistemi tarafından otomatik olarak oluşturulmuştur.<br>
                Rapor, öğrencilerin aldığı puanların aritmetik ortalaması baz alınarak hazırlanmıştır.
            </div>
        </div>
        </body></html>
        """
        
        st.download_button("🖨️ Resmi Raporu İndir (Yazdırılabilir PDF/HTML)", data=rapor_html, file_name="Ilce_Geneli_Okul_Raporu.html", mime="text/html", type="primary", use_container_width=True)
