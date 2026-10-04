# VERSİYONLAR

Her klasör, tasarımın o andaki halini **birebir yeniden üretecek** şekilde
dondurulmuştur: konfig dosyaları, CAD ölçü/hacimleri, basılacak STL+STEP'ler
ve ilgili dokümanlar.

> ⚠️ **Depo kökündeki `baski/` ve `AG_FIRLATICI_STL.zip` her zaman EN SON
> tasarımı taşır.** Belirli bir versiyonu basacaksan o versiyonun kendi
> `baski/` klasörünü kullan.

| Versiyon | Namlu | Strok | Bant L0 | Koni | Kapsül | Bant | Boncuk | Mesafe\* | Durum |
|---|---|---|---|---|---|---|---|---|---|
| [v1](v1/SURUM.md) | 149.8 mm | 91 mm | 30.3 mm | 40° | 45 mm | 2 | 6 | 0.80–0.98 m | **test ediliyor** |
| [v2](v2/SURUM.md) | 255.2 mm | 170 mm | 56.7 mm | 35° | 70 mm | 2 | 6 | 1.13–1.34 m | tasarlandı, basılmadı |

\* Gmod 0.45 MPa varsayımıyla. Bant sertliği **hâlâ ölçülmedi** — her versiyonun
`dok/` klasöründeki tabloda 0.25–0.65 MPa aralığı var.

Ortak: ağ Ø2.2 m · kare göz 220 mm · Dyneema Ø0.60 mm · 6 × Ø9 mm kurşun
boncuk (24 g) · namlu iç çap Ø43.4 mm · bant Ø13/iç Ø4 · bant ankrajı
Ø14 delik + delen pim.

## v1 → v2 nede değişti

v2'nin tek fikri **namluyu ve bandı uzatmak**. λ sabit tutulunca kurma kuvveti
strok'tan bağımsız kalıyor (ikisi de 426 N), ama depolanan enerji bant hacmiyle
2.75× büyüyor. Enerjinin menzile çevrilme verimi düşük (`mesafe ∝ strok^0.285`);
asıl kazanç, fazla enerjinin **daha düşük koni açısı** kullanmayı mümkün kılması
(v1'de 30° ağı açamıyordu). Ayrıntı ve geometrik kısıtlar: `v2/dok/V2.md`.

## Yeni versiyon dondurma

```
python3 versiyon_kaydet.py v3 "kısa açıklama"
```

CAD konfigini değiştirip `freecadcmd cad/lastik_montaj_v4.py`,
`cad/baski_parcalari.py` ve `cad/kontrol_ankraj.py` koşturduktan **sonra**
çalıştır.
