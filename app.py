import streamlit as st
import pandas as pd
import io
import os
import glob
import ast
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="1. Dargeçit Matematik Olimpiyatı", layout="wide", page_icon="🥇")

st.markdown("""
<style>
    :root {
        --meb-red: #E30A17;
        --navy: #111827;
        --light-bg: #f8fafc;
        --card-shadow: 0 10px 30px rgba(0,0,0,0.08);
    }
    .main { background-color: var(--light-bg); }
    * { -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }

    .header-banner {
        background: linear-gradient(135deg, #ffffff 0%, #fef2f2 100%);
        padding: 30px; border-bottom: 6px solid var(--meb-red);
        border-radius: 16px; margin-bottom: 30px; text-align: center;
        box-shadow: var(--card-shadow);
    }
    .header-banner h1 { color: var(--navy); font-weight: 900; font-size: 36px; margin: 0; letter-spacing:-0.5px; }
    .header-banner h3 { color: var(--meb-red); font-weight: 800; font-size: 18px; margin-top: 5px; text-transform: uppercase; letter-spacing: 2px; }
    
    .stTabs [data-baseweb="tab-list"] { gap: 15px; border-bottom: 2px solid #e2e8f0; }
    .stTabs [data-baseweb="tab"] { height: 50px; background: white; border-radius: 8px 8px 0 0; font-weight: 800; font-size: 16px; border: 1px solid #e2e8f0; border-bottom: none; padding: 0 20px; }
    .stTabs [aria-selected="true"] { background: var(--navy) !important; color: white !important; border-bottom: 4px solid var(--meb-red); }
    
    .metric-kutu { background: white; border-radius: 12px; padding: 24px 15px; text-align: center; box-shadow: var(--card-shadow); border: 1px solid #e2e8f0; border-top: 4px solid var(--navy); transition: 0.3s; }
    .metric-kutu:hover { transform: translateY(-3px); box-shadow: 0 15px 35px rgba(0,0,0,0.12); }
    .metric-kutu h2 { margin: 0; color: var(--meb-red); font-size: 38px; font-weight: 900; }
    .metric-kutu p { margin: 0; color: #64748b; font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }
    
    .stButton>button { background-color: var(--navy); color: white; border-radius: 8px; font-weight: bold; height: 3em; transition: 0.3s; width: 100%; border: none; letter-spacing: 0.5px; }
    .stButton>button:hover { background-color: var(--meb-red); color: white; transform: translateY(-2px); box-shadow: 0 8px 20px rgba(227,10,23,0.3); }
    
    div[data-testid="stDataFrame"] table { border-collapse: separate; border-spacing: 0; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; }
    div[data-testid="stDataFrame"] th { background-color: var(--navy); color: white; font-weight: bold; text-align: center; padding: 10px; }
    div[data-testid="stDataFrame"] td { padding: 8px; text-align: center; font-weight: 500; }
</style>
""", unsafe_allow_html=True)

def profesyonel_analiz(row):
    p, d, y, b, ad = row['Puan'], row['Doğru'], row['Yanlış'], row['Boş'], row['Ad']
    if p >= 85:
        return f"Olağanüstü bir performans gösterdin {ad}! Matematiksel muhakeme gücünün ve problem çözme yeteneğinin olimpiyat düzeyinde olduğunu bu sınavla kanıtladın. {d} doğru gibi muazzam bir sayıya ulaşman, analitik düşünme becerinin ne kadar keskin olduğunu gösteriyor. {y} yanlışın ise sadece küçük bir nazar boncuğu. Bu azim ve dikkatle yoluna devam ettiğinde başaramayacağın hiçbir şey yok. Seni gönülden tebrik ediyoruz!"
    elif p >= 65:
        return f"Harika bir gayret ve çok başarılı bir sonuç {ad}! Temel kavramlara ve matematiksel işlemlere olan hakimiyetin oldukça yüksek. Yaptığın {y} yanlış, muhtemelen zaman baskısından veya sorunun içindeki ufak bir detayı gözden kaçırmandan kaynaklanıyor. Hatalarını inceleyip bu ufak dikkatsizliklerin üzerine gidersen, matematik dünyasında zirveye yerleşmen an meselesidir. Kendinle gurur duymalısın!"
    elif p >= 40:
        return f"Önemli bir gayret gösterdin {ad}. Olimpiyat sorularının zorlu yapısına rağmen temel matematik becerilerini başarıyla sergiledin. {b} boş bırakman, emin olmadığın sorularda mantıklı bir risk yönetimi uyguladığını gösteriyor. Ancak {y} yanlışın, mantık-muhakeme sorularında daha fazla tecrübe kazanman gerektiğine işaret ediyor. Bol soru çözümü ve düzenli tekrarlarla netlerini çok daha yukarılara taşıyabilirsin."
    else:
        return f"Bu zorlu sınav, senin için çok değerli bir öğrenme tecrübesi oldu {ad}. Puanın hedeflediğinin altında kalsa da, olimpiyat düzeyindeki soruların her zaman en zorlayıcı seviyede olduğunu unutma. {y} yanlış ve {b} boşun, hangi konu başlıklarında pratiğe ihtiyacın olduğunu sana gösteren mükemmel bir yol haritasıdır. Asla pes etme; hatalarından ders alarak üzerine gittiğinde matematiğin ne kadar zevkli olduğunu göreceksin. Sana inanıyoruz!"

def okul_gelisim_metni(okul_adi, okul_ort, ilce_ort, toplam_ogrenci):
    fark = okul_ort - ilce_ort
    if fark > 5:
        durum = f"İlçe genel ortalamasının ({ilce_ort:.2f}) belirgin bir şekilde üzerine çıkarak <b>{okul_ort:.2f}</b> puan ortalaması ile üstün bir gayret sergilemiş ve zirvede yer almıştır."
        tavsiye = "Bu yüksek başarı ivmesini korumak adına, halihazırda iyi seviyede olan öğrencilerimizin daha üst düzey mantık-muhakeme olimpiyat kaynaklarıyla desteklenmesi önerilmektedir."
    elif fark >= -3:
        durum = f"İlçe genel ortalaması ({ilce_ort:.2f}) ile paralel, istikrarlı bir başarı göstererek <b>{okul_ort:.2f}</b> puan ortalamasına ulaşmıştır."
        tavsiye = "Mevcut ortalamayı daha da yukarılara taşımak için öğrencilerin kazanım eksikliklerinin birebir tespit edilmesi ve yeni nesil soru tarzlarına yönelik periyodik etüt çalışmaları yapılması kurumunuzun başarısını şüphesiz artıracaktır."
    else:
        durum = f"Olimpiyat sınavının zorlayıcı yapısı neticesinde, ilçe ortalamasının ({ilce_ort:.2f}) bir miktar gerisinde kalarak <b>{okul_ort:.2f}</b> puan ortalaması elde etmiştir."
        tavsiye = "Öğrencilerimizi demotive etmeden, temel matematik okuryazarlığını artıracak teşvik edici faaliyetlerle bu açığın hızla kapatılacağına inancımız tamdır."
    return f"""Saygıdeğer <b>{okul_adi}</b> İdarecileri ve Kıymetli Öğretmenlerimiz,<br><br>Eğitimdeki en büyük gücümüz, sizlerin öğrencilere dokunan vizyoner elleridir. Okulunuz, katıldığı bu matematik olimpiyatında toplam <b>{toplam_ogrenci}</b> öğrenci ile temsil edilmiş olup, {durum} {tavsiye}<br><br>Aşağıda sunulan şube ve öğretmen bazlı analiz raporlarını bir rekabet unsuru olarak değil, "Hangi sınıfımıza daha fazla pedagojik destek olmalıyız ve hangi konuların üzerine gitmeliyiz?" sorusunun somut bir rehberi olarak değerlendirmenizi rica ederiz."""

@st.cache_data
def verileri_yukle():
    dosyalar = glob.glob("sonuclar_*.xlsx")
    if not dosyalar:
        st.error("Hiçbir 'sonuclar_*.xlsx' dosyası bulunamadı. Lütfen dosyaları ana dizine ekleyin.")
        return pd.DataFrame()
    liste = []
    for d in dosyalar:
        try:
            df = pd.read_excel(d)
            if 'Puan' in df.columns and 'Öğrenci No' in df.columns:
                df['Arama_No'] = df['Öğrenci No'].astype(str).str.replace('.0', '', regex=False).str.strip().str.lstrip('0')
                df['Sınıf'] = df['Sınıf'].astype(str).str.replace('.0', '', regex=False).str.strip()
                liste.append(df)
        except Exception as e:
            st.warning(f"Dosya okunamadı: {d} - Hata: {e}")
    if liste:
        birlestirilmis = pd.concat(liste, ignore_index=True)
        birlestirilmis = birlestirilmis.sort_values(by=['Puan', 'Net'], ascending=[False, False]).reset_index(drop=True)
        return birlestirilmis
    return pd.DataFrame()

df_tum = verileri_yukle()

if df_tum.empty:
    st.stop()

with st.sidebar:
    st.markdown('<h3 style="color:#E30A17; text-align:center; margin-bottom: 20px;">📊 KONTROL PANELİ</h3>', unsafe_allow_html=True)
    mevcut_siniflar = sorted(df_tum['Sınıf'].unique(), key=lambda x: int(x))
    sinif_secenekleri = [f"{s}. Sınıf" for s in mevcut_siniflar]
    secilen_kademe_str = st.selectbox("Sınıf Düzeyi Seçin:", sinif_secenekleri, index=0)
    kademe_no = secilen_kademe_str.split(".")[0]
    st.divider()
    st.info("👤 **Öğrenciler:** Sınıfınızı seçip sonuçlarınıza ulaşabilirsiniz.\n\n🏫 **İdareciler:** Tüm analiz raporları ve çıktılar burada seçtiğiniz sınıfa göre hazırlanır.")

df_aktif = df_tum[df_tum['Sınıf'] == kademe_no].copy()

tab_ogrenci, tab_idareci = st.tabs(["👤 ÖĞRENCİ KARNESİ SORGULA", "🏫 KURUM İDARESİ VE M.E.B RAPORLARI"])

with tab_ogrenci:
    if df_aktif.empty:
        st.warning(f"⚠️ {secilen_kademe_str} düzeyine ait sınav sonucu bulunamadı.")
    else:
        st.markdown(f"### 🔍 {secilen_kademe_str} Bireysel Sonuç Sorgulama")
        col1, col2 = st.columns(2)
        with col1:
            okul_listesi = sorted(df_aktif['OKUL ADI'].dropna().unique())
            okul_secim = st.selectbox("Okulunuzu Seçin:", okul_listesi, key="ogr_okul")
        with col2:
            no_secim = st.text_input("Öğrenci Numaranızı Girin:", key="ogr_no", placeholder="Örn: 123").strip()
            no_secim_temiz = no_secim.replace('.0','').lstrip('0')
        
        if st.button("Karnemi Görüntüle", type="primary"):
            if not no_secim_temiz:
                st.error("Lütfen geçerli bir öğrenci numarası girin.")
            else:
                sonuc = df_aktif[(df_aktif['OKUL ADI'] == okul_secim) & (df_aktif['Arama_No'] == no_secim_temiz)]
                if not sonuc.empty:
                    st.balloons()
                    o = sonuc.iloc[0]
                    ilce_sira = o.get('İlçe Sırası', '-')
                    okul_sira = o.get('Okul Sırası', '-')
                    
                    st.markdown(f"""
                    <div style="background:white; padding:35px; border-radius:20px; border-top:8px solid #E30A17; box-shadow:0 15px 40px rgba(0,0,0,0.1); margin-top:20px;">
                        <h2 style="color:#111827; margin:0; font-size: 32px; font-weight: 900;">{o['Ad']} {o['Soyad']}</h2>
                        <p style="color:#64748b; font-size:18px; margin-bottom:20px;"><b>{o['OKUL ADI']}</b> | Sınıf: {o['Sınıf']}/{o['Şube']} | Numara: <b>{o['Öğrenci No']}</b></p>
                        <div style="display:flex; gap:15px; margin-bottom:30px;">
                            <span style="background:#111827; color:white; padding:10px 20px; border-radius:8px; font-weight:bold;">İlçe Sırası: {ilce_sira}</span>
                            <span style="background:#E30A17; color:white; padding:10px 20px; border-radius:8px; font-weight:bold;">Okul Sırası: {okul_sira}</span>
                        </div>
                        <div style="display:grid; grid-template-columns: repeat(5, 1fr); gap:15px; text-align:center;">
                            <div style="background:#f1f5f9; padding:15px; border-radius:12px; border:1px solid #e2e8f0;"><span style="color:#64748b;">Doğru</span><br><b style="font-size:28px; color:#059669;">{o['Doğru']}</b></div>
                            <div style="background:#fef2f2; padding:15px; border-radius:12px; border:1px solid #fecaca;"><span style="color:#64748b;">Yanlış</span><br><b style="font-size:28px; color:#E30A17;">{o['Yanlış']}</b></div>
                            <div style="background:#f1f5f9; padding:15px; border-radius:12px; border:1px solid #e2e8f0;"><span style="color:#64748b;">Boş</span><br><b style="font-size:28px; color:#64748b;">{o['Boş']}</b></div>
                            <div style="background:#eff6ff; padding:15px; border-radius:12px; border:1px solid #bfdbfe;"><span style="color:#64748b;">Net</span><br><b style="font-size:28px; color:#2563eb;">{o['Net']}</b></div>
                            <div style="background:#111827; padding:15px; border-radius:12px; color:white;"><span>Puan</span><br><b style="font-size:34px; font-weight:900;">{o['Puan']}</b></div>
                        </div>
                        <div style="margin-top:30px; padding:25px; background:#f8fafc; border-left:6px solid #E30A17; border-radius:12px;">
                            <p style="margin:0; font-size: 16px; line-height: 1.7; color:#111827;"><b>🎓 Pedagojik Değerlendirme:</b><br>{profesyonel_analiz(o)}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("❌ Kayıt bulunamadı. Lütfen Okul ve Numara bilgilerinizi kontrol ediniz.")

with tab_idareci:
    st.markdown("### 🔐 Kurumsal Yönetim ve Veri Analiz Merkezi")
    sifre = st.text_input("Yetkili Giriş Şifresi:", type="password")
    
    if sifre == "darder47":
        if df_tum.empty:
            st.error("Sistemde analiz edilecek veri bulunamadı.")
        else:
            sub1, sub2, sub3, sub4 = st.tabs([
                "🏆 İLÇE GENEL RAPORU", 
                "📈 OKUL GELİŞİM RAPORU", 
                "📉 ŞUBE / ÖĞRETMEN ANALİZİ", 
                "📑 LİSTELER VE KARNELER"
            ])

            with sub1:
                st.markdown("#### 🏢 İlçe Geneli Okul Başarı Sıralaması ve Temel İstatistikler")
                c_m1, c_m2, c_m3, c_m4 = st.columns(4)
                with c_m1: st.markdown(f"<div class='metric-kutu'><p>Sınava Giren Öğrenci</p><h2>{len(df_tum)}</h2></div>", unsafe_allow_html=True)
                with c_m2: st.markdown(f"<div class='metric-kutu'><p>Katılımcı Okul Sayısı</p><h2>{df_tum['OKUL ADI'].nunique()}</h2></div>", unsafe_allow_html=True)
                with c_m3: st.markdown(f"<div class='metric-kutu'><p>İlçe Puan Ortalaması</p><h2>{df_tum['Puan'].mean():.2f}</h2></div>", unsafe_allow_html=True)
                with c_m4: st.markdown(f"<div class='metric-kutu'><p>İlçe Net Ortalaması</p><h2 style='color:#111827;'>{df_tum['Net'].mean():.2f}</h2></div>", unsafe_allow_html=True)
                
                df_okul_genel = df_tum.groupby('OKUL ADI').agg(Ogr_Sayisi=('Puan', 'count'), Ort_Puan=('Puan', 'mean')).reset_index().sort_values(by='Ort_Puan', ascending=True)
                fig = px.bar(df_okul_genel, x='Ort_Puan', y='OKUL ADI', orientation='h', text_auto='.2f', color='Ort_Puan', color_continuous_scale='Reds', title="İlçe Geneli Okul Puan Sıralaması")
                fig.update_traces(textfont_size=14, textposition='outside')
                fig.update_layout(height=600, xaxis_title="Ortalama Puan", yaxis_title="", coloraxis_showscale=False)
                st.plotly_chart(fig, use_container_width=True)

            with sub2:
                st.markdown(f"#### 📈 Kurum Kapsamlı Gelişim ve Değerlendirme Raporu")
                st.caption("Seçili okulun tüm sınıf ve şubelerini kapsayan, ilçe ortalaması ile kıyaslamalı detaylı analiz.")
                
                tum_okullar = sorted(df_tum['OKUL ADI'].unique())
                secilen_kurum = st.selectbox("Gelişim Raporu Çıkarılacak Kurum:", tum_okullar, key="gelisim_okul")
                df_kurum = df_tum[df_tum['OKUL ADI'] == secilen_kurum]
                
                if df_kurum.empty:
                    st.warning("Seçili okula ait veri bulunamadı.")
                else:
                    ilce_ort = df_tum['Puan'].mean()
                    okul_ort = df_kurum['Puan'].mean()
                    toplam_ogrenci = len(df_kurum)
                    
                    st.info(f"📊 **{secilen_kurum}** kurumu **{toplam_ogrenci}** öğrenci ile sınava katılmış ve **{okul_ort:.2f}** puan ortalaması elde etmiştir. (İlçe Ort: {ilce_ort:.2f})")
                    st.markdown(okul_gelisim_metni(secilen_kurum, okul_ort, ilce_ort, toplam_ogrenci), unsafe_allow_html=True)
                    
                    st.markdown("---")
                    st.markdown("##### 📋 Sınıf Bazında Başarı Dağılımı")
                    sinif_rapor = df_kurum.groupby('Sınıf').agg(
                        Öğrenci_Sayısı=('Puan', 'count'), 
                        Ortalama_Puan=('Puan', 'mean'),
                        En_Yüksek=('Puan', 'max'),
                        Ortalama_Net=('Net', 'mean')
                    ).reset_index().sort_values(by='Sınıf')
                    
                    fig_sinif = make_subplots(specs=[[{"secondary_y": True}]])
                    fig_sinif.add_trace(go.Bar(x=sinif_rapor['Sınıf'], y=sinif_rapor['Ortalama_Puan'], name="Ortalama Puan", marker_color='#E30A17', text=sinif_rapor['Ortalama_Puan'].round(1), textposition='outside'), secondary_y=False)
                    fig_sinif.add_trace(go.Scatter(x=sinif_rapor['Sınıf'], y=sinif_rapor['Öğrenci_Sayısı'], name="Öğrenci Sayısı", marker_color='#111827', mode='lines+markers', line=dict(width=3)), secondary_y=True)
                    fig_sinif.update_layout(title=f"{secilen_kurum} - Sınıf Düzeyinde Ortalama Puan ve Katılım", hovermode='x unified', height=450)
                    st.plotly_chart(fig_sinif, use_container_width=True)

                    st.markdown("##### 📋 Şube Bazında Detaylı Kırılım")
                    sube_rapor = df_kurum.groupby(['Sınıf', 'Şube']).agg(
                        Öğrenci_Sayısı=('Puan', 'count'), 
                        Ortalama_Puan=('Puan', 'mean'),
                        En_Yüksek_Puan=('Puan', 'max')
                    ).reset_index().sort_values(by=['Sınıf', 'Ortalama_Puan'], ascending=[True, False])
                    st.dataframe(sube_rapor.style.background_gradient(subset=['Ortalama_Puan'], cmap='Reds'), use_container_width=True)

            with sub3:
                st.markdown(f"#### 📉 {secilen_kademe_str} Şube (Öğretmen) Karşılaştırma Analizleri")
                if df_aktif.empty:
                    st.warning("Bu sınıf düzeyinde veri bulunmamaktadır.")
                else:
                    c_g1, c_g2 = st.columns(2)
                    with c_g1:
                        st.markdown("**Okul Ortalamaları Kıyaslaması**")
                        df_okul_sinif = df_aktif.groupby('OKUL ADI')['Puan'].mean().reset_index().sort_values(by='Puan', ascending=True)
                        fig2 = px.bar(df_okul_sinif, x='Puan', y='OKUL ADI', orientation='h', text_auto='.2f', color='Puan', color_continuous_scale='Blues')
                        fig2.update_traces(textfont_size=13)
                        fig2.update_layout(height=500, coloraxis_showscale=False)
                        st.plotly_chart(fig2, use_container_width=True)
                    with c_g2:
                        st.markdown("**En Başarılı Şubeler (Minimum 3 Öğrenci)**")
                        df_sube_genel = df_aktif.groupby(['OKUL ADI', 'Şube']).agg(Ogr=('Puan', 'count'), Puan_Ort=('Puan', 'mean')).reset_index()
                        df_sube_genel = df_sube_genel[df_sube_genel['Ogr'] >= 3].sort_values(by='Puan_Ort', ascending=True).tail(15)
                        df_sube_genel['Sube_Ad'] = df_sube_genel['OKUL ADI'] + " - " + df_sube_genel['Şube']
                        fig3 = px.bar(df_sube_genel, x='Puan_Ort', y='Sube_Ad', orientation='h', text_auto='.2f', color='Puan_Ort', color_continuous_scale='Teal')
                        fig3.update_traces(textfont_size=12)
                        fig3.update_layout(height=500, coloraxis_showscale=False)
                        st.plotly_chart(fig3, use_container_width=True)

            with sub4:
                st.markdown(f"#### 📑 {secilen_kademe_str} Toplu Liste ve Resmi Öğrenci Karneleri")
                st.write("Bu bölümden öğrencilerin sonuçlarını hem Excel listesi hem de yazdırılabilir özel tasarım karneler olarak indirebilirsiniz.")
                
                if df_aktif.empty:
                    st.warning("Bu sınıf için veri bulunmamaktadır.")
                else:
                    kurum_secim = st.selectbox("İşlem Yapılacak Okulu Seçin:", ["Tüm İlçe Listesi"] + sorted(df_aktif['OKUL ADI'].unique()), key="k_karne")
                    df_filtre = df_aktif if kurum_secim == "Tüm İlçe Listesi" else df_aktif[df_aktif['OKUL ADI'] == kurum_secim]
                    df_filtre = df_filtre.sort_values(by=['Puan', 'Net'], ascending=[False, False])
                    
                    st.dataframe(df_filtre[['İlçe Sırası', 'Okul Sırası', 'Sınıf', 'Şube', 'Öğrenci No', 'Ad', 'Soyad', 'Net', 'Puan']], use_container_width=True, height=400)
                    
                    st.markdown("##### 🖨️ Doküman İndirme Seçenekleri")
                    c_btn1, c_btn2, c_btn3 = st.columns(3)
                    
                    buf_ex = io.BytesIO()
                    with pd.ExcelWriter(buf_ex, engine='openpyxl') as writer:
                        df_filtre.to_excel(writer, index=False)
                    c_btn1.download_button("📊 1) Excel Listesi", data=buf_ex.getvalue(), file_name=f"{kurum_secim}_Liste.xlsx", use_container_width=True)

                    pdf_liste_html = f"""
                    <html><head><meta charset="utf-8"><style>
                        @page {{ size: A4 portrait; margin: 15mm; }}
                        body {{ font-family: 'Segoe UI', Tahoma, sans-serif; color: #111827; }}
                        .baslik {{ text-align: center; border-bottom: 4px solid #111827; padding-bottom: 10px; margin-bottom: 20px; }}
                        .baslik h1 {{ margin: 0; font-size: 20px; font-weight: 900; }}
                        .baslik h2 {{ margin: 5px 0 0 0; color: #E30A17; font-size: 15px; }}
                        table {{ width: 100%; border-collapse: collapse; font-size: 12px; text-align: center; }}
                        th {{ background-color: #111827; color: white; padding: 8px; }}
                        td {{ padding: 6px; border: 1px solid #cbd5e1; }}
                    </style></head><body>
                        <div class="baslik"><h1>T.C. DARGEÇİT KAYMAKAMLIĞI</h1><h2>{kurum_secim} - {kademe_no}. SINIF BAŞARI LİSTESİ</h2></div>
                        <table><tr><th>İlçe S.</th><th>Okul S.</th><th>Ad Soyad</th><th>Sınıf/Şube</th><th>No</th><th>D</th><th>Y</th><th>B</th><th>Net</th><th>Puan</th></tr>
                    """
                    for _, row in df_filtre.iterrows():
                        pdf_liste_html += f"<tr><td>{row.get('İlçe Sırası','-')}</td><td>{row.get('Okul Sırası','-')}</td><td style='text-align:left;'>{row['Ad']} {row['Soyad']}</td><td>{row['Sınıf']}/{row['Şube']}</td><td>{row['Öğrenci No']}</td><td>{row['Doğru']}</td><td>{row['Yanlış']}</td><td>{row['Boş']}</td><td style='color:#2563eb;'>{row['Net']}</td><td style='color:#E30A17; font-weight:bold;'>{row['Puan']}</td></tr>"
                    pdf_liste_html += "</table></body></html>"
                    c_btn2.download_button("📑 2) PDF Liste", data=pdf_liste_html, file_name=f"{kurum_secim}_Liste.html", mime="text/html", use_container_width=True)

                    html_karne = """
                    <html><head><meta charset="utf-8"><style>
                        @page { size: A4 portrait; margin: 8mm; }
                        body { font-family: 'Segoe UI', Tahoma, sans-serif; margin: 0; background: white; }
                        .page { width: 190mm; height: 277mm; display: flex; flex-direction: column; justify-content: flex-start; gap: 5mm; page-break-after: always; }
                        .karne { width: 100%; height: 86mm; border: 2.5px solid #E30A17; border-radius: 12px; padding: 12px 15px; display: flex; flex-direction: column; justify-content: space-between; background: white; position: relative; page-break-inside: avoid; }
                        .baslik { color: #111827; text-align: center; font-weight: 900; font-size: 14px; border-bottom: 3px solid #E30A17; padding-bottom: 4px; text-transform: uppercase; }
                        .kimlik-satir { display: flex; justify-content: space-between; font-weight: 700; font-size: 12px; margin-top: 4px; }
                        .sira-kutu { text-align: center; background: #E30A17; color: white; padding: 4px; border-radius: 6px; font-size: 11px; font-weight: bold; margin-top: 4px; }
                        .stats-tablo { width: 100%; border-collapse: collapse; text-align: center; font-size: 12px; margin-top: 4px; }
                        .stats-tablo th { background: #fef2f2; border: 1px solid #fca5a5; padding: 4px; color: #E30A17; }
                        .stats-tablo td { border: 1px solid #fca5a5; padding: 4px; font-weight: 900; font-size: 14px; }
                        .optik-tablo { width: 100%; border-collapse: collapse; text-align: center; font-size: 8.5px; margin-top: 4px; table-layout: fixed; }
                        .optik-tablo th, .optik-tablo td { border: 1px solid #fca5a5; height: 16px; overflow: hidden; font-weight: bold; }
                        .dogru { background: #dcfce7 !important; color: #059669 !important; }
                        .yanlis { background: #111827 !important; color: white !important; }
                        .analiz-kutu { background: #f8fafc; border-left: 5px solid #E30A17; padding: 6px 8px; font-size: 9px; line-height: 1.3; font-style: italic; font-weight: 600; text-align: justify; margin-top: 4px; color: #111827; border-radius: 4px; border: 1px solid #e2e8f0; }
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
                        html_karne += f"""
                        <div class="karne">
                            <div>
                                <div class="baslik">T.C. DARGEÇİT KAYMAKAMLIĞI - 1. MATEMATİK OLİMPİYATI SONUÇ BELGESİ</div>
                                <div class="kimlik-satir"><span style="font-size: 14px;">{row['Ad']} {row['Soyad']}</span><span style="color:#E30A17;">Öğr. No: {row['Öğrenci No']}</span></div>
                                <div class="kimlik-satir" style="color:#555;"><span>{row['OKUL ADI']}</span><span>Sınıf: {row['Sınıf']}/{row['Şube']}</span></div>
                                <div class="sira-kutu">İlçe Sırası: {row.get('İlçe Sırası','-')} &nbsp;|&nbsp; Okul Sırası: {row.get('Okul Sırası','-')}</div>
                                <table class="stats-tablo">
                                    <tr><th>Doğru</th><th>Yanlış</th><th>Boş</th><th>Net</th><th>Puan</th></tr>
                                    <tr><td style="color:#059669;">{row['Doğru']}</td><td style="color:#E30A17;">{row['Yanlış']}</td><td>{row['Boş']}</td><td style="color:#2563eb;">{row['Net']}</td><td style="background:#111827; color:white; font-size: 18px;">{row['Puan']}</td></tr>
                                </table>
                                <table class="optik-tablo"><tr>{"".join([f"<th>{j+1}</th>" for j in range(20)])}</tr><tr>{optik_icerik}</tr></table>
                            </div>
                            <div class="analiz-kutu"><b>Pedagojik Analiz:</b> {profesyonel_analiz(row)}</div>
                        </div>
                        """
                        if (i + 1) % 3 == 0 or i == len(df_filtre) - 1: html_karne += "</div>"
                    html_karne += "</body></html>"
                    c_btn3.download_button("🖨️ 3) Alt Alta Resmi Karneler (PDF)", data=html_karne, file_name=f"{kurum_secim}_Karneler.html", mime="text/html", use_container_width=True)
                    st.info("💡 Yazdırma İpucu: HTML dosyasını tarayıcıda açıp Ctrl+P yapın. Kenar boşluklarını 'Yok', arka plan grafiklerini 'Açık' yapmayı unutmayın.", icon="🖨️")
    elif sifre != "":
        st.error("Hatalı Şifre! Lütfen yetkili giriş şifrenizi kontrol ediniz.")
