"""Gurbuzluk MC'si TAM 3B model ile (ROM mesafeyi dusuk tahmin ettigi icin).

ROM yaricapta dogru ama menzilde yaniltici: agir bilyelerin hafif agi
pesinden cekmesini goremiyor. Yay rejiminde bu fark karar degistiriyor.
"""
import sys; sys.path.insert(0,'/home/kayra/Masaüstü/ag_firlatma')
import numpy as np
from agsim.dse import vektor_to_tasarim
from agsim.launcher import firlat_genel
from agsim.netfull import simule

R_GER = 0.75
x = np.load("out/x_final.npy")

def tek(v_hedef, menzil, rng, m_yay=0.500, x0=0.25, R_ag=1.50):
    t, _, _ = vektor_to_tasarim(x)
    t.kapsul.L_kapsul, t.kapsul.m_kapsul = 0.050, 0.032
    t.ag.R_ag = R_ag
    t.ag.n_ring, t.ag.n_spoke = 5, 12            # kaba ag (hiz icin)
    t.kapsul.m_kapsul *= (1+0.08*rng.normal())
    t.namlu.mu_surtunme *= max(.1, 1+0.30*rng.normal())
    t.kapsul.alpha_cep = max(0., t.kapsul.alpha_cep + 0.035*rng.normal())
    k = (t.m_hareketli + m_yay/3)*v_hedef**2/x0**2 * (1+0.05*rng.normal())
    L = firlat_genel(t, k, m_yay, x0, x0)
    if L.get("basarisiz"): return False
    S = simule(t, L, T=0.45, kayit=90)
    R, ts, P, bd = S['R'], S['t'], S['P_snap'], S['bilye_dug']
    Z = np.array([p[bd,2].mean() for p in P])
    i = int(np.argmax(R[:len(R)//2]))             # ilk tepe
    j = i + int(np.argmin(R[i:]))
    m = (R >= R_GER) & (np.arange(len(R)) <= j)
    if not m.any(): return False
    return bool(Z[m].min() <= menzil <= Z[m].max())

def mc(v, menzil, sig, n, seed=31):
    rng = np.random.default_rng(seed); ok = 0
    for _ in range(n):
        try:
            ok += tek(v, max(0.5, menzil + sig*rng.normal()), rng)
        except Exception: pass
    return ok/n

if __name__ == "__main__":
    N = 90
    print(f"=== YAY MIMARISI - TAM MODEL MC (n={N}, Ø3.0 m ag) ===")
    print(f"{'v_cikis':>8} {'tetik@':>7} {'sig=0.60':>9} {'sig=0.25':>9} {'sig=0.10':>9}")
    for v in [20, 25, 30]:
        for menzil in [2.5, 3.0]:
            r = [mc(v, menzil, s, N) for s in (0.60, 0.25, 0.10)]
            print(f"{v:7.0f} {menzil:6.1f}m {100*r[0]:8.0f}% {100*r[1]:8.0f}% {100*r[2]:8.0f}%",
                  flush=True)
