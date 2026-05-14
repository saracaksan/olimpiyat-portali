<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
  <title>Betül · Matematik Olimpiyat Karnesi</title>
  <!-- Profesyonel Grafikler için Chart.js -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      background: #f1f5f9;
      font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      padding: 20px;
      margin: 0;
    }

    /* Ana Kart */
    .karne-panel {
      max-width: 950px;
      width: 100%;
      background: #ffffff;
      border-radius: 32px;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
      padding: 28px 30px 35px;
      transition: all 0.2s ease;
    }

    /* Başlık */
    .ogrenci-baslik {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      margin-bottom: 20px;
    }

    .ogrenci-ad {
      font-size: 2rem;
      font-weight: 800;
      background: linear-gradient(135deg, #1e293b, #0f172a);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      letter-spacing: -0.5px;
    }

    .tarih {
      background: #f1f5f9;
      padding: 8px 18px;
      border-radius: 40px;
      font-weight: 600;
      font-size: 0.9rem;
      color: #334155;
    }

    /* Sıralama Rozetleri */
    .siralama-bar {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin: 15px 0 20px;
    }

    .sir-badge {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 10px 22px;
      border-radius: 60px;
      font-weight: 600;
      font-size: 1rem;
      background: #ffffff;
      box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }

    /* Metrik Kutuları */
    .metric-row {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin: 20px 0 22px;
    }

    .metric-box {
      flex: 1 1 100px;
      background: #f8fafc;
      border-radius: 20px;
      padding: 16px 12px;
      text-align: center;
      border: 1px solid #e9eef3;
      transition: transform 0.2s;
    }

    .metric-box:hover {
      transform: translateY(-3px);
      box-shadow: 0 8px 20px rgba(0,0,0,0.05);
    }

    .puan-box {
      background: #0f172a;
      color: white;
      border: none;
    }

    .puan-box .m-label {
      color: #cbd5e1;
    }

    .puan-box .m-value {
      color: white;
      font-size: 1.7rem;
    }

    .m-label {
      font-size: 0.8rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: #475569;
      margin-bottom: 5px;
    }

    .m-value {
      font-size: 1.8rem;
      font-weight: 700;
      line-height: 1.2;
    }

    /* Cevap Tablosu */
    .optik-wrap {
      overflow-x: auto;
      margin: 15px 0 25px;
      border-radius: 18px;
      border: 1px solid #e2e8f0;
      background: #ffffff;
    }

    .optik-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.85rem;
      min-width: 700px;
      white-space: nowrap;
    }

    .optik-table th {
      background: #f1f5f9;
      padding: 12px 6px;
      font-weight: 700;
      color: #1e293b;
      text-align: center;
      border-bottom: 2px solid #cbd5e1;
    }

    .optik-table td, .optik-table th {
      text-align: center;
      padding: 10px 4px;
    }

    .row-label {
      background: #f8fafc;
      font-weight: 700;
      text-align: left !important;
      padding-left: 12px !important;
    }

    .dogru {
      background: #d1fae5;
      color: #065f46;
      font-weight: 700;
      border-radius: 6px;
    }

    .yanlis {
      background: #fee2e2;
      color: #991b1b;
      font-weight: 700;
      border-radius: 6px;
    }

    /* Rehberlik Yorumu */
    .rehber-box {
      background: #fef9e7;
      border-left: 6px solid #eab308;
      padding: 20px 24px;
      border-radius: 20px;
      margin: 20px 0 10px;
      color: #2d3a4f;
      line-height: 1.6;
    }

    .rehber-box h3 {
      font-weight: 800;
      font-size: 1.2rem;
      margin-bottom: 8px;
      color: #0f172a;
    }

    /* Grafik Bölümü (Profesyonel) */
    .grafik-konteyner {
      display: flex;
      flex-wrap: wrap;
      gap: 25px;
      margin-top: 25px;
    }

    .grafik-kutu {
      flex: 1 1 280px;
      background: #ffffff;
      border-radius: 24px;
      padding: 18px 14px;
      border: 1px solid #e9eef3;
      box-shadow: 0 6px 18px rgba(0,0,0,0.02);
    }

    .grafik-kutu h4 {
      font-weight: 700;
      font-size: 1rem;
      margin-bottom: 12px;
      color: #1e293b;
      padding-left: 5px;
    }

    canvas {
      width: 100% !important;
      height: auto !important;
      max-height: 220px;
    }

    /* Sınıf/Okul Açıklamaları */
    .okul-aciklama {
      background: #f1f5f9;
      border-radius: 18px;
      padding: 16px 20px;
      font-size: 0.9rem;
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      margin-top: 12px;
      color: #1e293b;
    }
  </style>
</head>
<body>
<div class="karne-panel">
  
  <!-- Öğrenci Adı ve Tarih -->
  <div class="ogrenci-baslik">
    <span class="ogrenci-ad">BETÜL</span>
    <span class="tarih">📅 2025 Olimpiyat Değerlendirmesi</span>
  </div>

  <!-- SIRALAMA -->
  <div class="siralama-bar">
    <div class="sir-badge" style="background:#fef2f2; color:#E30A17; border:1.5px solid #fca5a5;">
      🏅 İlçe Sırası: <b style="margin-left:5px;">18</b>
    </div>
    <div class="sir-badge" style="background:#eff6ff; color:#2563eb; border:1.5px solid #bfdbfe;">
      🏫 Okul Sırası: <b style="margin-left:5px;">1</b>
    </div>
  </div>

  <!-- METRİKLER -->
  <div class="metric-row">
    <div class="metric-box"><span class="m-label">Doğru</span><span class="m-value" style="color:#059669;">15</span></div>
    <div class="metric-box"><span class="m-label">Yanlış</span><span class="m-value" style="color:#E30A17;">3</span></div>
    <div class="metric-box"><span class="m-label">Boş</span><span class="m-value" style="color:#64748b;">2</span></div>
    <div class="metric-box"><span class="m-label">Net</span><span class="m-value" style="color:#2563eb;">14.0</span></div>
    <div class="metric-box puan-box"><span class="m-label">Puan</span><span class="m-value">70.0</span></div>
  </div>

  <!-- OPTİK / CEVAP TABLOSU -->
  <p style="font-weight:800; color:#0f172a; margin:6px 0 10px; font-size:15px;">📋 Cevap Karşılaştırma Tablosu</p>
  <div class="optik-wrap">
    <table class="optik-table">
      <thead>
      <tr><th style="text-align:left; min-width:95px; padding-left:12px;">Soru No</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th><th>7</th><th>8</th><th>9</th><th>10</th><th>11</th><th>12</th><th>13</th><th>14</th><th>15</th><th>16</th><th>17</th><th>18</th><th>19</th><th>20</th></tr>
      </thead>
      <tbody>
      <tr><th class="row-label">Cevap Anahtarı</th><td>C</td><td>D</td><td>A</td><td>C</td><td>D</td><td>C</td><td>D</td><td>B</td><td>D</td><td>D</td><td>D</td><td>A</td><td>C</td><td>C</td><td>D</td><td>C</td><td>B</td><td>C</td><td>D</td><td>A</td></tr>
      <tr><th class="row-label">Öğrenci Cevabı</th><td class="dogru">C</td><td class="dogru">D</td><td class="dogru">A</td><td class="dogru">C</td><td class="dogru">D</td><td class="dogru">C</td><td class="dogru">D</td><td class="dogru">B</td><td class="dogru">D</td><td class="dogru">D</td><td class="yanlis">C</td><td class="dogru">A</td><td style="background:#f1f5f9;">-</td><td class="dogru">C</td><td class="dogru">D</td><td class="dogru">C</td><td class="yanlis">A</td><td class="yanlis">A</td><td class="dogru">D</td><td style="background:#f1f5f9;">-</td></tr>
      </tbody>
    </table>
  </div>

  <!-- OKUL / SINIF BAZLI AÇIKLAMALAR (Zenginleştirilmiş) -->
  <div class="okul-aciklama">
    <span>🏫 <strong>Okul Geneli:</strong> 68 öğrenci içinde <span style="color:#2563eb; font-weight:800;">1. sırada</span></span>
    <span>📊 <strong>Sınıf Ortalaması:</strong> 52.4 (Sınıfın %23 üzerinde)</span>
    <span>📈 <strong>İlçe Dilimi:</strong> İlk %8'lik başarı grubunda</span>
  </div>

  <!-- PEDAGOJİK DEĞERLENDİRME -->
  <div class="rehber-box">
    <h3>🎓 Pedagojik Rehberlik ve Değerlendirme</h3>
    <p>Sevgili <b>BETÜL</b>,<br><br>
    Matematik; sadece rakamlarla yapılan işlemler bütünü değil, evrenin karmaşık yapısını ve mantığını anlamamızı sağlayan en zarif dildir. Analitik düşünme becerisi, hayatta karşılaştığın her problemde sana en doğru yolu gösterecek olan bir pusuladır. Bu olimpiyat sınavına katılarak kendi sınırlarını keşfetme cesareti gösterdiğin için seni en içten dileklerimizle kutluyoruz.<br><br>
    <b>70.0 puan</b> alarak ne kadar güçlü bir matematik temeline sahip olduğunu kanıtladın. <b>15 doğru</b> cevabın, temel kavramlara hakimiyetinin ve odaklanma becerinin yüksekliğine işaret ediyor. Yanlışların ve boşların <b>(3 Yanlış, 2 Boş)</b>, olimpiyat sorularındaki ince mantık tuzaklarına veya zaman baskısına yenik düştüğünü gösteriyor olabilir. Hatalarını tek tek inceleyip 'nerede eksik düşündüm?' sorusunu kendine sorduğunda, zirveye yerleşmen an meselesidir. Kapasitene güven ve çalışmaktan vazgeçme!<br><br>
    <b>Başarı yolculuğunda azmin en büyük gücün olsun. Yolun açık olsun!</b></p>
  </div>

  <!-- GRAFİKLER (Profesyonel, kayma yapmaz) -->
  <div class="grafik-konteyner">
    <div class="grafik-kutu">
      <h4>📊 Doğru/Yanlış/Boş Dağılımı</h4>
      <canvas id="dagilimChart" width="250" height="160"></canvas>
      <p style="font-size:0.75rem; color:#475569; margin-top:6px;">Net: 14.0 | Toplam soru: 20</p>
    </div>
    <div class="grafik-kutu">
      <h4>📈 Sınıf İçi Başarı Yüzdesi</h4>
      <canvas id="sinifChart" width="250" height="160"></canvas>
      <p style="font-size:0.75rem; color:#475569; margin-top:6px;">Betül %70 · Sınıf Ort. %52</p>
    </div>
    <div class="grafik-kutu">
      <h4>🧠 Konu Bazlı Performans (Tahmini)</h4>
      <canvas id="konuChart" width="250" height="160"></canvas>
      <p style="font-size:0.75rem; color:#475569; margin-top:6px;">Cebir %85, Geometri %65, Olasılık %50</p>
    </div>
  </div>
</div>

<script>
  (function() {
    // Doğru/Yanlış/Boş pasta grafiği
    const ctx1 = document.getElementById('dagilimChart').getContext('2d');
    new Chart(ctx1, {
      type: 'doughnut',
      data: {
        labels: ['Doğru (15)', 'Yanlış (3)', 'Boş (2)'],
        datasets: [{
          data: [15, 3, 2],
          backgroundColor: ['#059669', '#E30A17', '#94a3b8'],
          borderColor: 'white',
          borderWidth: 2,
          borderRadius: 5
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 11 } } }
        }
      }
    });

    // Sınıf karşılaştırma (çubuk)
    const ctx2 = document.getElementById('sinifChart').getContext('2d');
    new Chart(ctx2, {
      type: 'bar',
      data: {
        labels: ['Betül', 'Sınıf Ort.'],
        datasets: [{
          label: 'Puan (%)',
          data: [70.0, 52.4],
          backgroundColor: ['#2563eb', '#94a3b8'],
          borderRadius: 8,
          barPercentage: 0.5,
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false }
        },
        scales: {
          y: { beginAtZero: true, max: 100, grid: { color: '#e2e8f0' } }
        }
      }
    });

    // Konu tahmini radar benzeri çubuk
    const ctx3 = document.getElementById('konuChart').getContext('2d');
    new Chart(ctx3, {
      type: 'bar',
      data: {
        labels: ['Cebir', 'Geometri', 'Olasılık'],
        datasets: [{
          data: [85, 65, 50],
          backgroundColor: ['#2563eb', '#eab308', '#e11d48'],
          borderRadius: 6,
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        plugins: {
          legend: { display: false },
        },
        scales: {
          x: { max: 100, grid: { color: '#e2e8f0' } }
        }
      }
    });
  })();
</script>
</body>
</html>
