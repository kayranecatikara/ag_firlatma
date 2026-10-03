# TEST 1 — İLK GERÇEK ATIŞ (6 boncuk · 2 bant)

> Bu doküman `out/TASARIM_V9.md`'nin yerine geçer. Fark: boncuk 12→**6**,
> yuva eğimi 30°→**40°**, bant 4→**2** (ilk test).
> Amaç menzil rekoru değil; **simülasyonun nerede yanıldığını görmek.**

---

## 1. NEDEN 40° — BU DEĞİŞMEZ

Boncuk 12'den 6'ya inince köşe başına kütle 8 g→4 g düşüyor. Ağı açan şey
hız değil köşelerin **radyal momentumu**; kütle yarıya inince açıyı
artırıp telafi etmek **zorunlu**:

| yuva eğimi | 6 boncuk + 2 bant, açılma payı |
|---|---|
| 30° | 0.91–1.02× → **ağ açılmaz** |
| 35° | 0.99–1.10× → yumuşak bantta açılmaz |
| **40°** | **1.08–1.17× → her sertlikte açılır** |
| 45° | 1.14–1.22× (menzil kısalır) |

30°'de basarsan ağ kanat açıklığını örtmez. Eski STL'ler 30°'ydi; **yeniden bas.**

---

## 2. BEKLENEN SONUÇ (2 bant)

Bant sertliği hâlâ ölçülmedi, o yüzden aralık olarak:

| Gmod | kurma kuvveti | çıkış hızı | açılma yarıçapı | pay | ağ açıkken mesafe |
|---|---|---|---|---|---|
| 0.25 MPa | 237 N (24 kg) | 17.4 m/s | 0.925 m | 1.08× | 0.50 – 0.84 m |
| 0.35 MPa | 331 N (34 kg) | 20.7 m/s | 0.957 m | 1.11× | 0.67 – 0.92 m |
| **0.45 MPa** | **426 N (43 kg)** | **23.5 m/s** | **0.980 m** | **1.14×** | **0.80 – 0.98 m** |
| 0.65 MPa | 615 N (63 kg) | 28.3 m/s | 1.007 m | 1.17× | 0.87 – 1.06 m |

Gereken açılma yarıçapı 0.859 m (Talon yarı kanat açıklığı).
Ağ **~90 ms**'de tam açılır, ~50 ms açık kalır, sonra çevre halatı boncukları geri çeker.

4 banda çıkınca: kurma 473–1230 N, hız 24.4–39.4 m/s, mesafe 0.84–1.31 m.

---

## 3. BANDI NASIL BAĞLAYACAKSIN — SORDUĞUN YER

**Ø13 bant o yuvaya girmez.** Ağız bileziğindeki yuva **5.6 × 9.0 mm**;
Ø13 tüp yassılaşınca ~20 × 9 mm olur. Sıkıştırarak da olmaz.

O yuva bandın kendisi için değil, **bandın ucuna bağlanan Dyneema halka** için.
Yuvanın içinden geçen Ø4 pim, halkanın takıldığı ankrajdır.

### Bağlama (her bant ucu için, toplam 4 uç)

1. Bandın ucundan **15 mm** içeride, banda sıkı bir **tek düğüm** at
   (veya ucu 20 mm geri katla). Bu, lashing'in sıyrılmasını engelleyen stoperdir.
2. **0.60 mm Dyneema'dan 300 mm** kes, ikiye katla → ~120 mm'lik halka.
3. Halkanın iki ucunu, düğümün **arkasına** gelecek şekilde bandın üstüne koy;
   üzerine **constrictor düğümü** at, sonra aynı iple **15–20 mm boyunca sıkıca sar**
   (tur aralığı bırakma). Sonu iki yarım düğüm + 1 damla japon yapıştırıcı.
4. Halkayı ağız bileziğindeki yuvadan geçir, **Ø4 ankraj pimine** tak.
5. Arka uç aynı şekilde, **çapraz pimin oluğuna**.

Yük kontrolü: 0.45 MPa'da bant başına 213 N. Çift kat 0.60 mm Dyneema
890 N, düğüm verimi %55 → **490 N. Emniyet payı 2.3×.**

### 2 bant nereye

Dört ankraj yuvası var: z = ±33 ve ±44 mm.
**İç çifti kullan: z = +33 ve z = −33.** Simetri şart — tek tarafa takarsan
kapsül namluda yan basar.

---

## 4. TESTTE MUTLAKA ÖLÇ

Simülasyonun doğrulanması için şunlar lazım:

1. **BANT SERTLİĞİ** — tek kol 50 mm kes, kantarla 135 mm'ye çek, kuvveti yaz.
   `Gmod [MPa] = F [N] / 308`. Bu tek sayı yukarıdaki tablonun hangi satırında
   olduğunu söyler. **Bunu atlarsan test yorumlanamaz.**
2. **KURMA KUVVETİ** — kapsülü geri çekerken kantarı araya koy, tepe değeri yaz.
   Tabloyla karşılaştır.
3. **ÇIKIŞ HIZI** — telefonla 240 fps çek, namlu ağzına 100 mm'lik bir cetvel
   koy, kareler arası yer değiştirmeden hesapla.
4. **AÇILMA ÇAPI ve MESAFESİ** — yere 0.5 m aralıklarla şerit çek, yandan çek.
   Ağ en geniş halindeyken: çapı kaç, namludan kaç metre ötede?
5. **AÇILDI MI, DOLAŞTI MI** — en kritik soru. Simülasyon ağın dolaşmasını
   hiç modellemiyor. Dolaşırsa nerede dolaştığını not et (köşeler mi, merkez mi).

### Not düşülecek şeyler (simülasyon bunları bilmiyor)
- Ağın kapsülden çıkış sırası düzgün mü, yoksa topak halinde mi çıkıyor
- Boncuklar yuvadan aynı anda mı çıkıyor
- Kapsül namluda sıkışıyor mu, tamponlara nasıl çarpıyor
- Bant ankrajı kayıyor mu

---

## 5. GÜVENLİK

- Kurulu sistem **426 N** depoluyor. Namlu ağzının önüne **asla** geçme.
- İlk kurmayı ağ/boncuk **takmadan** yap, tetiği boşa çalıştır.
- Gözlük tak. Boncuk 4 g × 23 m/s = ciddi.
- Kapsül arkasında kimse durmasın — çapraz pim kırılırsa geriye gider.

---

## 6. BASILACAK PARÇALAR

`baski/` klasörü **40° ve 6 boncuk** için yeniden üretildi.
Eski 30°/12 boncuk STL'leri geçersiz.

| Dosya | Değişti mi |
|---|---|
| `01a_namlu_govde.stl` | hayır (gövde aynı) |
| `01b_agiz_basligi.stl` | **EVET** — ıraksak koni 30°→40° |
| `02_kapsul.stl` | **EVET** — yuva 40°, R_pitch 15.5, tek boncuk |
| diğerleri | hayır |

Gövdeyi zaten bastıysan tekrar basmana gerek yok; **başlık + kapsül** yeter.
