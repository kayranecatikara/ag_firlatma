# -*- coding: utf-8 -*-
"""Revize TETIK MEKANIZMASI gorseli: iki ayri pim, iki servo, ip tahrik."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, matplotlib, math
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from izdusum import ciz as izciz, kamera

S1, S2, S3 = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#d8d7d2"
GRI, CELIK = "#9a9a93", "#4a4a46"
plt.rcParams.update({"figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb",
                     "text.color": INK, "axes.labelcolor": INK, "font.size": 9.5})
D = np.load("cad/montaj_mesh.npz")

L_YAY, L_KAP, D_BORE, T_DUV = 160.0, 50.0, 43.4, 6.0
D_PIM, GIRINTI, BOSS_H = 5.0, 5.0, 10.0
Y_PIM = L_YAY - 0.5 * D_PIM
Rb, Ro = 0.5 * D_BORE, 0.5 * D_BORE + T_DUV
RENK = {"M_namlu": "#8fa3b8", "M_kapsul": S1, "M_pim_sag": S2, "M_pim_sol": S2}


def kirp(v, f, y0, y1, max_kenar=18.0):
    """y araligina kirpar; ayrica cok uzun ucgenleri atar (tesselasyon
    artefaktlarini temizler)."""
    m = (v[:, 1] >= y0) & (v[:, 1] <= y1)
    ok = m[f].all(1)
    tri = v[f[ok]]
    kenar = np.max(np.linalg.norm(
        tri[:, [1, 2, 0]] - tri, axis=2), axis=1)
    ok2 = kenar <= max_kenar
    ff = f[ok][ok2]
    idx = np.unique(ff)
    yeni = -np.ones(len(v), int); yeni[idx] = np.arange(len(idx))
    return v[idx], yeni[ff]


def kesit2d(ax, v, f, renk, zorder=2):
    vv = np.stack([v[:, 1], v[:, 0], v[:, 2]], 1)
    tri = vv[f]
    n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    ln = np.linalg.norm(n, axis=1, keepdims=True); ln[ln == 0] = 1
    kes = np.abs((n / ln)[:, 2]) > 0.98
    ax.add_collection(PolyCollection(tri[kes][:, :, :2], facecolors=renk,
                                     edgecolors=renk, linewidths=.3, zorder=zorder))


fig = plt.figure(figsize=(15.0, 8.6))
gs = fig.add_gridspec(2, 2, height_ratios=[1.05, 1], width_ratios=[1.5, 1],
                      hspace=.18, wspace=.10, left=.03, right=.985,
                      top=.885, bottom=.04)

# ---------------- (a) tetik istasyonu kesiti ---------------------------------
ax = fig.add_subplot(gs[0, 0])
kesit2d(ax, D["M_namlu_kv"], D["M_namlu_kf"], RENK["M_namlu"], zorder=1)
kesit2d(ax, D["M_kapsul_kv"], D["M_kapsul_kf"], S1, zorder=3)
for ad in ("M_pim_sag", "M_pim_sol"):
    vv = np.stack([D[ad + "_v"][:, 1], D[ad + "_v"][:, 0], D[ad + "_v"][:, 2]], 1)
    ax.scatter(vv[:, 0], vv[:, 1], s=.6, color=S2, zorder=6)
# yay
t = np.linspace(0, 44 * 2 * np.pi, 2000)
ax.plot(L_YAY * t / t[-1], 15 * np.cos(t), color=GRI, lw=1.6, zorder=2)
ax.plot([-6, 260], [0, 0], color=GRID, lw=1, ls="-.", zorder=0)

# ip + servo semasi
for sgn in (+1, -1):
    r_goz = Ro + BOSS_H + 3.0
    ax.plot([Y_PIM, Y_PIM - 30], [sgn * r_goz, sgn * (Ro + 14)], color=CELIK,
            lw=2.0, zorder=7)
    ax.add_patch(plt.Circle((Y_PIM - 30, sgn * (Ro + 14)), 5.5, fc="#d8d5cc",
                            ec=CELIK, lw=1.4, zorder=8))
    ax.add_patch(plt.Rectangle((Y_PIM - 43, sgn * (Ro + 3) if sgn > 0 else
                                sgn * (Ro + 25)), 26, 22, fc="#e6e3da",
                               ec=INK2, lw=1.2, zorder=5))
    ax.text(Y_PIM - 30, sgn * (Ro + 31), "SERVO", ha="center",
            va="center" if sgn > 0 else "center", fontsize=8.5,
            color=INK2, fontweight="bold", zorder=9)
    ax.annotate("", xy=(Y_PIM, sgn * (r_goz + 11)), xytext=(Y_PIM, sgn * r_goz),
                arrowprops=dict(arrowstyle="->", color=S2, lw=2.4), zorder=9)

ax.text(Y_PIM + 6, 46, "iki pim AYNI ANDA\nzıt yönde çekilir", fontsize=10,
        color=S2, fontweight="bold")
ax.annotate("pim ucu namluya\nsadece 5 mm girer\n(ortada BİRLEŞMEZ)",
            xy=(Y_PIM, Rb - 3), xytext=(Y_PIM + 22, -30), fontsize=9,
            color=INK, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=INK2, lw=1.2))
ax.annotate("kılavuz göbeği\n(pim eğilmez)", xy=(Y_PIM, Ro + 5),
            xytext=(Y_PIM + 46, 34), fontsize=9, color=INK2, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=INK2, lw=1.2))
ax.set_xlim(L_YAY - 80, L_YAY + 90); ax.set_ylim(-58, 58)
ax.set_aspect("equal"); ax.axis("off")
ax.set_title("(a) Tetik istasyonu — kesit", loc="left", fontweight="bold",
             fontsize=11.5)

# ---------------- (b) 3B tetik istasyonu -------------------------------------
ax = fig.add_subplot(gs[0, 1])
vn, fn = kirp(D["M_namlu_v"], D["M_namlu_f"], Y_PIM - 48, Y_PIM + 26)
izciz(ax, [(vn, fn, RENK["M_namlu"]),
           (D["M_pim_sag_v"], D["M_pim_sag_f"], S2),
           (D["M_pim_sol_v"], D["M_pim_sol_f"], S2)],
      elev=24, azim=-52)
ax.margins(.10)
ax.set_title("(b) 3B — göbekler + servo yatakları", loc="left",
             fontweight="bold", fontsize=11.5)

# ---------------- (c) kuvvet tablosu -----------------------------------------
ax = fig.add_subplot(gs[1, 0]); ax.axis("off")
sat = [("Kurulu yay kuvveti", "316 N", INK),
       ("Pim başına normal yük (2 pim)", "158 N", INK),
       ("Çekme kuvveti — kuru PETG (μ=0.30)", "47 N", S2),
       ("Çekme kuvveti — PTFE burçlu (μ=0.08)", "13 N", S3),
       ("MG996R @ r=10 mm makara", "108 N  ✓", S3),
       ("MG90S @ r=10 mm makara", "32 N  ✗", "#c0563a"),
       ("Pim kesme emniyeti (Ø5 çelik, çift kesme)", "50×", S3),
       ("PETG delik ezilme emniyeti", "19×", S3)]
y = 0.94
for a, b, c in sat:
    ax.text(0.01, y, a, fontsize=10, transform=ax.transAxes)
    ax.text(0.62, y, b, fontsize=10, fontweight="bold", color=c,
            transform=ax.transAxes)
    y -= 0.118
ax.set_title("(c) Kuvvetler ve servo seçimi", loc="left", fontweight="bold",
             fontsize=11.5)

# ---------------- (d) uyarilar -----------------------------------------------
ax = fig.add_subplot(gs[1, 1]); ax.axis("off")
ax.set_title("(d) Dikkat edilecekler", loc="left", fontweight="bold",
             fontsize=11.5)
notlar = [
    ("✓", "İki ayrı pim doğru karar — tek geçmeli çubukta bir uç\n"
          "   diğerinden önce boşalıyordu.", S3),
    ("~", "Senkron olmazsa 316 N tek pime biner → ~6 N·m moment.\n"
          "   Kamalar eğilmeyi 0.34° ile sınırlar, etkisi küçük.\n"
          "   Asıl risk bir servonun TAKILMASI — tek servo + rijit\n"
          "   bağlantı bunu da kaldırır.", INK2),
    ("!", "İp sadece ÇEKER. Pimleri geri sokmak için göbek içine\n"
          "   birer geri-getirme yayı gerekir.", S2),
    ("!", "Mikro servo yetmez — MG996R sınıfı kullanın,\n"
          "   makara yarıçapı ≤ 10 mm.", "#c0563a"),
]
y = 0.86
for im, mt, c in notlar:
    ax.text(0.01, y, im, fontsize=15, fontweight="bold", color=c,
            transform=ax.transAxes, va="top")
    ax.text(0.07, y, mt, fontsize=9.3, transform=ax.transAxes, va="top")
    y -= 0.245

fig.suptitle("TETİK MEKANİZMASI REVİZYONU — iki karşılıklı pim, iki servo, ip tahrik",
             fontsize=13.5, fontweight="bold", x=.03, ha="left", y=.96)
plt.savefig("out/cad_tetik.png", dpi=125)
print("-> out/cad_tetik.png")
