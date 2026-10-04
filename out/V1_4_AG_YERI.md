# v1.4 — AĞ ARTIK NAMLUDA, KAPSÜLÜN ÖNÜNDE

Render'da gördüğün şey doğruydu: **ağın çıkacağı yer kalmamıştı.**

---

## 1. ÖLÇÜLEN SORUN

6 boncuk borusu, 40° eğimli olduğu için ağız düzleminde elips kesit veriyor
(radyal yarı-ekseni 6.0 değil **7.83 mm**). R12 bölüm dairesinde 6 boru,
75.4 mm'lik çevrenin 72 mm'sini kaplıyor. Geriye kalan:

| | |
|---|---|
| Merkezdeki boş daire | **55 mm² (Ø8.3 eşdeğeri)** |
| Borular arası boşluk | 6 × 0.57 mm |
| Geçmesi gereken | 39.2 m ip = 11.1 cm³ |

**39 metre ipin Ø8 delikten geçmesi mümkün değil.**

## 2. BU BİR AYAR HATASI DEĞİL, MİMARİ ÇIKMAZ

Durdurma omzunun ≥250 mm² olması için namlu konisinin başlangıcı
R_om ≤ 19.34 olmalı. R_om = R_pitch + 7.08 olduğundan **R_pitch ≤ 12.26**.

R_pitch'i 12.26'ya kadar açsan bile merkezdeki boş daire **62 mm²**.

> **Durdurma omzu ile merkezi ağ çıkışı aynı kapsülde bir arada olamaz.**

R_pitch'i büyütmek omzu yok ediyor (R_pitch 15.3'te omuz sıfır), küçültmek
ağ çıkışını yok ediyor. Arada çözüm yok.

## 3. ÇÖZÜM: AĞ NAMLUYA

Ağ kapsülün içinden değil, **namlunun içinden, kapsülün önünden** çıkıyor.
Kapsül bir **piston**: ağı iterek dışarı çıkarıyor. Boncuklar yine kapsülün
yuvalarında ve 40° ile fırlıyor; iplerini önlerindeki ağa bağlıyorlar.

| | kapsül içinde (eski) | **namluda (yeni)** |
|---|---|---|
| Ağ için hacim | 22.1 cm³ | **134.6 cm³** |
| Doluluk | %75 (sıkışık) | **%8 (bol)** |
| Çıkış kesiti | 55 mm² (Ø8.3) | **tüm namlu Ø43.4** |
| Sıkışma riski | yüksek | yok |

Bu, ticari ağ tabancalarının da yaptığı şey — sabot ağı iter.

### Kapsülde ne değişti
- **Başlık artık MASİF.** Ağ geçmeyeceği için merkezi delik tamamen kaldırıldı:
  daha güçlü, takılacak çıkıntı yok.
- İç boşluk sadece **ağırlık azaltma** için, koni biçiminde ve kapalı
  (ağız yukarı basımda tavan yok, destek gerekmiyor).
- Boncuk yuvaları aynı: kapalı taban, Ø8.40 tutma dudağı, Ø3 ip/hava deliği.

### Bedeli
Kapsül 43.8 → **51.4 g** (başlık masifleşti). Çıkış hızı 23.1 → 22.0 m/s,
mesafe 0.78–0.97 → **0.73–0.95 m**. Küçük kayıp, karşılığında ağ gerçekten
çıkabiliyor.

---

## 4. YÜKLEME SIRASI DEĞİŞTİ

1. Ağı **namlunun ağzından** içeri, gevşek katlar halinde yerleştir.
   91 mm'lik strok boyunca yayılsın (çok yer var, sıkıştırma).
2. Boncukları kapsülün yuvalarına **bastırarak** oturt (dudak tutar).
   Her boncuğun ipi yuvanın ağzından öne, ağa gider.
   Durdurma düğümü boncuğun **arkasında**, yuvanın dibinde kalır.
3. Kapsülü namluya sok, çapraz pimi tak.
4. Kapsülü geri çek, tetik pimlerini sok.
5. Namlu ağzına **kırılgan ön kapak** (ince kağıt disk) yapıştır — ağ
   namluda serbest durduğu için, fırlatıcı aşağı bakarken dökülmesin.
   *(Malzeme listesinde F5)*

**Ön kapak artık opsiyonel değil, gerekli.**

---

## 5. SONUÇ

| Gmod | kurma | v_çıkış | ağ çapı | pay | mesafe |
|---|---|---|---|---|---|
| 0.25 MPa | 261 N (27 kg) | 16.4 m/s | 1.82 m | 1.06× | 0.44–0.81 m |
| 0.35 MPa | 365 N (37 kg) | 19.4 m/s | 1.89 m | 1.10× | 0.60–0.89 m |
| **0.45 MPa** | **470 N (48 kg)** | **22.0 m/s** | **1.94 m** | **1.13×** | **0.73–0.95 m** |
| 0.55 MPa | 574 N (58 kg) | 24.4 m/s | 1.97 m | 1.15× | 0.84–0.99 m |
| 0.65 MPa | 678 N (69 kg) | 26.5 m/s | 2.00 m | 1.16× | 0.86–1.03 m |

## 6. DİKKAT: DURDURMA ENERJİSİ ARTTI

Kapsül ağırlaştığı için duracak kütle **63.3 g**:

| v_çıkış | durdurulacak enerji | omuz (282 mm², TPU 2 mm) |
|---|---|---|
| 16.4 m/s | 8.5 J | rahat |
| 22.0 m/s | 15.3 J | tamam (tepe 14.092 N) |
| 26.5 m/s | 22.2 J | **sınırda** |

Bant ölçümü **0.55 MPa'nın üstü** çıkarsa tam gerdirme yapma; ya 1 bantla
git ya da omuz halkasını **iki kat** (2 × 2 mm TPU) koy.

Test merdiveni yine geçerli: ilk atış **1 bant + 40 mm çekiş**.
