"""Secilen tasarimlari YUKSEK COZUNURLUKLU model ile dogrular + Pareto grafigi.

ROM tasarim kesfi icin hizlidir ama yaklasiktir. Pareto'daki adaylar mutlaka
burada dogrulanmalidir - ozellikle YAVAS ACILAN (kucuk alpha) tasarimlar,
cunku ROM'un en az guvenilir oldugu rejim odur.
"""
import os, sys
_K = os.path.abspath(__file__)
while _K != os.path.dirname(_K) and not os.path.isdir(os.path.join(_K, "agsim")):
    _K = os.path.dirname(_K)
sys.path.insert(0, _K)
import numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from agsim.dse import vektor_to_tasarim, degerlendir_vektor, ADLAR, BILYE_SET
from agsim.launcher import firlat
from agsim.netrom import uc
from agsim.netfull import simule
from agsim.engagement import etkin_menzil

# ---------------------------------------------------------------- 1) dogrulama
x = np.load("out/x_opt.npy")
t, ok, _ = vektor_to_tasarim(x)
t.ag.n_ring, t.ag.n_spoke = 6, 12
L = firlat(t)
M = uc(t, L, T=0.8)
S = simule(t, L, T=0.45)
R_ger = 0.5*t.ang.hedef_kanat
print("=== OPTIMUM TASARIM DOGRULAMASI ===")
print(f"  ROM : R_max={M['R'].max():.3f} m @ {M['t'][np.argmax(M['R'])]*1e3:.0f} ms  "
      f"R_eff={etkin_menzil(M, R_ger):.2f} m")
print(f"  TAM : R_max={S['R'].max():.3f} m @ {S['t'][np.argmax(S['R'])]*1e3:.0f} ms  "
      f"T_iplik_tepe={S['T_max'].max():.1f} N / kopma {t.ag.F_kopma:.0f} N")
print(f"  sapma: R_max %{100*(M['R'].max()-S['R'].max())/S['R'].max():+.1f}")

# ---------------------------------------------------------------- 2) grafikler
df = pd.read_csv("out/sobol.csv"); U = df[df.uygun]
P = pd.read_csv("out/pareto.csv")
fig, ax = plt.subplots(1, 3, figsize=(16, 4.6))

sc = ax[0].scatter(U.E_depo, U.R_eff, c=U.m_sistem, s=14, cmap="plasma", alpha=.65)
ax[0].plot(P.E_depo.values, P.R_eff.values, "k.", ms=9)
Ps=P.sort_values("E_depo"); ax[0].plot(Ps.E_depo.values, Ps.R_eff.values, "k--", lw=1)
plt.colorbar(sc, ax=ax[0], label="sistem kutlesi [kg]")
ax[0].set(xlabel="depolanan yay enerjisi [J]", ylabel="etkin menzil [m]",
          title="(a) Pareto: menzil - enerji")
ax[0].grid(alpha=.3)

sc = ax[1].scatter(U.v_exit, U.v_radyal, c=U.R_eff, s=14, cmap="viridis")
plt.colorbar(sc, ax=ax[1], label="etkin menzil [m]")
ax[1].set(xlabel="namlu cikis hizi [m/s]", ylabel="radyal acilma hizi [m/s]",
          title="(b) Hiz bolusumu  (eksenel <-> radyal odunlesimi)")
ax[1].grid(alpha=.3)

ax[2].plot(S["t"]*1e3, S["R"], "tab:blue", lw=2, label="tam model (kutle-yay-sonum.)")
ax[2].plot(M["t"]*1e3, M["R"], "tab:orange", ls="--", lw=2, label="ROM (hizli)")
ax[2].axhline(R_ger, ls=":", c="k", label="gerekli yaricap")
ax[2].set(xlabel="zaman [ms]", ylabel="ag yaricapi R [m]", xlim=(0, 450),
          title="(c) Model dogrulamasi (optimum tasarim)")
ax[2].legend(fontsize=8); ax[2].grid(alpha=.3)
plt.tight_layout(); plt.savefig("out/dse.png", dpi=130)
print("-> out/dse.png")
