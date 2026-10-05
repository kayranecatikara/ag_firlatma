# v2.5 — Kapsül iki bloğa ayrıldı

## Sorun

Kapsül tek parçaydı ve esnek bandı taşıyan **çapraz pim** kapsülün arka
bloğundan geçiyordu. Bant pimi ileri doğru itiyor, ama pim yarık içinde
hareket ediyor ve **yarığın sonunda duruyor** — yani kapsülün gidebileceği
yolu bant/pim/yarık üçlüsü sınırlıyor. Kapsülün ağzı namlu ağzındaki omza
çarpmak zorunda; ikisi aynı parçada olduğu için ya pim yarığın sonuna
çarpıyor ya kapsül omza, hangisi önce gelirse.

## Çözüm

Kapsül yerel **y = 16.0 mm** düzleminden (arka bloğun üst yüzü) ikiye
bölündü:

| Blok | Ne taşıyor | Hacim | Kütle | Durduran |
|---|---|---|---|---|
| **02a_kapsul_alt** | çapraz pim, tutma kanalı, kurma deliği, hizalama spigotu | 33.75 cm³ | 35.1 g | yarık sonu TPU tamponu |
| **02b_kapsul_ust** | ağ haznesi, boncuk başlığı, 6 × yuva | 45.74 cm³ | 47.6 g | namlu ağzı omzu |

Alt blok üst bloğu **iter**, birbirine bağlı değiller. Alt blok yarık
sonunda durduğunda üst blok **serbest kalır** ve kendi atalet hızıyla
gidip omza çarpar.

### İtme yüzeyi

İtme spigottan değil, alt bloğun **tam halka yüzünden** geçiyor:

```
R_hazne 24.1 .. R_kapsül 31.6  →  594 mm²
PETG 50 MPa  →  29.712 N taşır
```

Gerekli itme kuvveti tam kurmada 391 N. Marj **76×**.

### Hizalama spigotu

Alt bloğun üstünde **cidar kalınlığı 2.5 mm**, yüksekliği **6 mm** bir
boru var; üst bloğun haznesine 0.4 mm boşlukla giriyor. İşi sadece iki
bloğu eş eksende tutmak — yük taşımıyor. Hazneden ~15 cm³ yiyor,
ağ için **~42 cm³** kalıyor (doluluk %26).

### Durdurma enerjisi bölündü

Eskiden tek stop (omuz) her şeyi durduruyordu. Şimdi:

```
v = 17.4 m/s
  alt blok + çapraz pim   50.3 g  →   7.6 J   (yarık sonu TPU tamponu)
  üst blok + ağ + boncuk  81.2 g  →  12.3 J   (namlu omzu, 295 mm²)
```

Omzun yükü ~15 J'den **12.3 J'ye** indi. 2 mm TPU 95A halka
(20 MPa, %60 ezilme) 7.1 J yutuyor; kalan 5.2 J / 14.744 N = **0.35 mm**
ezilme. Eskiden 1.19 mm'ydi.

## Ayrılma mesafesi — ayarlanacak

CAD'de alt bloğu durduran **geometrik** bir engel yok: çapraz pim
y=100.5'e kadar geliyor, omuz halkasının kulakları y=128.83'te başlıyor,
bant o noktada tam olarak serbest boyunda. Yani **alt bloğun nerede
durduğunu yarık sonundaki TPU tamponun kalınlığı belirliyor.**

Şu anki 3 mm tamponla iki blok **birlikte** varıyor — ayrılma olmuyor,
ama darbe yine iki stop arasında **paylaşılıyor** (kazanç bu).

Gerçek ayrılma istiyorsan tamponu kalınlaştır:

| Tampon | Alt blok erken durur | Üst blok serbest yolu | Strok | Enerji |
|---|---|---|---|---|
| 3 mm (şimdiki) | — | 0 mm | 91 mm | %100 |
| 8 mm | 5 mm | 5 mm | 86 mm | %95 |
| 13 mm | 10 mm | 10 mm | 81 mm | %89 |

Bedeli: strok kısalır → λ düşer → enerji düşer. **10 mm ayrılma için
%11 enerji** veriyorsun. İlk testte 3 mm ile başla, iki blok birlikte
gitsin; pim/yarık kırılma belirtisi görürsen tamponu kalınlaştır.
