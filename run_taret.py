"""TARET KISITI: kisa namluda ne elde edilir?

Tasarladigim namlu 486 mm. Fotograflardaki taret muhafazasi bunun cok
altinda gorunuyor. Bu betik, verilen TOPLAM namlu boyu icin:
  - yay ile ulasilabilecek en iyi cikis hizi (gerilme + blok boyu kisitli)
  - pnomatik ile ulasilabilecek cikis hizi
  - ve bunlarin atis penceresine yansimasini
hesaplar.

Yerlesim:  L_namlu = L_yay_kurulu + L_kapsul + STROK + (omuz 4 + koni 22)
Pnomatikte L_yay_kurulu yoktur -> ayni boyda COK DAHA UZUN strok.
"""
import sys
sys.path.insert(0, '/home/kayra/Masaüstü/ag_firlatma')
import numpy as np
from scipy.optimize import differential_evolution
from agsim.dse import vektor_to_tasarim
from agsim.launcher import firlat_genel
from agsim.pneumatic import firlat_pnomatik
from agsim.yay_coklu import yay_k, yay_m, yay_tau, tau_izin
from agsim.netfull import simule

L_KAPSUL, L_UC = 50.0, 26.0      # kapsul + (omuz + agiz konisi)
SF_MIN = 1.25
R_GER = 0.75
X = np.load("out/x_final.npy")


def tasarim(L_namlu_mm):
    t, _, _ = vektor_to_tasarim(X)
    t.kapsul.L_kapsul, t.kapsul.m_kapsul = 0.050, 0.032
    t.ag.R_ag = 1.50
    t.kapsul.alpha_cep = np.radians(18)
    t.namlu.L_namlu = L_namlu_mm * 1e-3
    t.ag.n_ring, t.ag.n_spoke = 7, 18
    return t


def en_iyi_yay(L_namlu_mm):
    """Verilen namlu boyunda en yuksek v_exit'i veren yay."""
    t = tasarim(L_namlu_mm)
    L_kul = L_namlu_mm - L_KAPSUL - L_UC        # yay + strok [mm]
    if L_kul <= 20:
        return None

    def amac(p):
        d_mm, C, n, orn = p
        d = d_mm * 1e-3; Dm = C * d
        x0 = orn * L_kul * 1e-3                 # strok
        L_cocked = (L_kul * 1e-3) - x0
        if L_cocked < (n + 2) * d:              # blok boyu
            return 50.0
        if Dm + d > t.namlu.D_bore - 1.5e-3:
            return 50.0
        k = yay_k(d, Dm, n); my = yay_m(d, Dm, n)
        if tau_izin(d) / yay_tau(d, Dm, k * x0) < SF_MIN:
            return 50.0
        L = firlat_genel(t, k, my, x0, x0)
        return 50.0 if L.get("basarisiz") else -L["v_exit"]

    r = differential_evolution(amac, [(2.0, 6.0), (5.0, 10.0), (6.0, 60.0),
                                      (0.25, 0.80)],
                               seed=3, maxiter=120, popsize=18, tol=1e-9,
                               polish=False, init='sobol')
    if r.fun > 40:
        return None
    d_mm, C, n, orn = r.x
    d = d_mm * 1e-3; Dm = C * d; x0 = orn * L_kul * 1e-3
    k = yay_k(d, Dm, n); my = yay_m(d, Dm, n)
    L = firlat_genel(t, k, my, x0, x0)
    return dict(v=L["v_exit"], k=k, m_yay=my, x0=x0, d=d_mm, Dm=Dm * 1e3, n=n,
                F=k * x0, SF=tau_izin(d) / yay_tau(d, Dm, k * x0), L=L, t=t)


def pnomatik(L_namlu_mm, p0=8.0, V0=500.0):
    t = tasarim(L_namlu_mm)
    L = firlat_pnomatik(t, p0, V0)
    return None if L.get("basarisiz") else dict(v=L["v_exit"], L=L, t=t)


def pencere(t, L):
    S = simule(t, L, T=0.80, kayit=320)
    R, ts, P, bd = S['R'], S['t'], S['P_snap'], S['bilye_dug']
    Z = np.array([p[bd, 2].mean() for p in P])
    i = int(np.argmax(R[:len(R) // 2])); j = i + int(np.argmin(R[i:]))
    m = (R >= R_GER) & (np.arange(len(R)) <= j)
    return (Z[m].min(), Z[m].max()) if m.any() else (np.nan, np.nan)


if __name__ == "__main__":
    print("=== TARET KISITI: namlu boyuna gore performans ===")
    print("  (ag Ø3.0 m, alpha=18°, hedef 100 km/h, drone 100 km/h)\n")
    print(f"{'namlu':>7} {'YAY v':>7} {'strok':>7} {'F_kurma':>8} "
          f"{'PNÖ v':>7} {'PNÖ strok':>10}")
    sonuc = {}
    for Ln in [180, 220, 260, 300, 380, 486]:
        y = en_iyi_yay(Ln)
        pn = pnomatik(Ln)
        sonuc[Ln] = (y, pn)
        sy = f"{y['v']:6.1f}" if y else "   --  "
        sx = f"{y['x0']*1e3:6.0f}mm" if y else "   --  "
        sf = f"{y['F']:7.0f}N" if y else "   --  "
        sp = f"{pn['v']:6.1f}" if pn else "   --  "
        spx = f"{pn['L']['strok']*1e3:8.0f}mm" if pn else "   --  "
        print(f"{Ln:5.0f}mm {sy} {sx} {sf} {sp} {spx}", flush=True)

    print(f"\n=== ATIS PENCERESI (tam 3B model) ===")
    print(f"{'namlu':>7} {'kaynak':>10} {'v':>7} {'pencere':>17} {'genişlik':>9}")
    for Ln in [180, 260, 380, 486]:
        y, pn = sonuc[Ln]
        for ad, r in (("YAY", y), ("PNÖMATİK", pn)):
            if r is None:
                continue
            a, b = pencere(r["t"], r["L"])
            if not np.isfinite(a):
                print(f"{Ln:5.0f}mm {ad:>10} {r['v']:6.1f}  --- ağ açılmıyor ---")
            else:
                print(f"{Ln:5.0f}mm {ad:>10} {r['v']:6.1f} {a:9.2f} – {b:5.2f} m "
                      f"{b-a:8.2f} m", flush=True)
