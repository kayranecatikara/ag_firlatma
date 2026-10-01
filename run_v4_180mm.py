"""v4 — NAMLU <= 180 mm kisiti altinda en iyi menzil.

L_namlu = 28.5 + STROK*(1 + 1/(lam-1))   [mm]  (bant kurulu boyu dahil)
  lam=4.0 -> STROK <= 113.6      lam=4.5 -> STROK <= 117.8
  lam=5.0 -> STROK <= 121.2      lam=5.5 -> STROK <= 124.0
Kisa strok = ayni enerji icin daha buyuk kuvvet.
Kisit: bant basina el kuvveti <= 360 N (~37 kg), 4 bant (kenar basina 2).
"""
import sys, itertools
sys.path.insert(0, '/home/kayra/Masaüstü/ag_firlatma')
import numpy as np
import run_v3_tarama as V

L_MAX = 180.0
HAZNE_MIN = 14e-3          # ag rahat sigsin (bkz. run_ag_paket.py)


def strok_max(lam):
    return (L_MAX - 28.5) / (1.0 + 1.0 / (lam - 1.0)) * 1e-3


def kos180(lam, F_bant, alpha, R_ag, goz, n=4, d_ip=0.165e-3):
    s = strok_max(lam)
    r = V.kos(s, n, F_bant, lam, alpha, R_ag, goz, d_ip)
    if r is None:
        return None
    r["lam"] = lam
    return r


if __name__ == "__main__":
    # hazne alt sinirini uygula (ag paketlemesi icin)
    import run_v3_tarama as T
    T.PAKET_DOL = 0.25
    print(f"namlu <= {L_MAX:.0f} mm, 4 bant (2/kenar), R_ger={V.R_GER} m (Talon)\n")
    print(f"{'lam':>4} {'strok':>6} {'namlu':>7} {'F/bant':>7} {'F_top':>7} "
          f"{'OD':>6} {'v':>6} {'R_tepe':>7} {'pencere':>14} {'gen':>6}")
    hepsi = []
    for lam, F, alpha, R_ag, goz in itertools.product(
            (4.0, 4.5, 5.0), (300.0, 340.0, 380.0), (11, 13, 15),
            (1.4,), (0.140,)):
        r = kos180(lam, F, alpha, R_ag, goz)
        if r is None:
            continue
        hepsi.append(r)
        pen = f"{r['lo']:5.2f}-{r['hi']:5.2f}" if np.isfinite(r['lo']) else " ACILMIYOR  "
        print(f"{lam:4.1f} {r['strok']:5.0f}mm {r['L_namlu']:6.0f}mm {F:6.0f}N "
              f"{r['F_top']:6.0f}N {r['OD']:5.1f} {r['v']:5.1f} {r['R_tepe']:6.3f} "
              f"{pen:>14} {r['w']:5.2f}", flush=True)

    print("\n=== 5.5 m USTU, el kuvveti <= 360 N ===")
    ok = [r for r in hepsi if np.isfinite(r["hi"]) and r["hi"] >= 5.5
          and r["F_bant"] <= 360]
    for r in sorted(ok, key=lambda r: -r["hi"])[:10]:
        N_pim = r["F_top"] / 2
        print(f"  lam{r['lam']:.1f} strok{r['strok']:.0f} {r['F_bant']:.0f}N/bant "
              f"a={r['alpha']} -> v={r['v']:.1f}, pencere {r['lo']:.2f}-{r['hi']:.2f} "
              f"(gen {r['w']:.2f}), pim yuku {N_pim:.0f} N, "
              f"tetik(PTFE) {2*0.08*N_pim:.0f} N")
    if not ok:
        print("  YOK — 180 mm'de 5.5 m'ye ulasilamiyor.")
        print("  En iyi 5:")
        for r in sorted(hepsi, key=lambda r: -(r['hi'] if np.isfinite(r['hi']) else 0))[:5]:
            print(f"    lam{r['lam']:.1f} strok{r['strok']:.0f} {r['F_bant']:.0f}N "
                  f"a={r['alpha']} -> {r['lo']:.2f}-{r['hi']:.2f}")
