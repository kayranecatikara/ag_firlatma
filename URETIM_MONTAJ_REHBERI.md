# ÜRETİM VE MONTAJ REHBERİ — Ağ Fırlatıcı v5

> **Bu rehber üretilecek sistemin TAMAMINI kapsar.** Sırayla uygula.
> Her bölümün sonunda bir **KONTROL** maddesi var — geçmeden sonrakine geçme.

---

## 0. ÖNCE GÜVENLİK — bunu atlama

Bu mekanizma kurulduğunda **4 lateks bantta toplam ~1200 N (120 kg)** enerji
depolar. Kurulu haldeki kapsül bir mermidir.

| Kural | Neden |
|---|---|
| **Kurulu namluyu asla kimseye doğrultma** | Kapsül 34.5 m/s ile çıkar |
| **Kurarken koruyucu gözlük tak** | Bant kopması yüze gelir |
| **Kurma sırasında namlu ağzının önüne elini sokma** | Pim kayarsa kapsül fırlar |
| **Lateks yaşlanır** — 6 ayda bir değiştir, çatlak görürsen hemen | Kopan bant kırbaç gibi savrulur |
| **Taşırken kurma** — kurulum atıştan hemen önce | Sürünme (creep) hem gücü düşürür hem risk |
| **İlk atışları yerde, ağırlıklı bir kızakta yap** | Geri tepme ~75 N·s |

**Kurma sırasında pim güvenliği:** iki tetik pimi takılı ve mil bilezikleri
(B3) sıkılı olmadan bantları germeye başlama.

---

## 1. ÜRETİM SIRASI (toplam ~3 gün + baskı süresi)

```
GÜN 1  : 3D baskıları başlat (A1 namlu ~14 saat)
         paralel: ağ örmeye başla (~2.5 saat)
GÜN 2  : baskılar biterken metal parçaları ısmarla/işlet
         bant uçlarını hazırla (D1-D3)
GÜN 3  : mekanizma montajı + kuru deneme (banttsız)
         sonra bant takma + yer testi
```

---

## 2. 3D BASKI

### 2.1 Basılacak parçalar

> **Hepsi `baski/` klasöründe.** STL'ler **slicer'a hazır yöndedir** —
> tablaya oturtulmuş, ortalanmış. **Döndürme, sadece sürükle-bırak.**
> Tam ayarlar: **`baski/BASKI_AYARLARI.md`**

| Dosya | Parça | Adet | Filament | Filament | Süre |
|---|---|---|---|---|---|
| `01_namlu` | Namlu gövdesi | 1 | **PETG** | ~170 g | ~14 sa |
| `02_kapsul` | Kapsül | 1 | **PETG** | ~29 g | ~3 sa |
| `03/04_tetik_kapagi` | Tetik kartuş kapağı | 2 | **PETG** | ~2 g | 15 dk |
| `05_servo_makarasi` | Servo ip makarası | 2 | **PETG** | ~2 g | 15 dk |
| `06_toz_kapagi` | Arka toz kapağı (ops.) | 1 | **PETG** | ~6 g | 20 dk |
| `07/08_tampon` | Yarık sonu tamponu | 2 | **TPU 95A** | ~0.2 g | 10 dk |

**TOPLAM: PETG ~210 g · TPU ~0.2 g.** Yazıcı Z yüksekliği **≥185 mm** olmalı.

> `cad/V4_bilye`, `V4_capraz_pim`, `V4_bant_*`, `V4_pim_*` **BASILMAZ** —
> bunlar satın alınan parçaların CAD'deki temsilleridir (kurşun bilye,
> alüminyum çapraz pim, lateks tüp, çelik tetik pimi).

### 2.2 Baskı ayarları

**A1 — NAMLU (en kritik parça)**
```
filament     : PETG  (ASA varsa tercih et — UV dayanımı)
nozzle       : 0.4 mm      yatak: 80 °C     nozzle: 240 °C
katman       : 0.20 mm
duvar        : 4 çevre  (≥1.6 mm)        ← bant kulakları bunu taşıyor
üst/alt      : 5 katman
dolgu        : %50 gyroid
destek       : YOK  (yarıklar ve delikler kendini taşır)
YÖN          : DİK — namlu ekseni Z'de, ağız yukarı
soğutma      : %30 (PETG'de fazla soğutma katman yapışmasını bozar)
```
**Neden dik:** bant kulaklarına gelen 1200 N çekme, katman düzlemine
**paralel** olur. Yatay basarsan kuvvet katmanları ayırmaya çalışır ve
kulak kopar. Bu pazarlık konusu değil.

**A2 — KAPSÜL**
```
PETG, 0.20 mm, 5 çevre, %60 dolgu, destek YOK
YÖN: ağız YUKARI (bilye yuvaları üstte)
```
Arka blok 16 mm boyunca 1200 N'u çapraz pime aktarır — dolguyu kısma.

**A3 — TETİK KAPAĞI (2 adet)**
```
PETG, 0.15 mm katman, %100 dolgu, düz yatır
```

**A5 — TAMPON (2 adet)**
```
TPU 95A, 0.20 mm, %30 dolgu, yavaş (20 mm/s), retraction KAPALI
```

**A4 — SERVO MAKARASI (2 adet)**
```
PETG, 0.15 mm, %100 dolgu. Servo dişlisine geçen göbek
kendi servonun kolundan ölçülerek çizilmeli (marka farkı var).
```

### 2.3 Baskı sonrası
1. Namludaki **iki düz yarığı** (6.4 mm) eğeyle temizle — kapsül çapraz pimi
   buradan geçecek, takılma olmamalı.
2. Tetik pimi deliklerine **PTFE burcu (B7)** çakmadan önce deliği 5.0 mm
   matkapla raybala.
3. **M2 ısıl gömme insertleri (C1)** havyayla otur — 8 adet (4 kapak + 4 servo).
   Havya ucu 220 °C, yavaş bastır, dik tut.
4. Kapsülü namluya **boş** sok, serbest kayıyor mu bak. Takılıyorsa yarığı
   ve kapsül dış çapını zımpara ile al (hedef boşluk 0.3 mm).

**KONTROL:** Kapsül namlu içinde kendi ağırlığıyla kayıyor mu? Hayırsa devam etme.

---

## 3. SATIN ALMA LİSTESİ

Tam liste: `malzeme_listesi.md`. Özet alışveriş:

### Metal
- [ ] **B1** Alüminyum 7075 çubuk Ø8 mm, 100 mm (çapraz pim — oluklar torna/eğe)
- [ ] **B2** Gümüş çeliği/paslanmaz çubuk Ø5 mm, 50 mm (2 tetik pimi)
- [ ] **B3** Mil bileziği Ø5 iç / Ø10 dış, set vidalı — 2 adet
- [ ] **B4** Basma yayı: iç ≥5.3, dış ≤10.2, serbest ~13 mm — 2 adet
- [ ] **B5** Paslanmaz pim Ø4 × 16 mm — 4 adet (bant ankrajı)
- [ ] **B6** Paslanmaz pim Ø3 × 10 mm — 2 adet (ip yönlendirme)
- [ ] **B7** PTFE burç iç Ø5 / dış Ø7 × 10 mm — 2 adet

### Bağlantı
- [ ] **C1** M2×3 ısıl insert — 8 ad
- [ ] **C2** M2×6 civata — 4 ad   **C3** M2×8 civata — 4 ad

### Tahrik
- [ ] **D1** Zıpkın lastiği, **SAF DOĞAL KAUÇUK**, Ø15.2 dış / Ø4 iç — 4 × 58 mm
      (silikon veya EPDM **OLMAZ** — enerji yoğunluğu çok düşük)
- [ ] **D2** Dyneema örgü halat Ø1.5 mm — 60 cm
- [ ] **D3** Sargı ipliği (naylon dikiş) — 2 m

### Elektrik
- [ ] **E1** MG996R sınıfı servo (≥11 kg·cm, metal dişli) — 2 ad
- [ ] **E2** Servo Y-kablosu  **E3** uzatma kablosu

### Ağ
- [ ] **F1** Dyneema **ÖRGÜ** balık ipi PE #1 (~0.165 mm, 8-9 kg) — 50 m makara
- [ ] **F2** Dyneema **ÖRGÜ** PE #3 (~0.285 mm, 18 kg) — 10 m
- [ ] **F4** **DELİKLİ kurşun balık ağırlığı** ~12 g, Ø12.7 mm — 6 ad
- [ ] **F5** Pelur kâğıt (kırılgan kapak)

### Sarf
- [ ] İnce makine yağı veya **PTFE kuru yağlayıcı sprey** (tercih)
- [ ] Loctite 243, CA yapıştırıcı, yapıştırıcı çubuk, talk pudrası

### Test
- [ ] Dijital bagaj kantarı 0-50 kg
- [ ] Kalın iş eldiveni, koruyucu gözlük

---

## 4. AĞ ÖRME (~2.5 saat) — en çok emek isteyen iş

### 4.1 Ağın tanımı
```
dış hat : DÜZGÜN ALTIGEN, köşe yarıçapı 1.30 m  (karşılıklı köşe arası 2.60 m)
          altıgenin her kenarı = 1.30 m
göz     : KARE, 200 mm
mesh ipi: Dyneema ÖRGÜ Ø0.165 mm (PE #1)  — F1
çevre   : Dyneema ÖRGÜ Ø0.285 mm (PE #3)  — F2, 7.8 m
bağ     : ~142 (≈83 göz kesişimi + ≈59 çevre bağlantısı)
```

### 4.2 Şablon hazırla (bunu atlama — elde düzgün olmaz)
1. Yere **2.8 × 2.8 m** kontrplak/OSB ya da düz zemin al.
2. Üzerine tebeşir/bantla **düzgün altıgen** çiz: merkezden 1.30 m'de 6 köşe,
   60° aralıklarla. (Pratik yol: 1.30 m ipin ucuna kalem bağla, daire çiz;
   sonra daire üzerinde pergeli 1.30 m'ye açıp 6 eşit yay işaretle.)
3. Altıgenin içine **200 mm aralıklı kare ızgara** çiz — iki yönde.
4. Her ızgara çizgisinin altıgen kenarını kestiği noktaya **çivi/raptiye** çak.
   Bunlar ipleri gerili tutacak.

### 4.3 İpleri ser — DÜĞÜM ATMA, SADECE SER
1. **Tek parça** ipi bir kenardaki çividen karşı kenardaki çiviye çek, çiviye
   bir tur dola, **kesme**, geri dön. Böylece zikzak giderek tüm bir yönü ser.
   (~13 hat)
2. Aynısını **dik yönde** yap. (~13 hat)
3. Toplam **~26 sürekli ip**. Hepsi gergin ama **aşırı germe** — elle çekince
   1-2 mm esneyecek kadar.

> **NEDEN SÜREKLİ:** ip boyunca düğüm yoksa tam dayanımını (64 N) korur.
> Kesip düğümlersen 35 N'a düşer. Ayrıca sürekli ip paketten çok daha
> düzgün açılır (paraşüt ip hattı mantığı).

### 4.4 Kesişimleri bağla (~83 adet)
Her kare kesişimde iki ip üst üste geçer. Bunları **birbirine düğümleme** —
sadece **kaymayı önle**:

**Yöntem (en kolay ve sağlam): sargı bağı**
1. 15 cm'lik ayrı bir ince ip parçası al (F1'den).
2. Kesişimin üstüne **çapraz sar**: önce bir yöne 3 tur, sonra dik yöne 3 tur
   (cerrahi dikişteki "çapraz sargı" gibi).
3. Ucunda **iki yarım düğüm** (square knot) at, 2 mm bırakıp kes.
4. Üstüne **bir damla CA yapıştırıcı** — Dyneema'ya tam yapışmaz ama sargıyı
   kilitler.

**Alternatif (daha hızlı): tek kravat bağı**
Kesişimi parmakla tut, ince ipi bir kez dolayıp **constrictor knot** at.
Dyneema'da constrictor iyi tutar.

> **DÜĞÜM ATMA UYARISI:** iki mesh ipini birbirine **sheet bend** ile
> bağlarsan ipler kesilmiş olur ve dayanım yarıya iner. Kesişimler
> **bağdır, ek değildir**.

### 4.5 Çevre halatını ekle (F2, ~59 bağ)
1. Ø0.285 mm halatı altıgenin **6 kenarı boyunca** ser, köşelerde
   **tam 1.30 m** olacak şekilde. Toplam 7.8 m. Uçları köşede birleştir
   (double fisherman's bend).
2. Her mesh ipinin kenara ulaştığı yerde, ipi halatın etrafına
   **3-4 tur SAR** (lacing), sonra kendi üstüne iki yarım düğüm.
   **DÜĞÜMLE BAĞLAMA.**

> **NEDEN SARARAK:** düğümlü uç 35 N taşır, sarılmış uç ~64 N.
> Ölçülen tepe yük 19 N → pay 1.9× yerine **3.4×**.

### 4.6 Bilyeleri bağla (6 adet)
1. Her **kurşun bilyenin deliğinden** 70 mm'lik F2 ipi geçir.
2. Dışta **durdurma düğümü** (figure-8) at — bilye düşmesin.
3. Diğer ucunu çevre halatının **köşesine** sar + bağla.
4. Bilye ile köşe arası serbest boy: **40 mm**.

### 4.7 Ağ bitti — KONTROL
- [ ] Altıgen düzgün mü? Karşılıklı köşeler **2.60 ± 0.03 m**
- [ ] 6 bilye köşelerde, hepsi sağlam
- [ ] Çevre halatı kesintisiz, hiçbir yerde gevşek değil
- [ ] Hiçbir kesişim kayıyor mu? Eliyle it — kaymamalı
- [ ] **Tart: ağ + bilye ≈ 74 g** olmalı (ağ ~1 g, bilyeler ~73 g)

### 4.8 KATLAMA — dolanmanın asıl belirleyicisi
> Hazne 17.3 cm³; ağ paketi **%33 doluluk** ile rahat sığar. **Hacim sorun
> değil, DÜZEN sorun.** Rastgele tıkarsan hacim yetse bile açılmaz.

**Doğru yöntem (dışarıdan içeri, akordeon):**
1. Ağı yere tam açık ser, bilyeleri 6 köşeye yay.
2. Üzerine **ince talk pudrası** serp, elle dağıt (ipler birbirine yapışmasın).
3. **Merkezden başlayarak** ağı kendi üzerine **akordeon gibi** katla:
   her kat 35 mm genişliğinde olsun (hazne çapından küçük).
4. Katlanmış şeridi **merkez uçta, bilyeler dışta** kalacak şekilde
   rulo yap. **Bilyeler EN SON, en dışta.**
5. Haznenin içine **merkez önce** koy — yani açılırken **dış halka
   önce çıkacak** ("pay-out" düzeni).
6. Bilyeleri 6 yuvasına otur (13° koni yuvalar).
7. Ağzına **pelur kâğıdı (F5)** yapıştırıcı çubukla **noktasal** yapıştır —
   zayıf tutsun, atışta yırtılsın.

> **Bu adımı ilk seferde 3 kez tekrarla.** Katlayıp çıkar, bak nasıl açılıyor.
> Model bu kısmı HESAPLAYAMIYOR; tek doğrulama senin gözün.

---

## 5. LATEKS BANT HAZIRLAMA (4 adet)

> Her bant kurulduğunda **~300 N (31 kg)** çeker. Uç bağlantısı kaçarsa
> bant kırbaç gibi savrulur. Bu bölümü dikkatli yap.

### 5.1 Ölçü
```
tüp        : Ø15.2 dış / Ø4 iç, SAF DOĞAL KAUÇUK
kesim boyu : 58 mm   =  çalışma 38 mm (L0) + 2 × 10 mm uç bağlantısı
kurulu boy : 152 mm  (λ = 4.0 uzama)
```

### 5.2 Uç halkası (her tüpün iki ucuna, toplam 8 halka)
1. **D2** Dyneema halattan 60 mm kes, uçlarını **yakma** (eriyip sertleşir).
2. Halatı **halka** yap, düğümle (double fisherman's). Halka iç çapı ~8 mm.
3. Halkanın düğümlü kısmını tüpün ucundan **10 mm içeri** sok.
4. Tüpün dışından, halkanın üstüne gelen bölgeyi **D3 sargı ipliğiyle
   sıkıca sar** — 10 mm boyunca, tur tur, üst üste bindirerek.
5. Sargı sonunu iki yarım düğümle kilitle, **CA damlat**.
6. **Uç başına toplam donanım çapı 7 mm'yi geçmesin** — yoksa namlu
   yarığından geçmez.

### 5.3 Bant testi — ATLAMA
Her bandı tek tek, **bagaj kantarıyla (H1)** çek:
```
boy 114 mm (λ=3.0) → ~184 N (18.8 kg) beklenir
boy 152 mm (λ=4.0) → ~300 N (30.6 kg) beklenir
```
- Ölçtüğün değer beklenenin **%25 altındaysa** tüp saf lateks değildir, kullanma.
- Çekerken **uç bağlantısı kayıyorsa** sargıyı yenile.
- Dört bandın kuvveti birbirinden **%10'dan fazla farklıysa** eşleştir
  (en yakın ikisini karşılıklı kenarlara koy) — asimetrik itme nişanı kaydırır.

---

## 6. MEKANİZMA MONTAJI

### 6.1 Tetik kartuşları (2 adet, namlunun iki yanında)
```
Sıra: PTFE burç → pim → yay → mil bileziği → kapak
```
1. **B7 PTFE burcu** namlunun tetik göbeğindeki deliğe çak (hafif sıkı geçme).
2. **B2 tetik pimini** burçtan geçir. Pimin **uç ucu** kapsül kanalına girecek.
3. Pimin dış ucundaki Ø1.5 mm delikten **E4 tetik ipini** geçir, düğümle.
4. **B4 yayını** pime geçir (kapağa dayanacak).
5. **B3 mil bileziğini** pim üzerinde **uçtan 12.2 mm**'ye getir, M3 set
   vidasını **Loctite 243** ile sık.
   > Dinlenmede pim ucu kanal dibine **0.3 mm** pay bırakmalı.
6. **A3 kapağı** M2×6 civatalarla (C2) insertlere tuttur. İp kapağın
   ortasındaki Ø2 delikten çıkıyor olmalı.
7. **G1 yağını** pime birkaç damla / PTFE sprey sık. Pimi elle it-çek:
   **pürüzsüz** hareket etmeli, takılırsa sök ve zımpara.

### 6.2 Servolar
1. **E1 servoyu** namlunun yan yatağına otur, M2×8 (C3) ile insertlere vidala.
2. **A4 makarasını** servo dişlisine geçir, servonun kendi kol vidasıyla sık.
3. **B6 yönlendirme pimini** kapak ile servo arasındaki deliğe çak.
4. Tetik ipini: **kapak deliği → yönlendirme pimi → servo makarası**
   yolundan geçir, makaraya 2 tur dola, düğümle.
5. İki servoyu **E2 Y-kablosuyla** birleştir — **AYNI SİNYAL** almalılar.

> **⚡ GÜÇ UYARISI:** iki servonun stall akımı ~2.5 A/adet = **5 A toplam**.
> İnce Y-kablo ve alıcı regülatörü bunu kaldırmaz, yanar.
> **Y-kabloyu yalnızca SİNYAL için kullan; +5V ve GND'yi her iki servoya
> doğrudan BEC'ten çek.**

> **Servo dişlisi hakkında:** Türkiye'de satılan MG996R'lerin tamamı
> "half metal" klon — sadece çıkış dişlisi metal, iç dişliler plastik.
> Makara yarıçapını **4 mm** tuttuğumuz için gereken tork 3.9 kg·cm
> (servo 11 kg·cm → **2.8× pay**) ve plastik dişli bunu kaldırır.
> Makarayı büyütme — r=6 mm'de pay 1.9×'e düşer.

### 6.3 Servo ayarı (bantlar TAKILI DEĞİLKEN)
1. Uçuş kontrolcüsünden servoya **"dinlenme"** konumu ver → iki pim de
   **tam içeride** (kapsül kanalına girmiş).
2. **"Ateş"** konumu ver → iki pim de **tam dışarıda** (kanaldan çıkmış).
3. İkisi **aynı anda** çıkıyor mu? Gecikme varsa servo kollarının
   açısını eşitle. **Asimetrik çekiş kapsülü yana kaydırır.**
4. Pim stroku: en az **6 mm** (kanal derinliği 5 mm + pay).

### 6.4 Tampon ve çapraz pim
1. **A5 TPU tamponlarını** namlunun iki yarığının **ön ucuna** CA ile yapıştır.
   Kapsülün çapraz pimi buraya çarparak duracak (~450 N).
2. **B1 çapraz pimini** kapsülün arka bloğundaki Ø8 deliğe geçir.
   Her iki ucu yarıklardan **eşit** çıkmalı (46 mm / 46 mm).

**KONTROL:** Bantsız, kapsülü elle namluda ileri-geri kaydır. Çapraz pim
yarıklarda takılmadan gidiyor mu? Tamponlara temas ediyor mu?

---

## 7. KURMA (COCKING) — en riskli işlem

> **Gözlük tak. Eldiven giy. Namlu ağzını kimseye doğrultma.**

### 7.1 Sıra
1. **Ağ yüklü kapsülü** namluya arkadan sok (§4.8'deki gibi paketlenmiş).
2. Kapsülü **strok sonuna kadar** (114 mm) geriye it — çapraz pim
   arka konuma gelsin.
3. **Servoları "dinlenme"ye al** → iki pim kapsül kanalına girsin.
   **Pimlerin girdiğini GÖZLE DOĞRULA.** Kapsülü elle ileri itmeye çalış,
   kıpırdamamalı.
4. Şimdi bantları tak — **tek tek, karşılıklı sırayla**:
   ```
   1. bant: üst-sağ     2. bant: alt-sol   (karşılıklı)
   3. bant: üst-sol     4. bant: alt-sağ
   ```
   Her bandın:
   - **arka halkası** → çapraz pimin oluğuna (r=33 ve r=44 mm olukları)
   - **ön halkası**  → ağız kulağındaki **B5 ankraj pimine**
5. Her bandı takarken **eldivenle ~31 kg** çekeceksin. Kısa bir kol/kanca
   kullanmak işi kolaylaştırır.
6. Dört bant da takıldıktan sonra **simetriyi kontrol et**: kapsül namlu
   ekseninde mi, yana kaçmış mı?

### 7.2 Kurulu sistem kontrolü
- [ ] İki tetik pimi de tam içeride
- [ ] Dört bant da ankraj pimlerinde, hiçbiri oluktan kaçmamış
- [ ] Kapsül eksende, yana yatmamış
- [ ] Çapraz pim iki yarıktan eşit çıkıyor
- [ ] Ön kapak (pelur kâğıt) yerinde
- [ ] **Namlu ağzı güvenli yöne bakıyor**

### 7.3 Ateşleme
Uçuş kontrolcüsünden servolara **"ateş"** sinyali → iki pim aynı anda
çekilir → kapsül 34.5 m/s ile çıkar → çapraz pim tamponlara çarpıp durur →
ağ ve bilyeler devam eder.

> **Kapsül namlu içinde kalır** — dışarı çıkan sadece ağ + 6 bilyedir.

---

## 8. YER TESTİ — uçuşa geçmeden ÖNCE

> Modelin **cevaplayamadığı tek şey dolanmadır**. Bu testler onu çözer.
> Hiçbirini atlama.

### T1 — Kuru tetik testi (bantsız, ağsız)
Servolara 20 kez ateş/dinlenme ver. Her seferinde iki pim **aynı anda**
tam çıkıp tam giriyor mu? Takılma varsa yağla/zımparala.
**Geç: 20/20.**

### T2 — Tek bant atışı (ağsız, boş kapsül)
1. Sadece **1 bant** tak (λ=4.0). Kapsül boş.
2. Namluyu bir kum torbasına doğrult, 5 m mesafe.
3. Ateşle. Kapsül tamponlara çarpıp **namluda kalmalı**.
4. Tamponlara, yarık uçlarına, ankraj pimlerine bak — çatlak var mı?

**Geç: hasar yok, kapsül namluda.**

### T3 — Tam kurulum, ağ ile YER ATIŞI  ★ en önemli test
1. Dört bant takılı, ağ §4.8'deki gibi paketlenmiş.
2. Namluyu **yukarı 30°** eğik, açık alana doğrult.
3. **Telefonla 240 fps** çek (H4).
4. Ateşle.

**Videodan ölç:**
| Ölçüm | Beklenen (model) | Senin ölçümün |
|---|---|---|
| Ağın tam açıldığı süre | ~200 ms | |
| En geniş çap | ~2.3 m | |
| Dolanma var mı? | YOK olmalı | |
| Kaç bilye serbest? | 6/6 | |

**Geç şartı:** ağ **dolanmadan** açılıyor ve çapı **≥1.8 m**'ye ulaşıyor.
- Dolanıyorsa → §4.8 katlamayı değiştir, talk pudrasını artır, tekrar dene.
- Açılmıyorsa → bilye bağ iplerinin (F3) 40 mm serbest boyunu kontrol et.

> **Bu testi en az 3 kez tekrarla.** Üçünde de temiz açılmadan uçuşa geçme.

### T4 — Statik hedef testi
1. Talon'u (ya da 1.7 m kanat açıklığında bir maket) yere/sehpaya koy.
2. **4.2 m** mesafeden ateşle (bkz. §9 — en iyi tetikleme mesafesi).
3. Ağ uçağı sarıyor mu? Pervaneye ip değiyor mu?
4. Pervaneyi elle döndür — ağ sarılıp kilitliyor mu?

### T5 — Pervane kesme testi  (modelin çözemediği ikinci şey)
1. Ağ ipinden 30 cm al, pervane kanadına sar.
2. Bagaj kantarıyla **~15 N** ger.
3. Motoru **düşük gazda** çalıştır (güvenli mesafeden, uçağı sabitle).
4. **İp kesiliyor mu, yoksa sarılıp motoru durduruyor mu?**

**Beklenen:** sarılıp durdurur. Kesiliyorsa → ipi Kevlar'a çevirmeyi
değerlendir (enine dayanımı 2.5× daha iyi).

### T6 — Bant yaşlanma kontrolü
Kurulu sistemi **30 dakika** bekletip ateşle. Çıkış hızı gözle belirgin
düştüyse lateks sürünüyor demektir → **kurulumu atıştan hemen önce yap**.

---

## 9. TETİKLEME MESAFESİ — Gazebo ölçümü

Geometrik pencere (ağın yeterince açık olduğu aralık) **3.6 – 6.8 m**,
ama **gerçek yakalama kalitesi mesafeyle hızla düşüyor**:

| tetikleme | ağın uçağa serilme oranı | aktarılan momentum | ip tepe yükü |
|---|---|---|---|
| 3.6 m | **%78** | 2.08 kg·m/s | 25.8 N |
| **4.2 m** | **%52** | 1.64 kg·m/s | 19.0 N |
| 5.0 m | %28 | 0.64 kg·m/s | 14.2 N |
| 5.8 m | %37 | 0.87 kg·m/s | 5.5 N |
| 6.5 m | %30 | 0.45 kg·m/s | 10.3 N |
| 7.0 m | %24 | 0.37 kg·m/s | 5.9 N |

**ÖNERİ: 4.0 – 4.5 m'den ateşle.**
- Uzakta ağ **yeterince açık** ama uçağın üzerinden **değip geçiyor**
- Yakında daha iyi sarıyor ama ip yükü artıyor (3.6 m'de 25.8 N)
- 4.2 m'de serilme %52, yük 19 N → **lacing** (sararak bağlama) ile pay 3.4×

> **DİKKAT — bu, önceki tavsiyemin TERSİ.** Daha önce "pencerenin uzak
> yarısından ateşle, ip yükü düşük olsun" demiştim. Gazebo'nun temas
> simülasyonu gösterdi ki uzakta ağ **yakalamıyor**. Python modeli sadece
> "ağ yeterince açık mı" diye bakıyordu; bu gerekli ama yeterli değilmiş.

**Tetikleme gecikmesi:** servo pimi ~120 ms'de çeker. 100 km/h'te bu
**0.77 m** demektir → hedef **5.0 m**'deyken tetikle ki ağ **4.2 m**'de
karşılasın.

---

## 10. UÇUŞ TESTİ

### Sıra
1. **Taret/gövde montajı** — namlu drona bağlanır (taret tasarımı henüz
   yapılmadı; şimdilik sabit, aşağı-ileri bakan bir yatak yeterli).
2. **Boş atış** (ağsız, tek bant) — uçuşta geri tepmenin dronu nasıl
   etkilediğini gör. Geri tepme toplam **~75 N·s**.
3. **Ağlı atış, hedefsiz** — havada açılmayı doğrula.
4. **Hedefli atış** — Talon ile.

### Geri tepme hakkında
Kapsül namluda durduğu için momentum kapsülle birlikte namluya geri döner.
Net dışarı atılan momentum = ağ + bilyeler = 74 g × 34.5 m/s ≈ **2.6 kg·m/s**.
Tail-sitter için tek atışlık bir itme; nişan kayması önemsiz (tek atış
yapılıp inilecek).

---

## 11. SORUN GİDERME

| Belirti | Olası sebep | Çözüm |
|---|---|---|
| Ağ dolanıp açılmıyor | Rastgele paketleme | §4.8 akordeon katlama, talk pudrası |
| Ağ yarım açılıyor | Bilye bağ ipi kısa/uzun | F3 serbest boyu 40 mm'ye ayarla |
| Kapsül yana kaçıyor | Bantlar eşit değil | Bantları kuvvete göre eşleştir, karşılıklı tak |
| Tek pim geç çekiyor | Servo kolları farklı açıda | §6.3 servo ayarını tekrarla |
| Pim takılıyor | Yağsız / burç dar | PTFE sprey; deliği raybala |
| Bant ankrajdan kaçıyor | Uç sargısı gevşek | §5.2 sargıyı yenile, CA damlat |
| Kulak çatlıyor | Namlu YATAY basılmış | Dik bas (§2.2) — katman yönü kritik |
| Çıkış hızı düşük | Lateks yaşlanmış/sahte | Bagaj kantarıyla test (§5.3) |
| Ağ hedefe değip geçiyor | Çok uzaktan ateşlendi | 4.0–4.5 m'den ateşle (§9) |

---

## 12. SİSTEM ÖZETİ — ne ürettiğin

```
NAMLU      : Ø55.4 dış × 180.5 mm, PETG, düz delik, arkadan yüklemeli
TAHRİK     : 4 × lateks tüp Ø15.2/4, kurulu λ=4.0, toplam ~1200 N
STROK      : 114 mm
KAPSÜL     : Ø43.1 × 38 mm, 6 bilye yuvası (13° koni), ağ haznesi Ø37.1 × 14
TETİK      : 2 karşılıklı çelik pim, PTFE burç, 2 × MG996R servo, Y-kablo
AĞ         : altıgen Ø2.6 m, KARE göz 200 mm, Dyneema örgü Ø0.165
             + çevre halatı Ø0.285, ~142 bağ, ~26 sürekli ip
BİLYE      : 6 × Ø12.7 delikli kurşun, ~12 g
KÜTLE      : ~469 g (servolar dahil)

PERFORMANS (Gazebo + Python, doğrulanmış)
  çıkış hızı       : 34.5 m/s
  açılma           : 200 ms'de R = 1.14 m  (gereken 0.859)
  geometrik pencere: 3.6 – 6.8 m
  EN İYİ TETİKLEME : 4.0 – 4.5 m
  ip tepe yükü     : 19 N  (lacing ile pay 3.4×, düğümle 1.9×)
  kopan eleman     : 0
```

---

## 13. DOĞRULANMAMIŞ — bunları test edeceksin

Modelin **söyleyemediği** üç şey var. Üçü de yer testiyle çözülür:

1. **Ağın dolanmadan açılması** (§T3) — rijit-cisim çözücüsü ipin ipe
   takılmasını modelleyemez. **En kritik belirsizlik.**
2. **Pervanenin ipi kesip kesmediği** (§T5) — kesme eşiği modelle
   belirlenemiyor; eğilim biliniyor, mutlak değer bilinmiyor.
3. **Düğüm/lacing verimi** — %55 (düğüm) ve %90 (lacing) literatür tahmini.
   Gerçek numuneyle çekme testi yap.

Ayrıca **taret tasarımı henüz yapılmadı** (senin isteğinle ertelendi).

---

## 14. HIZLI KONTROL LİSTESİ (atış öncesi, her seferinde)

- [ ] Gözlük takıldı
- [ ] Ağ §4.8'e göre katlandı, talk pudrası uygulandı
- [ ] 6 bilye yuvalarında
- [ ] Pelur kâğıt kapak yapıştırıldı
- [ ] Kapsül strok sonuna itildi
- [ ] **İki pim de kanala girdi** (gözle doğrulandı)
- [ ] Kapsül elle itilince kıpırdamıyor
- [ ] 4 bant takılı, hiçbiri oluktan kaçmamış
- [ ] Kapsül eksende
- [ ] Namlu ağzı güvenli yönde
- [ ] Servolar Y-kablodan aynı sinyali alıyor
