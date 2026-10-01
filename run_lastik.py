"""Lastik bant tahrikli tasarim: yiv karari + bant secimi + nihai performans.

Namlu yerlesimi (L_NAMLU = 260 mm, arkasi ACIK = yukleme agzi):
   0 ..  5          arka pay
   5 .. 55          kapsul (kurulu)
   55 .. 234        STROK (179 mm)
   234 .. 238       omuz
   238 .. 260       iraksak agiz konisi
Capraz pim kapsulun 4.5 mm'sinde -> kurulu y=9.5, strok sonu y=188.5.
Bant ankraji agiz bileziginde y=256.
"""
import sys
sys.path.insert(0, '/home/kayra/Masaüstü/ag_firlatma')
import numpy as np
from agsim.dse import vektor_to_tasarim
from agsim.lastik import Bant, firlat_lastik, cekme_testi_tablosu
from run_taret import pencere

L_NAMLU, ARKA, L_KAP, UC = 260.0, 5.0, 50.0, 26.0
STROK = (L_NAMLU - ARKA - L_KAP - UC) * 1e-3          # 0.179 m
Y_PIM0 = (ARKA + 4.5) * 1e-3                          # capraz pim, kurulu
Y_ANK = (L_NAMLU - 4.0) * 1e-3                        # agiz bilezigi ankraji
L_KURULU = Y_ANK - Y_PIM0                              # 0.2465 m
X = np.load("out/x_final.npy")


def tasarim(alpha_deg=18.0, yivli=True, m_kapsul=0.030):
    t, _, _ = vektor_to_tasarim(X)
    t.kapsul.L_kapsul, t.kapsul.m_kapsul = 0.050, m_kapsul
    t.ag.R_ag = 1.50
    t.kapsul.alpha_cep = np.radians(alpha_deg)
    t.namlu.L_namlu = L_NAMLU * 1e-3
    if not yivli:
        t.namlu.twist_L = 0.0
    t.ag.n_ring, t.ag.n_spoke = 7, 18
    return t


def bant_lam(OD, ID, lam, n=2, H=0.012, G=0.45e6):
    """Kurulu gerilme orani lam olacak sekilde L0'i geometriden cozer."""
    return Bant(n=n, OD=OD, ID=ID, L0=(L_KURULU - H) / lam, H=H, Gmod=G)


if __name__ == "__main__":
    print(f"Geometri: namlu {L_NAMLU:.0f} mm, strok {STROK*1e3:.0f} mm, "
          f"kurulu bant boyu {L_KURULU*1e3:.1f} mm\n")

    # ---------------------------------------------------------------- 1) YIV
    print("=== 1) YIV GEREKLI MI? (bantlar duz yarikta -> kapsul DONEMEZ) ===")
    b = bant_lam(14e-3, 4e-3, 3.5)
    print(f"{'konfig':>26} {'v_cik':>7} {'v_rad':>7} {'pencere':>17} {'genislik':>9}")
    for ad, a, yiv in [("alpha=18 + yiv 730mm", 18, True),
                       ("alpha=18, yivsiz", 18, False),
                       ("alpha=19, yivsiz", 19, False),
                       ("alpha=20, yivsiz", 20, False)]:
        t = tasarim(a, yiv)
        L = firlat_lastik(t, b, L_KURULU, STROK)
        lo, hi = pencere(t, L)
        print(f"{ad:>26} {L['v_exit']:6.1f} {L['v_radyal']:6.2f} "
              f"{lo:8.2f} – {hi:5.2f} m {hi-lo:8.2f} m", flush=True)

    # ---------------------------------------------------------- 2) BANT SECIMI
    print("\n=== 2) BANT SECIMI (2 bant, alpha=19, yivsiz) ===")
    print(f"{'tup OD/ID':>10} {'lam':>5} {'L0':>6} {'kutle':>6} {'E':>6} "
          f"{'F_kurma':>8} {'v_cik':>7} {'gucsuz':>7}")
    adaylar = []
    for OD, ID in [(12e-3, 4e-3), (14e-3, 4e-3), (16e-3, 5e-3)]:
        for lam in (3.0, 3.5, 4.0):
            b = bant_lam(OD, ID, lam)
            t = tasarim(19, False)
            L = firlat_lastik(t, b, L_KURULU, STROK)
            adaylar.append((OD, ID, lam, b, L))
            print(f"{OD*1e3:5.0f}/{ID*1e3:<4.0f} {lam:5.1f} {b.L0*1e3:5.0f}mm "
                  f"{b.m*1e3:5.1f}g {L['E_depo']:5.1f}J {L['F_kurma']:7.0f}N "
                  f"{L['v_exit']:6.1f} {L['gucsuz_yol']*1e3:5.0f}mm")

    # ------------------------------------------------------ 3) SECILEN BANT
    print("\n=== 3) SECILEN: 2 x 14/4 mm lateks tup, lam=3.5 ===")
    b = bant_lam(14e-3, 4e-3, 3.5)
    t = tasarim(19, False)
    L = firlat_lastik(t, b, L_KURULU, STROK)
    lo, hi = pencere(t, L)
    print(f"  kaucuk calisma boyu L0   : {b.L0*1e3:.0f} mm  (+{b.H*1e3:.0f} mm donanim)")
    print(f"  kurulu gerilme orani     : {L['lam_kurulu']:.2f}")
    print(f"  bant kutlesi (2 adet)    : {b.m*1e3:.1f} g")
    print(f"  depolanan enerji         : {L['E_depo']:.1f} J")
    print(f"  kurma kuvveti (toplam)   : {L['F_kurma']:.0f} N  ({L['F_kurma']/2:.0f} N / bant)")
    print(f"  v_cikis / v_radyal       : {L['v_exit']:.1f} / {L['v_radyal']:.2f} m/s")
    print(f"  atis penceresi           : {lo:.2f} – {hi:.2f} m  (genislik {hi-lo:.2f} m)")
    print(f"  bant gucsuz kalan yol    : {L['gucsuz_yol']*1e3:.0f} mm (son kisimda serbest kayma)")
    print("\n  CEKME TESTI (tek bant, donanimsiz) - elinizdeki banti boyle dogrulayin:")
    for la, Lx, F in cekme_testi_tablosu(b):
        print(f"    {b.L0*1e3:.0f} mm'lik kaucugu {Lx*1e3:5.0f} mm'ye cek (x{la:.1f}) "
              f"-> beklenen {F:5.0f} N  ({F/9.81:4.1f} kg)")
