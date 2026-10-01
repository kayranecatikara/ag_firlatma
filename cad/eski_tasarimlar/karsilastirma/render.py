# -*- coding: utf-8 -*-
"""FreeCAD katilarini tesselate edip mesh.npz olarak yazar.

Ciktida her parca icin:
  <ad>_v, <ad>_f    : tam kati
  <ad>_kv, <ad>_kf  : z>0 yarisi kesilmis (ic yapi icin)
Koordinatlar CAD'deki gibi birakilir; dondurmeyi cizim tarafi yapar.
"""
import FreeCAD as App, Part, os, numpy as np
from FreeCAD import Vector as V

OUT = os.path.dirname(os.path.abspath(__file__))
ADLAR = ["kapsul_ESKI_0deg", "kapsul_YENI_18deg",
         "namlu_agiz_ESKI", "namlu_agiz_YENI"]


def mesh(sh, tol=0.10):
    v, f = sh.tessellate(tol)
    return (np.array([[p.x, p.y, p.z] for p in v], dtype=np.float32),
            np.array(f, dtype=np.int32))


def yarim(sh):
    """z > 0 yarisini atar -> z=0 duzleminde kesit."""
    b = sh.BoundBox
    d = b.DiagonalLength * 1.5
    return sh.cut(Part.makeBox(d, d, d, V(b.XMin - d * .3, b.YMin - d * .3, 0.0)))


paket = {}
for ad in ADLAR:
    alt = os.path.join(OUT, "eski_tasarimlar") if "ESKI" in ad else OUT
    yol = os.path.join(alt, ad + ".brep")
    if not os.path.exists(yol):
        print("atlandi:", ad)
        continue
    sh = Part.Shape(); sh.read(yol)
    v, f = mesh(sh); paket[ad + "_v"], paket[ad + "_f"] = v, f
    vk, fk = mesh(yarim(sh)); paket[ad + "_kv"], paket[ad + "_kf"] = vk, fk
    print(f"{ad}: {len(v)} dugum / {len(f)} ucgen | kesit {len(vk)}/{len(fk)}")

np.savez_compressed(os.path.join(OUT, "mesh.npz"), **paket)
print("-> cad/mesh.npz")
