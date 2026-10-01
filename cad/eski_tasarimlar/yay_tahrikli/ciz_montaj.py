# -*- coding: utf-8 -*-
"""TAM MONTAJ gorseli: dis gorunus, boyuna kesit, agiz detayi, yerlesim semasi."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, matplotlib, math
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from izdusum import ciz as izciz
from matplotlib.collections import PolyCollection
sys_path_hack = None

S1, S2, S3 = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#d8d7d2"
GRI = "#9a9a93"
plt.rcParams.update({"figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb",
                     "text.color": INK, "axes.labelcolor": INK, "font.size": 9})
D = np.load("cad/montaj_mesh.npz")

# montaj.py ile ayni yerlesim
L_YAY, L_KAP, STROK, L_OMUZ, L_KONI = 160.0, 50.0, 250.0, 4.0, 22.0
Y_OMUZ = L_YAY + L_KAP + STROK
L_NAM = Y_OMUZ + L_OMUZ + L_KONI
D_YAY, N_SAR, D_TEL = 30.0, 44.0, 3.5

RENK = {"M_namlu": "#8fa3b8", "M_kapsul": S1, "M_bilye": "#4a4a46",
        "M_pim_sag": S2, "M_pim_sol": S2}


def don(v):
    return np.stack([v[:, 1], v[:, 0], v[:, 2]], 1)      # CAD(x,y,z) -> (y,x,z)


def ciz3d(ax, v, f, renk, alpha=1.0, isik=(0.5, 0.5, 0.7)):
    v = don(v); tri = v[f]
    n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    ln = np.linalg.norm(n, axis=1, keepdims=True); ln[ln == 0] = 1
    L = np.array(isik, float); L /= np.linalg.norm(L)
    sh = np.clip(np.abs((n / ln) @ L), 0, 1) * 0.60 + 0.40
    base = np.array(matplotlib.colors.to_rgb(renk))
    ax.add_collection3d(Poly3DCollection(tri, facecolors=np.clip(base * sh[:, None], 0, 1),
                                         edgecolors="none", alpha=alpha))


def yay_helis(y0=0.0, L=L_YAY, n=N_SAR, R=0.5 * D_YAY, N=2400):
    t = np.linspace(0, n * 2 * np.pi, N)
    return y0 + L * t / t[-1], R * np.cos(t), R * np.sin(t)


def kesit2d(ax, v, f, renk, zorder=2):
    v = don(v); tri = v[f]
    n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    ln = np.linalg.norm(n, axis=1, keepdims=True); ln[ln == 0] = 1
    kes = np.abs((n / ln)[:, 2]) > 0.98
    ax.add_collection(PolyCollection(tri[kes][:, :, :2], facecolors=renk,
                                     edgecolors=renk, linewidths=.3, zorder=zorder))


fig = plt.figure(figsize=(16.0, 10.4))
gs = fig.add_gridspec(3, 2, height_ratios=[1.15, 0.95, 0.85],
                      width_ratios=[1.35, 1], hspace=.20, wspace=.06,
                      left=.035, right=.985, top=.905, bottom=.045)

# ---------------- (a) dis gorunus 3B -----------------------------------------
ax = fig.add_subplot(gs[0, :])
izciz(ax, [(D["M_namlu_v"], D["M_namlu_f"], RENK["M_namlu"]),
           (D["M_pim_sag_v"], D["M_pim_sag_f"], RENK["M_pim_sag"]),
           (D["M_pim_sol_v"], D["M_pim_sol_f"], RENK["M_pim_sol"])],
      elev=17, azim=-22)
ax.margins(.06)
ax.set_title("(a) Dış görünüş — 6 helis yiv (730 mm/tur), ıraksak ağız, tetik pimi delikleri",
             loc="left", fontweight="bold", fontsize=11, y=.94)

# ---------------- (b) boyuna kesit -------------------------------------------
ax = fig.add_subplot(gs[1, :])
kesit2d(ax, D["M_namlu_kv"], D["M_namlu_kf"], RENK["M_namlu"], zorder=1)
kesit2d(ax, D["M_kapsul_kv"], D["M_kapsul_kf"], S1, zorder=3)
vb = don(D["M_bilye_v"])
for i in range(6):
    pass
ax.scatter(vb[:, 0], vb[:, 1], s=.05, color="#4a4a46", zorder=4)
yy, yx, yz = yay_helis()
ax.plot(yy, yx, color=GRI, lw=2.0, zorder=2, solid_capstyle="round")
for th in (1, -1):
    ax.plot([L_YAY - 6, L_YAY - 6], [th * 22, th * 34], color=S2, lw=5,
            solid_capstyle="round", zorder=5)
ax.plot([-10, L_NAM + 10], [0, 0], color=GRID, lw=1, ls="-.", zorder=0)

def ok(x0, x1, y, metin, renk=INK2, dy=4):
    ax.annotate("", xy=(x1, y), xytext=(x0, y),
                arrowprops=dict(arrowstyle="<->", color=renk, lw=1.2))
    ax.text((x0 + x1) / 2, y + dy, metin, ha="center", fontsize=8.5, color=renk)

ok(0, L_YAY, -40, f"yay (kurulu) {L_YAY:.0f} mm")
ok(L_YAY, L_YAY + L_KAP, -40, f"kapsül {L_KAP:.0f}")
ok(L_YAY + L_KAP, Y_OMUZ, -40, f"STROK {STROK:.0f} mm", S1)
ok(0, L_NAM, -56, f"namlu {L_NAM:.0f} mm", INK, dy=-11)
ax.annotate("tetik pimleri\n(servolar çeker)", xy=(L_YAY - 6, 30), xytext=(L_YAY - 96, 52),
            fontsize=9, color=S2, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=S2, lw=1.3))
ax.annotate("durdurma omuzu", xy=(Y_OMUZ + 2, -19), xytext=(Y_OMUZ - 170, -52),
            fontsize=9, color=S1, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=S1, lw=1.3))
ax.annotate("ıraksak ağız 18°", xy=(L_NAM - 4, 27), xytext=(L_NAM - 125, 56),
            fontsize=9, color=S1, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=S1, lw=1.3))
ax.set_xlim(-24, L_NAM + 24); ax.set_ylim(-70, 70); ax.axis("off")
ax.set_title("(b) Boyuna kesit — kurulu hâl", loc="left", fontweight="bold",
             fontsize=11, y=.96)

# ---------------- (c) agiz detayi 3B -----------------------------------------
ax = fig.add_subplot(gs[2, 0])
vk = D["M_kapsul_v"].copy(); vk[:, 1] += STROK
vb = D["M_bilye_v"].copy();  vb[:, 1] += STROK
izciz(ax, [(vk, D["M_kapsul_f"], RENK["M_kapsul"]),
           (vb, D["M_bilye_f"],  RENK["M_bilye"])],
      elev=20, azim=64)
# namlu agzinin konumu (referans cember)
th = np.linspace(0, 2*np.pi, 160)
from izdusum import kamera
dcam, rcam, ucam = kamera(20, 64)
for yy, RR, st in [(Y_OMUZ, 21.7, "-"), (L_NAM, 28.8, "--")]:
    P3 = np.stack([RR*np.cos(th), np.full_like(th, yy), RR*np.sin(th)], 1)
    ax.plot(P3 @ rcam, P3 @ ucam, st, color=GRI, lw=1.1, zorder=0)
ax.text(*(np.array([0., L_NAM, 36.]) @ np.stack([rcam, ucam], -1)), "namlu ağzı",
        fontsize=8.5, color=INK2, ha="center", va="bottom")
ax.margins(.12)
ax.set_title("(c) Ağız detayı — kapsül omuza dayanmış, bilyeler çıkışa hazır",
             loc="left", fontweight="bold", fontsize=10.5, y=.97)

# ---------------- (d) kutle / ozet -------------------------------------------
ax = fig.add_subplot(gs[2, 1]); ax.axis("off")
satir = [("Namlu (PETG, %40 dolgu)", "299 g"),
         ("Yay (Ø3.5 tel, Ø30, 44 sarım)", "335 g"),
         ("Kapsül (PETG)", "23 g"),
         ("6 × Ø12.9 mm çelik bilye", "52 g"),
         ("Ağ (Ø3.0 m, göz 78 mm, Dyneema Ø0.16)", "5 g"),
         ("Tetik pimleri (2 × Ø5 çelik)", "10 g"),
         ("TOPLAM", "728 g")]
y = 0.95
for k, (a, b) in enumerate(satir):
    kal = "bold" if a == "TOPLAM" else "normal"
    if a == "TOPLAM":
        ax.plot([0.02, 0.98], [y + .045, y + .045], color=GRID, lw=1,
                transform=ax.transAxes)
    ax.text(0.02, y, a, fontsize=9.5, fontweight=kal, transform=ax.transAxes)
    ax.text(0.98, y, b, fontsize=9.5, fontweight=kal, ha="right",
            transform=ax.transAxes)
    y -= 0.115
ax.text(0.02, y - .02, "Kurma kuvveti 316 N · çıkış hızı ~20 m/s\n"
                       "Geri tepme 1.1 N·s → 8 kg dronede 0.14 m/s",
        fontsize=9, color=INK2, transform=ax.transAxes, va="top")
ax.set_title("(d) Kütle dökümü", loc="left", fontweight="bold", fontsize=10.5)

fig.suptitle("AĞ FIRLATMA MEKANİZMASI — TAM MONTAJ  (revize: konik yuva + helis yiv + ıraksak ağız)",
             fontsize=13.5, fontweight="bold", x=.035, ha="left", y=.968)
plt.savefig("out/cad_montaj.png", dpi=120)
print("-> out/cad_montaj.png")
