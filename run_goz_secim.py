"""GOZ ARALIGI SECIMI — daha sik ag ne kazandirir, ne kaybettirir?

Ag boyutu SABIT (kose yaricapi 1.4 m -> kose-kose 2.80 m).
Goz kucultulunce: daha cok iplik -> daha cok surukleme -> menzil DUSER,
ama pervaneye daha cok iplik dolanir.

PERVANE YAKALAMA GEOMETRISI (kare goz, pitch a, pervane capi D):
  D >= a*sqrt(2) : cember MUTLAKA en az 1 DUGUM icerir  -> garanti kilit
  D >= a         : cember MUTLAKA en az 1 IPLIK keser
  D <  a         : delikten gecebilir
  kesilen iplik sayisi ~ 2D/a
"""
import sys
sys.path.insert(0, '/home/kayra/Masaüstü/ag_firlatma')
import numpy as np
import run_v3_tarama as V

R_AG = 1.4
D_PERVANE = 0.230          # X-UAV Talon, 9-10 inc pusher
IP_D, IP_M = 0.165e-3, 0.021      # PE #1
CEV_D, CEV_M = 0.285e-3, 0.062    # PE #3
HAZNE_A = 1081e-6
LAM, F_BANT, N_BANT, ALPHA = 4.0, 300.0, 4, 13
STROK = 0.114


def ag_olc(R, goz):
    A = 1.5 * np.sqrt(3) * R ** 2
    L_goz, L_cev = 2 * A / goz, 6 * R
    V_kati = (np.pi * .25 * IP_D ** 2 * L_goz + np.pi * .25 * CEV_D ** 2 * L_cev)
    return dict(A=A, L_goz=L_goz, L_top=L_goz + L_cev,
                m=L_goz * IP_M + L_cev * CEV_M, V=V_kati * 1e6,
                dugum=int(A / goz ** 2))


if __name__ == "__main__":
    print(f"Ag SABIT: kose-kose {2*R_AG:.2f} m, alan {1.5*np.sqrt(3)*R_AG**2:.2f} m2")
    print(f"Pervane {D_PERVANE*1e3:.0f} mm | namlu 180 mm, 4x{F_BANT:.0f} N bant\n")
    print(f"{'goz':>6} {'iplik':>7} {'dugum':>6} {'kutle':>6} {'kati':>6} "
          f"{'hazne@%20':>10} {'kesilen ip':>11} {'garanti':>8} {'R_tepe':>7} "
          f"{'pencere':>13} {'gen':>6}")
    for goz in (0.090, 0.100, 0.110, 0.120, 0.140):
        a = ag_olc(R_AG, goz)
        L_hazne = a["V"] / 0.20 * 1e-6 / HAZNE_A            # %20 dolgu (guvenli)
        # kapsul boyu hazneye gore; kutlesi de
        L_kap = 24e-3 + max(L_hazne, 8e-3)
        r = V.kos(STROK, N_BANT, F_BANT, LAM, ALPHA, R_AG, goz, IP_D)
        if r is None:
            print(f"{goz*1e3:5.0f}mm  --- basarisiz ---"); continue
        n_ip = 2 * D_PERVANE / goz
        gar = "EVET" if D_PERVANE >= goz * np.sqrt(2) else "hayir"
        pen = f"{r['lo']:5.2f}-{r['hi']:5.2f}" if np.isfinite(r['lo']) else " acilmiyor "
        print(f"{goz*1e3:5.0f}mm {a['L_top']:6.0f}m {a['dugum']:5d} {a['m']:5.2f}g "
              f"{a['V']:5.2f}cc {L_hazne*1e3:9.1f}mm {n_ip:10.1f} {gar:>8} "
              f"{r['R_tepe']:6.3f} {pen:>13} {r['w']:5.2f}", flush=True)
    print(f"\n  R_ger = {V.R_GER} m (Talon 1718 mm) — R_tepe bunun USTUNDE olmali")
    print("  'kesilen ip' = pervane diskini kesen iplik sayisi (~2D/goz)")
