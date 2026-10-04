"""BASKI ALINACAK PARCALARI uretir -> baski/  (STEP + STL)

Sadece 3D YAZICIDAN cikacak parcalar. Satin alinan parcalar (kursun bilye,
aluminyum capraz pim, lateks tup, celik tetik pimi) BURAYA GIRMEZ.

Ek olarak v4 montajinda MODELI OLMAYAN iki parca burada cizilir:
  * A4 servo ip makarasi
  * A6 arka toz kapagi
"""
import os, sys, json
import FreeCAD, Part
from FreeCAD import Vector as V

KOK = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(KOK, "cad"))
import lastik_montaj_v4 as M      # __main__ korumali, parcalari uretmez

P, Rb, Ro = M.P, M.Rb, M.Ro
OUT = os.path.join(KOK, "baski")
os.makedirs(OUT, exist_ok=True)


def sil(r, h, p, d): return Part.makeCylinder(r, h, p, d)


def servo_makarasi():
    """A4 — servonun KENDI koluna 2 vidayla oturan ip makarasi.

    Spline marka marka degisir; bu yuzden spline'a gecmez, servonun
    standart koluna vidalanir. Boylece her servoya uyar.
      tambur r = 2.2 mm  (MIKRO SERVO ICIN KUCULTULDU).

      IS KORUNUMLU: tork x aci = F_pim x strok = SABIT. Onceki r=4 mm
      servonun donus araliginin yalnizca 86 derecesini kullaniyordu;
      r=2.2'de 130 derece kullanilip gereken tork 3.9 -> 2.15 kg.cm'ye
      duser. Kanal derinligi de 5 -> 4 mm indirildigi icin strok 6 -> 5 mm.

      Sonuc: 2 x MG996R (110 g) yerine 2 x mikro metal disli servo
      (Savox SH-0255MG sinifi, 14 g, 3.9 kg.cm) -> PAY 1.81x.
      Sistem kutlesi 492 -> 410 g.
    """
    r_t, w_t, r_f, t_f = 2.2, 4.0, 5.0, 1.2
    g = sil(r_t, w_t, V(0, 0, t_f), V(0, 0, 1))                 # tambur
    g = g.fuse(sil(r_f, t_f, V(0, 0, 0), V(0, 0, 1)))           # alt flans
    g = g.fuse(sil(r_f, t_f, V(0, 0, t_f + w_t), V(0, 0, 1)))   # ust flans
    g = g.cut(sil(1.8, 20, V(0, 0, -1), V(0, 0, 1)))            # kol vidasi bosu
    for s in (+1, -1):                                          # 2x M2 vida
        g = g.cut(sil(1.1, 20, V(s * 3.6, 0, -1), V(0, 0, 1)))
    # ip deligi: tambura teget, ipi iceri alip dugumlemek icin
    g = g.cut(sil(0.6, 30, V(0, -r_t + 0.8, t_f + w_t / 2), V(0, 1, 0)))
    return g


def toz_kapagi():
    """A6 — namlunun ARKA agzina gecen tapa. Ortada havalandirma."""
    d = Rb * 2 - P["bosluk"]
    g = sil(d / 2, 4.0, V(0, 0, 0), V(0, 0, 1))
    g = g.fuse(sil(d / 2 + 3.0, 2.0, V(0, 0, 4.0), V(0, 0, 1)))   # omuz
    g = g.cut(sil(5.0, 20, V(0, 0, -1), V(0, 0, 1)))              # havalandirma
    return g


# ---- BASKI YONU ----
# STL'ler SLICER'A HAZIR yonde verilir: namlu ve kapsul DIK (eksen Z, agiz
# yukari). Boylece bant kulaklarina gelen 1200 N cekme katman duzlemine
# PARALEL olur. Yatay basilirsa kuvvet katmanlari ayirir ve kulak kopar.
# CAD'de +Y ileri (agiz yonu) -> X ekseni etrafinda -90 derece dondur.
def baski_yonu(sh, donus):
    """donus = (eksen, aci) veya None. Parca sonra tablaya oturtulur."""
    sh = sh.copy()
    if donus is not None:
        eks, aci = donus
        sh.rotate(V(0, 0, 0), V(*eks), aci)
    bb = sh.BoundBox
    sh.translate(V(-bb.XMin - bb.XLength / 2, -bb.YMin - bb.YLength / 2,
                   -bb.ZMin))          # tablaya otur, XY'de ortala
    return sh


if __name__ == "__main__":
    yk = P["arka"]
    k1, k2 = M.tetik_kapaklari(P)
    tp1, tp2 = M.tamponlar(P)
    PARCALAR = {
        # ad                      sekil      malzeme   adet  DIK_BAS
        # NAMLU IKI PARCA (bkz. cad/lastik_montaj_v4.py: namlu_bol)
        #  IKISI DE AGIZ ASAGI (-90). Olculdu:
        #    govde  : -90 -> 1769 mm2 destek,  +90 -> 2614 mm2
        #    baslik : -90 ->  338 mm2 destek,  +90 -> 2121 mm2
        #  Baslik ayrildigi icin O104 kulaklar artik HAVADA KALMIYOR.
        "01a_namlu_govde":     (M.namlu_bol(P)[0], "PETG",  1, ((1,0,0), -90)),
        "01b_agiz_basligi":    (M.namlu_bol(P)[1], "PETG",  1, ((1,0,0), -90)),
        "02_kapsul":           (M.kapsul(P, yk), "PETG",    1, ((1,0,0), -90)),
        # tetik kapaklari: CAD'de eksen +-X -> Y etrafinda 90 ile DUZ yatar
        "03_tetik_kapagi_sag": (k1,              "PETG",    1, ((0,1,0),  90)),
        "04_tetik_kapagi_sol": (k2,              "PETG",    1, ((0,1,0),  90)),
        "05_servo_makarasi":   (servo_makarasi(),"PETG",    2, None),
        "06_toz_kapagi":       (toz_kapagi(),    "PETG",    1, None),
        # tampon: en genis yuzey tablaya -> X etrafinda -90
        "07_tampon_ust":       (tp1,             "TPU 95A", 1, ((1,0,0), -90)),
        "08_tampon_alt":       (tp2,             "TPU 95A", 1, ((1,0,0), -90)),
        # DURDURMA OMUZU halkasi: kapsulun carptigi uyumlu katman.
        # Duz halka, CAD'de ekseni +Y -> X etrafinda -90 ile yatar.
        "10_omuz_halkasi":     (M.omuz_halkasi(P), "TPU 95A", 1, ((1,0,0), -90)),
    }
    # dolgu/duvar dahil gercek filament tahmini
    YOGUNLUK = {"PETG": 1.27, "TPU 95A": 1.21}
    DOLU_ORAN = {"01a_namlu_govde": 0.77, "01b_agiz_basligi": 0.80,
                 "02_kapsul": 0.82, "03_tetik_kapagi_sag": 1.0,
                 "04_tetik_kapagi_sol": 1.0, "05_servo_makarasi": 1.0,
                 "06_toz_kapagi": 0.55, "07_tampon_ust": 0.45,
                 "08_tampon_alt": 0.45, "10_omuz_halkasi": 1.0}
    ozet = []
    for ad, (sh0, mlz, adet, donus) in PARCALAR.items():
        sh = baski_yonu(sh0, donus)
        sh.exportStep(os.path.join(OUT, ad + ".step"))
        try:
            import MeshPart
            mesh = MeshPart.meshFromShape(Shape=sh, LinearDeflection=0.05,
                                          AngularDeflection=0.15)
            mesh.write(os.path.join(OUT, ad + ".stl"))
            stl = "var"
        except Exception as e:
            sh.exportStl(os.path.join(OUT, ad + ".stl")); stl = "var"
        bb = sh.BoundBox
        fil = sh.Volume / 1000 * DOLU_ORAN[ad] * YOGUNLUK[mlz] * adet
        ozet.append(dict(ad=ad, malzeme=mlz, adet=adet,
                         hacim_cm3=round(sh.Volume / 1000, 2),
                         filament_g=round(fil, 1),
                         x=round(bb.XLength, 1), y=round(bb.YLength, 1),
                         z=round(bb.ZLength, 1), gecerli=sh.isValid()))
        print(f"{ad:22s} {mlz:8s} x{adet}  {sh.Volume/1000:7.2f} cm3  "
              f"{bb.XLength:5.1f}x{bb.YLength:5.1f}x{bb.ZLength:6.1f} mm  "
              f"~{fil:6.1f} g  gecerli={sh.isValid()}")
    json.dump(ozet, open(os.path.join(OUT, "parcalar.json"), "w"), indent=1)
    tp = sum(o["filament_g"] for o in ozet if o["malzeme"] == "PETG")
    tt = sum(o["filament_g"] for o in ozet if o["malzeme"].startswith("TPU"))
    print(f"\nTOPLAM FILAMENT:  PETG {tp:.0f} g   TPU {tt:.1f} g")
    print(f"-> {OUT}  (STL'ler SLICER'A HAZIR yonde, tablaya oturtulmus)")
