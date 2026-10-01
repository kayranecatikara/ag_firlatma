"""Yakalama olasiligi: yay vs pnomatik, tetikleme mesafesine gore."""
import sys; sys.path.insert(0,'/home/kayra/Masaüstü/ag_firlatma')
import numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from agsim.params import Tasarim
from agsim.launcher import firlat
from agsim.pneumatic import firlat_pnomatik
from agsim.netrom import uc
from agsim.engagement import degerlendir
from run_montecarlo import BELIRSIZ

def yap(alpha=18):
    t = Tasarim(); t.namlu.L_namlu = 0.300
    t.bilye.D, t.bilye.malzeme = 12.6e-3, "Kursun"
    t.kapsul.R_pitch = 0.5*39e-3-0.5*12.6e-3-0.5e-3
    t.kapsul.alpha_cep = np.radians(alpha)
    t.ag.R_ag, t.ag.goz, t.ag.d_iplik = 0.95, 0.085, 0.22e-3
    t.yay.d_tel, t.yay.D_orta, t.yay.n_aktif = 3.52e-3, 34.5e-3, 21.0
    t.yay.x0 = 0.169; t.yay.L_serbest = 0.300 - t.kapsul.L_kapsul
    return t

def mc(alpha, menzil, pno, n=300, seed=5):
    rng = np.random.default_rng(seed); ok = 0
    for _ in range(n):
        t = yap(alpha)
        t.yay.d_tel *= (1+BELIRSIZ["k_yay"]*rng.normal()/4)
        t.kapsul.m_kapsul *= (1+BELIRSIZ["m_kapsul"]*rng.normal())
        t.namlu.mu_surtunme *= max(.1, 1+BELIRSIZ["mu"]*rng.normal())
        t.kapsul.alpha_cep = max(0., t.kapsul.alpha_cep+BELIRSIZ["alpha"]*rng.normal())
        t.ang.menzil0 = max(.5, menzil+BELIRSIZ["menzil"]*rng.normal())
        t.ang.V_hedef += BELIRSIZ["V_hedef"]*rng.normal()
        t.hava.ruzgar = np.array([BELIRSIZ["ruzgar"]*rng.normal(), 0., 0.])
        try:
            L = firlat_pnomatik(t, *pno) if pno else firlat(t)
            if L.get("basarisiz"): continue
            ok += bool(degerlendir(t, uc(t, L, T=0.9))["basari"])
        except Exception: pass
    return ok/n

menziller = np.array([1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0])
fig, ax = plt.subplots(figsize=(8.5, 5.2))
for ad, alpha, pno, st in [("Yay 300 mm, $\\alpha$=18°", 18, None, "r--o"),
                           ("Yay 300 mm, $\\alpha$=25°", 25, None, "r-.s"),
                           ("Pnömatik 8 bar/500cc, $\\alpha$=18°", 18, (8.,500.), "b-o"),
                           ("Pnömatik 8 bar/500cc, $\\alpha$=25°", 25, (8.,500.), "b--s")]:
    P = [mc(alpha, m, pno) for m in menziller]
    ax.plot(menziller, 100*np.array(P), st, label=ad, lw=2, ms=6)
    print(ad, [f"{100*p:.0f}%" for p in P])
ax.set(xlabel="tetikleme mesafesi [m]", ylabel="yakalama olasılığı [%]", ylim=(-2, 100),
       title="Gürbüzlük: 100 km/h'te yakalama olasılığı\n"
             "(Monte Carlo n=300; tetik ±0.6 m, sürtünme ±%30, rüzgâr ±3 m/s, koni ±2°)")
ax.legend(fontsize=9); ax.grid(alpha=.35)
plt.tight_layout(); plt.savefig("out/yakalama.png", dpi=130)
print("-> out/yakalama.png")
