#!/usr/bin/env python3
"""IPLIK CAPI KARARI — menzil kazanci vs uc kesilme/kopma mekanizmasi."""
import sys, json, os
sys.path.insert(0, '/home/kayra/Masaüstü/ag_firlatma')
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from agsim.params import Ag
from agsim.kesilme import (smith_kritik_hiz, kenar_basinci, sarilma_gerilimi,
                           uc_hizi, ENINE_DAYANIM, DUGUM_VERIMI, DUGUMSUZ_VERIM)

S1, S2, S3, S4 = "#2a78d6", "#eb6834", "#1baf7a", "#8b5cd6"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#d8d7d2"
plt.rcParams.update({"figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb",
    "text.color": INK, "axes.labelcolor": INK, "xtick.color": INK2,
    "ytick.color": INK2, "axes.edgecolor": GRID, "grid.color": GRID,
    "font.size": 9.5})

D = json.load(open("out/ip_capi_tarama.json"))
d = np.array([r["d_mm"] for r in D])
hi = np.array([r["hi"] for r in D]); lo = np.array([r["lo"] for r in D])
Rt = np.array([r["R_tepe"] for r in D])
T_YAK = float(os.environ.get("T_YAK", "9.9"))      # Gazebo yakalama gerilmesi
T_SAR = sarilma_gerilimi(0.30, 0.020)
MEVCUT = 0.165

fig, ax = plt.subplots(1, 4, figsize=(18.2, 4.5))
plt.subplots_adjust(left=.045, right=.988, top=.76, bottom=.15, wspace=.30)

# (a) MENZIL KAZANCI
a = ax[0]
a.fill_between(d, lo, hi, color=S1, alpha=.18)
a.plot(d, hi, color=S1, lw=2.4, marker="o", ms=4, label="pencere uzak kenarı")
a.plot(d, lo, color=S1, lw=1.6, ls="--", label="pencere yakın kenarı")
a.axvline(MEVCUT, color=INK2, lw=1.3, ls=":")
a.text(MEVCUT, a.get_ylim()[0], " mevcut", fontsize=8, color=INK2, va="bottom")
a.invert_xaxis()
a.set(xlabel="iplik çapı [mm]", ylabel="tetikleme mesafesi [m]")
a.set_title("(a) KAZANÇ — atış penceresi", loc="left", fontweight="bold")
a.legend(fontsize=8, frameon=False); a.grid(alpha=.3)

# (b) MEKANIZMA 1: enine darbe -- CAPTAN BAGIMSIZ
a = ax[1]
Vc, c, eb = smith_kritik_hiz("Dyneema_SK78")
a.axhline(Vc, color=S3, lw=2.6, label=f"Smith kritik hız {Vc:.0f} m/s")
for rpm, st in ((7000, ":"), (9000, "-"), (11000, "--")):
    a.axhline(uc_hizi(.230, rpm), color=S2, lw=1.7, ls=st,
              label=f"pervane ucu {rpm} rpm")
a.set(xlabel="iplik çapı [mm]", ylabel="hız [m/s]", xlim=(d.max(), d.min()),
      ylim=(0, Vc*1.15))
a.set_title("(b) Enine darbe — ÇAPTAN BAĞIMSIZ", loc="left", fontweight="bold")
a.legend(fontsize=7.5, frameon=False, loc="lower center"); a.grid(alpha=.3)
a.text(.5, .62, f"{Vc/uc_hizi(.230,11000):.0f}× pay — SINIRLAMIYOR",
       transform=a.transAxes, ha="center", fontsize=10.5, fontweight="bold",
       color=S3)

# (c) MEKANIZMA 2: kenar uzerinde kesme -- 1/d
a = ax[2]
dd = np.linspace(.09, .18, 60)
for re, st, lb in ((0.2e-3, ":", "0.20"), (0.35e-3, "-", "0.35"),
                   (0.5e-3, "--", "0.50")):
    a.plot(dd, kenar_basinci(T_SAR, dd*1e-3, re)/1e6, color=S2, ls=st, lw=1.9,
           label=f"kanat kenar yarıçapı {lb} mm")
a.axhline(ENINE_DAYANIM["Dyneema_SK78"]/1e6, color=S3, lw=2.4,
          label="Dyneema enine dayanım")
a.axhline(ENINE_DAYANIM["Kevlar_29"]/1e6, color=S4, lw=2.4, ls="-.",
          label="Kevlar enine dayanım")
a.axvline(MEVCUT, color=INK2, lw=1.3, ls=":")
a.invert_xaxis()
a.set(xlabel="iplik çapı [mm]", ylabel="kenar temas basıncı [MPa]")
a.set_title("(c) Kenar kesmesi — İNCELTMEK ZARARLI (∝1/d)", loc="left",
            fontweight="bold")
a.legend(fontsize=7.5, frameon=False); a.grid(alpha=.3)

# (d) MEKANIZMA 3: cekme + DUGUM, OLCULEN yakalama gerilmeleriyle
a = ax[3]
Fl = np.array([Ag(d_iplik=x*1e-3).F_kopma for x in dd])
a.plot(dd, Fl*DUGUMSUZ_VERIM, color=S3, lw=2.8, label="düğümsüz ağ dayanımı (%90)")
a.plot(dd, Fl*DUGUM_VERIMI["Dyneema_SK78"], color=S2, lw=2.8,
       label="düğümlü ağ dayanımı (%55)")
GZ = json.load(open("out/gazebo_yakalama_gerilme.json"))
mk = {"4.50": "v", "4.65": "o", "4.80": "^"}
for dk, mes in GZ.items():
    if dk.startswith("_"): continue
    for mk_, T in mes.items():
        a.plot(float(dk), T, mk[mk_], color=S1, ms=7, mec="white", mew=1.1,
               zorder=5)
for mk_, lb in (("4.50", "tetikleme 4.50 m"), ("4.65", "4.65 m"),
                ("4.80", "4.80 m")):
    a.plot([], [], mk[mk_], color=S1, ms=7, mec="white", label=lb)
a.axvline(MEVCUT, color=INK2, lw=1.3, ls=":")
a.invert_xaxis()
a.set(xlabel="iplik çapı [mm]", ylabel="yük / dayanım [N]", ylim=(0, 62))
a.set_title("(d) ÖLÇÜLEN yakalama yükü vs dayanım", loc="left",
            fontweight="bold")
a.legend(fontsize=7.2, frameon=False); a.grid(alpha=.3)

fig.suptitle("İPLİK İNCELTME KARARI — üç kesilme mekanizmasının çapa "
             "bağımlılığı FARKLI", fontsize=13.5, fontweight="bold",
             x=.045, ha="left", y=.945)
plt.savefig("out/ip_capi_karar.png", dpi=118)
print("-> out/ip_capi_karar.png")
