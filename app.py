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
        padding: 30px; border-bottom: 6px solid var(--meb-red);
        border-radius: 12px; margin-bottom: 30px; text-align: center;
        box-shadow: 0 4px 15px rgba(227, 10, 23, 0.1);
    }
    .header-banner h1 { color: var(--navy); font-weight: 900; font-size: 34px; margin: 0; letter-spacing:-0.5px; }
    .header-banner h3 { color: var(--meb-red); font-weight: 800; font-size: 18px; margin-top: 5px; text-transform: uppercase; }
    
    .stTabs [data-baseweb="tab-list"] { gap: 20px; border-bottom: 2px solid #e2e8f0; }
    .stTabs [data-baseweb="tab"] { height: 50px; background: white; border-radius: 8px 8px 0 0; font-weight: 800; font-size: 16px; border: 1px solid #e2e8f0; border-bottom: none; }
    .stTabs [aria-selected="true"] { background: var(--navy) !important; color: white !important; border-bottom: 4px solid var(--meb-red); }
    
    .metric-kutu { background: white; border-radius: 10px; padding: 20px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; border-top: 4px solid var(--navy); }
    .metric-kutu h2 { margin: 0; color: var(--meb-red); font-size: 36px; font-weight: 900; }
    .metric-kutu p { margin: 0; color: #64748b; font-size: 13px; font-weight: 900; text-transform: uppercase; }
    
    .stButton>button { background-color: var(--navy); color: white; border-radius: 8px; font-weight: bold; height: 3em; transition: 0.3s; width: 100%; }
    .stButton>button:hover { background-color: var(--meb-red); color: white; transform: translateY(-2px); }
    </style>
    """, unsafe_allow_html=True)

# --- İDARECİLER İÇİN KISA PEDAGOJİK ANALİZ (Karnelerde Kullanılır) ---
def profesyonel_analiz(row):
    p, d, y, b, ad = row['Puan'], row['Doğru'], row['Yanlış'], row['Boş'], row['Ad']
    if p >= 85:
        return f"Olağanüstü bir performans gösterdin {ad}! {p} gibi harika bir puan alarak matematiksel muhakeme gücünün ve problem çözme yeteneğinin olimpiyat düzeyinde olduğunu kanıtladın. {d} doğru sayısına ulaşman, soruları kavrama hızının ve analitik düşünme becerinin ne kadar keskin olduğunu gösteriyor. Yaptığın {y} yanlış ise bu zorlu yolda sadece küçük bir nazar boncuğudur. Sahip olduğun bu potansiyel, analitik zekanı en üst seviyede kullandığını kanıtlıyor. Bu azim ve dikkatle çalışmaya devam ettiğinde akademik hayatında başaramayacağın hiçbir şey yok. Seni ve aileni gönülden tebrik ediyoruz!"
    elif p >= 65:
        return f"Harika bir gayret ve çok başarılı bir sonuç {ad}! Elde ettiğin bu derece, temel kavramlara ve matematiksel işlemlere olan hakimiyetinin oldukça yüksek olduğunu kanıtlıyor. Yaptığın {y} yanlış, büyük ihtimalle zaman baskısından veya soruların içindeki ufak detayları gözden kaçırmandan kaynaklanıyor. Hatalarını dikkatlice inceleyip bu ufak dikkatsizliklerin üzerine gidersen, matematik dünyasında en zirveye yerleşmen an meselesidir. Kapasiten çok yüksek, kendinle gurur duymalısın ve disiplinli çalışmaktan asla vazgeçmemelisin!"
    elif p >= 40:
        return f"Önemli bir gayret gösterdin {ad}. Olimpiyat sorularının üst düzey ve zorlu yapısına rağmen temel matematik becerilerini başarıyla sergiledin. {b} boş bırakman, emin olmadığın sorularda mantıklı bir risk yönetimi uyguladığını ve bilinçli hareket ettiğini gösteriyor. Ancak {y} yanlışın, mantık ve muhakeme gerektiren yeni nesil sorularda daha fazla tecrübe kazanman gerektiğine işaret ediyor. Bol bol soru çözümü yaparak ve pes etmeden çalışarak bu eksiklerini kapatabilir, netlerini çok daha yukarılara taşıyabilirsin. Sana inanıyoruz!"
    else:
        return f"Bu sınav, senin için çok değerli bir öğrenme ve gelişim tecrübesi oldu {ad}. Puanın şu an için hedeflediğinin altında kalmış olabilir, ancak olimpiyat sınavlarının her zaman en zorlayıcı seviyede hazırlandığını unutmamalısın. Yaptığın {y} yanlış ve bıraktığın {b} boş, sana hangi konu başlıklarında daha fazla pratiğe ihtiyacın olduğunu gösteren mükemmel bir 'yol haritası' sunuyor. Başarı; hiç düşmemek değil, her düştüğünde daha güçlü kalkabilmektir. Hatalarından ders alarak konuların üzerine gittiğinde matematiğin aslında ne kadar zevkli olduğunu göreceksin. Pes etme, başaracaksın!"

# --- ÖĞRENCİLER İÇİN ÖZEL DETAYLI VE UZUN PEDAGOJİK ANALİZ (Sadece Öğrenci Ekranında Çıkar) ---
def ogrenci_uzun_analiz(row):
    p, d, y, b, ad = row['Puan'], row['Doğru'], row['Yanlış'], row['Boş'], row['Ad']
    
    giris = f"Sevgili <b>{ad}</b>,<br><br>"
    matematik_onemi = "Matematik; sadece sayılarla yapılan sıkıcı bir işlem yığını değil, evrenin sırlarını çözmemizi sağlayan eşsiz bir dildir. Analitik düşünme becerisi, hayatta karşılaştığın her zorlukta sana en doğru yolu gösteren bir pusula olacaktır. Bu olimpiyat sınavına katılarak yeteneklerini ölçme cesareti gösterdiğin için seni en içten dileklerimizle kutluyoruz.<br><br>"
    
    if p >= 85:
        durum = f"Bu zorlu sınavda gösterdiğin üstün performans ve elde ettiğin <b>{p} Puan</b>, senin matematiksel muhakeme gücünün ne kadar yüksek olduğunu kanıtlıyor. <b>{d} doğru</b> cevabın, karşılaştığın problemleri analiz etme hızının ve mantıksal bağlantıları kurma becerinin muazzam bir seviyede olduğunu gösteriyor. Yapmış olduğun <b>{y} yanlış</b> ise sadece küçük bir nazar boncuğu. Bu yeteneğini disiplinli bir çalışmayla birleştirmeye devam edersen akademik hayatında başaramayacağın hiçbir şey yok. Zirvede kalmak, oraya çıkmaktan daha büyük bir irade ister; bu yüzden asla rehavete kapılmadan, başarılarının üzerine yenilerini eklemelisin!"
    elif p >= 65:
        durum = f"Sınavda gösterdiğin <b>{p} Puanlık</b> performansın için seni tebrik ediyoruz. Bu sonuç, temel matematiksel kavramlara ve işlemlere olan hakimiyetinin oldukça iyi bir seviyede olduğunu kanıtlıyor. Yaptığın <b>{y} yanlış</b> ve bıraktığın <b>{b} boş</b>, bize sadece küçük işlem hataları yaşadığını veya zamanı yönetirken biraz daha pratik yapman gerektiğini gösteriyor. Çok güçlü bir temelin var; biraz daha sabır, dikkat ve yeni nesil mantık sorularında bol pratik ile zirveye yerleşmen an meselesi. Kendi potansiyelinin farkına var ve bu gücü açığa çıkarmaktan asla vazgeçme!"
    elif p >= 40:
        durum = f"Elde ettiğin <b>{p} Puan</b>, senin matematik temellerini attığını ancak bu temelin üzerine yeni katlar çıkmak için biraz daha fazla gayret göstermen gerektiğini ifade ediyor. Soruların <b>{b} tanesini boş bırakman</b>, aslında emin olmadığın konularda mantıklı bir risk yönetimi uyguladığını gösteriyor. Ancak yaptığın <b>{y} yanlış</b>, dikkat dağınıklığı veya bazı kavramları tam oturtamama durumundan kaynaklanıyor olabilir. Unutma; başarıya giden yol hatalardan ders çıkarmaktan geçer. Hatalarının üzerine cesaretle gitmeli, daha fazla soru çözerek o eksik parçaları tamamlamalısın. Senin içinde bu potansiyel var!"
    else:
        durum = f"Karşılaştığın bu sonucun <b>({p} Puan)</b> seni asla umutsuzluğa düşürmesine izin verme. Olimpiyat seviyesindeki sorular, en iyi öğrencileri bile zorlamak üzere özel olarak tasarlanmıştır ve standart okul sınavlarından çok farklıdır. Yaptığın <b>{y} yanlış</b> ve <b>{b} boş</b>; sana sadece eksik olduğun, pratiğe ihtiyaç duyduğun konuları gösteren değerli birer rehberdir. Unutma ki matematikte başarısızlık diye bir şey yoktur, sadece 'henüz' öğrenilmemiş konular vardır. Şimdi pes etme zamanı değil; aksine hatalarından ders alıp, düzenli tekrarlarla ve çok çalışarak matematiğin aslında ne kadar keyifli bir bulmaca olduğunu keşfetme zamanı. Biz sana inanıyoruz, yeter ki sen de kendine inan!"
        
    kapanis = "<br><br>Başarı; sadece zeka ile değil, azim ve döktüğün terle de şekillenir. Geleceğin parlak, yolun açık olsun!"
    return giris + matematik_onemi + durum + kapanis

# --- PROFESYONEL OKUL GELİŞİM RAPORU (RÖNTGEN) MOTORU ---
def okul_gelisim_metni(okul_adi, okul_ort, ilce_ort, toplam_ogrenci, df_subeler):
    fark = okul_ort - ilce_ort
    
    if fark > 5:
        durum = f"İlçe genel ortalamasının ({ilce_ort:.2f}) belirgin bir şekilde üzerine çıkarak <b>{okul_ort:.2f}</b> puan ortalaması ile üstün bir gayret sergilemiş ve zirvede yer almıştır."
        tavsiye = "Bu yüksek başarı ivmesini korumak adına, öğrencilerimizin daha üst düzey mantık-muhakeme olimpiyat kaynaklarıyla desteklenmesi önerilmektedir. Liderliğiniz ve özveriniz için şükranlarımızı sunarız."
    elif fark >= -3:
        durum = f"İlçe genel ortalaması ({ilce_ort:.2f}) ile paralel, istikrarlı bir başarı göstererek <b>{okul_ort:.2f}</b> puan ortalamasına ulaşmıştır."
        tavsiye = "Kıymetli idarecilerimizin ve öğretmenlerimizin yoğun çabaları takdire şayandır. Mevcut ortalamayı daha da yukarılara taşımak için öğrencilerin kazanım eksikliklerinin birebir tespit edilmesi ve yeni nesil soru tarzlarına yönelik etüt çalışmaları yapılması başarınızı şüphesiz artıracaktır."
    else:
        durum = f"Olimpiyat sınavının zorlayıcı yapısı neticesinde, ilçe ortalamasının ({ilce_ort:.2f}) bir miktar gerisinde kalarak <b>{okul_ort:.2f}</b> puan ortalaması elde etmiştir."
        tavsiye = "Öğretmenlerimizin sahadaki özverili çalışmaları son derece değerlidir. Sınav heyecanı veya yeni nesil sorulara aşinalık eksikliği bu sonuca etki etmiş olabilir. Öğrencilerimizi demotive etmeden, temel matematik okuryazarlığını artıracak teşvik edici faaliyetlerle bu açığın hızla kapatılacağına inancımız tamdır."
    
    if len(df_subeler) > 1:
        en_iyi_sube = df_subeler.iloc[0]
        gelisime_acik = df_subeler[df_subeler['Sube_Ort_Puan'] < okul_ort]
        
        rontgen = f"<br><br><b>🔍 Detaylı Şube Röntgeni ve Pedagojik Analiz:</b><br>"
        rontgen += f"Yapılan istatistiksel incelemeler sonucunda okulunuzda en yüksek ortalamaya sahip şubenin <b>{en_iyi_sube['Şube']} ({en_iyi_sube['Sube_Ort_Puan']:.2f} Puan)</b> olduğu tespit edilmiştir. Bu şubemizde derslere giren öğretmenlerimizin pedagojik yaklaşımlarının okuldaki diğer zümrelerle paylaşılması faydalı olacaktır. "
        
        if not gelisime_acik.empty:
            subeler_str = ", ".join(gelisime_acik['Şube'].astype(str).tolist())
            rontgen += f"Bununla birlikte, okul genel ortalamasının ({okul_ort:.2f}) altında kalan <b>{subeler_str}</b> şubelerimizdeki öğrencilerimizin konu eksiklerinin hızla tespit edilmesi gerekmektedir. Bu şubelere yönelik yapılacak özel etütler ve moral-motivasyon çalışmaları, okulumuzun genel başarısını doğrudan ve çok hızlı bir şekilde yukarı taşıyacaktır."
    else:
        rontgen = "<br><br><b>🔍 Detaylı Şube Röntgeni:</b> Okulunuzda tek şube sınava katıldığı için şubeler arası kıyaslama yapılamamıştır."

    return f"""Saygıdeğer <b>{okul_adi}</b> İdarecileri ve Kıymetli Öğretmenlerimiz,<br><br>
    Eğitimdeki en büyük gücümüz, sizlerin öğrencilere dokunan vizyoner elleridir. Okulunuz, katıldığı bu matematik olimpiyatında toplam <b>{toplam_ogrenci}</b> öğrenci ile temsil edilmiş olup, {durum} {tavsiye}
    {rontgen}
    <br><br>Bu raporu bir rekabet unsuru olarak değil, "Hangi sınıfımıza daha fazla pedagojik destek olmalıyız?" sorusunun somut bir rehberi olarak değerlendirmenizi rica ederiz."""

# --- BANNER ---
st.markdown("""
    <div class="header-banner">
        <h1>🥇 1. DARGEÇİT MATEMATİK OLİMPİYATI</h1>
        <h3>Sınav Sonuç, Okul Gelişim ve Raporlama Portalı</h3>
    </div>
""", unsafe_allow_html=True)

# --- TÜM VERİLERİ GÜVENLİ YÜKLEME ---
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
    st.info("💡 **Öğrenciler:** Sınıfınızı seçip sonuçlarınıza ulaşabilirsiniz.\n\n💡 **İdareciler:** Tüm analiz raporları ve çıktılar burada seçtiğiniz sınıfa göre hazırlanır.")

df_aktif = df_tum[df_tum['Sınıf'] == kademe_no].copy() if not df_tum.empty else pd.DataFrame()

# --- ANA SEKMELER ---
tab_ogrenci, tab_idareci = st.tabs(["👤 ÖĞRENCİ KARNESİ SORGULA", "🏫 KURUM İDARESİ VE M.E.B RAPORLARI"])

# ==============================================================================
# 1. ÖĞRENCİ GİRİŞİ (Sadece Numara İle Çalışır - Okul Seçimi Kaldırıldı)
# ==============================================================================
with tab_ogrenci:
    if df_aktif.empty:
        st.warning(f"⚠️ Sisteme henüz {secilen_kademe_str} düzeyine ait sınav sonuçları yüklenmemiştir.")
    else:
        st.markdown(f"### 🔍 {secilen_kademe_str} Bireysel Sınav Sonucu ve Detaylı Analiz")
        st.info("Aşağıdaki kutucuğa **sadece öğrenci numaranızı** yazarak karnenizi görebilir ve indirebilirsiniz.")
        
        no_secim = st.text_input("Öğrenci Numaranız:", key="ogr_no", placeholder="Okul numaranızı buraya giriniz...").strip().lstrip('0')
            
        if st.button("Karnemi Görüntüle ve Analizimi Oku", type="primary"):
            if no_secim == "":
                st.warning("Lütfen sonucunuzu görmek için yukarıdaki alana öğrenci numaranızı giriniz.")
            else:
                sonuc = df_aktif[df_aktif['Arama_No'] == no_secim]
                
                if not sonuc.empty:
                    st.balloons()
                    
                    # Eğer ilçedeki iki farklı okulda aynı numaralı öğrenci varsa her ikisini de gösterir (Hata Verdirmez)
                    if len(sonuc) > 1:
                        st.success(f"Aynı okul numarasına sahip {len(sonuc)} öğrenci bulundu. Lütfen kendi okulunuzu ve isminizi bulunuz.")
                    
                    for idx, o in sonuc.iterrows():
                        ilce_sira = o.get('İlçe Sırası', '-')
                        okul_sira = o.get('Okul Sırası', '-')
                        analiz_metni = ogrenci_uzun_analiz(o)
                        
                        st.markdown(f"""
                        <div style="background:white; padding:35px; border-radius:15px; border-top:8px solid #E30A17; box-shadow:0 10px 30px rgba(0,0,0,0.1); margin-bottom:30px;">
                            <h2 style="color:#111827; margin:0; font-size: 30px;">{o['Ad']} {o['Soyad']}</h2>
                            <p style="color:#555; font-size:18px; margin-bottom:15px;"><b>{o['OKUL ADI']}</b> | Sınıf: {o['Sınıf']}/{o['Şube']} | Öğrenci No: <b>{o['Öğrenci No']}</b></p>
                            
                            <div style="display:flex; gap:10px; margin-bottom:25px;">
                                <span style="background:#111827; color:white; padding:8px 15px; border-radius:5px; font-weight:bold;">İlçe Sırası: {ilce_sira}</span>
                                <span style="background:#E30A17; color:white; padding:8px 15px; border-radius:5px; font-weight:bold;">Okul Sırası: {okul_sira}</span>
                            </div>
                            
                            <div style="display:grid; grid-template-columns: repeat(5, 1fr); gap:15px; text-align:center;">
                                <div style="background:#f1f5f9; padding:15px; border-radius:10px; border:1px solid #e2e8f0;"><span>Doğru</span><br><b style="font-size:28px; color:#059669;">{o['Doğru']}</b></div>
                                <div style="background:#fef2f2; padding:15px; border-radius:10px; border:1px solid #fca5a5;"><span>Yanlış</span><br><b style="font-size:28px; color:#E30A17;">{o['Yanlış']}</b></div>
                                <div style="background:#f1f5f9; padding:15px; border-radius:10px; border:1px solid #e2e8f0;"><span>Boş</span><br><b style="font-size:28px; color:#64748b;">{o['Boş']}</b></div>
                                <div style="background:#eff6ff; padding:15px; border-radius:10px; border:1px solid #bfdbfe;"><span>Net</span><br><b style="font-size:28px; color:#2563eb;">{o['Net']}</b></div>
                                <div style="background:#111827; padding:15px; border-radius:10px; color:white;"><span>Puan</span><br><b style="font-size:32px; font-weight:900;">{o['Puan']}</b></div>
                            </div>
                            
                            <div style="margin-top:25px; padding:25px; background:#fff5f5; border-left:6px solid #E30A17; border-radius:8px;">
                                <h4 style="margin-top:0; color:#E30A17; font-size:18px;">🎓 Detaylı Pedagojik Analiz ve Rehberlik</h4>
                                <p style="margin:0; font-size: 16px; line-height: 1.7; color:#111827; text-align: justify;">{analiz_metni}</p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # BİREYSEL ÖĞRENCİ PDF İNDİRME BUTONU
                        bireysel_pdf = f"""
                        <html><head><meta charset="utf-8"><style>
                            @page {{ size: A4 portrait; margin: 15mm; }}
                            body {{ font-family: 'Segoe UI', Arial, sans-serif; background: white; margin: 0; padding: 0; -webkit-print-color-adjust: exact !important; }}
                            .pdf-kutu {{ border: 3px solid #111827; border-radius: 15px; padding: 25px; background: white; }}
                            .baslik {{ text-align: center; border-bottom: 4px solid #E30A17; padding-bottom: 10px; margin-bottom: 20px; }}
                            .baslik h1 {{ margin: 0; color: #111827; font-size: 22px; text-transform: uppercase; }}
                            .kimlik {{ display: flex; justify-content: space-between; font-size: 16px; font-weight: bold; margin-bottom: 15px; }}
                            .sira-vurgu {{ display: flex; gap: 15px; margin-bottom: 20px; }}
                            .s-kutu {{ background: #111827; color: white; padding: 8px 15px; border-radius: 8px; font-weight: bold; font-size: 14px; }}
                            .s-kutu.red {{ background: #E30A17; }}
                            .grid-5 {{ display: flex; justify-content: space-between; text-align: center; margin-bottom: 25px; gap: 10px; }}
                            .g-item {{ border: 1px solid #ccc; border-radius: 10px; padding: 12px; flex: 1; font-weight: bold; background: #f8fafc; }}
                            .g-item span {{ display: block; font-size: 13px; color: #555; margin-bottom: 5px; text-transform: uppercase; }}
                            .g-item b {{ font-size: 22px; }}
                            .yorum-kutusu {{ background: #fff5f5; border-left: 6px solid #E30A17; padding: 20px; font-size: 13px; line-height: 1.6; font-weight: 500; text-align: justify; border-radius: 8px; color: #111827; }}
                        </style></head><body>
                            <div class="pdf-kutu">
                                <div class="baslik"><h1>1. DARGEÇİT MATEMATİK OLİMPİYATI SONUÇ KARNESİ</h1></div>
                                <div class="kimlik"><span>{o['Ad']} {o['Soyad']} - {o['Sınıf']}/{o['Şube']}</span><span style="color:#E30A17;">Öğrenci No: {o['Öğrenci No']}</span></div>
                                <div style="font-size:14px; color:#555; margin-bottom:15px; font-weight:bold;">{o['OKUL ADI']}</div>
                                
                                <div class="sira-vurgu">
                                    <div class="s-kutu">İlçe Sırası: {ilce_sira}</div>
                                    <div class="s-kutu red">Okul Sırası: {okul_sira}</div>
                                </div>
                                
                                <div class="grid-5">
                                    <div class="g-item"><span>Doğru</span><b style="color:#059669;">{o['Doğru']}</b></div>
                                    <div class="g-item" style="background:#fef2f2; border-color:#fca5a5;"><span>Yanlış</span><b style="color:#E30A17;">{o['Yanlış']}</b></div>
                                    <div class="g-item"><span>Boş</span><b style="color:#64748b;">{o['Boş']}</b></div>
                                    <div class="g-item" style="background:#eff6ff; border-color:#bfdbfe;"><span>Net</span><b style="color:#2563eb;">{o['Net']}</b></div>
                                    <div class="g-item" style="background:#111827; color:white;"><span>Puan</span><b style="color:white; font-size:26px;">{o['Puan']}</b></div>
                                </div>
                                
                                <div class="yorum-kutusu">
                                    <b style="color:#E30A17; font-size: 16px;">🎓 Pedagojik Analiz ve Rehberlik:</b><br><br>{analiz_metni}
                                </div>
                            </div>
                        </body></html>
                        """
                        st.download_button(f"📥 {o['Ad']} {o['Soyad']} - Karneyi PDF Olarak İndir (Yazdır)", data=bireysel_pdf, file_name=f"{o['Ad']}_{o['Soyad']}_Karne.html", mime="text/html", type="primary", key=f"dl_{idx}")

                else:
                    st.error("❌ Sistemde bu numaraya ait bir kayıt bulunamadı. Lütfen numaranızı kontrol edip tekrar deneyiniz.")

# ==============================================================================
# 2. İDARECİ GİRİŞİ (Raporlar, Gelişim, Alt Alta Karneler, Toplu Listeler)
# ==============================================================================
with tab_idareci:
    st.markdown("### 🔐 Kurumsal Yönetim, Gelişim ve Raporlama Paneli")
    sifre = st.text_input("Yetkili Giriş Şifresi:", type="password")
    
    if sifre == "darder47":
        if df_tum.empty:
            st.error("Sistemde analiz edilecek sonuç verisi bulunamadı.")
        else:
            sub1, sub2, sub3, sub4 = st.tabs([
                "🏆 İLÇE GENEL RAPORU", 
                "📈 OKUL GELİŞİM RÖNTGENİ", 
                "📉 ŞUBE / ÖĞRETMEN ANALİZİ", 
                "📑 TOPLU LİSTELER VE KARNELER"
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
                
                df_okul_genel = df_tum.groupby('OKUL ADI').agg(Ogr_Sayisi=('Puan', 'count'), Ort_Puan=('Puan', 'mean')).reset_index()
                
                fig = px.bar(df_okul_genel.sort_values(by='Ort_Puan', ascending=True), x='Ort_Puan', y='OKUL ADI', orientation='h', text_auto='.2f', color='Ort_Puan', color_continuous_scale='Reds', title="İlçe Geneli Puan Sıralaması")
                fig.update_layout(height=600, xaxis_title="Puan Ortalaması", yaxis_title="")
                st.plotly_chart(fig, use_container_width=True)

            # -----------------------------------------------------
            # ALT SEKME 2: OKUL GELİŞİM RAPORU (Pedagojik Okul Röntgeni)
            # -----------------------------------------------------
            with sub2:
                st.markdown(f"#### 📈 {secilen_kademe_str} Kurum Gelişim ve Değerlendirme Raporu")
                st.write("Okulunuzun ilçe genelindeki durumunu, öğretmenlerinizin başarısını ve tüm şubelerin detaylı analizini (röntgenini) içeren resmi gelişim raporu.")
                
                if df_aktif.empty:
                    st.warning(f"Bu kademede veri bulunmamaktadır.")
                else:
                    secilen_kurum = st.selectbox("Gelişim Raporu Çıkarılacak Kurum:", sorted(df_aktif['OKUL ADI'].unique()), key="gelisim_okul")
                    
                    df_kurum_gelisim = df_aktif[df_aktif['OKUL ADI'] == secilen_kurum]
                    ilce_ort = df_aktif['Puan'].mean()
                    okul_ort = df_kurum_gelisim['Puan'].mean()
                    toplam_ogrenci = len(df_kurum_gelisim)
                    
                    df_subeler = df_kurum_gelisim.groupby('Şube').agg(Mevcut=('Puan', 'count'), Sube_Ort_Puan=('Puan', 'mean')).reset_index().sort_values(by='Sube_Ort_Puan', ascending=False)
                    
                    # Detaylı Röntgen Metnini Al
                    metin = okul_gelisim_metni(secilen_kurum, okul_ort, ilce_ort, toplam_ogrenci, df_subeler)
                    
                    st.info(f"📊 Rapor Özeti: {secilen_kurum} kurumu {toplam_ogrenci} öğrenci ile {okul_ort:.2f} ortalama elde etmiştir.")
                    
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
                        gelisim_html += f"<tr><td>{s_row['Şube']}</td><td>{s_row['Mevcut']}</td><td style='color:#E30A17; font-size:16px;'>{s_row['Sube_Ort_Puan']:.2f}</td></tr>"
                    gelisim_html += """
                        </table>
                        <div style="font-size: 12px; color: #64748b; text-align: center; margin-top: 50px; border-top: 1px solid #cbd5e1; padding-top:15px;">
                            Dargeçit İlçe Milli Eğitim Müdürlüğü - Matematik Olimpiyatı Ölçme Değerlendirme Merkezi
                        </div>
                    </body></html>
                    """
                    st.download_button("🖨️ Kurum Gelişim Raporunu İndir (Yazdırılabilir PDF)", data=gelisim_html, file_name=f"{secilen_kurum}_Gelisim_Raporu.html", mime="text/html", type="primary")

            # -----------------------------------------------------
            # ALT SEKME 3: ŞUBE VE ÖĞRETMEN ANALİZİ
            # -----------------------------------------------------
            with sub3:
                st.markdown(f"#### 📉 {secilen_kademe_str} Şube (Öğretmen) Karşılaştırma Analizleri")
                if df_aktif.empty:
                    st.warning("Bu sınıf düzeyinde veri yok.")
                else:
                    c_g1, c_g2 = st.columns(2)
                    with c_g1:
                        st.markdown("**Okul Ortalamaları Kıyaslaması**")
                        df_okul_sinif = df_aktif.groupby('OKUL ADI')['Puan'].mean().reset_index()
                        fig2 = px.bar(df_okul_sinif.sort_values(by='Puan', ascending=True), x='Puan', y='OKUL ADI', orientation='h', text_auto='.2f', color='Puan', color_continuous_scale='Blues')
                        st.plotly_chart(fig2, use_container_width=True)
                    with c_g2:
                        st.markdown("**En Başarılı Şubeler (Öğretmen Etkisi ve Sınıf İçi Rekabet)**")
                        df_sube_genel = df_aktif.groupby(['OKUL ADI', 'Şube']).agg(Ogr=('Puan', 'count'), Puan_Ort=('Puan', 'mean')).reset_index()
                        df_sube_genel = df_sube_genel[df_sube_genel['Ogr'] >= 3].sort_values(by='Puan_Ort', ascending=True).tail(15)
                        df_sube_genel['Sube_Ad'] = df_sube_genel['OKUL ADI'] + " - " + df_sube_genel['Şube']
                        fig3 = px.bar(df_sube_genel, x='Puan_Ort', y='Sube_Ad', orientation='h', text_auto='.2f', color='Puan_Ort', color_continuous_scale='Teal')
                        st.plotly_chart(fig3, use_container_width=True)

            # -----------------------------------------------------
            # ALT SEKME 4: PDF & EXCEL ÇIKTILARI (LİSTE VE KARNELER)
            # -----------------------------------------------------
            with sub4:
                st.markdown(f"#### 📑 {secilen_kademe_str} Toplu Liste ve Öğrenci Karneleri Merkezi")
                st.write("Bu bölümden öğrencilerin sonuçlarını hem toplu liste (Excel/PDF) halinde hem de A4 kağıdını tam kaplayan detaylı alt alta karneler olarak indirebilirsiniz.")
                
                if df_aktif.empty:
                    st.warning("Bu sınıf için veri bulunmamaktadır.")
                else:
                    kurum_secim = st.selectbox("İşlem Yapılacak Okulu Seçin:", ["Tüm İlçe Listesi"] + sorted(df_aktif['OKUL ADI'].unique()), key="k_karne")
                    df_filtre = df_aktif if kurum_secim == "Tüm İlçe Listesi" else df_aktif[df_aktif['OKUL ADI'] == kurum_secim]
                    
                    st.dataframe(df_filtre[['İlçe Sırası', 'Okul Sırası', 'Sınıf', 'Şube', 'Öğrenci No', 'Ad', 'Soyad', 'Net', 'Puan']], use_container_width=True)
                    
                    st.markdown("##### 🖨️ İndirme Seçenekleri")
                    c_btn1, c_btn2, c_btn3 = st.columns(3)
                    
                    # 1. EXCEL LİSTE
                    buf_ex = io.BytesIO()
                    with pd.ExcelWriter(buf_ex, engine='openpyxl') as writer:
                        df_filtre.to_excel(writer, index=False)
                    c_btn1.download_button("📊 1) Tabloyu Excel Olarak İndir", data=buf_ex.getvalue(), file_name=f"{kurum_secim}_Liste.xlsx", use_container_width=True)

                    # 2. PDF LİSTE (TABLO HALİNDE)
                    pdf_liste_html = f"""
                    <html><head><meta charset="utf-8"><style>
                        @page {{ size: A4 portrait; margin: 15mm; }}
                        body {{ font-family: 'Segoe UI', Tahoma, sans-serif; margin: 0; padding: 0; color: #111827; -webkit-print-color-adjust: exact !important; }}
                        .baslik {{ text-align: center; border-bottom: 4px solid #111827; padding-bottom: 10px; margin-bottom: 20px; }}
                        .baslik h1 {{ margin: 0; font-size: 20px; font-weight: 900; }}
                        .baslik h2 {{ margin: 5px 0 0 0; color: #E30A17; font-size: 15px; }}
                        table {{ width: 100%; border-collapse: collapse; font-size: 12px; text-align: center; }}
                        th {{ background-color: #111827; color: white; padding: 8px; border: 1px solid #111827; }}
                        td {{ padding: 6px; border: 1px solid #cbd5e1; }}
                        tr:nth-child(even) {{ background-color: #f8fafc; }}
                    </style></head><body>
                        <div class="baslik">
                            <h1>T.C. DARGEÇİT KAYMAKAMLIĞI - 1. MATEMATİK OLİMPİYATI</h1>
                            <h2>{kurum_secim} - {kademe_no}. SINIF ÖĞRENCİ BAŞARI LİSTESİ</h2>
                        </div>
                        <table>
                            <tr><th>İlçe S.</th><th>Okul S.</th><th>Ad Soyad</th><th>Sınıf/Şube</th><th>No</th><th>Doğru</th><th>Yanlış</th><th>Boş</th><th>Net</th><th>Puan</th></tr>
                    """
                    for _, row in df_filtre.iterrows():
                        pdf_liste_html += f"<tr><td>{row.get('İlçe Sırası','-')}</td><td>{row.get('Okul Sırası','-')}</td><td style='text-align:left; font-weight:bold;'>{row['Ad']} {row['Soyad']}</td><td>{row['Sınıf']}/{row['Şube']}</td><td>{row['Öğrenci No']}</td><td>{row['Doğru']}</td><td>{row['Yanlış']}</td><td>{row['Boş']}</td><td style='color:#2563eb; font-weight:bold;'>{row['Net']}</td><td style='color:#E30A17; font-weight:bold; font-size:14px;'>{row['Puan']}</td></tr>"
                    pdf_liste_html += "</table></body></html>"
                    
                    c_btn2.download_button("📑 2) Liste Halinde PDF İndir", data=pdf_liste_html, file_name=f"{kurum_secim}_PDF_Liste.html", mime="text/html", use_container_width=True)

                    # 3. KUSURSUZ, BOŞLUKSUZ ALT ALTA KARNELER (1 SAYFADA 3 ADET)
                    html_karne = """
                    <html><head><meta charset="utf-8"><style>
                        @page { size: A4 portrait; margin: 10mm; }
                        * { box-sizing: border-box; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
                        body { font-family: 'Segoe UI', Tahoma, sans-serif; margin: 0; padding: 0; color: #111827; background: white; }
                        
                        /* A4 Sayfası - Alt Alta Boşluksuz Tasarım */
                        .page { width: 190mm; height: 277mm; display: flex; flex-direction: column; justify-content: flex-start; gap: 8mm; page-break-after: always; }
                        
                        /* Karne Kutusu: Sayfayı yatayda tam kaplar */
                        .karne { 
                            width: 100%; height: 86mm; border: 2.5px solid #E30A17; border-radius: 12px; 
                            padding: 12px 15px; display: flex; flex-direction: column; justify-content: space-between;
                            background: white; position: relative; page-break-inside: avoid;
                        }
                        
                        .baslik { color: #111827; text-align: center; font-weight: 900; font-size: 15px; border-bottom: 3px solid #E30A17; padding-bottom: 5px; text-transform: uppercase; letter-spacing: 0.5px; }
                        .kimlik-satir { display: flex; justify-content: space-between; font-weight: 900; font-size: 13px; margin-top: 6px; }
                        .sira-kutu { text-align: center; background: #E30A17; color: white; padding: 6px; border-radius: 6px; font-size: 11px; font-weight: bold; margin-top: 6px; }
                        
                        .stats-tablo { width: 100%; border-collapse: collapse; text-align: center; font-size: 13px; margin-top: 6px; }
                        .stats-tablo th { background: #fef2f2; border: 1px solid #fca5a5; padding: 5px; color: #E30A17; }
                        .stats-tablo td { border: 1px solid #fca5a5; padding: 6px; font-weight: 900; font-size: 15px; }
                        
                        .optik-tablo { width: 100%; border-collapse: collapse; text-align: center; font-size: 10px; margin-top: 6px; table-layout: fixed; }
                        .optik-tablo th, .optik-tablo td { border: 1px solid #fca5a5; height: 18px; overflow: hidden; font-weight: bold; }
                        .optik-tablo th { background: #fef2f2; color: #E30A17; }
                        .dogru { background: #dcfce7 !important; color: #059669 !important; font-weight: 900; }
                        .yanlis { background: #111827 !important; color: white !important; font-weight: 900; } 
                        
                        .analiz-kutu { 
                            background: #f8fafc !important; border-left: 5px solid #E30A17; padding: 8px 10px; 
                            font-size: 9.5px; line-height: 1.4; font-weight: 600; text-align: justify;
                            margin-top: 8px; color: #111827; border-radius: 4px; border: 1px solid #e2e8f0;
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

                        # PDF için kısa özlü yorum
                        p_val = row['Puan']
                        if p_val >= 85: k_yr = "Üstün yetenek ve yüksek analitik zeka. 2. Aşamada başarılar!"
                        elif p_val >= 65: k_yr = "Çok başarılısın. Ufak işlem hatalarını kapatırsan zirvedesin."
                        elif p_val >= 40: k_yr = "Temelin sağlam, bol soru çözümü ve pratikle netlerin çok daha yükselecek."
                        else: k_yr = "Zor bir sınavdı, asla pes etme. Hatalarından ders çıkarıp eksiklerini tamamla."

                        html_karne += f"""
                        <div class="karne">
                            <div>
                                <div class="baslik">T.C. DARGEÇİT KAYMAKAMLIĞI - MATEMATİK OLİMPİYATI SONUÇ BELGESİ</div>
                                <div class="kimlik-satir"><span style="font-size: 14px;">{row['Ad']} {row['Soyad']}</span><span style="color:#E30A17;">Öğr. No: {row['Öğrenci No']}</span></div>
                                <div class="kimlik-satir" style="color:#555; font-size:12px;"><span>{row['OKUL ADI']}</span><span>Sınıf: {row['Sınıf']}/{row['Şube']}</span></div>
                                <div class="sira-kutu">İlçe Sırası: {row.get('İlçe Sırası','-')} &nbsp;|&nbsp; Okul Sırası: {row.get('Okul Sırası','-')}</div>
                                
                                <table class="stats-tablo">
                                    <tr><th>Doğru</th><th>Yanlış</th><th>Boş</th><th>Net</th><th>Puan</th></tr>
                                    <tr><td style="color:#059669;">{row['Doğru']}</td><td style="color:#E30A17;">{row['Yanlış']}</td><td>{row['Boş']}</td><td style="color:#2563eb;">{row['Net']}</td><td style="background:#111827 !important; color:white; font-size: 18px;">{row['Puan']}</td></tr>
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
                    c_btn3.download_button("🖨️ 3) Alt Alta Özel Karneleri Al (PDF)", data=html_karne, file_name=f"{kurum_secim}_ALT_ALTA_Karneler.html", mime="text/html", use_container_width=True)
                    st.info("💡 **Önemli Yazdırma Notu:** Tarayıcıda Ctrl+P yaptığınızda 'Kenar Boşlukları: Yok' (Margins: None) seçeneğini işaretlemeyi unutmayın.")
    elif sifre != "":
        st.error("Hatalı Şifre!")
