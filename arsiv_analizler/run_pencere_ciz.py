"""Atis penceresi nedir + drone'u hizlandirmanin etkisi."""
import os, sys
_K = os.path.abspath(__file__)
while _K != os.path.dirname(_K) and not os.path.isdir(os.path.join(_K, "agsim")):
    _K = os.path.dirname(_K)
sys.path.insert(0, _K)
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from run_cerceve import kos, R_GER

S1, S2, S3 = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#d8d7d2"
plt.rcParams.update({"figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb",
                     "axes.edgecolor": GRID, "text.color": INK,
                     "axes.labelcolor": INK, "xtick.color": INK2,
                     "ytick.color": INK2, "grid.color": GRID, "font.size": 9.5})

t, L, S = kos(alpha_deg=18, v_hedef=20.0, T=0.80)
R, ts, P, bd = S['R'], S['t'], S['P_snap'], S['bilye_dug']
Z = np.array([p[bd, 2].mean() for p in P])
i = int(np.argmax(R[:len(R) // 2])); j = i + int(np.argmin(R[i:]))
Rw, tsw, Zw = R[:j + 1], ts[:j + 1], Z[:j + 1]
m = Rw >= R_GER

# run_hizlanma.py sonuclari
KMH = np.array([100, 110, 120, 130, 140, 160])
ALT = np.array([1.98, 2.28, 2.58, 2.88, 3.18, 3.80])
UST = np.array([3.24, 3.84, 4.46, 5.10, 5.76, 7.06])
ZMAX = np.array([3.26, 3.04, 2.84, 2.68, 2.53, 2.27])

fig, ax = plt.subplots(1, 2, figsize=(14.0, 5.4))
plt.subplots_adjust(left=.06, right=.985, top=.80, bottom=.13, wspace=.24)

# ---- (a) pencere nedir ------------------------------------------------------
a = ax[0]
a.plot(Zw, Rw, color=S1, lw=2.6, zorder=4)
a.axhline(R_GER, color=S2, lw=2, ls="--", zorder=3)
a.text(0.12, R_GER + .05, "hedefi örtmek için gereken yarıçap (0.75 m)",
       fontsize=9, color=S2, fontweight="bold")
a.axvspan(Zw[m].min(), Zw[m].max(), color=S3, alpha=.18, lw=0, zorder=1)
a.fill_between(Zw, 0, Rw, where=~m, color=GRID, alpha=.35, zorder=2)

a.annotate("ağ hâlâ ÇOK KÜÇÜK\n(paket açılıyor)", xy=(1.0, 0.38),
           xytext=(0.15, 1.42), fontsize=9.5, color=INK2, fontweight="bold",
           arrowprops=dict(arrowstyle="->", color=INK2, lw=1.2))
a.annotate("ağ KAPANMIŞ\n(elastik geri tepme)", xy=(2.6, 0.45),
           xytext=(1.55, 0.13), fontsize=9.5, color=INK2, fontweight="bold",
           arrowprops=dict(arrowstyle="->", color=INK2, lw=1.2))
a.plot(Zw[i], Rw[i], "o", color=S1, ms=10, mec="white", mew=1.5, zorder=5)
a.text(Zw[i] + .08, Rw[i] + .06, f"en açık\n{Rw[i]:.2f} m", fontsize=9,
       color=S1, fontweight="bold")
a.annotate("", xy=(Zw[m].min(), 1.62), xytext=(Zw[m].max(), 1.62),
           arrowprops=dict(arrowstyle="<->", color="#0f6e4c", lw=2))
a.text((Zw[m].min() + Zw[m].max()) / 2, 1.66,
       f"ATIŞ PENCERESİ  {Zw[m].min():.2f} – {Zw[m].max():.2f} m",
       ha="center", fontsize=10.5, color="#0f6e4c", fontweight="bold")
a.set(xlabel="hedefin ateşleme anındaki mesafesi [m]",
      ylabel="ağın yarıçapı, hedefe vardığında [m]", xlim=(0, 3.6), ylim=(0, 1.85))
a.set_title("(a) “Pencere” = ağın hedefe vardığında YETERİNCE AÇIK olduğu\n"
            "ateşleme mesafeleri aralığı", loc="left", fontweight="bold")
a.grid(alpha=.3)

# ---- (b) hizlanma -----------------------------------------------------------
a = ax[1]
a.fill_between(KMH, ALT, UST, color=S3, alpha=.20, lw=0)
a.plot(KMH, UST, "-o", color=S1, lw=2.4, ms=6, label="en uzak ateşleme")
a.plot(KMH, ALT, "-s", color=S2, lw=2.4, ms=6, label="en yakın ateşleme")
a.plot(KMH, ZMAX, "--^", color=INK2, lw=1.8, ms=5,
       label="ağın kendi erişimi (Z_max)")
a.annotate("hedef bize geliyor\n→ pencere UZUYOR", xy=(150, 6.4),
           xytext=(112, 6.5), fontsize=9.5, color=S1, fontweight="bold",
           arrowprops=dict(arrowstyle="->", color=S1, lw=1.3))
a.annotate("karşı rüzgâr arttı\n→ ağın erişimi DÜŞÜYOR", xy=(150, 2.35),
           xytext=(103, 1.05), fontsize=9.5, color=INK2, fontweight="bold",
           arrowprops=dict(arrowstyle="->", color=INK2, lw=1.3))
a.plot(130, 5.10, "*", color=S3, ms=22, mec="white", mew=1.4, zorder=6)
a.text(131, 4.45, "ÖNERİ\n130 km/h", fontsize=9.5, color="#0f6e4c",
       fontweight="bold")
a.set(xlabel="drone hızı [km/h]   (hedef sabit 100 km/h)",
      ylabel="mesafe [m]", ylim=(0, 7.8))
a.set_title("(b) Atıştan önce hızlanmak İŞE YARIYOR\n"
            "(iki etki ters yönde; kapanma baskın çıkıyor)",
            loc="left", fontweight="bold")
a.legend(fontsize=8.5, frameon=False, loc="upper left",
         bbox_to_anchor=(0.0, 0.62))
a.grid(alpha=.3)

fig.suptitle("Atış penceresi nedir, ve hızlanarak nasıl genişletilir?"
             "   (α=18°, v_çıkış 20 m/s, Ø3.0 m ağ)",
             fontsize=12.5, fontweight="bold", x=.06, ha="left", y=.945)
plt.savefig("out/pencere.png", dpi=125)
print("-> out/pencere.png")
