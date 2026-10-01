"""Kapsama <-> geri tepme odunlesimi (epsilon-kisit yontemi).

Tek amac olarak kapsamayi maksimize etmek kaba kuvvete kacar (DE cozumu:
Ø20 mm tungsten, 452 g bilye, 12.7 N.s geri tepme). Drone icin asil soru
"ne kadar geri tepmeye razisin" -> her butce icin en iyi kapsama.
"""
import sys; sys.path.insert(0,'/home/kayra/Masaüstü/ag_firlatma')
import numpy as np
from agsim.dse import sobol_ornekle, degerlendir_vektor, pareto_front, ADLAR, BILYE_SET

PNO = (8.0, 500.0)
MENZILLER = [2.0, 3.0, 4.0]

def deg(x):
    s, son = [], None
    for m in MENZILLER:
        d = degerlendir_vektor(x, menzil0=m, pnomatik=PNO)
        if not d["uygun"]: return None
        s.append(d["kapsama"]); son = d
    son["kapsama_ort"] = float(np.mean(s))
    return son

X = sobol_ornekle(13, seed=11)
R = [deg(x) for x in X]
idx = [i for i, d in enumerate(R) if d is not None]
print(f"Sobol {len(X)} tasarim -> {len(idx)} uygun (%{100*len(idx)/len(X):.1f})")
U = [R[i] for i in idx]; XU = X[idx]
K = np.array([d["kapsama_ort"] for d in U])
J = np.array([d["J_geri"] for d in U])
M = np.array([d["m_sistem"] for d in U])
E = np.array([d["E_depo"] for d in U])

print("\n=== GERI TEPME BUTCESINE GORE EN IYI KAPSAMA ===")
print(f"{'J_geri butce':>13} {'8kg dronede dV':>15} {'en iyi kapsama':>15} {'E':>7} {'m_sis':>7}")
for Jmax in [1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 9.0]:
    m = J <= Jmax
    if not m.any(): print(f"{Jmax:11.1f} N.s   --- uygun tasarim yok ---"); continue
    i = np.argmax(np.where(m, K, -1))
    print(f"{Jmax:11.1f} N.s {Jmax/8:14.2f} m/s {K[i]:15.3f} {E[i]:6.0f}J {M[i]:6.2f}kg")

msk = pareto_front(np.c_[K, J, M], [+1, -1, -1])
P = np.argsort(-K[msk])
print(f"\n=== PARETO CEPHESI (kapsama max / geri tepme min / kutle min): {msk.sum()} tasarim ===")
print(f"{'kapsama':>8} {'J_geri':>7} {'m_sis':>6} {'E':>6} {'D_bore':>7} {'D_bilye':>8} "
      f"{'mlz':>9} {'alpha':>6} {'R_ag':>6} {'goz':>6} {'d_ip':>7} {'v':>6}")
XP, UP = XU[msk], [U[i] for i in np.where(msk)[0]]
for i in P[:14]:
    x, d = XP[i], UP[i]
    print(f"{d['kapsama_ort']:8.3f} {d['J_geri']:7.2f} {d['m_sistem']:6.2f} {d['E_depo']:5.0f}J "
          f"{x[0]*1e3:6.1f} {x[6]*1e3:7.1f} {BILYE_SET[int(x[7])]:>9} {x[8]:5.1f}° "
          f"{x[10]:5.2f} {x[11]*1e3:5.0f} {x[12]*1e3:6.2f} {d['v_exit']:5.1f}")
np.save("out/pareto2_X.npy", XP)
