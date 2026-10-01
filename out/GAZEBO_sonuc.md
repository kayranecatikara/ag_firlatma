# GAZEBO ENTEGRASYONU — SONUÇLAR

## 1. Ne yapıldı
Ağ fiziği (`agsim/netfull.py`) Gazebo Harmonic'e **özel bir sistem plugin'i**
(`gazebo/plugin/AgFizik.cc`) olarak taşındı. Gazebo'nun kendi sürükleme
eklentileri ipliği modelleyemez; iplik gerilmesi + normal/teğet silindir
sürüklemesi plugin içinde hesaplanıp `AddWorldForce` ile uygulanıyor.

## 2. Doğrulama — iki bağımsız çözücü
| | R_tepe | t_tepe | Pencere |
|---|---|---|---|
| Python (velocity-Verlet) | 1.126 m | 192 ms | 3.54 – 6.08 m |
| Gazebo (DART) | 1.120 m | 192 ms | 3.54 – 6.04 m |
| **sapma** | **−0.5 %** | **−0.2 %** | **0.04 m** |

Gerçek altıgen örgüde devir sonrası serbest uçuş sapması **%0.23**.

## 3. TASARIM SAYILARI DEĞİŞTİ — örgü topolojisi
Tüm tasarım taraması "örümcek ağı" topolojisiyle (halka + parmaklık)
yapılmıştı. Gerçek **altıgen (bal peteği)** örgü farklı açılıyor:

| topoloji | düğüm | R_tepe | pencere |
|---|---|---|---|
| örümcek 7×18 (tasarımda kullanılan) | 127 | 1.067 m | 3.56 – 5.74 m |
| örümcek 10×24 (yakınsama kontrolü) | 241 | 1.065 m | — |
| **ALTIGEN (gerçek, göz 140 mm)** | **709** | **1.139 m** | **3.56 – 6.22 m** |

Sebep topolojik: örümcek ağındaki **sürekli çevrel halkalar** çember
gerilmesiyle açılmaya direnir; bal peteğinde sürekli halka yoktur.
**Yön iyi:** tasarım öngörüldüğünden %6.7 daha geniş açılıyor, pencerenin
uzak kenarı 5.74 → 6.22 m'ye çıkıyor. Hedeflenen 5–6 m tamamen içeride.

Doğrulama: üretilen örgü 83.2 m iplik veriyor, `params.py`'daki analitik
`L_iplik = 2A/göz + 6R` formülü 81.1 m — **%2.5 uyum**.

## 4. YAKALAMA (Gazebo'nun asıl katkısı)
Hedef: X-UAV Talon, 4.65 m'de, seyir trimli (taşıma = ağırlık).

| büyüklük | değer |
|---|---|
| tepe iplik gerilmesi | **9.9 N** |
| iplik kopma yükü | 64.1 N |
| **emniyet katsayısı** | **6.5×** |
| kopan eleman | **0** |
| ağın uçak üzerine serilen oranı | **%58 (410/709 düğüm)** |
| hedefe aktarılan momentum | **1.05 kg·m/s** (hız 0 → 0.58 m/s) |

**Çözünürlük belirleyici:** kaba 5×12 ağda "uçak üzerindeki düğüm" 14'te tepe
yapıp **sıfıra** düşüyordu — ağ hedefin içinden geçiyordu (kaba örgünün göz
açıklığı 0.73 m, Talon gövdesi 0.085 m). Gerçek 140 mm gözlü örgüde sayı
410'a tırmanıp kalıyor.

## 5. SINIR — neyin cevabı Gazebo'dan ÇIKMAZ
Ağın **hazneden çıkışı** rijit-cisim temas problemi değildir: paketli halde
709 çarpışma küresi 16 mm'lik hazneye tıkılıdır, DART'ın LCP çözücüsü
yüz binlerce temas kısıtıyla çöker. Çözüm **hibrit**:
* paketten açılma → doğrulanmış Python modeli (`netfull`, hex topoloji)
* temas / sarma → Gazebo, ağı t = 80 ms'de **açık halde devralır**

Ayrıca **iplik düzeyinde pervaneye dolanma** (0.165 mm iplik, sürtünmeyle
sarılma) rijit-cisim + LCP ile çözülemez; bu bir ip/kumaş (Cosserat çubuk
veya konum-tabanlı dinamik) problemidir. O soru analitik olarak zaten
yanıtlanmıştı: çapı a√2 olan her çember bir ağ düğümü içerir.

## 6. Dosyalar
```
gazebo/plugin/AgFizik.cc        ağ fiziği sistem plugin'i (gz-sim 8)
gazebo/plugin/build/            derleme çıktısı (libAgFizik.so)
gazebo/scripts/ag_sdf_uret.py   dünya üreteci  (AG_ORGU, AG_CARPISMA, AG_DEVIR)
gazebo/scripts/karsilastir.py   Gazebo ↔ Python doğrulaması
gazebo/scripts/ciz_yakalama.py  3B yakalama görselleştirmesi
gazebo/kos.sh                   koşu betiği (dogrulama | yakalama [gui])
agsim/hexag.py                  GERÇEK altıgen örgü üreteci  [YENİ]
out/gazebo_ag.csv               ölçümler
out/gazebo_poz.txt              düğüm anlık görüntüleri
out/gazebo_dogrulama.png        çözücü karşılaştırması
out/gazebo_yakalama_dogrulama.png  yakalama doğrulaması
out/YAKALAMA_3b.png             3B dizi
```

### Çalıştırma
```bash
./gazebo/kos.sh dogrulama                 # hızlı, hedefsiz, Python ile karşılaştırma
AG_ORGU=hex ./gazebo/kos.sh yakalama      # gerçek örgü + hedef
AG_ORGU=hex ./gazebo/kos.sh yakalama gui  # üstüne GUI
```

## 7. Yol boyunca düzeltilen hatalar
1. `SetLinearVelocity` kalıcı **kinematik kısıt** bırakıyor (`LinearVelocityCmd`
   her adımda yeniden uygulanıyor) → gövdeler hıza kilitleniyordu. Atıştan bir
   adım sonra komut kaldırılıyor.
2. **dt çok büyüktü** (0.5 ms, kararlı sınır 0.12 ms) → sayısal patlama, ODE
   AABB taşması. Artık dt iplik periyodundan otomatik türetiliyor.
3. Sönümleme nominal 1e-4 kg kullanıyordu, gerçek düğüm kütlesi 2.76e-5 kg →
   **1.9× fazla sönümleme**. SDF'den gerçek kütle veriliyor.
4. Radyal açılma hızı tüm düğümlere veriliyordu; Python yalnızca bilyelere
   veriyor. Eşitlendi.
5. Hedef **serbest düşüyordu** → `hedef_dx` ağ etkisini değil düşüşü ölçüyordu.
   Seyir trim kuvveti (m·g) eklendi, atıştan önce de uygulanıyor.
6. Kuvvet tavanı 5 N, çarpma anında 10486 kez devreye girip **fiziği
   bozuyordu**. 200 N'a (yalnızca NaN koruması) çekildi; yerine kopma sayacı.
