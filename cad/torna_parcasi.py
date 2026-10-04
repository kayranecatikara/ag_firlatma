#!/usr/bin/env python3
"""Capraz pimi baski/ klasorune STL+STEP olarak koyar.

BASILMAZ parca: O8 aluminyum milden tornalanir. STL sadece olcu/gorsel icin,
tornaciya .step verilir. Baski filament toplamina DAHIL DEGILDIR.

Kullanim:  freecadcmd cad/torna_parcasi.py
"""
import os, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import FreeCAD, Part, Mesh                                    # noqa: E402
from agsim.yollar import kyol                                 # noqa: E402

src = kyol("cad", "V4_capraz_pim.step")
s = Part.Shape(); s.read(src)
m = Mesh.Mesh(); m.addFacets(s.tessellate(0.15))
m.write(kyol("baski", "09_capraz_pim_TORNA.stl"))
shutil.copy2(src, kyol("baski", "09_capraz_pim_TORNA.step"))
bb = s.BoundBox
print(f"09_capraz_pim_TORNA  {s.Volume/1000:.2f} cm3  "
      f"O{bb.XLength:.0f} x {bb.ZLength:.0f} mm  gecerli={s.isValid()}  (BASILMAZ)")
