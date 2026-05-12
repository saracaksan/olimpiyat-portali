import streamlit as st
import pandas as pd
import io
import os
import glob
import ast
import plotly.express as px

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="1. Dargeçit Matematik Olimpiyatı Portalı", layout="wide", page_icon="🥇")

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
    
    .sidebar-title { color: var(--meb-red); font-weight: 900; font-size: 18px; margin-bottom: 10px; display: block; text-align: center; }
    
    .metric-card {
        background: white; border-radius: 10px; padding: 20px; text-align: center;
        border: 1px solid #e2e8f0; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .metric-card h2 { margin: 0; color: var(--navy); font-size: 36px; font-weight: 900; }
    .metric-card p { margin: 0; color: #64748b; font-size: 14px; font-weight: bold; text-transform: uppercase; }
    
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] { height: 50px; background: white; border-radius: 8px 8px 0 0; font-weight: bold; border: 1px solid #ddd; }
    .stTabs [aria-selected="true"] { background: var(--navy) !important; color: white !important; border-bottom: 4px solid var(--meb-red); }
    
    .stButton>button { background-color: var(--navy); color: white; border-radius: 8px; font-weight: bold; transition: 0.3s; width: 100%; }
    .stButton>button:hover { background-color: var(--meb-red); color: white; transform: translateY(-2px); }
    </style>
    """, unsafe_allow_html=True)

# --- DETAYLI PEDAGOJİK ANALİZ MOTORU ---
def profesyonel_analiz(row):
    p, d, y, b, ad = row['Puan'], row['Doğru'], row['Yanlış'], row['Boş'], row['Ad']
    if p >= 85:
        return f"Harika bir sınav çıkardın {ad}! Matematiksel muhakeme yeteneğinin olimpiyat standartlarında olduğunu bu sınavla kanıtladın. {d} doğru ve sadece {y} yanlış ile elde ettiğin bu sonuç, detaylara gösterdiğin dikkatin bir eseri. 2. Aşamada da bu analitik düşünme becerini en iyi şekilde kullanacağına inancımız tam."
    elif p >= 65:
        return f"Çok başarılı bir performans {ad}! Temel matematiksel kavramlara ve problem çözme mantığına hakimsin. Yaptığın {y} yanlış, bazı sorularda küçük işlem hataları veya dikkatsizlikler yaşadığını gösteriyor. Kalan sürede bu pratik eksiklerini kapatırsan zirveye yerleşmen an meselesi."
    elif p >= 40:
        return f"Önemli bir çaba ve gayret gösterdin {ad}. Temel matematik becerilerine sahipsin ancak mantık ağırlıklı sorularda daha fazla tecrübeye ihtiyacın var. {b} boş bıraktığın soru, bilmediğin konularda risk almaman açısından olumlu bir sınav stratejisi. Pratik yaparak netlerini çok daha yukarılara taşıyabilirsin."
    else:
        return f"Bu sınav senin için çok değerli bir tecrübe oldu {ad}. Puanın hedeflerinin altında kalmış olabilir ancak olimpiyat sınavları zorluk derecesi yüksek sınavlardır. {y} yanlışın, konu eksiklerin olduğunu ve soru çözümünde daha fazla dikkat etmen gerektiğini gösteriyor. Asla pes etme, her hata yeni bir öğrenme fırsatıdır!"

# --- BANNER ---
st.markdown("""
    <div class="header-box">
        <h1>🥇 1. DARGEÇİT MATEMATİK OLİMPİYATI</h1>
        <h3>Sınav Sonuç, Analiz ve Raporlama Merkezi</h3>
    </div>
""", unsafe_allow_html=True)

# --- VERİ YÜKLEME SİSTEMİ ---
@st.cache_data
def tum_verileri_yukle():
    dosyalar = glob.glob("sonuclar_*.xlsx")
    df_list = []
    for d in dosyalar:
        try:
            temp_df = pd.read_excel(d)
            if set(['OKUL ADI', 'Sınıf', 'Şube', 'Puan', 'Net']).issubset(temp_df.columns):
                df_list.append(temp_df)
        except: pass
    if df_list:
        return pd.concat(df_list, ignore_index=True)
    return None

df_genel = tum_verileri_yukle()

# --- YAN MENÜ: SINIF SEÇİMİ ---
with st.sidebar:
    st.markdown('<span class="sidebar-title">⬇️ SINIF KATEGORİSİ</span>', unsafe_allow_html=True)
    sinif_listesi = [f"{i}. Sınıf" for i in range(4, 13)]
    secilen_sinif_str = st.selectbox("İşlem yapılacak sınıf düzeyini seçin:", sinif_listesi, index=3)
    sinif_no = secilen_sinif_str.split(".")[0]
    aktif_dosya = f"sonuclar_{sinif_no}.xlsx"
    st.divider()
    st.info("⚠️ İdareci Raporları ve Karneler, burada seçtiğiniz sınıf baz alınarak oluşturulur.")

# İlgili sınıfın özel verisini ayırma
if df_genel is not None and not df_genel.empty:
    df_sinif = df_genel[df_genel['Sınıf'].astype(str) == str(sinif_no)].copy()
    if not df_sinif.empty:
        df_sinif['Arama_No'] = df_sinif['Öğrenci No'].astype(str).str.lstrip('0').str.split('.').str[0]
        df_sinif = df_sinif.sort_values(by=['Puan', 'Net'], ascending=[False, False]).reset_index(drop=True)
else:
    df_sinif = pd.DataFrame()

if df_sinif.empty:
    st.warning(f"⚠️ {secilen_sinif_str} kategorisine ait öğrenci verisi sistemde bulunamadı.")
else:
    ana_tab1, ana_tab2 = st.tabs(["👤 Öğrenci Bireysel Sonuç Görüntüleme", "🏫 Okul İdaresi ve Milli Eğitim Paneli"])

    # =========================================================
    # 1. ANA TAB: ÖĞRENCİ SORGULAMA
    # =========================================================
    with ana_tab1:
        st.markdown(f"### 🔍 {secilen_sinif_str} Sınav Sonucu Sorgulama")
        col_ogr1, col_ogr2 = st.columns(2)
        with col_ogr1: okul_secim = st.selectbox("Okulunuzu Seçin:", sorted(df_sinif['OKUL ADI'].unique()))
        with col_ogr2: no_secim = st.text_input("Öğrenci Numaranız (Baştaki sıfırları girmeyebilirsiniz):").lstrip('0')

        if st.button("Karnemi Göster", type="primary"):
            sonuc = df_sinif[(df_sinif['OKUL ADI'] == okul_secim) & (df_sinif['Arama_No'] == no_secim)]
            if not sonuc.empty:
                st.balloons()
                o = sonuc.iloc[0]
                analiz_metni = profesyonel_analiz(o)
                st.markdown(f"""
                <div style="background:white; padding:35px; border-radius:15px; border-top:8px solid var(--meb-red); box-shadow:0 10px 30px rgba(0,0,0,0.1);">
                    <h2 style="color:var(--navy); margin:0; font-size: 28px;">{o['Ad']} {o['Soyad']}</h2>
                    <p style="color:#555; font-size:18px; margin-bottom:15px;"><b>{o['OKUL ADI']}</b> - Sınıf: {o['Sınıf']}/{o['Şube']} | No: <b>{o['Öğrenci No']}</b></p>
                    <div style="display:flex; gap:10px; margin-bottom:25px;">
                        <span style="background:var(--navy); color:white; padding:8px 15px; border-radius:5px; font-weight:bold;">İlçe Sıralaması: {o['İlçe Sırası']}</span>
                        <span style="background:var(--meb-red); color:white; padding:8px 15px; border-radius:5px; font-weight:bold;">Okul Sıralaması: {o['Okul Sırası']}</span>
                    </div>
                    <div style="display:grid; grid-template-columns: repeat(5, 1fr); gap:15px; text-align:center;">
                        <div style="background:#f1f5f9; padding:15px; border-radius:10px; border:1px solid #e2e8f0;"><span>Doğru</span><br><b style="font-size:26px; color:#059669;">{o['Doğru']}</b></div>
                        <div style="background:#fef2f2; padding:15px; border-radius:10px; border:1px solid #fca5a5;"><span>Yanlış</span><br><b style="font-size:26px; color:var(--meb-red);">{o['Yanlış']}</b></div>
                        <div style="background:#f1f5f9; padding:15px; border-radius:10px; border:1px solid #e2e8f0;"><span>Boş</span><br><b style="font-size:26px; color:#64748b;">{o['Boş']}</b></div>
                        <div style="background:#eff6ff; padding:15px; border-radius:10px; border:1px solid #bfdbfe;"><span>Net</span><br><b style="font-size:26px; color:#2563eb;">{o['Net']}</b></div>
                        <div style="background:var(--navy); padding:15px; border-radius:10px; color:white;"><span>Puan</span><br><b style="font-size:30px; font-weight:900;">{o['Puan']}</b></div>
                    </div>
                    <div style="margin-top:25px; padding:20px; background:#fff5f5; border-left:6px solid var(--meb-red); border-radius:8px;">
                        <p style="margin:0; font-size: 16px; line-height: 1.6; color:var(--navy);"><b>🎓 Detaylı Öğrenci Analizi:</b><br>{analiz_metni}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("❌ Sistemde bu bilgilere ait kayıt bulunamadı. Lütfen kontrol ediniz.")

    # =========================================================
    # 2. ANA TAB: İDARECİ VE RAPORLAMA PANELİ
    # =========================================================
    with ana_tab2:
        st.markdown(f"### 🏫 Kurumsal Veri, Analiz ve Çıktı Merkezi")
        sifre = st.text_input("Giriş Şifresi:", type="password")
        
        if sifre == "darder47":
            st.success("Yetki Onaylandı. Lütfen işlem yapmak istediğiniz sekmeyi seçin.")
            
            sub_tab1, sub_tab2, sub_tab3, sub_tab4 = st.tabs([
                "🏆 İLÇE GENEL RAPORLARI", 
                "📉 ŞUBE / ÖĞRETMEN ANALİZİ", 
                "📑 OKUL KAPI LİSTESİ & KARNELER", 
                "🎟️ SINAV GİRİŞ BELGELERİ"
            ])

            # --- SUB TAB 1: İLÇE GENEL RAPORLARI ---
            with sub_tab1:
                st.subheader("🏢 İlçe Geneli Okul Başarı Sıralaması (Tüm Sınıflar)")
                
                # Üst İstatistikler
                c1, c2, c3, c4 = st.columns(4)
                with c1: st.markdown(f"<div class='metric-card'><p>Sınava Giren Öğrenci</p><h2>{len(df_genel)}</h2></div>", unsafe_allow_html=True)
                with c2: st.markdown(f"<div class='metric-card'><p>Katılımcı Okul Sayısı</p><h2>{df_genel['OKUL ADI'].nunique()}</h2></div>", unsafe_allow_html=True)
                with c3: st.markdown(f"<div class='metric-card'><p>İlçe Puan Ortalaması</p><h2 style='color:#059669;'>{df_genel['Puan'].mean():.2f}</h2></div>", unsafe_allow_html=True)
                with c4: st.markdown(f"<div class='metric-card'><p>İlçe Net Ortalaması</p><h2 style='color:#2563eb;'>{df_genel['Net'].mean():.2f}</h2></div>", unsafe_allow_html=True)
                
                # Okul Sıralama Tablosu
                df_okul = df_genel.groupby('OKUL ADI').agg(
                    Ogr_Sayisi=('Puan', 'count'),
                    Ort_Dogru=('Doğru', 'mean'),
                    Ort_Yanlis=('Yanlış', 'mean'),
                    Ort_Net=('Net', 'mean'),
                    Ort_Puan=('Puan', 'mean')
                ).reset_index().sort_values(by='Ort_Puan', ascending=False)
                
                # Grafik
                df_okul_grafik = df_okul.sort_values(by='Ort_Puan', ascending=True)
                fig = px.bar(df_okul_grafik, x='Ort_Puan', y='OKUL ADI', orientation='h', 
                             text=df_okul_grafik['Ort_Puan'].apply(lambda x: f"{x:.2f}"),
                             color='Ort_Puan', color_continuous_scale='Reds',
                             title="İlçe Geneli Okul Başarı Sıralaması")
                fig.update_layout(height=600, showlegend=False, xaxis_title="Puan Ortalaması", yaxis_title="")
                st.plotly_chart(fig, use_container_width=True)

                # PDF Rapor İndirme (Kaymayan Kurumsal Rapor)
                rapor_html = """
                <html><head><meta charset="utf-8"><style>
                    @page { size: A4 portrait; margin: 15mm; }
                    * { box-sizing: border-box; -webkit-print-color-adjust: exact !important; }
                    body { font-family: 'Segoe UI', Arial, sans-serif; background: white; margin: 0; color: #111827; }
                    .baslik { text-align: center; border-bottom: 5px solid #111827; padding-bottom: 10px; margin-bottom: 20px; }
                    .baslik h1 { margin: 0; font-size: 22px; font-weight: 900; text-transform: uppercase; }
                    .baslik h2 { margin: 5px 0 0 0; color: #E30A17; font-size: 15px; }
                    .info { display: flex; justify-content: space-between; background: #f8fafc; padding: 12px; border-radius: 8px; border: 1px solid #e2e8f0; margin-bottom: 20px; font-weight: bold; font-size: 13px; }
                    .r-tablo { width: 100%; border-collapse: collapse; text-align: center; font-size: 12px; page-break-inside: auto; }
                    .r-tablo tr { page-break-inside: avoid; page-break-after: auto; }
                    .r-tablo th { background-color: #111827; color: white; padding: 10px; font-weight: bold; border: 1px solid #111827; }
                    .r-tablo td { padding: 8px; border: 1px solid #cbd5e1; font-weight: 600; color: #334155; }
                    .r-tablo tr:nth-child(even) { background-color: #f8fafc; }
                    .puan-cell { background-color: #fef2f2 !important; color: #E30A17 !important; font-size: 14px; font-weight: 900 !important; }
                </style></head><body>
                <div class="baslik">
                    <h1>T.C. DARGEÇİT KAYMAKAMLIĞI</h1>
                    <h2>1. MATEMATİK OLİMPİYATI - İLÇE GENELİ OKUL DEĞERLENDİRME RAPORU</h2>
                </div>
                """
                rapor_html += f"""
                <div class="info">
                    <span>Katılımcı Okul: {df_genel['OKUL ADI'].nunique()}</span>
                    <span>Toplam Öğrenci: {len(df_genel)}</span>
                    <span>İlçe Puan Ortalaması: {df_genel['Puan'].mean():.2f}</span>
                </div>
                <table class="r-tablo">
                    <thead><tr><th style="width: 5%;">Sıra</th><th style="text-align: left; width: 35%;">Kurum Adı</th><th>Öğrenci Sayısı</th><th>Ort. Doğru</th><th>Ort. Net</th><th>Puan Ortalaması</th></tr></thead><tbody>
                """
                for sira, (idx, row) in enumerate(df_okul.iterrows(), 1):
                    rapor_html += f"<tr><td>{sira}</td><td style='text-align:left; color:#0f172a;'>{row.name}</td><td>{int(row['Ogr_Sayisi'])}</td><td>{row['Ort_Dogru']:.1f}</td><td>{row['Ort_Net']:.2f}</td><td class='puan-cell'>{row['Ort_Puan']:.2f}</td></tr>"
                rapor_html += "</tbody></table></body></html>"
                
                st.download_button("🖨️ Resmi Raporu İndir (İlçe Geneli PDF)", data=rapor_html, file_name="Ilce_Okul_Raporu.html", mime="text/html")

            # --- SUB TAB 2: ŞUBE / ÖĞRETMEN ANALİZİ ---
            with sub_tab2:
                st.subheader(f"📉 {secilen_sinif_str} Şube ve Öğretmen Rekabet Analizi")
                st.info("Bu bölüm, okulların kendi içindeki veya diğer okullardaki şubeleri (öğretmen başarılarını) kıyaslamanızı sağlar.")
                
                c_an1, c_an2 = st.columns(2)
                with c_an1:
                    st.markdown(f"**{secilen_sinif_str} Okul Sıralaması**")
                    df_kad_okul = df_sinif.groupby('OKUL ADI')['Puan'].mean().reset_index().sort_values(by='Puan', ascending=True)
                    fig2 = px.bar(df_kad_okul, x='Puan', y='OKUL ADI', orientation='h', text=df_kad_okul['Puan'].apply(lambda x: f"{x:.2f}"), color='Puan', color_continuous_scale='Blues')
                    fig2.update_layout(xaxis_title="Ortalama Puan", yaxis_title="")
                    st.plotly_chart(fig2, use_container_width=True)
                    
                with c_an2:
                    st.markdown(f"**{secilen_sinif_str} En Başarılı Şubeler (Öğretmenler)**")
                    df_sube = df_sinif.groupby(['OKUL ADI', 'Şube']).agg(Ogrenci=('Puan', 'count'), Puan_Ort=('Puan', 'mean')).reset_index()
                    df_sube = df_sube[df_sube['Ogrenci'] >= 3].sort_values(by='Puan_Ort', ascending=True).tail(15) # En iyi 15
                    df_sube['Okul_Sube'] = df_sube['OKUL ADI'] + " - " + df_sube['Şube']
                    
                    fig3 = px.bar(df_sube, x='Puan_Ort', y='Okul_Sube', orientation='h', text=df_sube['Puan_Ort'].apply(lambda x: f"{x:.2f}"), color='Puan_Ort', color_continuous_scale='Teal')
                    fig3.update_layout(xaxis_title="Ortalama Puan", yaxis_title="")
                    st.plotly_chart(fig3, use_container_width=True)

            # --- SUB TAB 3: OKUL KAPI LİSTESİ & KUSURSUZ KARNELER ---
            with sub_tab3:
                st.subheader(f"📑 {secilen_sinif_str} Toplu Karne ve Liste Çıktıları")
                kurum_secimi = st.selectbox("İşlem Yapılacak Okul:", ["Tüm İlçe"] + sorted(df_sinif['OKUL ADI'].unique()), key="k_secim")
                df_filtre = df_sinif if kurum_secimi == "Tüm İlçe" else df_sinif[df_sinif['OKUL ADI'] == kurum_secimi]
                
                st.dataframe(df_filtre[['İlçe Sırası', 'Okul Sırası', 'OKUL ADI', 'Sınıf', 'Şube', 'Öğrenci No', 'Ad', 'Soyad', 'Net', 'Puan']], use_container_width=True)
                
                c_k1, c_k2 = st.columns(2)
                
                # Excel
                buf_ex = io.BytesIO()
                with pd.ExcelWriter(buf_ex, engine='openpyxl') as writer:
                    df_filtre.to_excel(writer, index=False)
                c_k1.download_button("📊 Excel Listeyi İndir", data=buf_ex.getvalue(), file_name=f"{kurum_secimi}_Listesi.xlsx", use_container_width=True)

                # A4'e 4 Adet Sığan, Üst Üste Binmeyen Kusursuz Karneler (CSS Grid)
                html_karne = """
                <html><head><meta charset="utf-8"><style>
                    @page { size: A4 portrait; margin: 10mm; }
                    * { box-sizing: border-box; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
                    body { font-family: 'Segoe UI', Arial, sans-serif; background: white; margin: 0; padding: 0; color: #111827; }
                    
                    /* Mükemmel Grid Sistemi - A4'e tam 4 karne, asla taşmaz */
                    .page { 
                        width: 190mm; height: 277mm; 
                        display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; gap: 8mm; 
                        page-break-after: always; 
                    }
                    .karne { 
                        border: 2px solid #111827; border-radius: 12px; padding: 12px; 
                        display: flex; flex-direction: column; justify-content: space-between;
                        background: white; overflow: hidden;
                    }
                    .baslik { color: #E30A17; text-align: center; font-weight: 900; font-size: 13px; border-bottom: 2px solid #eee; padding-bottom: 4px; text-transform: uppercase; }
                    .kimlik-satir { display: flex; justify-content: space-between; font-weight: 800; font-size: 11px; margin-top: 4px; }
                    .sira-kutu { text-align: center; background: #111827; color: white; padding: 4px; border-radius: 6px; font-size: 10px; font-weight: bold; margin-top: 4px; }
                    
                    .stats-tablo { width: 100%; border-collapse: collapse; text-align: center; font-size: 12px; margin-top: 4px; }
                    .stats-tablo th { background: #f8fafc; border: 1px solid #ccc; padding: 4px; }
                    .stats-tablo td { border: 1px solid #ccc; padding: 4px; font-weight: 900; }
                    
                    .optik-tablo { width: 100%; border-collapse: collapse; text-align: center; font-size: 9px; margin-top: 4px; table-layout: fixed; }
                    .optik-tablo th, .optik-tablo td { border: 1px solid #bbb; height: 16px; overflow: hidden; }
                    .dogru { background: #dcfce7 !important; color: #059669 !important; font-weight: 900; }
                    .yanlis { background: #fee2e2 !important; color: #E30A17 !important; font-weight: 900; }
                    
                    .analiz-kutu { 
                        background: #fff5f5 !important; border-left: 4px solid #E30A17; padding: 6px; 
                        font-size: 8.5px; line-height: 1.3; font-style: italic; font-weight: 600; text-align: justify;
                    }
                </style></head><body>
                """
                for i, row in df_filtre.reset_index().iterrows():
                    if i % 4 == 0: html_karne += "<div class='page'>"
                    
                    try:
                        ogr_cvp = ast.literal_eval(row['Ogrenci_Cevap_Listesi'])
                        key_cvp = ast.literal_eval(row['Cevap_Anahtari_Listesi'])
                    except: ogr_cvp = ["-"]*20; key_cvp = ["-"]*20
                    
                    optik_icerik = ""
                    for j in range(20):
                        c, k = (ogr_cvp[j] if j < len(ogr_cvp) else "-"), (key_cvp[j] if j < len(key_cvp) else "-")
                        if c == k and c != "-": optik_icerik += f"<td class='dogru'>{c}</td>"
                        elif c != k and c != "-": optik_icerik += f"<td class='yanlis'>{c}</td>"
                        else: optik_icerik += f"<td>-</td>"

                    html_karne += f"""
                    <div class="karne">
                        <div>
                            <div class="baslik">1. DARGEÇİT MATEMATİK OLİMPİYATI</div>
                            <div class="kimlik-satir"><span style="font-size: 13px;">{row['Ad']} {row['Soyad']}</span><span style="color:#E30A17;">Öğr. No: {row['Öğrenci No']}</span></div>
                            <div class="kimlik-satir" style="color:#555;"><span>{row['OKUL ADI']}</span><span>Sınıf: {row['Sınıf']}/{row['Şube']}</span></div>
                            <div class="sira-kutu">İlçe Sırası: {row['İlçe Sırası']} &nbsp;|&nbsp; Okul Sırası: {row['Okul Sırası']}</div>
                            
                            <table class="stats-tablo">
                                <tr><th>Doğru</th><th>Yanlış</th><th>Boş</th><th>Net</th><th>Puan</th></tr>
                                <tr><td style="color:#059669;">{row['Doğru']}</td><td style="color:#E30A17;">{row['Yanlış']}</td><td>{row['Boş']}</td><td style="color:#2563eb;">{row['Net']}</td><td style="background:#fef08a !important; font-size: 15px;">{row['Puan']}</td></tr>
                            </table>
                            
                            <table class="optik-tablo">
                                <tr style="background:#f1f5f9;">{"".join([f"<th>{j+1}</th>" for j in range(20)])}</tr>
                                <tr>{optik_icerik}</tr>
                            </table>
                        </div>
                        <div class="analiz-kutu"><b>Pedagojik Analiz:</b> {profesyonel_analiz(row)}</div>
                    </div>
                    """
                    if (i + 1) % 4 == 0 or i == len(df_filtre) - 1: html_karne += "</div>"
                
                html_karne += "</body></html>"
                c_k2.download_button("📑 Karneleri İndir (PDF - A4'e 4 Adet Kusursuz Sığar)", data=html_karne, file_name=f"{kurum_secimi}_Karneler.html", mime="text/html", use_container_width=True)

            # --- SUB TAB 4: SINAV GİRİŞ BELGELERİ ---
            with sub_tab4:
                st.subheader(f"🎟️ {secilen_sinif_str} Sınav Giriş Belgeleri (2. Aşama İçin)")
                baraj_puan = st.number_input("Finale Kalma Baraj Puanı:", value=75, key="b_puan")
                belge_df = df_sinif[df_sinif['Puan'] >= baraj_puan]
                
                if belge_df.empty:
                    st.warning("Bu sınıfta barajı geçen öğrenci bulunamadı.")
                else:
                    kurum_b = st.selectbox("Belgesi Çıkarılacak Okul:", ["Tüm İlçe"] + sorted(belge_df['OKUL ADI'].unique()), key="k_belge")
                    belge_filtre = belge_df if kurum_b == "Tüm İlçe" else belge_df[belge_df['OKUL ADI'] == kurum_b]
                    
                    html_belge = """
                    <html><head><meta charset="utf-8"><style>
                        @page { size: A4 portrait; margin: 10mm; }
                        * { box-sizing: border-box; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
                        body { font-family: 'Segoe UI', Tahoma, sans-serif; background: white; margin: 0; padding: 0; color: #111827; }
                        
                        /* A4'e 2 Adet, Taşıma ve Boşluk Yapmayan Grid */
                        .page { width: 190mm; height: 277mm; display: grid; grid-template-columns: 1fr; grid-template-rows: 1fr 1fr; gap: 10mm; page-break-after: always; }
                        
                        .belge { 
                            border: 3px solid #111827; border-radius: 15px; padding: 25px; 
                            background-color: white; background-image: radial-gradient(#f3f4f6 1px, transparent 1px); background-size: 20px 20px;
                            display: flex; flex-direction: column; justify-content: space-between;
                        }
                        .b-header { text-align: center; border-bottom: 5px solid #E30A17; padding-bottom: 12px; }
                        .b-header h2 { margin: 0; font-size: 20px; font-weight: 900; letter-spacing: 0.5px; }
                        .b-header h3 { margin: 5px 0 0 0; color: #E30A17; font-size: 15px; font-weight: 800; }
                        
                        .b-tablo { width: 100%; border-collapse: collapse; font-size: 14px; margin-top: 15px; background: white; }
                        .b-tablo td { padding: 10px; border: 2px solid #111827; }
                        .b-tablo .lbl { background: #f8fafc; font-weight: bold; width: 22%; color: #475569; }
                        .b-tablo .val { font-weight: 900; font-size: 15px; }
                        
                        .vurgu-alan { display: flex; justify-content: space-between; gap: 15px; margin-top: 15px; }
                        .kutu-lacivert { flex: 1; background: #111827; color: white; padding: 12px; border-radius: 8px; text-align: center; }
                        .kutu-kirmizi { flex: 1; background: #E30A17; color: white; padding: 12px; border-radius: 8px; text-align: center; }
                        .kutu-ust { font-size: 11px; text-transform: uppercase; display: block; margin-bottom: 4px; color: #e2e8f0; }
                        .kutu-alt { font-size: 18px; font-weight: 900; }
                        
                        .kurallar { border: 2px dashed #E30A17; background: white; padding: 15px; border-radius: 10px; margin-top: 15px; }
                        .kurallar h4 { margin: 0 0 8px 0; color: #E30A17; font-size: 14px; text-align: center; border-bottom: 1px solid #fee2e2; padding-bottom: 5px; }
                        .kurallar ul { margin: 0; padding-left: 20px; font-size: 11.5px; line-height: 1.5; font-weight: 600; color: #1e293b; }
                    </style></head><body>
                    """
                    for i, row in belge_filtre.reset_index().iterrows():
                        if i % 2 == 0: html_belge += "<div class='page'>"
                        html_belge += f"""
                        <div class="belge">
                            <div class="b-header">
                                <h2>T.C. DARGEÇİT KAYMAKAMLIĞI</h2>
                                <h2>1. MATEMATİK OLİMPİYATI</h2>
                                <h3>2. AŞAMA (FİNAL) SINAVA GİRİŞ BELGESİ</h3>
                            </div>
                            <table class="b-tablo">
                                <tr><td class="lbl">Adı Soyadı</td><td class="val">{row['Ad']} {row['Soyad']}</td><td class="lbl">Öğrenci No</td><td class="val" style="color:#E30A17;">{row['Öğrenci No']}</td></tr>
                                <tr><td class="lbl">Okulu</td><td class="val" colspan="3">{row['OKUL ADI']}</td></tr>
                                <tr><td class="lbl">Sınıfı / Şubesi</td><td class="val" colspan="3">{row['Sınıf']} / {row['Şube']}</td></tr>
                            </table>
                            <div class="vurgu-alan">
                                <div class="kutu-lacivert">
                                    <span class="kutu-ust">Sınav Yeri ve Tarihi</span>
                                    <span class="kutu-alt">Dargeçit Anadolu Lisesi</span><br>
                                    <span style="font-size: 14px; margin-top:5px; display:block;">18 Mayıs 2026 - 10:00</span>
                                </div>
                                <div class="kutu-kirmizi">
                                    <span class="kutu-ust">Sınav Salonu ve Sıra No</span>
                                    <span class="kutu-alt" style="font-size: 22px;">{row.get('Salon Adı', 'MERKEZ')}</span><br>
                                    <span style="font-size: 16px; display:block; margin-top:5px;">SIRA NO: {row.get('Sıra No', '1')}</span>
                                </div>
                            </div>
                            <div class="kurallar">
                                <h4>ÖĞRENCİNİN SINAVDA UYMASI GEREKEN RESMİ KURALLAR</h4>
                                <ul>
                                    <li>Adaylar sınava gelirken bu belgeyi ve <b>Geçerli Bir Kimlik Belgesini (Nüfus Cüzdanı)</b> mutlaka yanında bulundurmalıdır. Kimliği olmayan adaylar kesinlikle sınava alınmayacaktır.</li>
                                    <li>Sınav <b>klasik (açık uçlu)</b> formatta olacaktır. Tüm çözüm adımları detaylı olarak sınav kitapçığına yazılacaktır.</li>
                                    <li>Öğrenciler kendi kurşun kalem, silgi ve kalemtıraşlarını getirmekle yükümlüdür. Sınav esnasında öğrenciler arası <b>silgi vb. kırtasiye alışverişi kesinlikle yasaktır.</b></li>
                                    <li>Sınav süresince kopya çekmeye teşebbüs etmek, sağa sola bakmak veya konuşmak sınavın anında iptal sebebidir.</li>
                                    <li>Adaylar sınav saatinden <b>en az 30 dakika önce</b> sınav salonunda hazır bulunmalıdır. İlk 30 dakika dolmadan sınav salonundan çıkılamaz.</li>
                                </ul>
                            </div>
                        </div>
                        """
                        if (i + 1) % 2 == 0 or i == len(belge_filtre) - 1: html_belge += "</div>"
                    
                    html_belge += "</body></html>"
                    st.download_button("🎟️ Sınav Giriş Belgelerini Al (A4'e 2 Adet)", data=html_belge, file_name=f"{kurum_b}_Giris_Belgeleri.html", mime="text/html", type="primary")
        elif sifre != "":
            st.error("Hatalı Şifre!")
