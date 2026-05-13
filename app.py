import streamlit as st
import pandas as pd
import io
import ast
import os
import plotly.express as px

# ==========================================
# 1. BÖLÜM: AYARLAR, CSS VE ANALİZ MOTORLARI
# ==========================================
st.set_page_config(page_title="1. Dargeçit Matematik Olimpiyatı", layout="wide", page_icon="🥇")

st.markdown("""
    <style>
    :root { --meb-red: #E30A17; --navy: #111827; --light-bg: #f8fafc; --card-bg: #ffffff; }
    .main { background-color: var(--light-bg); }
    .header-banner { background: linear-gradient(135deg, #E30A17 0%, #990000 100%); padding: 25px 15px; border-radius: 0 0 20px 20px; margin: -60px -15px 25px -15px; text-align: center; box-shadow: 0 8px 20px rgba(227, 10, 23, 0.3); }
    .header-banner h1 { color: white; font-weight: 900; font-size: clamp(22px, 5vw, 36px); margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
    .header-banner h3 { color: #fecaca; font-weight: 700; font-size: clamp(14px, 3vw, 18px); margin-top: 5px; text-transform: uppercase; letter-spacing: 1px; }
    .selector-box { background: white; padding: 20px; border-radius: 12px; border: 2px solid #e2e8f0; border-top: 5px solid var(--navy); box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 25px; }
    .result-card { background: white; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0; border-top: 6px solid var(--meb-red); box-shadow: 0 10px 30px rgba(0,0,0,0.08); margin-bottom: 20px; overflow: hidden; }
    .metric-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); gap: 10px; margin: 15px 0; }
    .metric-box { background: var(--card-bg); padding: 12px; border-radius: 8px; text-align: center; border: 1px solid #e2e8f0; }
    .metric-box span { display: block; font-size: 11px; font-weight: 800; color: #64748b; text-transform: uppercase; }
    .metric-box b { font-size: 22px; color: var(--navy); }
    .optik-container { overflow-x: auto; margin-top: 15px; border-radius: 8px; border: 1px solid #e2e8f0; }
    .optik-table { width: 100%; border-collapse: collapse; font-size: 11px; text-align: center; }
    .optik-table th { background: #111827; color: white; padding: 6px; border: 1px solid #334155; }
    .optik-table td { padding: 6px; border: 1px solid #e2e8f0; font-weight: 700; }
    .dogru { background-color: #dcfce7 !important; color: #166534 !important; }
    .yanlis { background-color: #111827 !important; color: white !important; }
    .rehberlik-box { background: #fffafa; border-left: 5px solid var(--meb-red); padding: 15px; border-radius: 8px; margin-top: 15px; font-size: 13px; line-height: 1.5; color: #1e293b; text-align: justify; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: 700; height: 3.2em; background: var(--navy); color: white; transition: 0.3s; border: none; }
    .stButton>button:hover { background: var(--meb-red); transform: translateY(-2px); }
    </style>
""", unsafe_allow_html=True)

def detayli_pedagojik_analiz(row):
    p, d, y, b, ad = row['Puan'], row['Doğru'], row['Yanlış'], row['Boş'], row['Ad']
    vizyon = ("Matematik; evrenin dilini anlamamızı sağlayan eşsiz bir pusuladır. "
              "Bu sınav, senin sadece bilgini değil, analitik düşünme yeteneğini de ölçtü. ")
    if p >= 85: durum = f"<b>{p} puan</b> ile harika bir olimpiyat derecesi elde ettin {ad}! Analitik zekan en üst seviyede."
    elif p >= 65: durum = f"<b>{p} puan</b> ile çok güçlü bir temel sergiledin. Küçük dikkatsizliklerin üzerine gidersen zirvedesin."
    elif p >= 40: durum = f"<b>{p} puan</b> ile önemli bir direnç gösterdin. Olimpiyat soruları zordur. Bol pratikle başarıyı katlayabilirsin."
    else: durum = f"<b>{p} puan</b> aldın. Bu sonuç senin azmini kırmasın; aksine eksiklerini tamamlaman için bir rehberdir. Hatalarından ders çıkaranlar asıl kazananlardır."
    return f"Sevgili <b>{ad}</b>,<br>{vizyon}<br><br>{durum}<br><br><b>Başarılar Dileriz!</b>"

def idari_gelisim_raporu(okul_adi, okul_ort, ilce_ort, df_subeler):
    fark = okul_ort - ilce_ort
    if fark > 5: return f"Kurumunuz <b>{okul_ort:.2f}</b> ortalama ile ilçe başarısını sırtlayan okullardan biridir. Zümre öğretmenlerinin gayreti takdire şayandır."
    elif fark >= -2: return f"Kurumunuz <b>{okul_ort:.2f}</b> ortalama ile ilçe geneliyle paralel bir çizgidedir. Başarıyı artırmak için yeni nesil soru pratiklerine ağırlık verilmelidir."
    else: return f"Kurumunuz <b>{okul_ort:.2f}</b> ortalama ile ilçe ortalamasının gerisinde kalmıştır. Akademik eksiklikler hızla tespit edilip telafi çalışmalarına başlanmalıdır."

@st.cache_data
def verileri_yukle():
    mevcut_dosyalar = os.listdir('.')
    liste = []
    for d in mevcut_dosyalar:
        if "sonuc" in d.lower():
            try:
                if d.lower().endswith('.csv'): df = pd.read_csv(d, sep=',', quotechar='"', on_bad_lines='skip')
                elif d.lower().endswith('.xlsx') or d.lower().endswith('.xls'): df = pd.read_excel(d)
                else: continue
                
                if 'Puan' in df.columns and 'Öğrenci No' in df.columns:
                    df['Arama_No'] = df['Öğrenci No'].astype(str).str.replace('.0', '', regex=False).str.strip().str.lstrip('0')
                    df['Sınıf'] = df['Sınıf'].astype(str).str.replace('.0', '', regex=False).str.strip()
                    liste.append(df)
            except: pass
    if liste:
        birlestirilmis = pd.concat(liste, ignore_index=True)
        birlestirilmis = birlestirilmis.drop_duplicates(subset=['Öğrenci No', 'OKUL ADI', 'Sınıf'])
        return birlestirilmis.sort_values(by=['Puan', 'Net'], ascending=[False, False]).reset_index(drop=True)
    return pd.DataFrame()

df_tum = verileri_yukle()

# ==========================================
# 2. BÖLÜM: ÜST SEÇİM VE ÖĞRENCİ ARAYÜZÜ
# ==========================================
st.markdown('<div class="selector-box">', unsafe_allow_html=True)
st.markdown('<h3 style="color:#E30A17; margin-top:0; text-align:center;">📊 İŞLEM YAPILACAK SINIF DÜZEYİ</h3>', unsafe_allow_html=True)
sinif_listesi = [f"{i}. Sınıf" for i in range(4, 13)]
secilen_kademe_str = st.selectbox("Lütfen Listelemek İstediğiniz Sınıfı Seçiniz:", sinif_listesi, index=0)
kademe_no = secilen_kademe_str.split(".")[0]
st.markdown('</div>', unsafe_allow_html=True)

if not df_tum.empty: df_tum['Sınıf'] = df_tum['Sınıf'].astype(str)
df_aktif = df_tum[df_tum['Sınıf'] == str(kademe_no)].copy() if not df_tum.empty else pd.DataFrame()

# İŞTE EKSİK OLAN O ANA SATIR (SEKMELERİN OLUŞTURULDUĞU YER):
tab_ogrenci, tab_idareci = st.tabs(["🎓 ÖĞRENCİ SONUÇ EKRANI", "🏛️ İDARE VE KURUM DURUM ANALİZİ"])

with tab_ogrenci:
    if df_aktif.empty:
        st.warning(f"Sistemde henüz {secilen_kademe_str} seviyesine ait sınav verisi bulunmamaktadır.")
    else:
        st.markdown("### 🔍 Bireysel Başarı Sonucu, Optik Form ve Pedagojik Karne")
        c1, c2 = st.columns(2)
        with c1:
            okul_listesi = sorted(df_aktif['OKUL ADI'].dropna().unique())
            secilen_okul = st.selectbox("Okulunuzu Seçiniz:", okul_listesi)
        with c2:
            girilen_no = st.text_input("Öğrenci Numaranız:", placeholder="Örn: 145").strip().lstrip('0')
        
        if st.button("SONUÇLARI GETİR VE ANALİZ ET"):
            if not girilen_no: st.error("Lütfen öğrenci numaranızı giriniz.")
            else:
                sonuc = df_aktif[(df_aktif['OKUL ADI'] == secilen_okul) & (df_aktif['Arama_No'] == girilen_no)]
                if not sonuc.empty:
                    st.balloons()
                    o = sonuc.iloc[0]
                    analiz_html = detayli_pedagojik_analiz(o)
                    
                    try:
                        ogr_cvp = ast.literal_eval(str(o.get('Ogrenci_Cevap_Listesi', "['-']*20")))
                        key_cvp = ast.literal_eval(str(o.get('Cevap_Anahtari_Listesi', "['-']*20")))
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

                    st.markdown("#### 📊 Öğrenci Sonuç Veri Tablosu")
                    gosterilecek_tablo = pd.DataFrame([o])[['Öğrenci No', 'Ad', 'Soyad', 'OKUL ADI', 'Sınıf', 'Şube', 'Doğru', 'Yanlış', 'Boş', 'Net', 'Puan', 'Okul Sırası', 'İlçe Sırası']]
                    st.dataframe(gosterilecek_tablo, use_container_width=True, hide_index=True)
                    
                    st.markdown(f"""
                    <div class="result-card">
                        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:2px solid #e2e8f0; padding-bottom:15px; flex-wrap:wrap; gap:10px;">
                            <div>
                                <h1 style="margin:0; color:#111827; font-size:clamp(20px, 4vw, 28px);">{o['Ad']} {o['Soyad']}</h1>
                                <p style="margin:0; color:#E30A17; font-weight:800; font-size:clamp(14px, 2.5vw, 16px);">{o['OKUL ADI']} - Sınıf: {o['Sınıf']}/{o['Şube']}</p>
                            </div>
                            <div style="background:#111827; color:white; padding:8px 15px; border-radius:8px; font-weight:bold;">No: {o['Öğrenci No']}</div>
                        </div>
                        <div class="metric-grid">
                            <div class="metric-box"><span>Doğru</span><b style="color:#059669;">{o['Doğru']}</b></div>
                            <div class="metric-box"><span>Yanlış</span><b style="color:#E30A17;">{o['Yanlış']}</b></div>
                            <div class="metric-box"><span>Boş</span><b style="color:#64748b;">{o['Boş']}</b></div>
                            <div class="metric-box"><span>Net</span><b style="color:#2563eb;">{o['Net']}</b></div>
                            <div class="metric-box" style="background:#111827; border-color:#111827;"><span style="color:#94a3b8;">PUAN</span><b style="color:white;">{o['Puan']}</b></div>
                        </div>
                        <h4 style="color:#111827; margin-bottom:5px; font-size: 15px;">📋 Öğrenci Cevapları ve Doğru Şıklar</h4>
                        <div class="optik-container">
                            <table class="optik-table">
                                <tr><th style="text-align:left; background:#111827; color:white; padding:5px; width:90px;">Soru No</th>{optik_th}</tr>
                                <tr><th style="text-align:left; background:#f1f5f9; padding:5px; color:#111827;">Cevap Anh.</th>{optik_key}</tr>
                                <tr><th style="text-align:left; background:#f1f5f9; padding:5px; color:#111827;">Öğrenci</th>{optik_ogr}</tr>
                            </table>
                        </div>
                        <div class="rehberlik-box"><h3 style="margin-top:0; color:#E30A17; font-size:16px;">🎓 Pedagojik Rehberlik</h3>{analiz_html}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    bireysel_pdf_html = f"""
                    <html><head><meta charset="utf-8"><style>
                        @page {{ size: A4 portrait; margin: 15mm; }}
                        body {{ font-family: 'Segoe UI', Tahoma, sans-serif; padding: 0; margin: 0; color: #111827; -webkit-print-color-adjust: exact !important; }}
                        .karne-container {{ border: 4px solid #111827; border-radius: 15px; padding: 25px; background: white; }}
                        .header {{ text-align: center; border-bottom: 3px solid #E30A17; padding-bottom: 10px; margin-bottom: 15px; }}
                        .header h1 {{ margin: 0; font-size: 20px; text-transform: uppercase; }}
                        .header h2 {{ margin: 5px 0 0 0; color: #E30A17; font-size: 16px; }}
                        .info-strip {{ display: flex; justify-content: space-between; font-size: 14px; font-weight: bold; margin-bottom: 15px; background: #f8fafc; padding: 12px; border-radius: 8px; border: 1px solid #e2e8f0; }}
                        .stats-table {{ width: 100%; border-collapse: collapse; text-align: center; margin-bottom: 15px; }}
                        .stats-table th {{ background: #111827; color: white; padding: 8px; font-size: 14px; border: 1px solid #111827; }}
                        .stats-table td {{ padding: 10px; font-size: 20px; font-weight: 900; border: 1px solid #cbd5e1; }}
                        .optik-table {{ width: 100%; border-collapse: collapse; text-align: center; margin-bottom: 15px; font-size: 11px; }}
                        .optik-table th {{ background: #fef2f2; border: 1px solid #fca5a5; padding: 5px; color: #E30A17; }}
                        .optik-table td {{ border: 1px solid #fca5a5; padding: 6px; font-weight: bold; font-size: 12px; }}
                        .optik-table .baslik-hucre {{ background: #111827; color: white; text-align: left; width: 80px; }}
                        .optik-table .alt-baslik-hucre {{ background: #f1f5f9; color: #111827; text-align: left; font-size: 10px; }}
                        .dogru {{ background-color: #dcfce7 !important; color: #059669 !important; }}
                        .yanlis {{ background-color: #111827 !important; color: white !important; }}
                        .analiz-box {{ background: #fffafa; border-left: 6px solid #E30A17; padding: 15px; font-size: 13px; line-height: 1.5; text-align: justify; border-radius: 8px; border: 1px solid #fee2e2; }}
                    </style></head><body>
                        <div class="karne-container">
                            <div class="header"><h1>1. DARGEÇİT MATEMATİK OLİMPİYATI</h1><h2>RESMİ SINAV SONUÇ BELGESİ</h2></div>
                            <div class="info-strip">
                                <span>{o['Ad']} {o['Soyad']}</span><span>{o['OKUL ADI']} - Sınıf: {o['Sınıf']}/{o['Şube']}</span>
                                <span style="color:#E30A17;">No: {o['Öğrenci No']} | İlçe S: {o.get('İlçe Sırası','-')} | Okul S: {o.get('Okul Sırası','-')}</span>
                            </div>
                            <table class="stats-table">
                                <tr><th>Doğru</th><th>Yanlış</th><th>Boş</th><th>Net</th><th style="background:#E30A17;">PUAN</th></tr>
                                <tr><td style="color:#059669;">{o['Doğru']}</td><td style="color:#E30A17;">{o['Yanlış']}</td><td>{o['Boş']}</td><td style="color:#2563eb;">{o['Net']}</td><td>{o['Puan']}</td></tr>
                            </table>
                            <table class="optik-table">
                                <tr><th class="baslik-hucre">Soru No</th>{optik_th}</tr>
                                <tr><th class="alt-baslik-hucre">Cevap Anahtarı</th>{optik_key}</tr>
                                <tr><th class="alt-baslik-hucre">Öğrenci Cevabı</th>{optik_ogr}</tr>
                            </table>
                            <div class="analiz-box"><h3 style="margin-top:0; color:#E30A17; font-size: 15px;">🎓 Uzman Pedagojik Değerlendirme</h3>{analiz_html}</div>
                        </div>
                    </body></html>
                    """
                    st.download_button(f"📥 Bireysel Karne İndir (PDF)", data=bireysel_pdf_html, file_name=f"{o['Ad']}_{o['Soyad']}_Karne.html", mime="text/html")
                else: st.error("❌ Sistemde eşleşen kayıt bulunamadı. Lütfen bilgileri kontrol ediniz.")

# ==============================================================================
# 3. BÖLÜM: İDARE VE KURUM DURUM ANALİZİ (TOPLU SONUÇLAR)
# ==============================================================================
with tab_idareci:
    st.markdown("### 🔐 İlçe Milli Eğitim ve Kurum Yönetim Paneli")
    sifre = st.text_input("Yetkili Giriş Şifresi:", type="password")
    
    if sifre == "darder47":
        if df_tum.empty: st.error("Sistemde analiz edilecek sonuç verisi bulunamadı.")
        else:
            sub1, sub2, sub3, sub4 = st.tabs(["🏆 İLÇE GENEL DURUMU", "📈 KURUM GELİŞİM RAPORU", "📉 ŞUBE / ÖĞRETMEN ANALİZİ", "📑 TÜM SINIFLAR TOPLU LİSTE/KARNE"])

            with sub1:
                st.markdown(f"#### 🏢 {secilen_kademe_str} İlçe Geneli Toplu Sınav Sonuçları")
                if df_aktif.empty: st.warning("Bu sınıf düzeyinde veri bulunmamaktadır.")
                else:
                    st.markdown("<div class='metric-grid'>", unsafe_allow_html=True)
                    c_m1, c_m2, c_m3, c_m4 = st.columns(4)
                    with c_m1: st.markdown(f"<div class='metric-box'><span>Toplam Öğrenci</span><b>{len(df_aktif)}</b></div>", unsafe_allow_html=True)
                    with c_m2: st.markdown(f"<div class='metric-box'><span>Kurum Sayısı</span><b>{df_aktif['OKUL ADI'].nunique()}</b></div>", unsafe_allow_html=True)
                    with c_m3: st.markdown(f"<div class='metric-box'><span>İlçe Puan Ort.</span><b>{df_aktif['Puan'].mean():.2f}</b></div>", unsafe_allow_html=True)
                    with c_m4: st.markdown(f"<div class='metric-box'><span>İlçe Net Ort.</span><b style='color:#E30A17;'>{df_aktif['Net'].mean():.2f}</b></div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    df_okul_genel = df_aktif.groupby('OKUL ADI').agg(Ogr_Sayisi=('Puan', 'count'), Ort_Puan=('Puan', 'mean')).reset_index()
                    fig = px.bar(df_okul_genel.sort_values(by='Ort_Puan', ascending=True), x='Ort_Puan', y='OKUL ADI', orientation='h', text_auto='.2f', color='Ort_Puan', color_continuous_scale='Reds')
                    fig.update_layout(height=400, margin=dict(l=0, r=0, t=30, b=0), xaxis_title="Puan Ortalaması", yaxis_title="")
                    st.plotly_chart(fig, use_container_width=True)

            with sub2:
                st.markdown(f"#### 📈 {secilen_kademe_str} Kurum Denetim ve Gelişim Raporları")
                if df_aktif.empty: st.warning("Veri bulunamadı.")
                else:
                    ilce_ort = df_aktif['Puan'].mean()
                    secilen_kurum = st.selectbox("Ön İzleme Yapılacak Okulu Seçiniz:", sorted(df_aktif['OKUL ADI'].unique()), key="gelisim_okul")
                    
                    df_kurum_gelisim = df_aktif[df_aktif['OKUL ADI'] == secilen_kurum]
                    okul_ort = df_kurum_gelisim['Puan'].mean()
                    toplam_ogrenci = len(df_kurum_gelisim)
                    df_subeler = df_kurum_gelisim.groupby('Şube').agg(Mevcut=('Puan', 'count'), Sube_Ort_Puan=('Puan', 'mean')).reset_index().sort_values(by='Sube_Ort_Puan', ascending=False)
                    
                    metin = idari_gelisim_raporu(secilen_kurum, okul_ort, ilce_ort, df_subeler)
                    durum_renk = "#059669" if (okul_ort - ilce_ort) >= 0 else "#E30A17"
                    
                    st.markdown(f"""
                    <div style="background:white; padding:20px; border-radius:12px; border-left:8px solid {durum_renk}; box-shadow:0 4px 12px rgba(0,0,0,0.05);">
                        <h3 style="margin-top:0; font-size:18px;">{secilen_kurum} Durum Analizi Ön İzlemesi</h3>
                        <p style="font-size:14px;">Okul Ortalaması: <b>{okul_ort:.2f}</b> | İlçe Ortalaması: <b>{ilce_ort:.2f}</b></p><hr>
                        <p style="text-align:justify; line-height:1.6; font-size:14px;">{metin}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("📑 TÜM OKULLARIN GELİŞİM RAPORLARINI İNDİR (İlçe MEM Çıktısı)", type="primary"):
                        tum_okullar_html = """
                        <html><head><meta charset="utf-8"><style>
                            @page { size: A4 portrait; margin: 15mm; }
                            body { font-family: 'Segoe UI', Tahoma, sans-serif; margin: 0; padding: 0; color: #111827; -webkit-print-color-adjust: exact !important; }
                            .page { page-break-after: always; display: flex; flex-direction: column; min-height: 260mm; }
                            .baslik-alan { text-align: center; border-bottom: 5px solid #111827; padding-bottom: 15px; margin-bottom: 25px; }
                            .baslik-alan h1 { margin: 0; font-size: 22px; font-weight: 900; }
                            .baslik-alan h2 { margin: 5px 0 0 0; color: #E30A17; font-size: 16px; font-weight: bold; }
                            .bilgi-serit { display: flex; justify-content: space-between; background: #fef2f2; border: 1px solid #fca5a5; padding: 15px; border-radius: 8px; margin-bottom: 20px; font-weight: bold; font-size: 14px; }
                            .analiz-metni { font-size: 14px; line-height: 1.6; text-align: justify; margin-bottom: 30px; background: #f8fafc; padding: 25px; border-radius: 8px; border-left: 5px solid #111827; flex-grow: 1; }
                            .tablo-alan { width: 100%; border-collapse: collapse; text-align: center; margin-bottom: 20px; font-size: 14px; }
                            .tablo-alan th { background: #111827; color: white; padding: 10px; border: 1px solid #111827; }
                            .tablo-alan td { padding: 10px; border: 1px solid #cbd5e1; font-weight: bold; font-size: 15px; }
                            .imza-kismi { text-align: right; margin-top: 40px; font-weight: bold; font-size: 16px; }
                            .footer { font-size: 11px; color: #64748b; text-align: center; margin-top: auto; border-top: 1px solid #cbd5e1; padding-top: 10px; }
                        </style></head><body>
                        """
                        for okul in sorted(df_aktif['OKUL ADI'].unique()):
                            df_o = df_aktif[df_aktif['OKUL ADI'] == okul]
                            o_ort = df_o['Puan'].mean()
                            o_toplam = len(df_o)
                            df_s = df_o.groupby('Şube').agg(Mevcut=('Puan', 'count'), Sube_Ort_Puan=('Puan', 'mean')).reset_index().sort_values(by='Sube_Ort_Puan', ascending=False)
                            o_metin = idari_gelisim_raporu(okul, o_ort, ilce_ort, df_s)
                            
                            tum_okullar_html += f"""
                            <div class="page">
                                <div class="baslik-alan"><h1>T.C. DARGEÇİT KAYMAKAMLIĞI</h1><h2>1. MATEMATİK OLİMPİYATI KURUM DURUM ANALİZİ VE GELİŞİM RAPORU</h2></div>
                                <div class="bilgi-serit"><span>Kurum: {okul}</span><span>Sınıf Düzeyi: {kademe_no}. Sınıflar</span><span>İlçe Ortalaması: {ilce_ort:.2f}</span><span style="color:#E30A17;">Okul Ortalaması: {o_ort:.2f}</span></div>
                                <div class="analiz-metni">{o_metin}</div>
                                <div><h4 style="margin:0 0 10px 0; color:#111827;">Zümre / Şube Performans Tablosu</h4>
                                    <table class="tablo-alan"><tr><th>Şube Adı</th><th>Sınava Giren Öğrenci</th><th>Şube Puan Ortalaması</th></tr>
                            """
                            for _, s_row in df_s.iterrows(): tum_okullar_html += f"<tr><td>{s_row['Şube']}</td><td>{s_row['Mevcut']}</td><td style='color:#E30A17;'>{s_row['Sube_Ort_Puan']:.2f}</td></tr>"
                            tum_okullar_html += """</table></div>
                                <div class="imza-kismi">Dargeçit İlçe Milli Eğitim Müdürlüğü</div>
                                <div class="footer">Bu rapor Dargeçit İlçe Milli Eğitim Müdürlüğü Ölçme ve Değerlendirme Merkezi tarafından kurumsal gelişim amacıyla otomatik oluşturulmuştur.</div>
                            </div>"""
                        tum_okullar_html += "</body></html>"
                        st.download_button("📥 İLÇE MEM - TÜM OKULLARIN RAPORUNU İNDİR", data=tum_okullar_html, file_name=f"Dargecit_MEM_{kademe_no}_Siniflar_Kurum_Raporlari.html", mime="text/html")

            with sub3:
                st.markdown(f"#### 📉 {secilen_kademe_str} Zümre ve Sınıf Başarı Grafikleri")
                if not df_aktif.empty:
                    df_sube_genel = df_aktif.groupby(['OKUL ADI', 'Şube']).agg(Ogr=('Puan', 'count'), Puan_Ort=('Puan', 'mean')).reset_index()
                    df_sube_genel = df_sube_genel[df_sube_genel['Ogr'] >= 3].sort_values(by='Puan_Ort', ascending=True).tail(15)
                    df_sube_genel['Sube_Ad'] = df_sube_genel['OKUL ADI'] + " - " + df_sube_genel['Şube']
                    fig3 = px.bar(df_sube_genel, x='Puan_Ort', y='Sube_Ad', orientation='h', text_auto='.2f', color='Puan_Ort', color_continuous_scale='Teal', title="İlçenin En Başarılı Şubeleri")
                    fig3.update_layout(height=400, margin=dict(l=0, r=0, t=30, b=0))
                    st.plotly_chart(fig3, use_container_width=True)

            with sub4:
                st.markdown("#### 📑 Okul Bazlı TÜM SINIFLAR (Toplu Liste ve Karneler)")
                st.success("👨‍💼 **Okul Müdürleri İçin:** Bu bölümden, okulunuzdaki **TÜM SINIF KADEMELERİNE (4, 5, 6, 7 vb.)** ait listeleri ve Sayfada 2'li Optik Karneleri tek seferde alabilirsiniz.")
                
                okul_listesi_genel = ["Tüm İlçe Listesi"] + sorted(df_tum['OKUL ADI'].dropna().unique().tolist())
                kurum_secim_tum = st.selectbox("Tüm Kademeleri İndirilecek Okulu Seçin:", okul_listesi_genel, key="toplu_karne_okul_tum")
                
                if kurum_secim_tum == "Tüm İlçe Listesi": df_filtre = df_tum.copy()
                else: df_filtre = df_tum[df_tum['OKUL ADI'] == kurum_secim_tum].copy()
                
                df_filtre['Sınıf_Int'] = pd.to_numeric(df_filtre['Sınıf'], errors='coerce').fillna(0)
                df_filtre = df_filtre.sort_values(by=['Sınıf_Int', 'Şube', 'Puan'], ascending=[True, True, False])
                
                st.markdown(f"**Veri Özeti:** Seçilen okulda sınava giren toplam **{len(df_filtre)}** öğrencinin tüm kademelerdeki verisi çekildi.")
                c_btn1, c_btn2 = st.columns(2)
                
                pdf_liste_html = f"""
                <html><head><meta charset="utf-8"><style>
                    body {{ font-family: 'Segoe UI', Tahoma, sans-serif; }}
                    .h {{ text-align: center; border-bottom: 2px solid #111827; margin-bottom: 20px; padding-bottom: 10px; }}
                    table {{ width: 100%; border-collapse: collapse; text-align: center; font-size: 11px; }}
                    th {{ background: #111827; color: white; padding: 8px; border: 1px solid #111827; }}
                    td {{ border: 1px solid #ddd; padding: 6px; }}
                </style></head><body>
                    <div class="h"><h2 style="margin:0;">T.C. DARGEÇİT KAYMAKAMLIĞI - 1. MATEMATİK OLİMPİYATI</h2><h3 style="margin:5px 0 0 0; color:#E30A17;">{kurum_secim_tum} - TÜM SINIFLAR BAŞARI LİSTESİ</h3></div>
                    <table><tr><th>Ad Soyad</th><th>Sınıf/Şube</th><th>No</th><th>Doğru</th><th>Yanlış</th><th>Boş</th><th>Net</th><th>Puan</th></tr>
                """
                for _, r in df_filtre.iterrows(): pdf_liste_html += f"<tr><td style='text-align:left; font-weight:bold;'>{r['Ad']} {r['Soyad']}</td><td>{r['Sınıf']}/{r['Şube']}</td><td>{r['Öğrenci No']}</td><td>{r['Doğru']}</td><td>{r['Yanlış']}</td><td>{r['Boş']}</td><td>{r['Net']}</td><td style='color:#E30A17; font-weight:bold;'>{r['Puan']}</td></tr>"
                pdf_liste_html += "</table></body></html>"
                c_btn1.download_button("📊 1) Tüm Sınıfların Listesini İndir (PDF)", data=pdf_liste_html, file_name=f"{kurum_secim_tum}_Tum_Siniflar_Liste.html", mime="text/html")

                html_toplu_karne = """
                <html><head><meta charset="utf-8"><style>
                    @page { size: A4 portrait; margin: 10mm; }
                    body { font-family: 'Segoe UI', Tahoma, sans-serif; margin: 0; padding: 0; background: white; -webkit-print-color-adjust: exact !important; }
                    .page { width: 190mm; display: flex; flex-direction: column; gap: 6mm; page-break-after: always; }
                    .karne { width: 100%; height: 137mm; border: 3px solid #E30A17; border-radius: 12px; padding: 12px; position: relative; page-break-inside: avoid; display: flex; flex-direction: column; justify-content: space-between; overflow: hidden; box-sizing: border-box; }
                    .baslik { text-align: center; font-weight: 900; font-size: 13px; border-bottom: 2px solid #E30A17; padding-bottom: 4px; text-transform: uppercase; }
                    .kimlik { display: flex; justify-content: space-between; font-weight: 900; font-size: 12px; margin-top: 6px; }
                    .sira { text-align: center; background: #111827; color: white; padding: 4px; border-radius: 6px; font-size: 11px; margin: 6px 0; font-weight: bold; }
                    .stats { width: 100%; border-collapse: collapse; text-align: center; font-size: 11px; margin-bottom: 5px; }
                    .stats th { background: #fef2f2; border: 1px solid #fca5a5; padding: 4px; color: #E30A17; }
                    .stats td { border: 1px solid #fca5a5; padding: 5px; font-weight: 900; font-size: 14px; }
                    .optik-table { width: 100%; border-collapse: collapse; text-align: center; font-size: 9px; margin-bottom: 5px; }
                    .optik-table th { background: #fef2f2; border: 1px solid #fca5a5; padding: 3px; color: #E30A17; }
                    .optik-table td { border: 1px solid #fca5a5; padding: 4px; font-weight: bold; font-size: 10px; }
                    .optik-table .baslik-hucre { background: #111827; color: white; text-align: left; width: 75px; }
                    .optik-table .alt-baslik-hucre { background: #f1f5f9; color: #111827; text-align: left; font-size: 8px; }
                    .dogru { background-color: #dcfce7 !important; color: #059669 !important; }
                    .yanlis { background-color: #111827 !important; color: white !important; }
                    .analiz { background: #fffafa !important; border-left: 5px solid #E30A17; padding: 8px; font-size: 10.5px; line-height: 1.35; text-align: justify; border-radius: 6px; border: 1px solid #fee2e2; color: #111827; margin-top: auto; }
                </style></head><body>
                """
                
                for i, row in df_filtre.reset_index().iterrows():
                    if i % 2 == 0: html_toplu_karne += "<div class='page'>"
                    analiz_metni = detayli_pedagojik_analiz(row)
                    
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
                            <div class="kimlik" style="color:#555; font-size:10px; margin-top:2px;"><span>{row['OKUL ADI']}</span><span>Sınıf: {row['Sınıf']}/{row['Şube']}</span></div>
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
                        <div class="analiz"><b style="color:#E30A17; font-size:11px;">🎓 Pedagojik Değerlendirme:</b><br>{analiz_metni}</div>
                    </div>
                    """
                    if (i + 1) % 2 == 0 or i == len(df_filtre) - 1: html_toplu_karne += "</div>"
                
                html_toplu_karne += "</body></html>"
                c_btn2.download_button("🖨️ 2) Tüm Sınıfların Karnelerini Al (PDF)", data=html_toplu_karne, file_name=f"{kurum_secim_tum}_Tum_Siniflar_Karneler.html", mime="text/html")

    elif sifre != "":
        st.error("❌ Yetkisiz Erişim: Şifre Hatalı!")
