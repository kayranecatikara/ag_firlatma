# -*- coding: utf-8 -*-
"""Lastik bant tahrikli firlatici: dis gorunus, bant kesiti, tetik kesiti, bilgi."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from izdusum import ciz as izciz

S1, S2, S3 = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#d8d7d2"
RENK = {"L_namlu": "#8fa3b8", "L_kapsul": S1, "L_bilye": "#4a4a46",
        "L_capraz_pim": "#7d7d76", "L_bant_ust": S3, "L_bant_alt": S3,
        "L_pim_sag": S2, "L_pim_sol": S2}
plt.rcParams.update({"figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb",
                     "text.color": INK, "font.size": 9.5})
D = np.load("cad/lastik_mesh.npz")
ADLAR = list(RENK)


def kesit(ax, eksen, sirala, zorder0=1):
    """eksen='x': Y-Z duzlemi (ekran: y->yatay, z->dikey)
       eksen='z': X-Y duzlemi (ekran: y->yatay, x->dikey)"""
    ni = 0 if eksen == "x" else 2
    for k, ad in enumerate(sirala):
        key = f"{ad}_{eksen}v"
        if key not in D:
            continue
        v, f = D[key], D[f"{ad}_{eksen}f"]
        tri = v[f]
        n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
        ln = np.linalg.norm(n, axis=1, keepdims=True); ln[ln == 0] = 1
        m = np.abs((n / ln)[:, ni]) > 0.98
        yx = tri[m][:, :, [1, 2 if eksen == "x" else 0]]
        ax.add_collection(PolyCollection(yx, facecolors=RENK[ad], edgecolors=RENK[ad],
                                         linewidths=.25, zorder=zorder0 + k))


fig = plt.figure(figsize=(15.5, 10.2))
gs = fig.add_gridspec(3, 2, height_ratios=[1.0, 1.05, 0.95], width_ratios=[1.35, 1],
                      hspace=.22, wspace=.07, left=.025, right=.985, top=.905, bottom=.035)

# ---------------- (a) dis gorunus --------------------------------------------
ax = fig.add_subplot(gs[0, :])
izciz(ax, [(D[a + "_v"], D[a + "_f"], RENK[a]) for a in ADLAR], elev=28, azim=-18)
ax.margins(.03)
ax.set_title("(a) Dış görünüş — kurulu hâl: 2 lateks bant (yeşil) üstte/altta, "
             "tetik kartuşları yanlarda, ağızda bant bileziği",
             loc="left", fontweight="bold", fontsize=11)

# ---------------- (b) Y-Z kesiti: bantlar + capraz pim -----------------------
ax = fig.add_subplot(gs[1, 0])
kesit(ax, "x", ["L_namlu", "L_kapsul", "L_capraz_pim", "L_bant_ust", "L_bant_alt"])
ax.plot([-4, 264], [0, 0], color=GRID, lw=1, ls="-.", zorder=0)
for s in (+1, -1):
    ax.annotate("", xy=(186, s * 34), xytext=(24, s * 34),
                arrowprops=dict(arrowstyle="->", color=S3, lw=2.2), zorder=20)
ax.text(105, 41, "bantların çektiği yön", ha="center", fontsize=9, color="#0f6e4c",
        fontweight="bold")
ax.annotate("çapraz pim\n(yarıktan dışarı çıkar,\nbant buna bağlanır)", xy=(9.5, -30),
            xytext=(30, -58), fontsize=9, color=INK, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=INK2, lw=1.2), zorder=20)
ax.annotate("düz yarık\n(dönme engelleyici)", xy=(120, -24.7), xytext=(130, -56),
            fontsize=9, color=INK2, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=INK2, lw=1.2), zorder=20)
ax.annotate("bant kulağı", xy=(251, 36), xytext=(212, 52), fontsize=9, color=INK2,
            fontweight="bold", arrowprops=dict(arrowstyle="->", color=INK2, lw=1.2),
            zorder=20)
ax.annotate("omuz", xy=(236, -19), xytext=(214, -46), fontsize=9, color=INK2,
            fontweight="bold", arrowprops=dict(arrowstyle="->", color=INK2, lw=1.2),
            zorder=20)
ax.annotate("", xy=(234, -66), xytext=(55, -66),
            arrowprops=dict(arrowstyle="<->", color=S1, lw=1.4))
ax.text(144, -73, "STROK 179 mm", ha="center", fontsize=9, color=S1, fontweight="bold")
ax.annotate("", xy=(260, -80), xytext=(0, -80),
            arrowprops=dict(arrowstyle="<->", color=INK, lw=1.2))
ax.text(130, -87, "namlu 260 mm  (arka AÇIK = yükleme ağzı)", ha="center", fontsize=9)
ax.set_xlim(-6, 266); ax.set_ylim(-92, 60); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("(b) Bant düzlemi kesiti — yivsiz, düz delik", loc="left",
             fontweight="bold", fontsize=11)

# ---------------- (c) X-Y kesiti: tetik -------------------------------------
ax = fig.add_subplot(gs[1, 1])
kesit(ax, "z", ["L_namlu", "L_kapsul", "L_pim_sag", "L_pim_sol"])
ax.plot([-4, 90], [0, 0], color=GRID, lw=1, ls="-.", zorder=0)
for s in (+1, -1):
    ax.annotate("", xy=(16.7, s * 60), xytext=(16.7, s * 47),
                arrowprops=dict(arrowstyle="->", color=S2, lw=2.2), zorder=20)
ax.text(24, 55, "ip RADYAL çeker", fontsize=9, color=S2, fontweight="bold")
ax.annotate("pim, kapsülün\ntutma kanalında", xy=(16.7, 18.5), xytext=(40, 8),
            fontsize=9, color=INK, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=INK2, lw=1.2), zorder=20)
ax.annotate("geri-getirme\nyayı yuvası", xy=(16.7, -38), xytext=(38, -34),
            fontsize=9, color=INK2, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=INK2, lw=1.2), zorder=20)
ax.annotate("servo yatağı", xy=(50.7, -29.7), xytext=(56, -52), fontsize=9,
            color=INK2, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=INK2, lw=1.2), zorder=20)
ax.set_xlim(-4, 92); ax.set_ylim(-64, 64); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("(c) Tetik kartuşu kesiti (arka bölge)", loc="left",
             fontweight="bold", fontsize=11)

# ---------------- (d) bant sartnamesi ---------------------------------------
ax = fig.add_subplot(gs[2, 0]); ax.axis("off")
ax.set_title("(d) Lastik bant şartnamesi", loc="left", fontweight="bold", fontsize=11)
sat = [("Malzeme", "saf doğal kauçuk LATEKS tüp (zıpkın lastiği)"),
       ("Kesit", "Ø14 dış / Ø4 iç mm,  2 adet"),
       ("Kauçuk boyu (serbest)", "65 mm  (yüksükler arası)"),
       ("Kurulu uzama", "×3.5   (65 → 228 mm)"),
       ("Kurma kuvveti", "217 N / bant   (toplam 435 N)"),
       ("Depolanan enerji", "40.8 J   ·   bant kütlesi 17.5 g"),
       ("Çıkış hızı", "27.8 m/s   ·   atış penceresi 2.0 – 4.2 m")]
y = 0.90
for a, b in sat:
    ax.text(0.01, y, a, fontsize=9.8, color=INK2, transform=ax.transAxes)
    ax.text(0.34, y, b, fontsize=9.8, fontweight="bold", transform=ax.transAxes)
    y -= 0.13

# ---------------- (e) yukleme sirasi -----------------------------------------
ax = fig.add_subplot(gs[2, 1]); ax.axis("off")
ax.set_title("(e) Kurma sırası", loc="left", fontweight="bold", fontsize=11)
adim = ["Ağı + bilyeleri kapsüle yerleştir",
        "Kapsülü ARKADAN namluya sok, çapraz pim yarıklara",
        "İki tetik pimini içeri it (kapsül kilitlendi)",
        "Bantları tek tek çekip çapraz pim uçlarına tak",
        "Atış: iki servo aynı anda → pimler dışarı → fırlat"]
y = 0.88
for i, a in enumerate(adim, 1):
    ax.text(0.01, y, f"{i}", fontsize=13, fontweight="bold", color=S1,
            transform=ax.transAxes)
    ax.text(0.07, y, a, fontsize=9.8, transform=ax.transAxes)
    y -= 0.165

fig.suptitle("LASTİK BANT TAHRİKLİ AĞ FIRLATICI — yay kaldırıldı, namlu 486 → 260 mm, "
             "kütle ~730 → ~300 g", fontsize=13.5, fontweight="bold", x=.025,
             ha="left", y=.962)
plt.savefig("out/cad_lastik.png", dpi=120)
print("-> out/cad_lastik.png")
