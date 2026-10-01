"""Menzil grafigi: atis penceresinin kenarlarini ne belirliyor?"""
import sys
sys.path.insert(0, '/home/kayra/Masaüstü/ag_firlatma')
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

S1, S2, S3 = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#d8d7d2"
plt.rcParams.update({"figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb",
                     "axes.edgecolor": GRID, "text.color": INK,
                     "axes.labelcolor": INK, "xtick.color": INK2,
                     "ytick.color": INK2, "grid.color": GRID, "font.size": 9.5})

# run_menzil.py ciktilari
V = np.array([14.7, 19.8, 24.8, 29.8, 39.7, 54.7, 69.6])
YAK = np.array([1.87, 1.94, 1.96, 1.97, 2.01, 2.02, 2.10])
UZA = np.array([2.57, 3.19, 3.75, 4.30, 5.22, 6.02, 6.52])
EN = np.array([25, 44, 70, 100, 178, 336, 545])

A = np.array([8, 12, 18, 25, 35])
AY = np.array([3.87, 2.94, 2.04, 1.38, 0.89])
AU = np.array([6.19, 5.40, 4.39, 3.51, 2.57])

HV = [20, 30, 45]
HA = [8, 12, 18, 25]
H = np.array([[4.17, 3.95, 3.26, 2.58],
              [6.19, 5.40, 4.39, 3.51],
              [8.02, 6.97, 5.66, 4.51]])

fig, ax = plt.subplots(1, 3, figsize=(15.5, 5.0))
plt.subplots_adjust(left=.055, right=.985, top=.83, bottom=.13, wspace=.28)

# ---- (a) hiz ----------------------------------------------------------------
a = ax[0]
a.fill_between(V, YAK, UZA, color=S1, alpha=.16, label="atış penceresi")
a.plot(V, UZA, "-o", color=S1, lw=2.2, ms=6, label="UZAK kenar")
a.plot(V, YAK, "-s", color=S2, lw=2.2, ms=6, label="YAKIN kenar")
a.annotate("hızla büyüyor\n2.6 → 6.5 m", xy=(55, 6.02), xytext=(30, 6.6),
           fontsize=9.5, color=S1, fontweight="bold",
           arrowprops=dict(arrowstyle="->", color=S1, lw=1.3))
a.annotate("neredeyse sabit", xy=(45, 2.02), xytext=(44, 3.1),
           fontsize=9.5, color=S2, fontweight="bold",
           arrowprops=dict(arrowstyle="->", color=S2, lw=1.3))
a.axvspan(14, 21, color=GRID, alpha=.55, lw=0)
a.text(17.5, 7.3, "YAY\ntavanı", ha="center", fontsize=9, color=INK2,
       fontweight="bold")
a.set(xlabel="namlu çıkış hızı [m/s]", ylabel="drone'a göre mesafe [m]",
      ylim=(0, 7.9))
a.set_title("(a) Hız SADECE uzak kenarı büyütür", loc="left", fontweight="bold")
a.legend(fontsize=8.5, frameon=False, loc="upper left",
         bbox_to_anchor=(0.02, 0.86)); a.grid(alpha=.3)

# ---- (b) azalan verim -------------------------------------------------------
a = ax[1]
a.plot(EN, UZA, "-o", color=S1, lw=2.2, ms=6)
for e, u, v in zip(EN, UZA, V):
    a.annotate(f"{v:.0f} m/s", (e, u), textcoords="offset points",
               xytext=(6, -11), fontsize=8, color=INK2)
a.annotate("+1.1 m\n(+56 J)", xy=(72, 3.8), xytext=(95, 2.9), fontsize=9,
           color=S3, fontweight="bold",
           arrowprops=dict(arrowstyle="->", color=S3, lw=1.3))
a.annotate("+0.5 m\n(+209 J)", xy=(440, 6.3), xytext=(250, 5.2), fontsize=9,
           color=S2, fontweight="bold",
           arrowprops=dict(arrowstyle="->", color=S2, lw=1.3))
a.set(xlabel="depolanan enerji [J]", ylabel="uzak kenar [m]", ylim=(2, 7.2))
a.set_title("(b) Enerji v² ile, menzil ln(v) ile büyür", loc="left",
            fontweight="bold")
a.grid(alpha=.3)

# ---- (c) koni acisi ---------------------------------------------------------
a = ax[2]
a.fill_between(A, AY, AU, color=S3, alpha=.16)
a.plot(A, AU, "-o", color=S1, lw=2.2, ms=6, label="UZAK kenar")
a.plot(A, AY, "-s", color=S2, lw=2.2, ms=6, label="YAKIN kenar")
a.annotate("pencere KAYIYOR,\ngenişlemiyor", xy=(12, 4.2), xytext=(20, 5.9),
           fontsize=9.5, color=INK2, fontweight="bold",
           arrowprops=dict(arrowstyle="->", color=INK2, lw=1.3))
# v=20 m/s'de tam-model MC ile olculen yakalama olasiliklari
for aa, uu, pp in [(8, 6.19, "%78 / %93"), (12, 5.40, "%93 / %98"),
                   (18, 4.39, "%98 / %100")]:
    a.plot(aa, uu, "o", color=S1, ms=11, mec="white", mew=1.6, zorder=6)
    a.text(aa + 0.6, uu + 0.22, pp, fontsize=9, color=S1, fontweight="bold")
a.plot(12, 5.40, "*", color=S3, ms=20, mec="white", mew=1.4, zorder=7)
a.text(13.0, 4.30, "DENGE\nα=12°", fontsize=9.5, color=S3, fontweight="bold")
a.text(8.0, 7.7, "yakalama olasılığı:  baskı ±2° / işlenmiş ±0.5°",
       fontsize=8.5, color=INK2, va="top")
a.set(xlabel="yuva koni açısı α [°]", ylabel="drone'a göre mesafe [m]",
      ylim=(0, 8.2))
a.set_title("(c) Açı BEDELSİZ menzil verir",
            loc="left", fontweight="bold")
a.legend(fontsize=8.5, frameon=False, loc="lower left"); a.grid(alpha=.3)

fig.suptitle("Ağ menzilini ne belirliyor?  (Ø3.0 m ağ, tam 3B model, 100 km/h)",
             fontsize=13, fontweight="bold", x=.055, ha="left", y=.955)
plt.savefig("out/menzil.png", dpi=125)
print("-> out/menzil.png")
