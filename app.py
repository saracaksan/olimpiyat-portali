import streamlit as st
import pandas as pd
import io
import ast
import os

# --- EN YÜKSEK KALİTE SAYFA AYARLARI ---
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
    
    /* Yazı Netliği İçin Özel Ayar */
    * { -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }

    /* Üst Banner Tasarımı */
    .header-box {
        background: linear-gradient(135deg, white 0%, #fff5f5 100%);
        padding: 30px; border-bottom: 8px solid var(--meb-red);
        border-radius: 15px; margin-bottom: 35px; text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
    }
    .header-box h1 { color: var(--navy); font-weight: 900; font-size: 36px; margin: 0; letter-spacing: -1px; }
    .header-box h3 { color: var(--meb-red); font-weight: 800; font-size: 20px; margin-top: 5px; text-transform: uppercase; }

    /* Sidebar Etiketi */
    .sidebar-title { color: var(--meb-red); font-weight: 900; font-size: 20px; margin-bottom: 10px; display: block; text-align: center; }
    
    /* Sekme Tasarımı */
    .stTabs [data-baseweb="tab-list"] { gap: 30px; }
    .stTabs [data-baseweb="tab"] { 
        height: 55px; background: white; border-radius: 10px 10px 0 0; 
        font-weight: 800; font-size: 16px; border: 1px solid #ddd;
    }
    .stTabs [aria-selected="true"] { background: var(--meb-red) !important; color: white !important; border: none; }
    </style>
    """, unsafe_allow_html=True)

# --- DETAYLI PEDAGOJİK ANALİZ MOTORU ---
def ogrenci_analizi_uret(row):
    p = row['Puan']
    d = row['Doğru']
    y = row['Yanlış']
    b = row['Boş']
    ad = row['Ad']
    
    if p >= 85:
        return f"Sayın {ad}, sergilediğin üstün performans senin sadece işlem yeteneğini değil, aynı zamanda çok güçlü bir mantıksal muhakeme becerisine sahip olduğunu gösteriyor. {d} doğru sayısıyla olimpiyat standartlarının zirvesindesin. Soruları analiz etme hızın ve doğruluğun takdire şayandır. Bu başarını 2. aşamada da sürdüreceğine inancımız tamdır."
    elif p >= 65:
        return f"Başarılı bir sınav çıkardın {ad}. Matematiksel temelinin oldukça sağlam olduğu görülüyor. {y} yanlışın olması, bazı karmaşık sorularda dikkatinin dağıldığını veya zaman yönetiminde ufak sorunlar yaşadığını gösteriyor. Yanlış yaptığın konuların mantığını tekrar gözden geçirirsen, 2. aşamada ilçe derecesi yapman kaçınılmaz olacaktır."
    elif p >= 40:
        return f"Matematik yolculuğunda önemli bir adım attın. Sınav sonucun temel kavramlara hakim olduğunu ancak yeni nesil mantık sorularında daha fazla pratik yapman gerektiğini gösteriyor. {b} boşun olması, bilmediğin sorularda risk almaman açısından olumlu olsa da, konu eksiklerini tamamladığında bu potansiyelin çok daha yüksek puanlara dönüşecektir."
    else:
        return f"Bu sınav senin için bir tecrübe başlangıcıdır {ad}. {y} yanlışın doğru sayını etkilemiş olması, soruları çözerken daha dikkatli olman ve bol bol deneme çözerek işlem hatasını azaltman gerektiğini kanıtlıyor. Unutma ki matematik pes etmeyenlerin alanıdır; bu eksiklerini kapatarak bir sonraki sınavda çok daha ileriye gidebilirsin."

# --- VERİ VE SINIF SEÇİMİ ---
with st.sidebar:
    st.markdown('<span class="sidebar-title">📐 KATEGORİ SEÇİNİZ</span>', unsafe_allow_html=True)
    sinif_listesi = [f"{i}. Sınıf" for i in range(4, 13)]
    secilen_sinif = st.selectbox("İşlem yapılacak sınıf:", sinif_listesi, index=3)
    sinif_no = secilen_sinif.split(".")[0]
    aktif_dosya = f"sonuclar_{sinif_no}.xlsx"

@st.cache_data
def veriyi_oku(dosya):
    if not os.path.exists(dosya): return None
    df = pd.read_excel(dosya)
    df['Arama_No'] = df['Öğrenci No'].astype(str).str.lstrip('0').str.split('.').str[0]
    df = df.sort_values(by=['Puan', 'Net'], ascending=[False, False]).reset_index(drop=True)
    return df

df = veriyi_oku(aktif_dosya)

if df is None:
    st.warning(f"⚠️ {secilen_sinif} verileri henüz hazır değil.")
else:
    t1, t2 = st.tabs(["👤 Öğrenci Sorgulama", "🏫 İdareci Paneli"])

    with t1:
        st.markdown(f"### 🔍 {secilen_sinif} Bireysel Sonuç Paneli")
        c1, c2 = st.columns(2)
        with c1: okul = st.selectbox("Okulunuz:", sorted(df['OKUL ADI'].unique()), key="o1")
        with c2: no = st.text_input("Okul Numaranız:", key="n1").lstrip('0')

        if st.button("Sonucu Görüntüle", type="primary"):
            sonuc = df[(df['OKUL ADI'] == okul) & (df['Arama_No'] == no)]
            if not sonuc.empty:
                st.balloons()
                o = sonuc.iloc[0]
                analiz_metni = ogrenci_analizi_uret(o)
                st.markdown(f"""
                <div style="background:white; padding:40px; border-radius:20px; border-top:12px solid var(--meb-red); box-shadow:0 15px 40px rgba(0,0,0,0.15);">
                    <h1 style="color:var(--navy); margin:0;">{o['Ad']} {o['Soyad']}</h1>
                    <p style="font-size:20px; color:#555;">{o['OKUL ADI']} | Sınıf: {o['Sınıf']}/{o['Şube']}</p>
                    <div style="display:flex; gap:15px; margin:20px 0;">
                        <div style="background:var(--navy); color:white; padding:10px 20px; border-radius:8px;">İlçe Sırası: {o['İlçe Sırası']}</div>
                        <div style="background:var(--meb-red); color:white; padding:10px 20px; border-radius:8px;">Okul Sırası: {o['Okul Sırası']}</div>
                    </div>
                    <hr>
                    <div style="display:grid; grid-template-columns: repeat(5, 1fr); gap:20px; text-align:center; margin-top:20px;">
                        <div style="background:#f1f5f9; padding:20px; border-radius:12px;"><b>Doğru</b><br><span style="font-size:32px; color:#059669;">{o['Doğru']}</span></div>
                        <div style="background:#f1f5f9; padding:20px; border-radius:12px;"><b>Yanlış</b><br><span style="font-size:32px; color:var(--meb-red);">{o['Yanlış']}</span></div>
                        <div style="background:#f1f5f9; padding:20px; border-radius:12px;"><b>Boş</b><br><span style="font-size:32px; color:#64748b;">{o['Boş']}</span></div>
                        <div style="background:#f1f5f9; padding:20px; border-radius:12px;"><b>Net</b><br><span style="font-size:32px; color:#2563eb;">{o['Net']}</span></div>
                        <div style="background:var(--navy); padding:20px; border-radius:12px; color:white;"><b>Puan</b><br><span style="font-size:32px; font-weight:900;">{o['Puan']}</span></div>
                    </div>
                    <div style="margin-top:30px; padding:20px; background:#fff5f5; border-left:8px solid var(--meb-red); border-radius:8px; line-height:1.6; font-size:16px;">
                        <b>🎓 Başarı Analizi:</b> {analiz_metni}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else: st.error("❌ Bilgiler eşleşmedi.")

    with t2:
        st.markdown(f"### 🏫 {secilen_sinif} İdareci & Toplu İşlem Merkezi")
        sifre = st.text_input("Giriş Şifresi:", type="password", key="adm_s")
        if sifre == "darder47":
            c_a1, c_a2 = st.columns([2, 1])
            with c_a1: kurum = st.selectbox("Okul Filtrele:", ["Tüm İlçe"] + sorted(df['OKUL ADI'].unique()), key="k1")
            with c_a2: baraj = st.number_input("Baraj Puanı:", value=75)
            
            f_df = df if kurum == "Tüm İlçe" else df[df['OKUL ADI'] == kurum]
            st.dataframe(f_df, use_container_width=True)

            col_btn1, col_btn2, col_btn3 = st.columns(3)
            
            # --- PROFESYONEL KARNE HTML (1 SAYFADA 6 ADET) ---
            html_karne = """
            <html><head><meta charset="utf-8"><style>
                @page { size: A4 portrait; margin: 5mm; }
                * { box-sizing: border-box; -webkit-print-color-adjust: exact !important; }
                body { font-family: 'Segoe UI', Arial, sans-serif; background: white; padding: 0; margin: 0; }
                .page { width: 100%; height: 287mm; display: flex; flex-wrap: wrap; justify-content: center; align-content: center; page-break-after: always; padding: 10mm; }
                .karne { 
                    width: 92mm; height: 86mm; border: 2.5px solid #111827; border-radius: 12px; 
                    padding: 12px; margin: 4mm; position: relative; overflow: hidden; background: white;
                }
                .baslik { color: #E30A17; text-align: center; font-weight: 900; font-size: 13px; border-bottom: 2px solid #eee; padding-bottom: 5px; margin-bottom: 10px; }
                .kimlik { display: flex; justify-content: space-between; font-weight: 800; font-size: 11px; margin-bottom: 6px; }
                .siralama { text-align: center; background: #111827; color: white; padding: 4px; border-radius: 6px; font-size: 10px; margin-bottom: 8px; font-weight: bold; }
                .stats { width: 100%; border-collapse: collapse; text-align: center; margin-bottom: 8px; font-size: 11px; }
                .stats td { border: 1.5px solid #ddd; padding: 4px; font-weight: 900; }
                .optik { width: 100%; border-collapse: collapse; text-align: center; font-size: 8px; table-layout: fixed; }
                .optik th, .optik td { border: 1px solid #ccc; height: 16px; font-weight: 900; }
                .dogru { background: #dcfce7 !important; color: #059669; }
                .yanlis { background: #fee2e2 !important; color: #E30A17; }
                .analiz-notu { 
                    position: absolute; bottom: 8px; left: 10px; right: 10px; 
                    font-size: 8.5px; font-style: italic; line-height: 1.2; font-weight: 600;
                    background: #f8fafc; padding: 6px; border-left: 3px solid #E30A17; 
                }
            </style></head><body>
            """
            for i, row in f_df.reset_index().iterrows():
                if i % 6 == 0: html_karne += "<div class='page'>"
                try:
                    ogr_cvp = ast.literal_eval(row['Ogrenci_Cevap_Listesi'])
                    key_cvp = ast.literal_eval(row['Cevap_Anahtari_Listesi'])
                except: ogr_cvp = ["-"]*20; key_cvp = ["-"]*20
                
                st_tags = ""
                for j in range(20):
                    c, k = (ogr_cvp[j] if j < len(ogr_cvp) else "-"), (key_cvp[j] if j < len(key_cvp) else "-")
                    if c == k and c != "-": st_tags += f"<td class='dogru'>{c}</td>"
                    elif c != k and c != "-": st_tags += f"<td class='yanlis'>{c}</td>"
                    else: st_tags += f"<td>-</td>"

                html_karne += f"""
                <div class="karne">
                    <div class="baslik">1. DARGEÇİT MATEMATİK OLİMPİYATI</div>
                    <div class="kimlik"><span>{row['Ad']} {row['Soyad']}</span><span>No: {row['Öğrenci No']}</span></div>
                    <div class="kimlik" style="color:#555; font-size:9px;"><span>{row['OKUL ADI']}</span><span>{row['Sınıf']}/{row['Şube']}</span></div>
                    <div class="siralama">İlçe: {row['İlçe Sırası']} | Okul: {row['Okul Sırası']}</div>
                    <table class="stats">
                        <tr><td style="background:#f8fafc;">D: {row['Doğru']}</td><td style="background:#f8fafc;">Y: {row['Yanlış']}</td><td style="background:#fef08a; font-size:14px;">Puan: {row['Puan']}</td></tr>
                    </table>
                    <table class="optik"><tr>{"".join([f"<th>{j+1}</th>" for j in range(20)])}</tr><tr>{st_tags}</tr></table>
                    <div class="analiz-notu">{ogrenci_analizi_uret(row)[:160]}...</div>
                </div>
                """
                if (i + 1) % 6 == 0 or i == len(f_df) - 1: html_karne += "</div>"
            
            html_karne += "</body></html>"
            col_btn2.download_button("📑 Toplu Karneleri Al (6'lı)", data=html_karne, file_name=f"{kurum}_Karneler.html", mime="text/html")

            # --- PROFESYONEL GİRİŞ BELGESİ (MEB FORMATI - 1 SAYFADA 2 ADET) ---
            belge_df = f_df[f_df['Puan'] >= baraj]
            html_belge = """
            <html><head><meta charset="utf-8"><style>
                @page { size: A4; margin: 10mm; }
                * { box-sizing: border-box; -webkit-print-color-adjust: exact !important; }
                body { font-family: 'Segoe UI', Tahoma, sans-serif; background: white; margin: 0; padding: 0; }
                .sayfa { display: flex; flex-direction: column; justify-content: center; width: 100%; height: 285mm; page-break-after: always; padding: 10mm; }
                .belge { 
                    width: 100%; height: 130mm; border: 3px solid #111827; border-radius: 20px; padding: 30px; 
                    margin-bottom: 10mm; position: relative; background: #fff;
                    background-image: url('https://www.transparenttextures.com/patterns/cubes.png');
                }
                .b-header { text-align: center; border-bottom: 5px solid #E30A17; padding-bottom: 15px; margin-bottom: 20px; }
                .b-header h2 { margin: 0; color: #111827; font-size: 22px; font-weight: 900; }
                .b-header h3 { margin: 5px 0 0 0; color: #E30A17; font-size: 16px; }
                .b-tablo { width: 100%; border-collapse: collapse; font-size: 15px; margin-bottom: 20px; }
                .b-tablo td { padding: 12px; border: 2px solid #111827; font-weight: 800; }
                .b-tablo .lbl { background: #f1f5f9; width: 25%; font-weight: bold; color: #444; }
                .vurgu { display: flex; justify-content: space-around; background: #111827; color: white; padding: 15px; border-radius: 12px; margin-bottom: 20px; font-size: 20px; font-weight: 900; }
                .rules { border: 2px dashed #E30A17; padding: 15px; border-radius: 12px; font-size: 12px; line-height: 1.4; color: #111827; }
                .rules b { color: #E30A17; font-size: 14px; display: block; margin-bottom: 5px; text-align: center; }
            </style></head><body>
            """
            for i, row in belge_df.reset_index().iterrows():
                if i % 2 == 0: html_belge += "<div class='sayfa'>"
                html_belge += f"""
                <div class="belge">
                    <div class="b-header">
                        <h2>T.C. DARGEÇİT KAYMAKAMLIĞI</h2>
                        <h2>1. MATEMATİK OLİMPİYATI FİNAL GİRİŞ BELGESİ</h2>
                    </div>
                    <table class="b-tablo">
                        <tr><td class="lbl">Adı Soyadı</td><td>{row['Ad']} {row['Soyad']}</td><td class="lbl">Öğrenci No</td><td>{row['Öğrenci No']}</td></tr>
                        <tr><td class="lbl">Okul Adı</td><td colspan="3">{row['OKUL ADI']}</td></tr>
                        <tr><td class="lbl">Sınıf/Şube</td><td colspan="3">{row['Sınıf']} / {row['Şube']}</td></tr>
                    </table>
                    <div style="text-align:center; margin-bottom:15px; font-weight:bold; font-size:16px;">
                        📍 Sınav Yeri: Dargeçit Anadolu Lisesi | 📅 Tarih: 18 Mayıs 2026 - 10:00
                    </div>
                    <div class="vurgu">
                        <span>SALON: {row.get('Salon Adı', 'MERKEZ-1')}</span>
                        <span>SIRA: {row.get('Sıra No', '1')}</span>
                    </div>
                    <div class="rules">
                        <b>⚠️ ÖNEMLİ SINAV KURALLARI</b>
                        • Sınava gelirken bu belgeyi ve <b>Geçerli Kimlik Belgenizi</b> mutlaka yanınızda bulundurunuz.<br>
                        • Öğrenciler kendi kurşun kalem ve silgilerini getirmelidir; <b>silgi alışverişi kesinlikle yasaktır.</b><br>
                        • Sınav 10 klasik sorudan oluşmaktadır. İlk 30 dakika salondan çıkılamaz.
                    </div>
                </div>
                """
                if (i + 1) % 2 == 0 or i == len(belge_df) - 1: html_belge += "</div>"
            
            html_belge += "</body></html>"
            col_btn3.download_button("🎟️ Giriş Belgelerini Al (2'li)", data=html_belge, file_name=f"{kurum}_Giris_Belgeleri.html", mime="text/html")
