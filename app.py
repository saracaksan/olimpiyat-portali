import streamlit as st
import pandas as pd
import io
import ast
import os

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
    
    /* Yazı Keskinleştirme Teknolojisi */
    * { -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }

    /* Üst Banner */
    .header-box {
        background: white; padding: 25px; border-bottom: 6px solid var(--meb-red);
        border-radius: 12px; margin-bottom: 30px; text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }
    .header-box h1 { color: var(--navy); font-weight: 900; font-size: 32px; margin: 0; letter-spacing: -0.5px; }
    .header-box h3 { color: var(--meb-red); font-weight: 800; font-size: 18px; margin-top: 5px; text-transform: uppercase; }

    /* Yan Menü (Pop-up Vurgusu) */
    .sidebar-title { color: var(--meb-red); font-weight: 900; font-size: 18px; margin-bottom: 10px; display: block; text-align: center; }
    
    /* Butonlar */
    .stButton>button { 
        background-color: var(--navy); color: white; border-radius: 8px; 
        font-weight: bold; height: 3em; border: none; transition: 0.3s; width: 100%;
    }
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
        return f"Önemli bir çaba ve gayret gösterdin {ad}. Temel matematik becerilerine sahipsin ancak mantık ağırlıklı sorularda daha fazla tecrübeye ihtiyacın var. {b} boş bıraktığın soru, bilmediğin konularda risk almadığını gösteriyor ki bu iyi bir strateji. Pratik yaparak netlerini çok daha yukarılara taşıyabilirsin."
    else:
        return f"Bu sınav senin için çok değerli bir tecrübe oldu {ad}. Puanın hedeflerinin altında kalmış olabilir ancak olimpiyat sınavları zorluk derecesi yüksek sınavlardır. {y} yanlışın, konu eksiklerin olduğunu ve soru çözümünde daha fazla dikkat etmen gerektiğini gösteriyor. Asla pes etme, her hata yeni bir öğrenme fırsatıdır!"

# --- BANNER ---
st.markdown("""
    <div class="header-box">
        <h1>🥇 1. DARGEÇİT MATEMATİK OLİMPİYATI</h1>
        <h3>Sınav Sonuç ve İdari Yönetim Portalı</h3>
    </div>
""", unsafe_allow_html=True)

# --- VERİ YÜKLEME ---
@st.cache_data
def veriyi_oku(dosya_adi):
    if not os.path.exists(dosya_adi): return None
    try:
        df = pd.read_excel(dosya_adi)
        df['Arama_No'] = df['Öğrenci No'].astype(str).str.lstrip('0').str.split('.').str[0]
        df = df.sort_values(by=['Puan', 'Net'], ascending=[False, False]).reset_index(drop=True)
        return df
    except: return None

# --- YAN MENÜ: SINIF SEÇİMİ ---
with st.sidebar:
    st.markdown('<span class="sidebar-title">⬇️ KATEGORİ (POP-UP) MENÜSÜ</span>', unsafe_allow_html=True)
    sinif_listesi = [f"{i}. Sınıf" for i in range(4, 13)]
    secilen_sinif_str = st.selectbox("Lütfen listelemek istediğiniz sınıfı seçin:", sinif_listesi, index=3)
    sinif_no = secilen_sinif_str.split(".")[0]
    aktif_dosya = f"sonuclar_{sinif_no}.xlsx"
    st.divider()
    st.info("⚠️ İdareciler diğer sınıfların raporlarını görmek için yukarıdaki menüden sınıf değiştirebilirler.")

df = veriyi_oku(aktif_dosya)

if df is None:
    st.warning(f"⚠️ {secilen_sinif_str} kategorisine ait sonuç dosyası ({aktif_dosya}) sistemde bulunamadı.")
else:
    tab1, tab2 = st.tabs(["👤 Öğrenci Bireysel Sonuç Görüntüleme", "🏫 Okul İdaresi ve Müdür Paneli (Yazdırma Merkezi)"])

    # =========================================================
    # 1. TAB: ÖĞRENCİ SORGULAMA
    # =========================================================
    with tab1:
        st.markdown(f"### 🔍 {secilen_sinif_str} Sınav Sonucu Sorgulama")
        col_ogr1, col_ogr2 = st.columns(2)
        with col_ogr1: okul_secim = st.selectbox("Okulunuzu Seçin:", sorted(df['OKUL ADI'].unique()))
        with col_ogr2: no_secim = st.text_input("Öğrenci Numaranız (Baştaki sıfırları girmeyebilirsiniz):").lstrip('0')

        if st.button("Karnemi Göster", type="primary"):
            sonuc = df[(df['OKUL ADI'] == okul_secim) & (df['Arama_No'] == no_secim)]
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
    # 2. TAB: İDARECİ PANELİ VE KUSURSUZ YAZDIRMA MERKEZİ
    # =========================================================
    with tab2:
        st.markdown(f"### 🏫 {secilen_sinif_str} Raporlama ve Çıktı Alma Merkezi")
        sifre = st.text_input("Giriş Şifresi:", type="password")
        
        if sifre == "darder47":
            st.success("Yetkilendirme Başarılı. Yönetim Paneline Hoş Geldiniz.")
            
            c_id1, c_id2 = st.columns([2, 1])
            with c_id1: kurum = st.selectbox("İşlem Yapılacak Okul:", ["Tüm İlçe"] + sorted(df['OKUL ADI'].unique()))
            with c_id2: baraj = st.number_input("Giriş Belgesi Baraj Puanı:", value=75)
            
            f_df = df if kurum == "Tüm İlçe" else df[df['OKUL ADI'] == kurum]
            st.dataframe(f_df[['İlçe Sırası', 'Okul Sırası', 'OKUL ADI', 'Sınıf', 'Şube', 'Öğrenci No', 'Ad', 'Soyad', 'Net', 'Puan']], use_container_width=True)

            st.divider()
            st.markdown("### 🖨️ Profesyonel PDF ve Excel Çıktı Merkezi")
            
            c_btn1, c_btn2, c_btn3 = st.columns(3)
            
            # --- 1. EXCEL İNDİRME ---
            buf_ex = io.BytesIO()
            with pd.ExcelWriter(buf_ex, engine='openpyxl') as writer:
                f_df.to_excel(writer, index=False)
            c_btn1.download_button("📊 1) Excel Raporunu İndir", data=buf_ex.getvalue(), file_name=f"{kurum}_Raporu.xlsx")

            # --- 2. KUSURSUZ A4 KARNELER (1 SAYFADA 4 ADET - SİMETRİK GRID SİSTEMİ) ---
            html_karne = """
            <html><head><meta charset="utf-8"><style>
                @page { size: A4 portrait; margin: 10mm; }
                * { box-sizing: border-box; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
                body { font-family: 'Segoe UI', Arial, sans-serif; background: white; margin: 0; padding: 0; color: #111827; }
                
                /* Mükemmeliyetçi Grid Sistemi - Asla taşmaz, boşluk bırakmaz */
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
            for i, row in f_df.reset_index().iterrows():
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

                analiz_metni = profesyonel_analiz(row)

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
                    <div class="analiz-kutu"><b>Pedagojik Analiz:</b> {analiz_metni}</div>
                </div>
                """
                if (i + 1) % 4 == 0 or i == len(f_df) - 1: html_karne += "</div>"
            
            html_karne += "</body></html>"
            c_btn2.download_button("📑 2) Sonuç Karneleri PDF (A4'e 4 Adet Sığar)", data=html_karne, file_name=f"{kurum}_Karneler.html", mime="text/html")

            # --- 3. KUSURSUZ GİRİŞ BELGESİ (A4'E 2 ADET - DETAYLI KURALLARLA) ---
            belge_df = f_df[f_df['Puan'] >= baraj]
            
            html_belge = """
            <html><head><meta charset="utf-8"><style>
                @page { size: A4 portrait; margin: 10mm; }
                * { box-sizing: border-box; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
                body { font-family: 'Segoe UI', Tahoma, sans-serif; background: white; margin: 0; padding: 0; color: #111827; }
                
                /* 2'li Simetrik Grid */
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
            for i, row in belge_df.reset_index().iterrows():
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
                            <li>Sınav <b>klasik (açık uçlu)</b> formatta olacaktır. Tüm çözüm adımları detaylı olarak sınav kitapçığına yazılacaktır. Sadece cevapların yazılması puan kazandırmaz.</li>
                            <li>Öğrenciler kendi kurşun kalem, silgi ve kalemtıraşlarını getirmekle yükümlüdür. Sınav esnasında öğrenciler arası <b>silgi vb. kırtasiye alışverişi kesinlikle yasaktır.</b></li>
                            <li>Sınav süresince kopya çekmeye teşebbüs etmek, sağa sola bakmak veya konuşmak sınavın anında iptal sebebidir.</li>
                            <li>Adaylar sınav saatinden <b>en az 30 dakika önce</b> sınav salonunda hazır bulunmalıdır. İlk 30 dakika dolmadan sınav salonundan çıkılamaz.</li>
                        </ul>
                    </div>
                </div>
                """
                if (i + 1) % 2 == 0 or i == len(belge_df) - 1: html_belge += "</div>"
            
            html_belge += "</body></html>"
            c_btn3.download_button("🎟️ 3) Giriş Belgeleri PDF (A4'e 2 Adet)", data=html_belge, file_name=f"{kurum}_Giris_Belgeleri.html", mime="text/html")
            
            st.divider()
            st.success("Tebrikler! Sistem Kusursuz İşliyor. Çıktı alırken tarayıcınızda yazdır butonuna bastıktan sonra (Kenar Boşlukları: Yok) seçeneğini seçmeniz tavsiye edilir.")
        elif sifre != "":
            st.error("Hatalı Şifre!")
