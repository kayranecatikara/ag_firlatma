# v1.1 — DURDURMA OMUZU

v1 ile aynı: namlu 149.8 mm · strok 91 · L0 30.3 · koni 40° · 6 boncuk · 2 bant.
**Tek değişiklik: kapsülü ne durduracağı.**

---

## 1. SORUN

Kapsül namludan **çıkmıyor**; namlu içinde durması gerekiyor.
Duracak kütle = kapsül 35.5 g + çapraz pim 11.9 g = **47.4 g**.
Tam gerdirilmiş 2 bantla çıkış hızı 23.2 m/s → **12.8 J durdurulacak enerji**.

v1'de bunu durduran tek şey **Ø8 çapraz pimin yarık ucuna çarpması**:
temas alanı 96 mm², PETG'in taşıyabileceği azami kuvvet 4.800 N.
3 mm'lik TPU tampon ancak 3.5 J yutuyor. **Tam gerdirilirse yarık ucu kırılır.**

## 2. "SERTÇE ÇARPSIN" NEDEN OLMAZ

Enerji yok olmuyor, bir yere gitmek zorunda: **F × d = E**.
Durma mesafesi kısaldıkça kuvvet büyür.

| durma mesafesi | kuvvet (12.8 J için) |
|---|---|
| 0.2 mm (sert PETG-PETG) | **64.000 N ≈ 6.5 ton** |
| 1.2 mm (TPU ezilmesi) | 10.700 N |
| 5 mm | 2.560 N |

Saf PETG-PETG çarpmayı elastik olarak da hesapladım: temas rijitliği
`k = EA/L ≈ 6.1×10⁷ N/m`, `F = √(2kE) = 39.800 N` → **132 MPa**.
PETG 50 MPa'da kırılır. **Uyumlu katman şart** — enerjiyi "yutmak" için değil,
durmayı uzatıp kuvvet tepesini düşürmek için.

## 3. ÇÖZÜM: OMUZ + BONCUK ÇEMBERİNİ KÜÇÜLTME

Namlu ağzına içe doğru tam daire bir omuz; kapsülün halka kenarı ona oturuyor.
**Ama bu, boncuk çemberi küçülmeden anlamsız:**

| R_pitch | boncuk dış kenarı | omuz iç R | halka alanı | F_max |
|---|---|---|---|---|
| 15.5 (v1) | 20.0 | 21.0 | **74 mm²** | 3.676 N ← pimden kötü |
| 13.0 | 17.5 | 20.2 | 180 mm² | 8.992 N |
| **12.0** | 16.5 | **19.18** | **303 mm²** | **15.174 N** |

v1'de omuz zaten denenmiş ve kaldırılmıştı — çünkü R_pitch 15.5'te omuza
yer kalmıyor, boncuklar omuza çarpıyordu. **R_pitch 12.0'a inince** omuz
303 mm² oluyor: eski durdurmanın **3.2 katı kuvvet**.

Anti-çakışma sınırı R_pitch ≥ 11.89 (komşu yuvaların boncukları değmesin);
12.0 bu sınırın hemen üstünde, arka boncuk ekseni 9.11 mm.

### Enerji dengesi
- TPU halka (2 mm, 303 mm²): 1.2 mm ezilir → **7.3 J**
- Kalan 5.5 J elastik, 15.174 N'de **0.36 mm**
- Tepe kuvvet ≤ 15.174 N, PETG sınırının altında ✓

## 4. YOLDA YAKALANAN HATA

Koni, TPU kalınlığı kadar **geriden** başlıyor; bu kayma boncuk açıklığını
yiyor. İlk denemede namlu ağzında boncuklar koniye **1.1 mm giriyordu**.
Düzeltme: omuz yarıçapına `t_omuz × tan(ALFA)` kadar fazladan pay eklendi
ve bu artık ALFA'dan türetiliyor (açı değişirse kendiliğinden düzeliyor).

Doğrulama (`cad/kontrol_omuz.py`):
- omuz düzleminde pay **+2.68 mm**
- namlu ağzında pay **+1.00 mm**

## 5. PERFORMANSA ETKİSİ: YOK

| Gmod | v1 mesafe | **v1.1 mesafe** | v1.1 pay |
|---|---|---|---|
| 0.25 MPa | 0.50–0.84 m | 0.49–0.83 m | 1.07× |
| 0.45 MPa | 0.80–0.98 m | **0.79–0.97 m** | 1.14× |
| 0.65 MPa | 0.87–1.06 m | 0.86–1.05 m | 1.17× |

Fark 1–2 cm. Yani daha iyi durdurma **bedava geldi.**

## 6. BASKIDA NE DEĞİŞTİ

| Dosya | Durum |
|---|---|
| `01a_namlu_govde` | değişmedi |
| `01b_agiz_basligi` | **YENİ** — durdurma omuzu eklendi (31.8 → 40.6 cm³) |
| `02_kapsul` | **YENİ** — yuvalar R12.0'a çekildi |
| `10_omuz_halkasi` | **YENİ PARÇA** — TPU 95A, Ø43 × 2 mm halka, 0.7 g |
| diğerleri | değişmedi |

TPU halka omuzun arkasındaki cebe **yapıştırılır** (yk..yk+2 mm).
Yerinden çıkarsa PETG omuz yedek olarak devrede kalır — ama tam gerdirilmiş
atışta yapıştırıcı şart.

## 7. TEST MERDİVENİ (yine de kademeli git)

Omuz 15.174 N taşıyor ve tam atış 12.8 J gerektiriyor; hesap tutuyor ama
**hiç gerçek veri yok**. İlk atışı yine düşük çekişle yap:

| çekiş | 1 bant | 2 bant |
|---|---|---|
| 40 mm | 1.6 J | 3.1 J |
| 55 mm | 2.7 J | 5.4 J |
| 70 mm | 4.2 J | 8.3 J |
| 91 mm (tam) | 6.6 J | **12.8 J** |

Her atıştan sonra omuz halkasına ve kapsülün ön kenarına bak.
