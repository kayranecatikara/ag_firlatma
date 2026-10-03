# TASARIM v9 — ELDEKİ MALZEMELERLE NİHAİ REVİZYON

> **GÜNCEL DEĞİL — bkz. `out/TEST_1.md`.** Bu doküman 12 boncuk / 30° / 4 bant
> konfigürasyonunu anlatır. Test konfigürasyonu 6 boncuk / 40° / 2 bant olarak
> değişti.

Ölçülen boncuk: **Captain 1216, Ø9 mm, 4 g, ortası delikli.**
Ø9 kurşun + Ø2 mm delik = **4.01 g** → ölçümle tutarlı.
(Önceki Ø8 varsayımı 14921 kg/m³ sahte yoğunluk veriyordu; o ölçüm hatalıydı.)

---

## 1. NİHAİ TASARIM

### Ağ
| | |
|---|---|
| Biçim | altıgen, köşeden köşeye **Ø2.2 m** (köşe yarıçapı 1.1 m) |
| Göz | **kare 220 mm** |
| İp | Hyper Dyneema **Ø0.60 mm / 45.40 kg** — göz, çevre halatı ve radyal bağların **hepsi aynı ip** |
| Bağ sayısı | 65 kesişim + 30 çevre + **40 radyal** = 135 |
| Ağdaki ip | 39.2 m · **kesilecek: 47.2 m** (elde 90 m → 1 deneme payı daha var) |
| Ağ kütlesi | 9.6 g |

**Yakalama kriteri — sayısal doğrulama.** Ağ düzlemindeki *en büyük boş daire* hesaplandı
(601×601 ızgara, her noktanın en yakın ipe uzaklığı):

| bölge | en büyük boş daire |
|---|---|
| iç kafes (r < 850 mm) | **220 mm** (göz hücresinin kendisi) |
| dış halka (r ≥ 850 mm) | **198 mm** |
| **tüm ağ** | **220 mm** |

9" pervane (229 mm) hiçbir yerden süzülemez. **Pay yalnızca 9 mm** — Talon'a 8" (203 mm)
pervane takılırsa bu kriter **çöker**, göz küçültülmelidir.

Kafes ±880 mm'de biter, çevre halatı 1100 mm'dedir; aradaki 220 mm'lik halkayı **40 radyal bağ**
doldurur (halat düğümleri arası tam 220 mm; radyal bağ boyu 102–381 mm, ort. 200 mm).
Dış halkanın iç kafesten *daha sıkı* çıkması, halkanın zayıf nokta olmadığını gösterir.
Ölçülü çizim: `out/AG_ORME_KILAVUZU.png`.

### Boncuklar
6 yuva × **2 × Ø9 mm (8 g/köşe)** = **12 boncuk, 48 g**.
İp boncukların deliğinden geçer, dışta figure-8 durdurma düğümü.

### Kapsül (yeniden boyutlandırıldı)
| | |
|---|---|
| Boy | 45 mm · 31.9 cm³ · ~**38.5 g** PETG |
| Yuva | 6 ad, Ø9.6 mm, derinlik 9 mm, **eğim 30°**, bölüm dairesi R16 mm |
| Hazne | Ø37.1 × 20 mm (ağ + arka boncuklar) |

### Namlu — İKİ PARÇA
| | |
|---|---|
| Boy | 149.8 mm · iç Ø43.4 mm (**değişmedi**) |
| Iraksak koni | **30°**, y=141 mm'den ağza — tamamen **ağız başlığı** parçasının içinde |
| Bölme | y=128 mm, spigot 14 mm, boşluk 0.25 mm, 3 × M3 radyal vida |
| Hacim | gövde 122.60 + başlık 31.82 = 154.42 cm³ (tek parça 155.01 → çakışma yok) |

> Koni açısı değiştiği için **sadece ağız başlığı** yeniden basılır; gövde parçası aynen geçerlidir.

### Bant
Zıpkın lastiği **Ø13 / iç Ø4**, **4 kol**, serbest boy 30.3 mm, H 14 mm, strok 91 mm.

### Kütle bütçesi
ağ 9.6 g + boncuk 48 g = **uçan 57.6 g**; + kapsül 38.5 g = **ivmelenen 96.1 g**.

---

## 2. MENZİL — BANT SERTLİĞİNİN FONKSİYONU OLARAK

Gerekli açılma yarıçapı = yarı kanat açıklığı = **0.859 m** (Talon 1718 mm).

| Gmod | Kurma kuvveti | v_çıkış | R_tepe | pay | **ATIŞ PENCERESİ** | genişlik |
|---|---|---|---|---|---|---|
| 0.25 MPa | 473 N | 20.6 m/s | 0.969 m | 1.13× | **1.34 – 1.48 m** | 0.14 m |
| 0.35 MPa | 662 N | 24.4 m/s | 0.996 m | 1.16× | **1.36 – 1.72 m** | 0.35 m |
| **0.45 MPa** | **852 N** | **27.7 m/s** | **1.013 m** | **1.18×** | **1.36 – 1.88 m** | **0.52 m** |
| 0.55 MPa | 1041 N | 30.7 m/s | 1.024 m | 1.19× | **1.36 – 2.01 m** | 0.65 m |
| 0.65 MPa | 1230 N | 33.3 m/s | 1.033 m | 1.20× | **1.37 – 2.11 m** | 0.74 m |

**Cevap: menzil ≈ 1.4 – 2.1 m.** Tüm makul sertlik aralığında ağ yeterince açılıyor
(pay ≥ 1.13×), ama pencere dar. Tipik lateks (0.45 MPa) varsayımıyla
**Talon 1.4–1.9 m öndeyken ateşlenmeli.**

### Neden bu kadar kısa
0.60 mm ip, tasarımın 0.165 mm ipine göre **metre başına 13.2× ağır ve 3.6× daha sürüklemeli**.
Orijinal tasarımın 4.0–4.5 m atış mesafesi bu iple **ulaşılamaz**; bu bir ayar değil,
malzemenin dayattığı sınırdır. Boncuk kütlesini artırmak da çözmüyor (24 g'a kadar tarandı).

### Açılma zaman geçmişi (0.45 MPa)
88 ms'de R = 1.01 m (tepe) → 240 ms'de R ≈ 0.25 m'ye **geri kapanır** → sonra serbest düşerken
yeniden yayılır (z negatif, işe yaramaz). **Kullanılabilir açık kalma süresi ~50 ms.**
Tetik zamanlaması bu yüzden ±9 ms hassasiyet ister.

---

## 3. BANT SERTLİĞİ HÂLÂ ÖLÇÜLMEDİ — NASIL ÖLÇÜLÜR

Ø13 bant için kesit A₀ = π/4·(13² − 4²) = **120.2 mm²**.

1. Banttan **tek kol** 50 mm kes, iki ucunu işaretle.
2. Bir ucu sabitle, kantarla çekerek **135 mm**'ye uzat (λ = 2.70).
3. Kantar okumasını N'ye çevir (kg × 9.81).
4. **Gmod [MPa] = F [N] / 308**

Örnek: 9.7 kg (95 N) → Gmod = 0.31 MPa.
Ölçtükten sonra yukarıdaki tablodan ilgili satırı oku.

---

## 4. AÇIK SORUNLAR (dürüst liste)

1. **Kurma kuvveti 473–1230 N.** Elle kurulamaz; kaldıraç veya vinç şart.
   *(Eski tasarım da ~1200 N istiyordu, bunu daha önce hiç raporlamamıştım.)*
2. **Pim yatak basıncı kritik.** 852 N'de Ø5 pim / 4 mm PETG duvarda 43 MPa →
   PETG ~50 MPa, **SF 1.16**. Pim yuvasına **çelik burç** veya daha kalın duvar gerekli.
   Pimin kendisi sorun değil (Ø5 çelik çift kesme SF 11×).
3. **Pencere 0.52 m / ~50 ms.** Tetik zamanlaması ±9 ms.
4. **Hiçbir yer testi yapılmadı**: ağ açılma/dolaşma, pervane kesme, düğüm verimi çekme testi.
5. **3 boncuk/yuva daha iyiydi ama sığmıyor.** Arkaya doğru yuvalar eksene yaklaştığı için
   komşu boncuklar çakışıyor; 3 boncuk Ø48 mm (25°) veya Ø51 mm (30°) namlu ister.
   Ø2.2/220/25°/3 boncuk → pencere 1.73–2.36 m (0.63 m). Namlu çapını büyütmeye değer mi,
   karar verilmedi.

---

## 5. BU REVİZYONDA DÜZELTİLEN HATALAR

- **Tepe tespiti yanlıştı.** `argmax(R[:yarı])` ağın serbest düşerken yeniden yayılmasını
  yakalıyordu; R_tepe 1.097 m ve 0.52–1.84 m penceresi **geçersizdi**. Artık **ilk yerel tepe**
  kullanılıyor; gerçek pencereler 0.3–0.7 m (benim raporladığım 1.0–1.7 m değil).
- **3 boncuk tek hatta çakışıyordu.** CAD 4.93 cm³ veriyordu, 6.37 olmalıydı. Geometrik sınır
  türetildi (R_arka ≥ 9 mm) ve 2 boncuğa inildi.
- **`malzeme_listesi.py`, `cad/ciz_v4.py`, `cad/ciz_montaj_rehber.py` çalışmıyordu** —
  yol refaktörü (`3d2888d`) `vyol()` çağrısı eklemiş ama import'u koymamıştı.
- **Malzeme listesi eski ağı sabit kodluyordu** (R 1.4, göz 140). Artık konfigden okuyor.
- **B7 satırı yanlış bölüme düşüyordu** (ikinci bir "B." başlığı açıyordu).
- **Örme kılavuzundaki radyal bağlar hiç çizilmemişti** — simülasyon onları modelliyordu ama
  kılavuz 220 mm'lik bağsız halkayı göstermiyordu. 40 bağ eklendi.
- **Bant ölçüm katsayısı eskiydi**: 473 değeri Ø15.2 bant içindi, Ø13 için **308**.
