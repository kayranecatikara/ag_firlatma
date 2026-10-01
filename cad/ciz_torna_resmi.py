#!/usr/bin/env python3
"""TORNACIYA VERILECEK OLCULU RESIM — B1 capraz pim, B2 tetik pimi."""
import os
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

KOK = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INK, INK2, GRID = "#0b0b0b", "#52514e", "#c9c8c4"
MET, OLC = "#b9bcc4", "#eb6834"
plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "white",
                     "font.size": 9, "text.color": INK})

fig, ax = plt.subplots(2, 1, figsize=(13.5, 8.2))
plt.subplots_adjust(left=.04, right=.98, top=.88, bottom=.06, hspace=.42)


def olcu(a, x0, x1, y, txt, yaz_ust=True, renk=OLC):
    a.annotate("", (x0, y), (x1, y),
               arrowprops=dict(arrowstyle="<->", color=renk, lw=1.1))
    a.text((x0+x1)/2, y + (1.6 if yaz_ust else -3.2), txt, ha="center",
           va="bottom" if yaz_ust else "top", fontsize=8.5, color=renk,
           fontweight="bold")


# ------------------------------------------------- B1 CAPRAZ PIM
a = ax[0]
L, D, Dg = 92.0, 8.0, 6.0
a.add_patch(Rectangle((-L/2, -D/2), L, D, fc=MET, ec=INK, lw=1.3))
for zc in (-44, -33, 33, 44):                      # 4 oluk
    a.add_patch(Rectangle((zc-1.2, -Dg/2), 2.4, Dg, fc="white", ec=INK, lw=1.1))
    a.plot([zc, zc], [-D/2-7, D/2+7], color=GRID, lw=.7, ls="-.")
a.plot([-L/2-6, L/2+6], [0, 0], color=GRID, lw=.8, ls="-.")   # eksen

olcu(a, -L/2, L/2, 15, "92.0")
olcu(a, -44, 44, 10.5, "88.0  (oluk merkezleri)")
olcu(a, -33, 33, 6.5, "66.0")
olcu(a, 33, 44, -11, "11.0", False)
a.annotate("Ø8.0", (-L/2+5, 0), (-L/2+5, -17), ha="center", fontsize=9,
           color=OLC, fontweight="bold",
           arrowprops=dict(arrowstyle="->", color=OLC, lw=1.1))
a.annotate("oluk: 2.4 geniş × 1.0 derin\n(dip çapı Ø6.0), 4 ADET",
           (44, Dg/2), (56, 17), fontsize=8.5, color=OLC, fontweight="bold",
           ha="center", arrowprops=dict(arrowstyle="->", color=OLC, lw=1.1))
a.set_title("B1 — ÇAPRAZ PİM   ·   Alüminyum 7075-T6 (alt.: gümüş çeliği)   ·   1 adet",
            loc="left", fontweight="bold", fontsize=12)
a.set_xlim(-62, 72); a.set_ylim(-24, 24); a.set_aspect("equal"); a.axis("off")

# ------------------------------------------------- B2 TETIK PIMI
a = ax[1]
L2, D2 = 20.7, 5.0
a.add_patch(Rectangle((0, -D2/2), L2, D2, fc=MET, ec=INK, lw=1.3))
a.add_patch(plt.Circle((L2-1.0, 0), 0.75, fc="white", ec=INK, lw=1.1))
a.plot([L2-1.0, L2-1.0], [-D2/2-5, D2/2+5], color=GRID, lw=.7, ls="-.")
a.plot([-4, L2+4], [0, 0], color=GRID, lw=.8, ls="-.")
# uc pah
a.plot([0, 0.8], [-D2/2, -D2/2+0.8], color=INK, lw=1.3)
a.plot([0, 0.8], [D2/2, D2/2-0.8], color=INK, lw=1.3)

olcu(a, 0, L2, 7.5, "20.7")
a.annotate("1.0", (L2-0.5, -D2/2-1.2), (L2+6, -5.5), fontsize=8.5,
           color=OLC, fontweight="bold", ha="center",
           arrowprops=dict(arrowstyle="->", color=OLC, lw=1.0))
a.annotate("Ø5.0", (3, 0), (3, -9), ha="center", fontsize=9, color=OLC,
           fontweight="bold",
           arrowprops=dict(arrowstyle="->", color=OLC, lw=1.1))
a.annotate("Ø1.5 enine delik\n(ip geçecek)", (L2-1.0, 0.75), (L2+5, 9),
           fontsize=8.5, color=OLC, fontweight="bold", ha="center",
           arrowprops=dict(arrowstyle="->", color=OLC, lw=1.1))
a.annotate("uç hafif pahlı\n(kanala girecek)", (0.4, -D2/2+0.4), (-7, -10),
           fontsize=8.5, color=OLC, fontweight="bold", ha="center",
           arrowprops=dict(arrowstyle="->", color=OLC, lw=1.1))
a.set_title("B2 — TETİK PİMİ   ·   Gümüş çeliği / paslanmaz   ·   2 adet\n"
            "yüzey PÜRÜZSÜZ olmalı — PTFE burç içinde kayacak",
            loc="left", fontweight="bold", fontsize=11.5)
a.set_xlim(-16, 40); a.set_ylim(-15, 14); a.set_aspect("equal"); a.axis("off")

fig.suptitle("TORNA İŞ EMRİ — Ağ Fırlatıcı v5   ·   ölçüler mm   ·   "
             "tolerans ±0.1 mm   ·   kesme sonrası çapak alınacak",
             fontsize=13, fontweight="bold", x=.04, ha="left", y=.965)
out = os.path.join(KOK, "TORNA_IS_EMRI.png")
plt.savefig(out, dpi=135, facecolor="white")
print("->", out)
