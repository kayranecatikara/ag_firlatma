# -*- coding: utf-8 -*-
"""Montaj parcalarini tesselate edip montaj_mesh.npz olarak yazar."""
import FreeCAD as App, Part, os, numpy as np
from FreeCAD import Vector as V

OUT = os.path.dirname(os.path.abspath(__file__))
ADLAR = ["M_namlu", "M_kapsul", "M_bilye", "M_yay", "M_pim_sag", "M_pim_sol"]


def mesh(sh, tol=0.25):
    v, f = sh.tessellate(tol)
    return (np.array([[p.x, p.y, p.z] for p in v], dtype=np.float32),
            np.array(f, dtype=np.int32))


def yarim(sh):
    b = sh.BoundBox
    d = b.DiagonalLength * 1.5
    return sh.cut(Part.makeBox(d, d, d, V(b.XMin - d * .3, b.YMin - d * .3, 0.0)))


paket = {}
for ad in ADLAR:
    yol = os.path.join(OUT, ad + ".brep")
    if not os.path.exists(yol):
        print("atlandi:", ad); continue
    sh = Part.Shape(); sh.read(yol)
    tol = {"M_yay": 1.2, "M_bilye": 0.6}.get(ad, 0.20)
    v, f = mesh(sh, tol); paket[ad + "_v"], paket[ad + "_f"] = v, f
    # namlu ve kapsul icin kesit; kucuk parcalar tam kalsin
    if ad in ("M_namlu", "M_kapsul"):
        vk, fk = mesh(yarim(sh), tol)
    else:
        vk, fk = v, f
    paket[ad + "_kv"], paket[ad + "_kf"] = vk, fk
    print(f"{ad}: {len(v)} dugum / {len(f)} ucgen")

np.savez_compressed(os.path.join(OUT, "montaj_mesh.npz"), **paket)
print("-> cad/montaj_mesh.npz")
