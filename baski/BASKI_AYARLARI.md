# 3D BASKI AYARLARI — Ağ Fırlatıcı v5

Bu klasördeki **8 parça** 3D yazıcıdan çıkacak. Satın alınan parçalar
(kurşun bilye, alüminyum çapraz pim, lateks tüp, çelik tetik pimi, servo…)
burada **yok** — onlar `malzeme_listesi.md`'de.

> **STL'ler slicer'a hazır yöndedir.** Tablaya oturtulmuş, XY'de ortalanmış.
> **Döndürme. Sadece sürükle-bırak.** Yön kritik (bkz. §2).

---

## 1. PARÇA LİSTESİ

| Dosya | Parça | Adet | Filament | Ölçü (X×Y×Z mm) | Filament |
|---|---|---|---|---|---|
| `01_namlu` | Namlu gövdesi | 1 | **PETG** | 88 × 104 × **180.5** | ~170 g |
| `02_kapsul` | Kapsül | 1 | **PETG** | 43 × 43 × 40 | ~29 g |
| `03_tetik_kapagi_sag` | Tetik kartuş kapağı (sağ) | 1 | **PETG** | 18 × 18 × 3 | ~1 g |
| `04_tetik_kapagi_sol` | Tetik kartuş kapağı (sol) | 1 | **PETG** | 18 × 18 × 3 | ~1 g |
| `05_servo_makarasi` | Servo ip makarası | **2** | **PETG** | 18 × 18 × 8 | ~2 g |
| `06_toz_kapagi` | Arka toz kapağı (opsiyonel) | 1 | **PETG** | 49 × 49 × 6 | ~6 g |
| `07_tampon_ust` | Yarık sonu tamponu (üst) | 1 | **TPU 95A** | 9 × 7 × 3 | ~0.1 g |
| `08_tampon_alt` | Yarık sonu tamponu (alt) | 1 | **TPU 95A** | 9 × 7 × 3 | ~0.1 g |

**TOPLAM: PETG ~210 g · TPU ~0.2 g**

Her parça hem `.stl` (baskı) hem `.step` (CAD, ölçü almak/değiştirmek için)
olarak var. Ölçüler `parcalar.json`'da.

### Yazıcı şartı
**Z yüksekliği ≥ 185 mm** gerekli (namlu 180.5 mm dik basılıyor).
Tabla ≥ 110 × 110 mm. Ender 3 / Prusa MK3 / Bambu P1 sınıfı yeterli.

---

## 2. NEDEN BU YÖN — namluyu YATAY basma

Namlu kurulduğunda bant kulaklarına **toplam ~1200 N** çekme gelir.

* **Dik basılırsa** (bu klasördeki STL): kuvvet katman düzlemine **paralel**
  olur. Yük, filamentin kendi mukavemetiyle taşınır.
* **Yatay basılırsa**: kuvvet katmanları **ayırmaya** çalışır. FDM'de
  katmanlar arası dayanım, katman içi dayanımın **%40-60'ıdır**.
  Kulak kopar.

Bu pazarlık konusu değil. Aynı mantık kapsül için de geçerli: arka blok
16 mm boyunca 1200 N'u çapraz pime aktarır.

---

## 3. PETG AYARLARI

### 3.1 Ortak (tüm PETG parçalar)
```
nozzle çapı        : 0.4 mm
nozzle sıcaklığı   : 240 °C   (ilk katman 245 °C)
tabla sıcaklığı    : 80 °C
katman yüksekliği  : 0.20 mm
ilk katman         : 0.25 mm, %50 hız
hız                : 45 mm/s  (dış duvar 25 mm/s)
soğutma            : %30      ← PETG'de fazla fan katman yapışmasını BOZAR
retraction         : 4 mm @ 35 mm/s  (direct drive: 1.5 mm)
z-hop              : 0.2 mm   (PETG sicim yapar)
```

### 3.2 Parça bazlı

**`01_namlu` — en kritik parça (~14 saat)**
```
duvar (perimeter)  : 4 çevre     → 1.6 mm katı kabuk
üst/alt katman     : 5
dolgu              : %50 gyroid
destek             : YOK
brim               : 5 mm        ← 180 mm yüksek, devrilmesin
```
> Yarıklar ve delikler köprü/overhang olarak kendini taşır, destek gerekmez.
> %50'nin altına inme — bant kulakları ve tetik göbekleri dolguya oturuyor.

**`02_kapsul` (~3 saat)**
```
duvar              : 5 çevre
üst/alt            : 5
dolgu              : %60 gyroid
destek             : YOK
```
> Bilye yuvaları 13° konik — overhang değil, destek istemez.

**`03`/`04` tetik kapağı, `05` servo makarası**
```
katman             : 0.15 mm   (delik hassasiyeti için)
duvar              : 3 çevre
dolgu              : %100
destek             : YOK
```
> Küçük parçalar: ikisini/dördünü aynı anda bas, soğuma süresi artsın.

**`06` toz kapağı (opsiyonel)**
```
duvar              : 3 çevre,  dolgu %20,  destek YOK
```

---

## 4. TPU 95A AYARLARI (`07`, `08`)

```
nozzle             : 230 °C
tabla              : 50 °C
katman             : 0.20 mm
hız                : 20 mm/s     ← YAVAŞ, TPU hızda kaçırır
dolgu              : %30
duvar              : 2 çevre
retraction         : KAPALI      ← TPU'da retraction tıkanma yapar
soğutma            : %50
```
> İkisi birlikte 10 dakikada biter. Bowden ekstruderle zorlanırsan
> hızı 12 mm/s'ye düşür.

---

## 5. BASKI SONRASI İŞLEMLER

Sırayla yap:

1. **Namlu yarıklarını temizle** — iki düz yarık (9.4 mm) eğeyle açılsın.
   Kapsülün çapraz pimi buradan geçecek, takılma olmamalı.

2. **Tetik pimi deliklerini raybala** — 5.0 mm matkapla geç, sonra
   **PTFE burcu (B7)** çak.

3. **M2 ısıl insertleri otur** — 8 adet (4 kapak + 4 servo).
   Havya 220 °C, dik tut, yavaş bastır. Eğri girerse vida tutmaz.

4. **Kapsül–namlu uyumunu test et** — kapsülü namluya **boş** sok.
   Kendi ağırlığıyla kaymalı. Takılıyorsa kapsül dış çapını
   zımparala (hedef boşluk 0.3 mm).

5. **Tamponları yapıştır** — TPU tamponları yarıkların **ön ucuna**
   CA ile. Kapsülün çarpma yükünü (~450 N) bunlar yumuşatacak.

### KONTROL — geçmeden montaja başlama
- [ ] Kapsül namluda serbest kayıyor
- [ ] Tetik pimleri burçlarda pürüzsüz hareket ediyor
- [ ] 8 insert dik oturmuş, M2 vida tutuyor
- [ ] Namlu kulaklarında katman ayrışması / çatlak yok
- [ ] Tamponlar yarık ucunda sağlam

---

## 6. FİLAMENT SEÇİMİ

| | Öneri | Neden |
|---|---|---|
| **PETG** | Standart PETG yeterli | Tok, katmanlar iyi kaynaşır, 80 °C'ye dayanır |
| **ASA** (daha iyi) | Dışarıda kalacaksa | UV dayanımı. Ama kapalı kabin ister, çeker |
| **PLA** | **KULLANMA** | Kırılgan; 1200 N çekme altında ani kırılır. Güneşte 50 °C'de yumuşar |
| **ABS** | Gerekmez | PETG'den avantajı yok, baskısı zor |
| **TPU 95A** | Tampon için şart | 85A çok yumuşak, 98A çok sert |

> **PLA uyarısı ciddi.** Bu parça kurulduğunda 120 kg depoluyor ve
> güneş altında bekleyecek. PLA'da kulak kopması zaman meselesidir.

---

## 7. YEDEK BAS

İlk denemede kırılması muhtemel parçalar:
- **tetik kapağı** ×2 fazladan (ince, M2 deliği yırtılabilir)
- **servo makarası** ×2 fazladan (servo kolu markaya göre değişir, ölçü tutmayabilir)
- **tampon** ×2 fazladan (her atışta eziliyor)

Namlu ve kapsülü yedeklemek pahalı; onun yerine **ayarları doğrula**
(§5 kontrol listesi) ve bir kez doğru bas.
