# BANT ÖLÇÜMÜ — SONUÇ

Ölçülen (50 mm serbest boylu numune, asma kantar):

| çekiş | boy | λ | okuma | N |
|---|---|---|---|---|
| 20 mm | 70 mm | 1.40 | 5.685 kg | 55.77 |
| 40 mm | 90 mm | 1.80 | 8.350 kg | 81.91 |
| 60 mm | 110 mm | 2.20 | 11.070 kg | 108.60 |

## Modele oturdu

`F = G·A₀·(λ − 1/λ²)` ile **G·A₀ = 54.7 N**.
Son iki noktayı **%0.4 hatayla** veriyor (ilk nokta düşük uzamada modelin
zayıf olduğu bölge, %12.7 sapıyor — normal).

İç çapı ölçmedik ama gerek de yok: kuvveti belirleyen `G·A₀` çarpımı ve
onu doğrudan ölçtük. (Ø4 varsayarsak Gmod = **0.413 MPa**; varsayımımız
0.45 idi — tutmuş.)

## KESİM BOYU

Montaj geometrisi (CAD'den, v2.1):

| | |
|---|---|
| Ağız ankraj pimi | y = 138.83 |
| Çapraz pim ön yüzü — dinlenmede | y = 104.5 |
| Çapraz pim ön yüzü — kurulu | y = 13.5 |
| **Düz lastik boyu** | **34.3 mm → 125.3 mm** |
| **Uzama oranı λ** | **3.65** |

| Kesim payı | |
|---|---|
| Düz çalışma boyu | 34.3 mm |
| Ön: pimden ağız yüzüne 6 + 30 mm kuyruk | 36.0 mm |
| Arka: çapraz pim sarımı 12.6 + 30 mm katlama | 42.6 mm |
| **TOPLAM** | **≈ 113 → 115 mm** |

### **2 adet × 115 mm kes (toplam 230 mm)**

## KURMA KUVVETİ

| | |
|---|---|
| Bant başına (λ=3.65) | 196 N = **19.9 kg** |
| **İki bant** | **391 N = 40 kg** |

**Uyarı:** ölçüm λ ≤ 2.2'ye kadar; λ = 3.65 bir **ekstrapolasyon**.
Doğal kauçuk yüksek uzamada sertleşir, gerçek kuvvet **%10–25 fazla**
çıkabilir → beklenen aralık **40–50 kg**.

Kurarken kantarı araya koy ve tepe değeri oku. 50 kg'ı belirgin aşarsa
dur ve söyle — modelde bir şey eksik demektir.

## BEKLENEN PERFORMANS

| | ölçülen (0.41 MPa) | %20 sertleşirse |
|---|---|---|
| Kurma kuvveti | 391 N (40 kg) | 469 N (48 kg) |
| Çıkış hızı | 21.0 m/s | 23.1 m/s |
| Ağ çapı | 1.92 m | 1.95 m |
| Açılma payı | **1.12×** | 1.14× |
| **Mesafe** | **0.69 – 0.93 m** | 0.78 – 0.97 m |

Gerekli açılma yarıçapı 0.859 m (Talon yarı kanat açıklığı) — **sağlanıyor.**

## TEST MERDİVENİ HÂLÂ GEÇERLİ

40 kg'lık tam kurma, duracak kütleye 13.5 J yüklüyor. Durdurma takozu
304 mm² / 15.200 N ve TPU ped 10.9 J yutuyor — hesapta tutuyor, ama
**hiç gerçek atış verisi yok.**

| çekiş | 1 bant | 2 bant |
|---|---|---|
| 40 mm | ~9 kg | ~18 kg |
| 60 mm | ~13 kg | ~26 kg |
| **91 mm (tam)** | ~20 kg | **~40 kg** |

İlk atışı **1 bant + 40 mm çekiş** ile yap, kademeli çık, her atıştan
sonra takoza ve çapraz pime bak.
