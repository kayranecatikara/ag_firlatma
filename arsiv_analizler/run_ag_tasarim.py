"""AG TASARIMI — DUZELTILMIS surukleme modeliyle yeniden optimizasyon.

Sabit firlatici: 260 mm namlu, 2x 14/4 lateks (referans). Taranan:
  ag kose yaricapi R_ag, goz araligi, ip capi, bilye malzemesi, koni acisi.
Her aday icin: ag kutlesi, paket boyu (kapsul haznesi), cikis hizi, pencere.

Paketleme: dugumlu Dyneema ag, hacimsel doluluk ~0.30 (dugumler dahil).
Hazne kesiti: kapsul ic yaricapi 18.55 mm -> 1081 mm2.
"""
import sys, itertools
sys.path.insert(0, '/home/kayra/Masaüstü/ag_firlatma')
import numpy as np
from agsim.lastik import Bant, firlat_lastik
from run_lastik import tasarim, STROK
from run_taret import pencere

L_KUR = (256.0 - 9.5) * 1e-3
H = 0.018
BANT = Bant(n=2, OD=14e-3, ID=4e-3, L0=(L_KUR - H) / 3.5, H=H)
PAKET_DOL, HAZNE_A = 0.30, 1081e-6
RHO_DYN = 970.0


def aday(R_ag, goz, d_ip, mlz, alpha):
    t = tasarim(alpha, False, m_kapsul=0.029)
    t.ag.R_ag, t.ag.goz, t.ag.d_iplik = R_ag, goz, d_ip
    t.bilye.malzeme, t.bilye.D = mlz, 12.7e-3
    V_ip = np.pi * 0.25 * d_ip ** 2 * t.ag.L_iplik
    L_hazne = V_ip / PAKET_DOL / HAZNE_A
    L = firlat_lastik(t, BANT, L_KUR, STROK)
    lo, hi = pencere(t, L)
    return dict(R=R_ag, goz=goz, d=d_ip, mlz=mlz, a=alpha, m_ag=t.ag.m_ag,
                L_hazne=L_hazne, v=L["v_exit"], lo=lo, hi=hi,
                w=(hi - lo) if np.isfinite(lo) else 0.0, m_bil=6 * t.bilye.m)


if __name__ == "__main__":
    print("R_ag  goz  d_ip   bilye    a    m_ag  hazne   v     pencere        genislik",
          flush=True)
    sonuc = []
    for R_ag, goz, d_ip, mlz, a in itertools.product(
            (0.9, 1.1, 1.3, 1.5), (0.10, 0.13), (0.16e-3, 0.235e-3),
            ("Celik", "Kursun"), (13, 16, 19)):
        r = aday(R_ag, goz, d_ip, mlz, a)
        sonuc.append(r)
        pen = (f"{r['lo']:5.2f}-{r['hi']:5.2f}" if np.isfinite(r['lo'])
               else "  acilmiyor  ")
        print(f"{R_ag:4.1f} {goz*1e3:4.0f} {d_ip*1e3:5.3f} {mlz:>7} {a:3d} "
              f"{r['m_ag']*1e3:6.1f}g {r['L_hazne']*1e3:5.0f}mm {r['v']:5.1f} "
              f"{pen:>13} {r['w']:6.2f}m", flush=True)
    np.save("out/ag_tasarim.npy", sonuc, allow_pickle=True)
    print("\n=== EN GENIS PENCERELER ===")
    for r in sorted(sonuc, key=lambda r: -r["w"])[:12]:
        print(f"  R={r['R']:.1f} goz={r['goz']*1e3:.0f} d={r['d']*1e3:.3f} "
              f"{r['mlz']:>6} a={r['a']:2d}  pencere {r['lo']:.2f}-{r['hi']:.2f} "
              f"(gen {r['w']:.2f} m)  hazne {r['L_hazne']*1e3:.0f} mm")
    print("\n=== EN UZAK ATIS (uzak kenar) ===")
    for r in sorted(sonuc, key=lambda r: -(r["hi"] if np.isfinite(r["hi"]) else 0))[:8]:
        print(f"  R={r['R']:.1f} goz={r['goz']*1e3:.0f} d={r['d']*1e3:.3f} "
              f"{r['mlz']:>6} a={r['a']:2d}  pencere {r['lo']:.2f}-{r['hi']:.2f}")
