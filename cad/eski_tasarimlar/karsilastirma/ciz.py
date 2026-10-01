# -*- coding: utf-8 -*-
"""Eski / yeni parca karsilastirma gorselleri.

CAD'de namlu ekseni +Y. Cizimde ekseni ekranin yatayina (+X) tasimak icin
(x,y,z)_cad -> (y, x, z)_cizim donusumu uygulanir.
"""
import numpy as np, matplotlib, math
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

S1, S2, INK, INK2, GRID = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e", "#d8d7d2"
KIRMIZI = "#c0563a"
plt.rcParams.update({"figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb",
                     "text.color": INK, "axes.labelcolor": INK, "font.size": 9})
D = np.load("cad/mesh.npz")


def don(v):
    """CAD (x,y,z) -> cizim (y,x,z): namlu ekseni yatay."""
    return np.stack([v[:, 1], v[:, 0], v[:, 2]], 1)


def ciz3d(ax, v, f, renk, elev, azim, isik=(0.55, 0.45, 0.70), zoom=0.60):
    v = don(v); tri = v[f]
    n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    ln = np.linalg.norm(n, axis=1, keepdims=True); ln[ln == 0] = 1
    n = n / ln
    L = np.array(isik, float); L /= np.linalg.norm(L)
    sh = np.clip(np.abs(n @ L), 0, 1) * 0.62 + 0.38
    base = np.array(matplotlib.colors.to_rgb(renk))
    ax.add_collection3d(Poly3DCollection(tri, facecolors=np.clip(base * sh[:, None], 0, 1),
                                         edgecolors="none", linewidths=0))
    c = v.mean(0); r = np.abs(v - c).max() * zoom
    ax.set_xlim(c[0] - r, c[0] + r); ax.set_ylim(c[1] - r, c[1] + r)
    ax.set_zlim(c[2] - r, c[2] + r)
    ax.set_box_aspect((1, 1, 1)); ax.view_init(elev, azim); ax.set_axis_off()


def kesit2d(ax, v, f, renk, etiket=None):
    """z=0 kesitini (y_cad, x_cad) duzleminde 2B doldurarak cizer."""
    v = don(v); tri = v[f]
    n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    ln = np.linalg.norm(n, axis=1, keepdims=True); ln[ln == 0] = 1
    kesit = np.abs((n / ln)[:, 2]) > 0.98          # z-normalli yuzler = kesit yuzeyi
    from matplotlib.collections import PolyCollection
    ax.add_collection(PolyCollection(tri[kesit][:, :, :2], facecolors=renk,
                                     edgecolors=renk, linewidths=.3))
    ax.autoscale_view(); ax.set_aspect("equal")


# ============================== SEKIL 1: KAPSUL ==============================
fig = plt.figure(figsize=(15.0, 8.8))
gs = fig.add_gridspec(2, 3, width_ratios=[1.0, 1.15, 1.25],
                      hspace=.06, wspace=.05, left=.01, right=.99,
                      top=.885, bottom=.04)

for k, (ad, renk, bas) in enumerate([
        ("kapsul_ESKI_0deg", KIRMIZI, "MEVCUT  —  yuva ekseni 0° (paralel)"),
        ("kapsul_YENI_18deg", S1,      "REVİZE  —  yuva ekseni 18° (ıraksak)")]):
    ax = fig.add_subplot(gs[k, 0], projection='3d')
    ciz3d(ax, D[ad + "_v"], D[ad + "_f"], renk, elev=24, azim=-38, zoom=.56)
    ax.set_title(bas, fontsize=11, fontweight="bold", color=renk, y=.92)
    ax.text2D(.5, .02, "ön yüz (bilye yuvaları)", transform=ax.transAxes,
              ha="center", fontsize=8.5, color=INK2)

    ax = fig.add_subplot(gs[k, 1])
    kesit2d(ax, D[ad + "_kv"], D[ad + "_kf"], renk)
    a = math.radians(0 if k == 0 else 18)
    for sgn in (+1, -1):
        y0, x0 = 50.0, sgn * 13.5
        ax.arrow(y0, x0, 26 * math.cos(a), 26 * math.sin(a) * sgn,
                 head_width=2.2, head_length=4.5, fc=renk, ec=renk, lw=2,
                 length_includes_head=True, zorder=5)
    ax.plot([0, 86], [0, 0], color=GRID, lw=1, ls="-.")
    ax.set_xlim(-4, 88); ax.set_ylim(-30, 30); ax.axis("off")
    ax.set_title("kesit — yuva ekseni", fontsize=9.5, color=INK2, y=.93)

# --- sag sutun: kavram semasi -------------------------------------------------
ax = fig.add_subplot(gs[:, 2])
L, Rb, Rp, a = 50, 21.7, 13.5, math.radians(18)
ax.add_patch(plt.Rectangle((-Rb, 0), 2 * Rb, L, fc="#eceae4", ec=GRID, lw=1.2))
ax.plot([0, 0], [-4, L + 60], color=GRID, lw=1, ls="-.")
ax.text(2, L + 56, "namlu ekseni", fontsize=8, color=INK2)
for sgn in (+1, -1):
    x0 = sgn * Rp
    ax.arrow(x0, L, 0, 46, head_width=2.6, head_length=5, fc=KIRMIZI,
             ec=KIRMIZI, lw=2.2, length_includes_head=True)
    ax.arrow(x0, L, math.sin(a) * 50 * sgn, math.cos(a) * 50, head_width=2.6,
             head_length=5, fc=S1, ec=S1, lw=2.2, length_includes_head=True)
    ax.add_patch(plt.Circle((x0, L - 2), 6.45, fc="#b9c7d8", ec=INK2, lw=1))
th = np.linspace(np.pi / 2 - a, np.pi / 2, 40)
ax.plot(Rp + 27 * np.cos(th), L + 27 * np.sin(th), color=INK2, lw=1.2)
ax.text(Rp + 17, L + 32, "18°", fontsize=14, fontweight="bold", color=S1)
ax.text(-Rp - 4, L + 50, "MEVCUT\n(paralel)", ha="right", fontsize=9.5,
        fontweight="bold", color=KIRMIZI)
ax.text(Rp + 32, L + 44, "REVİZE\n(ıraksak)", ha="left", fontsize=9.5,
        fontweight="bold", color=S1)
ax.annotate("", xy=(-Rp, L - 22), xytext=(Rp, L - 22),
            arrowprops=dict(arrowstyle="<->", color=INK2, lw=1.1))
ax.text(0, L - 30, f"bölme çemberi Ø{2 * Rp:.0f} mm", ha="center", fontsize=8.5,
        color=INK2)
ax.text(0, 8, "ağ haznesi", ha="center", fontsize=9.5, color=INK2)
ax.set(xlim=(-76, 76), ylim=(-16, L + 72)); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("“Koniklendirme” ne demek?\nBilye yuvalarının EKSENİ dışa eğiliyor",
             fontsize=11.5, fontweight="bold", y=.97)
ax.text(0, -6, "Yuva ekseni eğik olunca bilyeler ıraksak çıkar →\n"
               "radyal hız doğar → ağ açılır.\n"
               "Paralel çıkarsa radyal hız SIFIR, ağ HİÇ açılmaz.",
        ha="center", va="top", fontsize=9, color=INK2)

fig.suptitle("AĞ KAPSÜLÜ REVİZYONU  —  kritik değişiklik: bilye yuvası koniklendirmesi",
             fontsize=13.5, fontweight="bold", x=.012, ha="left", y=.965)
plt.savefig("out/cad_kapsul.png", dpi=125)
print("-> out/cad_kapsul.png")

# ============================== SEKIL 2: NAMLU AGZI ==========================
fig = plt.figure(figsize=(14.0, 7.4))
gs = fig.add_gridspec(2, 2, hspace=.06, wspace=.04, left=.01, right=.99,
                      top=.87, bottom=.04)
for k, (ad, renk, bas) in enumerate([
        ("namlu_agiz_ESKI", KIRMIZI, "MEVCUT  —  düz delik, yiv yok, ağız düz"),
        ("namlu_agiz_YENI", S1,      "REVİZE  —  6 helis yiv (730 mm/tur) + 18° ıraksak ağız")]):
    ax = fig.add_subplot(gs[k, 0], projection='3d')
    ciz3d(ax, D[ad + "_v"], D[ad + "_f"], renk, elev=20, azim=-40, zoom=.58)
    ax.set_title(bas, fontsize=11, fontweight="bold", color=renk, y=.94)
    ax = fig.add_subplot(gs[k, 1])
    kesit2d(ax, D[ad + "_kv"], D[ad + "_kf"], renk)
    ax.plot([-6, 104], [0, 0], color=GRID, lw=1, ls="-.")
    ax.set_xlim(-6, 104); ax.set_ylim(-46, 46); ax.axis("off")
    if k == 1:
        ax.annotate("ıraksak ağız konisi 18°", xy=(86, 26), xytext=(30, 40),
                    fontsize=9.5, color=S1, fontweight="bold",
                    arrowprops=dict(arrowstyle="->", color=S1, lw=1.3))
        ax.annotate("durdurma omuzu", xy=(66, -22), xytext=(14, -40),
                    fontsize=9.5, color=S1, fontweight="bold",
                    arrowprops=dict(arrowstyle="->", color=S1, lw=1.3))
        ax.annotate("helis yiv kanalı", xy=(30, 23), xytext=(4, 40),
                    fontsize=9.5, color=S1, fontweight="bold",
                    arrowprops=dict(arrowstyle="->", color=S1, lw=1.3))
    ax.set_title("kesit", fontsize=9.5, color=INK2, y=.93)
fig.suptitle("NAMLU AĞIZ BÖLÜMÜ REVİZYONU  —  helis yiv + ıraksak ağız + durdurma omuzu",
             fontsize=13.5, fontweight="bold", x=.012, ha="left", y=.955)
plt.savefig("out/cad_namlu.png", dpi=125)
print("-> out/cad_namlu.png")
