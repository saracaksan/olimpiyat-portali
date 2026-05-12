import streamlit as st
import pandas as pd
import io
import ast
import os

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="1. Dargeçit Matematik Olimpiyatı Portalı", layout="wide", page_icon="🥇")

# --- GELİŞMİŞ KURUMSAL CSS ---
st.markdown("""
    <style>import streamlit as st
import pandas as pd
import io
import ast
import os

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="1. Dargeçit Matematik Olimpiyatı Portalı", layout="wide", page_icon="🥇")

# --- PROFESYONEL TASARIM (CSS) ---
st.markdown("""
    <style>
    :root {
        --meb-kirmizi: #E30A17;
        --koyu-siyah: #111827;
        --acik-gri: #f3f4f6;
    }
    .main { background-color: var(--acik-gri); }
    .header-banner { 
        background-color: white; padding: 25px; border-bottom: 5px solid var(--meb-kirmizi); 
        border-radius: 12px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center; 
    }
    .header-banner h1 { color: var(--koyu-siyah); font-weight: 800; font-size: 30px; margin-bottom: 5px; }
    .header-banner h3 { color: var(--meb-kirmizi); font-weight: 600; font-size: 18px; margin-top: 0; }
    
    /* Sol Menü Sınıf Seçimi Vurgusu */
    .sidebar-label { color: var(--meb-kirmizi); font-weight: bold; font-size: 16px; margin-bottom: 10px; display: block; }
    
    /* Buton Tasarımları */
    .stButton>button { background-color: var(--koyu-siyah); color: white; border-radius: 8px; font-weight: bold; border:none; transition: 0.3s; }
    .stButton>button:hover { background-color: var(--meb-kirmizi); color: white; transform: translateY(-2px); }
    </style>
    """, unsafe_allow_html=True)

# --- ÜST BAŞLIK ---
st.markdown("""
    <div class="header-banner">
        <h1>🥇 1. DARGEÇİT MATEMATİK OLİMPİYATI</h1>
        <h3>Sınav Sonuç Sorgulama ve Analiz Sistemi</h3>
    </div>
""", unsafe_allow_html=True)

# --- VERİ OKUMA SİSTEMİ ---
@st.cache_data
def veriyi_oku(dosya_adi):
    if not os.path.exists(dosya_adi): return None
    df = pd.read_excel(dosya_adi)
    # Öğrenci numaralarını temizleme ve stringe çevirme
    df['Arama_No'] = df['Öğrenci No'].astype(str).str.lstrip('0').str.split('.').str[0]
    # Otomatik Başarı Sıralaması (Yüksek puan üstte)
    df = df.sort_values(by=['Puan', 'Net'], ascending=[False, False]).reset_index(drop=True)
    return df

# --- SOL MENÜ (SINIF SEÇİMİ) ---
with st.sidebar:
    st.markdown('<span class="sidebar-label">📊 SINIF SEÇİNİZ (POP-UP MENÜ)</span>', unsafe_allow_html=True)
    siniflar = [f"{i}. Sınıf" for i in range(4, 13)]
    # Öğretmenlerin fark etmesi için ibare eklendi
    secilen_sinif_str = st.selectbox("Lütfen listeden sınav kategorisini belirleyin:", siniflar, index=3)
    secilen_no = secilen_sinif_str.split(".")[0]
    aktif_dosya = f"sonuclar_{secilen_no}.xlsx"
    st.divider()
    st.caption("Not: Diğer sınıfların sonuçlarını görmek için yukarıdaki menüyü kullanabilirsiniz.")

df = veriyi_oku(aktif_dosya)

if df is None:
    st.warning(f"⚠️ {secilen_sinif_str} kategorisine ait 'sonuclar_{secilen_no}.xlsx' dosyası GitHub deponuzda bulunamadı.")
else:
    tab1, tab2 = st.tabs(["👤 Öğrenci Sorgulama", "🏫 Kurum ve Öğretmen Paneli"])
    # --- app.py içindeki tab2 (Kurumsal Panel) bölümüne eklenecek ek özellik ---

with tab2:
    sifre = st.text_input("🔐 Kurum Şifresi:", type="password")
    if sifre == "darder47":
        st.success("Yetki Onaylandı.")
        
        # Filtreleme Seçenekleri
        kurum_okul = st.selectbox("Görüntülenecek Kurum:", ["Tüm İlçe Listesi"] + sorted(df['OKUL ADI'].unique()))
        
        f_df = df if kurum_okul == "Tüm İlçe Listesi" else df[df['OKUL ADI'] == kurum_okul]
        
        # 2. AŞAMA İÇİN BARAJ FİLTRESİ (Sadece Finalistlerin Belgesini Çıkarmak İçin)
        st.divider()
        st.subheader("🎟️ 2. Aşama Sınav Giriş Belgeleri")
        st.info("Sadece 2. aşamaya girmeye hak kazanan (barajı geçen) öğrencilerin belgeleri listelenir.")
        
        baraj_puani = st.number_input("Giriş Belgesi İçin Baraj Puanı:", value=75)
        belge_df = f_df[f_df['Puan'] >= baraj_puani]
        
        if belge_df.empty:
            st.warning("Bu okulda veya sınıfta belirlenen barajı geçen öğrenci bulunamadı.")
        else:
            st.write(f"Toplam {len(belge_df)} öğrenci için belge hazırlanabilir.")
            
            # GİRİŞ BELGESİ İÇİN DİNAMİK BİLGİLER
            c_giris1, c_giris2 = st.columns(2)
            sinav_yeri = c_giris1.text_input("Sınav Bina Adı:", value="Dargeçit Anadolu Lisesi")
            sinav_tarihi = c_giris2.text_input("Sınav Tarihi ve Saati:", value="18 Mayıs 2026 - 10:00")

            # --- PROFESYONEL GİRİŞ BELGESİ HTML MOTORU ---
            # (Bu şablon yönetici panelindekiyle aynıdır, idareciler buradan çıktı alabilir)
            belge_html = """
            <html><head><meta charset="utf-8"><style>
                @page { size: A4 portrait; margin: 10mm; }
                * { box-sizing: border-box; }
                body { font-family: 'Segoe UI', Arial, sans-serif; background: white; margin: 0; padding: 0; -webkit-print-color-adjust: exact !important; }
                .sayfa { width: 100%; height: 277mm; page-break-after: always; display: flex; flex-direction: column; }
                .belge-kutu { 
                    border: 2px solid #111827; border-radius: 12px; padding: 15px; 
                    margin-bottom: 10mm; height: 128mm; position: relative; overflow: hidden;
                    background-image: radial-gradient(#f3f4f6 1px, transparent 1px); background-size: 20px 20px;
                }
                .baslik-alan { text-align: center; border-bottom: 3px solid #E30A17; padding-bottom: 8px; margin-bottom: 10px; }
                .baslik-alan h2 { margin: 0; font-size: 17px; font-weight: 900; }
                .baslik-alan h3 { margin: 4px 0 0 0; color: #E30A17; font-size: 13px; font-weight: 800; }
                .bilgi-tablo { width: 100%; border-collapse: collapse; font-size: 12px; margin-bottom: 10px; }
                .bilgi-tablo td { padding: 6px; border: 1px solid #111827; }
                .bilgi-tablo td:nth-child(odd) { background: #f3f4f6; font-weight: bold; width: 22%; }
                .bilgi-tablo td:nth-child(even) { font-weight: 800; font-size: 13px; }
                .salon-vurgu { display: flex; justify-content: space-around; background: #111827; color: white; padding: 10px; border-radius: 8px; margin-bottom: 10px; }
                .kurallar { border: 2px dashed #E30A17; padding: 10px; border-radius: 8px; font-size: 10.5px; line-height: 1.3; }
            </style></head><body>
            """
            
            for i, row in belge_df.reset_index().iterrows():
                if i % 2 == 0: belge_html += "<div class='sayfa'>"
                
                belge_html += f"""
                <div class="belge-kutu">
                    <div class="baslik-alan">
                        <h2>T.C. DARGEÇİT KAYMAKAMLIĞI</h2>
                        <h3>1. MATEMATİK OLİMPİYATI FİNAL GİRİŞ BELGESİ</h3>
                    </div>
                    <table class="bilgi-tablo">
                        <tr><td>Adı Soyadı</td><td>{row['Ad']} {row['Soyad']}</td><td>Öğrenci No</td><td>{row['Öğrenci No']}</td></tr>
                        <tr><td>Okulu</td><td colspan="3">{row['OKUL ADI']}</td></tr>
                        <tr><td>Sınıf / Şube</td><td colspan="3">{row['Sınıf']} / {row['Şube']}</td></tr>
                    </table>
                    <div style="background:#f3f4f6; padding:8px; border-radius:8px; text-align:center; margin-bottom:10px; border:1px solid #ccc;">
                        <b>Sınav Yeri:</b> {sinav_yeri} | <b>Tarih:</b> {sinav_tarihi}
                    </div>
                    <div class="salon-vurgu">
                        <span>SALON ADI: {row.get('Salon Adı', 'Tanımsız')}</span>
                        <span>SIRA NO: {row.get('Sıra No', 'Tanımsız')}</span>
                    </div>
                    <div class="kurallar">
                        <b style="color:#E30A17;">SINAV KURALLARI:</b>
                        <ul>
                            <li>Sınava gelirken bu belgeyi ve <b>Nüfus Cüzdanınızı</b> mutlaka getiriniz.</li>
                            <li>Sınav klasik (açık uçlu) sorulardan oluşur. Kendi kaleminizi ve silginizi getirmelisiniz.</li>
                            <li>Sınav esnasında silgi vb. alışverişi kesinlikle yasaktır.</li>
                        </ul>
                    </div>
                </div>
                """
                if i % 2 == 1 or i == len(belge_df) - 1: belge_html += "</div>"

            belge_html += "</body></html>"
            
            st.download_button(
                label=f"🖨️ {kurum_okul} Giriş Belgelerini PDF Hazırla",
                data=belge_html,
                file_name=f"Giris_Belgeleri_{kurum_okul}.html",
                mime="text/html",
                use_container_width=True
            )

    # ---------------------------------------------------------
    # 1. ÖĞRENCİ SORGULAMA TABI
    # ---------------------------------------------------------
    with tab1:
        st.markdown(f"### 🔍 {secilen_sinif_str} Sonuç Sorgulama")
        c1, c2 = st.columns(2)
        with c1:
            okul_secim = st.selectbox("Okulunuzu Seçin:", sorted(df['OKUL ADI'].unique()))
        with c2:
            no_secim = st.text_input("Öğrenci Numaranız (Örn: 35):").lstrip('0')

        if st.button("Sonucumu Göster", type="primary"):
            sonuc = df[(df['OKUL ADI'] == okul_secim) & (df['Arama_No'] == no_secim)]
            if not sonuc.empty:
                st.balloons()
                o = sonuc.iloc[0]
                
                # Dinamik Yorum Sistemi
                p = o['Puan']
                if p >= 85: yr = "🌟 Üstün Başarı! Olimpiyat standartlarında bir zekaya sahipsin. 2. Aşamada başarılar!"
                elif p >= 65: yr = "👍 Çok İyi! Birkaç küçük dikkat hatası dışında hedefine çok yakınsın."
                elif p >= 40: yr = "📚 Başarılı bir temel. Düzenli soru çözümü ile netlerini hızla artırabilirsin."
                else: yr = "💪 Bu sınav senin için harika bir tecrübe oldu, çalışmaya devam et!"

                st.markdown(f"""
                <div style="background:white; padding:30px; border-radius:15px; border-top:8px solid var(--meb-kirmizi); box-shadow:0 10px 30px rgba(0,0,0,0.15);">
                    <h2 style="color:var(--koyu-siyah); margin:0;">{o['Ad']} {o['Soyad']}</h2>
                    <p style="color:#555; font-size:18px;"><b>{o['OKUL ADI']}</b> - {o['Sınıf']}/{o['Şube']} | Öğr. No: <b>{o['Öğrenci No']}</b></p>
                    <div style="background:var(--koyu-siyah); color:white; padding:10px; border-radius:8px; display:inline-block; margin-bottom:20px;">
                        İlçe Sıralaması: {o['İlçe Sırası']} | Okul Sıralaması: {o['Okul Sırası']}
                    </div>
                    <div style="display:flex; justify-content:space-around; text-align:center; border:2px solid #eee; padding:20px; border-radius:12px;">
                        <div><p style="margin:0; color:#666;">Doğru</p><h3 style="color:#059669; margin:0;">{o['Doğru']}</h3></div>
                        <div><p style="margin:0; color:#666;">Yanlış</p><h3 style="color:#E30A17; margin:0;">{o['Yanlış']}</h3></div>
                        <div><p style="margin:0; color:#666;">Boş</p><h3 style="color:#6b7280; margin:0;">{o['Boş']}</h3></div>
                        <div><p style="margin:0; color:#666;">Net</p><h3 style="color:#2563eb; margin:0;">{o['Net']}</h3></div>
                        <div><p style="margin:0; color:#666;">Puan</p><h2 style="color:var(--koyu-siyah); margin:0;">{o['Puan']}</h2></div>
                    </div>
                    <div style="background:#fff5f5; padding:15px; border-radius:8px; border-left:5px solid var(--meb-kirmizi); margin-top:20px;">
                        <p style="margin:0; font-style:italic;"><b>Analiz:</b> {yr}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("❌ Kayıt bulunamadı. Lütfen okul ve numara bilgilerinizi kontrol edin.")

    # ---------------------------------------------------------
    # 2. ÖĞRETMEN VE MÜDÜR PANELİ (PDF AKTARIM)
    # ---------------------------------------------------------
    with tab2:
        st.markdown(f"### 🏫 {secilen_sinif_str} Kurumsal Raporlama")
        st.info("⚠️ Diğer sınıfların listesini görmek için sol taraftaki **'SINIF SEÇİNİZ'** menüsünü kullanın.")
        
        sifre = st.text_input("Giriş Şifresi:", type="password")
        if sifre == "darder47":
            kurum = st.selectbox("Görüntülenecek Okul:", ["Tüm İlçe Listesi"] + sorted(df['OKUL ADI'].unique()))
            f_df = df if kurum == "Tüm İlçe Listesi" else df[df['OKUL ADI'] == kurum]

            # Tablo Görünümü
            st.dataframe(f_df[['İlçe Sırası', 'Okul Sırası', 'OKUL ADI', 'Sınıf', 'Şube', 'Öğrenci No', 'Ad', 'Soyad', 'Doğru', 'Yanlış', 'Net', 'Puan']], use_container_width=True)

            c_ex, c_pdf = st.columns(2)
            
            # Excel İndir
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                f_df.to_excel(writer, index=False)
            c_ex.download_button("📊 Excel Listeyi İndir", data=buffer.getvalue(), file_name=f"{kurum}_Sonuclar.xlsx", use_container_width=True)

            # --- SİMETRİK VE KUSURSUZ A4 PDF ŞABLONU (1 SAYFA / 6 KARNE) ---
            html_sablon = """
            <html><head><meta charset="utf-8"><style>
                @page { size: A4 portrait; margin: 8mm; }
                * { box-sizing: border-box; }
                body { font-family: 'Segoe UI', Arial, sans-serif; background: white; margin: 0; padding: 0; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
                .page { display: flex; flex-wrap: wrap; justify-content: space-between; align-content: flex-start; width: 100%; height: 275mm; page-break-after: always; }
                .karne { width: 49%; height: 88mm; border: 2.5px solid #111827; border-radius: 10px; padding: 12px; margin-bottom: 3mm; position: relative; overflow: hidden; }
                .baslik { color: #E30A17; text-align: center; font-weight: 900; font-size: 14px; border-bottom: 2px solid #eee; padding-bottom: 5px; margin-bottom: 8px; text-transform: uppercase; }
                .kimlik { display: flex; justify-content: space-between; font-weight: bold; margin-bottom: 4px; font-size: 12px; }
                .siralama { text-align: center; background: #111827; color: white; padding: 5px; border-radius: 5px; margin-bottom: 8px; font-size: 11px; font-weight: bold; }
                .analiz-tablo { width: 100%; border-collapse: collapse; text-align: center; margin-bottom: 8px; table-layout: fixed; }
                .analiz-tablo th { background: #f3f4f6; border: 1px solid #ccc; padding: 4px; font-size: 10px; }
                .analiz-tablo td { border: 1px solid #ccc; padding: 5px; font-weight: bold; font-size: 14px; }
                .optik-tablo { width: 100%; border-collapse: collapse; text-align: center; font-size: 9px; table-layout: fixed; }
                .optik-tablo td, .optik-tablo th { border: 1px solid #bbb; padding: 3px 0; height: 18px; }
                .optik-tablo th { background: #eee; font-weight: bold; }
                .dogru { background-color: #dcfce7 !important; color: #059669 !important; font-weight: 900; }
                .yanlis { background-color: #fee2e2 !important; color: #E30A17 !important; font-weight: 900; }
                .yorum { position: absolute; bottom: 8px; left: 12px; right: 12px; padding: 8px; background: #fff5f5 !important; border-left: 4px solid #E30A17; font-size: 10px; font-style: italic; font-weight: 600; line-height: 1.3; }
            </style></head><body>
            """
            
            kart_sayaci = 0
            html_sablon += "<div class='page'>"
            
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
                    key_td += f"<td>{dogru_cevap[i]}</td>"
                    o_cvp = ogr_cevap[i] if i < len(ogr_cevap) else '-'
                    if o_cvp == dogru_cevap[i] and o_cvp != '-':
                        stu_td += f"<td class='dogru'>{o_cvp}</td>"
                    elif o_cvp != dogru_cevap[i] and o_cvp != '-':
                        stu_td += f"<td class='yanlis'>{o_cvp}</td>"
                    else:
                        stu_td += f"<td>-</td>"

                p_val = row['Puan']
                if p_val >= 85: y_txt = "🌟 Üstün Başarı! Olimpiyat standartlarında bir zekaya sahipsin. Tebrikler!"
                elif p_val >= 65: y_txt = "👍 Çok İyi! Birkaç küçük dikkat hatası dışında harika bir performans."
                elif p_val >= 40: y_txt = "📚 Başarılı bir temel. Düzenli soru çözümü ile zirveye çıkabilirsin."
                else: y_txt = "💪 Bu sınav harika bir tecrübe oldu, çalışmaya devam!"

                html_sablon += f"""
                <div class="karne">
                    <div class="baslik">1. DARGEÇİT MATEMATİK OLİMPİYATI</div>
                    <div class="kimlik"><span>{row['Ad']} {row['Soyad']}</span><span style="color:#E30A17;">Öğr. No: {row['Öğrenci No']}</span></div>
                    <div class="kimlik" style="font-size:11px; color:#555; margin-bottom:5px;"><span>{row['OKUL ADI']}</span><span>{row['Sınıf']}/{row['Şube']}</span></div>
                    <div class="siralama">İlçe Sırası: {row['İlçe Sırası']} | Okul Sırası: {row['Okul Sırası']}</div>
                    <table class="analiz-tablo">
                        <tr><th>Doğru</th><th>Yanlış</th><th>Boş</th><th>Net</th><th>Puan</th></tr>
                        <tr><td>{row['Doğru']}</td><td>{row['Yanlış']}</td><td>{row['Boş']}</td><td>{row['Net']}</td><td style="background:#fef08a !important; font-size:16px;">{row['Puan']}</td></tr>
                    </table>
                    <table class="optik-tablo"><tr><td>Soru</td>{soru_th}</tr><tr><td>Cvp</td>{key_td}</tr><tr><td>Öğr</td>{stu_td}</tr></table>
                    <div class="yorum">{y_txt}</div>
                </div>
                """
                kart_sayaci += 1
                if kart_sayaci % 6 == 0 and kart_sayaci < len(f_df):
                    html_sablon += "</div><div class='page'>"
            
            html_sablon += "</div></body></html>"
            
            c_pdf.download_button("🖨️ PDF Karneleri Hazırla", data=html_sablon, file_name=f"{kurum}_Karneler.html", mime="text/html", use_container_width=True)

    :root {
        --meb-red: #E30A17;
        --navy: #111827;
        --gray: #f3f4f6;
    }
    .main { background-color: var(--gray); }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] { 
        height: 50px; background-color: white; border-radius: 8px 8px 0 0; 
        font-weight: bold; border: 1px solid #ddd;
    }
    .stTabs [aria-selected="true"] { background-color: var(--meb-red) !important; color: white !important; }
    
    /* Üst Banner */
    .header-container {
        background: white; padding: 25px; border-bottom: 6px solid var(--meb-red);
        border-radius: 12px; margin-bottom: 30px; text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .header-container h1 { color: var(--navy); font-weight: 900; font-size: 32px; margin-bottom: 5px; }
    .header-container h3 { color: var(--meb-red); font-weight: 700; font-size: 18px; margin-top: 0; }
    
    /* Butonlar */
    .stButton>button { 
        background-color: var(--navy); color: white; border-radius: 10px; 
        font-weight: bold; height: 3.5em; border: none; transition: 0.3s;
    }
    .stButton>button:hover { background-color: var(--meb-red); transform: translateY(-2px); }
    
    /* Yan Menü */
    .sidebar-label { color: var(--meb-red); font-weight: 900; font-size: 18px; margin-bottom: 15px; display: block; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- BANNER ---
st.markdown("""
    <div class="header-container">
        <h1>🥇 1. DARGEÇİT MATEMATİK OLİMPİYATI</h1>
        <h3>Sınav Sonuç Sorgulama ve Resmi Belge Portalı</h3>
    </div>
""", unsafe_allow_html=True)

# --- VERİ YÜKLEME ---
@st.cache_data
def veriyi_oku(dosya_adi):
    if not os.path.exists(dosya_adi): return None
    try:
        df = pd.read_excel(dosya_adi)
        df['Arama_No'] = df['Öğrenci No'].astype(str).str.lstrip('0').str.split('.').str[0]
        # Puan ve Net'e göre en iyiden en düşüğe sırala
        df = df.sort_values(by=['Puan', 'Net'], ascending=[False, False]).reset_index(drop=True)
        return df
    except: return None

# --- YAN MENÜ: SINIF SEÇİMİ ---
with st.sidebar:
    st.markdown('<span class="sidebar-label">📊 KATEGORİ SEÇİNİZ</span>', unsafe_allow_html=True)
    sinif_listesi = [f"{i}. Sınıf" for i in range(4, 13)]
    secilen_sinif_str = st.selectbox("Lütfen işlem yapacağınız sınıfı seçin:", sinif_listesi, index=3)
    sinif_no = secilen_sinif_str.split(".")[0]
    aktif_dosya = f"sonuclar_{sinif_no}.xlsx"
    st.divider()
    st.info(f"Su an **{secilen_sinif_str}** verileri üzerinde işlem yapmaktasınız.")

df = veriyi_oku(aktif_dosya)

if df is None:
    st.warning(f"⚠️ {secilen_sinif_str} sonuç dosyası ({aktif_dosya}) sistemde bulunamadı.")
else:
    tab1, tab2 = st.tabs(["👤 Öğrenci Sonuç Sorgulama", "🏫 İdareci ve Müdür Paneli"])

    # =========================================================
    # 1. TAB: ÖĞRENCİ SORGULAMA
    # =========================================================
    with tab1:
        st.markdown(f"### 🔍 {secilen_sinif_str} Bireysel Sorgulama")
        col_ogr1, col_ogr2 = st.columns(2)
        with col_ogr1:
            okul_secim = st.selectbox("Okulunuzu Seçin:", sorted(df['OKUL ADI'].unique()), key="okul_ogr")
        with col_ogr2:
            no_secim = st.text_input("Öğrenci Numaranız (Örn: 125):", key="no_ogr").lstrip('0')

        if st.button("Sonucumu Göster", type="primary"):
            sonuc = df[(df['OKUL ADI'] == okul_secim) & (df['Arama_No'] == no_secim)]
            if not sonuc.empty:
                st.balloons()
                o = sonuc.iloc[0]
                p = o['Puan']
                
                # Başarı Notu
                if p >= 85: yr = "🌟 Üstün Başarı! 2. Aşama final sınavında başarılar dileriz!"
                elif p >= 65: yr = "👍 Çok İyi! Güzel bir performans sergiledin, hedefine çok yakınsın."
                elif p >= 40: yr = "📚 Başarılı bir temel. Düzenli çalışma ile netlerini zirveye taşıyabilirsin."
                else: yr = "💪 Bu sınav harika bir tecrübe oldu. Eksiklerini kapatıp çalışmaya devam et!"

                st.markdown(f"""
                <div style="background:white; padding:35px; border-radius:15px; border-top:10px solid var(--meb-red); box-shadow:0 10px 30px rgba(0,0,0,0.1);">
                    <h2 style="color:var(--navy); margin:0;">{o['Ad']} {o['Soyad']}</h2>
                    <p style="color:#555; font-size:18px; margin-bottom:15px;"><b>{o['OKUL ADI']}</b> - {o['Sınıf']}/{o['Şube']} | No: <b>{o['Öğrenci No']}</b></p>
                    <div style="display:flex; gap:10px; margin-bottom:25px;">
                        <span style="background:var(--navy); color:white; padding:8px 15px; border-radius:5px; font-weight:bold;">İlçe Sırası: {o['İlçe Sırası']}</span>
                        <span style="background:var(--meb-red); color:white; padding:8px 15px; border-radius:5px; font-weight:bold;">Okul Sırası: {o['Okul Sırası']}</span>
                    </div>
                    <div style="display:grid; grid-template-columns: repeat(5, 1fr); gap:15px; text-align:center;">
                        <div style="background:#f9fafb; padding:15px; border-radius:10px; border:1px solid #eee;"><small>Doğru</small><br><b style="font-size:24px; color:#059669;">{o['Doğru']}</b></div>
                        <div style="background:#f9fafb; padding:15px; border-radius:10px; border:1px solid #eee;"><small>Yanlış</small><br><b style="font-size:24px; color:var(--meb-red);">{o['Yanlış']}</b></div>
                        <div style="background:#f9fafb; padding:15px; border-radius:10px; border:1px solid #eee;"><small>Boş</small><br><b style="font-size:24px; color:#6b7280;">{o['Boş']}</b></div>
                        <div style="background:#f9fafb; padding:15px; border-radius:10px; border:1px solid #eee;"><small>Net</small><br><b style="font-size:24px; color:#2563eb;">{o['Net']}</b></div>
                        <div style="background:#fff7ed; padding:15px; border-radius:10px; border:2px solid #fdba74;"><small>Puan</small><br><b style="font-size:28px; color:var(--navy);">{o['Puan']}</b></div>
                    </div>
                    <div style="margin-top:25px; padding:15px; background:#fef2f2; border-left:5px solid var(--meb-red); border-radius:5px;">
                        <p style="margin:0; font-weight:bold; font-style:italic; color:var(--navy);">Analiz: {yr}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("❌ Kayıt bulunamadı. Lütfen okulunuzu ve numaranızı kontrol edin.")

    # =========================================================
    # 2. TAB: İDARECİ PANELİ (TOPLU İŞLEMLER VE BELGELER)
    # =========================================================
    with tab2:
        st.markdown(f"### 🏫 {secilen_sinif_str} Kurumsal İdareci Paneli")
        sifre = st.text_input("Giriş Şifresi:", type="password", key="admin_sifre")
        
        if sifre == "darder47":
            st.success("Yetkilendirme Başarılı.")
            
            col_id1, col_id2 = st.columns([2, 1])
            with col_id1:
                kurum = st.selectbox("İşlem Yapılacak Okulu Seçin:", ["Tüm İlçe"] + sorted(df['OKUL ADI'].unique()))
            with col_id2:
                baraj = st.number_input("Giriş Belgesi Baraj Puanı:", value=75)
            
            f_df = df if kurum == "Tüm İlçe" else df[df['OKUL ADI'] == kurum]
            st.dataframe(f_df[['İlçe Sırası', 'Okul Sırası', 'OKUL ADI', 'Sınıf', 'Şube', 'Öğrenci No', 'Ad', 'Soyad', 'Net', 'Puan']], use_container_width=True)

            st.divider()
            
            # --- ÇIKTI ALMA BÖLÜMÜ ---
            st.markdown("### 🖨️ Toplu Çıktı ve Belge Oluşturucu")
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            
            # 1. EXCEL
            buf_ex = io.BytesIO()
            with pd.ExcelWriter(buf_ex, engine='openpyxl') as writer:
                f_df.to_excel(writer, index=False)
            col_btn1.download_button("📊 Excel Listeyi İndir", data=buf_ex.getvalue(), file_name=f"{kurum}_Listesi.xlsx")

            # 2. PROFESYONEL KARNELER (PDF/HTML)
            # (1 sayfada 6 simetrik karne)
            html_karne = """
            <html><head><meta charset="utf-8"><style>
                @page { size: A4; margin: 10mm; }
                body { font-family: Arial, sans-serif; margin: 0; padding: 0; -webkit-print-color-adjust: exact !important; }
                .sayfa { display: flex; flex-wrap: wrap; justify-content: space-between; width: 100%; height: 275mm; page-break-after: always; }
                .karne { width: 48%; height: 88mm; border: 2px solid #111827; border-radius: 10px; padding: 15px; margin-bottom: 3mm; box-sizing: border-box; position: relative; }
                .baslik { color: #E30A17; text-align: center; font-weight: 900; font-size: 14px; border-bottom: 2px solid #eee; padding-bottom: 5px; margin-bottom: 8px; }
                .kimlik { display: flex; justify-content: space-between; font-weight: bold; font-size: 11px; margin-bottom: 5px; }
                .sira { text-align: center; background: #111827; color: white; padding: 5px; border-radius: 5px; font-size: 10px; margin-bottom: 8px; }
                .tablo { width: 100%; border-collapse: collapse; text-align: center; font-size: 10px; margin-bottom: 8px; }
                .tablo th, .tablo td { border: 1px solid #ccc; padding: 4px; }
                .tablo th { background: #f3f4f6; }
                .optik { width: 100%; border-collapse: collapse; text-align: center; font-size: 9px; table-layout: fixed; }
                .optik th, .optik td { border: 1px solid #bbb; height: 18px; }
                .dogru { background: #dcfce7 !important; color: #059669; font-weight: bold; }
                .yanlis { background: #fee2e2 !important; color: #E30A17; font-weight: bold; }
                .yorum { position: absolute; bottom: 10px; left: 15px; right: 15px; padding: 8px; background: #fef2f2; border-left: 3px solid #E30A17; font-size: 9.5px; font-style: italic; }
            </style></head><body>
            """
            for i, row in f_df.reset_index().iterrows():
                if i % 6 == 0: html_karne += "<div class='sayfa'>"
                
                # Cevapları hazırlama
                try:
                    ogr_cvp = ast.literal_eval(row['Ogrenci_Cevap_Listesi'])
                    key_cvp = ast.literal_eval(row['Cevap_Anahtari_Listesi'])
                except:
                    ogr_cvp = ["-"] * 20; key_cvp = ["-"] * 20
                
                th_tags = "".join([f"<th>{j+1}</th>" for j in range(20)])
                st_tags = ""
                for j in range(20):
                    c = ogr_cvp[j] if j < len(ogr_cvp) else "-"
                    k = key_cvp[j] if j < len(key_cvp) else "-"
                    if c == k and c != "-": st_tags += f"<td class='dogru'>{c}</td>"
                    elif c != k and c != "-": st_tags += f"<td class='yanlis'>{c}</td>"
                    else: st_tags += f"<td>-</td>"

                html_karne += f"""
                <div class="karne">
                    <div class="baslik">1. DARGEÇİT MATEMATİK OLİMPİYATI</div>
                    <div class="kimlik"><span>{row['Ad']} {row['Soyad']}</span><span>No: {row['Öğrenci No']}</span></div>
                    <div class="kimlik" style="color:#555; font-size:9px;"><span>{row['OKUL ADI']}</span><span>{row['Sınıf']}/{row['Şube']}</span></div>
                    <div class="sira">İlçe Sırası: {row['İlçe Sırası']} | Okul Sırası: {row['Okul Sırası']}</div>
                    <table class="tablo">
                        <tr><th>D</th><th>Y</th><th>B</th><th>Net</th><th>Puan</th></tr>
                        <tr><td>{row['Doğru']}</td><td>{row['Yanlış']}</td><td>{row['Boş']}</td><td>{row['Net']}</td><td style="background:#fef08a;">{row['Puan']}</td></tr>
                    </table>
                    <table class="optik"><tr>{th_tags}</tr><tr>{st_tags}</tr></table>
                    <div class="yorum">Başarılar dileriz...</div>
                </div>
                """
                if (i + 1) % 6 == 0 or i == len(f_df) - 1: html_karne += "</div>"
            
            html_karne += "</body></html>"
            col_btn2.download_button("📑 Toplu Karneleri Al (PDF)", data=html_karne, file_name=f"{kurum}_Karneler.html", mime="text/html")

            # 3. PROFESYONEL GİRİŞ BELGELERİ (PDF/HTML)
            # (1 sayfada 2 simetrik belge - A5 boyutu gibi)
            belge_df = f_df[f_df['Puan'] >= baraj]
            
            html_belge = """
            <html><head><meta charset="utf-8"><style>
                @page { size: A4; margin: 10mm; }
                body { font-family: Arial, sans-serif; margin: 0; padding: 0; -webkit-print-color-adjust: exact !important; }
                .sayfa { display: flex; flex-direction: column; width: 100%; height: 275mm; page-break-after: always; }
                .belge { width: 100%; height: 128mm; border: 2.5px solid #111827; border-radius: 15px; padding: 25px; margin-bottom: 10mm; box-sizing: border-box; position: relative; background-image: radial-gradient(#f3f4f6 1px, transparent 1px); background-size: 20px 20px; }
                .belge-baslik { text-align: center; border-bottom: 4px solid #E30A17; padding-bottom: 12px; margin-bottom: 15px; }
                .belge-baslik h2 { margin: 0; color: #111827; font-size: 20px; text-transform: uppercase; }
                .belge-baslik h3 { margin: 5px 0 0 0; color: #E30A17; font-size: 16px; font-weight: bold; }
                .b-tablo { width: 100%; border-collapse: collapse; font-size: 14px; margin-bottom: 15px; background: white; }
                .b-tablo td { padding: 10px; border: 1px solid #111827; }
                .b-tablo .etiket { background: #f3f4f6; font-weight: bold; width: 22%; }
                .vurgu-kutu { display: flex; justify-content: space-around; background: #111827; color: white; padding: 15px; border-radius: 10px; margin-bottom: 15px; }
                .kurallar { border: 2px dashed #E30A17; background: white; padding: 15px; border-radius: 10px; font-size: 11.5px; line-height: 1.5; }
                .kurallar b { color: #E30A17; }
            </style></head><body>
            """
            for i, row in belge_df.reset_index().iterrows():
                if i % 2 == 0: html_belge += "<div class='sayfa'>"
                
                html_belge += f"""
                <div class="belge">
                    <div class="belge-baslik">
                        <h2>T.C. DARGEÇİT KAYMAKAMLIĞI</h2>
                        <h3>1. MATEMATİK OLİMPİYATI FİNAL GİRİŞ BELGESİ</h3>
                    </div>
                    <table class="b-tablo">
                        <tr><td class="etiket">Adı Soyadı</td><td style="font-weight:900;">{row['Ad']} {row['Soyad']}</td><td class="etiket">Öğrenci No</td><td style="font-weight:900;">{row['Öğrenci No']}</td></tr>
                        <tr><td class="etiket">Okulu</td><td colspan="3">{row['OKUL ADI']}</td></tr>
                        <tr><td class="etiket">Sınıf / Şube</td><td colspan="3">{row['Sınıf']} / {row['Şube']}</td></tr>
                    </table>
                    <div style="background:white; border:1px solid #ccc; padding:10px; text-align:center; border-radius:8px; margin-bottom:15px; font-size:14px;">
                        📍 <b>Sınav Yeri:</b> Dargeçit Anadolu Lisesi | 📅 <b>Tarih:</b> 18 Mayıs 2026 - 10:00
                    </div>
                    <div class="vurgu-kutu">
                        <span style="font-size:18px;">SALON: <b>{row.get('Salon Adı', 'Belirlenmedi')}</b></span>
                        <span style="font-size:18px;">SIRA: <b>{row.get('Sıra No', 'Belirlenmedi')}</b></span>
                    </div>
                    <div class="kurallar">
                        <b>ÖNEMLİ KURALLAR:</b>
                        <ul style="margin:5px 0 0 0; padding-left:20px;">
                            <li>Sınava gelirken bu belgeyi ve <b>Nüfus Cüzdanınızı</b> getirmek zorunludur.</li>
                            <li>Kendi kurşun kalem ve silginizi getirmelisiniz. Silgi alışverişi yasaktır.</li>
                            <li>Sınav klasik (açık uçlu) sorulardan oluşmaktadır.</li>
                        </ul>
                    </div>
                </div>
                """
                if (i + 1) % 2 == 0 or i == len(belge_df) - 1: html_belge += "</div>"
            
            html_belge += "</body></html>"
            col_btn3.download_button("🎟️ Giriş Belgelerini Al (PDF)", data=html_belge, file_name=f"{kurum}_Giris_Belgeleri.html", mime="text/html")
        elif sifre != "":
            st.error("Hatalı Şifre!")
