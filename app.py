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
