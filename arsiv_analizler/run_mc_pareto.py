"""Pareto adaylarinin gurbuzluk dogrulamasi (deterministik optimum != gurbuz optimum)."""
import os, sys
_K = os.path.abspath(__file__)
while _K != os.path.dirname(_K) and not os.path.isdir(os.path.join(_K, "agsim")):
    _K = os.path.dirname(_K)
sys.path.insert(0, _K)
import numpy as np
from agsim.dse import vektor_to_tasarim, BILYE_SET
from agsim.pneumatic import firlat_pnomatik
from agsim.netrom import uc
from agsim.engagement import degerlendir
from run_montecarlo import BELIRSIZ
PNO = (8.0, 500.0)

def mc(x, menzil, n=250, seed=17):
    rng = np.random.default_rng(seed); ok = 0
    for _ in range(n):
        t, uy, _ = vektor_to_tasarim(x)
        if not uy: return 0.0
        t.kapsul.m_kapsul *= (1+BELIRSIZ["m_kapsul"]*rng.normal())
        t.namlu.mu_surtunme *= max(.1, 1+BELIRSIZ["mu"]*rng.normal())
        t.kapsul.alpha_cep = max(0., t.kapsul.alpha_cep+BELIRSIZ["alpha"]*rng.normal())
        t.ang.menzil0 = max(.5, menzil+BELIRSIZ["menzil"]*rng.normal())
        t.ang.V_hedef += BELIRSIZ["V_hedef"]*rng.normal()
        t.hava.ruzgar = np.array([BELIRSIZ["ruzgar"]*rng.normal(), 0., 0.])
        p0 = PNO[0]*(1+0.06*rng.normal())          # regulator toleransi
        try:
            L = firlat_pnomatik(t, p0, PNO[1])
            if L.get("basarisiz"): continue
            ok += bool(degerlendir(t, uc(t, L, T=0.9))["basari"])
        except Exception: pass
    return ok/n

XP = np.load("out/pareto2_X.npy")
print(f"{'#':>2} {'alpha':>6} {'yiv':>12} {'D_bilye':>9} {'mlz':>9} {'R_ag':>5} "
      f"{'P@2m':>6} {'P@3m':>6} {'P@4m':>6}")
for i, x in enumerate(XP):
    tw = x[9]; yiv = "duz" if tw < 0.5 else f"{1000/tw:.0f} mm/tur"
    ps = [mc(x, m) for m in (2., 3., 4.)]
    print(f"{i:2d} {x[8]:5.1f}° {yiv:>12} {x[6]*1e3:8.1f} {BILYE_SET[int(x[7])]:>9} "
          f"{x[10]:5.2f} {100*ps[0]:5.0f}% {100*ps[1]:5.0f}% {100*ps[2]:5.0f}%")
