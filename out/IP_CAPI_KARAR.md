# İPLİK İNCELTME — KARAR

**Soru:** İpi inceltip menzili uzatalım; pervanenin kesmesine dayanırsa.

**Cevap: İNCELTME. Ama sınırı koyan, beklediğimiz yer değil.**

---

## 1. "Pervane ipi keser mi?" — ÜÇ ayrı mekanizma, çapa bağımlılıkları FARKLI

### (a) Kanadın serbest uçan ipe çarpması — ÇAPTAN BAĞIMSIZ
Enine darbede ip bir örse (anvil) dayalı değildir; sadece hızlanıp savrulur.
Smith enine darbe teorisi: kritik hız yalnızca malzemeye bağlıdır.
```
c   = sqrt(E/rho) = 9632 m/s          (Dyneema SK78)
e_b = 3.33 %
V_c = 1022 m/s
```
Pervane ucu (Ø230 mm): 7000 rpm → 84 m/s, 11000 rpm → 133 m/s.
**8× pay. Bu mekanizma inceltmeyi sınırlamıyor.** (Balistik liflerde tek-lif
V50'sinin çaptan bağımsız olmasının sebebi budur.)

### (b) Kenara sarılınca bükülme — ip ÖRGÜ olmak ZORUNDA
Bükülme gerinimini belirleyen **demetin çapı değil, tek filamentin çapı**dır:
| ip tipi | bükülen çap | ε (r_e=0.35 mm) | durum |
|---|---|---|---|
| monofilament 0.165 mm | 165 µm | **%19.1** | **kırılır** |
| monofilament 0.120 mm | 120 µm | %14.6 | kırılır |
| örgü, filament 20 µm | 20 µm | %2.8 | dayanır |
| örgü, filament 15 µm | 15 µm | %2.1 | dayanır |

Dyneema kopma gerinimi %3.33. **Monofilament ip, hangi çapta olursa olsun,
pervane kenarına ilk sarılışta kırılır.** Örgü (braided multifilament) şarttır
— ve inceltmek filament çapını değiştirmediği için bu mekanizma inceltmeden
etkilenmez. (Malzeme listesi F1 zaten "PE örgü balık ipi" diyor; gerekçesi
şimdi kayıtlı.)

### (c) Kenar üzerinde kesme basıncı — İNCELTMEK ZARARLI (∝1/d)
İp sarılıp gerilince kanat kenarı örs görevi görür: `p = T/(r_e·d)`.
0.165 → 0.120 mm geçişi basıncı **%37 artırır**.

> **DÜRÜSTLÜK NOTU:** Bu mekanizmanın *eğilimi* (∝1/d) sağlam, *mutlak eşiği*
> DEĞİL. Kullanılan "enine dayanım ~100 MPa" lif enine basma verisidir; gerçek
> kesilme kriteri enine kayma ve lif yassılaşmasını içerir, model bunu
> yakalamıyor. **Tezgâh testi gerekir:** ipi pervane kanadına sar, ~15 N ger,
> motoru çalıştır, kesiyor mu bak. Model çapları sıralayabilir, eşiği söyleyemez.

---

## 2. ASIL SINIR: çekme + DÜĞÜM, ve ince ağ kendini DAHA ÇOK geriyor

Gazebo yakalama koşuları (gerçek altıgen örgü, 709 düğüm), **tepe iplik
gerilmesi [N]**:

| d [mm] | 4.50 m | 4.65 m | 4.80 m | **en kötü** | ortalama |
|---|---|---|---|---|---|
| 0.165 | 15.08 | 9.92 | 8.79 | **15.08** | 11.3 |
| 0.140 | 17.17 | 16.97 | 9.17 | **17.17** | 14.4 |
| 0.120 | — | 13.10 | — | ≥13.10 | — |

İki bulgu:
1. **İnce ağ yumuşaktır → uçağa daha çok serilir (%58 → %69) → daha çok takılır
   → kendini daha çok gerer.** Yani inceltmenin maliyeti çift taraflı: dayanım
   d² ile düşerken yük de artıyor.
2. **Tetikleme mesafesinin etkisi çaptan BÜYÜK.** 4.80 → 4.50 m geçişi yükü
   8.8 → 15.1 N'a çıkarıyor (+%72); çap etkisi ortalamada +%27.

### Düğüm verimi — gözden kaçan asıl faktör
Altıgen ağın her düğümünde bağ var; Dyneema düğümde dayanımının ~%45'ini
kaybeder. **Gerçek dayanım lif dayanımı değil, düğüm dayanımıdır.**

| d [mm] | lif | düğümlü (%55) | düğümsüz (%90) | en kötü yük | pay (düğümlü) | pay (düğümsüz) |
|---|---|---|---|---|---|---|
| **0.165** | 64.1 N | 35.3 N | 57.7 N | 15.1 N | **2.3×** | **3.8×** |
| 0.140 | 46.2 N | 25.4 N | 41.6 N | 17.2 N | **1.5×** | 2.4× |
| 0.120 | 33.9 N | 18.7 N | 30.5 N | ≥13.1 N | ≤1.4× | ≤2.3× |

---

## 2b. DÜZELTME — "2.3× pay" yanıltıcıydı; elle düğümlü Dyneema FAZLASIYLA yeterli

İlk değerlendirmede *tepe gerilmeyi* ağın dayanımıyla kıyasladım. Yanlış
çerçeve: tepe gerilme **1029 elemanın en yüklü TEKİNİN** değeridir. Ağın
kaderini kaç elemanın zorlandığı belirler. Ölçüm:

| tetikleme | tepe gerilme | >%50 (17.7 N) | >%75 (26.5 N) | >%100 (35.3 N) |
|---|---|---|---|---|
| 4.50 m | 14.6 N | **0** / 1029 | 0 | 0 |
| 4.65 m | 7.9 N | **0** / 1029 | 0 | 0 |

**Tek bir eleman bile düğümlü kopma yükünün yarısına ulaşmıyor.** En yüklü
eleman kapasitesinin %41'inde. Üstelik hekzagonal ağ yüksek yedeklidir:
bir eleman kopsa yük 1028 elemana dağılır, ağ işlevini sürdürür.

### Düğümsüz ağ tavsiyesi GERİ ÇEKİLDİ
Tedarik edilebilirliği hesaba katmamıştım. Piyasadaki düğümsüz raşel file
0.3–0.5 mm iplikle gelir:

| seçenek | ağ | R_tepe | pencere | dayanım | pay |
|---|---|---|---|---|---|
| **Dyneema 0.165 elle düğümlü** | 1.68 g | 1.139 m | **3.56 – 6.22 m** | 35.3 N | 2.3× |
| Dyneema 0.165 düğümsüz | 1.68 g | 1.139 m | 3.56 – 6.22 m | 57.7 N | 3.8× |
| Naylon 0.30 düğümsüz raşel | 6.54 g | 1.018 m | 3.70 – 5.16 m | 50.9 N | **1.7×** |
| Naylon 0.50 düğümsüz raşel | 18.16 g | **0.855 m** | **YOK** | 141.4 N | — |

Kalın ipin menzilden götürdüğü, düğümsüzün dayanımdan kazandırdığından
büyük. 0.50 mm'de ağ 0.855 m'ye açılıyor — Talon'un yarı açıklığı 0.859 m,
**hiç yakalayamıyor**. Dyneema düğümsüz ağ ideal ama 0.165 mm'de tek parça
özel imalat; pratikte temin edilemez.

**Sonuç: elle düğümlenmiş Dyneema 0.165 mm, temin edilebilir seçenekler
içinde açık ara en iyisi ve payı fazlasıyla yeterli.**

### Düğüm neden Dyneema'da bu kadar düşürür (ama sorun değil)
| malzeme | kopma gerinimi | düğüm verimi |
|---|---|---|
| Dyneema SK78 | %3.3 | %50–60 |
| Kevlar 29 | %4.1 | %55–65 |
| Polyester | %9.2 | %60–70 |
| Naylon 66 | %26.7 | %60–80 |

Düğümün içinde demetin **dış filamentleri iç filamentlerden daha uzun yol
kateder** → önce onlar gerilir, önce onlar kopar, zincirleme. Naylon %27
uzayarak bu farkı eşitler; Dyneema %3.3 uzar, **eşitleyemez**. Ayrıca
Dyneema'nın enine dayanımı eksenelin %3'üdür (nip ezilmesi) ve kaygandır
(gerilme yığılması). Denizcilikte Dyneema halatın düğümlenmeyip
**eklenmesinin** (splice, %90–95) sebebi budur.

---

## 3. KARAR

**1) Çap 0.165 mm'de KALSIN.** 0.140'a inince hem dayanım düşüyor (d²) hem
   yük artıyor (yumuşak ağ daha çok serilip daha çok takılıyor). Kazanç ise
   sadece +0.38 m pencere (6.22 → 6.60 m), ki pencere istenen 5–6 m'yi zaten
   0.6 m payla kapsıyor.

**2) ELLE DÜĞÜMLENMİŞ Dyneema ile devam.** Düğümsüz ağ gerekmiyor (hiçbir
   eleman kopma yükünün yarısına ulaşmıyor) ve zaten temin edilemiyor.
   Düğüm: **çift sheet bend** (Dyneema kaygandır), sıkıca çekilsin.

**3) Tetiklemeyi pencerenin UZAK yarısından yap.** 4.80 m, 4.50 m yerine:
   tepe iplik yükü neredeyse yarıya iniyor (8.8 vs 15.1 N) **ve** ağ daha açık
   ulaşıyor. Bedava pay.

**4) İp ÖRGÜ olacak** (monofilament değil) — gerekçesi §1(b).

Menzil hâlâ isteniyorsa kaldıraç ip değil: namlu çıkış hızı (bant/strok —
ama namlu 180 mm ile sınırlı) veya daha ağır bilye. İkisi de yakalama payına
dokunmuyor.

---

## 4. Bu analizin zayıf noktaları
* Her hücrede **tek koşu** (n=1). Temas kaotik; tetikleme mesafesine bağlı
  ±%30, aynı konfigürasyonda tekrar koşuda ±%20 saçılma ölçüldü.
* **Düğüm verimi %55 bir tahmindir** (UHMWPE literatür aralığı %50–60). Ama
  artık belirleyici değil: %50 alsak bile hiçbir eleman kapasitenin yarısına
  ulaşmıyor. Yine de gerçek düğümlü numuneyle çekme testi yapılması iyi olur.
* Malzeme listesi **düğüm sayısını 259 diyordu, gerçek 709** — düzeltildi
  (~12 saat el emeği, 150 m makara).
* **Kenar kesme eşiği çözülmedi** — tezgâh testi şart (§1c).
* Pervane dönüşü modellenmedi; Gazebo'da pervane sabit disk. Dönen pervanenin
  ipi sarması, yani asıl kilitleme mekanizması, rijit-cisim + LCP ile
  çözülemez (ip/kumaş problemi).
