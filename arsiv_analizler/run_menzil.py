"""MENZIL calismasi: atis penceresinin YAKIN ve UZAK kenarini ne belirliyor?

Onceki MC SABIT 3 m tetikleme mesafesinde yapilmisti; "20 m/s ustu bir sey
kazandirmiyor" ifadesi yalnizca O MESAFE icin dogruydu. Menzili uzatmak
istiyorsak dogru soru: pencerenin UZAK kenari hizla nasil buyuyor?
"""
import os, sys
_K = os.path.abspath(__file__)
while _K != os.path.dirname(_K) and not os.path.isdir(os.path.join(_K, "agsim")):
    _K = os.path.dirname(_K)
sys.path.insert(0, _K)
import numpy as np
from agsim.dse import vektor_to_tasarim
from agsim.launcher import firlat_genel
from agsim.netfull import simule

R_GER = 0.75
X = np.load("out/x_final.npy")


def kur(R_ag=1.50, alpha_deg=None, kaba=False):
    t, _, _ = vektor_to_tasarim(X)
    t.kapsul.L_kapsul, t.kapsul.m_kapsul = 0.050, 0.032
    t.ag.R_ag = R_ag
    if alpha_deg is not None:
        t.kapsul.alpha_cep = np.radians(alpha_deg)
    t.ag.n_ring, t.ag.n_spoke = (5, 12) if kaba else (7, 18)
    return t


def pencere(t, v_hedef, m_yay=0.400, x0=0.25, T=0.60):
    """Atis penceresi: (yakin, uzak, R_max, t_Rmax, z_enacik)."""
    k = (t.m_hareketli + m_yay / 3) * v_hedef ** 2 / x0 ** 2
    L = firlat_genel(t, k, m_yay, x0, x0)
    if L.get("basarisiz"):
        return None
    S = simule(t, L, T=T, kayit=int(T * 400))
    R, ts, P, bd = S['R'], S['t'], S['P_snap'], S['bilye_dug']
    Z = np.array([p[bd, 2].mean() for p in P])
    i = int(np.argmax(R[:max(len(R) // 2, 2)]))       # ilk tepe
    j = i + int(np.argmin(R[i:]))
    m = (R >= R_GER) & (np.arange(len(R)) <= j)
    if not m.any():
        return None
    return dict(yakin=float(Z[m].min()), uzak=float(Z[m].max()),
                R_max=float(R.max()), t_Rmax=float(ts[i]),
                z_enacik=float(Z[i]), v=float(L["v_exit"]),
                J=float(L["J_geri"]), E=float(L["E_depo"]))


if __name__ == "__main__":
    print("=== A) HIZ SUPURMESI  (Ø3.0 m ag, koni 18°) ===")
    print(f"{'v_cikis':>8} {'YAKIN':>7} {'UZAK':>7} {'genislik':>9} "
          f"{'en acik@':>9} {'E':>6} {'J_geri':>7}")
    for v in [15, 20, 25, 30, 40, 55, 70]:
        r = pencere(kur(), v)
        if r is None:
            print(f"{v:7.0f}  --- ag {R_GER} m'ye ulasmiyor ---"); continue
        print(f"{r['v']:7.1f} {r['yakin']:6.2f}m {r['uzak']:6.2f}m "
              f"{r['uzak']-r['yakin']:8.2f}m {r['z_enacik']:8.2f}m "
              f"{r['E']:5.0f}J {r['J']:6.2f}")

    print("\n=== B) KONI ACISI SUPURMESI  (v=30 m/s sabit) ===")
    print(f"{'alpha':>6} {'YAKIN':>7} {'UZAK':>7} {'genislik':>9} {'t_Rmax':>8}")
    for a in [8, 12, 18, 25, 35]:
        r = pencere(kur(alpha_deg=a), 30)
        if r is None:
            print(f"{a:5.0f}°  --- acilmiyor ---"); continue
        print(f"{a:5.0f}° {r['yakin']:6.2f}m {r['uzak']:6.2f}m "
              f"{r['uzak']-r['yakin']:8.2f}m {r['t_Rmax']*1e3:6.0f}ms")

    print("\n=== C) HIZ x KONI: UZAK KENARI EN COK NE BUYUTUR? ===")
    print(f"{'':>6} " + " ".join(f"{a:>6.0f}°" for a in [8, 12, 18, 25]))
    for v in [20, 30, 45]:
        sat = []
        for a in [8, 12, 18, 25]:
            r = pencere(kur(alpha_deg=a), v)
            sat.append(f"{r['uzak']:6.2f}" if r else "   --- ")
        print(f"{v:5.0f}m/s " + " ".join(sat))
