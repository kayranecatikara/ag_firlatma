# -*- coding: utf-8 -*-
"""SISTEM REHBERI — calisma prensibi + angajman + performans ozeti."""
import sys, os, json
sys.path.insert(0, '/home/kayra/Masaüstü/ag_firlatma')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle

S1, S2, S3 = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#d8d7d2"
KIRMIZI = "#c0563a"
plt.rcParams.update({"figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb",
                     "text.color": INK, "axes.labelcolor": INK,
                     "xtick.color": INK2, "ytick.color": INK2,
                     "axes.edgecolor": GRID, "grid.color": GRID, "font.size": 9.5})

import run_menzil_nihai as M
t, L = M.kur()
ts, Z, R = M.yol(t, L, T=0.6)
tw, Zw, Rw, i = M.ilk_cevrim(ts, Z, R)
lo, hi = M.pencere_bagil(tw, Zw, Rw, 0.0)
V100 = 100 / 3.6

fig = plt.figure(figsize=(16.0, 10.0))
gs = fig.add_gridspec(3, 3, height_ratios=[0.92, 1, 1], hspace=.42, wspace=.26,
                      left=.05, right=.98, top=.90, bottom=.06)

# ================= (a) CALISMA PRENSIBI — 4 asama =========================
ax = fig.add_subplot(gs[0, :]); ax.axis("off")
ax.set_xlim(0, 100); ax.set_ylim(0, 26)
ax.set_title("(a) ÇALIŞMA PRENSİBİ", loc="left", fontweight="bold", fontsize=12)
asama = [
    (2,  "1. KURULU", "4 bant gergin (×4)\n1200 N · 2 pim tutuyor", S1),
    (26, "2. ATIŞ", "Servolar pimleri çeker\nkapsül 114 mm hızlanır", S2),
    (50, "3. DURMA", "Çapraz pim yarık sonuna\nçarpar · 34.5 m/s", KIRMIZI),
    (74, "4. AÇILMA", "6 bilye 13° ıraksak çıkar\nağ 192 ms'de Ø2.15 m", S3),
]
for x, bas, det, renk in asama:
    ax.add_patch(FancyBboxPatch((x, 3), 21, 18, boxstyle="round,pad=0.6",
                                fc="white", ec=renk, lw=2))
    ax.text(x + 10.5, 17.5, bas, ha="center", fontsize=11, fontweight="bold", color=renk)
    ax.text(x + 10.5, 9.5, det, ha="center", fontsize=9.2, color=INK, linespacing=1.6)
    if x < 74:
        ax.annotate("", xy=(x + 24.5, 12), xytext=(x + 21.5, 12),
                    arrowprops=dict(arrowstyle="-|>", color=INK2, lw=2.2))

# ================= (b) ANGAJMAN SEMASI ====================================
ax = fig.add_subplot(gs[1, :2])
ax.set_xlim(-1.4, 9.8); ax.set_ylim(-3.3, 2.4); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("(b) ANGAJMAN — ikisi de 100 km/h, aynı yön (takip)", loc="left",
             fontweight="bold", fontsize=12)
# drone (tail-sitter)
ax.add_patch(Rectangle((-1.0, -0.22), 1.0, 0.44, fc="#8fa3b8", ec=INK2, lw=1.2))
ax.plot([-0.75, -0.75], [-0.75, 0.75], color="#8fa3b8", lw=3)
ax.text(-0.5, -0.95, "DRONE\n100 km/h", ha="center", fontsize=9, fontweight="bold",
        color=INK, va="top")
ax.add_patch(Rectangle((0.0, -0.10), 0.5, 0.20, fc=S1, ec=INK2, lw=1))
ax.text(0.25, 0.42, "namlu", ha="center", fontsize=8, color=S1, fontweight="bold")
# pencere
ax.add_patch(Rectangle((lo, -1.18), hi - lo, 2.36, fc=S3, alpha=.16, ec="none"))
ax.annotate("", xy=(hi, 1.45), xytext=(lo, 1.45),
            arrowprops=dict(arrowstyle="<->", color="#0f6e4c", lw=2))
ax.text((lo + hi) / 2, 1.62, f"ATIŞ PENCERESİ  {lo:.1f} – {hi:.1f} m", ha="center",
        fontsize=10.5, fontweight="bold", color="#0f6e4c")
# ag konileri
for d, al in ((1.8, .30), (3.6, .55), (Zw[i], 1.0)):
    j = np.argmin(abs(Zw - d))
    ax.plot([d, d], [-Rw[j], Rw[j]], color=S1, lw=2.4, alpha=al,
            solid_capstyle="round")
    ax.plot(d, Rw[j], "o", color=S1, ms=5, alpha=al)
    ax.plot(d, -Rw[j], "o", color=S1, ms=5, alpha=al)
ax.text(Zw[i], Rw[i] + 0.16, f"ağ Ø{2*Rw[i]:.2f} m", ha="center", fontsize=9,
        color=S1, fontweight="bold")
# hedef
hx = 6.9
ax.plot([hx, hx], [-0.859, 0.859], color=KIRMIZI, lw=4, solid_capstyle="round")
ax.add_patch(Rectangle((hx - 0.28, -0.11), 0.56, 0.22, fc=KIRMIZI, ec="none"))
ax.text(hx + 0.45, 0.30, "TALON\n1718 mm kanat\n100 km/h", ha="left", fontsize=9,
        fontweight="bold", color=KIRMIZI, va="center")
ax.annotate("", xy=(hx - 0.22, 0.859), xytext=(hx - 0.22, 0.0),
            arrowprops=dict(arrowstyle="<->", color=KIRMIZI, lw=1.2))
ax.text(hx - 0.34, 0.43, "0.86 m\ngereken", fontsize=8, color=KIRMIZI, ha="right",
        va="center")
ax.annotate("", xy=(9.4, -2.30), xytext=(0.2, -2.30),
            arrowprops=dict(arrowstyle="->", color=INK2, lw=1.4))
ax.text(4.8, -3.10, "drone'a göre mesafe [m]", ha="center", fontsize=9, color=INK2)
for xx in range(1, 10):
    ax.plot([xx, xx], [-2.38, -2.22], color=INK2, lw=1)
    ax.text(xx, -2.66, str(xx), ha="center", fontsize=8, color=INK2, va="center")

# ================= (c) PERFORMANS KARTI ===================================
ax = fig.add_subplot(gs[1, 2]); ax.axis("off")
ax.set_title("(c) PERFORMANS", loc="left", fontweight="bold", fontsize=12)
kart = [("Atış penceresi", f"{lo:.2f} – {hi:.2f} m", S3),
        ("Tetikleme", f"{(lo+hi)/2:.1f} m", S3),
        ("Çıkış hızı", f"{L['v_exit']:.1f} m/s", INK),
        ("Ağ en açık", f"Ø{2*Rw[i]:.2f} m @ {Zw[i]:.1f} m", INK),
        ("Açılma süresi", f"{tw[i]*1e3:.0f} ms", INK),
        ("Yakalama ±25 cm", "%82", S2),
        ("Yakalama ±10 cm", "%95", S3),
        ("Kurma", "4 × 31 kg", INK),
        ("Toplam kütle", "469 g", INK)]
y = 0.95
for a, b, c in kart:
    ax.text(0.0, y, a, fontsize=9.3, color=INK2, transform=ax.transAxes)
    ax.text(1.0, y, b, fontsize=9.8, fontweight="bold", color=c, ha="right",
            transform=ax.transAxes)
    y -= 0.108

# ================= (d) AG =================================================
ax = fig.add_subplot(gs[2, 0])
ax.set_aspect("equal"); ax.axis("off")
ax.set_title("(d) AĞ — Ø2.80 m altıgen, göz 140 mm", loc="left",
             fontweight="bold", fontsize=11.5)
Rn, gz = 1.4, 0.14
th = np.linspace(0, 2 * np.pi, 7)
ax.fill(Rn * np.cos(th), Rn * np.sin(th), fc="#eef3f9", ec=S1, lw=2)
alt = plt.Polygon(np.c_[Rn * np.cos(th), Rn * np.sin(th)], closed=True,
                  fc="none", ec="none")
ax.add_patch(alt)
for v in np.arange(-Rn, Rn + gz, gz):
    l1, = ax.plot([v, v], [-Rn, Rn], color=S1, lw=.55, alpha=.55)
    l2, = ax.plot([-Rn, Rn], [v, v], color=S1, lw=.55, alpha=.55)
    l1.set_clip_path(alt); l2.set_clip_path(alt)
for k in range(6):
    ax.plot(Rn * np.cos(th[k]), Rn * np.sin(th[k]), "o", color="#4a4a46", ms=9,
            zorder=5)
ax.add_patch(Circle((0, 0), 0.115, fc=KIRMIZI, alpha=.5, ec=KIRMIZI, lw=1.5))
ax.text(0, -0.30, "pervane\nØ230", ha="center", fontsize=8, color=KIRMIZI,
        fontweight="bold")
ax.annotate("", xy=(Rn, -1.62), xytext=(-Rn, -1.62),
            arrowprops=dict(arrowstyle="<->", color=INK2, lw=1.2))
ax.text(0, -1.80, "2.80 m (köşe-köşe)", ha="center", fontsize=8.5, color=INK2)
ax.text(Rn * 1.02, Rn * 0.62, "6 bilye\nØ12.7 kurşun", fontsize=8.5,
        color="#4a4a46", fontweight="bold")
ax.set_xlim(-1.75, 2.35); ax.set_ylim(-1.95, 1.7)

# ================= (e) SURUKLEME ==========================================
ax = fig.add_subplot(gs[2, 1])
ts0, Z0, R0 = M.yol(t, L, T=0.6, aero=0.0)
ax.plot(ts0 * 1e3, Z0, color=INK2, lw=1.8, ls="--", label="havasız olsaydı")
ax.plot(ts * 1e3, Z, color=S1, lw=2.4, label="gerçek")
ax.fill_between(ts * 1e3, Z, np.interp(ts, ts0, Z0), color=S2, alpha=.15)
j = np.argmin(abs(ts - .25))
ax.annotate(f"{np.interp(.25, ts0, Z0)-Z[j]:.1f} m\ngeri", xy=(250, (Z[j] + np.interp(.25, ts0, Z0)) / 2),
            xytext=(285, 3.0), fontsize=9, color=S2, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=S2, lw=1.2))
ax.axhspan(lo, hi, color=S3, alpha=.13, lw=0)
ax.set(xlabel="zaman [ms]", ylabel="ileri mesafe [m]", ylim=(0, 10))
ax.set_title("(e) Hava sürüklemesi", loc="left", fontweight="bold", fontsize=11.5)
ax.legend(fontsize=8.5, frameon=False, loc="upper left"); ax.grid(alpha=.3)

# ================= (f) KAPANMA HIZI ======================================
ax = fig.add_subplot(gs[2, 2])
kmh = np.array([100, 110, 120, 130])
alt = np.array([3.56, 3.86, 4.18, 4.50]); ust = np.array([5.76, 6.22, 6.66, 7.06])
ax.fill_between(kmh, alt, ust, color=S3, alpha=.22, lw=0)
ax.plot(kmh, ust, "-o", color=S1, lw=2.2, ms=5, label="en uzak")
ax.plot(kmh, alt, "-s", color=S2, lw=2.2, ms=5, label="en yakın")
ax.set(xlabel="drone hızı [km/h]  (hedef 100)", ylabel="tetikleme [m]", ylim=(0, 8))
ax.set_title("(f) Kapanırsanız pencere uzar", loc="left", fontweight="bold",
             fontsize=11.5)
ax.legend(fontsize=8.5, frameon=False, loc="lower right"); ax.grid(alpha=.3)

fig.suptitle("AĞ FIRLATMA SİSTEMİ v4 — GENEL BAKIŞ", fontsize=14,
             fontweight="bold", x=.05, ha="left", y=.965)
plt.savefig("out/REHBER_sistem.png", dpi=120)
print(f"-> out/REHBER_sistem.png  (pencere {lo:.2f}-{hi:.2f} m)")
