# VERSİYONLAR

Her klasör, tasarımın o andaki halini **birebir yeniden üretecek** şekilde
dondurulmuştur: konfig dosyaları, CAD ölçü/hacimleri, basılacak STL+STEP'ler
ve ilgili dokümanlar.

> ⚠️ **Depo kökündeki `baski/` ve `AG_FIRLATICI_STL.zip` her zaman EN SON
> tasarımı taşır.** Belirli bir versiyonu basacaksan o versiyonun kendi
> `baski/` klasörünü kullan.

| Versiyon | Namlu | Strok | Bant L0 | Koni | Kapsül | R_pitch | Kapsülü durduran | Mesafe\* | Durum |
|---|---|---|---|---|---|---|---|---|---|
| [v1](v1/SURUM.md) | 149.8 mm | 91 mm | 30.3 mm | 40° | 45 mm | 15.5 | çapraz pim, 96 mm² | 0.80–0.98 m | ilk test |
| [v1.1](v1.1/SURUM.md) | 149.8 mm | 91 mm | 30.3 mm | 40° | 45 mm | **12.0** | **omuz, 303 mm²** | 0.79–0.97 m | basıldı |
| [v1.2](v1.2/SURUM.md) | 149.8 mm | 91 mm | 30.3 mm | 40° | 45 mm | 12.0 | omuz, 270 mm² | 0.79–0.97 m | basıldı |
| [**v1.3**](v1.3/SURUM.md) | 149.8 mm | 91 mm | 30.3 mm | 40° | 45 mm | 12.0 | omuz, 282 mm² | 0.78–0.97 m | **güncel** |
| [v2](v2/SURUM.md) | 255.2 mm | 170 mm | 56.7 mm | 35° | 70 mm | 15.5 | çapraz pim, 96 mm² | 1.13–1.34 m | beklemede |

\* Gmod 0.45 MPa varsayımıyla, 2 bant. Bant sertliği **hâlâ ölçülmedi** —
her versiyonun `dok/` klasöründeki tabloda 0.25–0.65 MPa aralığı var.

Ortak: ağ Ø2.2 m · kare göz 220 mm · Dyneema Ø0.60 mm · 6 × **Ø8.80 mm**
kurşun boncuk (24 g, kumpasla ölçüldü) · namlu iç çap Ø43.4 mm · bant **Ø13.59** · bant ankrajı
Ø14 delik + delen pim.

## Neler değişti

**v1 → v1.1 — durdurma omuzu.** Kapsül namludan çıkmıyor, namlu içinde durması
gerekiyor: 47 g'ı 23 m/s'den durdurmak **12.8 J** demek. v1'de bunu sadece
Ø8 çapraz pimin yarık ucuna çarpması karşılıyordu (96 mm², 4.800 N) — tam
gerdirilirse yarık ucu kırılırdı. Namlu ağzına içe doğru omuz kondu; ama bu
ancak **boncuk çemberi 15.5 → 12.0 mm'ye çekilince** anlamlı oluyor (omuza yer
açılıyor): 303 mm², 15.174 N, eskisinin 3.2 katı. Menzile etkisi yok (1–2 cm).
Ayrıntı: `v1.1/dok/V1_1_OMUZ.md`.

**v1.1 → v1.2 — ilk baskıdan gelen iki düzeltme.** Kapsül namluda takılıyordu:
boşluk 0.30 → **0.80 mm** (yan başına 0.40; FDM'de Ø43 delik için 0.15 çok sıktı).
Bant ankrajındaki ön yüz oluğu kulağı zayıflatıyordu ve pim hiçbir yere
kenetlenmiyordu: yerine kulağın bir yan duvarından girip bandı delen ve
**karşı duvardaki deliğe oturan Ø4 enine pim** kondu. Ayrıntı: `v1.2/dok/V1_2.md`.

**v1.2 → v1.3 — ölçümler + kapsül içi.** Boncuk kumpasla **Ø8.80 mm / 4 g**,
bant **Ø13.59 mm** ölçüldü (eski varsayımlar Ø9.0 ve Ø13.0 idi). Kapsülde
üç sorun düzeltildi: ağ çıkış konisi **boncuk yuvalarının tabanını yiyordu**
(boncuklar hazneye düşüyordu) → her yuvanın etrafına boru füzelenip tabanı
kapatıldı, sadece Ø3 ip deliği kaldı; yuva ağzına **tutma dudağı** (Ø8.40 <
boncuk Ø8.80) eklendi; hazne→başlık geçişi **koni** yapıldı ve kapsül
**ağız yukarı** basılacak şekilde çevrildi — iç destek ve basamak kalmadı.
Bant ölçüm yöntemi: `v1.3/dok/BANT_OLCUMU.md`.

**v1 → v2 — uzun namlu + uzun bant.** λ sabit tutulunca kurma kuvveti strok'tan
bağımsız kalıyor (ikisi de 426 N), ama depolanan enerji bant hacmiyle 2.75×
büyüyor. Enerjinin menzile çevrilme verimi düşük (`mesafe ∝ strok^0.285`);
asıl kazanç, fazla enerjinin **daha düşük koni açısı** kullanmayı mümkün kılması
(v1'de 30° ağı açamıyordu). Ayrıntı: `v2/dok/V2.md`.

> v2 henüz **durdurma omuzunu almadı**. v1.1 testi iyi giderse v2'ye de
> uygulanmalı — v2'nin durdurma enerjisi 27.5 J, yani sorun daha büyük.

## Yeni versiyon dondurma

```
python3 versiyon_kaydet.py v3 "kısa açıklama"
```

CAD konfigini değiştirip şunları koşturduktan **sonra** çalıştır:

```
freecadcmd cad/lastik_montaj_v4.py     # katıları üret
freecadcmd cad/kontrol_omuz.py         # omuz + boncuk/koni açıklığı
freecadcmd cad/kontrol_ankraj.py       # bant ankrajı + koni çakışması
freecadcmd cad/baski_parcalari.py      # baski/ STL+STEP
freecadcmd cad/torna_parcasi.py        # çapraz pim (basılmaz)
python3 cad/baski_md_guncelle.py       # baskı ayarları tablosu
python3 malzeme_listesi.py             # BOM
```

## Konfig dosyaları

| Dosya | Ne |
|---|---|
| `cad_v4_konfig.json` | CAD giriş parametreleri (türetilmişler hariç) |
| `cad_v4_olcu.json` | CAD'in yazdığı **tam** ölçü dökümü (türetilmişler dahil) |
| `cad_v4_hacim.json` | her parçanın hacmi ve sınır kutusu |
| `out_v4_konfig.json` | simülasyon konfigi (ağ, boncuk, bant sayısı) |
