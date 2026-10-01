# -*- coding: utf-8 -*-
"""v2 (kisa namlu, omuzsuz) gorseli: dis gorunus, bant kesiti, tetik kesiti, ozet."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from izdusum import ciz as izciz

S1, S2, S3 = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#d8d7d2"
RENK = {"V2_namlu": "#8fa3b8", "V2_kapsul": S1, "V2_bilye": "#4a4a46",
        "V2_capraz_pim": "#7d7d76", "V2_bant_ust": S3, "V2_bant_alt": S3,
        "V2_pim_sag": S2, "V2_pim_sol": S2, "V2_kapak_sag": "#5f6f82",
        "V2_kapak_sol": "#5f6f82", "V2_tampon_ust": "#c0563a", "V2_tampon_alt": "#c0563a"}
plt.rcParams.update({"figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb",
                     "text.color": INK, "font.size": 9.5})
D = np.load("cad/v2_mesh.npz")
P = json.load(open("cad/v2_olcu.json"))
AD = list(RENK)


def kesit(ax, eksen, sirala):
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
                                         linewidths=.25, zorder=1 + k))


def ok(ax, xy, xyt, metin, renk=INK2, **kw):
    ax.annotate(metin, xy=xy, xytext=xyt, fontsize=9, color=renk, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=renk, lw=1.2), zorder=30, **kw)


fig = plt.figure(figsize=(15.5, 10.0))
gs = fig.add_gridspec(2, 3, height_ratios=[1, 1.1], width_ratios=[1.25, 1, 0.9],
                      hspace=.16, wspace=.06, left=.02, right=.985, top=.905, bottom=.03)

ax = fig.add_subplot(gs[0, :2])
izciz(ax, [(D[a + "_v"], D[a + "_f"], RENK[a]) for a in AD], elev=26, azim=-20)
ax.margins(.04)
ax.set_title("(a) Kurulu hâl — 2 lateks bant (yeşil) üst/alt, tetik kartuşları yanlarda",
             loc="left", fontweight="bold", fontsize=11)

ax = fig.add_subplot(gs[0, 2]); ax.axis("off")
ax.set_title("Özet (v2)", loc="left", fontweight="bold", fontsize=11)
sat = [("Namlu boyu", f"{P['L_namlu']:.1f} mm  (v1: 260)"),
       ("Strok", f"{P['STROK']:.0f} mm"),
       ("Kapsül", f"{P['L_kapsul']:.0f} mm  (v1: 50)"),
       ("Bant", f"2 × Ø16/4 lateks, ×{P['lam']:.0f}"),
       ("Kurma kuvveti", "668 N  (334 N / pim)"),
       ("Çıkış hızı", "24.4 m/s"),
       ("Atış penceresi", "2.44 – 4.02 m"),
       ("Durdurma", "çapraz pim → yarık sonu\n(TPU tampon)"),
       ("Ağız", f"{P['koni_acisi']:.0f}° ıraksak koni,\nomuz YOK")]
y = 0.93
for a, b in sat:
    ax.text(0.0, y, a, fontsize=9.5, color=INK2, transform=ax.transAxes, va="top")
    ax.text(0.40, y, b, fontsize=9.5, fontweight="bold", transform=ax.transAxes, va="top")
    y -= 0.105 if "\n" not in b else 0.15

ax = fig.add_subplot(gs[1, :2])
kesit(ax, "x", ["V2_namlu", "V2_kapsul", "V2_capraz_pim", "V2_bant_ust", "V2_bant_alt",
                "V2_tampon_ust", "V2_tampon_alt"])
L = P["L_namlu"]
ax.plot([-4, L + 6], [0, 0], color=GRID, lw=1, ls="-.", zorder=0)
for s in (+1, -1):
    ax.annotate("", xy=(P["y_capraz1"] - 4, s * P["r_bant"]),
                xytext=(P["y_capraz0"] + 18, s * P["r_bant"]),
                arrowprops=dict(arrowstyle="->", color=S3, lw=2.2), zorder=31)
ok(ax, (P["y_capraz0"], -33), (18, -56), "çapraz pim\n(bant buraya)", INK)
ok(ax, (P["y_capraz1"] + 4, -25), (80, -60), "yarık sonu + TPU tampon\n= DURDURMA", "#c0563a")
ok(ax, (P["y_yuz_dur"] + 6, -24), (150, -56), "ıraksak koni\n(omuz yok)", S1)
ok(ax, (P["y_ankraj"], 33), (118, 52), "bant ankraj pimi", INK2)
ax.annotate("", xy=(P["y_yuz_dur"] - P["L_kapsul"] + P["STROK"], -70),
            xytext=(P["y_yuz_dur"] - P["L_kapsul"], -70),
            arrowprops=dict(arrowstyle="<->", color=S1, lw=1.4))
ax.text(P["arka"] + P["L_kapsul"] / 2 + P["STROK"] / 2, -77, f"STROK {P['STROK']:.0f} mm",
        ha="center", fontsize=9, color=S1, fontweight="bold")
ax.annotate("", xy=(L, -86), xytext=(0, -86), arrowprops=dict(arrowstyle="<->", color=INK, lw=1.2))
ax.text(L / 2, -93, f"namlu {L:.1f} mm   (arka açık = yükleme ağzı)", ha="center", fontsize=9)
ax.set_xlim(-6, L + 8); ax.set_ylim(-98, 62); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("(b) Bant düzlemi kesiti", loc="left", fontweight="bold", fontsize=11)

ax = fig.add_subplot(gs[1, 2])
kesit(ax, "z", ["V2_namlu", "V2_kapsul", "V2_pim_sag", "V2_pim_sol", "V2_kapak_sag", "V2_kapak_sol"])
yt = P["y_tetik"]
ax.plot([-3, 60], [0, 0], color=GRID, lw=1, ls="-.", zorder=0)
for s in (+1, -1):
    ax.annotate("", xy=(yt, s * 56), xytext=(yt, s * 48),
                arrowprops=dict(arrowstyle="->", color=S2, lw=2.2), zorder=31)
ok(ax, (yt, 18), (26, 10), "pim, kapsül\nkanalında", INK)
ok(ax, (yt + 4, 31.5), (28, 30), "Ø5 mil\nbileziği", INK2)
ok(ax, (yt, -40), (28, -46), "yay boşluğu\n(Ø10.6)", INK2)
ok(ax, (yt, 45.5), (28, 52), "kapak (M2)", INK2)
ax.set_xlim(-3, 62); ax.set_ylim(-60, 60); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("(c) Tetik kartuşu kesiti", loc="left", fontweight="bold", fontsize=11)

fig.suptitle("AĞ FIRLATICI NAMLU v2 — kısa namlu, omuzsuz, lastik bant tahrikli",
             fontsize=13.5, fontweight="bold", x=.02, ha="left", y=.965)
plt.savefig("out/cad_v2.png", dpi=120)
print("-> out/cad_v2.png")
