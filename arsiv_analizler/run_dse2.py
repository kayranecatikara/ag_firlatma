"""Duzeltilmis DSE: amac = KESISME ANINDAKI kapsama, birden cok tetik mesafesinde.

R_eff'i amac almak hataliydi: cok yavas acilan bir ag paket halinde uzaga gidip
R_eff'i buyuk gosterir, ama her gercekci tetikleme mesafesinde hala kapalidir
(Monte Carlo: %0 yakalama). Dogru amac, agin HEDEFE VARDIGINDA acik olmasidir.
"""
import os, sys
_K = os.path.abspath(__file__)
while _K != os.path.dirname(_K) and not os.path.isdir(os.path.join(_K, "agsim")):
    _K = os.path.dirname(_K)
sys.path.insert(0, _K)
import numpy as np
from scipy.optimize import differential_evolution
from agsim.dse import degerlendir_vektor, ALT, UST, ADLAR, BILYE_SET

MENZILLER = [2.0, 3.0, 4.0]
PNO = (8.0, 500.0)          # 8 bar, 500 cm3 depo

def amac(x):
    s = []
    for m in MENZILLER:
        d = degerlendir_vektor(x, menzil0=m, pnomatik=PNO)
        if not d["uygun"]:
            return 10.0
        s.append(d["kapsama"])
    return -float(np.mean(s))       # 3 mesafede de iyi olmali (gurbuz)

if __name__ == "__main__":
    r = differential_evolution(amac, list(zip(ALT, UST)), seed=5, maxiter=70,
                               popsize=16, tol=1e-10, polish=False, init='sobol')
    print(f"ort. kapsama (2/3/4 m) = {-r.fun:.3f}   (1.0 = hedefi tam ortuyor)")
    for a, v in zip(ADLAR, r.x):
        if a == "mlz_bilye":  print(f"  {a:11s} = {BILYE_SET[int(v)]}")
        elif a == "twist_inv":print(f"  yiv         = {'duz' if v<0.5 else f'{1000/v:.0f} mm/tur'}")
        else:                 print(f"  {a:11s} = {v:.5g}")
    for m in MENZILLER:
        d = degerlendir_vektor(r.x, menzil0=m, pnomatik=PNO)
        print(f"  @{m} m: kapsama={d['kapsama']:.3f} R_kes={d['R_kesisme']:.2f}m "
              f"v={d['v_exit']:.1f} vR={d['v_radyal']:.2f} t_ac={d['t_acilma']*1e3:.0f}ms "
              f"E={d['E_depo']:.0f}J J_geri={d['J_geri']:.2f} F_sok={d['F_sok']:.0f}N")
    np.save("out/x_opt2.npy", r.x)
    print("-> out/x_opt2.npy")
