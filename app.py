# YENİ NESİL IŞIK HIZINDA VE ORANTILI PDF KARNELER
            html_sablon = """
            <html><head><meta charset="utf-8"><style>
                @page { size: A4; margin: 10mm; }
                body { font-family: 'Segoe UI', Arial, sans-serif; background: white; font-size: 13px; margin: 0; color: #111827; }
                .karne { border: 2px solid #111827; border-radius: 12px; padding: 20px; margin-bottom: 25px; width: 48%; float: left; margin-right: 2%; box-sizing: border-box; page-break-inside: avoid; }
                .baslik { color: #E30A17; text-align: center; font-weight: 900; font-size: 16px; border-bottom: 3px solid #eee; padding-bottom: 8px; margin-bottom: 12px; }
                .kimlik { display: flex; justify-content: space-between; font-weight: bold; margin-bottom: 10px; font-size: 14px; }
                .siralama { text-align: center; background: #111827; color: white; padding: 8px; border-radius: 6px; margin-bottom: 15px; font-size: 12px; font-weight: bold; }
                .analiz-tablo { width: 100%; border-collapse: collapse; text-align: center; margin-bottom: 15px; font-size: 14px; }
                .analiz-tablo th { background: #f3f4f6; border: 1px solid #ccc; padding: 6px; color: #111827; }
                .analiz-tablo td { border: 1px solid #ccc; padding: 8px; font-weight: bold; font-size: 15px; }
                .optik-tablo { width: 100%; border-collapse: collapse; text-align: center; font-size: 12px; }
                .optik-tablo td, .optik-tablo th { border: 1px solid #ccc; padding: 5px; }
                .optik-tablo th { background: #e5e7eb; }
                .dogru { background-color: #dcfce7; color: #059669; font-weight: 900; }
                .yanlis { background-color: #fee2e2; color: #E30A17; font-weight: 900; font-size: 13px; }
                .bos { color: #9ca3af; font-weight: bold; }
                .yorum { margin-top: 15px; padding: 10px; background: #fef2f2; border-left: 4px solid #E30A17; font-size: 12px; font-style: italic; font-weight: 600; line-height: 1.4; }
            </style></head><body>
            """
            
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
                if p >= 85: yr = "🌟 Üstün Başarı! Olimpiyat standartlarında harika bir analitik zekaya sahipsin. 2. Aşamada başarılar!"
                elif p >= 65: yr = "👍 Çok İyi! Birkaç küçük dikkat hatası dışında hedefine çok yakınsın."
                elif p >= 40: yr = "📚 Başarılı bir temel. Düzenli soru çözümü ile netlerini artırabilirsin."
                else: yr = "💪 Bu sınav harika bir tecrübe oldu, eksiklerini kapatarak yola devam et."

                # HTML İÇİNE ÖĞRENCİ NUMARASI (Öğr. No) EKLENDİ
                html_sablon += f"""
                <div class="karne">
                    <div class="baslik">1. DARGEÇİT MATEMATİK OLİMPİYATI</div>
                    <div class="kimlik">
                        <span>{row['Ad']} {row['Soyad']}</span>
                        <span style="color:#E30A17;">Öğr. No: {row.get('Öğrenci No', '-')}</span>
                    </div>
                    <div class="kimlik" style="font-size: 12px; color: #555; margin-bottom:12px;">
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
                            <td style="font-size:16px; color:#111827; background:#fef08a;">{row['Puan']}</td>
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
                if (index + 1) % 2 == 0: html_sablon += "<div style='clear: both;'></div>"
                if (index + 1) % 6 == 0: html_sablon += "<div style='page-break-after: always; clear: both;'></div>"

            html_sablon += "</body></html>"
