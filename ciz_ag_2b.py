#!/usr/bin/env python3
"""AGIN TAM ACILMIS HALI — 2B, topoloji secenekleri yan yana."""
import os, sys
_K = os.path.abspath(__file__)
while _K != os.path.dirname(_K) and not os.path.isdir(os.path.join(_K, "agsim")):
    _K = os.path.dirname(_K)
sys.path.insert(0, _K)
from agsim.yollar import vyol
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from agsim.hexag import altigen_ag, kare_ag, cevre_ipi_ekle
from agsim.params import Ag

S1, S2, S3 = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#d8d7d2"
plt.rcParams.update({"figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb",
    "text.color": INK, "axes.labelcolor": INK, "xtick.color": INK2,
    "ytick.color": INK2, "axes.edgecolor": GRID, "font.size": 9.5})

ag = Ag(R_ag=1.4, goz=0.14, d_iplik=0.165e-3)
PERV = 0.230                       # Talon pervane capi
# kapsul ag haznesi -- CAD'den: Rh = D_bore/2 - bosluk/2 - t_govde
V_HAZNE = np.pi * 18.55e-3**2 * 16.0e-3        # 17.3 cm3
YOGUNLUK = 0.20                                 # parasut-katlama yogunlugu

# (ad, uretici, R_ag, goz, pencere, vurgu)
SEC = [("ESKİ:  ALTIGEN  Ø2.8 m  göz 140", altigen_ag, 1.4, .140,
        "3.56 – 6.44 m", False),
       ("ARA:  KARE  Ø2.8 m  göz 140", kare_ag, 1.4, .140,
        "3.56 – 6.22 m", False),
       ("YENİ:  KARE  Ø2.6 m  göz 200", kare_ag, 1.3, .200,
        "3.58 – 6.80 m", True)]

fig, ax = plt.subplots(1, 3, figsize=(16.5, 6.4))
plt.subplots_adjust(left=.03, right=.985, top=.72, bottom=.06, wspace=.06)

for a, (ad, fn, Rag, g, pen, vurgu) in zip(ax, SEC):
    P, E, _ = fn(Rag, g)
    P, E, bd = cevre_ipi_ekle(P, E, Rag)     # ÇEVRE HALATI dahil
    L0 = np.linalg.norm(P[E[:, 1]] - P[E[:, 0]], axis=1)
    m = ag.rho_iplik * ag.A_iplik * L0.sum()

    seg = np.stack([P[E[:, 0], :2], P[E[:, 1], :2]], axis=1)
    a.add_collection(LineCollection(seg, colors=S1, lw=.6, alpha=.85))
    a.plot(P[:, 0], P[:, 1], ".", color=S1, ms=1.6, alpha=.5)
    a.plot(P[bd, 0], P[bd, 1], "o", color="#2b2b2b", ms=11, mec="white", mew=1.4,
           zorder=5, label="kurşun bilye Ø12.7 × 6")

    # cevre halati (gercek iplik, cizimde vurgulu)
    th = np.arange(7) * np.pi / 3
    a.plot(Rag*np.cos(th), Rag*np.sin(th), color=S3, lw=2.6, alpha=.95,
           solid_joinstyle="round", label="çevre halatı (8.4 m)", zorder=4)

    # pervane yakalama cemberi (en kotu konum: hucrenin tam ortasi)
    cx, cy = (0.42, -0.45)
    a.add_patch(plt.Circle((cx, cy), PERV/2, fill=False, color=S2, lw=2.3,
                           zorder=6))
    a.text(cx, cy - PERV/2 - .085, "Talon pervanesi Ø230", color=S2,
           fontsize=8.2, ha="center", fontweight="bold")

    a.set_aspect("equal"); a.set_xlim(-1.55, 1.55); a.set_ylim(-1.58, 1.62)
    a.axis("off")
    renk = S3 if vurgu else INK
    a.set_title(f"{ad}", loc="center", fontweight="bold", fontsize=12,
                color=renk, pad=10)
    a.text(0, -1.50,
           f"{len(P)} bağ · {L0.sum():.0f} m iplik (örgü+halat) · {m*1e3:.2f} g\n"
           f"~{len(P)/60:.1f} saat el emeği · hazne dolumu "
           f"%{ag.A_iplik*L0.sum()/YOGUNLUK/V_HAZNE*100:.0f}\n"
           f"pencere {pen}",
           ha="center", va="top", fontsize=9.6, color=INK,
           bbox=dict(boxstyle="round,pad=0.45", fc="white", ec=GRID))
    if a is ax[0]:
        a.legend(fontsize=8.5, frameon=False, loc="upper left")

fig.suptitle("AĞ SADELEŞTİRME — tek ip pervaneye yeterse düğüm şartı kalkar, "
             "göz açılır\n"
             "Daha az iplik + daha az bağ = daha az dolanma riski VE daha uzun "
             "menzil (az sürükleme)",
             fontsize=13.5, fontweight="bold", x=.03, ha="left", y=.965)
plt.savefig(vyol(__file__, "out", "AG_2B_topoloji.png"), dpi=118)
print("-> out/AG_2B_topoloji.png")
