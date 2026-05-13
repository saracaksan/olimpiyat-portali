import streamlit as st
import pandas as pd
import io
import ast
import os
import plotly.express as px

# --- SAYFA AYARLARI (Mobil Uyumluluk İçin Layout Wide) ---
st.set_page_config(page_title="1. Dargeçit Matematik Olimpiyatı", layout="wide", page_icon="🥇")

# --- GELİŞMİŞ MOBİL VE MODERN UI CSS ---
st.markdown("""
    <style>
    :root {
        --meb-red: #E30A17;
        --navy: #111827;
        --bg-gray: #f8fafc;
    }
    
    /* Genel Arkaplan ve Yazı Tipi */
    .main { background-color: var(--bg-gray); }
    body { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }

    /* Mobil Uyumlu Header Banner */
    .header-banner {
        background: linear-gradient(135deg, #ffffff 0%, #fef2f2 100%);
        padding: 25px 15px; border-bottom: 6px solid var(--meb-red);
        border-radius: 12px; margin-bottom: 25px; text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    .header-banner h1 { color: var(--navy); font-weight: 900; font-size: clamp(24px, 5vw, 36px); margin: 0; }
    .header-banner h3 { color: var(--meb-red); font-weight: 700; font-size: clamp(14px, 3vw, 18px); margin-top: 5px; }

    /* Mobil Uyumlu Kartlar */
    .result-card {
        background: white; padding: 20px; border-radius: 15px;
        border-top: 6px solid var(--meb-red);
        box-shadow: 0 10px 25px rgba(0,0,0,0.08); margin-bottom: 20px;
    }
    
    /* Mobil Izgara Yapısı (Flexbox) */
    .metric-container {
        display: flex; flex-wrap: wrap; gap: 10px; margin: 20px 0;
    }
    .metric-box {
        flex: 1 1 calc(50% - 10px); /* Mobilde yan yana 2 kutu */
        background: #fdfdfd; padding: 15px; border-radius: 10px;
        text-align: center; border: 1px solid #e2e8f0;
    }
    @media (min-width: 768px) {
        .metric-box { flex: 1; } /* Tablet ve PC'de yan yana dizil */
    }
    .metric-box span { display: block; font-size: 11px; font-weight: 800; color: #64748b; text-transform: uppercase; }
    .metric-box b { font-size: 22px; color: var(--navy); }

    /* Optik Tablo Tasarımı */
    .optik-wrapper { overflow-x: auto; margin: 15px 0; } /* Mobilde kaydırılabilir tablo */
    .optik-table { width: 100%; border-collapse: collapse; text-align: center; font-size: 12px; }
    .optik-table th { background: #f1f5f9; padding: 6px; border: 1px solid #cbd5e1; }
    .optik-table td { padding: 8px; border: 1px solid #cbd5e1; font-weight: bold; }
    .dogru { background-color: #dcfce7 !important; color: #166534 !important; }
    .yanlis { background-color: #111827 !important; color: white !important; }
    
    /* Butonlar */
    .stButton>button {
        width: 100%; border-radius: 8px; font-weight: 700; height: 3.5em;
        background: var(--navy); color: white; transition: 0.3s;
    }
    .stButton>button:hover { background: var(--meb-red); border-color: var(--meb-red); }

    /* Input Alanları Mobilde Tam Genişlik */
    .stSelectbox, .stTextInput { width: 100% !important; }
    </style>
""", unsafe_allow_html=True)

# --- ANALİZ MOTORU: ÖĞRENCİ (DOKUNULMADI - GELİŞTİRİLDİ) ---
def detayli_pedagojik_analiz(row):
    p, d, y, b, ad = row['Puan'], row['Doğru'], row['Yanlış'], row['Boş'], row['Ad']
    giris = f"Sevgili <b>{ad}</b>,<br><br>"
    vizyon = ("Matematik sadece rakamlar değildir; hayatı analiz etme sanatıdır. "
              "Bu olimpiyat sınavı, senin analitik düşünme maratonundaki en değerli adımlarından biridir.<br><br>")
    if p >= 85:
        durum = f"<b>{p} puan</b> ile zirvedesin! Matematiksel muhakeme gücün olimpiyat düzeyinde. Bu potansiyelle geleceğin bilim dünyasında parlayabilirsin."
    elif p >= 65:
        durum = f"<b>{p} puan</b> ile harika bir başarı gösterdin. Temelin çok sağlam. Küçük dikkatsizlikleri elersen şampiyonluk kaçınılmaz."
    elif p >= 40:
        durum = f"<b>{p} puan</b> aldın. Olimpiyat soruları zordur ancak sen bu zorluğa direnç gösterdin. Bol soru çözümü ile netlerini hızla artırabilirsin."
    else:
        durum = f"<b>{p} puan</b> aldın. Sakın pes etme! Bu sınav senin gelişim alanlarını gösteren bir pusuladır. Yanlışlarından ders alarak matematikte devleşebilirsin."
    return giris + vizyon + durum + "<br><br><b>Başarılar dileriz!</b>"

# --- ANALİZ MOTORU: İDARE (TENKİT EDİCİ) ---
def idari_rapor_ozeti(okul_adi, okul_ort, ilce_ort, df_subeler):
    fark = okul_ort - ilce_ort
    if fark > 5:
        return f"Kurumunuz <b>{okul_ort:.2f}</b> ortalama ile ilçe ortalamasının üzerinde, gıpta edilecek bir başarı sergilemektedir."
    elif fark >= -2:
        return f"Kurumunuz <b>{okul_ort:.2f}</b> ortalama ile ilçe geneliyle paralel bir çizgidedir. Gelişim için zümre çalışmalarına ağırlık verilmelidir."
    else:
        return f"Kurumunuz <b>{okul_ort:.2f}</b> ortalama ile ilçe ortalamasının gerisindedir. Akademik takip ve ek etüt çalışmaları acilen planlanmalıdır."

# --- VERİ YÜKLEME (TÜM CSV'LERİ OKUYAN YAPI) ---
@st.cache_data
def verileri_yukle():
    mevcut_dosyalar = os.listdir('.')
    liste = []
    for d in mevcut_dosyalar:
        # İsmi ne olursa olsun içinde "sonuc" geçen ve .csv olanları yakala
        if "sonuc" in d.lower() and d.endswith(".csv"):
            try:
                df = pd.read_csv(d, sep=',', quotechar='"')
                if 'Puan' in df.columns:
                    # Temizlik
                    df['Arama_No'] = df['Öğrenci No'].astype(str).str.replace('.0', '', regex=False).str.strip().str.lstrip('0')
                    df['Sınıf'] = df['Sınıf'].astype(str).str.replace('.0', '', regex=False).str.strip()
                    liste.append(df)
            except: pass
    if liste:
        birlestirilmis = pd.concat(liste, ignore_index=True)
        return birlestirilmis.drop_duplicates(subset=['Öğrenci No', 'OKUL ADI', 'Sınıf'])
    return pd.DataFrame()

df_tum = verileri_yukle()
# --- YAN MENÜ (KADEME SEÇİMİ) ---
with st.sidebar:
    st.markdown('<h3 style="color:#E30A17; text-align:center;">📊 KADEME SEÇİMİ</h3>', unsafe_allow_html=True)
    sinif_listesi = [f"{i}. Sınıf" for i in range(4, 13)]
    secilen_kademe_str = st.selectbox("Lütfen Sınıf Düzeyini Seçiniz:", sinif_listesi, index=3) # 7. Sınıf varsayılan (index=3)
    kademe_no = secilen_kademe_str.split(".")[0]
    st.divider()
    st.info("💡 **Öğrenciler:** Sonucunuzu görmek için sınıfınızı ve okulunuzu seçip numaranızı giriniz.\n\n💡 **İdareciler:** Kurum röntgenleri ve toplu listeler için İdare sekmesine geçiniz.")

# Seçilen kademeye göre aktif veriyi belirle
if not df_tum.empty:
    df_tum['Sınıf'] = df_tum['Sınıf'].astype(str)
df_aktif = df_tum[df_tum['Sınıf'] == str(kademe_no)].copy() if not df_tum.empty else pd.DataFrame()

# --- ANA SEKMELER ---
tab_ogrenci, tab_idareci = st.tabs(["🎓 ÖĞRENCİ SONUÇ EKRANI", "🏛️ İDARE VE KURUM RÖNTGENİ"])

# ==============================================================================
# 2. BÖLÜM: ÖĞRENCİ GİRİŞİ, MOBİL UYUMLU ÖN İZLEME VE YENİ OPTİKLİ KARNE
# ==============================================================================
with tab_ogrenci:
    if df_aktif.empty:
        st.warning(f"Sistemde henüz {secilen_kademe_str} seviyesine ait sınav verisi bulunmamaktadır. Lütfen doğru sınıfı seçtiğinizden emin olun.")
    else:
        st.markdown("### 🔍 Bireysel Sonuç, Soru Analizi ve Pedagojik Karne")
        
        # Öğrenci Arama Paneli (Mobil Uyumlu)
        with st.container():
            c1, c2 = st.columns(2)
            with c1:
                okul_listesi = sorted(df_aktif['OKUL ADI'].dropna().unique())
                secilen_okul = st.selectbox("Okulunuzu Seçiniz:", okul_listesi)
            with c2:
                girilen_no = st.text_input("Öğrenci Numaranız:", placeholder="Örn: 145").strip().lstrip('0')
            
            search_btn = st.button("SONUÇLARI GETİR VE ANALİZ ET")

        if search_btn:
            if not girilen_no:
                st.error("Lütfen öğrenci numaranızı giriniz.")
            else:
                sonuc = df_aktif[(df_aktif['OKUL ADI'] == secilen_okul) & (df_aktif['Arama_No'] == girilen_no)]
                
                if not sonuc.empty:
                    st.balloons()
                    o = sonuc.iloc[0]
                    
                    # 1. Bölümdeki ortak analiz motorunu çağırıyoruz
                    analiz_html = detayli_pedagojik_analiz(o)
                    
                    # --- YENİ OPTİK FORM (CEVAP ANAHTARI VE ÖĞRENCİ ŞIKKI BİR ARADA) ---
                    try:
                        ogr_cvp = ast.literal_eval(str(o.get('Ogrenci_Cevap_Listesi', "['-']*20")))
                        key_cvp = ast.literal_eval(str(o.get('Cevap_Anahtari_Listesi', "['-']*20")))
                    except:
                        ogr_cvp = ["-"]*20
                        key_cvp = ["-"]*20

                    optik_th = "".join([f"<th>{j+1}</th>" for j in range(20)])
                    optik_key = "".join([f"<td>{key_cvp[j]}</td>" for j in range(20)])
                    optik_ogr = ""
                    for j in range(20):
                        c = ogr_cvp[j] if j < len(ogr_cvp) else "-"
                        k = key_cvp[j] if j < len(key_cvp) else "-"
                        if c == k and c != "-": optik_ogr += f"<td class='dogru'>{c}</td>"
                        elif c != k and c != "-": optik_ogr += f"<td class='yanlis'>{c}</td>"
                        else: optik_ogr += f"<td>{c}</td>"

                    # AŞAMA 1: TABLOLU ÖN İZLEME (Mobil Uyumlu DataFrame)
                    st.markdown("#### 📊 Öğrenci Sonuç Veri Tablosu")
                    gosterilecek_tablo = pd.DataFrame([o])[['Öğrenci No', 'Ad', 'Soyad', 'OKUL ADI', 'Sınıf', 'Şube', 'Doğru', 'Yanlış', 'Boş', 'Net', 'Puan', 'Okul Sırası', 'İlçe Sırası']]
                    st.dataframe(gosterilecek_tablo, use_container_width=True, hide_index=True)
                    
                    # AŞAMA 2: PROFESYONEL KARNE VE YENİ OPTİK KARTI (Mobil CSS ile)
                    st.markdown(f"""
                    <div class="result-card">
                        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:2px solid #e2e8f0; padding-bottom:15px; flex-wrap: wrap; gap: 10px;">
                            <div>
                                <h1 style="margin:0; color:#111827; font-size:clamp(20px, 4vw, 32px);">{o['Ad']} {o['Soyad']}</h1>
                                <p style="margin:0; color:#E30A17; font-weight:800; font-size:clamp(14px, 2.5vw, 18px);">{o['OKUL ADI']} - Sınıf: {o['Sınıf']}/{o['Şube']}</p>
                            </div>
                            <div style="background:#111827; color:white; padding:8px 15px; border-radius:8px; font-weight:bold; font-size:clamp(14px, 2.5vw, 18px);">
                                No: {o['Öğrenci No']}
                            </div>
                        </div>
                        
                        <div class="metric-container">
                            <div class="metric-box"><span>Doğru</span><b style="color:#059669;">{o['Doğru']}</b></div>
                            <div class="metric-box"><span>Yanlış</span><b style="color:#E30A17;">{o['Yanlış']}</b></div>
                            <div class="metric-box"><span>Boş</span><b style="color:#64748b;">{o['Boş']}</b></div>
                            <div class="metric-box"><span>Net</span><b style="color:#2563eb;">{o['Net']}</b></div>
                            <div class="metric-box" style="background:#111827; border-color:#111827;"><span style="color:#94a3b8;">PUAN</span><b style="color:white; font-size:clamp(22px, 4vw, 34px);">{o['Puan']}</b></div>
                        </div>

                        <h4 style="color:#111827; margin-bottom:5px; font-size: 16px;">📋 Soru Analizi (Cevap Anahtarı vs Öğrenci Cevabı)</h4>
                        <div class="optik-wrapper">
                            <table class="optik-table">
                                <tr><th style="text-align:left; background:#111827; color:white; padding:5px;">Soru No</th>{optik_th}</tr>
                                <tr><th style="text-align:left; background:#f1f5f9; padding:5px;">Cevap Anahtarı</th>{optik_key}</tr>
                                <tr><th style="text-align:left; background:#f1f5f9; padding:5px;">Öğrenci Cevabı</th>{optik_ogr}</tr>
                            </table>
                        </div>

                        <div style="background:#fff5f5; border-left:6px solid #E30A17; padding:20px; border-radius:10px; margin-top:20px;">
                            <h3 style="margin-top:0; color:#E30A17; font-size:18px;">🎓 Uzman Pedagojik Analiz ve Rehberlik</h3>
                            <p style="margin:0; font-size:clamp(14px, 2vw, 16px); line-height:1.6; color:#1e293b; text-align:justify;">{analiz_html}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # AŞAMA 3: İNDİRİLEBİLİR BİREYSEL RESMİ PDF BELGESİ
                    bireysel_pdf_html = f"""
                    <html><head><meta charset="utf-8"><style>
                        @page {{ size: A4 portrait; margin: 15mm; }}
                        body {{ font-family: 'Segoe UI', Tahoma, sans-serif; padding: 0; margin: 0; color: #111827; -webkit-print-color-adjust: exact !important; }}
                        .karne-container {{ border: 5px solid #111827; border-radius: 20px; padding: 30px; background: white; }}
                        .header {{ text-align: center; border-bottom: 4px solid #E30A17; padding-bottom: 15px; margin-bottom: 20px; }}
                        .header h1 {{ margin: 0; font-size: 24px; text-transform: uppercase; }}
                        .header h2 {{ margin: 8px 0 0 0; color: #E30A17; font-size: 18px; }}
                        .info-strip {{ display: flex; justify-content: space-between; font-size: 16px; font-weight: bold; margin-bottom: 20px; background: #f8fafc; padding: 15px; border-radius: 10px; border: 1px solid #e2e8f0; }}
                        .stats-table {{ width: 100%; border-collapse: collapse; text-align: center; margin-bottom: 20px; }}
                        .stats-table th {{ background: #111827; color: white; padding: 12px; font-size: 16px; border: 1px solid #111827; }}
                        .stats-table td {{ padding: 15px; font-size: 24px; font-weight: 900; border: 1px solid #cbd5e1; }}
                        .optik-table {{ width: 100%; border-collapse: collapse; text-align: center; margin-bottom: 20px; font-size: 12px; }}
                        .optik-table th {{ background: #fef2f2; border: 1px solid #fca5a5; padding: 6px; color: #E30A17; }}
                        .optik-table td {{ border: 1px solid #fca5a5; padding: 8px; font-weight: bold; font-size: 14px; }}
                        .optik-table .baslik-hucre {{ background: #111827; color: white; text-align: left; width: 100px; }}
                        .optik-table .alt-baslik-hucre {{ background: #f1f5f9; color: #111827; text-align: left; font-size: 11px; }}
                        .dogru {{ background-color: #dcfce7 !important; color: #059669 !important; }}
                        .yanlis {{ background-color: #111827 !important; color: white !important; }}
                        .analiz-box {{ background: #fef2f2; border-left: 8px solid #E30A17; padding: 20px; font-size: 14px; line-height: 1.5; text-align: justify; border-radius: 10px; }}
                    </style></head><body>
                        <div class="karne-container">
                            <div class="header">
                                <h1>1. DARGEÇİT MATEMATİK OLİMPİYATI</h1>
                                <h2>RESMİ SINAV SONUÇ BELGESİ</h2>
                            </div>
                            <div class="info-strip">
                                <span>{o['Ad']} {o['Soyad']}</span>
                                <span>{o['OKUL ADI']} - {o['Sınıf']}/{o['Şube']}</span>
                                <span style="color:#E30A17;">No: {o['Öğrenci No']} | İlçe S: {o.get('İlçe Sırası','-')} | Okul S: {o.get('Okul Sırası','-')}</span>
                            </div>
                            <table class="stats-table">
                                <tr><th>Doğru</th><th>Yanlış</th><th>Boş</th><th>Net</th><th style="background:#E30A17;">PUAN</th></tr>
                                <tr>
                                    <td style="color:#059669;">{o['Doğru']}</td>
                                    <td style="color:#E30A17;">{o['Yanlış']}</td>
                                    <td>{o['Boş']}</td>
                                    <td style="color:#2563eb;">{o['Net']}</td>
                                    <td>{o['Puan']}</td>
                                </tr>
                            </table>
                            <table class="optik-table">
                                <tr><th class="baslik-hucre">Soru No</th>{optik_th}</tr>
                                <tr><th class="alt-baslik-hucre">Cevap Anahtarı</th>{optik_key}</tr>
                                <tr><th class="alt-baslik-hucre">Öğrenci Cevabı</th>{optik_ogr}</tr>
                            </table>
                            <div class="analiz-box">
                                <h3 style="margin-top:0; color:#E30A17;">🎓 Uzman Pedagojik Değerlendirme</h3>
                                {analiz_html}
                            </div>
                        </div>
                    </body></html>
                    """
                    st.download_button(f"📥 {o['Ad']} {o['Soyad']} - Karnesini İndir (Yazdırılabilir PDF)", data=bireysel_pdf_html, file_name=f"{o['Ad']}_{o['Soyad']}_Olimpiyat_Karne.html", mime="text/html")
                else:
                    st.error("❌ Sistemde eşleşen kayıt bulunamadı. Lütfen 'Okul' ve 'Öğrenci No' bilgisini kontrol ediniz.")
                    # ==============================================================================
# 3. BÖLÜM: TOPLU SINAV SONUÇLARI, İDARİ RÖNTGEN VE ANALİZ MERKEZİ
# ==============================================================================
with tab_idareci:
    st.markdown("### 🔐 İlçe Milli Eğitim ve Kurum Yönetim Paneli")
    sifre = st.text_input("Yetkili Giriş Şifresi:", type="password")
    
    if sifre == "darder47":
        if df_tum.empty:
            st.error("Sistemde analiz edilecek sonuç verisi bulunamadı.")
        else:
            sub1, sub2, sub3, sub4 = st.tabs([
                "🏆 İLÇE GENEL BAŞARI", 
                "📈 KURUM DENETİM RÖNTGENİ", 
                "📉 ŞUBE / ÖĞRETMEN ANALİZİ", 
                "📑 TÜM KADEMELER TOPLU LİSTE/KARNE"
            ])

            # -----------------------------------------------------
            # ALT SEKME 1: İLÇE GENEL BAŞARI RAPORU (Aktif Kademe İçin)
            # -----------------------------------------------------
            with sub1:
                st.markdown(f"#### 🏢 {secilen_kademe_str} İlçe Geneli Toplu Sınav Sonuçları")
                
                if df_aktif.empty:
                    st.warning("Bu sınıf düzeyinde veri bulunmamaktadır.")
                else:
                    st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
                    c_m1, c_m2, c_m3, c_m4 = st.columns(4)
                    with c_m1: st.markdown(f"<div class='metric-box'><span>Toplam Öğrenci</span><b>{len(df_aktif)}</b></div>", unsafe_allow_html=True)
                    with c_m2: st.markdown(f"<div class='metric-box'><span>Kurum Sayısı</span><b>{df_aktif['OKUL ADI'].nunique()}</b></div>", unsafe_allow_html=True)
                    with c_m3: st.markdown(f"<div class='metric-box'><span>İlçe Puan Ort.</span><b>{df_aktif['Puan'].mean():.2f}</b></div>", unsafe_allow_html=True)
                    with c_m4: st.markdown(f"<div class='metric-box'><span>İlçe Net Ort.</span><b style='color:#E30A17;'>{df_aktif['Net'].mean():.2f}</b></div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    df_okul_genel = df_aktif.groupby('OKUL ADI').agg(Ogr_Sayisi=('Puan', 'count'), Ort_Puan=('Puan', 'mean')).reset_index()
                    
                    st.markdown("##### 📊 Kurumlar Arası Başarı Kıyaslaması", unsafe_allow_html=True)
                    fig = px.bar(df_okul_genel.sort_values(by='Ort_Puan', ascending=True), 
                                 x='Ort_Puan', y='OKUL ADI', orientation='h', text_auto='.2f', 
                                 color='Ort_Puan', color_continuous_scale='Reds')
                    fig.update_layout(height=400, margin=dict(l=0, r=0, t=30, b=0), xaxis_title="Puan Ortalaması", yaxis_title="")
                    st.plotly_chart(fig, use_container_width=True)

            # -----------------------------------------------------
            # ALT SEKME 2: KURUM DENETİM RÖNTGENİ (İDARECİ TENKİT RAPORU)
            # -----------------------------------------------------
            with sub2:
                st.markdown(f"#### 📈 {secilen_kademe_str} Kurum Denetim, Tenkit ve Gelişim Raporları")
                st.info("Bu bölümdeki raporlar, okulların eksikliklerini ve zümre performanslarını net bir dille idarecilere sunmak için tasarlanmıştır.")
                
                if df_aktif.empty:
                    st.warning("Veri bulunamadı.")
                else:
                    ilce_ort = df_aktif['Puan'].mean()
                    
                    # TEK BİR KURUM İÇİN ÖN İZLEME VE İNDİRME
                    secilen_kurum = st.selectbox("Ön İzleme Yapılacak Okulu Seçiniz:", sorted(df_aktif['OKUL ADI'].unique()), key="gelisim_okul")
                    
                    df_kurum_gelisim = df_aktif[df_aktif['OKUL ADI'] == secilen_kurum]
                    okul_ort = df_kurum_gelisim['Puan'].mean()
                    toplam_ogrenci = len(df_kurum_gelisim)
                    df_subeler = df_kurum_gelisim.groupby('Şube').agg(Mevcut=('Puan', 'count'), Sube_Ort_Puan=('Puan', 'mean')).reset_index().sort_values(by='Sube_Ort_Puan', ascending=False)
                    
                    # 1. Bölümdeki sert ve profesyonel analizi çekiyoruz
                    metin = idari_pedagojik_rapor(secilen_kurum, okul_ort, ilce_ort, toplam_ogrenci, df_subeler)
                    
                    fark = okul_ort - ilce_ort
                    durum_renk = "#059669" if fark >= 0 else "#E30A17"
                    
                    st.markdown(f"""
                    <div style="background:white; padding:20px; border-radius:12px; border-left:8px solid {durum_renk}; box-shadow:0 5px 15px rgba(0,0,0,0.05); overflow-x: auto;">
                        <h3 style="margin-top:0; font-size:18px;">{secilen_kurum} Denetim Raporu Ön İzlemesi</h3>
                        <p style="font-size:14px;">Okul Ortalaması: <b>{okul_ort:.2f}</b> | İlçe Ortalaması: <b>{ilce_ort:.2f}</b></p>
                        <hr>
                        <p style="text-align:justify; line-height:1.6; font-size:14px;">{metin}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # TÜM OKULLARIN RAPORUNU TEK BİR PDF'TE BİRLEŞTİRME MANTIĞI
                    if st.button("📑 TÜM OKULLARIN DENETİM RAPORLARINI TEK DOSYADA İNDİR (İlçe MEM Çıktısı)", type="primary"):
                        tum_okullar_html = """
                        <html><head><meta charset="utf-8"><style>
                            @page { size: A4 portrait; margin: 15mm; }
                            body { font-family: 'Segoe UI', Tahoma, sans-serif; margin: 0; padding: 0; color: #111827; -webkit-print-color-adjust: exact !important; }
                            .page { page-break-after: always; display: flex; flex-direction: column; min-height: 260mm; }
                            .baslik-alan { text-align: center; border-bottom: 5px solid #111827; padding-bottom: 15px; margin-bottom: 25px; }
                            .baslik-alan h1 { margin: 0; font-size: 22px; font-weight: 900; }
                            .baslik-alan h2 { margin: 5px 0 0 0; color: #E30A17; font-size: 16px; font-weight: bold; text-transform: uppercase; }
                            .bilgi-serit { display: flex; justify-content: space-between; background: #fef2f2; border: 1px solid #fca5a5; padding: 15px; border-radius: 8px; margin-bottom: 20px; font-weight: bold; font-size: 14px; }
                            .analiz-metni { font-size: 14px; line-height: 1.6; text-align: justify; margin-bottom: 30px; background: #f8fafc; padding: 25px; border-radius: 8px; border-left: 5px solid #111827; flex-grow: 1; }
                            .tablo-alan { width: 100%; border-collapse: collapse; text-align: center; margin-bottom: 20px; font-size: 14px; }
                            .tablo-alan th { background: #111827; color: white; padding: 10px; border: 1px solid #111827; }
                            .tablo-alan td { padding: 10px; border: 1px solid #cbd5e1; font-weight: bold; font-size: 15px; }
                            .imza-kismi { text-align: right; margin-top: 40px; font-weight: bold; font-size: 16px; }
                            .footer { font-size: 11px; color: #64748b; text-align: center; margin-top: auto; border-top: 1px solid #cbd5e1; padding-top: 10px; }
                        </style></head><body>
                        """
                        
                        okul_listesi_tum = sorted(df_aktif['OKUL ADI'].unique())
                        
                        for okul in okul_listesi_tum:
                            df_o = df_aktif[df_aktif['OKUL ADI'] == okul]
                            o_ort = df_o['Puan'].mean()
                            o_toplam = len(df_o)
                            df_s = df_o.groupby('Şube').agg(Mevcut=('Puan', 'count'), Sube_Ort_Puan=('Puan', 'mean')).reset_index().sort_values(by='Sube_Ort_Puan', ascending=False)
                            o_metin = idari_pedagojik_rapor(okul, o_ort, ilce_ort, o_toplam, df_s)
                            
                            tum_okullar_html += f"""
                            <div class="page">
                                <div class="baslik-alan">
                                    <h1>T.C. DARGEÇİT KAYMAKAMLIĞI</h1>
                                    <h2>1. MATEMATİK OLİMPİYATI KURUM DENETİM VE GELİŞİM RAPORU</h2>
                                </div>
                                <div class="bilgi-serit">
                                    <span>Kurum: {okul}</span>
                                    <span>Sınıf Düzeyi: {kademe_no}. Sınıflar</span>
                                    <span>İlçe Ortalaması: {ilce_ort:.2f}</span>
                                    <span style="color:#E30A17;">Okul Ortalaması: {o_ort:.2f}</span>
                                </div>
                                <div class="analiz-metni">
                                    {o_metin}
                                </div>
                                <div>
                                    <h4 style="margin:0 0 10px 0; color:#111827;">Zümre Şube Karnesi</h4>
                                    <table class="tablo-alan">
                                        <tr><th>Şube Adı</th><th>Sınava Giren Öğrenci</th><th>Şube Puan Ortalaması</th></tr>
                            """
                            for _, s_row in df_s.iterrows():
                                tum_okullar_html += f"<tr><td>{s_row['Şube']}</td><td>{s_row['Mevcut']}</td><td style='color:#E30A17;'>{s_row['Sube_Ort_Puan']:.2f}</td></tr>"
                            
                            tum_okullar_html += f"""
                                    </table>
                                </div>
                                <div class="imza-kismi">Dargeçit İlçe Milli Eğitim Müdürlüğü</div>
                                <div class="footer">Bu rapor Dargeçit İlçe Milli Eğitim Müdürlüğü Ölçme ve Değerlendirme Merkezi tarafından kurumsal gelişim amacıyla otomatik oluşturulmuştur.</div>
                            </div>
                            """
                        tum_okullar_html += "</body></html>"
                        
                        st.download_button("📥 İLÇE MEM - TÜM OKULLARIN RAPORUNU İNDİR", data=tum_okullar_html, file_name=f"Dargecit_Ilce_MEM_{kademe_no}_Siniflar_Kurum_Raporlari.html", mime="text/html")

            # -----------------------------------------------------
            # ALT SEKME 3: ŞUBE / ÖĞRETMEN ANALİZİ
            # -----------------------------------------------------
            with sub3:
                st.markdown(f"#### 📉 {secilen_kademe_str} Zümre ve Sınıf Başarı Grafikleri")
                if not df_aktif.empty:
                    df_sube_genel = df_aktif.groupby(['OKUL ADI', 'Şube']).agg(Ogr=('Puan', 'count'), Puan_Ort=('Puan', 'mean')).reset_index()
                    df_sube_genel = df_sube_genel[df_sube_genel['Ogr'] >= 3].sort_values(by='Puan_Ort', ascending=True).tail(15)
                    df_sube_genel['Sube_Ad'] = df_sube_genel['OKUL ADI'] + " - " + df_sube_genel['Şube']
                    
                    fig3 = px.bar(df_sube_genel, x='Puan_Ort', y='Sube_Ad', orientation='h', text_auto='.2f', color='Puan_Ort', color_continuous_scale='Teal', title="İlçenin En Başarılı Şubeleri")
                    fig3.update_layout(height=400, margin=dict(l=0, r=0, t=30, b=0))
                    st.plotly_chart(fig3, use_container_width=True)

            # -----------------------------------------------------
            # ALT SEKME 4: OKUL MÜDÜRLERİ İÇİN "TÜM KADEMELER" TOPLU LİSTE/KARNE
            # -----------------------------------------------------
            with sub4:
                st.markdown("#### 📑 Okul Bazlı TÜM KADEMELER (Toplu Liste ve Karneler)")
                st.success("👨‍💼 **Okul Müdürleri İçin Özel Alan:** Bu bölümden, seçtiğiniz okulun **TÜM SINIFLARINA (5, 6, 7, 8 vb.)** ait başarı listelerini ve Sayfada 2'li Optik Karneleri tek çırpıda alabilirsiniz.")
                
                # df_tum kullanılarak sistemdeki tüm okullar listelenir
                okul_listesi_genel = ["Tüm İlçe Listesi"] + sorted(df_tum['OKUL ADI'].dropna().unique().tolist())
                kurum_secim_tum = st.selectbox("Tüm Kademeleri İndirilecek Okulu Seçin:", okul_listesi_genel, key="toplu_karne_okul_tum")
                
                # Tüm sınıfları kapsayacak şekilde filtrele ve sırala
                if kurum_secim_tum == "Tüm İlçe Listesi":
                    df_filtre = df_tum.copy()
                else:
                    df_filtre = df_tum[df_tum['OKUL ADI'] == kurum_secim_tum].copy()
                
                # Karnelerin sırayla çıkması için Sınıf, Şube ve Puana göre sıralıyoruz
                df_filtre = df_filtre.sort_values(by=['Sınıf', 'Şube', 'Puan'], ascending=[True, True, False])
                
                st.markdown(f"**Veri Özeti:** Seçilen okulda sınava giren toplam {len(df_filtre)} öğrencinin verisi çekildi.")
                
                c_btn1, c_btn2 = st.columns(2)
                
                # 1. TÜM KADEMELER TOPLU LİSTE (PDF)
                pdf_liste_html = f"""
                <html><head><meta charset="utf-8"><style>
                    body {{ font-family: 'Segoe UI', Tahoma, sans-serif; }}
                    .h {{ text-align: center; border-bottom: 2px solid #111827; margin-bottom: 20px; padding-bottom: 10px; }}
                    table {{ width: 100%; border-collapse: collapse; text-align: center; font-size: 11px; }}
                    th {{ background: #111827; color: white; padding: 8px; border: 1px solid #111827; }}
                    td {{ border: 1px solid #ddd; padding: 6px; }}
                </style></head><body>
                    <div class="h">
                        <h2 style="margin:0;">T.C. DARGEÇİT KAYMAKAMLIĞI - 1. MATEMATİK OLİMPİYATI</h2>
                        <h3 style="margin:5px 0 0 0; color:#E30A17;">{kurum_secim_tum} - TÜM KADEMELER BAŞARI LİSTESİ</h3>
                    </div>
                    <table><tr><th>Ad Soyad</th><th>Sınıf/Şube</th><th>No</th><th>Doğru</th><th>Yanlış</th><th>Boş</th><th>Net</th><th>Puan</th></tr>
                """
                for _, r in df_filtre.iterrows():
                    pdf_liste_html += f"<tr><td style='text-align:left; font-weight:bold;'>{r['Ad']} {r['Soyad']}</td><td>{r['Sınıf']}/{r['Şube']}</td><td>{r['Öğrenci No']}</td><td>{r['Doğru']}</td><td>{r['Yanlış']}</td><td>{r['Boş']}</td><td>{r['Net']}</td><td style='color:#E30A17; font-weight:bold;'>{r['Puan']}</td></tr>"
                pdf_liste_html += "</table></body></html>"
                
                c_btn1.download_button("📊 1) Tüm Kademeler Listesini İndir (PDF)", data=pdf_liste_html, file_name=f"{kurum_secim_tum}_Tum_Siniflar_Liste.html", mime="text/html")

                # 2. TÜM KADEMELER TOPLU KARNE DAĞITIMI (SAYFADA 2 ADET - OPTİKLİ)
                html_toplu_karne = """
                <html><head><meta charset="utf-8"><style>
                    @page { size: A4 portrait; margin: 10mm; }
                    body { font-family: 'Segoe UI', Tahoma, sans-serif; margin: 0; padding: 0; background: white; -webkit-print-color-adjust: exact !important; }
                    .page { width: 190mm; display: flex; flex-direction: column; gap: 8mm; page-break-after: always; }
                    .karne { width: 100%; height: 135mm; border: 3px solid #E30A17; border-radius: 12px; padding: 12px; position: relative; page-break-inside: avoid; display: flex; flex-direction: column; justify-content: space-between; overflow: hidden; }
                    .baslik { text-align: center; font-weight: 900; font-size: 14px; border-bottom: 2px solid #E30A17; padding-bottom: 4px; text-transform: uppercase; }
                    .kimlik { display: flex; justify-content: space-between; font-weight: 900; font-size: 13px; margin-top: 6px; }
                    .sira { text-align: center; background: #111827; color: white; padding: 4px; border-radius: 6px; font-size: 12px; margin: 6px 0; font-weight: bold; }
                    
                    .stats { width: 100%; border-collapse: collapse; text-align: center; font-size: 12px; margin-bottom: 5px; }
                    .stats th { background: #fef2f2; border: 1px solid #fca5a5; padding: 4px; color: #E30A17; }
                    .stats td { border: 1px solid #fca5a5; padding: 6px; font-weight: 900; font-size: 16px; }
                    
                    .optik-table { width: 100%; border-collapse: collapse; text-align: center; font-size: 10px; margin-bottom: 5px; }
                    .optik-table th { background: #fef2f2; border: 1px solid #fca5a5; padding: 4px; color: #E30A17; }
                    .optik-table td { border: 1px solid #fca5a5; padding: 5px; font-weight: bold; font-size: 11px; }
                    .optik-table .baslik-hucre { background: #111827; color: white; text-align: left; width: 85px; }
                    .optik-table .alt-baslik-hucre { background: #f1f5f9; color: #111827; text-align: left; font-size: 9px; }
                    .dogru { background-color: #dcfce7 !important; color: #059669 !important; }
                    .yanlis { background-color: #111827 !important; color: white !important; }
                    
                    .analiz { background: #f8fafc !important; border-left: 5px solid #E30A17; padding: 8px; font-size: 10px; line-height: 1.4; text-align: justify; border-radius: 6px; border: 1px solid #e2e8f0; color: #111827; }
                </style></head><body>
                """
                
                for i, row in df_filtre.reset_index().iterrows():
                    if i % 2 == 0: html_toplu_karne += "<div class='page'>"
                    
                    # 1. Bölümdeki ortak fonksiyonu çağırıyoruz!
                    analiz_metni = detayli_pedagojik_analiz(row)
                    
                    # Optik Form Hesaplama
                    try:
                        ogr_cvp = ast.literal_eval(str(row.get('Ogrenci_Cevap_Listesi', "['-']*20")))
                        key_cvp = ast.literal_eval(str(row.get('Cevap_Anahtari_Listesi', "['-']*20")))
                    except:
                        ogr_cvp = ["-"]*20; key_cvp = ["-"]*20
                        
                    optik_th = "".join([f"<th>{j+1}</th>" for j in range(20)])
                    optik_key = "".join([f"<td>{key_cvp[j]}</td>" for j in range(20)])
                    optik_ogr = ""
                    for j in range(20):
                        c = ogr_cvp[j] if j < len(ogr_cvp) else "-"
                        k = key_cvp[j] if j < len(key_cvp) else "-"
                        if c == k and c != "-": optik_ogr += f"<td class='dogru'>{c}</td>"
                        elif c != k and c != "-": optik_ogr += f"<td class='yanlis'>{c}</td>"
                        else: optik_ogr += f"<td>{c}</td>"
                    
                    html_toplu_karne += f"""
                    <div class="karne">
                        <div>
                            <div class="baslik">1. DARGEÇİT MATEMATİK OLİMPİYATI SONUÇ BELGESİ</div>
                            <div class="kimlik"><span>{row['Ad']} {row['Soyad']}</span><span style="color:#E30A17;">No: {row['Öğrenci No']}</span></div>
                            <div class="kimlik" style="color:#555; font-size:11px; margin-top:2px;"><span>{row['OKUL ADI']}</span><span>Sınıf: {row['Sınıf']}/{row['Şube']}</span></div>
                            <div class="sira">İlçe S: {row.get('İlçe Sırası','-')} &nbsp;|&nbsp; Okul S: {row.get('Okul Sırası','-')}</div>
                            
                            <table class="stats">
                                <tr><th>Doğru</th><th>Yanlış</th><th>Boş</th><th>Net</th><th style="background:#E30A17; color:white;">PUAN</th></tr>
                                <tr><td style="color:#059669;">{row['Doğru']}</td><td style="color:#E30A17;">{row['Yanlış']}</td><td>{row['Boş']}</td><td style="color:#2563eb;">{row['Net']}</td><td style="background:#111827 !important; color:white;">{row['Puan']}</td></tr>
                            </table>
                            
                            <table class="optik-table">
                                <tr><th class="baslik-hucre">Soru No</th>{optik_th}</tr>
                                <tr><th class="alt-baslik-hucre">Cevap Anahtarı</th>{optik_key}</tr>
                                <tr><th class="alt-baslik-hucre">Öğrenci Cevabı</th>{optik_ogr}</tr>
                            </table>
                        </div>
                        <div class="analiz">
                            <b style="color:#E30A17; font-size:12px;">🎓 Pedagojik Değerlendirme:</b><br>{analiz_metni}
                        </div>
                    </div>
                    """
                    if (i + 1) % 2 == 0 or i == len(df_filtre) - 1: html_toplu_karne += "</div>"
                
                html_toplu_karne += "</body></html>"
                
                c_btn2.download_button("🖨️ 2) Tüm Kademelerin Karnelerini Al (PDF)", data=html_toplu_karne, file_name=f"{kurum_secim_tum}_Tum_Siniflar_Karneler.html", mime="text/html")

    elif sifre != "":
        st.error("❌ Yetkisiz Erişim: Şifre Hatalı!")
