# TEDARİK PLANI — doğrulanmış linkler ve sipariş sırası

> Tüm linkler tek tek **açılıp sayfa içeriğinden** doğrulandı.
> Trendyol / Hepsiburada / n11 / Koçtaş bot korumasıyla okunamadı — o
> platformlardan link **verilmedi** (ürün olabilir, ama doğrulayamadım).
> **Fiyatlar Ekim 2026 itibarıyla, değişebilir.**

---

## ⚠️ ARAŞTIRMANIN DEĞİŞTİRDİĞİ 2 TASARIM KARARI

### 1. Çapraz pim: 7075-T6 → **civa çeliği (gümüş çeliği)**
Türkiye'de **Ø8 mm 7075-T6 satılmıyor** — çekme 7075 Ø13'ten başlıyor
(aluminyumburada.com stok listesinden doğrulandı).

Tasarım gerilmesini hesapladım: kapsül kenarında M = 10170 N·mm → **202 MPa**.

| malzeme | akma | SF | karar |
|---|---|---|---|
| 7075-T6 *(hedef, TR'de yok)* | 480 MPa | 2.4× | — |
| **civa çeliği 1.2210** | 450 MPa | **2.2×** | ✅ **KULLAN** |
| 6061-T6 | 276 MPa | 1.4× | sınırda |
| 6063 *(piyasada bulunan Al)* | 170 MPa | **0.84×** | ❌ KIRILIR |
| 304 paslanmaz | 210 MPa | **1.04×** | ❌ yetersiz |

**Bedeli:** pim 13 g yerine 36 g (+23 g). Paslanır,
yağlanmalı (zaten pimleri yağlıyoruz).

### 2. Servo: MG996R → **MİKRO servo** (makara r=2.2 mm)
MG996R **110 g = sistemin %22'si** idi. İş korunumlu: `tork × açı =
F_pim × strok`. r=4 mm makara servonun dönüş aralığının yalnızca 86°'sini
kullanıyordu; **r=2.2 mm + kanal 4 mm** ile 130° kullanılıyor ve gereken
tork **3.9 → 2.15 kg·cm**'ye düşüyor.
→ **mikro metal dişli servo** (Savöx SH-0255MG / MG92B sınıfı, ~14 g,
≥3.5 kg·cm) **1.81× payla** yetiyor. **−82 g → sistem 410 g.**
Namlunun servo yatağı zaten M2/mikro için tasarlanmıştı; delik aralığı
18 → 28 mm'ye düzeltildi (oval, marka farkını tolere eder).

---

## 🔧 TEK TORNA ZİYARETİ — 5 sorunlu kalemi birden çözüyor

Zaten çapraz pim olukları için tornacıya gideceksin. **Aynı ziyarette
şunları da yaptır** — hepsi ya TR'de bulunamıyor ya çok pahalı:

| Parça | Normalde sorun | Tornada çözüm | Hammadde |
|---|---|---|---|
| **B1** çapraz pim | — | Ø8'den 92 mm kes + 4 oluk | civa çeliği Ø8 |
| **B2** tetik pimi ×2 | — | Ø5'ten 20.7 mm kes + Ø1.5 delik | civa çeliği Ø5 |
| **B7** PTFE burç ×2 | TR'de hazır **YOK** | PTFE çubuktan Ø7 dış / Ø5 iç × 10 mm | PTFE çubuk Ø8-10 |
| **B3** mil bileziği ×2 | tek kaynak **305 TL/ad** | Ø10'dan 6 mm kes, Ø5 del, yandan M3 kılavuz | civa çeliği Ø10 |
| **B5/B6** pimler | fiyat doğrulanamadı | Ø4'ten 4×16 mm, Ø3'ten 2×10 mm kes | civa çeliği Ø4, Ø3 |

**Teknik resim:** `TORNA_IS_EMRI.png` (B1 ve B2 ölçülü). Diğerleri basit kesim.

---

## 📦 SİPARİŞ 1 — MetalAVM (hammadde, tek kargo)
https://metalavm.com · yerli, TR içi kargo, sepet indirimi %2-4

| Ne | Link | Fiyat (2 m tam boy) |
|---|---|---|
| Civa çeliği Ø8 | [metalavm.com/civa-celigi-1-2210-800-mm](https://metalavm.com/civa-celigi-1-2210-800-mm) | ~360 TL + KDV |
| Civa çeliği Ø5 | [civa-celigi-1-2210-500-mm](https://metalavm.com/civa-celigi-1-2210-500-mm) | ~148 TL + KDV |
| Civa çeliği Ø4 | [civa-celigi-1-2210-400-mm](https://metalavm.com/civa-celigi-1-2210-400-mm) | ~120 TL + KDV |
| Civa çeliği Ø3 | [civa-celigi-1-2210-300-mm](https://metalavm.com/civa-celigi-1-2210-300-mm) | ~75 TL + KDV |

**≈ 700 TL + KDV.** ⚠️ Kısa boy satan online satıcı yok; 2 m almak zorundasın
(ucuz, ömür boyu yeter). Mil bileziği için **Ø10 da ekle** istersen.

## 📦 SİPARİŞ 2 — Dalış mağazası (lastik)
| Ne | Satıcı | Link | Fiyat |
|---|---|---|---|
| **O.M.E.R Performer 2 Ø16 metraj** — sayfada *"%100 doğal lateks kauçuk"* ✅ | mertsubonline | [link](https://www.mertsubonline.com/urun/o-m-e-r-performer-2-o16mm-metraj-lastik) | 1.367,80 TL |
| *alternatif* Free-Sub 16mm × 100cm ⚠️ **çift komponentli** (çekirdek doğal, kılıf sentetik) | daliselbisesi | [link](https://daliselbisesi.com/products/free-sub-metraj-zipkin-lastigi-16mm-x-100cm-zipkin-lastik) | 1.113,60 TL |

> **İç çap hiçbir sitede yazmıyor** — ama hesapladım: iç çap ±1 mm bant
> kuvvetini sadece **%4** değiştiriyor. Kritik değil. Kritik olan **dış çap**
> ve **doğal lateks**. İlkini al.

## 📦 SİPARİŞ 3 — avmarketi (iki ip, tek kargo)
| Ne | Link | Fiyat |
|---|---|---|
| DFT Bojin Dyneema **0,16 mm / 9,07 kg / 100 m** ✅ | [link](https://www.avmarketi.com/urun/dft-bojin-dyneema-ip-misina-100-m-0-16-mm-yesil) | 129,51 TL |
| DFT Bojin Dyneema **0,30 mm / 22,67 kg / 100 m** ✅ | [link](https://www.avmarketi.com/urun/dft-bojin-dyneema-ip-misina-100-m-0-30mm-yesil) | 415,32 TL |

## 📦 SİPARİŞ 4 — Robot Sepeti (servo + civata)

> ⚠️ **SERVO SEÇİMİ DEĞİŞTİ.** Aşağıdaki MG996R linki **artık geçerli değil** —
> 110 g gereksiz ağırdı. Makara r=2.2 mm'ye küçültülünce gereken tork
> 2.15 kg·cm'ye düştü ve **mikro metal dişli servo** (~14 g, ≥3.5 kg·cm,
> delik aralığı 28 mm) yetiyor. **−82 g.** Yeni servo için arama gerekli.
| Ne | Link | Fiyat |
|---|---|---|
| Tower Pro MG996R ×2 (11 kg·cm @6V) | [link](https://www.robotsepeti.com/tower-pro-mg996-r-servo-motor-180) | 257,17 ×2 = 514 TL |
| M2×6 imbus DIN912 A2 10'lu | [link](https://www.robotsepeti.com/m2x6-imbus-civata-paslanmaz) | 43,36 TL |
| M2×8 imbus DIN912 A2 10'lu | [link](https://www.robotsepeti.com/m2x8-imbus-civata-10lu) | 37,34 TL |

## 📦 SİPARİŞ 5 — hiber.com.tr (kablolar)
| Ne | Link | Fiyat |
|---|---|---|
| Y-kablo **1 JR erkek → 2 Futaba dişi** 30 cm ✅ | [link](https://www.hiber.com.tr/30-cm-y-tipi-servo-kablosu) | 71,71 TL |
| Servo uzatma 30 cm dişi-erkek | [link](https://www.hiber.com.tr/servo-uzatma-kablosu-30-cm-disi-erkek) | 85,33 TL |

> ⚡ **Y-kabloyu yalnızca SİNYAL için kullan.** İki servonun stall akımı
> 5 A; 22AWG kablo ve alıcı regülatörü yanar. +5V/GND doğrudan BEC'ten.

## 📦 SİPARİŞ 6 — tek kalemlik olanlar
| Ne | Satıcı | Link | Fiyat |
|---|---|---|---|
| M2×3 pirinç insert (Ø3.2 / 3 mm) ✅ **spec %100** | robotizmo | [link](https://www.robotizmo.net/en/insert-cakma-somun-m2-yukseklik-3mm) | 4,71 ×10 = 47 TL |
| Bagaj kantarı 50 kg / 10 g **veri kilitlemeli** | kalitelial | [link](https://kalitelial.com/product/dijital-el-kantari-ve-hassas-valiz-terazisi-50-kg-kapasiteli-termometreli-askili-tarti) | 289 TL |
| Winkel PTFE **kuru** yağlama sprey 400 ml | kulucteknik | [link](https://kulucteknik.com/urun/ptfe-kuru-yaglama-sprey-400ml) | 209 TL |
| Loctite 243 10 ml | yildizburo | [link](https://yildizburo.com) | 515 TL |
| Yay seti 200 parça (içinde 7×12,5 mm var) | worldforce | [link](https://www.worldforce.com.tr/urun/yay-seti-200-parca) | 671,80 TL |
| PTFE çubuk Ø8-10 (20 mm'den kesim) | martanonline | [link](https://martanonline.com/product/ptfe-teflon-cubuk-beyaz/) | 750 TL/kg → ~3 TL malzeme |

> **PTFE'de dikkat:** malzeme bedava sayılır ama **minimum sipariş tutarı**
> olabilir — sipariş öncesi sor.
> **Yay setinde tel çapı hiçbir sayfada yazmıyor** — set gelince kumpasla
> ölç, iç çap ≥5.3 mm olanı seç.

## 🏪 YERELDEN AL — online almak mantıksız
| Ne | Nereden | Neden |
|---|---|---|
| **Kurşun bilye** (aşağıya bak) | Av malzemesi / döküm | ↓ özel durum |
| Talk pudrası | Eczane, bebek pudrası 100-200 g | Online'da 1 kg endüstriyel çuval |
| CA yapıştırıcı | Hırdavatçı/kırtasiye | 35 TL ürüne 60 TL kargo |
| Yapıştırıcı çubuk | Kırtasiye | Aynı |
| **Koruyucu gözlük** | Hırdavatçı, EN166 **F sınıfı** yeterli | **Yüze oturması önemli, dene** |
| **İş eldiveni** | Hırdavatçı, avuç içi deri | **Beden kritik, elle dene** |

### ⚠️ KURŞUN BİLYE — özel durum
Tasarımdaki bilye **Ø12.7 mm kurşun küre = tam 12.16 g**. Piyasada:
- **misket (yuvarlak) seri 8 g'da bitiyor** → 4 g eksik
- **zeytin seri 10/15 g'a çıkıyor** ama **oval** → kapsül yuvasına (Ø12.9) oturmaz

**Çözüm:** **.50 kalibre yuvarlak kurşun** al (tam Ø12.7 mm, karabina/
muzzleloader için satılır) ve **2 mm matkapla kendin del**. Kurşun çok
yumuşak, el matkabıyla 1 dakika. Alternatif: kurşun döküm kalıbı.

---

## 💰 TAHMİNİ TOPLAM

| Grup | Tutar |
|---|---|
| Metal hammadde (MetalAVM) | ~700 TL + KDV |
| Lastik | ~1.370 TL |
| İpler | ~545 TL |
| Servo + civata | ~595 TL |
| Kablolar | ~157 TL |
| Insert + kantar + sprey + Loctite + yay seti | ~1.730 TL |
| PTFE + kurşun + yerel sarf | ~400 TL |
| **ARA TOPLAM** | **~5.500 TL** |
| 3D baskı filament (~210 g PETG) | ~150-250 TL |
| **Torna işçiliği** | **fiyat alınacak** |

> Torna işçiliği için rakam vermiyorum — güncel atölye fiyatlarını
> doğrulayamam. `TORNA_IS_EMRI.png`'yi gösterip teklif al.
> İş ~yarım saat; **malzemeyi sen götür**, onlardan alırsan pahalanır.

## 📋 SİPARİŞ SIRASI (önerilen)
1. **MetalAVM** + **PTFE çubuk** → geldiğinde **tornaya git** (en uzun süren iş)
2. Aynı gün: **lastik**, **ipler**, **servo**, **kablolar** (paralel)
3. 3D baskıları başlat (namlu ~14 saat)
4. Yerel alışveriş: kurşun, talk, CA, gözlük, eldiven
5. Hepsi gelince montaj (`URETIM_MONTAJ_REHBERI.md`)

## ❌ BULUNAMAYANLAR
- **Ø8 7075-T6** → civa çeliğiyle çözüldü (yukarıda)
- **Hazır PTFE burç 5/7×10** → PTFE çubuktan tornada
- **Ø5 mil bileziği** → tek kaynak RS 305 TL/ad, tornada yapılabilir
- **12 g delikli kurşun bilye** → .50 kalibre kurşun + kendin del
- **Tam metal dişli MG996R** → r=4 makarayla gerek kalmadı
