"""NAMLU BOYU <-> MENZIL <-> KURMA KUVVETI (duzeltilmis model, yeni yerlesim).

Yeni yerlesim (omuz YOK — omuz bilyelerin yolunu kesiyordu):
  y=0 acik arka | 5 mm pay | kapsul (L_kap) | STROK s | koni | agiz
  Kapsul, capraz pimin yarik SONUNA carpmasiyla durur (+ TPU tampon).
  Bant, capraz pim durdugu anda tam gevsek olacak sekilde boyutlanir:
      L0 = s/(lam-1),   D_son = L0 + H,   lam_kurulu = 3.5
  Namlu boyu:  L = 5 + 4.5 + s + D_son + 3   (ve kapsul agzi <= namlu agzi)
Bant kesiti kurma kuvveti sinirindan (servo secimi) belirlenir.
"""
import os, sys
_K = os.path.abspath(__file__)
while _K != os.path.dirname(_K) and not os.path.isdir(os.path.join(_K, "agsim")):
    _K = os.path.dirname(_K)
sys.path.insert(0, _K)
import numpy as np
from agsim.lastik import Bant, firlat_lastik
from run_lastik import tasarim
from run_taret import pencere

LAM, H, G, N = 3.5, 0.018, 0.45e6, 2
HAZNE_A, PAKET_DOL = 1081e-6, 0.30


def yerlesim(s, L_hazne):
    L_kap = 24.0e-3 + max(L_hazne, 6e-3)
    L0 = s / (LAM - 1)
    D_son = L0 + H
    L = max(5e-3 + 4.5e-3 + s + D_son + 3e-3, 5e-3 + L_kap + s + 6e-3)
    m_kap = 0.0232 * (L_kap / 0.050) + 0.0057
    return L, L_kap, L0, D_son, m_kap


def kos(s, F_max, R_ag, goz, d_ip, mlz, alpha):
    t = tasarim(alpha, False)
    t.ag.R_ag, t.ag.goz, t.ag.d_iplik = R_ag, goz, d_ip
    t.bilye.malzeme, t.bilye.D = mlz, 12.7e-3
    V_ip = np.pi * 0.25 * d_ip ** 2 * t.ag.L_iplik
    L_hazne = V_ip / PAKET_DOL / HAZNE_A
    L, L_kap, L0, D_son, m_kap = yerlesim(s, L_hazne)
    t.kapsul.m_kapsul, t.kapsul.L_kapsul = m_kap, L_kap
    t.namlu.L_namlu = L
    A0 = F_max / (N * G * (LAM - 1 / LAM ** 2))
    OD = np.sqrt(4 * A0 / np.pi + (4e-3) ** 2)
    b = Bant(n=N, OD=OD, ID=4e-3, L0=L0, H=H, Gmod=G)
    Lr = firlat_lastik(t, b, D_son + s, s)
    lo, hi = pencere(t, Lr)
    return dict(L=L, s=s, L_kap=L_kap, OD=OD, L0=L0, E=Lr["E_depo"], v=Lr["v_exit"],
                F=Lr["F_kurma"], m_bant=b.m, lo=lo, hi=hi,
                w=(hi - lo) if np.isfinite(lo) else 0.0)


if __name__ == "__main__":
    import ast
    ag = ast.literal_eval(sys.argv[1]) if len(sys.argv) > 1 else (1.1, 0.13, 0.16e-3, "Kursun", 16)
    R_ag, goz, d_ip, mlz, a = ag
    print(f"AG: R={R_ag} m, goz {goz*1e3:.0f} mm, ip {d_ip*1e3:.3f} mm, {mlz}, alpha {a}\n")
    print(f"{'namlu':>7} {'strok':>6} {'F_kurma':>8} {'bant OD':>8} {'L0':>6} "
          f"{'E':>6} {'v':>6} {'pencere':>14} {'genislik':>9}")
    for F_max in (450, 600, 750):
        for s in (0.080, 0.100, 0.120, 0.140, 0.165):
            r = kos(s, F_max, R_ag, goz, d_ip, mlz, a)
            pen = f"{r['lo']:5.2f}-{r['hi']:5.2f}" if np.isfinite(r["lo"]) else "  acilmiyor "
            print(f"{r['L']*1e3:5.0f}mm {s*1e3:4.0f}mm {r['F']:7.0f}N "
                  f"{r['OD']*1e3:6.1f}mm {r['L0']*1e3:4.0f}mm {r['E']:5.1f}J "
                  f"{r['v']:5.1f} {pen:>14} {r['w']:7.2f}m", flush=True)
        print()
