"""Iki cerceve + bagil hiz toleransi gorseli."""
import os, sys
_K = os.path.abspath(__file__)
while _K != os.path.dirname(_K) and not os.path.isdir(os.path.join(_K, "agsim")):
    _K = os.path.dirname(_K)
sys.path.insert(0, _K)
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from run_cerceve import kos, R_GER, V_DRONE
from run_bagil_hiz import kesisme

S1, S2, S3 = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#d8d7d2"
plt.rcParams.update({"figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb",
                     "axes.edgecolor": GRID, "text.color": INK,
                     "axes.labelcolor": INK, "xtick.color": INK2,
                     "ytick.color": INK2, "grid.color": GRID, "font.size": 9.5})

t, L, S = kos(alpha_deg=18, v_hedef=20.0, T=0.80)
R, ts, P, Vv, bd = S['R'], S['t'], S['P_snap'], S['V_snap'], S['bilye_dug']
Z = np.array([p[bd, 2].mean() for p in P])
Vz = np.array([v[bd, 2].mean() for v in Vv])
S_yer = Z + V_DRONE * ts
V_hava = Vz + V_DRONE
i = int(np.argmax(R[:len(R) // 2])); j = i + int(np.argmin(R[i:]))
m = (R >= R_GER) & (np.arange(len(R)) <= j)

fig, ax = plt.subplots(1, 3, figsize=(15.5, 5.0))
plt.subplots_adjust(left=.055, right=.985, top=.82, bottom=.135, wspace=.30)

# ---- (a) iki cerceve --------------------------------------------------------
a = ax[0]
a.plot(ts * 1e3, S_yer, color=S2, lw=2.4, label="YERDE aldığı yol")
a.plot(ts * 1e3, Z, color=S1, lw=2.4, label="DRONE'a göre mesafe")
a.plot(ts * 1e3, V_DRONE * ts, color=INK2, lw=1.6, ls="--",
       label="drone (ve hedef) yolu")
a.fill_between(ts * 1e3, Z, S_yer, color=S2, alpha=.10)
k = np.argmin(abs(ts - .20))
a.annotate(f"t=200 ms\nyerde {S_yer[k]:.1f} m\ndrone'a göre {Z[k]:.1f} m",
           xy=(200, S_yer[k]), xytext=(232, 3.0), fontsize=9,
           color=INK, fontweight="bold",
           arrowprops=dict(arrowstyle="->", color=INK2, lw=1.2))
a.axvspan(ts[m].min() * 1e3, ts[m].max() * 1e3, color=S3, alpha=.14, lw=0)
a.text((ts[m].min() + ts[m].max()) / 2 * 1e3, 15.2, "atış\npenceresi",
       ha="center", fontsize=9, color="#0f6e4c", fontweight="bold")
a.set(xlabel="zaman [ms]", ylabel="mesafe [m]", ylim=(0, 17))
a.set_title("(a) Ağ havada 5–15 m süpürüyor,\ndrone'a göre sadece 2–3 m kazanıyor",
            loc="left", fontweight="bold")
a.legend(fontsize=8.5, frameon=False, loc="upper left",
         bbox_to_anchor=(0.0, 0.88)); a.grid(alpha=.3)

# ---- (b) enerji -------------------------------------------------------------
a = ax[1]
KE = 0.5 * t.m_ucan * V_hava ** 2
KE_namlu = 0.5 * t.m_ucan * L["v_exit"] ** 2
a.plot(S_yer, KE, color=S1, lw=2.4)
a.fill_between(S_yer, 0, KE, color=S1, alpha=.12)
a.axhline(KE_namlu, color=S2, lw=2, ls="--")
a.text(S_yer[-1] * .98, KE_namlu + 1.4, f"namlunun verdiği: {KE_namlu:.0f} J",
       ha="right", fontsize=9, color=S2, fontweight="bold")
a.annotate(f"drone hızından gelen\n'bedava' {KE[0]-KE_namlu:.0f} J",
           xy=(0.3, KE[0]), xytext=(4.2, 54), fontsize=9, color=INK2,
           fontweight="bold",
           arrowprops=dict(arrowstyle="->", color=INK2, lw=1.2))
a.annotate(f"sürüklemenin yuttuğu\n{KE[0]-KE[m][-1]:.0f} J  (%{100*(KE[0]-KE[m][-1])/KE[0]:.0f})",
           xy=(8, 30), xytext=(7.5, 44), fontsize=9.5, color=S1,
           fontweight="bold",
           arrowprops=dict(arrowstyle="->", color=S1, lw=1.3))
a.set(xlabel="yerde alınan yol [m]", ylabel="havaya göre kinetik enerji [J]",
      xlim=(0, 17), ylim=(0, 68))
a.set_title("(b) Enerjinin %76'sı havaya gidiyor", loc="left", fontweight="bold")
a.grid(alpha=.3)

# ---- (c) bagil hiz ----------------------------------------------------------
a = ax[2]
Rw, tsw, Zw = R[:j + 1], ts[:j + 1], Z[:j + 1]
d0_ara = np.arange(0.2, 8.0, 0.02)
vb = np.arange(-11, 9.01, 0.5)
alt, ust = [], []
for v in vb:
    ok = np.array([kesisme(tsw, Zw, Rw, d, v)[0] for d in d0_ara])
    if ok.any():
        alt.append(d0_ara[ok].min()); ust.append(d0_ara[ok].max())
    else:
        alt.append(np.nan); ust.append(np.nan)
alt, ust = np.array(alt), np.array(ust)
a.fill_between(vb * 3.6, alt, ust, color=S3, alpha=.22, lw=0)
a.plot(vb * 3.6, ust, "-o", color=S1, lw=2.2, ms=4, label="en uzak tetikleme")
a.plot(vb * 3.6, alt, "-s", color=S2, lw=2.2, ms=4, label="en yakın tetikleme")
a.axvline(0, color=INK2, lw=1.2, ls=":")
a.text(1.5, 7.3, "aynı hız\n(varsaydığım)", fontsize=8.5, color=INK2)
a.annotate("KAPANIRSANIZ\nmenzil uzuyor", xy=(-30, 6.2), xytext=(-34, 3.4),
           fontsize=9.5, color=S1, fontweight="bold",
           arrowprops=dict(arrowstyle="->", color=S1, lw=1.3))
a.set(xlabel="bağıl hız  (hedef − drone)  [km/h]",
      ylabel="tetikleme mesafesi [m]", ylim=(0, 8))
a.set_title("(c) Hedefe kapanmak menzili İYİLEŞTİRİYOR", loc="left",
            fontweight="bold")
a.legend(fontsize=8.5, frameon=False, loc="lower left"); a.grid(alpha=.3)

fig.suptitle("Referans çerçevesi: ağ havada ne kadar yol alıyor, enerjisi nereye gidiyor?"
             "   (100 km/h, α=18°, v_çıkış 20 m/s)",
             fontsize=12.5, fontweight="bold", x=.055, ha="left", y=.95)
plt.savefig("out/cerceve.png", dpi=125)
print("-> out/cerceve.png")
