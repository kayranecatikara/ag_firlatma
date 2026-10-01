# -*- coding: utf-8 -*-
"""Lastik montaj parcalarini tesselate eder: tam + iki kesit duzlemi.

  <ad>_v/_f    : tam kati
  <ad>_zv/_zf  : z>0 atilmis  -> X-Y duzlemi kesiti (tetik pimleri +/-X)
  <ad>_xv/_xf  : x>0 atilmis  -> Y-Z duzlemi kesiti (bantlar + capraz pim +/-Z)
"""
import FreeCAD as App, Part, os, numpy as np
from FreeCAD import Vector as V

OUT = os.path.dirname(os.path.abspath(__file__))
ADLAR = ["L_namlu", "L_kapsul", "L_bilye", "L_capraz_pim",
         "L_bant_ust", "L_bant_alt", "L_pim_sag", "L_pim_sol"]
TOL = {"L_bilye": 0.5, "L_bant_ust": 0.4, "L_bant_alt": 0.4}


def mesh(sh, tol):
    v, f = sh.tessellate(tol)
    return (np.array([[p.x, p.y, p.z] for p in v], dtype=np.float32),
            np.array(f, dtype=np.int32))


def kes(sh, eksen):
    b = sh.BoundBox; d = b.DiagonalLength * 2
    if eksen == "z":
        k = Part.makeBox(d, d, d, V(b.XMin - d * .3, b.YMin - d * .3, 0.0))
    else:
        k = Part.makeBox(d, d, d, V(0.0, b.YMin - d * .3, b.ZMin - d * .3))
    r = sh.cut(k)
    return r if r.Volume > 1e-6 else None


paket = {}
for ad in ADLAR:
    sh = Part.Shape(); sh.read(os.path.join(OUT, ad + ".brep"))
    t = TOL.get(ad, 0.15)
    paket[ad + "_v"], paket[ad + "_f"] = mesh(sh, t)
    for e in ("z", "x"):
        c = kes(sh, e)
        if c is not None:
            paket[f"{ad}_{e}v"], paket[f"{ad}_{e}f"] = mesh(c, t)
    print(f"{ad}: {len(paket[ad + '_f'])} ucgen")
np.savez_compressed(os.path.join(OUT, "lastik_mesh.npz"), **paket)
print("-> cad/lastik_mesh.npz")
