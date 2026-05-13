import streamlit as st
import pandas as pd
import io
import ast
import os
import plotly.express as px

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="1. Dargeçit Matematik Olimpiyatı", layout="wide", page_icon="🥇")

# --- KUSURSUZ MOBİL UYUMLU, MEB KONSEPTLİ CSS ---
st.markdown("""
    <style>
    :root { 
        --meb-red: #E30A17; 
        --navy: #111827; 
        --light-bg: #f8fafc; 
        --card-bg: #ffffff; 
    }
    .main { background-color: var(--light-bg); }
    
    .selector-box { 
        background: white; padding: 20px; border-radius: 12px; 
        border: 2px solid #e2e8f0; border-top: 5px solid var(--navy); 
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 25px; 
        width: 100%; text-align: center;
    }
    .selector-box > div { margin: 0 auto; }

    .result-card { 
        background: white; padding: 20px; border-radius: 12px; 
        border: 1px solid #e2e8f0; border-top: 6px solid var(--meb-red); 
        box-shadow: 0 10px 30px rgba(0,0,0,0.08); margin-bottom: 20px; overflow: hidden; 
    }
    
    .metric-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(80px, 1fr)); gap: 10px; margin: 15px 0; }
    .metric-box { background: var(--card-bg); padding: 12px 5px; border-radius: 8px; text-align: center; border: 1px solid #e2e8f0; }
    .metric-box span { display: block; font-size: 11px; font-weight: 800; color: #64748b; text-transform: uppercase; }
    .metric-box b { font-size: clamp(18px, 4vw, 24px); color: var(--navy); }

    .optik-container { width: 100%; overflow-x: auto; margin-top: 15px; border-radius: 8px; border: 1px solid #e2e8f0; -webkit-overflow-scrolling: touch; }
    .optik-table { width: 100%; border-collapse: collapse; font-size: 12px; text-align: center; min-width: 600px; }
    .optik-table th { background: #111827; color: white; padding: 8px; border: 1px solid #334155; }
    .optik-table td { padding: 8px; border: 1px solid #e2e8f0; font-weight: 700; }
    .dogru { background-color: #dcfce7 !important; color: #166534 !important; }
    .yanlis { background-color: #111827 !important; color: white !important; }

    .rehberlik-box { background: #fffafa; border-left: 5px solid var(--meb-red); padding: 15px; border-radius: 8px; margin-top: 15px; font-size: 14px; line-height: 1.6; color: #1e293b; text-align: justify; }
    
    .stButton>button { width: 100%; border-radius: 8px; font-weight: 700; height: 3.5em; background: var(--navy); color: white; transition: 0.3s; border: none; margin-top: 10px; }
    .stButton>button:hover { background: var(--meb-red); transform: translateY(-2px); }
    
    .stTabs [data-baseweb="tab-list"] { display: flex; flex-wrap: wrap; justify-content: center; gap: 5px; }
    .stTabs [data-baseweb="tab"] { padding: 10px 15px; font-size: 14px; white-space: normal; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- 1. DOKUNULMAMIŞ, DETAYLI ÖĞRENCİ PEDAGOJİK ANALİZ MOTORU ---
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

# --- YENİ EKSİKSİZ VERİ YÜKLEME ALTYAPISI (CSV VE EXCEL TAM DESTEK) ---
@st.cache_data
def verileri_yukle():
    mevcut_dosyalar = os.listdir('.')
    liste = []
    for d in mevcut_dosyalar:
        if "sonuc" in d.lower() or "sonuç" in d.lower():
            try:
                if d.lower().endswith('.csv'):
                    df = pd.read_csv(d, sep=',', quotechar='"', on_bad_lines='skip')
                elif d.lower().endswith('.xlsx') or d.lower().endswith('.xls'):
                    df = pd.read_excel(d)
                else:
                    continue
                    
                if 'Puan' in df.columns and 'Öğrenci No' in df.columns:
                    df['Arama_No'] = df['Öğrenci No'].astype(str).str.replace('.0', '', regex=False).str.strip().str.lstrip('0')
                    df['Sınıf'] = df['Sınıf'].astype(str).str.replace('.0', '', regex=False).str.strip()
                    liste.append(df)
            except Exception: 
                pass
                
    if liste:
        birlestirilmis = pd.concat(liste, ignore_index=True)
        birlestirilmis = birlestirilmis.drop_duplicates(subset=['Öğrenci No', 'OKUL ADI', 'Sınıf'])
        return birlestirilmis.sort_values(by=['Puan', 'Net'], ascending=[False, False]).reset_index(drop=True)
    return pd.DataFrame()

df_tum = verileri_yukle()
# ==============================================================================
# 2. BÖLÜM: MOBİL UYUMLU ÖĞRENCİ ARAMA ARAYÜZÜ VE DETAYLI KARNE EKRANI
# ==============================================================================

# --- ANA SEKMELER ---
tab_ogrenci, tab_idareci = st.tabs(["🎓 ÖĞRENCİ SONUÇ EKRANI", "🏛️ İDARE VE KURUM DURUM ANALİZİ"])

with tab_ogrenci:
    st.markdown("### 🔍 Bireysel Başarı Sonucu ve Pedagojik Karne")
    st.info("💡 **Sevgili Öğrenciler:** Lütfen önce okulunuzu, ardından sınıfınızı seçip numaranızı girerek sonuçlarınızı görüntüleyiniz.")
    
    # --- MOBİL UYUMLU, ORTALANMIŞ ARAMA PANELİ ---
    st.markdown('<div class="selector-box">', unsafe_allow_html=True)
    
    # 1. Adım: Okul Seçimi
    okul_listesi = ["Okul Seçiniz..."] + sorted(df_tum['OKUL ADI'].dropna().unique().tolist()) if not df_tum.empty else ["Veri Yok"]
    secilen_okul = st.selectbox("1️⃣ Okulunuzu Seçiniz:", okul_listesi)
    
    # 2. Adım: Sınıf Seçimi (Sadece seçilen okula ait sınıflar listelenir)
    if secilen_okul != "Okul Seçiniz..." and secilen_okul != "Veri Yok":
        siniflar = sorted(df_tum[df_tum['OKUL ADI'] == secilen_okul]['Sınıf'].dropna().unique().tolist())
        sinif_listesi = ["Sınıf Seçiniz..."] + siniflar
    else:
        sinif_listesi = ["Önce Okul Seçiniz..."]
        
    secilen_sinif = st.selectbox("2️⃣ Sınıfınızı Seçiniz:", sinif_listesi)
    
    # 3. Adım: Öğrenci Numarası
    girilen_no = st.text_input("3️⃣ Öğrenci Numaranız:", placeholder="Örn: 145").strip().lstrip('0')
    
    search_btn = st.button("SONUÇLARI GETİR VE ANALİZ ET")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- SONUÇ GETİRME VE GÖSTERİM MANTIĞI ---
    if search_btn:
        if secilen_okul in ["Okul Seçiniz...", "Veri Yok"] or secilen_sinif in ["Sınıf Seçiniz...", "Önce Okul Seçiniz..."]:
            st.warning("⚠️ Lütfen okulunuzu ve sınıfınızı eksiksiz seçiniz.")
        elif not girilen_no:
            st.error("⚠️ Lütfen öğrenci numaranızı giriniz.")
        else:
            # Okul, sınıf ve numaranın üçünün de eşleştiği kaydı arıyoruz
            sonuc = df_tum[(df_tum['OKUL ADI'] == secilen_okul) & 
                           (df_tum['Sınıf'] == secilen_sinif) & 
                           (df_tum['Arama_No'] == girilen_no)]
            
            if not sonuc.empty:
                st.balloons()
                o = sonuc.iloc[0]
                
                # Sizin yazdığınız pedagojik analiz motorunu çağırıyoruz
                analiz_html = detayli_pedagojik_analiz(o)
                
                # --- OPTİK FORM DÖNÜŞÜMÜ VE KONTROLÜ ---
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

                # AŞAMA 1: EKRANDAKİ KARNE ARAYÜZÜ (Mobil ekranlardan taşmaz)
                st.markdown(f"""
                <div class="result-card">
                    <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:2px solid #e2e8f0; padding-bottom:15px; flex-wrap:wrap; gap:10px;">
                        <div>
                            <h1 style="margin:0; color:#111827; font-size:clamp(20px, 4vw, 28px);">{o['Ad']} {o['Soyad']}</h1>
                            <p style="margin:0; color:#E30A17; font-weight:800; font-size:clamp(14px, 2.5vw, 16px);">{o['OKUL ADI']} - Sınıf: {o['Sınıf']}/{o['Şube']}</p>
                        </div>
                        <div style="background:#111827; color:white; padding:8px 15px; border-radius:8px; font-weight:bold;">
                            No: {o['Öğrenci No']}
                        </div>
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
                            <tr><th style="text-align:left; background:#111827; color:white; padding:5px; min-width:80px;">Soru No</th>{optik_th}</tr>
                            <tr><th style="text-align:left; background:#f1f5f9; padding:5px; color:#111827;">Cevap Anh.</th>{optik_key}</tr>
                            <tr><th style="text-align:left; background:#f1f5f9; padding:5px; color:#111827;">Öğrenci</th>{optik_ogr}</tr>
                        </table>
                    </div>

                    <div class="rehberlik-box">
                        <h3 style="margin-top:0; color:#E30A17; font-size:16px;">🎓 Pedagojik Rehberlik</h3>
                        {analiz_html}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # AŞAMA 2: BİREYSEL PDF İNDİRME KODU (İndirilebilir karne)
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
                    .imza-kismi {{ text-align: center; margin-top: 15px; font-weight: bold; font-size: 14px; color: #64748b; }}
                </style></head><body>
                    <div class="karne-container">
                        <div class="header">
                            <h1>1. DARGEÇİT MATEMATİK OLİMPİYATI</h1>
                            <h2>RESMİ SINAV SONUÇ BELGESİ</h2>
                        </div>
                        <div class="info-strip">
                            <span>{o['Ad']} {o['Soyad']}</span>
                            <span>{o['OKUL ADI']} - Sınıf: {o['Sınıf']}/{o['Şube']}</span>
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
                            <h3 style="margin-top:0; color:#E30A17; font-size: 15px;">🎓 Uzman Pedagojik Değerlendirme</h3>
                            {analiz_html}
                        </div>
                        <div class="imza-kismi">Dargeçit İlçe Milli Eğitim Müdürlüğü</div>
                    </div>
                </body></html>
                """
                st.download_button(f"📥 Bireysel Karne İndir (PDF)", data=bireysel_pdf_html, file_name=f"{o['Ad']}_{o['Soyad']}_Karne.html", mime="text/html")
            else:
                st.error("❌ Sistemde eşleşen kayıt bulunamadı. Lütfen okul, sınıf ve numara bilgilerinizi kontrol ediniz.")
# ==============================================================================
# 3. VE 4. BÖLÜM: İDARE PANELİ VE İNDİRME MERKEZİ (BİRLEŞTİRİLMİŞ TAM KOD)
# ==============================================================================
with tab_idareci:
    st.markdown("### 🔐 İlçe Milli Eğitim ve Kurum Yönetim Paneli")
    sifre = st.text_input("Yetkili Giriş Şifresi:", type="password")

    if sifre == "darder47":
        if df_tum.empty:
            st.error("Sistemde analiz edilecek sonuç verisi bulunamadı.")
        else:
            st.success("Giriş Başarılı. Yönetim Paneline Hoş Geldiniz.")

            # --- DİNAMİK FİLTRELEME ALANI (Tam Esnek Yapı) ---
            st.markdown("#### ⚙️ Raporlama ve Filtreleme Seçenekleri")
            st.info("💡 Buradan seçeceğiniz kriterler; hem aşağıdaki başarı grafiklerini hem de toplu listeleri ve karneleri şekillendirecektir.")
            
            c_f1, c_f2 = st.columns(2)
            with c_f1:
                okul_secenekleri = ["Tüm İlçe (Genel)"] + sorted(df_tum['OKUL ADI'].dropna().unique().tolist())
                idare_okul = st.selectbox("1. Kurum Seçimi:", okul_secenekleri)
            with c_f2:
                if idare_okul == "Tüm İlçe (Genel)":
                    sinif_secenekleri = ["Tüm Sınıflar Kademesi"] + sorted(df_tum['Sınıf'].dropna().unique().tolist())
                else:
                    sinif_secenekleri = ["Tüm Sınıflar Kademesi"] + sorted(df_tum[df_tum['OKUL ADI'] == idare_okul]['Sınıf'].dropna().unique().tolist())
                idare_sinif = st.selectbox("2. Sınıf Kademesi Seçimi:", sinif_secenekleri)

            # --- SEÇİME GÖRE VERİYİ FİLTRELEME ---
            if idare_okul == "Tüm İlçe (Genel)":
                df_idare = df_tum.copy()
                kapsam_metni = "İlçe Geneli"
            else:
                df_idare = df_tum[df_tum['OKUL ADI'] == idare_okul].copy()
                kapsam_metni = idare_okul

            if idare_sinif != "Tüm Sınıflar Kademesi":
                df_idare = df_idare[df_idare['Sınıf'] == idare_sinif].copy()
                kapsam_metni += f" ({idare_sinif}. Sınıflar)"
            else:
                kapsam_metni += " (Tüm Kademeler)"

            if df_idare.empty:
                st.warning(f"Seçilen kriterlere uygun ({kapsam_metni}) sınav verisi bulunamadı.")
            else:
                # İDARE İÇ SEKMELERİ
                idare_tab1, idare_tab2 = st.tabs(["📈 BAŞARI GRAFİKLERİ VE İDARİ YORUMLAR", "📑 TOPLU LİSTE VE KARNELER (İndirme Merkezi)"])

                with idare_tab1:
                    st.markdown(f"#### 📊 {kapsam_metni} Gelişim Raporu")

                    met1, met2, met3, met4 = st.columns(4)
                    met1.markdown(f"<div class='metric-box'><span>Öğrenci Sayısı</span><b>{len(df_idare)}</b></div>", unsafe_allow_html=True)
                    met2.markdown(f"<div class='metric-box'><span>Ortalama Puan</span><b>{df_idare['Puan'].mean():.2f}</b></div>", unsafe_allow_html=True)
                    met3.markdown(f"<div class='metric-box'><span>Ortalama Net</span><b>{df_idare['Net'].mean():.2f}</b></div>", unsafe_allow_html=True)
                    en_yuksek = df_idare['Puan'].max()
                    met4.markdown(f"<div class='metric-box'><span>En Yüksek Puan</span><b style='color:#059669;'>{en_yuksek}</b></div>", unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)

                    if idare_okul == "Tüm İlçe (Genel)":
                        df_grup = df_idare.groupby('OKUL ADI').agg(Ort_Puan=('Puan', 'mean')).reset_index().sort_values(by='Ort_Puan', ascending=True)
                        fig = px.bar(df_grup, x='Ort_Puan', y='OKUL ADI', orientation='h', text_auto='.2f', color='Ort_Puan', color_continuous_scale='Reds', title=f"{kapsam_metni} - Kurumlar Arası Başarı Sıralaması")
                        fig.update_layout(height=max(400, len(df_grup)*35), margin=dict(l=0, r=0, t=40, b=0))
                        st.plotly_chart(fig, use_container_width=True)

                        ilce_ort = df_idare['Puan'].mean()
                        lider_okul = df_grup.iloc[-1]['OKUL ADI']
                        lider_puan = df_grup.iloc[-1]['Ort_Puan']
                        zayif_okul = df_grup.iloc[0]['OKUL ADI']

                        yorum = f"<b>📌 MEM Analiz ve Yönlendirme Notu:</b> Seçilen <i>'{kapsam_metni}'</i> kriteri bazında yapılan incelemede ilçe genel olimpiyat ortalamasının <b>{ilce_ort:.2f}</b> olduğu tespit edilmiştir. Grafikte net bir şekilde görüldüğü üzere <b>{lider_okul}</b> kurumu, {lider_puan:.2f} ortalama ile ilçede lider konumdadır ve uyguladığı pedagojik yöntemlerin/soru çözüm tekniklerinin zümre çalıştaylarında diğer kurumlara örnek teşkil etmesi önem arz etmektedir. Diğer yandan, başarı ortalamasının altında kalan kurumlarımızın (özellikle {zayif_okul} vb.) okul idareleri ve matematik zümreleriyle ivedilikle 'Durum Değerlendirme Toplantısı' yapması, öğrencilerin yeni nesil sorulara aşinalığını artıracak eylem planları hazırlaması tavsiye edilmektedir."
                        st.markdown(f"<div style='background:#f8fafc; border-left:6px solid var(--navy); padding:15px; border-radius:8px; font-size:14px; line-height:1.6; margin-bottom:25px;'>{yorum}</div>", unsafe_allow_html=True)

                        if idare_sinif == "Tüm Sınıflar Kademesi":
                            df_sinif_grup = df_idare.groupby('Sınıf').agg(Ort_Puan=('Puan', 'mean')).reset_index().sort_values(by='Sınıf', ascending=True)
                            df_sinif_grup['Sınıf_Gorsel'] = df_sinif_grup['Sınıf'] + ". Sınıflar"

                            fig2 = px.bar(df_sinif_grup, x='Sınıf_Gorsel', y='Ort_Puan', text_auto='.2f', color='Ort_Puan', color_continuous_scale='Viridis', title="İlçe Geneli Sınıf Kademeleri Arası Başarı Dağılımı")
                            fig2.update_layout(height=400, margin=dict(l=0, r=0, t=40, b=0))
                            st.plotly_chart(fig2, use_container_width=True)

                            en_iyi_kademe = df_sinif_grup.sort_values(by='Ort_Puan').iloc[-1]['Sınıf_Gorsel']
                            yorum2 = f"<b>📌 Kademe Analiz Notu:</b> İlçe genelinde farklı sınıf düzeyleri kıyaslandığında, en yüksek verimin ve olimpiyat uyumunun <b>{en_iyi_kademe}</b> düzeyinde gerçekleştiği görülmektedir. Olimpiyat sorularının analitik yapısı ve öğrencilerin bilişsel gelişimleri dikkate alındığında, grafikte düşük kalan kademeler için zümre bazında öğretim stratejileri güncellenmeli, çocuklara mantık-muhakeme oyunları ve pratikleri yaptırılmalıdır."
                            st.markdown(f"<div style='background:#f8fafc; border-left:6px solid var(--meb-red); padding:15px; border-radius:8px; font-size:14px; line-height:1.6;'>{yorum2}</div>", unsafe_allow_html=True)

                    else:
                        df_sube_grup = df_idare.groupby(['Sınıf', 'Şube']).agg(Ort_Puan=('Puan', 'mean')).reset_index()
                        df_sube_grup['Sube_Ad'] = df_sube_grup['Sınıf'] + "/" + df_sube_grup['Şube']
                        df_sube_grup = df_sube_grup.sort_values(by='Ort_Puan', ascending=True)

                        fig3 = px.bar(df_sube_grup, x='Ort_Puan', y='Sube_Ad', orientation='h', text_auto='.2f', color='Ort_Puan', color_continuous_scale='Teal', title=f"{kapsam_metni} - Şubeler (Zümre) Arası Başarı Sıralaması")
                        fig3.update_layout(height=max(400, len(df_sube_grup)*40), margin=dict(l=0, r=0, t=40, b=0))
                        st.plotly_chart(fig3, use_container_width=True)

                        okul_ort = df_idare['Puan'].mean()
                        if len(df_sube_grup) > 1:
                            lider_sube = df_sube_grup.iloc[-1]['Sube_Ad']
                            lider_sube_puan = df_sube_grup.iloc[-1]['Ort_Puan']
                            yorum3 = f"<b>📌 Kurum İçi İdari Analiz Notu:</b> Seçtiğiniz <i>'{kapsam_metni}'</i> filtrelerine göre kurumunuzdaki genel olimpiyat ortalaması <b>{okul_ort:.2f}</b> puandır. Şubeler arası akademik rekabet tablosu incelendiğinde, <b>{lider_sube} şubesinin</b> {lider_sube_puan:.2f} ortalama ile öne çıktığı ve okulu sırtladığı tespit edilmiştir. İlgili sınıfın öğretmenini pedagojik yaklaşımından ötürü tebrik eder; kurumsal topyekün başarının artması adına, tüm şubelerin bu homojen başarı ivmesini yakalaması için sınıf içi farklılaştırılmış eğitim yöntemlerine başvurulmasını idare olarak tavsiye ederiz."
                        else:
                            yorum3 = f"<b>📌 Kurum İçi İdari Analiz Notu:</b> Seçilen kriterlerde sınava sadece tek bir şube katılım sağladığı için şubeler arası öğretmen/sınıf kıyaslaması oluşturulamamıştır. Ancak elde edilen <b>{okul_ort:.2f}</b> puanlık sınıf ortalamasının, ilçe geneli ve olimpiyat standartlarına çekilebilmesi için öğrencilerin sınav kaygısı yaşamadan yeni nesil problemlerle daha sık karşılaştırılması (haftalık mini quizler vb.) önerilmektedir."
                        st.markdown(f"<div style='background:#f8fafc; border-left:6px solid #059669; padding:15px; border-radius:8px; font-size:14px; line-height:1.6;'>{yorum3}</div>", unsafe_allow_html=True)

                # ==============================================================================
                # BÖLÜM 4: TOPLU LİSTE VE TOPLU KARNE İNDİRME MERKEZİ
                # ==============================================================================
                with idare_tab2:
                    st.markdown(f"#### 📑 {kapsam_metni} - İndirme Merkezi")
                    st.success("👨‍💼 **Sayın İdareci:** Seçtiğiniz filtrelere ait sıralı başarı listelerini ve sayfada 2'li olarak tasarlanmış toplu karneleri aşağıdan indirebilirsiniz.")
                    
                    df_export = df_idare.copy()
                    df_export['Sınıf_Int'] = pd.to_numeric(df_export['Sınıf'], errors='coerce').fillna(0)
                    df_export = df_export.sort_values(by=['Sınıf_Int', 'Puan'], ascending=[True, False])
                    
                    st.markdown(f"**Hazırlanan Veri:** {len(df_export)} öğrenci (En yüksek puandan en düşük puana sıralı)")
                    
                    c_btn1, c_btn2 = st.columns(2)
                    
                    # --- 1. LİSTE OLUŞTURMA ---
                    pdf_liste_html = f"""
                    <html><head><meta charset="utf-8"><style>
                        body {{ font-family: 'Segoe UI', Tahoma, sans-serif; font-size: 12px; }}
                        .h {{ text-align: center; border-bottom: 2px solid #111827; margin-bottom: 20px; padding-bottom: 10px; }}
                        table {{ width: 100%; border-collapse: collapse; text-align: center; }}
                        th {{ background: #111827; color: white; padding: 10px; border: 1px solid #111827; }}
                        td {{ border: 1px solid #ddd; padding: 8px; }}
                        .satir-hover:nth-child(even) {{ background-color: #f8fafc; }}
                    </style></head><body>
                        <div class="h">
                            <h2 style="margin:0;">T.C. DARGEÇİT KAYMAKAMLIĞI - 1. MATEMATİK OLİMPİYATI</h2>
                            <h3 style="margin:5px 0 0 0; color:#E30A17;">{kapsam_metni.upper()} BAŞARI LİSTESİ</h3>
                        </div>
                        <table><tr><th>Okul</th><th>Ad Soyad</th><th>Sınıf/Şube</th><th>No</th><th>Doğru</th><th>Yanlış</th><th>Boş</th><th>Net</th><th>Puan</th></tr>
                    """
                    for _, r in df_export.iterrows():
                        pdf_liste_html += f"<tr class='satir-hover'><td>{r['OKUL ADI']}</td><td style='text-align:left; font-weight:bold;'>{r['Ad']} {r['Soyad']}</td><td>{r['Sınıf']}/{r['Şube']}</td><td>{r['Öğrenci No']}</td><td>{r['Doğru']}</td><td>{r['Yanlış']}</td><td>{r['Boş']}</td><td>{r['Net']}</td><td style='color:#E30A17; font-weight:bold;'>{r['Puan']}</td></tr>"
                    pdf_liste_html += "</table></body></html>"
                    
                    c_btn1.download_button(
                        f"📊 1) {kapsam_metni} Başarı Listesi (İndir)", 
                        data=pdf_liste_html, 
                        file_name=f"{kapsam_metni.replace(' ', '_')}_Liste.html", 
                        mime="text/html"
                    )

                    # --- 2. TOPLU KARNE OLUŞTURMA ---
                    html_toplu_karne = f"""
                    <html><head><meta charset="utf-8"><style>
                        @page {{ size: A4 portrait; margin: 10mm; }}
                        body {{ font-family: 'Segoe UI', Tahoma, sans-serif; margin: 0; padding: 0; background: white; -webkit-print-color-adjust: exact !important; }}
                        .page {{ width: 100%; height: 277mm; display: flex; flex-direction: column; gap: 5mm; page-break-after: always; justify-content: flex-start; }}
                        .karne {{ width: 100%; height: 136mm; border: 3px solid #E30A17; border-radius: 12px; padding: 10px; box-sizing: border-box; display: flex; flex-direction: column; overflow: hidden; page-break-inside: avoid; }}
                        .baslik {{ text-align: center; font-weight: 900; font-size: 13px; border-bottom: 2px solid #E30A17; padding-bottom: 4px; text-transform: uppercase; margin-bottom: 4px; color:#111827; }}
                        .kimlik {{ display: flex; justify-content: space-between; font-weight: 900; font-size: 12px; margin-top: 2px; }}
                        .sira {{ text-align: center; background: #111827; color: white; padding: 3px; border-radius: 6px; font-size: 11px; margin: 4px 0; font-weight: bold; }}
                        .stats {{ width: 100%; border-collapse: collapse; text-align: center; font-size: 11px; margin-bottom: 4px; }}
                        .stats th {{ background: #fef2f2; border: 1px solid #fca5a5; padding: 3px; color: #E30A17; }}
                        .stats td {{ border: 1px solid #fca5a5; padding: 3px; font-weight: 900; font-size: 13px; }}
                        .optik-table {{ width: 100%; border-collapse: collapse; text-align: center; font-size: 9px; margin-bottom: 4px; }}
                        .optik-table th {{ background: #fef2f2; border: 1px solid #fca5a5; padding: 2px; color: #E30A17; }}
                        .optik-table td {{ border: 1px solid #fca5a5; padding: 2px; font-weight: bold; font-size: 10px; }}
                        .optik-table .baslik-hucre {{ background: #111827; color: white; text-align: left; width: 65px; }}
                        .optik-table .alt-baslik-hucre {{ background: #f1f5f9; color: #111827; text-align: left; font-size: 8px; }}
                        .dogru {{ background-color: #dcfce7 !important; color: #059669 !important; }}
                        .yanlis {{ background-color: #111827 !important; color: white !important; }}
                        .analiz {{ background: #fffafa !important; border-left: 5px solid #E30A17; padding: 8px; font-size: 10.5px; line-height: 1.35; text-align: justify; border-radius: 6px; border: 1px solid #fee2e2; color: #111827; flex-grow: 1; }}
                        .imza-kismi {{ text-align: center; font-weight: bold; font-size: 10px; color: #64748b; margin-top: auto; padding-top: 3px; }}
                    </style></head><body>
                    """
                    
                    for i, row in df_export.reset_index().iterrows():
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
                        
                        html_toplu_karne += f'''
                        <div class="karne">
                            <div class="baslik">1. DARGEÇİT MATEMATİK OLİMPİYATI SONUÇ BELGESİ</div>
                            <div class="kimlik"><span>{row['Ad']} {row['Soyad']}</span><span style="color:#E30A17;">No: {row['Öğrenci No']}</span></div>
                            <div class="kimlik" style="color:#555; font-size:11px;"><span>{row['OKUL ADI']}</span><span>Sınıf: {row['Sınıf']}/{row['Şube']}</span></div>
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
                            
                            <div class="analiz"><b style="color:#E30A17; font-size:11px;">🎓 Pedagojik Değerlendirme:</b><br>{analiz_metni}</div>
                            <div class="imza-kismi">Dargeçit İlçe Milli Eğitim Müdürlüğü</div>
                        </div>
                        '''
                        if (i + 1) % 2 == 0 or i == len(df_export) - 1: html_toplu_karne += "</div>"
                    
                    html_toplu_karne += "</body></html>"
                    
                    c_btn2.download_button(
                        f"🖨️ 2) {kapsam_metni} Toplu Karneler (İndir)", 
                        data=html_toplu_karne, 
                        file_name=f"{kapsam_metni.replace(' ', '_')}_Karneler.html", 
                        mime="text/html"
                    )

    elif sifre != "":
        st.error("❌ Yetkisiz Erişim: Şifre Hatalı!")
