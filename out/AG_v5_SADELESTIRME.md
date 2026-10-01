# AĞ SADELEŞTİRME (v5) — "tek ip yeter" tezinin sonuçları

## Tetikleyici
Kullanıcı itirazı: *"Bu ağın tek bir ipinin pervaneye değmesi uçağı
düşürmeye yeter. Sen ipi bu kadar fazla kullanıyorsun ama ağın hazne
içinde açılıp açılmayacağını, birbirine dolanıp kalmayacağını hiç
düşünmüyorsun."*

İtirazın **üç parçası doğru, bir parçası fazla iddialı** çıktı.

---

## 1. "Tek ip pervaneye değse yeter" — DOĞRU ✓
Motor stall torku ipi `T = τ/r_sarım` ile gerer:

| τ_stall | r_sarım 12 mm | 20 mm | 30 mm |
|---|---|---|---|
| 0.15 N·m | 12.5 N | 7.5 N | 5.0 N |
| 0.30 N·m | 25.0 N | 15.0 N | 10.0 N |
| 0.50 N·m | 41.7 N | 25.0 N | 16.7 N |

Tek ip: lif 64.1 N, düğümlü 35.3 N. **Dokuz durumun sekizinde tek ip yeter.**

### Bunun büyük sonucu: GÖZ ŞARTI DEĞİŞTİ
Eski kriter: *pervane diskinin içinde bir DÜĞÜM bulunmalı* → `göz < D/√2 = 163 mm`
Yeni kriter: *pervane diskini en az bir İP kesmeli* → `göz < D = 230 mm`

Pervane Ø230 mm. **Göz 180 mm seçildi (%22 pay).**
En kötü durumda (pervane hücre ortasında) diske giren ip uzunluğu 143 mm —
sarılmaya fazlasıyla yeter.

## 2. "Ağ aşırı büyük, bu kadar ipe gerek yok" — DOĞRU ✓
Kaba göz **her eksende** daha iyi çıktı (az iplik = az sürükleme = uzak menzil):

| tasarım | bağ | iplik | kütle | emek | R_açık | pencere |
|---|---|---|---|---|---|---|
| ESKİ: altıgen Ø2.8 göz140 | 811 | 100 m | 2.08 g | 13.5 sa | 1.170 | 3.56 – 6.44 |
| ara: kare Ø2.8 göz140 | 315 | 81 m | 1.69 g | 5.2 sa | 1.127 | 3.56 – 6.22 |
| **YENİ: kare Ø2.6 göz180** | **179** | **59 m** | **1.17 g** | **3.0 sa** | **1.129** | **3.58 – 6.62** |

**Bağ %78 ↓, iplik %41 ↓, el emeği %78 ↓ — ve pencere 0.18 m UZADI.**

## 3. "Dolanmayı hiç düşünmüyorsun" — HAKLI ELEŞTİRİ ✓
Modellememiştim. Ölçülebilen göstergeler:

| gösterge | eski (altıgen) | yeni (kare) |
|---|---|---|
| toplam iplik | 100 m | 59 m |
| bağ sayısı (takılma noktası) | 811 | 179 |
| **sürekli ip sayısı** | **1257 ayrı kenar (ort. 8 cm)** | **~28 ip (ort. 1.8 m)** |
| hazne dolgu oranı | %10.5 | %5.9 |

En önemlisi sonuncudan bir önceki: altıgen kafeste her kenar ayrı bir
parçadır; kare gözde ipler baştan sona **süreklidir**. Paraşüt ip hattı
mantığı — az sayıda uzun ip, çok sayıda kısa parçadan çok daha düzgün açılır.

> **MODELLENEMİYOR:** ipin ipe takılması (self-contact). Rijit-cisim + LCP
> çözücüsüyle çözülemez; ip/kumaş çözücüsü gerekir. **Tek doğrulama yolu
> YER TESTİ:** ağı pakete koy, yerde ateşle, yüksek hızlı kamera ya da
> gözle açılmayı doğrula. Bu test YAPILMADAN uçuş denemesine geçilmemeli.

## 4. "Bilyeler uçağı kırar" — FAZLA İDDİALI ✗
| bağıl hız | tek bilye | 6 bilye |
|---|---|---|
| 15 m/s | 1.37 J | 8.2 J |
| 20 m/s | 2.43 J | 14.6 J |

20 m/s'de tek bilye 2.43 J — 0.8 kg'ı 30 cm'den düşürmeye denk. EPO köpüğe
çukur açar, kumanda yüzeyini sıkıştırabilir; **yapı kırmaz**. Gazebo ölçümü
de bunu doğruluyor: uçağa aktarılan 1.05 kg·m/s → 1.8 kg'lık uçakta
0.58–0.95 m/s hız değişimi. İtiyor, parçalamıyor.
**Asıl öldürücü mekanizma PERVANE; bilyeler ikincil.**

---

## 5. Gazebo doğrulaması (tetikleme 4.50 m — en ağır yük)
| tasarım | T_tepe | kopan | >%50 | pay | ağın hedefte | hedef v |
|---|---|---|---|---|---|---|
| kare Ø2.8 göz140 (4.65 m) | 7.8 N | 0 | 0 | 4.5× | %33 | 0.50 m/s |
| kare Ø2.6 göz200 | 16.9 N | 0 | 0 | 2.1× | %47 | 0.86 m/s |
| **kare Ø2.6 göz180** | **14.8 N** | **0** | **0** | **2.4×** | **%51** | **0.95 m/s** |
| kare Ø2.6 göz160 | 19.3 N | 0 | **2** | 1.8× | %55 | 0.87 m/s |

İki bulgu:
1. **Kaba ağ hedefe DAHA ÇOK seriliyor ve 1.9× fazla momentum aktarıyor.**
   Az sayıda uzun ip daha iyi sarıyor; ince örgü bir "yaprak" gibi kayıyor.
2. Gerilme arttı (yükü paylaşan eleman azaldı) ama 160/180/200 arasındaki
   fark (16.9 / 14.8 / 19.3 N) **temas saçılmasının içinde** — tek düze
   değil. Göz seçimi gerilmeye değil, pay + emek dengesine dayandırıldı.

## 6. Payı geri kazanmanın ucuz yolu: BAĞLANTI ŞEKLİ
Ölçülen tepe yük 14.8 N. Kapasite, mesh ipinin çevre halatına nasıl
bağlandığına bağlı:
* **düğümle** → 35.3 N → pay **2.4×**
* **sararak (lacing)** → ~64 N → pay **4.3×**

Düğüm atmadan, halatın etrafına sararak bağla. Bedava pay.

## 7. Kopmanın sonucu — kare gözün tek zayıf yanı
İpler sürekli olduğu için bir ip koparsa **2 m boyunca** hat gider ve yerel
açıklık `2×göz = 360 mm` olur; pervane (Ø230) o delikten geçebilir.
Altıgen kafeste tek kenar (8 cm) kaybı bu kadar önemli değildi.
Bu yüzden (6)'daki lacing şartı **tavsiye değil, gereklilik**.

---

## 8. Kesinleşen v5 ağ tanımı
```
dış hat      : altıgen, köşe yarıçapı 1.30 m (Ø2.60 m)
göz          : KARE 180 mm
mesh ipi     : Dyneema SK78 ÖRGÜ Ø0.165 mm, ~50 m, ~28 sürekli ip
çevre halatı : PE örgü Ø0.285 mm, 7.8 m (altıgenin 6 kenarı)
bağ          : ~179 (120 göz kesişimi + 59 çevre bağlantısı), ~3 saat
bilye        : Ø12.7 kurşun × 6, halatın 6 köşesinde
kütle        : 1.17 g ağ + 73 g bilye
açılma       : R = 1.129 m (gereken 0.859 m, %31 pay)
pencere      : 3.58 – 6.62 m
hazne dolgusu: %5.9
```

## 9. Sıradaki iş
1. **YER TESTİ** — dolanma/açılma. Modelin cevaplayamadığı tek şey.
2. Mesh ipi–halat bağlantısında lacing'i doğrula (çekme testi).
3. Pervane kenarında kesme testi (bkz. `IP_CAPI_KARAR.md` §1c).

---

## 10. GÜNCELLEME — statik göz kriteri ÇOK KATI çıktı (Gazebo ölçümü)

Göz sınırını "pervane diskinin içinde en az bir ip bulunsun" diye *statik*
koymuştum: `göz < 230 mm`. Bu, ağın tek bir anlık görüntüsü için doğru ama
**gerçekte ağ uçağın üzerinden GERİYE SÜPÜRÜLÜYOR** (ölçüldü: ağ merkezi
5.4 m'den 4.78 m'ye geri geliyor). Süpürme sırasında diskten kaç farklı
iplik geçtiğini ölçtüm:

| R_ag | göz | bağ | iplik | T_tepe | pervane: anlık max / **toplam farklı** | hedefte | hedef v |
|---|---|---|---|---|---|---|---|
| 1.3 | 180 | 179 | 57 m | 15.8 N | 5 / **18** | %50 | 0.89 m/s |
| **1.3** | **200** | **142** | **52 m** | **15.3 N** | **12 / 32** | **%54** | **0.86 m/s** |
| 1.3 | 220 | 133 | 48 m | **12.8 N** | 23 / **92** | %51 | 0.80 m/s |
| 1.2 | 200 | 133 | 45 m | 14.7 N | 13 / **32** | %58 | **1.03 m/s** |

**Her göz boyutunda diskten onlarca iplik geçiyor.** "Pervane gözün ortasına
denk gelip hiç ip kesmeyebilir" endişesi gerçekleşmiyor.

Ayrıca kabalaştıkça **iyileşiyor**: göz 220'de hem en düşük tepe gerilme
(12.8 N) hem en çok pervane teması (92 iplik). Yumuşak ağ daha iyi sarıyor.

**Seçim: göz 200 mm.** 220 ölçümde daha iyi çıktı ama statik garanti payı
%4'e iniyor; 200 hem %13 statik pay bırakıyor hem ölçümde 32 iplik veriyor.

### Hazneye sığma — kapandı
CAD'den gerçek hazne: **R 18.55 × L 16 mm = 17.3 cm³** (önce 20.5 demiştim, yanlıştı).

| iplik | katı hacim | %20 yoğunlukta | hazne dolumu |
|---|---|---|---|
| 100 m (eski) | 2.14 cm³ | 10.7 cm³ | %62 |
| **45 m (yeni)** | **0.96 cm³** | **4.8 cm³** | **%33** |

Hazne kapasitesi %20 yoğunlukta **162 m**. Sıkışmaya yakın bile değiliz.
**Sorun hacim değil, DÜZENLİ KATLAMA.** Rastgele tıkılırsa hacim yetse bile
dolanır — bu montaj talimatının meselesi, tasarımın değil.

### Nişan toleransı — küçültmenin gizli maliyeti
Ağın tüm uçağı örtmesi için R_açık ≥ 0.859 m (Talon yarı açıklığı) gerekir.
Fazlası nişan hatası payıdır:

| R_ag | R_açık | tam uçak örtme payı | sadece pervane payı |
|---|---|---|---|
| 1.3 | 1.141 m | **0.28 m** | 1.03 m |
| 1.2 | 1.086 m | 0.23 m | 0.97 m |
| 1.1 | 1.039 m | 0.18 m | 0.92 m |

Ağı küçültmek doğrudan nişan payını yiyor. "Tek ip pervaneye yeter" tezi
kabul edilirse pay ~1 m'ye çıkar, ama o zaman da ağın pervaneyi bulması
nişana bağlı kalır. **R_ag 1.3'te kalındı** — asıl kazanç gözden geldi,
ağı küçültmeye gerek yok.

## 11. KESİNLEŞEN v5 ağ
```
dış hat      : altıgen, köşe yarıçapı 1.30 m (Ø2.60 m)
göz          : KARE 200 mm
mesh ipi     : Dyneema SK78 ÖRGÜ Ø0.165 mm, ~45 m, ~26 sürekli ip
çevre halatı : PE örgü Ø0.285 mm, 7.8 m
bağ          : ~142 (83 göz kesişimi + 59 çevre), ~2.5 saat
bilye        : Ø12.7 kurşun × 6, halatın 6 köşesinde
kütle        : 0.95 g ağ + 73 g bilye
açılma       : R = 1.141 m   |   pencere 3.58 – 6.80 m
hazne dolumu : %33 (kapasite 162 m)
pervane teması: 32 farklı iplik (ölçüm)
tepe gerilme : 15.3 N, kopan 0  (lacing ile pay 4.2x)
```

### ESKİ → YENİ
| | eski (altıgen Ø2.8 göz140) | **yeni (kare Ø2.6 göz200)** |
|---|---|---|
| bağ | 811 | **142**  (−%82) |
| iplik | 100 m | **45 m**  (−%55) |
| el emeği | 13.5 saat | **2.5 saat**  (−%81) |
| hazne dolumu | %62 | **%33** |
| pencere | 3.56 – 6.44 m | **3.58 – 6.80 m** |
| hedefe serilme | %33 | **%54** |
| aktarılan momentum | 0.50 m/s | **0.86 m/s** |

## 12. Yol boyunca yaptığım hatalar
1. Altıgen kafes kurup düğüm sayısını 709 sandım; `params.py` baştan KARE
   göz varsayıyordu, malzeme listesindeki 259 doğruydu.
2. Çevre halatını (F2, listede vardı) modellemedim; onsuz kare ağın köşeleri
   desteksiz kalıp açılamıyordu — yanlış sonuca götürdü.
3. Hazne hacmini Python'daki eski `D_hazne`'den aldım (20.5 cm³); CAD'deki
   gerçek değer 17.3 cm³.
4. `PERVANE` sabitini tanımlanmadan önce kullandım; SDF üretimi sessizce
   çöktü, Gazebo 4 koşuyu ESKİ dünya dosyasıyla yaptı ve dördü de aynı
   sayıyı verdi. Üretici hatası artık koşuyu durduruyor.

---

## 13. v5 TAM ATIŞ SİMÜLASYONU (Gazebo) — ve ÖNEMLİ bir düzeltme

Ağ: Ø2.6 m, kare göz 200 mm, 142 düğüm, 269 eleman. Hedef: Talon, seyir trimli.

### Pencere taraması — geometrik pencere YANILTICIYMIŞ
| tetikleme | pervaneden geçen ip | ağın uçağa serilme oranı | aktarılan momentum | ip tepe yükü |
|---|---|---|---|---|
| 3.6 m | 16 | **%78** | **2.08 kg·m/s** | 25.8 N |
| **4.2 m** | **53** | %52 | 1.64 kg·m/s | 19.0 N |
| 5.0 m | 4 | %28 | 0.64 kg·m/s | 14.2 N |
| 5.8 m | 46 | %37 | 0.87 kg·m/s | 5.5 N |
| 6.5 m | 6 | %30 | 0.45 kg·m/s | 10.3 N |
| 7.0 m | 12 | %24 | 0.37 kg·m/s | 5.9 N |

**Serilme ve momentum mesafeyle tutarlı biçimde düşüyor.** Uzakta ağ
yeterince AÇIK ama uçağın üzerinden **değip geçiyor** — 7.0 m'de ağın
sadece %24'ü uçağa değiyor.

> **BU, ÖNCEKİ TAVSİYEMİN TERSİ.** Daha önce "pencerenin uzak yarısından
> ateşle, ip yükü düşük olur" demiştim. O tavsiye Python modelinin
> penceresine dayanıyordu ve o model yalnızca *"ağ yeterince açık mı"*
> diye bakıyor — **yakalayıp yakalamadığına bakmıyor.** Gazebo'nun temas
> simülasyonu farkı gösterdi.
>
> **DÜZELTME: 4.0 – 4.5 m'den ateşle.**

### Tekrarlanabilirlik
Aynı konfigürasyon 3 kez koşuldu:
```
4.2 m -> pervane 49 / 53 / 53 ip, serilme %51 / %51 / %51, T 19.03 N (3/3)
5.0 m -> pervane  4 /  4 ip,      serilme %28 / %28,       T 14.17 N (2/2)
```
Koşular **deterministik**. Yani mesafeler arasındaki saçılma (16/53/4/46/6/12)
gürültü DEĞİL — tetikleme mesafesine gerçek hassasiyet. Pervane teması
mesafeye çok duyarlı; serilme oranı ise düzgün ve güvenilir bir gösterge.

### Nominal koşu (4.2 m)
```
ip tepe yükü      : 19.03 N
kopan eleman      : 0 / 269
%50'yi aşan eleman: 2  (düğümlü 35.3 N kapasiteye göre)
                    0  (lacing ile 64 N kapasiteye göre)   <- LACING ŞART
pervaneden geçen  : 53 farklı iplik
ağın uçağa serilme: %52
aktarılan momentum: 1.64 kg·m/s  (1.8 kg uçakta 0.91 m/s)
```
Görsel: `out/YAKALAMA_v5_3b.png`

### Sonuç
v5 ağ **çalışıyor**: 142 bağ ve 45 m iple, 811 bağlı eski ağdan daha iyi
yakalıyor (serilme %52 vs %33, momentum 1.64 vs 0.50 kg·m/s). Tek şart:
mesh iplerini çevre halatına **sararak** bağlamak ve **4.0–4.5 m'den**
ateşlemek.
