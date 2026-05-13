import streamlit as st
import pandas as pd
import io
import os
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
    * { -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }

    .header-banner {
        background: linear-gradient(to right, #ffffff, #fef2f2);
        padding: 25px; border-bottom: 6px solid var(--meb-red);
        border-radius: 12px; margin-bottom: 25px; text-align: center;
        box-shadow: 0 4px 15px rgba(227, 10, 23, 0.1);
    }
    .header-banner h1 { color: var(--navy); font-weight: 900; font-size: 32px; margin: 0; }
    .header-banner h3 { color: var(--meb-red); font-weight: 800; font-size: 18px; margin-top: 5px; text-transform: uppercase; }
    
    .stTabs [data-baseweb="tab-list"] { gap: 20px; border-bottom: 2px solid #e2e8f0; }
    .stTabs [data-baseweb="tab"] { height: 50px; background: white; border-radius: 8px 8px 0 0; font-weight: 800; font-size: 16px; border: 1px solid #e2e8f0; border-bottom: none; }
    .stTabs [aria-selected="true"] { background: var(--navy) !important; color: white !important; border-bottom: 4px solid var(--meb-red); }
    
    .metric-kutu { background: white; border-radius: 10px; padding: 20px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; border-top: 4px solid var(--navy); }
    .metric-kutu h2 { margin: 0; color: var(--meb-red); font-size: 36px; font-weight: 900; }
    .metric-kutu p { margin: 0; color: #64748b; font-size: 13px; font-weight: 900; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# --- DETAYLI PEDAGOJİK ÖĞRENCİ ANALİZ MOTORU ---
def profesyonel_analiz(row):
    p, d, y, b, ad = row['Puan'], row['Doğru'], row['Yanlış'], row['Boş'], row['Ad']
    if p >= 85:
        return f"Üstün yetenekli {ad}! Matematiksel muhakeme gücünün olimpiyat düzeyinde olduğunu kanıtladın. {d} doğru gibi muazzam bir sayıya ulaşman, problem çözme stratejilerindeki ustalığını gösteriyor. Bu zirveyi koruman dileğiyle, tebrik ederiz."
    elif p >= 65:
        return f"Tebrikler {ad}! Çok başarılı bir performans sergiledin. Temel kavramlara ve işlemlere hakimiyetin oldukça yüksek. Yaptığın {y} yanlış, ufak dikkatsizliklerin habercisi. Biraz daha pratik yaparak mükemmele ulaşman an meselesi."
    elif p >= 40:
        return f"Gayretin ve azmin için tebrikler {ad}. Temel düzeydeki matematik becerilerin gelişmiş olsa da, yeni nesil mantık sorularında tecrübe kazanman gerekiyor. {b} boşun olması risk almadığını gösteriyor. Bol soru çözerek bu açığı rahatlıkla kapatabilirsin."
    else:
        return f"Bu zorlu sınav, senin için çok değerli bir tecrübe oldu {ad}. Olimpiyat düzeyindeki sorular her zaman zordur. Yanlış yaptığın konuları tespit edip üzerine gitmeli, bu sonuçtan ders çıkararak azmini asla kaybetmemelisin. Biz sana inanıyoruz!"

# --- PROFESYONEL OKUL GELİŞİM RAPORU METNİ OLUŞTURUCU ---
def okul_gelisim_metni(okul_adi, okul_ort, ilce_ort):
    fark = okul_ort - ilce_ort
    if fark > 5:
        durum = f"İlçe ortalamasının ({ilce_ort:.2f}) belirgin bir şekilde üzerine çıkarak <b>{okul_ort:.2f}</b> puan ortalaması ile üstün bir gayret sergilemiştir."
        tavsiye = "Bu yüksek ivmeyi korumak için ileri düzey mantık-muhakeme sorularına ağırlık verilmesi ve yetenekli öğrencilerin olimpiyat seviyesi kaynaklarla desteklenmesi önerilmektedir. Liderliğiniz ve özveriniz için teşekkür ederiz."
    elif fark > -5:
        durum = f"İlçe ortalaması ({ilce_ort:.2f}) ile paralel bir başarı göstererek <b>{okul_ort:.2f}</b> puan ortalamasına ulaşmıştır."
        tavsiye = "Kıymetli öğretmenlerimizin çabaları takdire şayandır. Ortalamayı daha da yükseltmek için temel kazanım eksikliklerinin tespit edilip, yeni nesil sorulara yönelik periyodik etüt çalışmaları yapılması faydalı olacaktır."
    else:
        durum = f"Olimpiyat sınavının zorlayıcı yapısı neticesinde, ilçe ortalamasının ({ilce_ort:.2f}) bir miktar gerisinde kalarak <b>{okul_ort:.2f}</b> puan ortalaması elde etmiştir."
        tavsiye = "Öğretmenlerimizin özverili çalışmaları çok değerlidir. Sınav heyecanı veya tecrübe eksikliği bu sonuca etki etmiş olabilir. Öğrencilerimizi demotive etmeden, temel okuryazarlığı artıracak teşvik edici faaliyetlerle bu açığın hızla kapatılacağına inancımız tamdır. Kurumunuzun yanındayız."
    
    return f"""Saygıdeğer <b>{okul_adi}</b> İdarecileri ve Kıymetli Öğretmenlerimiz,<br><br>
    Eğitimdeki en büyük gücümüz, sizlerin öğrencilere dokunan vizyoner elleridir. Okulunuz, katıldığı bu olimpiyat sınavında {durum} {tavsiye}<br><br>
    Aşağıda sunulan şube analizlerini bir rekabet unsuru olarak değil, "hangi sınıfımıza daha fazla pedagojik destek olmalıyız?" sorusunun bir rehberi olarak değerlendirmenizi rica ederiz."""

# --- BANNER ---
st.markdown("""
    <div class="header-banner">
        <h1>🥇 1. DARGEÇİT MATEMATİK OLİMPİYATI</h1>
        <h3>Sınav Sonuç, Okul Gelişim ve Raporlama Portalı</h3>
    </div>
""", unsafe_allow_html=True)

# --- TÜM VERİLERİ YÜKLEME ---
@st.cache_data
def verileri_yukle():
    dosyalar = glob.glob("sonuclar_*.xlsx")
    liste = []
    for d in dosyalar:
        try:
            df = pd.read_excel(d)
            if 'Puan' in df.columns and 'Öğrenci No' in df.columns:
                df['Arama_No'] = df['Öğrenci No'].astype(str).str.lstrip('0').str.split('.').str[0]
                df['Sınıf'] = df['Sınıf'].astype(str).str.replace('.0', '', regex=False)
                liste.append(df)
        except: pass
    if liste:
        birlestirilmis = pd.concat(liste, ignore_index=True)
        return birlestirilmis.sort_values(by=['Puan', 'Net'], ascending=[False, False]).reset_index(drop=True)
    return pd.DataFrame()

df_tum = verileri_yukle()

# --- YAN MENÜ ---
with st.sidebar:
    st.markdown('<h3 style="color:#E30A17; text-align:center;">⬇️ KADEME SEÇİMİ</h3>', unsafe_allow_html=True)
    siniflar = [f"{i}. Sınıf" for i in range(4, 13)]
    secilen_kademe_str = st.selectbox("İşlem yapılacak sınıf düzeyini seçiniz:", siniflar, index=3)
    kademe_no = secilen_kademe_str.split(".")[0]
    st.divider()
    st.info("💡 **Öğrenciler:** Sınıfınızı seçip sonuçlarınıza ulaşabilirsiniz.\n\n💡 **İdareciler:** Sınıf bazlı tüm raporlar için bu menüyü kullanın.")

# Aktif sınıfın verisini filtrele
df_aktif = df_tum[df_tum['Sınıf'] == kademe_no].copy() if not df_tum.empty else pd.DataFrame()

# --- ANA SEKMELER ---
tab_ogrenci, tab_idareci = st.tabs(["👤 ÖĞRENCİ KARNE SORGULAMA", "🏫 İDARECİ VE RAPORLAMA PANELİ"])

# ==============================================================================
# 1. ÖĞRENCİ GİRİŞİ 
# ==============================================================================
with tab_ogrenci:
    if df_aktif.empty:
        st.warning(f"⚠️ Sisteme henüz {secilen_kademe_str} sonuçları yüklenmemiştir.")
    else:
        st.markdown(f"### 🔍 {secilen_kademe_str} Sınav Sonucunu Öğren")
        col1, col2 = st.columns(2)
        with col1:
            okul_secim = st.selectbox("Okulunuz:", sorted(df_aktif['OKUL ADI'].dropna().unique()), key="ogr_okul")
        with col2:
            no_secim = st.text_input("Öğrenci Numaranız:", key="ogr_no").lstrip('0')
            
        if st.button("Karnemi Görüntüle", type="primary"):
            sonuc = df_aktif[(df_aktif['OKUL ADI'] == okul_secim) & (df_aktif['Arama_No'] == no_secim)]
            if not sonuc.empty:
                st.balloons()
                o = sonuc.iloc[0]
                
                st.markdown(f"""
                <div style="background:white; padding:35px; border-radius:15px; border-top:8px solid #E30A17; box-shadow:0 10px 30px rgba(0,0,0,0.1);">
                    <h2 style="color:#111827; margin:0; font-size: 28px;">{o['Ad']} {o['Soyad']}</h2>
                    <p style="color:#555; font-size:18px; margin-bottom:15px;"><b>{o['OKUL ADI']}</b> | Sınıf: {o['Sınıf']}/{o['Şube']} | No: <b>{o['Öğrenci No']}</b></p>
                    
                    <div style="display:flex; gap:10px; margin-bottom:25px;">
                        <span style="background:#111827; color:white; padding:8px 15px; border-radius:5px; font-weight:bold;">İlçe Sırası: {o.get('İlçe Sırası', '-')}</span>
                        <span style="background:#E30A17; color:white; padding:8px 15px; border-radius:5px; font-weight:bold;">Okul Sırası: {o.get('Okul Sırası', '-')}</span>
                    </div>
                    
                    <div style="display:grid; grid-template-columns: repeat(5, 1fr); gap:15px; text-align:center;">
                        <div style="background:#f1f5f9; padding:15px; border-radius:10px; border:1px solid #e2e8f0;"><span>Doğru</span><br><b style="font-size:26px; color:#059669;">{o['Doğru']}</b></div>
                        <div style="background:#fef2f2; padding:15px; border-radius:10px; border:1px solid #fca5a5;"><span>Yanlış</span><br><b style="font-size:26px; color:#E30A17;">{o['Yanlış']}</b></div>
                        <div style="background:#f1f5f9; padding:15px; border-radius:10px; border:1px solid #e2e8f0;"><span>Boş</span><br><b style="font-size:26px; color:#64748b;">{o['Boş']}</b></div>
                        <div style="background:#eff6ff; padding:15px; border-radius:10px; border:1px solid #bfdbfe;"><span>Net</span><br><b style="font-size:26px; color:#2563eb;">{o['Net']}</b></div>
                        <div style="background:#111827; padding:15px; border-radius:10px; color:white;"><span>Puan</span><br><b style="font-size:30px; font-weight:900;">{o['Puan']}</b></div>
                    </div>
                    
                    <div style="margin-top:25px; padding:20px; background:#fff5f5; border-left:6px solid #E30A17; border-radius:8px;">
                        <p style="margin:0; font-size: 16px; line-height: 1.6; color:#111827;"><b>🎓 Pedagojik Analiz:</b><br>{profesyonel_analiz(o)}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("❌ Kayıt bulunamadı. Lütfen okulunuzu ve numaranızı kontrol edin.")

# ==============================================================================
# 2. İDARECİ GİRİŞİ (Okul Gelişim Raporları, Alt Alta Karneler vb.)
# ==============================================================================
with tab_idareci:
    st.markdown("### 🔐 Kurumsal Yönetim, Gelişim ve Raporlama Paneli")
    sifre = st.text_input("Yetkili Giriş Şifresi:", type="password")
    
    if sifre == "darder47":
        if df_tum.empty:
            st.error("Sistemde analiz edilecek hiçbir veri yok.")
        else:
            sub1, sub2, sub3, sub4 = st.tabs([
                "🏆 İLÇE GENEL RAPORU", 
                "📈 OKUL GELİŞİM RAPORU", 
                "📉 ŞUBE / ÖĞRETMEN ANALİZİ", 
                "📑 ÖĞRENCİ KARNELERİ VE LİSTELER"
            ])

            # -----------------------------------------------------
            # ALT SEKME 1: İLÇE GENEL RAPORU
            # -----------------------------------------------------
            with sub1:
                st.markdown("#### 🏢 İlçe Geneli Okul Başarı Sıralaması (Tüm Sınıflar Karışık)")
                
                c_m1, c_m2, c_m3, c_m4 = st.columns(4)
                with c_m1: st.markdown(f"<div class='metric-kutu'><p>Sınava Giren Öğrenci</p><h2>{len(df_tum)}</h2></div>", unsafe_allow_html=True)
                with c_m2: st.markdown(f"<div class='metric-kutu'><p>Katılımcı Okul Sayısı</p><h2>{df_tum['OKUL ADI'].nunique()}</h2></div>", unsafe_allow_html=True)
                with c_m3: st.markdown(f"<div class='metric-kutu'><p>İlçe Puan Ortalaması</p><h2>{df_tum['Puan'].mean():.2f}</h2></div>", unsafe_allow_html=True)
                with c_m4: st.markdown(f"<div class='metric-kutu'><p>İlçe Net Ortalaması</p><h2 style='color:#111827;'>{df_tum['Net'].mean():.2f}</h2></div>", unsafe_allow_html=True)
                
                df_okul_genel = df_tum.groupby('OKUL ADI').agg(Ogr_Sayisi=('Puan', 'count'), Ort_Puan=('Puan', 'mean')).reset_index().sort_values(by='Ort_Puan', ascending=False)
                
                fig = px.bar(df_okul_genel.sort_values(by='Ort_Puan', ascending=True), x='Ort_Puan', y='OKUL ADI', orientation='h', text_auto='.2f', color='Ort_Puan', color_continuous_scale='Reds', title="İlçe Geneli Puan Sıralaması")
                fig.update_layout(height=600, xaxis_title="Puan Ortalaması", yaxis_title="")
                st.plotly_chart(fig, use_container_width=True)

            # -----------------------------------------------------
            # ALT SEKME 2: YENİ! OKUL GELİŞİM RAPORU (Pedagojik Okul Analizi)
            # -----------------------------------------------------
            with sub2:
                st.markdown(f"#### 📈 {secilen_kademe_str} Kurum Gelişim Raporu")
                st.write("Seçtiğiniz okula özel; ilçe durumu, öğretmenleri teşvik eden yapıcı pedagojik analizler ve şube ortalamalarının yer aldığı resmi bir PDF gelişim raporu hazırlar.")
                
                if df_aktif.empty:
                    st.warning("Bu kademede veri bulunmamaktadır.")
                else:
                    secilen_kurum = st.selectbox("Gelişim Raporu Çıkarılacak Okul:", sorted(df_aktif['OKUL ADI'].unique()), key="gelisim_okul")
                    
                    df_kurum_gelisim = df_aktif[df_aktif['OKUL ADI'] == secilen_kurum]
                    ilce_ort = df_aktif['Puan'].mean()
                    okul_ort = df_kurum_gelisim['Puan'].mean()
                    
                    df_subeler = df_kurum_gelisim.groupby('Şube').agg(Mevcut=('Puan', 'count'), Sube_Ort_Puan=('Puan', 'mean')).reset_index().sort_values(by='Sube_Ort_Puan', ascending=False)
                    
                    metin = okul_gelisim_metni(secilen_kurum, okul_ort, ilce_ort)
                    
                    st.info(f"Rapor Önizlemesi: {secilen_kurum} okulunun ortalaması {okul_ort:.2f} olarak hesaplandı.")
                    
                    # OKUL GELİŞİM RAPORU PDF ŞABLONU
                    gelisim_html = f"""
                    <html><head><meta charset="utf-8"><style>
                        @page {{ size: A4 portrait; margin: 15mm; }}
                        body {{ font-family: 'Segoe UI', Tahoma, sans-serif; margin: 0; padding: 0; color: #111827; -webkit-print-color-adjust: exact !important; }}
                        .baslik-alan {{ text-align: center; border-bottom: 5px solid #111827; padding-bottom: 15px; margin-bottom: 25px; }}
                        .baslik-alan h1 {{ margin: 0; font-size: 22px; font-weight: 900; }}
                        .baslik-alan h2 {{ margin: 5px 0 0 0; color: #E30A17; font-size: 16px; font-weight: bold; }}
                        .bilgi-serit {{ display: flex; justify-content: space-between; background: #fef2f2; border: 1px solid #fca5a5; padding: 15px; border-radius: 8px; margin-bottom: 20px; font-weight: bold; }}
                        .analiz-metni {{ font-size: 14px; line-height: 1.6; text-align: justify; margin-bottom: 30px; }}
                        .tablo-alan {{ width: 100%; border-collapse: collapse; text-align: center; margin-bottom: 30px; }}
                        .tablo-alan th {{ background: #111827; color: white; padding: 10px; border: 1px solid #111827; }}
                        .tablo-alan td {{ padding: 10px; border: 1px solid #cbd5e1; font-weight: bold; }}
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
                        gelisim_html += f"<tr><td>{s_row['Şube']}</td><td>{s_row['Mevcut']}</td><td style='color:#E30A17; font-size:16px;'>{s_row['Sube_Ort_Puan']:.2f}</td></tr>"
                    
                    gelisim_html += """
                        </table>
                        <div style="font-size: 12px; color: #64748b; text-align: center; margin-top: 50px;">
                            Dargeçit İlçe Milli Eğitim Müdürlüğü - Matematik Olimpiyatı Ölçme Değerlendirme Merkezi
                        </div>
                    </body></html>
                    """
                    
                    st.download_button("🖨️ Kurum Gelişim Raporunu İndir (PDF)", data=gelisim_html, file_name=f"{secilen_kurum}_Gelisim_Raporu.html", mime="text/html", type="primary")

            # -----------------------------------------------------
            # ALT SEKME 3: ŞUBE VE ÖĞRETMEN ANALİZİ
            # -----------------------------------------------------
            with sub3:
                st.markdown(f"#### 📉 {secilen_kademe_str} Şube ve Öğretmen Analizi")
                if df_aktif.empty:
                    st.warning("Bu sınıf düzeyinde veri yok.")
                else:
                    c_g1, c_g2 = st.columns(2)
                    with c_g1:
                        st.markdown("**Okul Ortalamaları Kıyaslaması**")
                        df_okul_sinif = df_aktif.groupby('OKUL ADI')['Puan'].mean().reset_index().sort_values(by='Puan', ascending=True)
                        fig2 = px.bar(df_okul_sinif, x='Puan', y='OKUL ADI', orientation='h', text_auto='.2f', color='Puan', color_continuous_scale='Blues')
                        st.plotly_chart(fig2, use_container_width=True)
                    with c_g2:
                        st.markdown("**En Başarılı Şubeler (Sınıf İçi Rekabet)**")
                        df_sube_genel = df_aktif.groupby(['OKUL ADI', 'Şube']).agg(Ogr=('Puan', 'count'), Puan_Ort=('Puan', 'mean')).reset_index()
                        df_sube_genel = df_sube_genel[df_sube_genel['Ogr'] >= 3].sort_values(by='Puan_Ort', ascending=True).tail(15)
                        df_sube_genel['Sube_Ad'] = df_sube_genel['OKUL ADI'] + " - " + df_sube_genel['Şube']
                        fig3 = px.bar(df_sube_genel, x='Puan_Ort', y='Sube_Ad', orientation='h', text_auto='.2f', color='Puan_Ort', color_continuous_scale='Teal')
                        st.plotly_chart(fig3, use_container_width=True)

            # -----------------------------------------------------
            # ALT SEKME 4: ALT ALTA (TAM GENİŞLİK) KARNELER VE LİSTELER
            # -----------------------------------------------------
            with sub4:
                st.markdown(f"#### 📑 {secilen_kademe_str} Listeler ve ALT ALTA Mükemmel PDF Karneler")
                if df_aktif.empty:
                    st.warning("Veri yok.")
                else:
                    kurum_secim = st.selectbox("İşlem Yapılacak Okulu Seçin:", ["Tüm İlçe"] + sorted(df_aktif['OKUL ADI'].unique()), key="k_karne")
                    df_filtre = df_aktif if kurum_secim == "Tüm İlçe" else df_aktif[df_aktif['OKUL ADI'] == kurum_secim]
                    
                    st.dataframe(df_filtre[['İlçe Sırası', 'Okul Sırası', 'Sınıf', 'Şube', 'Öğrenci No', 'Ad', 'Soyad', 'Net', 'Puan']], use_container_width=True)
                    
                    c_btn1, c_btn2 = st.columns(2)
                    
                    # 1. EXCEL LİSTE
                    buf_ex = io.BytesIO()
                    with pd.ExcelWriter(buf_ex, engine='openpyxl') as writer:
                        df_filtre.to_excel(writer, index=False)
                    c_btn1.download_button("📊 1) Okul Listesini Excel Olarak İndir", data=buf_ex.getvalue(), file_name=f"{kurum_secim}_Liste.xlsx", use_container_width=True)

                    # 2. ALT ALTA (TAM GENİŞLİK) KIRMIZI KONSEPT KUSURSUZ KARNELER (1 Sayfada 3 Adet)
                    html_karne = """
                    <html><head><meta charset="utf-8"><style>
                        @page { size: A4 portrait; margin: 10mm; }
                        * { box-sizing: border-box; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
                        body { font-family: 'Segoe UI', Tahoma, sans-serif; margin: 0; padding: 0; color: #111827; background: white; }
                        
                        /* A4 Sayfası - Flex ile Alt Alta (Tek Sütun) Dizilim */
                        .page { width: 190mm; height: 277mm; display: flex; flex-direction: column; gap: 8mm; page-break-after: always; justify-content: flex-start; }
                        
                        /* Karne Kutusu: Tam Genişlik, Boşluksuz */
                        .karne { 
                            width: 100%; height: 86mm; border: 2.5px solid #E30A17; border-radius: 12px; 
                            padding: 10px 15px; display: flex; flex-direction: column; justify-content: space-between;
                            background: white; overflow: hidden; position: relative;
                        }
                        
                        .baslik { color: #111827; text-align: center; font-weight: 900; font-size: 14px; border-bottom: 3px solid #E30A17; padding-bottom: 5px; text-transform: uppercase; letter-spacing: 0.5px; }
                        .kimlik-satir { display: flex; justify-content: space-between; font-weight: 900; font-size: 13px; margin-top: 6px; }
                        .sira-kutu { text-align: center; background: #E30A17; color: white; padding: 4px; border-radius: 6px; font-size: 11px; font-weight: bold; margin-top: 6px; }
                        
                        .stats-tablo { width: 100%; border-collapse: collapse; text-align: center; font-size: 12px; margin-top: 6px; }
                        .stats-tablo th { background: #fef2f2; border: 1px solid #fca5a5; padding: 4px; color: #E30A17; }
                        .stats-tablo td { border: 1px solid #fca5a5; padding: 5px; font-weight: 900; font-size: 14px; }
                        
                        .optik-tablo { width: 100%; border-collapse: collapse; text-align: center; font-size: 10px; margin-top: 6px; table-layout: fixed; }
                        .optik-tablo th, .optik-tablo td { border: 1px solid #fca5a5; height: 18px; overflow: hidden; font-weight: bold; }
                        .optik-tablo th { background: #fef2f2; color: #E30A17; }
                        .dogru { background: #dcfce7 !important; color: #059669 !important; font-weight: 900; }
                        .yanlis { background: #111827 !important; color: white !important; font-weight: 900; } /* Yanlışlar Siyah Çarpıcı */
                        
                        .analiz-kutu { 
                            background: #f8fafc !important; border-left: 5px solid #E30A17; padding: 8px 10px; 
                            font-size: 10px; line-height: 1.4; font-style: italic; font-weight: 600; text-align: justify;
                            margin-top: 6px; color: #111827; border-radius: 4px;
                        }
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

                        # Kısa Yorum
                        p_val = row['Puan']
                        if p_val >= 85: k_yr = "Üstün yetenek. 2. Aşamada başarılar!"
                        elif p_val >= 65: k_yr = "Çok başarılı, ufak eksiklerini kapatırsan mükemmel olur."
                        elif p_val >= 40: k_yr = "Temelin sağlam, bol pratikle netlerin çok daha yükselecek."
                        else: k_yr = "Asla pes etme, eksiklerini tamamla."

                        html_karne += f"""
                        <div class="karne">
                            <div>
                                <div class="baslik">T.C. DARGEÇİT KAYMAKAMLIĞI - 1. MATEMATİK OLİMPİYATI SONUÇ BELGESİ</div>
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
                            <div class="analiz-kutu"><b>Analiz Özeti:</b> {k_yr}</div>
                        </div>
                        """
                        if (i + 1) % 3 == 0 or i == len(df_filtre) - 1: html_karne += "</div>"
                    
                    html_karne += "</body></html>"
                    c_btn2.download_button("🖨️ 2) Karneleri İndir (Alt Alta Tam Genişlik - PDF)", data=html_karne, file_name=f"{kurum_secim}_ALT_ALTA_Karneler.html", mime="text/html", use_container_width=True)
                    st.info("💡 PDF ayarları: Tarayıcıda açıp Ctrl+P yaptığınızda 'Kenar Boşlukları: Yok' seçeneğini işaretlemeyi unutmayın. Sayfada yan yana değil, alt alta 3 tane büyük karne göreceksiniz.")
    elif sifre != "":
        st.error("Hatalı Şifre!")
