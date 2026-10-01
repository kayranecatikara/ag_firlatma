# -*- coding: utf-8 -*-
"""Revize AG KAPSULU - parametrik yeniden insa.

EN KRITIK DEGISIKLIK: bilye yuvalari ALFA kadar disa egik.
Mevcut tasarimda yuva eksenleri (0,1,0), yani tam eksenel -> bilyeler
paralel cikiyor, radyal hiz sifir, AG HIC ACILMIYOR.
"""
import FreeCAD as App, Part, math, os
from FreeCAD import Vector as V

# ---- parametreler (optimizasyondan) -----------------------------------------
P = dict(
    D_bore   = 43.4,    # namlu ic capi
    bosluk   = 0.30,    # kapsul-namlu bosluk (capta)
    L_kapsul = 50.0,
    D_bilye  = 12.9,
    R_pitch  = 13.5,    # bilye bolme cemberi yaricapi
    ALFA     = 18.0,    # >>> YUVA KONIKLIK ACISI (eskiden 0) <<<
    derinlik = 4.2,     # yuva derinligi (bilye yarisindan az -> serbest cikis)
    t_kapak  = 8.0,     # on kapak kalinligi
    t_duvar  = 3.0,     # govde et kalinligi
    t_arka   = 5.0,     # arka duvar (yay basar)
    n_key    = 6,       # donme engelleyici kama sayisi
    key_w    = 3.0, key_h = 1.2,
)

def kapsul(p, egik=True):
    R_out = 0.5*(p["D_bore"] - p["bosluk"])
    R_haz = R_out - p["t_duvar"]
    L, tk, ta = p["L_kapsul"], p["t_kapak"], p["t_arka"]
    a = math.radians(p["ALFA"] if egik else 0.0)

    # govde: silindir, +Y ileri (namlu ekseni), arka yuz y=0
    govde = Part.makeCylinder(R_out, L, V(0,0,0), V(0,1,0))
    # ag haznesi: arka duvar ile on kapak arasi
    hazne = Part.makeCylinder(R_haz, L-tk-ta, V(0,ta,0), V(0,1,0))
    govde = govde.cut(hazne)

    # --- bilye yuvalari: on kapagin on yuzunden ALFA egik --------------------
    yuvalar = []
    for i in range(6):
        th = math.radians(60*i)
        u  = V(math.cos(th), 0, math.sin(th))          # radyal birim
        eks = V(u.x*math.sin(a), math.cos(a), u.z*math.sin(a))  # egik eksen
        # yuva merkezi on yuzde
        c = V(u.x*p["R_pitch"], L, u.z*p["R_pitch"])
        d = p["derinlik"]
        taban = c - eks*d
        # kure yuvasi (bilyeyi saran) + silindirik agiz
        kure = Part.makeSphere(0.5*p["D_bilye"], taban + eks*(0.5*p["D_bilye"]-d*0.0))
        sil  = Part.makeCylinder(0.5*p["D_bilye"], d+8, taban, eks)
        yuvalar.append(kure.fuse(sil))
    for y in yuvalar:
        govde = govde.cut(y)

    # --- donme engelleyici kamalar (namlu yivine oturur) ---------------------
    for i in range(p["n_key"]):
        th = math.radians(60*i + 30)
        u  = V(math.cos(th), 0, math.sin(th))
        kama = Part.makeBox(p["key_w"], L, p["key_h"]*2,
                            V(-p["key_w"]/2, 0, -p["key_h"]))
        m = App.Matrix(); m.rotateY(-th)
        kama = kama.transformGeometry(m)
        kama.translate(u*(R_out + p["key_h"]*0.2))
        govde = govde.fuse(kama)

    # --- ag cikis deligi (merkez) + yay pilotu --------------------------------
    govde = govde.cut(Part.makeCylinder(R_haz*0.62, tk+2, V(0,L-tk-1,0), V(0,1,0)))
    govde = govde.cut(Part.makeCylinder(4.0, ta+1, V(0,-0.5,0), V(0,1,0)))
    return govde.removeSplitter()

def _yol(out, ad, uzanti):
    """ESKI modeller eski_tasarimlar/ alt klasorunde tutulur."""
    alt = os.path.join(out, "eski_tasarimlar") if "ESKI" in ad else out
    os.makedirs(alt, exist_ok=True)
    return os.path.join(alt, ad + uzanti)


if __name__ == "__main__":
    out = os.path.dirname(os.path.abspath(__file__))
    for egik, ad in [(False, "kapsul_ESKI_0deg"), (True, "kapsul_YENI_18deg")]:
        sh = kapsul(P, egik)
        sh.exportStep(_yol(out, ad, ".step"))
        sh.exportBrep(_yol(out, ad, ".brep"))
        print(f"{ad}: hacim={sh.Volume/1000:.2f} cm3  kutle(PETG %40)="
              f"{sh.Volume*1e-9*700*1e3:.1f} g  yuzey={len(sh.Faces)}  "
              f"gecerli={sh.isValid()}")
