import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                if os.path.basename(os.path.dirname(os.path.abspath(__file__))) == "cad"
                else os.path.dirname(os.path.abspath(__file__)))
from agsim.yollar import vyol, kyol
# -*- coding: utf-8 -*-
"""MONTAJ REHBERI GORSELI — patlatilmis gorunum + parca yerlesimi.

Hangi parca nereye gidiyor, hangi malzemeden, kac adet.
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from izdusum import ciz as izciz, kamera

S1, S2, S3 = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#d8d7d2"
CELIK, ALU, TPU = "#4a4a46", "#9aa3ad", "#c0563a"
plt.rcParams.update({"figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb",
                     "text.color": INK, "font.size": 9.5})
D = np.load(vyol(__file__, "cad", "v4_mesh.npz"))
P = json.load(open(vyol(__file__, "cad", "v4_olcu.json")))

# parca -> (renk, patlatma vektoru [mm], etiket, malzeme/adet)
PARCA = {
    "V4_namlu":      ("#8fa3b8", (0, 0, 0),      "NAMLU GÖVDESİ", "PETG · 1 ad"),
    "V4_kapsul":     (S1,        (0, -95, 0),    "KAPSÜL", "PETG · 1 ad"),
    "V4_bilye":      (CELIK,     (0, -55, 0),    "BİLYE", "Ø12.7 kurşun · 6 ad"),
    "V4_capraz_pim": (ALU,       (0, -150, 0),   "ÇAPRAZ PİM", "Ø8 Al 7075 · 1 ad"),
    "V4_pim_sag":    (S2,        (55, 0, 0),     "TETİK PİMİ", "Ø5 çelik · 2 ad"),
    "V4_pim_sol":    (S2,        (-55, 0, 0),    None, None),
    "V4_kapak_sag":  ("#5f6f82", (85, 0, 0),     "KARTUŞ KAPAĞI", "PETG · 2 ad"),
    "V4_kapak_sol":  ("#5f6f82", (-85, 0, 0),    None, None),
    "V4_tampon_ust": (TPU,       (0, 0, 42),     "TPU TAMPON", "TPU 95A · 2 ad"),
    "V4_tampon_alt": (TPU,       (0, 0, -42),    None, None),
    "V4_bant_1":     (S3,        (0, 0, 30),     "LATEKS BANT", "Ø15.2/4 · 4 ad"),
    "V4_bant_2":     (S3,        (0, 0, 30),     None, None),
    "V4_bant_3":     (S3,        (0, 0, -30),    None, None),
    "V4_bant_4":     (S3,        (0, 0, -30),    None, None),
}

fig = plt.figure(figsize=(16.0, 10.4))
gs = fig.add_gridspec(2, 2, height_ratios=[1.15, 1], width_ratios=[1.45, 1],
                      hspace=.14, wspace=.05, left=.02, right=.985,
                      top=.905, bottom=.03)

# ---------------- (a) PATLATILMIS GORUNUM -----------------------------------
ax = fig.add_subplot(gs[0, :])
parcalar, etiketler = [], []
for ad, (renk, dv, lbl, mat) in PARCA.items():
    v = D[ad + "_v"].copy()
    v[:, 0] += dv[0]; v[:, 1] += dv[1]; v[:, 2] += dv[2]
    parcalar.append((v, D[ad + "_f"], renk))
    if lbl:
        etiketler.append((v.mean(0), lbl, mat, renk))
izciz(ax, parcalar, elev=24, azim=-26)
d, r, u = kamera(24, -26)
x0, x1 = ax.get_xlim(); y0, y1 = ax.get_ylim()
H = y1 - y0
ax.set_ylim(y0 - 0.30 * H, y1 + 0.34 * H)
konum = [(x, y) for x, y in zip(
    np.linspace(x0 + 0.02 * (x1 - x0), x1 - 0.02 * (x1 - x0), 8),
    [y1 + 0.24 * H, y0 - 0.20 * H] * 4)]
sirali = sorted(etiketler, key=lambda e: e[0] @ r)
for (c, lbl, mat, renk), (lx, ly) in zip(sirali, konum):
    px, py = c @ r, c @ u
    ax.annotate(f"{lbl}\n{mat}", xy=(px, py), xytext=(lx, ly), fontsize=9,
                fontweight="bold", color=renk, ha="center",
                va="bottom" if ly > py else "top",
                arrowprops=dict(arrowstyle="-", color=renk, lw=1.0, alpha=.55,
                                shrinkA=2, shrinkB=2),
                zorder=40)
ax.set_title("(a) PATLATILMIŞ GÖRÜNÜM — 8 farklı parça, toplam 20 adet",
             loc="left", fontweight="bold", fontsize=12)

# ---------------- (b) MONTAJ SIRASI -----------------------------------------
ax = fig.add_subplot(gs[1, 0]); ax.axis("off")
ax.set_title("(b) MONTAJ SIRASI", loc="left", fontweight="bold", fontsize=12)
adimlar = [
    ("1", "NAMLUYU HAZIRLA", "2× PTFE burç → tetik delikleri.  8× M2 ısıl insert\n"
     "(4 kapak + 4 servo).  2× TPU tampon → yarık ÖN ucu (CA).", S1),
    ("2", "TETİK KARTUŞLARINI KUR", "Göbeğe: pim → yay → mil bileziği (uçtan 12.2 mm,\n"
     "Loctite). İpi pimden geçir, kapağı M2 ile vidala.", S2),
    ("3", "AĞI KAPSÜLE YERLEŞTİR", "6 dilime katla, köşeler üstte. Hazneye bastır (16 mm),\n"
     "bilyeleri yuvalara oturt. Kâğıt kapağı noktasal yapıştır.", S3),
    ("4", "KAPSÜLÜ NAMLUYA SOK", "ARKADAN sok, çapraz pimi kapsül deliğinden geçir ve\n"
     "yarıklara hizala. İki tetik pimini it → kapsül KİLİTLİ.", S1),
    ("5", "BANTLARI TAK", "Her bandı TEK TEK çek (31 kg), çapraz pim oluğuna tak.\n"
     "Ön uçlar ağız kulağındaki ankraj pimlerine.", "#0f6e4c"),
    ("6", "SERVOLARI BAĞLA", "2× MG996R yataklara, ipleri tamburlara sar. Y-kablo ile\n"
     "TEK PWM kanalı. ATIŞ: tek komut → iki pim aynı anda.", S2),
]
y = 0.97
for no, bas, det, renk in adimlar:
    ax.add_patch(plt.Circle((0.028, y - 0.022), 0.021, color=renk,
                            transform=ax.transAxes, clip_on=False, zorder=5))
    ax.text(0.028, y - 0.022, no, fontsize=11, fontweight="bold", color="white",
            ha="center", va="center", transform=ax.transAxes, zorder=6)
    ax.text(0.075, y, bas, fontsize=10.5, fontweight="bold", color=renk,
            transform=ax.transAxes, va="top")
    ax.text(0.075, y - 0.050, det, fontsize=9, color=INK, transform=ax.transAxes,
            va="top", linespacing=1.5)
    y -= 0.163

# ---------------- (c) PARCA -> KONUM TABLOSU --------------------------------
ax = fig.add_subplot(gs[1, 1]); ax.axis("off")
ax.set_title("(c) HANGİ PARÇA NEREYE", loc="left", fontweight="bold", fontsize=12)
tab = [
    ("Namlu gövdesi", "PETG", "1", "—  (ana gövde)"),
    ("Kapsül", "PETG", "1", "namlu içi, arkada"),
    ("Bilye Ø12.7", "kurşun", "6", "kapsül ön yüzü, 13° yuvalar"),
    ("Ağ Ø2.80 m", "PE #1/#3", "1", "kapsül haznesi (16 mm)"),
    ("Çapraz pim Ø8", "Al 7075", "1", "kapsül + yarıklar"),
    ("Lateks bant Ø15.2", "lateks", "4", "namlu dışı, 2/kenar"),
    ("Tetik pimi Ø5", "çelik", "2", "kartuş göbekleri, ±X"),
    ("PTFE burç", "PTFE", "2", "tetik delikleri"),
    ("Mil bileziği Ø5/Ø10", "çelik", "2", "pim üzerinde, yay tablası"),
    ("Geri yay", "yay çeliği", "2", "göbek içi, bilezik arkası"),
    ("Kartuş kapağı", "PETG", "2", "göbek ucu, M2"),
    ("TPU tampon", "TPU 95A", "2", "yarık ÖN ucu"),
    ("Ankraj pimi Ø4", "paslanmaz", "4", "ağız kulakları"),
    ("Servo MG996R", "—", "2", "yan yataklar"),
    ("Makara Ø8", "PETG", "2", "servo dişlisi"),
]
ax.text(0.0, 0.955, "Parça", fontsize=9, fontweight="bold", color=INK2,
        transform=ax.transAxes)
ax.text(0.42, 0.955, "Malz.", fontsize=9, fontweight="bold", color=INK2,
        transform=ax.transAxes)
ax.text(0.60, 0.955, "Ad.", fontsize=9, fontweight="bold", color=INK2,
        transform=ax.transAxes)
ax.text(0.68, 0.955, "Konum", fontsize=9, fontweight="bold", color=INK2,
        transform=ax.transAxes)
ax.plot([0, 1], [0.935, 0.935], color=GRID, lw=1, transform=ax.transAxes)
y = 0.895
for a, m, n, k in tab:
    ax.text(0.0, y, a, fontsize=8.8, transform=ax.transAxes)
    ax.text(0.42, y, m, fontsize=8.8, color=INK2, transform=ax.transAxes)
    ax.text(0.63, y, n, fontsize=8.8, fontweight="bold", ha="center",
            transform=ax.transAxes)
    ax.text(0.68, y, k, fontsize=8.8, color=INK2, transform=ax.transAxes)
    y -= 0.0605
ax.plot([0, 1], [y + 0.030, y + 0.030], color=GRID, lw=1, transform=ax.transAxes)
ax.text(0.0, y - 0.01, "+ M2 insert ×8, M2 civata ×8, ip, yağ, CA, Loctite",
        fontsize=8.5, color=INK2, transform=ax.transAxes)
ax.text(0.0, y - 0.065, "TOPLAM ~469 g", fontsize=11, fontweight="bold",
        color=INK, transform=ax.transAxes)

fig.suptitle("AĞ FIRLATICI NAMLU v4 — MONTAJ REHBERİ   (namlu 180.5 mm · "
             "4 lateks bant · atış penceresi 3.6–5.9 m)",
             fontsize=13.5, fontweight="bold", x=.02, ha="left", y=.965)
plt.savefig(vyol(__file__, "out", "REHBER_montaj.png"), dpi=120)
print("-> out/REHBER_montaj.png")
