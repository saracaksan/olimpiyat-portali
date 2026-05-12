# --- KUSURSUZ SİMETRİK, EŞİT BOYUTLU VE A4 UYUMLU PDF ŞABLONU ---
            html_sablon = """
            <html><head><meta charset="utf-8"><style>
                @page { size: A4 portrait; margin: 10mm; }
                * { box-sizing: border-box; }
                body { 
                    font-family: 'Segoe UI', Arial, sans-serif; background: white; margin: 0; padding: 0; 
                    color: #111827; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; 
                }
                /* Sayfa Konteyneri: Flexbox ile simetrik 2 sütun */
                .page { 
                    display: flex; flex-wrap: wrap; justify-content: space-between; align-content: flex-start;
                    width: 100%; height: 277mm; page-break-after: always; 
                }
                /* Karne Kartı: Sabit boyutlu, asla esnemez! */
                .karne { 
                    width: 48.5%; height: 88mm; border: 2px solid #111827; border-radius: 8px; 
                    padding: 8px; margin-bottom: 4mm; position: relative; overflow: hidden; background: white; 
                }
                .baslik { color: #E30A17; text-align: center; font-weight: 900; font-size: 13px; border-bottom: 2px solid #eee; padding-bottom: 4px; margin-bottom: 6px; text-transform: uppercase; }
                .kimlik { display: flex; justify-content: space-between; font-weight: bold; margin-bottom: 4px; font-size: 11px; }
                .siralama { text-align: center; background: #111827; color: white; padding: 4px; border-radius: 4px; margin-bottom: 6px; font-size: 10px; font-weight: bold; }
                
                /* Tablolar kilitlendi (table-layout: fixed). Tüm kutular milimetrik aynıdır. */
                .analiz-tablo { width: 100%; border-collapse: collapse; text-align: center; margin-bottom: 6px; font-size: 10px; table-layout: fixed; }
                .analiz-tablo th { background: #f3f4f6; border: 1px solid #ccc; padding: 3px; color: #111827; }
                .analiz-tablo td { border: 1px solid #ccc; padding: 4px; font-weight: bold; font-size: 13px; }
                
                .optik-tablo { width: 100%; border-collapse: collapse; text-align: center; font-size: 9px; table-layout: fixed; }
                .optik-tablo td, .optik-tablo th { border: 1px solid #ccc; padding: 2px 0; height: 16px; overflow: hidden; }
                .optik-tablo th { background: #e5e7eb; font-weight: bold; color:#111827; }
                
                /* Renk Garantisi */
                .dogru { background-color: #dcfce7 !important; color: #059669 !important; font-weight: 900; }
                .yanlis { background-color: #fee2e2 !important; color: #E30A17 !important; font-weight: 900; }
                .bos { color: #9ca3af; font-weight: bold; }
                
                /* Yorum kutusu her zaman kartın en altına sabitlenir (Tam Simetri) */
                .yorum { 
                    position: absolute; bottom: 8px; left: 8px; right: 8px; padding: 6px; 
                    background: #fef2f2 !important; border-left: 4px solid #E30A17; 
                    font-size: 9.5px; font-style: italic; font-weight: 600; line-height: 1.2; margin: 0; 
                }
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
                    anahtar_cvp = dogru_cevap[i]
                    key_td += f"<td>{anahtar_cvp}</td>"
                    ogr_cvp = ogr_cevap[i] if i < len(ogr_cevap) else '-'
                    
                    if ogr_cvp == anahtar_cvp and ogr_cvp != '-':
                        stu_td += f"<td class='dogru'>{ogr_cvp}</td>" 
                    elif ogr_cvp != anahtar_cvp and ogr_cvp != '-':
                        stu_td += f"<td class='yanlis'>{ogr_cvp}</td>" 
                    else:
                        stu_td += f"<td class='bos'>-</td>"

                p = row['Puan']
                if p >= 85: yr = "🌟 Üstün Başarı! Olimpiyat standartlarında harika bir zekaya sahipsin. 2. Aşamada başarılar!"
                elif p >= 65: yr = "👍 Çok İyi! Birkaç küçük dikkat hatası dışında hedefine çok yakınsın."
                elif p >= 40: yr = "📚 Başarılı bir temel. Düzenli soru çözümü ile netlerini artırabilirsin."
                else: yr = "💪 Bu sınav senin için harika bir tecrübe oldu, eksiklerini kapatarak devam et."

                html_sablon += f"""
                <div class="karne">
                    <div class="baslik">1. DARGEÇİT MATEMATİK OLİMPİYATI</div>
                    <div class="kimlik">
                        <span>{row['Ad']} {row['Soyad']}</span>
                        <span style="color:#E30A17;">Öğr. No: {row.get('Öğrenci No', '-')}</span>
                    </div>
                    <div class="kimlik" style="font-size: 10.5px; color: #555; margin-bottom:6px;">
                        <span>{row['OKUL ADI']}</span>
                        <span>Sınıf: {row['Sınıf']}/{row['Şube']}</span>
                    </div>
                    <div class="siralama">İlçe Sırası: {row['İlçe Sırası']} &nbsp;|&nbsp; Okul Sırası: {row['Okul Sırası']}</div>
                    
                    <table class="analiz-tablo">
                        <tr><th>Doğru</th><th>Yanlış</th><th>Boş</th><th>Net</th><th>Puan</th></tr>
                        <tr>
                            <td style="color:#059669;">{row['Doğru']}</td>
                            <td style="color:#E30A17;">{row['Yanlış']}</td>
                            <td style="color:#6b7280;">{row['Boş']}</td>
                            <td style="color:#2563eb;">{row['Net']}</td>
                            <td style="font-size:14px; color:#111827; background:#fef08a !important;">{row['Puan']}</td>
                        </tr>
                    </table>

                    <table class="optik-tablo">
                        <tr><td>Soru</td>{soru_th}</tr>
                        <tr><td>Cevap</td>{key_td}</tr>
                        <tr><td>Öğrenci</td>{stu_td}</tr>
                    </table>
                    
                    <div class="yorum">{yr}</div>
                </div>
                """
                
                kart_sayaci += 1
                # Her 6 karnede bir YENİ SAYFA oluştur (A4 kağıdına 6'lı tam oturuş)
                if kart_sayaci % 6 == 0 and kart_sayaci < len(f_df):
                    html_sablon += "</div><div class='page'>"

            html_sablon += "</div></body></html>"
            
            st.markdown("""<style> div[data-testid="stDownloadButton"] button { background-color: #E30A17; color: white; font-weight: bold; width:100%; border-radius: 8px;} </style>""", unsafe_allow_html=True)
            colC.download_button("🖨️ PDF Karneleri Al (Kusursuz A4 Baskı)", data=html_sablon, file_name=f"{kurum}_Karneler.html", mime="text/html")
