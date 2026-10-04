#!/usr/bin/env python3
"""v1.1 parcalarini MONTAJ KOORDINATLARINDA, web icin seyreltilmis ikili
STL olarak disa aktarir -> web/geo/

Baski STL'leri tablaya dondurulmus/otelenmistir; montaj gorsellestirmesi
icin kullanilamaz. Burada her parca CAD'deki gercek yerinde kalir.

Kullanim:  freecadcmd cad/web_geometri.py
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import FreeCAD, Part, Mesh                                    # noqa: E402
from FreeCAD import Vector as V                               # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lastik_montaj_v4 as M                                  # noqa: E402
from agsim.yollar import kyol                                 # noqa: E402

P = M.P
OUT = kyol("web", "geo")
os.makedirs(OUT, exist_ok=True)
TOL = 0.7                         # tessellation toleransi (mm)

yk = P["arka"]
k1, k2 = M.tetik_kapaklari(P)
t1, t2 = M.tetik_pimleri(P)
tp1, tp2 = M.tamponlar(P)
bs = M.bantlar(P)
gov, bas = M.namlu_bol(P)

PARCALAR = {
    "namlu_govde":   gov,
    "agiz_basligi":  bas,
    "kapsul":        M.kapsul_hazneli(P, yk),
    "capraz_pim":    M.capraz_pim(P),
    "tetik_pim_sag": t1,
    "tetik_pim_sol": t2,
    "tetik_kapak_sag": k1,
    "tetik_kapak_sol": k2,
    "tampon_ust":    tp1,
    "tampon_alt":    tp2,
    "takoz_pad_sag": M.takoz_padi(P)[0],
    "takoz_pad_sol": M.takoz_padi(P)[1],
    "toz_kapagi":    None,          # asagida ayri
    "bant_sag":      bs[0],
    "bant_sol":      bs[1],
}

# toz kapagi baski betiginde tanimli; burada basit halka olarak uretilir
Rb = 0.5 * P["D_bore"]
PARCALAR["toz_kapagi"] = Part.makeCylinder(
    Rb + 2.8, 6.0, V(0, -6.0, 0), V(0, 1, 0)).cut(
    Part.makeCylinder(Rb - 6.0, 8.0, V(0, -7.0, 0), V(0, 1, 0)))

ozet = {}
for ad, sh in PARCALAR.items():
    if sh is None:
        continue
    m = Mesh.Mesh()
    m.addFacets(sh.tessellate(TOL))
    yol = os.path.join(OUT, ad + ".stl")
    m.write(yol)
    bb = sh.BoundBox
    ozet[ad] = {
        "ucgen": m.CountFacets,
        "kb": round(os.path.getsize(yol) / 1024, 1),
        "merkez": [round(bb.Center.x, 2), round(bb.Center.y, 2),
                   round(bb.Center.z, 2)],
        "boyut": [round(bb.XLength, 2), round(bb.YLength, 2),
                  round(bb.ZLength, 2)],
    }
    print(f"  {ad:18} {m.CountFacets:6d} ucgen  {ozet[ad]['kb']:7.1f} kB")

# BONCUKLAR: STL yerine analitik merkez + yaricap (49k ucgen -> 6 sayi ucu)
import math
a = math.radians(P["ALFA"]); Lk = P["L_kapsul"]; Db = P["D_bilye"]
boncuk = []
for i in range(6):
    th = math.radians(60 * i)
    ur = (math.cos(th), math.sin(th))
    eks = (ur[0] * math.sin(a), math.cos(a), ur[1] * math.sin(a))
    c0 = (ur[0] * P["R_pitch"], yk + Lk, ur[1] * P["R_pitch"])
    c = [c0[k] - eks[k] * (Db / 2) for k in range(3)]
    boncuk.append([round(v, 3) for v in c])

# montaj icin gereken olculer
olcu = {k: P[k] for k in (
    "L_namlu", "D_bore", "t_duvar", "STROK", "L_kapsul", "y_yuz_dur",
    "y_ankraj", "y_capraz0", "y_capraz1", "y_bol", "R_pitch", "D_bilye",
    "ALFA", "koni_acisi", "L0", "D_son", "r_bant", "y_tetik", "boss_h",
    "t_omuz", "omuz_bosluk", "arka", "d_pim", "bosluk") if k in P}
json.dump({"parcalar": ozet, "olcu": olcu,
           "boncuk": {"merkez": boncuk, "cap": Db}},
          open(os.path.join(OUT, "_index.json"), "w"), indent=1)
top = sum(v["kb"] for v in ozet.values())
print(f"\n{len(ozet)} parca · toplam {top:.0f} kB -> web/geo/")
