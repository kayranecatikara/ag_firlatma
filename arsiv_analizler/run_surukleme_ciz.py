"""Hava suruklemesi agi ne kadar geri cekiyor — nihai tasarim (v2)."""
import sys; sys.path.insert(0, '/home/kayra/Masaüstü/ag_firlatma')
import numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import run_menzil_nihai as M

S1, S2, S3 = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#d8d7d2"
plt.rcParams.update({"figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb",
                     "axes.edgecolor": GRID, "text.color": INK, "axes.labelcolor": INK,
                     "xtick.color": INK2, "ytick.color": INK2, "grid.color": GRID,
                     "font.size": 9.5})
t, L = M.kur()
ts, Z, R = M.yol(t, L, T=0.45)
ts0, Z0, R0 = M.yol(t, L, T=0.45, aero=0.0)
tw, Zw, Rw, i = M.ilk_cevrim(ts, Z, R)
lo, hi = M.pencere_bagil(tw, Zw, Rw, 0.0)

fig, ax = plt.subplots(1, 2, figsize=(14, 5.0))
plt.subplots_adjust(left=.06, right=.985, top=.82, bottom=.13, wspace=.22)
a = ax[0]
a.plot(ts0 * 1e3, Z0, color=INK2, lw=2, ls="--", label="havasız olsaydı")
a.plot(ts * 1e3, Z, color=S1, lw=2.6, label="gerçek (100 km/h karşı rüzgâr)")
a.fill_between(ts * 1e3, Z, np.interp(ts, ts0, Z0), color=S2, alpha=.15)
for tt in (0.15, 0.25, 0.35):
    j = np.argmin(abs(ts - tt)); z0 = np.interp(tt, ts0, Z0)
    a.annotate("", xy=(tt * 1e3, Z[j]), xytext=(tt * 1e3, z0),
               arrowprops=dict(arrowstyle="<->", color=S2, lw=1.4))
    a.text(tt * 1e3 + 5, (Z[j] + z0) / 2, f"{z0 - Z[j]:.1f} m\ngeri", fontsize=9,
           color=S2, fontweight="bold", va="center")
a.axhspan(lo, hi, color=S3, alpha=.13, lw=0)
a.text(8, (lo + hi) / 2, f"atış penceresi\n{lo:.1f}–{hi:.1f} m", fontsize=9,
       color="#0f6e4c", fontweight="bold", va="center")
a.set(xlabel="zaman [ms]", ylabel="drone'a göre ileri mesafe [m]", ylim=(0, 11))
a.set_title("(a) Hava sürüklemesi ağı ne kadar GERİ çekiyor?", loc="left",
            fontweight="bold")
a.legend(fontsize=8.5, frameon=False, loc="upper left"); a.grid(alpha=.3)

a = ax[1]
a.plot(Z, R, color=S1, lw=2.6, label="ağ yarıçapı")
a.axhline(M.R_GER, color=S2, lw=2, ls="--", label="gerekli 0.75 m (1.5 m kanat)")
a.axvspan(lo, hi, color=S3, alpha=.15, lw=0)
a.plot(Zw[i], Rw[i], "o", color=S1, ms=9, mec="white", mew=1.4)
a.annotate(f"en açık {Rw[i]:.2f} m\n@ {Zw[i]:.1f} m", xy=(Zw[i], Rw[i]),
           xytext=(Zw[i] + .3, Rw[i] + .1), fontsize=9, color=S1, fontweight="bold")
a.text((lo + hi) / 2, .12, f"TETİKLE: hedef\n{lo:.1f}–{hi:.1f} m'deyken", ha="center",
       fontsize=9.5, fontweight="bold", color="#0f6e4c")
a.set(xlabel="drone'a göre ileri mesafe [m]", ylabel="ağ yarıçapı [m]",
      xlim=(0, 5.5), ylim=(0, 1.25))
a.set_title("(b) Ağ nerede ne kadar açık?", loc="left", fontweight="bold")
a.legend(fontsize=8.5, frameon=False, loc="upper left"); a.grid(alpha=.3)
fig.suptitle(f"Nihai tasarım (v2): 162 mm namlu, v_çıkış {L['v_exit']:.1f} m/s, "
             f"Ø2.2 m ağ, drone ve hedef 100 km/h", fontsize=12.5, fontweight="bold",
             x=.06, ha="left", y=.95)
plt.savefig("out/surukleme_v2.png", dpi=125)
print("-> out/surukleme_v2.png", f"pencere {lo:.2f}-{hi:.2f}")
