"""Faz-4: Gurbuzluk (robustness) analizi.

Deterministik optimum, imalat/nisan/zamanlama sacilmasi altinda cokebilir.
Bir tasarimi SECMEDEN once bu kosulmalidir: aranan sey en yuksek R_eff degil,
en yuksek YAKALAMA OLASILIGI'dir.
"""
import os, sys
_K = os.path.abspath(__file__)
while _K != os.path.dirname(_K) and not os.path.isdir(os.path.join(_K, "agsim")):
    _K = os.path.dirname(_K)
sys.path.insert(0, _K)
import numpy as np
from agsim.dse import vektor_to_tasarim
from agsim.launcher import firlat
from agsim.netrom import uc
from agsim.engagement import degerlendir

# belirsizlikler (1-sigma)
BELIRSIZ = dict(
    k_yay      = 0.05,    # yay sertligi toleransi (%)
    m_kapsul   = 0.08,    # baski kutlesi sacilmasi (%)
    mu         = 0.30,    # surtunme katsayisi (%) - EN BUYUK BILINMEZ
    alpha      = 0.035,   # cep acisi imalat hatasi [rad] ~ 2 deg
    menzil     = 0.60,    # tetikleme mesafesi hatasi [m]
    V_hedef    = 2.0,     # hedef hiz kestirim hatasi [m/s]
    ruzgar     = 3.0,     # ruzgar [m/s]
)

def kosum(x, n=600, seed=0, menzil_nom=3.0):
    rng = np.random.default_rng(seed)
    basari = 0; R_k = []
    for _ in range(n):
        t, ok, _ = vektor_to_tasarim(x)
        if not ok: return 0.0, np.array([])
        t.yay.d_tel      *= (1+BELIRSIZ["k_yay"]*rng.normal()/4)   # k ~ d^4
        t.kapsul.m_kapsul*= (1+BELIRSIZ["m_kapsul"]*rng.normal())
        t.namlu.mu_surtunme *= max(0.1, 1+BELIRSIZ["mu"]*rng.normal())
        t.kapsul.alpha_cep = max(0.0, t.kapsul.alpha_cep + BELIRSIZ["alpha"]*rng.normal())
        t.ang.menzil0    = max(0.5, menzil_nom + BELIRSIZ["menzil"]*rng.normal())
        t.ang.V_hedef   += BELIRSIZ["V_hedef"]*rng.normal()
        t.hava.ruzgar    = np.array([BELIRSIZ["ruzgar"]*rng.normal(), 0., 0.])
        try:
            L = firlat(t)
            if L.get("basarisiz"): continue
            F = uc(t, L, T=0.8); E = degerlendir(t, F)
        except Exception:
            continue
        basari += bool(E["basari"])
        if np.isfinite(E["R_kesisme"]): R_k.append(E["R_kesisme"])
    return basari/n, np.array(R_k)

if __name__ == "__main__":
    x = np.load("out/x_opt.npy")
    print("=== GURBUZLUK (Monte Carlo, n=600) ===")
    print(f"{'tetik mesafesi':>16} {'P_yakalama':>12} {'R_kesisme ort':>15} {'std':>8}")
    for m in [1.5, 2.0, 2.5, 3.0, 4.0]:
        p, R = kosum(x, n=600, seed=11, menzil_nom=m)
        print(f"{m:13.1f} m {100*p:11.1f}% "
              f"{(R.mean() if len(R) else np.nan):14.3f} m {(R.std() if len(R) else np.nan):7.3f}")
