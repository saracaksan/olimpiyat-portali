import streamlit as st
import pandas as pd
import io
import glob
import ast
import plotly.express as px

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="1. Dargeçit Matematik Olimpiyatı", layout="wide", page_icon="🥇")

# --- PROFESYONEL VE ESTETİK CSS ---
st.markdown("""
    <style>
    :root {
        --meb-red: #E30A17;
        --navy: #111827;
        --light-bg: #f8fafc;
    }
    .main { background-color: var(--light-bg); }
    
    /* Başlık Banner Tasarımı */
    .header-banner {
        background: linear-gradient(135deg, #ffffff 0%, #fef2f2 100%);
        padding: 35px; border-bottom: 8px solid var(--meb-red);
        border-radius: 12px; margin-bottom: 30px; text-align: center;
        box-shadow: 0 8px 20px rgba(227, 10, 23, 0.08);
    }
    .header-banner h1 { color: var(--navy); font-weight: 900; font-size: 38px; margin: 0; letter-spacing:-1px; }
    .header-banner h3 { color: var(--meb-red); font-weight: 800; font-size: 18px; margin-top: 8px; text-transform: uppercase; }

    /* Tab Tasarımları */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { 
        height: 55px; background: white; border-radius: 8px 8px 0 0; 
        font-weight: 800; font-size: 16px; border: 1px solid #e2e8f0; border-bottom:none;
    }
    .stTabs [aria-selected="true"] { background: var(--navy) !important; color: white !important; border-bottom: 5px solid var(--meb-red) !important; }

    /* Ön İzleme ve Sonuç Kartları */
    .preview-card {
        background: white; padding: 30px; border-radius: 15px;
        border-top: 6px solid var(--meb-red); border-left: 6px solid var(--navy);
        box-shadow: 0 10px 25px rgba(0,0,0,0.08); margin-top: 20px;
    }
    
    .metric-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 15px; margin: 25px 0; }
    .metric-box {
        padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #e2e8f0; background: #fdfdfd;
    }
    .metric-box span { display: block; font-size: 13px; font-weight: 800; color: #64748b; text-transform: uppercase; }
    .metric-box b { font-size: 28px; color: var(--navy); }

    /* Estetik Veri Tabloları */
    .stDataFrame { border-radius: 10px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
    
    /* İndirme Butonları */
    .stButton>button {
        background: var(--navy); color: white; border-radius: 8px; font-weight: 800; height: 3.2em;
        transition: 0.3s; border: none; width: 100%;
    }
    .stButton>button:hover { background: var(--meb-red); transform: translateY(-2px); box-shadow: 0 5px 15px rgba(227,10,23,0.3); }
    </style>
""", unsafe_allow_html=True)

# --- DERİNLİKLİ PEDAGOJİK ANALİZ MOTORU ---
def profesyonel_pedagojik_analiz(row):
    p, d, y, b, ad = row['Puan'], row['Doğru'], row['Yanlış'], row['Boş'], row['Ad']
    
    giris = f"Değerli Öğrencimiz <b>{ad}</b>,<br><br>"
    vizyon = ("Matematik; sadece rakamlardan oluşan bir ders değil, analitik düşünme yeteneğimizi geliştiren en güçlü pusuladır. "
              "Bu olimpiyat sınavına katılarak yeteneklerini sınırların ötesine taşıma cesareti gösterdiğin için seni kutluyoruz.<br><br>")
    
    if p >= 85:
        durum = (f"<b>{p} puan</b> ile sergilediğin bu olağanüstü performans, zihnindeki matematiksel haritanın ne kadar kusursuz olduğunu kanıtlıyor. "
                 f"Sınavdaki <b>{d} doğru</b> cevabın, en karmaşık problemleri bile saniyeler içinde çözebildiğini gösteriyor. "
                 f"Yaptığın <b>{y} yanlış</b>, zirveye giden yoldaki küçük birer tecrübedir. Asla durma!")
    elif p >= 65:
        durum = (f"<b>{p} puan</b> alarak ne kadar güçlü bir temel üzerine inşa edildiğini herkese gösterdin. "
                 f"<b>{d} doğru</b> cevabın odaklanma becerinin yüksekliğine işaret ediyor. "
                 f"Yanlışların ve boşların <b>({y} Yanlış, {b} Boş)</b>, olimpiyat sorularındaki o ince tuzaklara yenik düştüğünü gösterse de, "
                 "bu ufak dikkatsizlikleri elediğinde zirve senin olacak.")
    elif p >= 40:
        durum = (f"<b>{p} puan</b> ile çok kıymetli bir eşiği geride bıraktın. <b>{b} soruyu boş bırakman</b>, "
                 "emin olmadığın riskten kaçınma stratejisini doğru kullandığını gösteriyor. "
                 "Yanlış yaptığın konuları öğrenmen gereken birer fırsat gibi gör. Pratik yaptıkça netlerin hızla artacak!")
    else:
        durum = (f"<b>{p} puan</b> almış olman senin yeteneğini değil, olimpiyat dünyasına attığın zorlu ilk adımı temsil eder. "
                 f"Olimpiyat soruları en iyileri bile zorlamak için tasarlanmıştır. Yaptığın <b>{y} yanlış</b> senin 'gelişim alanını' gösteren "
                 "birer hazinedir. Pes etme; hatalarından ders çıkardıkça başaracaksın.")
    
    kapanis = "<br><br><b>Başarı yolculuğunda her zaman yanındayız!</b>"
    return giris + vizyon + durum + kapanis

# --- OKUL VE MİLLİ EĞİTİM RÖNTGEN MOTORU ---
def okul_gelisim_metni(okul_adi, okul_ort, ilce_ort, toplam_ogrenci):
    fark = okul_ort - ilce_ort
    if fark > 5:
        durum = f"İlçe genel ortalamasının ({ilce_ort:.2f}) belirgin bir şekilde üzerine çıkarak <b>{okul_ort:.2f}</b> ortalama ile üstün bir başarı sergilemiştir."
        tavsiye = "Bu yüksek başarı ivmesini korumak adına, halihazırda iyi seviyede olan öğrencilerimizin daha üst düzey olimpiyat kaynaklarıyla desteklenmesi önerilmektedir. Liderliğiniz için teşekkür ederiz."
    elif fark >= -3:
        durum = f"İlçe genel ortalaması ({ilce_ort:.2f}) ile paralel, istikrarlı bir başarı göstererek <b>{okul_ort:.2f}</b> ortalamaya ulaşmıştır."
        tavsiye = "Mevcut ortalamayı yukarılara taşımak için öğrencilerin kazanım eksikliklerinin birebir tespit edilmesi ve yeni nesil soru tarzlarına yönelik periyodik etüt çalışmaları yapılması başarınızı artıracaktır."
    else:
        durum = f"Olimpiyat sınavının zorlayıcı yapısı neticesinde, ilçe ortalamasının ({ilce_ort:.2f}) bir miktar gerisinde kalarak <b>{okul_ort:.2f}</b> ortalama elde etmiştir."
        tavsiye = "Öğrencilerimizdeki sınav heyecanı veya yeni nesil sorulara aşinalık eksikliği bu sonuca etki etmiş olabilir. Temel matematik okuryazarlığını artıracak teşvik edici faaliyetlerle bu açığın hızla kapatılacağına inancımız tamdır."
    
    return f"""Saygıdeğer <b>{okul_adi}</b> İdarecileri ve Zümre Öğretmenlerimiz,<br><br>
    Okulunuz, bu olimpiyatta toplam <b>{toplam_ogrenci}</b> öğrenci ile temsil edilmiş olup, {durum} {tavsiye}<br><br>
    Aşağıda sunulan şube, öğrenci ve zümre bazlı analizleri "Hangi sınıfımıza/konuya daha fazla pedagojik destek olmalıyız?" sorusunun rehberi olarak değerlendiriniz."""

# --- BANNER ---
st.markdown("""
    <div class="header-banner">
        <h1>🥇 1. DARGEÇİT MATEMATİK OLİMPİYATI</h1>
        <h3>Sınav Sonuç, Veri Analizi ve Kurum Röntgen Portalı</h3>
    </div>
""", unsafe_allow_html=True)

# --- VERİ YÜKLEME ---
@st.cache_data
def verileri_yukle():
    dosyalar = glob.glob("sonuclar_*.xlsx")
    liste = []
    for d in dosyalar:
        try:
            df = pd.read_excel(d)
            if 'Puan' in df.columns and 'Öğrenci No' in df.columns:
                df['Arama_No'] = df['Öğrenci No'].astype(str).str.replace('.0', '', regex=False).str.strip().str.lstrip('0')
                df['Sınıf'] = df['Sınıf'].astype(str).str.replace('.0', '', regex=False).str.strip()
                liste.append(df)
        except: pass
    if liste:
        return pd.concat(liste, ignore_index=True).sort_values(by=['Puan', 'Net'], ascending=[False, False]).reset_index(drop=True)
    return pd.DataFrame()

df_tum = verileri_yukle()
# --- YAN MENÜ (KADEME SEÇİMİ) ---
with st.sidebar:
    st.markdown('<h3 style="color:#E30A17; text-align:center;">📊 KADEME SEÇİNİZ</h3>', unsafe_allow_html=True)
    sinif_listesi = [f"{i}. Sınıf" for i in range(4, 13)]
    secilen_kademe_str = st.selectbox("Sınıf Düzeyi:", sinif_listesi, index=3)
    kademe_no = secilen_kademe_str.split(".")[0]
    st.divider()
    st.info("💡 **Öğrenciler:** Önce sınıfınızı, sonra okulunuzu seçip numaranızı giriniz.\n\n💡 **İdareciler:** Tüm analiz, röntgen ve liste dökümleri burada seçtiğiniz sınıfa göre otomatik hazırlanır.")

# Aktif kademenin verisini filtrele
df_aktif = df_tum[df_tum['Sınıf'] == kademe_no].copy() if not df_tum.empty else pd.DataFrame()

# --- ANA SEKMELER ---
tab_ogrenci, tab_idareci = st.tabs(["🎓 ÖĞRENCİ SONUÇ EKRANI", "🏛️ MİLLİ EĞİTİM / KURUM RÖNTGENİ"])

# ==============================================================================
# 2. BÖLÜM: ÖĞRENCİ GİRİŞ, TABLOLU ÖN İZLEME VE ANALİZ EKRANI
# ==============================================================================
with tab_ogrenci:
    if df_aktif.empty:
        st.warning(f"Sistemde henüz {secilen_kademe_str} seviyesine ait sınav verisi bulunmamaktadır.")
    else:
        st.markdown("### 🔍 Bireysel Sonuç, Tablolu Ön İzleme ve Pedagojik Karne")
        
        # Öğrenci Arama Paneli
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
                    analiz_html = profesyonel_pedagojik_analiz(o)
                    
                    # 1. Aşama: TABLOLU ÖN İZLEME (İstediğiniz Veri Okuryazarlığı Formatı)
                    st.markdown("#### 📊 Öğrenci Sonuç Veri Tablosu (Ön İzleme)")
                    gosterilecek_tablo = pd.DataFrame([o])[['Öğrenci No', 'Ad', 'Soyad', 'OKUL ADI', 'Sınıf', 'Şube', 'Doğru', 'Yanlış', 'Boş', 'Net', 'Puan', 'Okul Sırası', 'İlçe Sırası']]
                    st.dataframe(gosterilecek_tablo, use_container_width=True, hide_index=True)
                    
                    # 2. Aşama: PROFESYONEL KARNE VE ANALİZ KARTI
                    st.markdown(f"""
                    <div class="preview-card">
                        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:2px solid #e2e8f0; padding-bottom:15px;">
                            <div>
                                <h1 style="margin:0; color:#111827; font-size:32px;">{o['Ad']} {o['Soyad']}</h1>
                                <p style="margin:0; color:#E30A17; font-weight:800; font-size:18px;">{o['OKUL ADI']} - {o['Sınıf']}/{o['Şube']}</p>
                            </div>
                            <div style="background:#111827; color:white; padding:10px 20px; border-radius:8px; font-weight:bold; font-size:18px;">
                                No: {o['Öğrenci No']}
                            </div>
                        </div>
                        
                        <div class="metric-grid">
                            <div class="metric-box"><span>Doğru</span><b style="color:#059669;">{o['Doğru']}</b></div>
                            <div class="metric-box"><span>Yanlış</span><b style="color:#E30A17;">{o['Yanlış']}</b></div>
                            <div class="metric-box"><span>Boş</span><b style="color:#64748b;">{o['Boş']}</b></div>
                            <div class="metric-box"><span>Net</span><b style="color:#2563eb;">{o['Net']}</b></div>
                            <div class="metric-box" style="background:#111827; border-color:#111827;"><span style="color:#94a3b8;">PUAN</span><b style="color:white; font-size:34px;">{o['Puan']}</b></div>
                        </div>

                        <div style="background:#fff5f5; border-left:6px solid #E30A17; padding:25px; border-radius:10px;">
                            <h3 style="margin-top:0; color:#E30A17; font-size:20px;">🎓 Uzman Pedagojik Analiz ve Rehberlik</h3>
                            <p style="margin:0; font-size:16px; line-height:1.7; color:#1e293b; text-align:justify;">{analiz_html}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # 3. Aşama: İNDİRİLEBİLİR RESMİ PDF BELGESİ
                    bireysel_pdf_html = f"""
                    <html><head><meta charset="utf-8"><style>
                        @page {{ size: A4 portrait; margin: 15mm; }}
                        body {{ font-family: 'Segoe UI', Tahoma, sans-serif; padding: 0; margin: 0; color: #111827; -webkit-print-color-adjust: exact !important; }}
                        .karne-container {{ border: 5px solid #111827; border-radius: 20px; padding: 40px; background: white; }}
                        .header {{ text-align: center; border-bottom: 4px solid #E30A17; padding-bottom: 20px; margin-bottom: 30px; }}
                        .header h1 {{ margin: 0; font-size: 26px; text-transform: uppercase; }}
                        .header h2 {{ margin: 10px 0 0 0; color: #E30A17; font-size: 20px; }}
                        .info-strip {{ display: flex; justify-content: space-between; font-size: 18px; font-weight: bold; margin-bottom: 30px; background: #f8fafc; padding: 15px; border-radius: 10px; border: 1px solid #e2e8f0; }}
                        .stats-table {{ width: 100%; border-collapse: collapse; text-align: center; margin-bottom: 30px; }}
                        .stats-table th {{ background: #111827; color: white; padding: 15px; font-size: 18px; border: 1px solid #111827; }}
                        .stats-table td {{ padding: 20px; font-size: 28px; font-weight: 900; border: 1px solid #cbd5e1; }}
                        .ranks {{ display: flex; justify-content: center; gap: 30px; margin-bottom: 30px; }}
                        .rank-box {{ background: #E30A17; color: white; padding: 15px 30px; border-radius: 10px; font-weight: bold; font-size: 18px; }}
                        .analiz-box {{ background: #fef2f2; border-left: 8px solid #E30A17; padding: 25px; font-size: 16px; line-height: 1.6; text-align: justify; border-radius: 10px; }}
                    </style></head><body>
                        <div class="karne-container">
                            <div class="header">
                                <h1>1. DARGEÇİT MATEMATİK OLİMPİYATI</h1>
                                <h2>RESMİ SINAV SONUÇ BELGESİ</h2>
                            </div>
                            <div class="info-strip">
                                <span>{o['Ad']} {o['Soyad']}</span>
                                <span>{o['OKUL ADI']} - {o['Sınıf']}/{o['Şube']}</span>
                                <span style="color:#E30A17;">No: {o['Öğrenci No']}</span>
                            </div>
                            <div class="ranks">
                                <div class="rank-box" style="background:#111827;">İlçe Sırası: {o.get('İlçe Sırası','-')}</div>
                                <div class="rank-box">Okul Sırası: {o.get('Okul Sırası','-')}</div>
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
                            <div class="analiz-box">
                                <h3 style="margin-top:0; color:#E30A17;">🎓 Uzman Pedagojik Değerlendirme</h3>
                                {analiz_html}
                            </div>
                        </div>
                    </body></html>
                    """
                    st.download_button(f"📥 {o['Ad']} {o['Soyad']} - Karnesini İndir (Yazdırılabilir PDF/HTML)", data=bireysel_pdf_html, file_name=f"{o['Ad']}_{o['Soyad']}_Olimpiyat_Karne.html", mime="text/html")
                else:
                    st.error("❌ Sistemde eşleşen kayıt bulunamadı. Lütfen 'Okul' ve 'Öğrenci No' bilgisini kontrol ediniz.")
                    # ==============================================================================
# 3. BÖLÜM: İDARECİ VE MİLLİ EĞİTİM RÖNTGEN / RAPORLAMA PANELİ
# ==============================================================================
with tab_idareci:
    st.markdown("### 🔐 İlçe Milli Eğitim ve Okul İdaresi Yönetim Paneli")
    sifre = st.text_input("Yetkili Giriş Şifresi:", type="password")
    
    if sifre == "darder47":
        if df_tum.empty:
            st.error("Sistemde analiz edilecek herhangi bir sonuç verisi bulunamadı.")
        else:
            sub1, sub2, sub3, sub4 = st.tabs([
                "🏆 İLÇE GENEL RÖNTGENİ", 
                "📈 OKUL GELİŞİM RÖNTGENİ", 
                "📉 ŞUBE / ÖĞRETMEN RÖNTGENİ", 
                "📑 TOPLU LİSTELER VE KARNELER"
            ])

            # -----------------------------------------------------
            # ALT SEKME 1: İLÇE GENEL RÖNTGENİ
            # -----------------------------------------------------
            with sub1:
                st.markdown(f"#### 🏢 {secilen_kademe_str} İlçe Geneli Okul Başarı Sıralaması ve İstatistikleri")
                
                if df_aktif.empty:
                    st.warning("Bu sınıf düzeyinde henüz sınav verisi yok.")
                else:
                    c_m1, c_m2, c_m3, c_m4 = st.columns(4)
                    with c_m1: st.markdown(f"<div class='metric-box'><span>Sınava Giren Öğrenci</span><b>{len(df_aktif)}</b></div>", unsafe_allow_html=True)
                    with c_m2: st.markdown(f"<div class='metric-box'><span>Katılımcı Okul</span><b>{df_aktif['OKUL ADI'].nunique()}</b></div>", unsafe_allow_html=True)
                    with c_m3: st.markdown(f"<div class='metric-box'><span>İlçe Puan Ortalaması</span><b>{df_aktif['Puan'].mean():.2f}</b></div>", unsafe_allow_html=True)
                    with c_m4: st.markdown(f"<div class='metric-box'><span>İlçe Net Ortalaması</span><b style='color:#E30A17;'>{df_aktif['Net'].mean():.2f}</b></div>", unsafe_allow_html=True)
                    
                    df_okul_genel = df_aktif.groupby('OKUL ADI').agg(Ogr_Sayisi=('Puan', 'count'), Ort_Puan=('Puan', 'mean')).reset_index()
                    
                    st.markdown("<br>##### 📊 Okul Puan Ortalamaları Kıyaslaması", unsafe_allow_html=True)
                    fig = px.bar(df_okul_genel.sort_values(by='Ort_Puan', ascending=True), 
                                 x='Ort_Puan', y='OKUL ADI', orientation='h', text_auto='.2f', 
                                 color='Ort_Puan', color_continuous_scale='Reds')
                    fig.update_layout(height=500, xaxis_title="Puan Ortalaması", yaxis_title="")
                    st.plotly_chart(fig, use_container_width=True)

            # -----------------------------------------------------
            # ALT SEKME 2: OKUL GELİŞİM RÖNTGENİ
            # -----------------------------------------------------
            with sub2:
                st.markdown(f"#### 📈 {secilen_kademe_str} Okul Gelişim ve Değerlendirme Raporu")
                
                if df_aktif.empty:
                    st.warning("Bu kademede veri bulunmamaktadır.")
                else:
                    secilen_kurum = st.selectbox("Röntgeni Çekilecek Okulu Seçiniz:", sorted(df_aktif['OKUL ADI'].unique()), key="gelisim_okul")
                    
                    df_kurum_gelisim = df_aktif[df_aktif['OKUL ADI'] == secilen_kurum]
                    ilce_ort = df_aktif['Puan'].mean()
                    okul_ort = df_kurum_gelisim['Puan'].mean()
                    toplam_ogrenci = len(df_kurum_gelisim)
                    
                    df_subeler = df_kurum_gelisim.groupby('Şube').agg(Mevcut=('Puan', 'count'), Sube_Ort_Puan=('Puan', 'mean')).reset_index().sort_values(by='Sube_Ort_Puan', ascending=False)
                    
                    metin = okul_gelisim_metni(secilen_kurum, okul_ort, ilce_ort, toplam_ogrenci)
                    
                    st.info(f"📋 Rapor Özeti: {secilen_kurum} kurumu {toplam_ogrenci} öğrenci ile {okul_ort:.2f} puan ortalaması elde etmiştir.")
                    
                    # OKUL GELİŞİM RAPORU PDF ŞABLONU
                    gelisim_html = f"""
                    <html><head><meta charset="utf-8"><style>
                        @page {{ size: A4 portrait; margin: 15mm; }}
                        body {{ font-family: 'Segoe UI', Tahoma, sans-serif; margin: 0; padding: 0; color: #111827; -webkit-print-color-adjust: exact !important; }}
                        .baslik-alan {{ text-align: center; border-bottom: 5px solid #111827; padding-bottom: 15px; margin-bottom: 25px; }}
                        .baslik-alan h1 {{ margin: 0; font-size: 22px; font-weight: 900; letter-spacing: 0.5px; }}
                        .baslik-alan h2 {{ margin: 5px 0 0 0; color: #E30A17; font-size: 16px; font-weight: bold; text-transform: uppercase; }}
                        .bilgi-serit {{ display: flex; justify-content: space-between; background: #fef2f2; border: 1px solid #fca5a5; padding: 15px; border-radius: 8px; margin-bottom: 20px; font-weight: bold; font-size: 14px; }}
                        .analiz-metni {{ font-size: 14px; line-height: 1.6; text-align: justify; margin-bottom: 30px; background: #f8fafc; padding: 20px; border-radius: 8px; border-left: 5px solid #111827; }}
                        .tablo-alan {{ width: 100%; border-collapse: collapse; text-align: center; margin-bottom: 30px; font-size: 14px; }}
                        .tablo-alan th {{ background: #111827; color: white; padding: 12px; border: 1px solid #111827; }}
                        .tablo-alan td {{ padding: 12px; border: 1px solid #cbd5e1; font-weight: bold; font-size: 15px; }}
                    </style></head><body>
                        <div class="baslik-alan">
                            <h1>T.C. DARGEÇİT KAYMAKAMLIĞI</h1>
                            <h2>{kademe_no}. SINIFLAR MATEMATİK OLİMPİYATI - KURUM GELİŞİM RAPORU</h2>
                        </div>
                        <div class="bilgi-serit">
                            <span>Kurum: {secilen_kurum}</span>
                            <span>İlçe Ortalaması: {ilce_ort:.2f}</span>
                            <span style="color:#E30A17;">Okul Ortalaması: {okul_ort:.2f}</span>
                        </div>
                        <div class="analiz-metni">
                            {metin}
                        </div>
                        <table class="tablo-alan">
                            <tr><th>Şube Adı</th><th>Sınava Giren Öğrenci</th><th>Şube Puan Ortalaması</th></tr>
                    """
                    for _, s_row in df_subeler.iterrows():
                        gelisim_html += f"<tr><td>{s_row['Şube']}</td><td>{s_row['Mevcut']}</td><td style='color:#E30A17;'>{s_row['Sube_Ort_Puan']:.2f}</td></tr>"
                    gelisim_html += """
                        </table>
                        <div style="font-size: 12px; color: #64748b; text-align: center; margin-top: 50px; border-top: 1px solid #cbd5e1; padding-top:15px;">
                            Dargeçit İlçe Milli Eğitim Müdürlüğü - Matematik Olimpiyatı Ölçme Değerlendirme Merkezi
                        </div>
                    </body></html>
                    """
                    st.download_button("🖨️ Kurum Gelişim Raporunu İndir (Yazdırılabilir PDF)", data=gelisim_html, file_name=f"{secilen_kurum}_Gelisim_Raporu.html", mime="text/html")

            # -----------------------------------------------------
            # ALT SEKME 3: ŞUBE VE ÖĞRETMEN RÖNTGENİ
            # -----------------------------------------------------
            with sub3:
                st.markdown(f"#### 📉 {secilen_kademe_str} Şube ve Sınıf İçi Başarı Analizleri")
                if df_aktif.empty:
                    st.warning("Bu sınıf düzeyinde veri yok.")
                else:
                    st.markdown("**En Başarılı Şubeler (Öğretmen Etkisi ve Sınıf İçi Rekabet)**")
                    st.write("İlçe genelindeki tüm şubelerin başarı sıralaması aşağıdadır (Sadece en az 3 öğrencisi olan sınıflar baz alınmıştır).")
                    
                    df_sube_genel = df_aktif.groupby(['OKUL ADI', 'Şube']).agg(Ogr=('Puan', 'count'), Puan_Ort=('Puan', 'mean')).reset_index()
                    df_sube_genel = df_sube_genel[df_sube_genel['Ogr'] >= 3].sort_values(by='Puan_Ort', ascending=True).tail(20)
                    df_sube_genel['Sube_Ad'] = df_sube_genel['OKUL ADI'] + " - " + df_sube_genel['Şube']
                    
                    fig3 = px.bar(df_sube_genel, x='Puan_Ort', y='Sube_Ad', orientation='h', text_auto='.2f', color='Puan_Ort', color_continuous_scale='Teal')
                    fig3.update_layout(height=600, xaxis_title="Şube Puan Ortalaması", yaxis_title="")
                    st.plotly_chart(fig3, use_container_width=True)

            # -----------------------------------------------------
            # ALT SEKME 4: TOPLU LİSTELER VE KARNELER
            # -----------------------------------------------------
            with sub4:
                st.markdown(f"#### 📑 {secilen_kademe_str} Toplu Veri Çekimi ve Çoklu Karneler")
                
                if df_aktif.empty:
                    st.warning("Bu sınıf için veri bulunmamaktadır.")
                else:
                    kurum_secim = st.selectbox("İşlem Yapılacak Kurumu Seçin:", ["Tüm İlçe Listesi"] + sorted(df_aktif['OKUL ADI'].unique()), key="k_karne")
                    df_filtre = df_aktif if kurum_secim == "Tüm İlçe Listesi" else df_aktif[df_aktif['OKUL ADI'] == kurum_secim]
                    
                    st.markdown("##### 🗃️ Veri Tablosu")
                    st.dataframe(df_filtre[['İlçe Sırası', 'Okul Sırası', 'OKUL ADI', 'Sınıf', 'Şube', 'Öğrenci No', 'Ad', 'Soyad', 'Net', 'Puan']], use_container_width=True)
                    
                    st.markdown("##### 🖨️ İndirme Seçenekleri")
                    c_btn1, c_btn2, c_btn3 = st.columns(3)
                    
                    # 1. EXCEL LİSTE
                    buf_ex = io.BytesIO()
                    with pd.ExcelWriter(buf_ex, engine='openpyxl') as writer:
                        df_filtre.to_excel(writer, index=False)
                    c_btn1.download_button("📊 1) Excel Tablosu Olarak İndir", data=buf_ex.getvalue(), file_name=f"{kurum_secim}_Liste.xlsx", use_container_width=True)

                    # 2. PDF LİSTE (TABLO HALİNDE)
                    pdf_liste_html = f"""
                    <html><head><meta charset="utf-8"><style>
                        @page {{ size: A4 portrait; margin: 15mm; }}
                        body {{ font-family: 'Segoe UI', Tahoma, sans-serif; margin: 0; font-size: 11px; }}
                        .baslik {{ text-align: center; border-bottom: 2px solid #111827; margin-bottom: 15px; padding-bottom:10px; }}
                        table {{ width: 100%; border-collapse: collapse; text-align: center; }}
                        th {{ background-color: #111827; color: white; padding: 6px; border: 1px solid #111827; }}
                        td {{ padding: 5px; border: 1px solid #cbd5e1; }}
                        tr:nth-child(even) {{ background-color: #f8fafc; }}
                    </style></head><body>
                        <div class="baslik">
                            <h2 style="margin:0;">T.C. DARGEÇİT KAYMAKAMLIĞI - 1. MATEMATİK OLİMPİYATI</h2>
                            <h3 style="margin:5px 0 0 0; color:#E30A17;">{kurum_secim} - {kademe_no}. SINIF BAŞARI LİSTESİ</h3>
                        </div>
                        <table>
                            <tr><th>İlçe S.</th><th>Okul S.</th><th>Okul</th><th>Sınıf/Şube</th><th>No</th><th>Ad Soyad</th><th>D</th><th>Y</th><th>B</th><th>Net</th><th>Puan</th></tr>
                    """
                    for _, r in df_filtre.iterrows():
                        pdf_liste_html += f"<tr><td>{r.get('İlçe Sırası','-')}</td><td>{r.get('Okul Sırası','-')}</td><td>{r['OKUL ADI']}</td><td>{r['Sınıf']}/{r['Şube']}</td><td>{r['Öğrenci No']}</td><td style='text-align:left;'>{r['Ad']} {r['Soyad']}</td><td>{r['Doğru']}</td><td>{r['Yanlış']}</td><td>{r['Boş']}</td><td style='font-weight:bold;'>{r['Net']}</td><td style='color:#E30A17; font-weight:bold;'>{r['Puan']}</td></tr>"
                    pdf_liste_html += "</table></body></html>"
                    
                    c_btn2.download_button("📑 2) Liste Halinde PDF İndir", data=pdf_liste_html, file_name=f"{kurum_secim}_PDF_Liste.html", mime="text/html", use_container_width=True)

                    # 3. KUSURSUZ ALT ALTA KARNELER (1 SAYFADA 3 ADET)
                    html_karne = """
                    <html><head><meta charset="utf-8"><style>
                        @page { size: A4 portrait; margin: 10mm; }
                        * { box-sizing: border-box; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
                        body { font-family: 'Segoe UI', Tahoma, sans-serif; margin: 0; padding: 0; color: #111827; background: white; }
                        .page { width: 190mm; height: 277mm; display: flex; flex-direction: column; justify-content: flex-start; gap: 8mm; page-break-after: always; }
                        .karne { width: 100%; height: 86mm; border: 2.5px solid #E30A17; border-radius: 12px; padding: 12px 15px; display: flex; flex-direction: column; justify-content: space-between; position: relative; page-break-inside: avoid; }
                        .baslik { text-align: center; font-weight: 900; font-size: 14px; border-bottom: 2px solid #E30A17; padding-bottom: 5px; }
                        .kimlik-satir { display: flex; justify-content: space-between; font-weight: 900; font-size: 13px; margin-top: 6px; }
                        .sira-kutu { text-align: center; background: #111827; color: white; padding: 5px; border-radius: 5px; font-size: 11px; font-weight: bold; margin-top: 4px; }
                        .stats-tablo { width: 100%; border-collapse: collapse; text-align: center; font-size: 12px; margin-top: 6px; }
                        .stats-tablo th { background: #fef2f2; border: 1px solid #fca5a5; padding: 4px; color: #E30A17; }
                        .stats-tablo td { border: 1px solid #fca5a5; padding: 4px; font-weight: 900; font-size: 14px; }
                        .optik-tablo { width: 100%; border-collapse: collapse; text-align: center; font-size: 9px; margin-top: 6px; table-layout: fixed; }
                        .optik-tablo th, .optik-tablo td { border: 1px solid #fca5a5; height: 16px; overflow: hidden; font-weight: bold; }
                        .optik-tablo th { background: #fef2f2; color: #E30A17; }
                        .dogru { background: #dcfce7 !important; color: #059669 !important; }
                        .yanlis { background: #111827 !important; color: white !important; } 
                        .analiz-kutu { background: #f8fafc !important; border-left: 4px solid #E30A17; padding: 6px 8px; font-size: 9px; line-height: 1.3; font-weight: 600; text-align: justify; margin-top: 6px; border-radius: 4px; border: 1px solid #e2e8f0; }
                    </style></head><body>
                    """
                    for i, row in df_filtre.reset_index().iterrows():
                        if i % 3 == 0: html_karne += "<div class='page'>"
                        
                        try: ogr_cvp = ast.literal_eval(row['Ogrenci_Cevap_Listesi']); key_cvp = ast.literal_eval(row['Cevap_Anahtari_Listesi'])
                        except: ogr_cvp = ["-"]*20; key_cvp = ["-"]*20
                        
                        optik_icerik = ""
                        for j in range(20):
                            c, k = (ogr_cvp[j] if j < len(ogr_cvp) else "-"), (key_cvp[j] if j < len(key_cvp) else "-")
                            if c == k and c != "-": optik_icerik += f"<td class='dogru'>{c}</td>"
                            elif c != k and c != "-": optik_icerik += f"<td class='yanlis'>{c}</td>"
                            else: optik_icerik += f"<td>-</td>"

                        # Öğrenciye özel esprili ve cesaretlendirici, A4 formatına (sayfada 3 karne) sığacak özel analiz
                        p_val = row['Puan']
                        if p_val >= 85: k_yr = "Mükemmel! Matematiksel zekan olimpiyat seviyesinde. Yaptığın ufak tefek yanlışlar sadece birer nazar boncuğu. Durmak yok, zirve senin!"
                        elif p_val >= 65: k_yr = "Harika iş çıkardın! Temelin çok sağlam. Yanlışların ve boşların muhtemelen ufak dikkatsizliklerden ya da süre sıkıntısından. Üzerine gidersen şampiyonsun."
                        elif p_val >= 40: k_yr = "İyi bir gayret! Boş bırakarak mantıklı risk yönetimi yaptın. Yanlışlarını sakın dert etme, onlar senin öğrenmen gereken kıymetli hazinelerin. Soru çözmeye devam!"
                        else: k_yr = "Olimpiyat soruları en iyileri bile zorlar. Hataların sana hangi konulara çalışman gerektiğini gösteren birer pusula. Asla pes etme, hatalarından ders çıkardıkça yükseleceksin!"

                        html_karne += f"""
                        <div class="karne">
                            <div>
                                <div class="baslik">1. DARGEÇİT MATEMATİK OLİMPİYATI SONUÇ BELGESİ</div>
                                <div class="kimlik-satir"><span>{row['Ad']} {row['Soyad']}</span><span style="color:#E30A17;">Öğr. No: {row['Öğrenci No']}</span></div>
                                <div class="kimlik-satir" style="color:#555; font-size:11px;"><span>{row['OKUL ADI']}</span><span>Sınıf: {row['Sınıf']}/{row['Şube']}</span></div>
                                <div class="sira-kutu">İlçe Sırası: {row.get('İlçe Sırası','-')} &nbsp;|&nbsp; Okul Sırası: {row.get('Okul Sırası','-')}</div>
                                
                                <table class="stats-tablo">
                                    <tr><th>Doğru</th><th>Yanlış</th><th>Boş</th><th>Net</th><th>Puan</th></tr>
                                    <tr><td style="color:#059669;">{row['Doğru']}</td><td style="color:#E30A17;">{row['Yanlış']}</td><td>{row['Boş']}</td><td style="color:#2563eb;">{row['Net']}</td><td style="background:#111827 !important; color:white; font-size: 16px;">{row['Puan']}</td></tr>
                                </table>
                                
                                <table class="optik-tablo">
                                    <tr>{"".join([f"<th>{j+1}</th>" for j in range(20)])}</tr>
                                    <tr>{optik_icerik}</tr>
                                </table>
                            </div>
                            <div class="analiz-kutu"><b style="color:#E30A17;">🎓 Analiz:</b> {k_yr}</div>
                        </div>
                        """
                        if (i + 1) % 3 == 0 or i == len(df_filtre) - 1: html_karne += "</div>"
                    
                    html_karne += "</body></html>"
                    c_btn3.download_button("🖨️ 3) Alt Alta Özel Karneleri Al (PDF)", data=html_karne, file_name=f"{kurum_secim}_Karneler.html", mime="text/html", use_container_width=True)
                    
                    st.info("💡 **Önemli Yazdırma Notu:** Karneleri veya Raporları tarayıcıda açıp `Ctrl+P` yaptığınızda ayarlar kısmından **'Kenar Boşlukları: Yok (Margins: None)'** ve **'Altbilgi/Üstbilgi yazdırılmasın (Headers/Footers: Off)'** seçeneklerini işaretlerseniz belgeleriniz matbaadan çıkmış gibi kusursuz olur.")
    
    elif sifre != "":
        st.error("❌ Hatalı Şifre Girdiniz!")
                    
