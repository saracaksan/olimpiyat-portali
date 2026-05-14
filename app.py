import streamlit as st
import pandas as pd
import io
import ast
import os
import plotly.express as px

# ─────────────────────────────────────────────────────────────────────────────
# SAYFA AYARLARI
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="1. Dargeçit Matematik Olimpiyatı",
    layout="wide",
    page_icon="🥇",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS — Mobil + Masaüstü tam uyumlu, profesyonel MEB teması
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;800;900&family=Playfair+Display:wght@700&display=swap');

:root {
    --red:    #E30A17;
    --navy:   #111827;
    --teal:   #0d9488;
    --gold:   #f59e0b;
    --bg:     #f0f4f8;
    --card:   #ffffff;
    --border: #e2e8f0;
    --muted:  #64748b;
    --green:  #059669;
    --blue:   #2563eb;
}

/* ── Global ── */
html, body, [class*="css"] { font-family: 'Nunito', sans-serif !important; }
.main { background: var(--bg) !important; }
.block-container { padding-top: 1rem !important; max-width: 1100px; }

/* ── Hero Banner ── */
.hero-banner {
    background: linear-gradient(135deg, var(--navy) 0%, #1e3a5f 60%, #0d9488 100%);
    border-radius: 18px;
    padding: clamp(20px,4vw,36px) clamp(20px,5vw,48px);
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 12px 40px rgba(0,0,0,0.18);
}
.hero-banner::before {
    content: "🏆";
    position: absolute; right: 30px; top: 50%;
    transform: translateY(-50%);
    font-size: clamp(60px,10vw,100px);
    opacity: 0.12;
    pointer-events: none;
}
.hero-banner h1 {
    color: white; margin: 0;
    font-family: 'Playfair Display', serif;
    font-size: clamp(18px,3.5vw,32px);
    letter-spacing: -0.5px;
    text-shadow: 0 2px 8px rgba(0,0,0,0.3);
}
.hero-banner p {
    color: rgba(255,255,255,0.85);
    font-size: clamp(12px,2vw,15px);
    margin: 6px 0 0;
}
.hero-badge {
    display: inline-block;
    background: var(--red);
    color: white;
    font-size: 11px; font-weight: 900;
    padding: 3px 10px; border-radius: 20px;
    letter-spacing: 1px; text-transform: uppercase;
    margin-bottom: 10px;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--navy);
    border-radius: 12px 12px 0 0;
    padding: 6px 8px 0;
    gap: 4px;
    flex-wrap: wrap;
}
.stTabs [data-baseweb="tab"] {
    background: rgba(255,255,255,0.08) !important;
    color: rgba(255,255,255,0.7) !important;
    border-radius: 8px 8px 0 0 !important;
    font-weight: 800 !important;
    font-size: clamp(12px,2vw,14px) !important;
    padding: 10px 18px !important;
    border: none !important;
    transition: all 0.2s;
}
.stTabs [aria-selected="true"] {
    background: white !important;
    color: var(--navy) !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: white;
    border-radius: 0 12px 12px 12px;
    padding: clamp(14px,3vw,28px);
    border: 1px solid var(--border);
    box-shadow: 0 8px 32px rgba(0,0,0,0.07);
}

/* ── Tab açıklaması ── */
.tab-info {
    background: linear-gradient(135deg, #eff6ff, #f0fdf4);
    border: 1.5px solid #bfdbfe;
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 22px;
    display: flex;
    align-items: flex-start;
    gap: 12px;
}
.tab-info .tab-icon { font-size: 28px; flex-shrink: 0; }
.tab-info h4 { margin: 0 0 4px; color: var(--navy); font-size: 15px; }
.tab-info p  { margin: 0; color: var(--muted); font-size: 13px; line-height: 1.5; }

/* ── Arama Paneli ── */
.search-panel {
    background: linear-gradient(135deg, #f8fafc, #eff6ff);
    border: 2px solid #c7d2fe;
    border-top: 5px solid var(--navy);
    border-radius: 14px;
    padding: clamp(16px,3vw,28px);
    margin-bottom: 24px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
}
.search-panel h3 {
    margin: 0 0 16px;
    color: var(--navy);
    font-size: 16px;
    display: flex; align-items: center; gap: 8px;
}
.step-label {
    display: block;
    font-size: 11px; font-weight: 900; letter-spacing: 1px;
    color: var(--muted); text-transform: uppercase;
    margin-bottom: 4px;
}

/* ── Buton ── */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, var(--navy), #1e3a5f) !important;
    color: white !important;
    font-weight: 900 !important;
    font-size: 15px !important;
    height: 52px !important;
    border-radius: 10px !important;
    border: none !important;
    letter-spacing: 0.5px;
    box-shadow: 0 4px 15px rgba(17,24,39,0.3) !important;
    transition: all 0.25s !important;
    margin-top: 8px;
}
.stButton > button:hover {
    background: linear-gradient(135deg, var(--red), #c00) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(227,10,23,0.35) !important;
}

/* ── Karne Kartı ── */
.karne-card {
    background: white;
    border-radius: 16px;
    border: 1px solid var(--border);
    border-top: 6px solid var(--red);
    box-shadow: 0 12px 40px rgba(0,0,0,0.1);
    overflow: hidden;
    margin-bottom: 20px;
}
.karne-header {
    padding: 18px 22px;
    border-bottom: 2px solid var(--border);
    background: linear-gradient(135deg, #f8fafc, white);
}
.karne-body { padding: 20px 22px; }
.karne-name {
    font-family: 'Playfair Display', serif;
    font-size: clamp(20px,4vw,28px);
    color: var(--navy); margin: 0;
}
.karne-school {
    color: var(--red); font-weight: 800;
    font-size: clamp(13px,2vw,15px); margin: 2px 0 0;
}
.karne-no-badge {
    background: var(--navy); color: white;
    padding: 6px 14px; border-radius: 8px;
    font-weight: 900; font-size: 13px;
    white-space: nowrap;
}

/* ── Metrik Kutuları ── */
.metric-row {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 10px; margin: 16px 0;
}
@media (max-width: 500px) {
    .metric-row { grid-template-columns: repeat(3, 1fr); }
}
.metric-box {
    background: #f8fafc; border: 1.5px solid var(--border);
    border-radius: 10px; padding: 12px 6px;
    text-align: center;
}
.metric-box .m-label {
    font-size: 10px; font-weight: 900; color: var(--muted);
    text-transform: uppercase; letter-spacing: 0.5px;
    display: block; margin-bottom: 4px;
}
.metric-box .m-value {
    font-size: clamp(20px,4vw,26px);
    font-weight: 900; display: block;
}
.metric-box.puan-box {
    background: var(--navy); border-color: var(--navy);
}
.metric-box.puan-box .m-label { color: #94a3b8; }
.metric-box.puan-box .m-value { color: white; }

/* ── Optik Tablo ── */
.optik-wrap {
    overflow-x: auto; -webkit-overflow-scrolling: touch;
    border-radius: 10px; border: 1.5px solid var(--border);
    margin: 14px 0;
}
.optik-wrap::-webkit-scrollbar { height: 4px; }
.optik-wrap::-webkit-scrollbar-thumb { background: var(--navy); border-radius: 2px; }
.optik-table {
    width: 100%; border-collapse: collapse;
    font-size: 11px; text-align: center;
    min-width: 640px;
}
.optik-table th {
    background: var(--navy); color: white;
    padding: 7px 4px; border: 1px solid #334155;
    font-size: 10px;
}
.optik-table td { padding: 7px 4px; border: 1px solid var(--border); font-weight: 800; }
.optik-table .row-label {
    background: #f1f5f9 !important; color: var(--navy) !important;
    text-align: left; padding-left: 8px; font-size: 10px;
    min-width: 90px; font-weight: 900;
}
.dogru { background: #dcfce7 !important; color: #166534 !important; }
.yanlis { background: var(--navy) !important; color: white !important; }

/* ── Pedagojik Alan ── */
.rehber-box {
    background: linear-gradient(135deg, #fffafa, #fff7ed);
    border-left: 5px solid var(--red);
    border: 1px solid #fee2e2;
    border-left-width: 5px;
    border-radius: 10px;
    padding: 18px 20px;
    font-size: 14px; line-height: 1.75;
    color: #1e293b; text-align: justify;
    margin-top: 16px;
}
.rehber-box h3 { margin: 0 0 12px; color: var(--red); font-size: 15px; }

/* ── Sıralama rozetleri ── */
.siralama-bar {
    display: flex; flex-wrap: wrap; gap: 8px;
    margin: 10px 0 16px;
}
.sir-badge {
    padding: 5px 14px; border-radius: 20px;
    font-size: 12px; font-weight: 900;
}

/* ── İdare Metrik ── */
.idare-metric {
    background: white; border: 1.5px solid var(--border);
    border-radius: 12px; padding: 16px 12px;
    text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}
.idare-metric .im-label { font-size: 11px; color: var(--muted); font-weight: 800; text-transform: uppercase; display: block; }
.idare-metric .im-value { font-size: clamp(22px,4vw,30px); font-weight: 900; color: var(--navy); display: block; }

/* ── İndirme Butonu ── */
.stDownloadButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, var(--teal), #0f766e) !important;
    color: white !important;
    font-weight: 900 !important;
    border-radius: 10px !important;
    height: 52px !important;
    border: none !important;
    font-size: 14px !important;
    box-shadow: 0 4px 14px rgba(13,148,136,0.3) !important;
    transition: all 0.25s !important;
}
.stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(13,148,136,0.45) !important;
}

/* ── Yorum Kutuları ── */
.yorum-box {
    border-radius: 12px;
    padding: 16px 18px;
    font-size: 14px; line-height: 1.7;
    margin: 16px 0;
}
.yorum-navy  { background: #f8fafc; border-left: 6px solid var(--navy); }
.yorum-red   { background: #fff5f5; border-left: 6px solid var(--red);  }
.yorum-green { background: #f0fdf4; border-left: 6px solid var(--green);}

/* ── Filtre Paneli ── */
.filter-panel {
    background: #f8fafc; border: 1.5px solid var(--border);
    border-radius: 12px; padding: 18px 20px; margin-bottom: 20px;
}

/* ── Selectbox / Input ── */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] input {
    border-radius: 8px !important;
    border-color: #c7d2fe !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# HERO BANNER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-badge">T.C. Dargeçit Kaymakamlığı</div>
    <h1>1. Dargeçit Matematik Olimpiyatı</h1>
    <p>Bireysel Sonuç Sorgulama · Pedagojik Karne · Kurumsal Analiz Portalı</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PEDAGOJİK ANALİZ MOTORU (DOKUNULMADI — ÖZGÜN METİN KORUNDU)
# ─────────────────────────────────────────────────────────────────────────────
def detayli_pedagojik_analiz(row):
    p, d, y, b, ad = row['Puan'], row['Doğru'], row['Yanlış'], row['Boş'], row['Ad']
    giris = f"Sevgili <b>{ad}</b>,<br><br>"
    felsefe = ("Matematik; sadece rakamlarla yapılan işlemler bütünü değil, evrenin karmaşık yapısını ve mantığını anlamamızı sağlayan "
               "en zarif dildir. Analitik düşünme becerisi, hayatta karşılaştığın her problemde sana en doğru yolu gösterecek olan bir pusuladır. "
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

# ─────────────────────────────────────────────────────────────────────────────
# VERİ YÜKLEME
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def verileri_yukle():
    mevcut_dosyalar = os.listdir('.')
    liste = []
    for d in mevcut_dosyalar:
        if "sonuc" in d.lower() or "sonuç" in d.lower():
            try:
                if d.lower().endswith('.csv'):
                    df = pd.read_csv(d, sep=',', quotechar='"', on_bad_lines='skip')
                elif d.lower().endswith(('.xlsx', '.xls')):
                    df = pd.read_excel(d)
                else:
                    continue
                if 'Puan' in df.columns and 'Öğrenci No' in df.columns:
                    df['Arama_No'] = (df['Öğrenci No'].astype(str)
                                       .str.replace('.0', '', regex=False)
                                       .str.strip().str.lstrip('0'))
                    df['Sınıf'] = (df['Sınıf'].astype(str)
                                   .str.replace('.0', '', regex=False).str.strip())
                    liste.append(df)
            except Exception:
                pass
    if liste:
        birlesik = pd.concat(liste, ignore_index=True)
        birlesik = birlesik.drop_duplicates(subset=['Öğrenci No', 'OKUL ADI', 'Sınıf'])
        return (birlesik.sort_values(['Puan', 'Net'], ascending=[False, False])
                        .reset_index(drop=True))
    return pd.DataFrame()

df_tum = verileri_yukle()

# ─────────────────────────────────────────────────────────────────────────────
# YARDIMCI: Optik satırları oluştur
# ─────────────────────────────────────────────────────────────────────────────
def optik_satirlari(row):
    try:
        ogr_cvp = ast.literal_eval(str(row.get('Ogrenci_Cevap_Listesi', "['-']*20")))
        key_cvp = ast.literal_eval(str(row.get('Cevap_Anahtari_Listesi', "['-']*20")))
    except Exception:
        ogr_cvp = ['-'] * 20
        key_cvp = ['-'] * 20

    th = "".join(f"<th>{j+1}</th>" for j in range(20))
    key_row = "".join(f"<td>{key_cvp[j] if j < len(key_cvp) else '-'}</td>" for j in range(20))
    ogr_row = ""
    for j in range(20):
        c = ogr_cvp[j] if j < len(ogr_cvp) else '-'
        k = key_cvp[j] if j < len(key_cvp) else '-'
        if c == k and c != '-':
            ogr_row += f"<td class='dogru'>{c}</td>"
        elif c != k and c != '-':
            ogr_row += f"<td class='yanlis'>{c}</td>"
        else:
            ogr_row += f"<td>{c}</td>"
    return th, key_row, ogr_row

# ─────────────────────────────────────────────────────────────────────────────
# YARDIMCI: Bireysel karne HTML (PDF indirme için)
# ─────────────────────────────────────────────────────────────────────────────
def bireysel_karne_html(o, analiz_html, th, key_row, ogr_row):
    return f"""<!DOCTYPE html>
<html lang="tr"><head><meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;900&family=Playfair+Display:wght@700&display=swap');
@page {{ size: A4 portrait; margin: 12mm; }}
* {{ box-sizing: border-box; }}
body {{ font-family:'Nunito',sans-serif; margin:0; padding:0; background:white; -webkit-print-color-adjust:exact !important; }}
.wrap {{ border:4px solid #111827; border-radius:16px; padding:22px; background:white; }}
.hdr {{ text-align:center; border-bottom:3px solid #E30A17; padding-bottom:10px; margin-bottom:14px; }}
.hdr h1 {{ margin:0; font-family:'Playfair Display',serif; font-size:18px; color:#111827; }}
.hdr h2 {{ margin:4px 0 0; color:#E30A17; font-size:14px; font-weight:900; }}
.info {{ display:flex; justify-content:space-between; flex-wrap:wrap; gap:6px; font-size:13px; font-weight:700; background:#f8fafc; padding:10px 14px; border-radius:8px; margin-bottom:12px; }}
.info span {{ color:#111827; }}
.info .red {{ color:#E30A17; }}
.stats {{ width:100%; border-collapse:collapse; text-align:center; margin-bottom:12px; }}
.stats th {{ background:#111827; color:white; padding:8px; font-size:13px; border:1px solid #111827; }}
.stats td {{ padding:10px; font-size:22px; font-weight:900; border:1px solid #cbd5e1; }}
.optik-t {{ width:100%; border-collapse:collapse; text-align:center; font-size:11px; margin-bottom:12px; }}
.optik-t th {{ background:#fef2f2; border:1px solid #fca5a5; padding:5px; color:#E30A17; font-size:10px; }}
.optik-t td {{ border:1px solid #fca5a5; padding:6px; font-weight:800; font-size:12px; }}
.optik-t .lbl {{ background:#111827; color:white; text-align:left; padding-left:8px; min-width:80px; }}
.optik-t .lbl2 {{ background:#f1f5f9; color:#111827; text-align:left; padding-left:8px; font-size:10px; }}
.dogru {{ background:#dcfce7 !important; color:#059669 !important; }}
.yanlis {{ background:#111827 !important; color:white !important; }}
.analiz {{ background:#fffafa; border-left:6px solid #E30A17; border:1px solid #fee2e2; border-left-width:6px; padding:14px 16px; font-size:12.5px; line-height:1.6; text-align:justify; border-radius:8px; }}
.analiz h3 {{ margin:0 0 8px; color:#E30A17; font-size:14px; }}
.imza {{ text-align:center; margin-top:12px; font-weight:900; font-size:12px; color:#64748b; }}
</style></head><body>
<div class="wrap">
  <div class="hdr">
    <h1>1. DARGEÇİT MATEMATİK OLİMPİYATI</h1>
    <h2>RESMİ SINAV SONUÇ BELGESİ</h2>
  </div>
  <div class="info">
    <span>{o['Ad']} {o['Soyad']}</span>
    <span>{o['OKUL ADI']} · Sınıf: {o['Sınıf']}/{o['Şube']}</span>
    <span class="red">No: {o['Öğrenci No']} &nbsp;|&nbsp; İlçe S: {o.get('İlçe Sırası','-')} &nbsp;|&nbsp; Okul S: {o.get('Okul Sırası','-')}</span>
  </div>
  <table class="stats">
    <tr><th>Doğru</th><th>Yanlış</th><th>Boş</th><th>Net</th><th style="background:#E30A17;">PUAN</th></tr>
    <tr>
      <td style="color:#059669;">{o['Doğru']}</td>
      <td style="color:#E30A17;">{o['Yanlış']}</td>
      <td>{o['Boş']}</td>
      <td style="color:#2563eb;">{o['Net']}</td>
      <td style="background:#111827;color:white;">{o['Puan']}</td>
    </tr>
  </table>
  <table class="optik-t">
    <tr><th class="lbl">Soru No</th>{th}</tr>
    <tr><th class="lbl2">Cevap Anahtarı</th>{key_row}</tr>
    <tr><th class="lbl2">Öğrenci Cevabı</th>{ogr_row}</tr>
  </table>
  <div class="analiz">
    <h3>🎓 Uzman Pedagojik Değerlendirme</h3>
    {analiz_html}
  </div>
  <div class="imza">Dargeçit İlçe Milli Eğitim Müdürlüğü</div>
</div>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# YARDIMCI: Toplu karne HTML — A4'te 2'li (tam düzeltilmiş)
# ─────────────────────────────────────────────────────────────────────────────
def toplu_karne_html(df_export, baslik_metni):
    css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;900&family=Playfair+Display:wght@700&display=swap');
@page { size: A4 portrait; margin: 8mm; }
* { box-sizing: border-box; }
body { font-family:'Nunito',sans-serif; margin:0; padding:0; background:white; -webkit-print-color-adjust:exact !important; }
.sayfa { width:100%; height:277mm; display:flex; flex-direction:column; gap:4mm; page-break-after:always; }
.sayfa:last-child { page-break-after:auto; }
.karne {
    width:100%; height:136mm; border:2.5px solid #E30A17; border-radius:12px;
    padding:8px 10px; overflow:hidden; display:flex; flex-direction:column; gap:3px;
    page-break-inside:avoid;
}
.k-baslik { text-align:center; font-family:'Playfair Display',serif; font-size:12px; font-weight:700; color:#111827; border-bottom:2px solid #E30A17; padding-bottom:3px; text-transform:uppercase; }
.k-kimlik { display:flex; justify-content:space-between; align-items:center; margin-top:2px; }
.k-kimlik .isim { font-weight:900; font-size:12px; color:#111827; }
.k-kimlik .no   { background:#E30A17; color:white; padding:2px 8px; border-radius:6px; font-size:10px; font-weight:900; }
.k-alt { display:flex; justify-content:space-between; font-size:10px; font-weight:700; color:#555; }
.k-sira { text-align:center; background:#111827; color:white; padding:2px; border-radius:5px; font-size:10px; font-weight:900; }
.stats { width:100%; border-collapse:collapse; text-align:center; font-size:10px; }
.stats th { background:#fef2f2; border:1px solid #fca5a5; padding:3px; color:#E30A17; font-weight:900; }
.stats td { border:1px solid #fca5a5; padding:3px; font-weight:900; font-size:14px; }
.optik { width:100%; border-collapse:collapse; text-align:center; font-size:9px; }
.optik th { background:#fef2f2; border:1px solid #fca5a5; padding:2px; color:#E30A17; font-size:9px; }
.optik td { border:1px solid #fca5a5; padding:2px; font-weight:800; font-size:10px; }
.optik .lbl  { background:#111827; color:white; text-align:left; padding-left:5px; width:70px; }
.optik .lbl2 { background:#f1f5f9; color:#111827; text-align:left; padding-left:5px; font-size:8px; }
.dogru  { background:#dcfce7 !important; color:#059669 !important; }
.yanlis { background:#111827 !important; color:white !important; }
.analiz {
    background:#fffafa; border-left:4px solid #E30A17;
    border:1px solid #fee2e2; border-left-width:4px;
    padding:6px 8px; font-size:9.5px; line-height:1.3;
    text-align:justify; border-radius:6px; flex-grow:1;
    overflow:hidden;
}
.analiz b { color:#E30A17; font-size:10px; }
.imza { text-align:center; font-weight:900; font-size:9px; color:#64748b; margin-top:auto; padding-top:2px; }
</style>"""

    html = f"<!DOCTYPE html><html lang='tr'><head><meta charset='utf-8'>{css}</head><body>"
    satirlar = df_export.reset_index(drop=True)

    for i, row in satirlar.iterrows():
        if i % 2 == 0:
            html += "<div class='sayfa'>"

        analiz = detayli_pedagojik_analiz(row)
        th, key_row, ogr_row = optik_satirlari(row)

        html += f"""
<div class="karne">
  <div class="k-baslik">1. Dargeçit Matematik Olimpiyatı — Sonuç Belgesi</div>
  <div class="k-kimlik">
    <span class="isim">{row['Ad']} {row['Soyad']}</span>
    <span class="no">No: {row['Öğrenci No']}</span>
  </div>
  <div class="k-alt">
    <span>{row['OKUL ADI']}</span>
    <span>Sınıf: {row['Sınıf']}/{row['Şube']}</span>
  </div>
  <div class="k-sira">İlçe Sırası: {row.get('İlçe Sırası','-')} &nbsp;|&nbsp; Okul Sırası: {row.get('Okul Sırası','-')}</div>
  <table class="stats">
    <tr><th>Doğru</th><th>Yanlış</th><th>Boş</th><th>Net</th><th style="background:#E30A17;color:white;">PUAN</th></tr>
    <tr>
      <td style="color:#059669;">{row['Doğru']}</td>
      <td style="color:#E30A17;">{row['Yanlış']}</td>
      <td>{row['Boş']}</td>
      <td style="color:#2563eb;">{row['Net']}</td>
      <td style="background:#111827;color:white;">{row['Puan']}</td>
    </tr>
  </table>
  <table class="optik">
    <tr><th class="lbl">Soru No</th>{th}</tr>
    <tr><th class="lbl2">Cevap Anahtarı</th>{key_row}</tr>
    <tr><th class="lbl2">Öğrenci Cevabı</th>{ogr_row}</tr>
  </table>
  <div class="analiz"><b>🎓 Pedagojik Değerlendirme:</b><br>{analiz}</div>
  <div class="imza">Dargeçit İlçe Milli Eğitim Müdürlüğü</div>
</div>"""

        if (i + 1) % 2 == 0 or i == len(satirlar) - 1:
            html += "</div>"

    html += "</body></html>"
    return html

# ─────────────────────────────────────────────────────────────────────────────
# YARDIMCI: Başarı listesi HTML
# ─────────────────────────────────────────────────────────────────────────────
def liste_html(df_export, baslik_metni):
    satirlar = ""
    for _, r in df_export.iterrows():
        bg = "#f8fafc" if _ % 2 == 0 else "white"
        satirlar += f"""<tr style="background:{bg};">
            <td style="text-align:left;">{r['OKUL ADI']}</td>
            <td style="text-align:left;font-weight:900;">{r['Ad']} {r['Soyad']}</td>
            <td>{r['Sınıf']}/{r['Şube']}</td>
            <td>{r['Öğrenci No']}</td>
            <td style="color:#059669;font-weight:900;">{r['Doğru']}</td>
            <td style="color:#E30A17;font-weight:900;">{r['Yanlış']}</td>
            <td>{r['Boş']}</td>
            <td style="color:#2563eb;font-weight:900;">{r['Net']}</td>
            <td style="color:#E30A17;font-weight:900;font-size:15px;">{r['Puan']}</td>
        </tr>"""
    return f"""<!DOCTYPE html><html lang="tr"><head><meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;900&display=swap');
body {{ font-family:'Nunito',sans-serif; padding:20px; font-size:12px; }}
.hdr {{ text-align:center; border-bottom:3px solid #111827; margin-bottom:20px; padding-bottom:10px; }}
.hdr h1 {{ margin:0; font-size:16px; color:#111827; }}
.hdr h2 {{ margin:4px 0 0; color:#E30A17; font-size:13px; font-weight:900; }}
.hdr p  {{ margin:2px 0 0; color:#64748b; font-size:11px; }}
table {{ width:100%; border-collapse:collapse; text-align:center; }}
th {{ background:#111827; color:white; padding:9px 6px; border:1px solid #111827; font-size:11px; }}
td {{ border:1px solid #e2e8f0; padding:7px 5px; }}
</style></head><body>
<div class="hdr">
  <h1>T.C. DARGEÇİT KAYMAKAMLIĞI</h1>
  <h2>1. MATEMATİK OLİMPİYATI — {baslik_metni.upper()} BAŞARI LİSTESİ</h2>
  <p>Toplam {len(df_export)} öğrenci · En yüksek puandan düşüğe sıralı</p>
</div>
<table>
<tr><th>Okul</th><th>Ad Soyad</th><th>Sınıf/Şube</th><th>No</th><th>D</th><th>Y</th><th>B</th><th>Net</th><th>Puan</th></tr>
{satirlar}
</table>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# ANA SEKMELER
# ─────────────────────────────────────────────────────────────────────────────
tab_ogrenci, tab_idareci = st.tabs([
    "🎓  Öğrenci Sonuç Sorgulama",
    "🏛️  İdare & Kurumsal Analiz Paneli"
])

# ══════════════════════════════════════════════════════════════════════════════
# SEKME 1 — ÖĞRENCİ SONUÇ SORGULAMA
# ══════════════════════════════════════════════════════════════════════════════
with tab_ogrenci:

    # Tab açıklaması
    st.markdown("""
    <div class="tab-info">
        <div class="tab-icon">🎓</div>
        <div>
            <h4>Bireysel Sonuç Sorgulama & Pedagojik Karne</h4>
            <p>Bu ekrandan <b>sınav sonucunuzu</b> anında görebilir, doğru/yanlış cevaplarınızı karşılaştırabilir
            ve size özel hazırlanmış <b>pedagojik değerlendirme raporunuzu</b> indirebilirsiniz.
            Okulunuzu → Sınıfınızı → Numaranızı seçip butona basmanız yeterlidir.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Arama Paneli
    st.markdown('<div class="search-panel">', unsafe_allow_html=True)
    st.markdown('<h3>🔍 Sonuç Sorgulama Formu</h3>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([3, 2, 2])

    with col1:
        st.markdown('<span class="step-label">1️⃣ Adım — Okul Seçimi</span>', unsafe_allow_html=True)
        okul_listesi = (["— Okulunuzu Seçiniz —"] +
                        sorted(df_tum['OKUL ADI'].dropna().unique().tolist())
                        ) if not df_tum.empty else ["Veri Bulunamadı"]
        secilen_okul = st.selectbox("Okul:", okul_listesi, label_visibility="collapsed")

    with col2:
        st.markdown('<span class="step-label">2️⃣ Adım — Sınıf</span>', unsafe_allow_html=True)
        if secilen_okul not in ["— Okulunuzu Seçiniz —", "Veri Bulunamadı"]:
            siniflar = sorted(df_tum[df_tum['OKUL ADI'] == secilen_okul]['Sınıf'].dropna().unique().tolist())
            sinif_listesi = ["— Sınıf Seçiniz —"] + siniflar
        else:
            sinif_listesi = ["Önce Okul Seçin"]
        secilen_sinif = st.selectbox("Sınıf:", sinif_listesi, label_visibility="collapsed")

    with col3:
        st.markdown('<span class="step-label">3️⃣ Adım — Öğrenci No</span>', unsafe_allow_html=True)
        girilen_no = st.text_input("No:", placeholder="Örn: 145", label_visibility="collapsed").strip().lstrip('0')

    search_btn = st.button("🔎  SONUÇLARIMI GÖSTER", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # SONUÇ
    if search_btn:
        if secilen_okul in ["— Okulunuzu Seçiniz —", "Veri Bulunamadı"]:
            st.warning("⚠️ Lütfen okulunuzu seçiniz.")
        elif secilen_sinif in ["— Sınıf Seçiniz —", "Önce Okul Seçin"]:
            st.warning("⚠️ Lütfen sınıfınızı seçiniz.")
        elif not girilen_no:
            st.error("⚠️ Lütfen öğrenci numaranızı giriniz.")
        else:
            sonuc = df_tum[
                (df_tum['OKUL ADI'] == secilen_okul) &
                (df_tum['Sınıf'] == secilen_sinif) &
                (df_tum['Arama_No'] == girilen_no)
            ]

            if not sonuc.empty:
                st.balloons()
                o = sonuc.iloc[0]
                analiz_html = detayli_pedagojik_analiz(o)
                th, key_row, ogr_row = optik_satirlari(o)

                # ── CANLI KARNE ÖN İZLEMESİ ──────────────────────────────
                st.markdown("---")
                st.markdown("### 📋 Karne Ön İzleme")

                st.markdown(f"""
                <div class="karne-card">

                  <!-- BAŞLIK -->
                  <div class="karne-header" style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:12px;">
                    <div>
                      <p class="karne-name">{o['Ad']} {o['Soyad']}</p>
                      <p class="karne-school">{o['OKUL ADI']} · Sınıf: {o['Sınıf']}/{o['Şube']}</p>
                    </div>
                    <span class="karne-no-badge">No: {o['Öğrenci No']}</span>
                  </div>

                  <div class="karne-body">

                    <!-- SIRALAMA -->
                    <div class="siralama-bar">
                      <span class="sir-badge" style="background:#fef2f2;color:#E30A17;border:1.5px solid #fca5a5;">
                        🏅 İlçe Sırası: <b>{o.get('İlçe Sırası', '-')}</b>
                      </span>
                      <span class="sir-badge" style="background:#eff6ff;color:#2563eb;border:1.5px solid #bfdbfe;">
                        🏫 Okul Sırası: <b>{o.get('Okul Sırası', '-')}</b>
                      </span>
                    </div>

                    <!-- METRİKLER -->
                    <div class="metric-row">
                      <div class="metric-box">
                        <span class="m-label">Doğru</span>
                        <span class="m-value" style="color:#059669;">{o['Doğru']}</span>
                      </div>
                      <div class="metric-box">
                        <span class="m-label">Yanlış</span>
                        <span class="m-value" style="color:#E30A17;">{o['Yanlış']}</span>
                      </div>
                      <div class="metric-box">
                        <span class="m-label">Boş</span>
                        <span class="m-value" style="color:#64748b;">{o['Boş']}</span>
                      </div>
                      <div class="metric-box">
                        <span class="m-label">Net</span>
                        <span class="m-value" style="color:#2563eb;">{o['Net']}</span>
                      </div>
                      <div class="metric-box puan-box">
                        <span class="m-label">Puan</span>
                        <span class="m-value">{o['Puan']}</span>
                      </div>
                    </div>

                    <!-- OPTİK FORM -->
                    <p style="font-weight:900;color:#111827;margin:14px 0 6px;font-size:14px;">📋 Cevap Karşılaştırma Tablosu</p>
                    <div class="optik-wrap">
                      <table class="optik-table">
                        <tr><th style="text-align:left;min-width:95px;padding-left:8px;">Soru No</th>{th}</tr>
                        <tr><th class="row-label">Cevap Anahtarı</th>{key_row}</tr>
                        <tr><th class="row-label">Öğrenci Cevabı</th>{ogr_row}</tr>
                      </table>
                    </div>

                    <!-- PEDAGOJİK DEĞERLENDİRME -->
                    <div class="rehber-box">
                      <h3>🎓 Pedagojik Rehberlik ve Değerlendirme</h3>
                      {analiz_html}
                    </div>

                  </div><!-- /karne-body -->
                </div><!-- /karne-card -->
                """, unsafe_allow_html=True)

                # ── İNDİRME BUTONU ───────────────────────────────────────
                st.markdown("<br>", unsafe_allow_html=True)
                karne_html_str = bireysel_karne_html(o, analiz_html, th, key_row, ogr_row)
                st.download_button(
                    label=f"📥  Karnemi İndir (Yazdırılabilir HTML → PDF)",
                    data=karne_html_str,
                    file_name=f"{o['Ad']}_{o['Soyad']}_Karne.html",
                    mime="text/html",
                    use_container_width=True
                )
                st.caption("💡 İndirilen dosyayı tarayıcıda açın → Ctrl+P (veya ⌘+P) → 'PDF olarak kaydet' seçeneğiyle PDF'e dönüştürebilirsiniz.")

            else:
                st.error("❌ Eşleşen kayıt bulunamadı. Okul, sınıf ve numara bilgilerinizi kontrol ediniz.")

# ══════════════════════════════════════════════════════════════════════════════
# SEKME 2 — İDARE PANELİ
# ══════════════════════════════════════════════════════════════════════════════
with tab_idareci:

    st.markdown("""
    <div class="tab-info" style="background:linear-gradient(135deg,#fafafa,#f1f5f9);border-color:#cbd5e1;">
        <div class="tab-icon">🏛️</div>
        <div>
            <h4>İlçe Milli Eğitim ve Kurum Yönetim Paneli</h4>
            <p>Bu alan <b>yetkili personele</b> özeldir. İlçe geneli ve kurum bazlı başarı analizlerine,
            toplu karne üretimine ve excel listelerine buradan ulaşabilirsiniz.
            Devam etmek için yetkili şifreyi giriniz.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    sifre = st.text_input("🔐 Yetkili Giriş Şifresi:", type="password", placeholder="Şifrenizi giriniz")

    if sifre == "darder47":
        if df_tum.empty:
            st.error("Sistemde analiz edilecek veri bulunamadı.")
        else:
            st.success(f"✅ Giriş başarılı. Hoş geldiniz — Toplam {len(df_tum)} öğrenci kaydı yüklendi.")

            # ── FİLTRELEME PANELİ ────────────────────────────────────────
            st.markdown('<div class="filter-panel">', unsafe_allow_html=True)
            st.markdown("#### ⚙️ Raporlama Filtresi")

            fc1, fc2 = st.columns(2)
            with fc1:
                okul_secs = ["📍 Tüm İlçe (Genel)"] + sorted(df_tum['OKUL ADI'].dropna().unique().tolist())
                idare_okul = st.selectbox("Kurum Seçimi:", okul_secs)
            with fc2:
                kaynak = df_tum if idare_okul == "📍 Tüm İlçe (Genel)" else df_tum[df_tum['OKUL ADI'] == idare_okul]
                sinif_secs = ["📚 Tüm Sınıf Kademeleri"] + sorted(kaynak['Sınıf'].dropna().unique().tolist())
                idare_sinif = st.selectbox("Sınıf Kademesi:", sinif_secs)
            st.markdown('</div>', unsafe_allow_html=True)

            # ── VERİ FİLTRELE ────────────────────────────────────────────
            df_idare = df_tum.copy() if idare_okul == "📍 Tüm İlçe (Genel)" else df_tum[df_tum['OKUL ADI'] == idare_okul].copy()
            kapsam = "İlçe Geneli" if idare_okul == "📍 Tüm İlçe (Genel)" else idare_okul
            if idare_sinif != "📚 Tüm Sınıf Kademeleri":
                df_idare = df_idare[df_idare['Sınıf'] == idare_sinif].copy()
                kapsam += f" ({idare_sinif}. Sınıflar)"
            else:
                kapsam += " (Tüm Kademeler)"

            if df_idare.empty:
                st.warning(f"Seçilen kriterlere uygun veri bulunamadı: {kapsam}")
            else:
                idare_tab1, idare_tab2 = st.tabs(["📈 Başarı Grafikleri & Yorumlar", "📑 İndirme Merkezi"])

                # ── SEKME A — GRAFİKLER ───────────────────────────────────
                with idare_tab1:
                    st.markdown(f"#### 📊 {kapsam} — Gelişim ve Başarı Raporu")

                    m1, m2, m3, m4 = st.columns(4)
                    m1.markdown(f"<div class='idare-metric'><span class='im-label'>Öğrenci</span><span class='im-value'>{len(df_idare)}</span></div>", unsafe_allow_html=True)
                    m2.markdown(f"<div class='idare-metric'><span class='im-label'>Ort. Puan</span><span class='im-value'>{df_idare['Puan'].mean():.1f}</span></div>", unsafe_allow_html=True)
                    m3.markdown(f"<div class='idare-metric'><span class='im-label'>Ort. Net</span><span class='im-value'>{df_idare['Net'].mean():.1f}</span></div>", unsafe_allow_html=True)
                    m4.markdown(f"<div class='idare-metric'><span class='im-label'>En Yüksek</span><span class='im-value' style='color:#059669;'>{df_idare['Puan'].max()}</span></div>", unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)

                    if idare_okul == "📍 Tüm İlçe (Genel)":
                        df_g = df_idare.groupby('OKUL ADI').agg(Ort=('Puan','mean'), N=('Puan','count')).reset_index().sort_values('Ort', ascending=True)
                        fig = px.bar(df_g, x='Ort', y='OKUL ADI', orientation='h', text_auto='.1f',
                                     color='Ort', color_continuous_scale='RdYlGn',
                                     title=f"{kapsam} — Kurumlar Arası Başarı Sıralaması")
                        fig.update_layout(height=max(420, len(df_g)*38), margin=dict(l=0,r=0,t=40,b=0))
                        st.plotly_chart(fig, use_container_width=True)

                        il_ort = df_idare['Puan'].mean()
                        lider = df_g.iloc[-1]
                        zayif = df_g.iloc[0]
                        yorum = (f"<b>📌 MEM Analiz Notu:</b> <i>{kapsam}</i> bazında ilçe olimpiyat ortalaması <b>{il_ort:.2f}</b>'dir. "
                                 f"<b>{lider['OKUL ADI']}</b> kurumu {lider['Ort']:.2f} ortalama ile ilçede öndedir; "
                                 "uyguladığı pedagojik yöntemlerin zümre çalıştaylarında paylaşılması önerilir. "
                                 f"Ortalama altındaki kurumların ({zayif['OKUL ADI']} vb.) matematik zümreleriyle ivedi 'Durum Değerlendirme Toplantısı' yapması gerekmektedir.")
                        st.markdown(f"<div class='yorum-box yorum-navy'>{yorum}</div>", unsafe_allow_html=True)

                        if idare_sinif == "📚 Tüm Sınıf Kademeleri":
                            df_sk = df_idare.groupby('Sınıf').agg(Ort=('Puan','mean')).reset_index().sort_values('Sınıf')
                            df_sk['Etiket'] = df_sk['Sınıf'] + ". Sınıflar"
                            fig2 = px.bar(df_sk, x='Etiket', y='Ort', text_auto='.1f', color='Ort',
                                          color_continuous_scale='Viridis',
                                          title="İlçe Geneli — Sınıf Kademeleri Başarı Dağılımı")
                            fig2.update_layout(height=380, margin=dict(l=0,r=0,t=40,b=0))
                            st.plotly_chart(fig2, use_container_width=True)

                            en_iyi = df_sk.sort_values('Ort').iloc[-1]['Etiket']
                            yorum2 = (f"<b>📌 Kademe Analiz Notu:</b> Sınıf düzeyleri kıyaslandığında en yüksek olimpiyat uyumu "
                                      f"<b>{en_iyi}</b>'da görülmektedir. Düşük kalan kademeler için mantık-muhakeme odaklı öğretim stratejileri güncellenmeli, "
                                      "haftalık mini pratik uygulamaları planlanmalıdır.")
                            st.markdown(f"<div class='yorum-box yorum-red'>{yorum2}</div>", unsafe_allow_html=True)
                    else:
                        df_sb = df_idare.groupby(['Sınıf','Şube']).agg(Ort=('Puan','mean')).reset_index()
                        df_sb['Etiket'] = df_sb['Sınıf'] + "/" + df_sb['Şube']
                        df_sb = df_sb.sort_values('Ort', ascending=True)
                        fig3 = px.bar(df_sb, x='Ort', y='Etiket', orientation='h', text_auto='.1f',
                                      color='Ort', color_continuous_scale='Teal',
                                      title=f"{kapsam} — Şubeler Arası Başarı Sıralaması")
                        fig3.update_layout(height=max(380, len(df_sb)*45), margin=dict(l=0,r=0,t=40,b=0))
                        st.plotly_chart(fig3, use_container_width=True)

                        ok_ort = df_idare['Puan'].mean()
                        if len(df_sb) > 1:
                            lider_sb = df_sb.iloc[-1]
                            yorum3 = (f"<b>📌 Kurum İçi Analiz Notu:</b> <i>{kapsam}</i> filtresi bazında kurumunuz ortalaması "
                                      f"<b>{ok_ort:.2f}</b> puandır. <b>{lider_sb['Etiket']}</b> şubesi {lider_sb['Ort']:.2f} ortalama ile öne çıkmaktadır. "
                                      "İlgili şube öğretmeninin pedagojik yaklaşımı tüm zümreyle paylaşılmalıdır.")
                        else:
                            yorum3 = (f"<b>📌 Kurum İçi Analiz Notu:</b> Seçilen filtreler kapsamında tek şube katılımı bulunmaktadır. "
                                      f"Sınıf ortalaması <b>{ok_ort:.2f}</b>'dir. Öğrencilerin yeni nesil soru tipleriyle daha sık pratik yapması önerilir.")
                        st.markdown(f"<div class='yorum-box yorum-green'>{yorum3}</div>", unsafe_allow_html=True)

                # ── SEKME B — İNDİRME MERKEZİ ────────────────────────────
                with idare_tab2:
                    st.markdown(f"#### 📑 {kapsam} — İndirme Merkezi")
                    st.info("👨‍💼 Aşağıdan sıralı başarı listesini ve toplu karne kitapçığını indirebilirsiniz. "
                            "HTML dosyasını tarayıcıda açıp **Ctrl+P → PDF olarak kaydet** ile PDF'e dönüştürebilirsiniz.")

                    df_export = df_idare.copy()
                    df_export['_sinif_int'] = pd.to_numeric(df_export['Sınıf'], errors='coerce').fillna(0)
                    df_export = df_export.sort_values(['_sinif_int', 'Puan'], ascending=[True, False]).drop(columns=['_sinif_int'])

                    st.markdown(f"**📊 Hazırlanan veri:** `{len(df_export)}` öğrenci kaydı")

                    # ── Sınıf bazlı karne seçeneği ───────────────────────
                    siniflar_mevcut = sorted(df_export['Sınıf'].dropna().unique().tolist())
                    karne_sinif_sec = st.radio(
                        "Karne kitapçığı kapsamı:",
                        options=["📋 Tüm Seçili Veri (Hepsi Birden)"] + [f"Sadece {s}. Sınıflar" for s in siniflar_mevcut],
                        horizontal=True
                    )

                    if karne_sinif_sec == "📋 Tüm Seçili Veri (Hepsi Birden)":
                        df_karne_export = df_export
                        karne_label = kapsam
                    else:
                        sec_sinif = karne_sinif_sec.split()[1].rstrip('.')
                        df_karne_export = df_export[df_export['Sınıf'] == sec_sinif]
                        karne_label = f"{kapsam} — {sec_sinif}. Sınıflar"

                    st.markdown(f"*Seçilen karne kapsamı:* `{len(df_karne_export)}` öğrenci")

                    col_l, col_k = st.columns(2)
                    with col_l:
                        liste_h = liste_html(df_export, kapsam)
                        st.download_button(
                            label="📊  Başarı Listesi İndir (HTML)",
                            data=liste_h,
                            file_name=f"{kapsam.replace(' ','_')}_Liste.html",
                            mime="text/html",
                            use_container_width=True
                        )
                    with col_k:
                        if not df_karne_export.empty:
                            t_karne = toplu_karne_html(df_karne_export, karne_label)
                            st.download_button(
                                label=f"🖨️  Toplu Karne Kitapçığı İndir ({len(df_karne_export)} öğrenci)",
                                data=t_karne,
                                file_name=f"{karne_label.replace(' ','_')}_Karneler.html",
                                mime="text/html",
                                use_container_width=True
                            )
                        else:
                            st.warning("Seçilen sınıfa ait kayıt bulunamadı.")

                    # ── CSV / Excel Export ────────────────────────────────
                    st.markdown("---")
                    st.markdown("**📂 Ham Veri Dışa Aktarımı**")
                    csv_str = df_export.to_csv(index=False, encoding='utf-8-sig')
                    st.download_button(
                        label="⬇️  Excel/CSV Formatında İndir",
                        data=csv_str,
                        file_name=f"{kapsam.replace(' ','_')}_Ham_Veri.csv",
                        mime="text/csv",
                        use_container_width=True
                    )

    elif sifre != "":
        st.error("❌ Yetkisiz Erişim: Şifre hatalı! Lütfen tekrar deneyiniz.")
