import streamlit as st
import pandas as pd
import io
import glob
import ast
import plotly.express as px

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="1. Dargeçit Matematik Olimpiyatı", layout="wide", page_icon="🥇")

# --- PROFESYONEL VE ESTETİK CSS (MEB KIRMIZISI KONSEPTİ) ---
st.markdown("""
    <style>
    :root {
        --meb-red: #E30A17;
        --navy: #111827;
        --light-bg: #f8fafc;
    }
    .main { background-color: var(--light-bg); }
    
    .header-banner {
        background: linear-gradient(135deg, #ffffff 0%, #fef2f2 100%);
        padding: 35px; border-bottom: 8px solid var(--meb-red);
        border-radius: 12px; margin-bottom: 30px; text-align: center;
        box-shadow: 0 8px 20px rgba(227, 10, 23, 0.08);
    }
    .header-banner h1 { color: var(--navy); font-weight: 900; font-size: 38px; margin: 0; letter-spacing:-1px; }
    .header-banner h3 { color: var(--meb-red); font-weight: 800; font-size: 18px; margin-top: 8px; text-transform: uppercase; }

    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { 
        height: 55px; background: white; border-radius: 8px 8px 0 0; 
        font-weight: 800; font-size: 16px; border: 1px solid #e2e8f0;
    }
    .stTabs [aria-selected="true"] { background: var(--navy) !important; color: white !important; border-bottom: 5px solid var(--meb-red) !important; }

    .result-card {
        background: white; padding: 30px; border-radius: 15px;
        border-top: 8px solid var(--meb-red); border-left: 8px solid var(--navy);
        box-shadow: 0 12px 30px rgba(0,0,0,0.1); margin-top: 20px;
    }
    
    .metric-box {
        padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #e2e8f0; background: #fdfdfd;
    }
    .metric-box span { display: block; font-size: 13px; font-weight: 800; color: #64748b; text-transform: uppercase; }
    .metric-box b { font-size: 28px; color: var(--navy); }

    .stButton>button {
        background: var(--navy); color: white; border-radius: 8px; font-weight: 800; height: 3.2em;
        transition: 0.3s; border: none; width: 100%;
    }
    .stButton>button:hover { background: var(--meb-red); transform: translateY(-2px); }
    </style>
""", unsafe_allow_html=True)

# --- BİRLEŞİK VE DERİN PEDAGOJİK ANALİZ MOTORU ---
# Bu fonksiyon hem bireysel hem toplu karnelerde noktası virgülüne aynı içeriği üretir.
def detayli_pedagojik_analiz(row):
    p, d, y, b, ad = row['Puan'], row['Doğru'], row['Yanlış'], row['Boş'], row['Ad']
    
    giris = f"Sevgili <b>{ad}</b>,<br><br>"
    felsefe = ("Matematik; sadece rakamlarla yapılan işlemler bütünü değil, evrenin karmaşık yapısını ve mantığını anlamamızı sağlayan en zarif dildir. "
               "Analitik düşünme becerisi, hayatta karşılaştığın her problemde sana en doğru yolu gösterecek olan bir pusuladır. "
               "Bu olimpiyat sınavına katılarak kendi sınırlarını keşfetme cesareti gösterdiğin için seni en içten dileklerimizle kutluyoruz.<br><br>")
    
    if p >= 85:
        durum = (f"<b>{p} puan</b> ile sergilediğin bu olağanüstü performans, matematiksel muhakeme gücünün olimpiyat düzeyinde olduğunu kanıtlıyor. "
                 f"Sınavdaki <b>{d} doğru</b> sayın, en karmaşık problemleri bile parçalara ayırarak çözümleyebildiğini gösteriyor. "
                 f"Yaptığın <b>{y} yanlış</b>, zirveye giden yolda sadece küçük birer nazar boncuğudur. Sen, analitik zekanı en üst seviyede kullanarak "
                 "geleceğin bilimsel dünyasında söz sahibi olabilecek bir potansiyele sahipsin. Asla rehavete kapılmadan, hep daha derinini merak etmeye devam et!")
    elif p >= 65:
        durum = (f"<b>{p} puan</b> alarak ne kadar güçlü bir matematik temeline sahip olduğunu kanıtladın. "
                 f"<b>{d} doğru</b> cevabın, temel kavramlara hakimiyetinin ve odaklanma becerinin yüksekliğine işaret ediyor. "
                 f"Yanlışların ve boşların <b>({y} Yanlış, {b} Boş)</b>, olimpiyat sorularındaki ince mantık tuzaklarına veya zaman baskısına yenik düştüğünü gösteriyor olabilir. "
                 "Hatalarını tek tek inceleyip 'nerede eksik düşündüm?' sorusunu kendine sorduğunda, zirveye yerleşmen an meselesidir. Kapasitene güven ve çalışmaktan vazgeçme!")
    elif p >= 40:
        durum = (f"<b>{p} puan</b> ile bu zorlu maratonda önemli bir direnç gösterdin. Olimpiyat seviyesindeki sorular, okul sınavlarından farklı bir bakış açısı gerektirir. "
                 f"<b>{b} soruyu boş bırakman</b>, aslında bir matematikçinin sahip olması gereken 'emin olmadığı riskten kaçınma' stratejisini doğru kullandığını gösteriyor. "
                 f"Ancak <b>{y} yanlışın</b>, mantık-muhakeme gerektiren konularda daha fazla pratiğe ihtiyacın olduğunu fısıldıyor. "
                 "Pes etmeden, hatalarının üzerine giderek ve bol bol yeni nesil soru çözerek bu potansiyeli çok daha yukarılara taşıyabilirsin. Sana inanıyoruz!")
    else:
        durum = (f"<b>{p} puan</b> almış olman senin yeteneğini değil, olimpiyat dünyasına attığın cesur ilk adımı temsil eder. "
                 "Unutma ki; büyük başarılar, hatalarından en çok ders çıkaranlardan gelir. "
                 f"Yaptığın <b>{y} yanlış</b> ve bıraktığın <b>{b} boş</b>; sana hangi konuları henüz 'tam keşfetmediğini' gösteren çok değerli birer yol haritasıdır. "
                 "Matematikte başarısızlık yoktur, sadece henüz öğrenilmemiş çözümler vardır. Şimdi bu hatalardan ders alıp daha güçlü bir hazırlıkla "
                 "matematiğin o keyifli dünyasını keşfetme zamanı. Biz senin her zaman yanındayız!")
    
    kapanis = "<br><br><b>Başarı yolculuğunda azmin en büyük gücün olsun. Yolun açık olsun!</b>"
    return giris + felsefe + durum + kapanis

# --- VERİ YÜKLEME ALTYAPISI ---
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
    st.markdown('<h3 style="color:#E30A17; text-align:center;">📊 KADEME SEÇİMİ</h3>', unsafe_allow_html=True)
    sinif_listesi = [f"{i}. Sınıf" for i in range(4, 13)]
    secilen_kademe_str = st.selectbox("Lütfen Sınıf Düzeyini Seçiniz:", sinif_listesi, index=3)
    kademe_no = secilen_kademe_str.split(".")[0]
    st.divider()
    st.info("💡 **Öğrenciler:** Sonucunuzu görmek için sınıfınızı, okulunuzu seçip numaranızı giriniz.\n\n💡 **İdareciler:** Tüm analiz ve liste raporları burada seçtiğiniz sınıfa göre hazırlanır.")

# Seçilen kademeye göre aktif veriyi belirle
df_aktif = df_tum[df_tum['Sınıf'] == kademe_no].copy() if not df_tum.empty else pd.DataFrame()

# --- ANA SEKMELER ---
tab_ogrenci, tab_idareci = st.tabs(["🎓 ÖĞRENCİ SONUÇ EKRANI", "🏛️ TOPLU SINAV SONUÇLARI"])

# ==============================================================================
# 2. BÖLÜM: ÖĞRENCİ GİRİŞİ, TABLOLU ÖN İZLEME VE PEDAGOJİK KARNE
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
                    
                    # 1. Bölümdeki ortak analiz motorunu çağırıyoruz! (Toplu karnede de aynı analiz kullanılacak)
                    analiz_html = detayli_pedagojik_analiz(o)
                    
                    # AŞAMA 1: TABLOLU ÖN İZLEME (Veri Okuryazarlığı Formatı)
                    st.markdown("#### 📊 Öğrenci Sonuç Veri Tablosu (Ön İzleme)")
                    gosterilecek_tablo = pd.DataFrame([o])[['Öğrenci No', 'Ad', 'Soyad', 'OKUL ADI', 'Sınıf', 'Şube', 'Doğru', 'Yanlış', 'Boş', 'Net', 'Puan', 'Okul Sırası', 'İlçe Sırası']]
                    st.dataframe(gosterilecek_tablo, use_container_width=True, hide_index=True)
                    
                    # AŞAMA 2: PROFESYONEL KARNE VE ANALİZ KARTI
                    st.markdown(f"""
                    <div class="result-card">
                        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:2px solid #e2e8f0; padding-bottom:15px;">
                            <div>
                                <h1 style="margin:0; color:#111827; font-size:32px;">{o['Ad']} {o['Soyad']}</h1>
                                <p style="margin:0; color:#E30A17; font-weight:800; font-size:18px;">{o['OKUL ADI']} - {o['Sınıf']}/{o['Şube']}</p>
                            </div>
                            <div style="background:#111827; color:white; padding:10px 20px; border-radius:8px; font-weight:bold; font-size:18px;">
                                No: {o['Öğrenci No']}
                            </div>
                        </div>
                        
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 15px; margin: 25px 0;">
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
                    
                    # AŞAMA 3: İNDİRİLEBİLİR BİREYSEL RESMİ PDF BELGESİ
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
# 3. BÖLÜM: TOPLU SINAV SONUÇLARI, KURUM RÖNTGENİ VE ANALİZ MERKEZİ
# ==============================================================================
with tab_idareci:
    st.markdown("### 🔐 Kurumsal Yetkili Yönetim Paneli")
    sifre = st.text_input("Yetkili Giriş Şifresi:", type="password")
    
    if sifre == "darder47":
        if df_tum.empty:
            st.error("Sistemde analiz edilecek sonuç verisi bulunamadı.")
        else:
            sub1, sub2, sub3, sub4 = st.tabs([
                "🏆 İLÇE GENEL BAŞARI RAPORU", 
                "📈 OKUL GELİŞİM RÖNTGENİ", 
                "📉 ŞUBE / ÖĞRETMEN ANALİZİ", 
                "📑 TOPLU LİSTELER VE DAĞITILACAK KARNELER"
            ])

            # -----------------------------------------------------
            # ALT SEKME 1: İLÇE GENEL BAŞARI RAPORU
            # -----------------------------------------------------
            with sub1:
                st.markdown(f"#### 🏢 {secilen_kademe_str} İlçe Geneli Toplu Sınav Sonuçları")
                
                if df_aktif.empty:
                    st.warning("Bu sınıf düzeyinde veri bulunmamaktadır.")
                else:
                    c_m1, c_m2, c_m3, c_m4 = st.columns(4)
                    with c_m1: st.markdown(f"<div class='metric-box'><span>Toplam Öğrenci</span><b>{len(df_aktif)}</b></div>", unsafe_allow_html=True)
                    with c_m2: st.markdown(f"<div class='metric-box'><span>Kurum Sayısı</span><b>{df_aktif['OKUL ADI'].nunique()}</b></div>", unsafe_allow_html=True)
                    with c_m3: st.markdown(f"<div class='metric-box'><span>İlçe Puan Ort.</span><b>{df_aktif['Puan'].mean():.2f}</b></div>", unsafe_allow_html=True)
                    with c_m4: st.markdown(f"<div class='metric-box'><span>İlçe Net Ort.</span><b style='color:#E30A17;'>{df_aktif['Net'].mean():.2f}</b></div>", unsafe_allow_html=True)
                    
                    df_okul_genel = df_aktif.groupby('OKUL ADI').agg(Ogr_Sayisi=('Puan', 'count'), Ort_Puan=('Puan', 'mean')).reset_index()
                    
                    st.markdown("<br>##### 📊 Kurumlar Arası Başarı Kıyaslaması", unsafe_allow_html=True)
                    fig = px.bar(df_okul_genel.sort_values(by='Ort_Puan', ascending=True), 
                                 x='Ort_Puan', y='OKUL ADI', orientation='h', text_auto='.2f', 
                                 color='Ort_Puan', color_continuous_scale='Reds')
                    fig.update_layout(height=500, xaxis_title="Puan Ortalaması", yaxis_title="")
                    st.plotly_chart(fig, use_container_width=True)

            # -----------------------------------------------------
            # ALT SEKME 2: OKUL GELİŞİM RÖNTGENİ
            # -----------------------------------------------------
            with sub2:
                st.markdown(f"#### 📈 {secilen_kademe_str} Kurum Röntgeni ve Gelişim Raporu")
                
                if df_aktif.empty:
                    st.warning("Veri bulunamadı.")
                else:
                    secilen_kurum = st.selectbox("Analizi Yapılacak Okul:", sorted(df_aktif['OKUL ADI'].unique()), key="gelisim_okul")
                    
                    df_kurum_gelisim = df_aktif[df_aktif['OKUL ADI'] == secilen_kurum]
                    ilce_ort = df_aktif['Puan'].mean()
                    okul_ort = df_kurum_gelisim['Puan'].mean()
                    toplam_ogrenci = len(df_kurum_gelisim)
                    
                    # Şube bazlı röntgen
                    df_subeler = df_kurum_gelisim.groupby('Şube').agg(Mevcut=('Puan', 'count'), Sube_Ort_Puan=('Puan', 'mean')).reset_index().sort_values(by='Sube_Ort_Puan', ascending=False)
                    
                    # Dinamik rapor metni (1. Bölümdeki fonksiyonu kullanır)
                    fark = okul_ort - ilce_ort
                    durum_renk = "#059669" if fark >= 0 else "#E30A17"
                    
                    st.markdown(f"""
                    <div style="background:white; padding:25px; border-radius:12px; border-left:10px solid {durum_renk}; box-shadow:0 5px 15px rgba(0,0,0,0.05);">
                        <h3 style="margin-top:0;">{secilen_kurum} Gelişim Analizi</h3>
                        <p style="font-size:16px;">Okul Ortalaması: <b>{okul_ort:.2f}</b> | İlçe Ortalaması: <b>{ilce_ort:.2f}</b></p>
                        <hr>
                        <p style="text-align:justify; line-height:1.6;">Okulunuzdaki <b>{toplam_ogrenci}</b> öğrencinin verileri analiz edildiğinde, ilçe geneline göre akademik duruşunuz 
                        belirlenmiştir. Bu rapor, sadece bir sıralama değil; sınıflar arası pedagojik aktarımı güçlendirmek için bir yol haritasıdır.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.write("##### 🔍 Şube Bazlı Başarı Röntgeni")
                    st.table(df_subeler)

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
                    st.plotly_chart(fig3, use_container_width=True)

            # -----------------------------------------------------
            # ALT SEKME 4: TOPLU LİSTELER VE DAĞITILACAK KARNELER
            # -----------------------------------------------------
            with sub4:
                st.markdown(f"#### 📑 {secilen_kademe_str} Dağıtılacak Toplu Karneler ve Listeler")
                st.info("Bu bölümden, her öğrenci için bireysel sorgulama ekranındaki analizlerin aynısını içeren toplu karne dökümü alabilirsiniz.")
                
                kurum_secim = st.selectbox("İşlem Yapılacak Okulu Seçin:", ["Tüm İlçe Listesi"] + sorted(df_aktif['OKUL ADI'].unique()), key="toplu_karne_okul")
                df_filtre = df_aktif if kurum_secim == "Tüm İlçe Listesi" else df_aktif[df_aktif['OKUL ADI'] == kurum_secim]
                
                st.dataframe(df_filtre[['İlçe Sırası', 'Okul Sırası', 'OKUL ADI', 'Sınıf', 'Şube', 'Öğrenci No', 'Ad', 'Soyad', 'Net', 'Puan']], use_container_width=True)
                
                c_btn1, c_btn2 = st.columns(2)
                
                # 1. TOPLU LİSTE (PDF)
                pdf_liste_html = f"""
                <html><head><meta charset="utf-8"><style>
                    body {{ font-family: 'Segoe UI', Tahoma, sans-serif; }}
                    .h {{ text-align: center; border-bottom: 2px solid #111827; margin-bottom: 20px; }}
                    table {{ width: 100%; border-collapse: collapse; text-align: center; font-size: 12px; }}
                    th {{ background: #111827; color: white; padding: 8px; }}
                    td {{ border: 1px solid #ddd; padding: 6px; }}
                </style></head><body>
                    <div class="h"><h2>{kurum_secim} - {kademe_no}. SINIF TOPLU BAŞARI LİSTESİ</h2></div>
                    <table><tr><th>İlçe S.</th><th>Okul S.</th><th>Ad Soyad</th><th>Sınıf/Şube</th><th>No</th><th>Net</th><th>Puan</th></tr>
                """
                for _, r in df_filtre.iterrows():
                    pdf_liste_html += f"<tr><td>{r.get('İlçe Sırası','-')}</td><td>{r.get('Okul Sırası','-')}</td><td>{r['Ad']} {r['Soyad']}</td><td>{r['Sınıf']}/{r['Şube']}</td><td>{r['Öğrenci No']}</td><td>{r['Net']}</td><td style='font-weight:bold;'>{r['Puan']}</td></tr>"
                pdf_liste_html += "</table></body></html>"
                
                c_btn1.download_button("📊 Toplu Başarı Listesini İndir (PDF)", data=pdf_liste_html, file_name=f"{kurum_secim}_Liste.html", mime="text/html")

                # 2. TOPLU KARNE DAĞITIMI (Bireysel ile Birebir Aynı Analizler)
                html_toplu_karne = """
                <html><head><meta charset="utf-8"><style>
                    @page { size: A4 portrait; margin: 10mm; }
                    body { font-family: 'Segoe UI', Tahoma, sans-serif; margin: 0; padding: 0; background: white; }
                    .page { width: 190mm; display: flex; flex-direction: column; gap: 8mm; page-break-after: always; }
                    .karne { width: 100%; height: 88mm; border: 3px solid #E30A17; border-radius: 15px; padding: 15px; position: relative; page-break-inside: avoid; display: flex; flex-direction: column; justify-content: space-between; }
                    .baslik { text-align: center; font-weight: 900; font-size: 15px; border-bottom: 3px solid #E30A17; padding-bottom: 5px; text-transform: uppercase; }
                    .kimlik { display: flex; justify-content: space-between; font-weight: 900; font-size: 13px; margin-top: 8px; }
                    .sira { text-align: center; background: #111827; color: white; padding: 5px; border-radius: 6px; font-size: 11px; margin: 8px 0; }
                    .stats { width: 100%; border-collapse: collapse; text-align: center; font-size: 12px; }
                    .stats th { background: #fef2f2; border: 1px solid #fca5a5; padding: 5px; color: #E30A17; }
                    .stats td { border: 1px solid #fca5a5; padding: 6px; font-weight: 900; font-size: 15px; }
                    .analiz { background: #f8fafc !important; border-left: 5px solid #E30A17; padding: 10px; font-size: 10px; line-height: 1.4; text-align: justify; border-radius: 5px; border: 1px solid #e2e8f0; color: #111827; }
                </style></head><body>
                """
                
                for i, row in df_filtre.reset_index().iterrows():
                    if i % 3 == 0: html_toplu_karne += "<div class='page'>"
                    
                    # BİREBİR AYNI ANALİZ MOTORU KULLANILIYOR
                    analiz_metni = detayli_pedagojik_analiz(row)
                    
                    html_toplu_karne += f"""
                    <div class="karne">
                        <div>
                            <div class="baslik">T.C. DARGEÇİT KAYMAKAMLIĞI - MATEMATİK OLİMPİYATI SONUÇ BELGESİ</div>
                            <div class="kimlik"><span>{row['Ad']} {row['Soyad']}</span><span style="color:#E30A17;">No: {row['Öğrenci No']}</span></div>
                            <div class="kimlik" style="color:#555; font-size:11px; margin-top:2px;"><span>{row['OKUL ADI']}</span><span>Sınıf: {row['Sınıf']}/{row['Şube']}</span></div>
                            <div class="sira">İlçe Sırası: {row.get('İlçe Sırası','-')} &nbsp;|&nbsp; Okul Sırası: {row.get('Okul Sırası','-')}</div>
                            
                            <table class="stats">
                                <tr><th>Doğru</th><th>Yanlış</th><th>Boş</th><th>Net</th><th style="background:#E30A17; color:white;">PUAN</th></tr>
                                <tr><td style="color:#059669;">{row['Doğru']}</td><td style="color:#E30A17;">{row['Yanlış']}</td><td>{row['Boş']}</td><td style="color:#2563eb;">{row['Net']}</td><td style="background:#111827 !important; color:white;">{row['Puan']}</td></tr>
                            </table>
                        </div>
                        <div class="analiz">
                            <b style="color:#E30A17; font-size:11px;">🎓 Detaylı Pedagojik Değerlendirme:</b><br>{analiz_metni}
                        </div>
                    </div>
                    """
                    if (i + 1) % 3 == 0 or i == len(df_filtre) - 1: html_toplu_karne += "</div>"
                
                html_toplu_karne += "</body></html>"
                
                c_btn2.download_button("🖨️ Dağıtılacak Toplu Karneleri Al (PDF)", data=html_toplu_karne, file_name=f"{kurum_secim}_Dagitmaya_Hazir_Karneler.html", mime="text/html")

    elif sifre != "":
        st.error("❌ Yetkisiz Erişim: Şifre Hatalı!")
