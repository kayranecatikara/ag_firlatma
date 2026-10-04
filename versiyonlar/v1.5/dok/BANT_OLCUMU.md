# BANT KUVVETİNİ KANTARLA ÖLÇME

Aldığın asma kantarla bandın gerçek kuvvetini ölçeceğiz. Bu ölçüm,
tasarımın **en büyük bilinmeyenini** kapatıyor: şu ana kadarki bütün
hız/menzil sayıları 0.45 MPa *varsayımına* dayanıyor.

---

## NEDEN BU ÖLÇÜM YETİYOR

Kauçukta kuvvet, **uzama oranına (λ) ve kesite** bağlıdır — boya değil.
Yani 50 mm'lik bir parçayı 4 katına çekerken okuduğun kuvvet,
30.3 mm'lik gerçek bandı 4 katına çekerkenki kuvvetin **aynısıdır.**

Bu yüzden iç çapı bilmeme bile gerek yok: kuvveti doğrudan okuyoruz.

---

## HAZIRLIK

- Banttan **70 mm** kes (50 mm ölçü + uçlarda tutuş payı)
- Üzerine, tam **50 mm** arayla iki işaret koy (keçeli kalem)
- Her iki uca, bandı **delerek** birer Ø4 pim geçir (montajdaki yöntemin aynısı)
- Alt pimi sağlam bir yere bağla (kapı kolu, mengene, duvar kancası)
- Üst pime kantarın kancasını tak
- Yanına metre/cetvel koy — işaretler arası mesafeyi okuyacaksın

**ÖN ÇALIŞTIRMA (atlamak ölçümü %20–30 yanıltır):** ölçmeden önce bandı
**3–5 kez** λ≈4'e kadar çekip bırak. Yeni kauçuk ilk çekişlerde daha sert
davranır (Mullins etkisi); bu turlardan sonra kararlı hale gelir.

---

## ÖLÇÜM

Üç noktada oku. Her çekişte: işaretler hedef mesafeye gelsin, **5 saniye
bekle**, sonra oku (kauçuk gevşer, beklemeden okursan yüksek çıkar).

| # | işaretler arası | λ | beklenen (0.45 MPa'da) |
|---|---|---|---|
| 1 | **100 mm** | 2.0 | ~11 kg |
| 2 | **150 mm** | 3.0 | ~18 kg |
| 3 | **200 mm** | 4.0 | **~24 kg** ← en önemlisi |

Kantar **kg** gösteriyorsa Newton'a çevir: `F[N] = kg × 9.81`

**Bana üç okumayı da yaz.** Tek sayı yeterli değil: üç nokta eğriyi
oturtmamı sağlıyor ve modelin doğru olup olmadığını gösteriyor.

---

## SONUÇ NE ANLAMA GELİYOR

λ=4'teki okuma **kol başına kurma kuvvetidir.** İki bant kullanıyorsun:

**toplam kurma kuvveti = 2 × (λ=4 okuması)**

| λ=4 okuması | toplam kurma | karşılık gelen Gmod | menzil |
|---|---|---|---|
| ~13 kg | 261 N | 0.25 MPa | 0.48–0.83 m |
| ~19 kg | 365 N | 0.35 MPa | 0.65–0.91 m |
| ~24 kg | 470 N | 0.45 MPa | 0.78–0.97 m |
| ~29 kg | 574 N | 0.55 MPa | 0.86–1.01 m |
| ~35 kg | 678 N | 0.65 MPa | 0.86–1.05 m |

Hangi satıra düştüğünü söyle, bütün tasarımı o sayıyla sabitlerim —
varsayım kalmaz.

---

## GÜVENLİK

- λ=4'te 24–35 kg gerilim var. Pim sıyrılırsa bant **geri fırlar.**
- **Gözlük tak.** Bandın hizasında durma, yandan çek.
- Pimi bandın ucundan en az **20 mm** içeriden geçir, yoksa yırtar.
- Kantarın kapasitesini aşma (çoğu 50 kg). Aşarsan okuma yanlış olur.

---

## BONUS: KANTARLA KURMA KUVVETİNİ DE ÖLÇ

Fırlatıcı kurulduğunda kantarı kapsül ile çekme ipi arasına koy, geri
çekerken tepe değeri oku. Bu, yukarıdaki tablonun **doğrulamasıdır** —
tutmuyorsa bir yerde hata var, atış yapmadan önce konuşalım.
