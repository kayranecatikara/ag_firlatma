#!/usr/bin/env python3
"""GAZEBO <-> PYTHON karsilastirmasi.

Iki BAGIMSIZ cozucu ayni fizigi cozuyor:
  * Python (agsim/netfull.py): kendi velocity-Verlet entegratoru
  * Gazebo (AgFizik plugin + DART): ayni kuvvetler, DART entegratoru
Uyusurlarsa guven artar; uyusmazlarsa hangisinin dogru oldugunu
ancak GERCEK ATIS soyler.
"""
import sys, os, json
KOK = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, KOK)
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import run_menzil_nihai as M

S1, S2, S3 = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#d8d7d2"
plt.rcParams.update({"figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb",
                     "text.color": INK, "axes.labelcolor": INK,
                     "xtick.color": INK2, "ytick.color": INK2,
                     "axes.edgecolor": GRID, "grid.color": GRID, "font.size": 9.5})

CSV = os.path.join(KOK, "out", "gazebo_ag.csv")
if not os.path.exists(CSV) or sum(1 for _ in open(CSV)) < 5:
    sys.exit("gazebo_ag.csv yok veya bos — once simulasyonu calistirin.")
G = np.genfromtxt(CSV, delimiter=",", names=True)
gt, gR, gX = G["t"], G["R_bilye"], G["X_bilye"]

# --- Python referansi. Gazebo SDF hangi cozunurlukte uretildiyse ONU kullan;
#     ayrica ince orguyu de ciz -> ORGU DUYARLILIGI gorunur olsun.
TSON = float(gt.max()) + 0.01
import os
NR = int(os.environ.get("AG_NRING", 5)); NS = int(os.environ.get("AG_NSPOKE", 12))

def python_yol(nr, ns):
    t, L = M.kur()
    t.ag.n_ring, t.ag.n_spoke = nr, ns
    return M.yol(t, L, T=TSON)

ts, Z, R = python_yol(NR, NS)              # Gazebo ile AYNI orgu
ts2, Z2, R2 = python_yol(7, 18)            # ince orgu (tasarim kararlarinda kullanilan)

def tepe(a):
    return int(np.argmax(a[:max(len(a)//2, 2)]))
i_p, i_g, i_2 = tepe(R), tepe(gR), tepe(R2)

fig, ax = plt.subplots(1, 3, figsize=(15.0, 4.6))
plt.subplots_adjust(left=.055, right=.985, top=.80, bottom=.14, wspace=.28)

a = ax[0]
a.plot(ts*1e3, R, color=S1, lw=2.4, label=f"Python {NR}×{NS}")
a.plot(ts2*1e3, R2, color=S3, lw=1.5, alpha=.8, label="Python 7×18")
a.plot(gt*1e3, gR, color=S2, lw=2.0, ls="--", label=f"Gazebo {NR}×{NS}")
a.axhline(M.R_GER, color=INK2, lw=1.4, ls=":", label=f"gerekli {M.R_GER} m")
a.plot(ts[i_p]*1e3, R[i_p], "o", color=S1, ms=8, mec="white", mew=1.2)
a.plot(gt[i_g]*1e3, gR[i_g], "s", color=S2, ms=8, mec="white", mew=1.2)
a.set(xlabel="atıştan sonra [ms]", ylabel="ağ yarıçapı [m]")
a.set_title("(a) Ağ açılması", loc="left", fontweight="bold")
a.legend(fontsize=8.5, frameon=False); a.grid(alpha=.3)

a = ax[1]
a.plot(ts*1e3, Z, color=S1, lw=2.4, label=f"Python {NR}×{NS}")
a.plot(ts2*1e3, Z2, color=S3, lw=1.5, alpha=.8, label="Python 7×18")
a.plot(gt*1e3, gX, color=S2, lw=2.0, ls="--", label=f"Gazebo {NR}×{NS}")
a.set(xlabel="atıştan sonra [ms]", ylabel="ileri mesafe [m]")
a.set_title("(b) Bilye yolu", loc="left", fontweight="bold")
a.legend(fontsize=8.5, frameon=False); a.grid(alpha=.3)

a = ax[2]
a.plot(Z, R, color=S1, lw=2.4, label=f"Python {NR}×{NS}")
a.plot(Z2, R2, color=S3, lw=1.5, alpha=.8, label="Python 7×18")
a.plot(gX, gR, color=S2, lw=2.0, ls="--", label=f"Gazebo {NR}×{NS}")
a.axhline(M.R_GER, color=INK2, lw=1.4, ls=":")
a.set(xlabel="ileri mesafe [m]", ylabel="ağ yarıçapı [m]")
a.set_title("(c) Atış penceresi", loc="left", fontweight="bold")
a.legend(fontsize=8.5, frameon=False); a.grid(alpha=.3)

d_R = 100*(gR[i_g]-R[i_p])/R[i_p]
d_t = 100*(gt[i_g]-ts[i_p])/ts[i_p]
fig.suptitle(f"GAZEBO ↔ PYTHON DOĞRULAMASI   —   R_tepe: "
             f"{R[i_p]:.3f} vs {gR[i_g]:.3f} m ({d_R:+.0f}%)   ·   "
             f"t_tepe: {ts[i_p]*1e3:.0f} vs {gt[i_g]*1e3:.0f} ms ({d_t:+.0f}%)",
             fontsize=12.5, fontweight="bold", x=.055, ha="left", y=.95)
out = os.path.join(KOK, "out", "gazebo_dogrulama.png")
plt.savefig(out, dpi=125)
print(f"-> {out}")
print(f"  Python {NR}x{NS} : R_tepe {R[i_p]:.3f} m @ {ts[i_p]*1e3:.0f} ms, X={Z[i_p]:.2f} m")
print(f"  Gazebo {NR}x{NS} : R_tepe {gR[i_g]:.3f} m @ {gt[i_g]*1e3:.0f} ms, X={gX[i_g]:.2f} m")
print(f"  Python 7x18 : R_tepe {R2[i_2]:.3f} m @ {ts2[i_2]*1e3:.0f} ms, X={Z2[i_2]:.2f} m")
print(f"  SAPMA (ayni orgu) : R %{d_R:+.1f}, t %{d_t:+.1f}")
print(f"  ORGU etkisi (Py 5x12 -> 7x18): R %{100*(R2[i_2]-R[i_p])/R[i_p]:+.1f}")

# --- atis penceresi: iki cozucu ayni pencereyi veriyor mu?
def pencere(tt, zz, rr):
    j = tepe(rr); j2 = j + int(np.argmin(rr[j:]))
    return M.pencere_bagil(tt[:j2+1], zz[:j2+1], rr[:j2+1], 0.0)
pp, pg = pencere(ts, Z, R), pencere(gt, gX, gR)
print(f"  PENCERE Python : {pp[0]:.2f} – {pp[1]:.2f} m")
print(f"  PENCERE Gazebo : {pg[0]:.2f} – {pg[1]:.2f} m")
