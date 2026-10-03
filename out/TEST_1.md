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

## 3. BANDI NASIL BAĞLAYACAKSIN — DYNEEMA YOK, PİM VAR

Ankraj yeniden tasarlandı: **bant deliğin içinden geçer, tailini bir pim deler.**
Eski 5.6 × 9 mm yuva ve Dyneema halka kaldırıldı.

### Ağız bileziği (ön uç)
- Her kenarda **Ø14 mm delik**, namlu ekseni boyunca, bilezikten baştan sona (16 mm).
- Deliğin arka ağzında **2.5 mm pah** — gergin bant kenarda kesilmesin.
- Bileziğin ön yüzünde **5.4 mm genişlik × 2.8 mm derinlik oluk**, taşıyıcı pim oraya oturur.
- Kulak kalınlığı 14 → **22 mm** (Ø14 deliğe her yandan 4 mm cidar).
- Ankraj yarıçapı 33 → **36 mm** (delik ıraksak koniyi delmesin diye).

**Bilezik artık y = 144.8'de bitiyor** (eskiden namlu ağzına kadar gidiyordu).
Bu kasıtlı: pim tam tasarımın ankraj noktasına oturuyor, böylece **L0, H ve λ
değişmiyor** — yukarıdaki hız/menzil tablosu aynen geçerli.

**Takma:**
1. Bandı arkadan Ø14 delikten geçir, ön yüzden **45 mm** çıkar.
2. Çıkan tailin ucundan **25 mm** içeride, bandı çapraz **del** (Ø5 matkap veya sivri mil).
3. **Ø5 × 30 mm çelik pimi** delikten geçir, oluğa yatır.
4. Bandı geri çek — pim oluğa oturur, kilitlenir.

### Çapraz pim (arka uç)
- Oluk 2.4 mm → **14 mm genişliğe** açıldı, Ø13 bant oturuyor.
- Çapraz pim 92 → **100 mm** uzatıldı (oluk sonuna pay).

**Takma:**
1. Bandı çapraz pimin oluğuna sar.
2. Tail'i **30 mm** geri katla, ana kolun yanına yatır.
3. Çapraz pimin ~15 mm arkasında, **ana kol + tail'i birlikte del**.
4. **Ø4 × 25 mm pimi** geçir.

### Dayanım kontrolü

| | 0.45 MPa (213 N/bant) | 0.65 MPa (308 N) |
|---|---|---|
| Ø5 pim eğilme (en kötü: nokta yük) | 61 MPa — **SF 6.6×** | 88 MPa — SF 4.6× |
| PETG oluk yatak basıncı | 5.3 MPa — **SF 9.4×** | 7.7 MPa — SF 6.5× |
| Lastik yırtılma (25 mm kenar mesafesi) | 0.47 MPa — kauçuk ~3–5 MPa | 0.68 MPa |

Bant sıyrılmaz: tail gergin değil, Ø13 kalır; pim 30 mm > delik 14 mm.
(Gergin kol λ=4'te Ø6.5'e incelir, delikten rahat geçer.)

**Riskli olan tek şey:** pim deliği lastikte çentik yaratır, kauçuk çentiğe
duyarlıdır. Birkaç atış için sorun yok; **her kurmadan önce pim bölgesine bak**,
yırtık başlangıcı görürsen tail'i kesip yeniden del.

### Bant kesim boyu
Kol başına **130 mm** (30 çalışma + 45 ön + 55 arka pay). **2 kol = 260 mm.**

### 2 bant nereye
Kenar başına **1 bant**: z = **+36** ve **−36** mm. Simetri şart.
(Ø13 bant + Ø14 delikle kenar başına ikinci ankraj sığmıyor; 4 bant istersen
çapraz pim ve kulaklar büyümeli.)

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
| `01b_agiz_basligi.stl` | **EVET** — koni 30°→40° **+ yeni bant ankrajı** |
| `02_kapsul.stl` | **EVET** — yuva 40°, R_pitch 15.5, tek boncuk |
| `V4_capraz_pim` (alüminyum, torna) | **EVET** — oluk 14 mm, boy 100 mm |
| diğerleri | hayır |

Gövdeyi zaten bastıysan tekrar basmana gerek yok; **başlık + kapsül** yeter.
