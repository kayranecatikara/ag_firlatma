# -*- coding: utf-8 -*-
"""Revize NAMLU AGIZ bolumu: helis yiv + iraksak agiz konisi + durdurma omuzu.

Yiv adimi DSE optimumundan gelir (730 mm/tur). Yiv, kapsulu dondurerek
bilyelere TEGET hiz kazandirir; bu, konik yuvalarin radyal hizina eklenir
ve agin acilma suresini kisaltir.
"""
import FreeCAD as App, Part, math, os
from FreeCAD import Vector as V

P = dict(D_bore=43.4, t_duvar=6.0, L=90.0,
         twist=730.0,                   # mm/tur (DSE optimumu)
         n_yiv=6, yiv_w=3.4, yiv_d=1.4,
         ALFA=18.0, L_koni=22.0,        # iraksak agiz konisi
         omuz=3.0)                      # kapsul durdurma omuzu


def _helis_kanal(Rb, L, twist, th0_deg, w, d):
    """Helis yiv kanalini kati olarak uretir (Y ekseni boyunca)."""
    h = Part.makeHelix(twist, L + 6.0, Rb)          # Z ekseninde uretilir
    prof = Part.makePlane(w, d * 2.0, V(Rb - d, -w / 2.0, 0.0))
    m = App.Matrix(); m.rotateZ(math.radians(th0_deg))
    h = h.copy(); h.transformShape(m)
    prof = prof.copy(); prof.transformShape(m)
    kanal = Part.Wire(h.Edges).makePipeShell([Part.Wire(prof.Edges)], True, True)
    kanal = Part.Solid(Part.Shell(kanal.Faces)) if not kanal.Solids else kanal.Solids[0]
    mr = App.Matrix(); mr.rotateX(math.radians(-90))   # Z -> Y
    kanal = kanal.copy(); kanal.transformShape(mr)
    kanal.translate(V(0.0, -3.0, 0.0))
    return kanal


def agiz(p, yivli=True, konili=True):
    Rb, tw, L = 0.5 * p["D_bore"], p["t_duvar"], p["L"]
    Ro = Rb + tw
    govde = Part.makeCylinder(Ro, L, V(0, 0, 0), V(0, 1, 0))
    govde = govde.cut(Part.makeCylinder(Rb, L + 4, V(0, -2, 0), V(0, 1, 0)))

    if yivli:
        for i in range(p["n_yiv"]):
            th0 = 360.0 * i / p["n_yiv"]
            try:
                govde = govde.cut(_helis_kanal(Rb, L, p["twist"], th0,
                                               p["yiv_w"], p["yiv_d"]))
            except Exception:
                kutu = Part.makeBox(p["yiv_w"], L + 4, p["yiv_d"] * 2,
                                    V(-p["yiv_w"] / 2, -2, Rb - p["yiv_d"]))
                mk = App.Matrix(); mk.rotateY(math.radians(-th0))
                kutu = kutu.copy(); kutu.transformShape(mk)
                govde = govde.cut(kutu)

    if konili:
        Lk = p["L_koni"]
        R2 = Rb + Lk * math.tan(math.radians(p["ALFA"]))
        govde = govde.cut(Part.makeCone(Rb, R2, Lk + 0.5,
                                        V(0, L - Lk, 0), V(0, 1, 0)))

    # kapsul durdurma omuzu: koni girisinde ic bilezik
    y0 = L - p["L_koni"] - 4.0
    bilezik = Part.makeCylinder(Rb, 4.0, V(0, y0, 0), V(0, 1, 0)).cut(
        Part.makeCylinder(Rb - p["omuz"], 6.0, V(0, y0 - 1, 0), V(0, 1, 0)))
    govde = govde.fuse(bilezik)
    return govde.removeSplitter()


def _yol(out, ad, uzanti):
    """ESKI modeller eski_tasarimlar/ alt klasorunde tutulur."""
    alt = os.path.join(out, "eski_tasarimlar") if "ESKI" in ad else out
    os.makedirs(alt, exist_ok=True)
    return os.path.join(alt, ad + uzanti)


if __name__ == "__main__":
    out = os.path.dirname(os.path.abspath(__file__))
    for yivli, ad in [(False, "namlu_agiz_ESKI"), (True, "namlu_agiz_YENI")]:
        sh = agiz(P, yivli=yivli, konili=yivli)
        sh.exportStep(_yol(out, ad, ".step"))
        sh.exportBrep(_yol(out, ad, ".brep"))
        print(f"{ad}: hacim={sh.Volume/1000:.2f} cm3 yuzey={len(sh.Faces)} "
              f"gecerli={sh.isValid()}")
