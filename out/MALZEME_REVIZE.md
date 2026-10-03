# ELDEKİ MALZEMELERLE REVİZE — ölçüm sonuçları

## Aldığın malzemeler vs tasarım

| | tasarım | eldeki | oran |
|---|---|---|---|
| iplik çapı | 0.165 mm | **0.60 mm** | 3.6× |
| iplik kesiti | 0.021 mm² | 0.283 mm² | **13.2×** |
| iplik kütle/m | 0.021 g | 0.27 g | **13.2×** |
| iplik kopma | 64 N | **445 N** | 6.9× |
| bilye | Ø12.7 / 12.16 g | Ø8 / **4 g** | **0.33×** |
| bant dış çap | 15.2 mm | **13 mm** | 0.86× |

> ⚠️ Ø8 kürenin 4 g olması **14921 kg/m³** yoğunluk demek — kurşundan ağır,
> tungstenden hafif. Ya çap ya kütle yaklaşık ölçülmüş olmalı.
> **Hassas tartıp söyle**; balistikte belirleyici olan kütledir.

## Bulgu 1 — ilk denemede ağ HİÇ AÇILMIYOR

| R_ag | göz | ağ | R_tepe | durum |
|---|---|---|---|---|
| 1.30 | 200 | 14.18 g | 0.568 | YETERSİZ |
| 1.20 | 200 | 12.24 g | 0.622 | YETERSİZ |
| 1.00 | 200 | 8.77 g | 0.566 | YETERSİZ |

Gereken 0.859 m. Sebep: bilyeler 3× hafifledi, ağ 13× ağırlaştı →
açma momentumu **46× yetersiz**.

## Bulgu 2 — koni açısı açılmayı kurtarıyor

| α | R_tepe |
|---|---|
| 13° *(tasarım)* | 0.566 |
| 25° | 0.792 |
| **35°** | **0.908** ✅ |
| 45° | 0.980 ✅ |

## Bulgu 3 — AMA 0.60 mm iplik menzili ÖLDÜRÜYOR

Koni açısı açılma sorununu çözüyor, **menzil sorununu çözmüyor**:

| bilye kütlesi | 6 bilye | PENCERE |
|---|---|---|
| 4 g | 24 g | 1.14 – 1.44 m |
| 8 g | 48 g | 1.06 – 1.60 m |
| 12 g | 72 g | 1.04 – 1.70 m |
| **24 g** | **144 g** | **1.02 – 1.80 m** |

**Bilye ne kadar ağırlaşırsa ağırlaşsın pencere 1.8 m'yi geçmiyor.**
0.60 mm iplik, çapıyla orantılı sürükleme yaratıyor (3.6×) ve ağı
frenliyor. Gözü açmak da kurtarmıyor (göz 350 mm'de bile 1.58 m) —
üstelik göz > 230 mm olunca pervane garantisi kalkıyor.

## Bulgu 4 — ÇÖZÜM: karma kullanım

**0.60 mm ipi ÇEVRE HALATI olarak kullan** (7–8 m, orada dayanım lazım
ve uzunluk kısa), **meshi ince iple ör**:

| mesh ipi | bilye | α | R_tepe | PENCERE |
|---|---|---|---|---|
| 0.165 mm | 4 g ×1 | 15° | 0.923 | 3.16 – 4.06 |
| 0.165 mm | **4 g ×2 = 8 g** | **20°** | **1.106** | **2.20 – 5.78** ✅ |
| 0.165 mm | 4 g ×3 = 12 g | 25° | 1.277 | 1.64 – 6.08 |

**Önerilen: yuva başına 2 bilye (toplam 12 adet), α = 20°.**
Pencere 2.20 – 5.78 m — eski tasarımın 3.56 – 6.54'üne yakın, hem de
eldeki bilyelerle.

## KARAR

```
mesh ipi   : 0.165 mm Dyneema örgü  -> SATIN ALINACAK (~130 TL / 100 m)
çevre ipi  : eldeki 0.60 mm          -> 8 m kullan, 82 m artar
bilye      : eldeki Ø8 / 4 g         -> YUVA BAŞINA 2 ADET, 12 adet
koni açısı : 13° -> 20°              -> kapsül yuvaları değişecek
ağ         : Ø2.2 m (R_ag 1.1), kare göz 200 mm
bant       : eldeki Ø13              -> sertlik ÖLÇÜLECEK
PENCERE    : 2.20 – 5.78 m
```

## Bandın sertliğini ölç — tasarım buna bağlı

Eldeki Ø13 lastiğin sertliği bilinmiyor. **50 mm kes, 135 mm'ye ger,
bagaj kantarıyla oku.**

```
Gmod [MPa] = okunan_kuvvet [N] / 473
```

| okursan | Gmod | 4 bant toplam | kurma/bant |
|---|---|---|---|
| 100 N (10 kg) | 0.21 MPa | 568 N | 14.5 kg |
| 200 N (20 kg) | 0.42 MPa | 852 N | 21.7 kg |
| 300 N (31 kg) | 0.63 MPa | 1136 N | 28.9 kg |

Sonucu söyle, çıkış hızını ve pencereyi ona göre yeniden hesaplayayım.

## Hâlâ açık
* Ø8 bilyenin gerçek kütlesi (hassas tartım)
* Ø13 bandın Gmod'u (çekme testi)
* 12 bilye için kapsül yuvaları yeniden çizilecek (2 bilye derinliği)
