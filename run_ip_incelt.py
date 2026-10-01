"""IPLIK CAPI TARAMASI — menzil kazanci vs kesilme/kopma payi.

Gercek ALTIGEN orgu (agsim.hexag) ile kosar; orumcek topolojisi tasarim
sayilarini %6.7 yanlis veriyordu (bkz. out/GAZEBO_sonuc.md).
"""
import sys, json
sys.path.insert(0, '/home/kayra/Masaüstü/ag_firlatma')
import numpy as np
import run_menzil_nihai as M
from agsim.hexag import altigen_ag, bilye_dugumleri
from agsim.netfull import simule
from agsim.kesilme import sarilma_gerilimi, kenar_basinci, ENINE_DAYANIM

CAPLAR = (0.165, 0.150, 0.140, 0.130, 0.120, 0.110, 0.100)
T_SAR = sarilma_gerilimi(0.30, 0.020)       # motor stall -> sarim gerilimi [N]


def kos(d_mm, T=0.55):
    t, L = M.kur()
    t.ag.d_iplik = d_mm * 1e-3
    P, E, cev = altigen_ag(t.ag.R_ag, t.ag.goz)
    bd = bilye_dugumleri(P, cev)
    S = simule(t, L, T=T, kayit=int(T*400), topoloji=(P, E, bd))
    R, ts = S['R'], S['t']
    Z = np.array([p[bd, 2].mean() for p in S['P_snap']])
    i = int(np.argmax(R[:max(len(R)//2, 2)]))
    j = i + int(np.argmin(R[i:]))
    lo, hi = M.pencere_bagil(ts[:j+1], Z[:j+1], R[:j+1], 0.0)
    return dict(R_tepe=R[i], t_tepe=ts[i], X_tepe=Z[i], lo=lo, hi=hi,
                T_max=float(S['T_max'][:j+1].max()), m_ag=t.ag.m_ag,
                F_kopma=t.ag.F_kopma, v_cik=L['v_exit'])


if __name__ == "__main__":
    print(f"{'d':>6} {'ag':>6} {'R_tepe':>7} {'X_tepe':>7} {'PENCERE':>15} "
          f"{'genis':>6} {'T_tepe':>7} {'F_kop':>7} {'pay':>6} {'p_kenar':>8}")
    print(f"{'[mm]':>6} {'[g]':>6} {'[m]':>7} {'[m]':>7} {'[m]':>15} "
          f"{'[m]':>6} {'[N]':>7} {'[N]':>7} {'':>6} {'[MPa]':>8}")
    sat = []
    for d in CAPLAR:
        r = kos(d)
        pk = kenar_basinci(T_SAR, d*1e-3, 0.35e-3)/1e6
        sat.append((d, r, pk))
        print(f"{d:6.3f} {r['m_ag']*1e3:6.2f} {r['R_tepe']:7.3f} "
              f"{r['X_tepe']:7.2f} {r['lo']:6.2f} – {r['hi']:6.2f} "
              f"{r['hi']-r['lo']:6.2f} {r['T_max']:7.2f} {r['F_kopma']:7.1f} "
              f"{r['F_kopma']/r['T_max']:5.1f}x {pk:8.0f}")
    json.dump([{**{'d_mm': d, 'p_kenar_MPa': pk},
                **{k: float(v) for k, v in r.items()}} for d, r, pk in sat],
              open('out/ip_capi_tarama.json', 'w'), indent=1)
    print("\n-> out/ip_capi_tarama.json")
