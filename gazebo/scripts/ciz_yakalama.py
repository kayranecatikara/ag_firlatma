#!/usr/bin/env python3
"""Gazebo YAKALAMA kosusunu 3B cizer: ag + Talon, zaman dilimleri halinde.

Girdi : out/gazebo_poz.txt  (AgFizik plugin'in yazdigi anlik goruntuler)
        out/gazebo_ag.csv   (olcumler)
Cikti : out/YAKALAMA_3b.png
"""
import sys, os
KOK = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, KOK)
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Line3DCollection

INK, INK2, GRID = "#0b0b0b", "#52514e", "#d8d7d2"
S1, S2, S3 = "#2a78d6", "#eb6834", "#1baf7a"
plt.rcParams.update({"figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb",
                     "text.color": INK, "axes.labelcolor": INK,
                     "xtick.color": INK2, "ytick.color": INK2,
                     "axes.edgecolor": GRID, "grid.color": GRID, "font.size": 9})

POZ = os.path.join(KOK, "out", os.environ.get("AG_POZ", "gazebo_poz.txt"))
E, T, P, H = [], [], [], []
for satir in open(POZ):
    if satir.startswith("# e "):
        _, _, i, j = satir.split(); E.append((int(i), int(j)))
    elif satir.startswith("#"):
        continue
    else:
        gov, _, hed = satir.partition("# hedef")
        v = np.fromstring(gov, sep=" ")
        T.append(v[0]); P.append(v[1:].reshape(-1, 3))
        H.append(np.fromstring(hed, sep=" ") if hed else np.zeros(3))
E = np.array(E); T = np.array(T); P = np.array(P); H = np.array(H)
print(f"{len(T)} anlik goruntu, {P.shape[1]} dugum, {len(E)} eleman")

# --- Talon govde cizgileri (gorsel): govde, kanat, kuyruk, pervane
KANAT, GOVDE_L, PERV = 1.718, 0.90, 0.230


def talon(h):
    x, y, z = h
    g = [([x - GOVDE_L/2, x + GOVDE_L/2], [y, y], [z, z]),
         ([x - .05, x - .05], [y - KANAT/2, y + KANAT/2], [z + .03, z + .03]),
         ([x - .40, x - .40], [y - .26, y + .26], [z + .10, z + .10])]
    th = np.linspace(0, 2*np.pi, 40)
    g.append(([x - .47]*40, y + PERV/2*np.cos(th), z + PERV/2*np.sin(th)))
    return g


# --- hangi anlari cizelim: devir, acilma, carpma, sarma
hedef_t = [T[0], 0.14, 0.18, 0.22, 0.28, T[-1]]
idx = [int(np.argmin(abs(T - h))) for h in hedef_t]

fig = plt.figure(figsize=(16.5, 9.2))
fig.suptitle("GAZEBO YAKALAMA — v5 ağ: Ø2.6 m, KARE göz 200 mm (142 bağ), tetikleme 4.2 m",
             fontsize=14, fontweight="bold", x=.045, ha="left", y=.975)
for n, i in enumerate(idx):
    ax = fig.add_subplot(2, 3, n+1, projection="3d")
    seg = np.stack([P[i][E[:, 0]], P[i][E[:, 1]]], axis=1)
    ax.add_collection3d(Line3DCollection(seg, colors=S1, lw=.45, alpha=.7))
    for gx, gy, gz in talon(H[i]):
        ax.plot(gx, gy, gz, color=S2, lw=2.2, solid_capstyle="round")
    xm = H[i][0]
    ax.set(xlim=(xm-1.6, xm+1.6), ylim=(-1.6, 1.6), zlim=(H[i][2]-1.6, H[i][2]+1.6))
    ax.set_title(f"t = {T[i]*1e3:.0f} ms", loc="left", fontweight="bold", fontsize=11)
    ax.set_xlabel("x (uçuş) [m]", fontsize=8); ax.set_ylabel("y [m]", fontsize=8)
    ax.view_init(elev=18, azim=-62)
    ax.tick_params(labelsize=7); ax.set_box_aspect((1, 1, 1))
plt.tight_layout(rect=(0, 0, 1, .955))
out = os.path.join(KOK, "out", os.environ.get("AG_CIKTI", "YAKALAMA_3b.png"))
plt.savefig(out, dpi=115); print("->", out)
