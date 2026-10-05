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
| [v1.3](v1.3/SURUM.md) | 149.8 mm | 91 mm | 30.3 mm | 40° | 45 mm | 12.0 | omuz, 282 mm² | 0.78–0.97 m | ağ çıkamıyordu |
| [v1.4](v1.4/SURUM.md) | 149.8 mm | 91 mm | 30.3 mm | 40° | 45 mm | 12.0 | omuz, 282 mm² | 0.73–0.95 m | ağ namluda |
| [v1.5](v1.5/SURUM.md) | 149.8 mm | 91 mm | 30.3 mm | 40° | 45 mm | 12.0 / 13.4 | omuz, 282 mm² | 0.73–0.97 m | ağ geçişi Ø10.8 — yetersiz |
| [v2.0](v2.0/SURUM.md) | 149.8 mm | 91 mm | 30.3 mm | 40° | 45 mm | 18.2 | omuz, 300 mm² | 0.62–0.90 m | merkez hâlâ dar |
| [v2.1](v2.1/SURUM.md) | 149.8 mm | 91 mm | 30.3 mm | 40° | 45 mm | **22.0** | takoz, 304 mm² | 0.72–0.94 m | merkez ok, takoz bandı engelledi |
| [v2.2](v2.2/SURUM.md) | 149.8 mm | 91 mm | **34.3 mm** | 40° | 45 mm | **23.0** | omuz, 295 mm² | 0.50–0.84 m | namlu Ø55→**Ø64** |
| [v2.3](v2.3/SURUM.md) | 149.8 mm | 91 mm | 34.3 mm | 40° | 45 mm | 23.0 | omuz, 295 mm² | 0.50–0.84 m | takoz kaldırıldı |
| [v2.4](v2.4/SURUM.md) | 149.8 mm | 91 mm | 34.3 mm | 40° | 45 mm | 23.0 | omuz, 295 mm² | 0.50–0.84 m | yuva derinliği 9.0, başlık 11.0 |
| [**v2.5**](v2.5/SURUM.md) | 149.8 mm | 91 mm | 34.3 mm | 40° | 45 mm | 23.0 | **alt: tampon 7.6 J<br>üst: omuz 12.3 J** | 0.50–0.84 m | **güncel — kapsül 2 blok** |
| [v2](v2/SURUM.md) | 255.2 mm | 170 mm | 56.7 mm | 35° | 70 mm | 15.5 | çapraz pim, 96 mm² | 1.13–1.34 m | beklemede |

\* v2.2'den itibaren **ölçülmüş** bant ile (G·A0 = 54.7 N, dijital kantar,
50 mm numune +20/+40/+60 mm → 5.685/8.350/11.070 kg). Öncesi Gmod 0.45 MPa
varsayımı. 2 bant, L0 34.3 mm, λ 3.65 → **391 N (40 kg) kurma**, 17.4 m/s.

Ortak: ağ Ø2.2 m · kare göz 220 mm · Dyneema Ø0.60 mm · 6 × **Ø8.80 mm**
kurşun boncuk (24 g, kumpasla ölçüldü) · namlu iç çap **Ø64.0** (v2.2'den önce Ø55.0, v2.0'dan önce Ø43.4) · bant **Ø13.59** · bant ankrajı
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

**v1.3 → v1.4 — ağ namluya taşındı.** 6 boncuk borusu 40° eğimli olduğu için
ağız düzleminde elips kesit veriyor ve R12 bölüm dairesinde çevrenin 72/75.4
mm'sini kaplıyordu: merkezde ağa **55 mm² (Ø8.3)** kalıyordu, 39 m ip oradan
geçmez. Ayar hatası değil, mimari çıkmaz — omuz ≥250 mm² için R_pitch ≤ 12.26
ve orada bile merkez 62 mm². **Durdurma omzu ile merkezi ağ çıkışı bir arada
olamaz.** Çözüm: ağ kapsülün değil, namlunun içinde, kapsülün önünde duruyor;
kapsül piston. Ağ hacmi 22.1 → **134.6 cm³**, doluluk %75 → **%8**. Başlık
masifleşti (kapsül 43.8 → 51.4 g, mesafe −0.02 m). Ayrıntı: `v1.4/dok/V1_4_AG_YERI.md`.

**v1.4 → v1.5 — iki kapsül.** Ağı içeride taşıyan varyant (`02b_kapsul_hazneli`)
da üretildi; boncuk düzeltmeleri ikisinde de aynı. Ağ çıkışını büyütmek için
boncuk bölüm dairesi cidarın izin verdiği en dışa itildi (R12.0 → 13.4):
merkezi bağlı boş alan 55 → **92 mm² (Ø10.8)**, 1.7×. Namlu başlığı
değişmiyor (boncuk dış kenarı 17.80 < koni 19.08), yani **aynı namlu ikisiyle
de çalışır**. 02b daha hafif (44.3 vs 51.4 g) ve biraz daha uzak; tek
belirsizlik 39 m ipin Ø10.8'den geçip geçmeyeceği — test edilecek.

**v1.5 → v2.0 — istenen mimari kuruldu, namlu büyüdü.** Ağ haznede, boncuklar
kapsülün ağzında; kapsül omza çarpınca önce boncuklar fırlıyor, ağı
arkalarından çekiyorlar. Ø43.4'te bu mümkün değildi: 6 yuva ağız çevresinde
74.4 mm istiyor ve 40° eğimden dolayı elips kesit veriyor, merkezde en fazla
Ø10.8 kalıyordu. **Namlu Ø43.4 → Ø55.0** ile ağ geçişi **Ø18.6 (271 mm²)**,
hazne doluluğu %51 → **%31**. Yuvalar da genişletildi (boşluk 0.4 → 0.8 mm,
dudak sıkması 0.4 → 0.2 mm — baskıda boncuklar zor giriyordu).
Bedeli: kapsül 44 → 71 g, baskı 214 → 281 g, menzil ~%10 kısa.
Ayrıntı: `v2.0/dok/V2_0.md`.

**v2.0 → v2.1 — boncuklar kapsülün kenarına alındı.** v2.0'da yuvalar R18.2'de
olduğu için 40° eğimden doğan elips kesit ağzın üstünü yiyordu; merkezde
271 mm² kalıyordu. Yuvalar **R22.0**'a, yani kapsül cidarına kadar itildi:
yuva dış kenarı 30.1 > cidar 27.1 olduğu için cidarı delip **en fazla 3.25 mm
genişliğinde radyal yarık** açıyor — boncuk Ø8.80 oradan **çıkamaz**, plastik
onu sarıyor, namlu deliği dışarıdan kapatıyor. Merkez **556 mm² (Ø26.6)**,
v2.0'ın 2.1 katı; hazne doluluğu %21. Koni R29.1'den başlamak zorunda olduğu
için omuz kalmadı; kapsülü **çapraz pim + namlu dışındaki durdurma takozu**
durduruyor (304 mm² / 15.200 N, TPU ped 10.9 J).

**v2.1 → v2.2 — namlu Ø64, omuz geri geldi.** v2.1'de kapsülü namlu
*dışındaki* takoz durduruyordu; takoz z 37–50 arasında, esnek bant ise
z 42.6–49.4'te — **takoz bandı engelliyordu**. Omza dönmek için koniye yer
gerekti: namlu **Ø55 → Ø64**. Boncuk çemberi R22 → R23, omuz 295 mm²
(14.744 N) geri geldi. Bant da **ölçüldü** (G·A0 = 54.7 N): kurma 391 N,
çıkış 17.4 m/s, marj 1.08×.

**v2.2 → v2.3 — takoz komple kaldırıldı.** Artık durdurmayı omuz yapıyor,
takozun işi kalmadı ve bandın yolunda duruyordu. `kontrol_bant_yolu.py`
eklendi: bant yolunu 121 nokta × 9 kesit köşesinde tarayıp namluyla
çakışma arıyor.

**v2.3 → v2.4 — boncuklar daha derine.** Yuva derinliği 9.0 mm, başlık
kalınlığı 11.0 mm: boncuk eğimli yuvada **7.5 mm** yol alıyor (önce 5.5),
yani 40° çıkış açısını tam kazanarak ayrılıyor.

**v2.4 → v2.5 — kapsül iki bloğa ayrıldı.** Çapraz pim arka bloktan
geçiyor ve yarık sonunda duruyor; kapsülün ağzı ise namlu omzuna çarpmak
zorunda. Tek parçada bu ikisi çelişiyordu. Kapsül yerel y=16'dan bölündü:
**alt blok** (pim + kanal + kurma deliği, 35.1 g) **üst bloğu**
(hazne + boncuk başlığı, 47.6 g) 594 mm² halka yüzünden itiyor; alt blok
yarık sonunda durunca üst blok serbest kalıp omza çarpıyor. Durdurma
enerjisi tek stop yerine ikiye bölündü (7.6 J + 12.3 J), omzun TPU ezilmesi
1.19 → **0.35 mm**. Ayrıntı: `dok/V2_5_IKI_BLOK.md`.

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
