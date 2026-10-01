"""HIPOTEZ: kucuk koni acisini olduren sey IMALAT TOLERANSI.

v_radyal ~ v * tan(alpha). +-2 derecelik yuva acisi toleransi
  8 derecede  -> v_radyal'de  %25 bagil hata
 18 derecede  -> v_radyal'de  %11 bagil hata
Kucuk acida atis penceresi cok kaydigi icin gurbuzluk cokuyor.
Toleransi sikarsak kucuk aci (=uzun menzil) kullanilabilir hale gelir mi?
"""
import sys
sys.path.insert(0, '/home/kayra/Masaüstü/ag_firlatma')
import numpy as np
from agsim.dse import vektor_to_tasarim
from agsim.launcher import firlat_genel
from agsim.netfull import simule

R_GER = 0.75
X = np.load("out/x_final.npy")


def tek(alpha_deg, v_hedef, menzil, rng, sig_aci_deg=2.0, m_yay=0.400, x0=0.25):
    t, _, _ = vektor_to_tasarim(X)
    t.kapsul.L_kapsul, t.kapsul.m_kapsul = 0.050, 0.032
    t.ag.R_ag = 1.50
    t.ag.n_ring, t.ag.n_spoke = 5, 12
    t.kapsul.alpha_cep = max(0.0, np.radians(alpha_deg + sig_aci_deg * rng.normal()))
    t.kapsul.m_kapsul *= (1 + 0.08 * rng.normal())
    t.namlu.mu_surtunme *= max(.1, 1 + 0.30 * rng.normal())
    t.hava.ruzgar = np.array([3.0 * rng.normal(), 0., 0.])
    k = (t.m_hareketli + m_yay / 3) * v_hedef ** 2 / x0 ** 2 * (1 + 0.05 * rng.normal())
    L = firlat_genel(t, k, m_yay, x0, x0)
    if L.get("basarisiz"):
        return False
    S = simule(t, L, T=0.70, kayit=120)
    R, ts, P, bd = S['R'], S['t'], S['P_snap'], S['bilye_dug']
    Z = np.array([p[bd, 2].mean() for p in P])
    i = int(np.argmax(R[:max(len(R) // 2, 2)]))
    j = i + int(np.argmin(R[i:]))
    m = (R >= R_GER) & (np.arange(len(R)) <= j)
    return bool(m.any() and Z[m].min() <= menzil <= Z[m].max())


def mc(alpha, menzil, sig_menzil, sig_aci, n=55, seed=53):
    rng = np.random.default_rng(seed)
    ok = 0
    for _ in range(n):
        try:
            ok += tek(alpha, 20.0, max(0.5, menzil + sig_menzil * rng.normal()),
                      rng, sig_aci_deg=sig_aci)
        except Exception:
            pass
    return ok / n


if __name__ == "__main__":
    N = 55
    print(f"=== YUVA ACISI TOLERANSININ ETKISI  (v=20 m/s, Ø3.0 m ağ, n={N}) ===")
    print(f"  Mesafeölçer σ = 0.25 m sabit.\n")
    print(f"{'alpha':>6} {'tetik@':>8} {'pencere':>14} {'±2.0° (baskı)':>14} "
          f"{'±0.5° (işlenmiş)':>17}")
    # v=20 m/s'deki GERCEK pencere ortalari (run_menzil.pencere ile olculdu)
    for a, menzil, gen in [(8, 4.05, "3.66-4.43"), (12, 3.40, "2.85-3.95"),
                           (18, 2.62, "1.98-3.26"), (25, 1.98, "1.37-2.58")]:
        p2 = mc(a, menzil, 0.25, 2.0, N)
        p05 = mc(a, menzil, 0.25, 0.5, N)
        print(f"{a:5.0f}° {menzil:7.2f}m {gen:>14} {100*p2:13.0f}% {100*p05:16.0f}%",
              flush=True)
