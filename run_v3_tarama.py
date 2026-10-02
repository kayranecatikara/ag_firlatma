"""v3 TARAMA — hedef: UZAK kenar >= 5.5 m, Talon (1718 mm kanat -> R_ger 0.859 m).

Kaldirac'lar:
  STROK      : namlu boyunu belirler (L ~ 28.5 + (1 + 1/(lam-1))*STROK)
  bant       : adet x kesit x lam  -> enerji ve KURMA KUVVETI (bant basina!)
  alpha      : kucuk aci pencereyi UZAGA kaydirir (bedelsiz)
  ag         : buyuk ag = marj, ama surukleme; buyuk goz + ince ip = az surukleme

Kisit: bant basina kurma kuvveti <= F_BANT_MAX (elle tek tek cekilecek).
"""
import sys, itertools, json
import os, sys
_K = os.path.abspath(__file__)
while _K != os.path.dirname(_K) and not os.path.isdir(os.path.join(_K, "agsim")):
    _K = os.path.dirname(_K)
sys.path.insert(0, _K)
from agsim.yollar import vyol
import numpy as np
from agsim.lastik import Bant, firlat_lastik
from run_lastik import tasarim
from agsim.netfull import simule

R_GER = 0.859          # Mini Talon: 1718 mm kanat acikligi
G_LATEKS = 0.45e6
H = 14.0e-3            # uzamayan uc donanimi (yuksuk + halka)
ARKA, Y_CAPRAZ, PAY = 5.0e-3, 4.5e-3, 5.0e-3
HAZNE_A, PAKET_DOL = 1081e-6, 0.30
F_BANT_MAX = 360.0     # N, tek bandi elle cekme siniri (~37 kg)


def geometri(strok, lam):
    L0 = strok / (lam - 1.0)
    D_son = L0 + H
    L_namlu = ARKA + Y_CAPRAZ + strok + D_son + PAY
    return L0, D_son, L_namlu


def bant_kesit(F_bant, lam):
    """Istenen bant basina kurma kuvvetini veren kesit alani."""
    return F_bant / (G_LATEKS * (lam - 1.0 / lam ** 2))


def kos(strok, n_bant, F_bant, lam, alpha, R_ag, goz, d_ip, mlz="Kursun",
        D_bilye=12.7e-3, T=0.75):
    L0, D_son, L_namlu = geometri(strok, lam)
    t = tasarim(alpha, False)
    t.ag.R_ag, t.ag.goz, t.ag.d_iplik = R_ag, goz, d_ip
    t.bilye.malzeme, t.bilye.D = mlz, D_bilye
    V_ip = np.pi * 0.25 * d_ip ** 2 * t.ag.L_iplik
    L_hazne = max(V_ip / PAKET_DOL / HAZNE_A, 8e-3)
    L_kap = 24e-3 + L_hazne
    t.kapsul.L_kapsul = L_kap
    t.kapsul.m_kapsul = 0.0194 * (L_kap / 0.036) + 0.0060
    t.namlu.L_namlu = L_namlu
    A0 = bant_kesit(F_bant, lam)
    OD = np.sqrt(4 * A0 / np.pi + (4e-3) ** 2)
    b = Bant(n=n_bant, OD=OD, ID=4e-3, L0=L0, H=H, Gmod=G_LATEKS)
    L = firlat_lastik(t, b, D_son + strok, strok)
    if L.get("basarisiz"):
        return None
    S = simule(t, L, T=T, kayit=int(T * 360))
    R, ts, P, bd = S['R'], S['t'], S['P_snap'], S['bilye_dug']
    Z = np.array([p[bd, 2].mean() for p in P])
    # ILK acilma cevrimi: ilk tepe, sonra ilk cokus dibi.
    # (Gec zamanda model kararsizlasiyor; R.max() yanıltıcı - ilk tepeyi kullan.)
    d = np.diff(R)
    i = int(np.argmax(d < 0)) if (d < 0).any() else int(np.argmax(R))
    j = i + int(np.argmin(R[i:min(i + len(R) // 2, len(R))]))
    m = (R[:j + 1] >= R_GER)
    lo, hi = (Z[:j + 1][m].min(), Z[:j + 1][m].max()) if m.any() else (np.nan, np.nan)
    return dict(L_namlu=L_namlu * 1e3, strok=strok * 1e3, n=n_bant, OD=OD * 1e3,
                lam=lam, F_bant=F_bant, F_top=n_bant * F_bant, L0=L0 * 1e3,
                alpha=alpha, R_ag=R_ag, goz=goz * 1e3, d_ip=d_ip * 1e3,
                v=L["v_exit"], E=L["E_depo"], m_bant=b.m * 1e3, L_kap=L_kap * 1e3,
                R_max=R[:j + 1].max(), R_tepe=R[i], T_tepe=S['T_max'][:j+1].max(), lo=lo, hi=hi,
                w=(hi - lo) if np.isfinite(lo) else 0.0)


if __name__ == "__main__":
    sonuc = []
    print(f"hedef: UZAK kenar >= 5.5 m,  R_ger = {R_GER} m (Talon 1718 mm)")
    print(f"{'namlu':>7} {'strok':>6} {'bant':>13} {'F/bant':>7} {'a':>3} "
          f"{'ag':>16} {'v':>6} {'R_max':>6} {'pencere':>14} {'gen':>6}")
    for strok, (n, F), lam, alpha, R_ag, goz in itertools.product(
            (0.140, 0.170, 0.200),
            ((2, 360.0), (3, 300.0), (3, 360.0)),
            (4.0,), (10, 13, 16), (1.2, 1.4), (0.140, 0.170)):
        r = kos(strok, n, F, lam, alpha, R_ag, goz, 0.165e-3)
        if r is None:
            continue
        sonuc.append(r)
        pen = f"{r['lo']:5.2f}-{r['hi']:5.2f}" if np.isfinite(r["lo"]) else "  acilmiyor  "
        bant = f"{n}xO{r['OD']:.1f}x{lam:.1f}"
        print(f"{r['L_namlu']:6.0f}mm {r['strok']:5.0f} {bant:>13} {F:6.0f}N "
              f"{alpha:3d} O{2*R_ag:.1f}m/{r['goz']:.0f}mm {r['v']:5.1f} "
              f"{r['R_max']:5.2f} {pen:>14} {r['w']:5.2f}", flush=True)
    np.save(vyol(__file__, "out", "v3_tarama.npy"), sonuc, allow_pickle=True)
    uygun = [r for r in sonuc if np.isfinite(r["hi"]) and r["hi"] >= 5.5]
    print(f"\n=== UZAK KENAR >= 5.5 m OLANLAR ({len(uygun)} adet) ===")
    for r in sorted(uygun, key=lambda r: (r["L_namlu"], -r["w"]))[:15]:
        print(f"  namlu {r['L_namlu']:.0f} mm, {r['n']}xO{r['OD']:.1f} bant "
              f"({r['F_bant']:.0f} N/bant, top {r['F_top']:.0f} N), a={r['alpha']}, "
              f"ag O{2*r['R_ag']:.1f} m/{r['goz']:.0f} mm -> v={r['v']:.1f}, "
              f"pencere {r['lo']:.2f}-{r['hi']:.2f} (gen {r['w']:.2f})")
    print(f"\n=== EN UZAK 8 ===")
    for r in sorted(sonuc, key=lambda r: -(r["hi"] if np.isfinite(r["hi"]) else 0))[:8]:
        print(f"  hi={r['hi']:.2f} namlu {r['L_namlu']:.0f} {r['n']}x{r['OD']:.1f} "
              f"a={r['alpha']} ag O{2*r['R_ag']:.1f}/{r['goz']:.0f} v={r['v']:.1f} "
              f"gen={r['w']:.2f}")
