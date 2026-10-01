"""Kucuk koni acisi menzili uzatiyor - ama GURBUZ MU?

alpha=8 derecede ag 272 ms'de aciliyor. Uzun acilma suresi, bu oturumda
defalarca goruldugu gibi, gurbuzlugu bozabiliyor. Tam model MC ile test.
"""
import sys
sys.path.insert(0, '/home/kayra/Masaüstü/ag_firlatma')
import numpy as np
from agsim.dse import vektor_to_tasarim
from agsim.launcher import firlat_genel
from agsim.netfull import simule

R_GER = 0.75
X = np.load("out/x_final.npy")


def tek(alpha_deg, v_hedef, menzil, rng, m_yay=0.400, x0=0.25):
    t, _, _ = vektor_to_tasarim(X)
    t.kapsul.L_kapsul, t.kapsul.m_kapsul = 0.050, 0.032
    t.ag.R_ag = 1.50
    t.ag.n_ring, t.ag.n_spoke = 5, 12
    t.kapsul.alpha_cep = max(0.0, np.radians(alpha_deg) + 0.035 * rng.normal())
    t.kapsul.m_kapsul *= (1 + 0.08 * rng.normal())
    t.namlu.mu_surtunme *= max(.1, 1 + 0.30 * rng.normal())
    t.hava.ruzgar = np.array([3.0 * rng.normal(), 0., 0.])
    k = (t.m_hareketli + m_yay / 3) * v_hedef ** 2 / x0 ** 2 * (1 + 0.05 * rng.normal())
    L = firlat_genel(t, k, m_yay, x0, x0)
    if L.get("basarisiz"):
        return False
    S = simule(t, L, T=0.70, kayit=140)
    R, ts, P, bd = S['R'], S['t'], S['P_snap'], S['bilye_dug']
    Z = np.array([p[bd, 2].mean() for p in P])
    i = int(np.argmax(R[:max(len(R) // 2, 2)]))
    j = i + int(np.argmin(R[i:]))
    m = (R >= R_GER) & (np.arange(len(R)) <= j)
    return bool(m.any() and Z[m].min() <= menzil <= Z[m].max())


def mc(alpha, v, menzil, sig, n=70, seed=41):
    rng = np.random.default_rng(seed)
    ok = 0
    for _ in range(n):
        try:
            ok += tek(alpha, v, max(0.5, menzil + sig * rng.normal()), rng)
        except Exception:
            pass
    return ok / n


if __name__ == "__main__":
    N = 70
    print(f"=== KONI ACISI GURBUZLUK TESTI (v=20 m/s, Ø3.0 m ag, n={N}) ===")
    print("  Her aci kendi pencere ORTASINDA tetikleniyor.")
    print(f"\n{'alpha':>6} {'tetik@':>8} {'sig=0.60':>9} {'sig=0.25':>9} {'sig=0.10':>9}")
    # A bolumundeki pencere ortalari (v=20): 8->3.1, 12->2.8, 18->2.6
    for a, menzil in [(8, 3.3), (12, 3.0), (18, 2.6), (25, 2.1)]:
        r = [mc(a, 20, menzil, s, N) for s in (0.60, 0.25, 0.10)]
        print(f"{a:5.0f}° {menzil:7.1f}m {100*r[0]:8.0f}% {100*r[1]:8.0f}% {100*r[2]:8.0f}%",
              flush=True)
