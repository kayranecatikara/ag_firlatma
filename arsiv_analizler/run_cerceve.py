"""REFERANS CERCEVESI DOGRULAMASI.

Soru: "menzil 3 m" derken agin HAVADA aldigi yolu ve o yol boyunca etkiyen
surukleme isini hesaba katiyor muyuz?

netfull.simule DRONE CERCEVESINDE calisir:
  - ruzgar = (0, 0, -V_drone)  -> 27.8 m/s karsi ruzgar VAR
  - surukleme  v_bagil = v_sim + V_drone*z_sapkasi  ile hesaplanir
  - z_sim dogrudan DRONE'A GORE ileri mesafedir
Yer cercevesindeki yol:  s_yer = z_sim + V_drone * t
"""
import sys
sys.path.insert(0, '/home/kayra/Masaüstü/ag_firlatma')
import numpy as np
from agsim.dse import vektor_to_tasarim
from agsim.launcher import firlat_genel
from agsim.netfull import simule

X = np.load("out/x_final.npy")
V_DRONE = 100 / 3.6
R_GER = 0.75


def kos(alpha_deg=18, v_hedef=20.0, R_ag=1.50, m_yay=0.400, x0=0.25, T=0.60):
    t, _, _ = vektor_to_tasarim(X)
    t.kapsul.L_kapsul, t.kapsul.m_kapsul = 0.050, 0.032
    t.ag.R_ag = R_ag
    t.kapsul.alpha_cep = np.radians(alpha_deg)
    t.ag.n_ring, t.ag.n_spoke = 7, 18
    k = (t.m_hareketli + m_yay / 3) * v_hedef ** 2 / x0 ** 2
    L = firlat_genel(t, k, m_yay, x0, x0)
    S = simule(t, L, T=T, kayit=int(T * 400))
    return t, L, S


if __name__ == "__main__":
    t, L, S = kos()
    R, ts, P, Vv, bd = S['R'], S['t'], S['P_snap'], S['V_snap'], S['bilye_dug']
    Z = np.array([p[bd, 2].mean() for p in P])          # DRONE'a gore
    Vz = np.array([v[bd, 2].mean() for v in Vv])        # drone cercevesinde hiz
    S_yer = Z + V_DRONE * ts                            # YER cercevesinde yol
    V_hava = Vz + V_DRONE                               # HAVAYA gore hiz

    i = int(np.argmax(R[:len(R) // 2]))
    m = (R >= R_GER) & (np.arange(len(R)) <= i + int(np.argmin(R[i:])))

    print("=== AG NEREDE, NE KADAR YOL GIDIYOR? (v_cikis=%.0f m/s, alpha=18) ===" % L["v_exit"])
    print(f"{'t [ms]':>7} {'DRONE-göre':>11} {'YERDE yol':>10} {'hava hızı':>10} "
          f"{'R [m]':>7} {'sürükleme':>10}")
    CdA = 1.10 * t.ag.solidite * np.pi * np.maximum(R, 1e-3) ** 2
    Fd = 0.5 * 1.225 * CdA * V_hava ** 2
    for tt in [0, .05, .10, .15, .20, .25, .30, .40, .50]:
        j = np.argmin(abs(ts - tt))
        print(f"{ts[j]*1e3:6.0f} {Z[j]:10.2f}m {S_yer[j]:9.2f}m "
              f"{V_hava[j]:9.1f} {R[j]:6.2f} {Fd[j]:9.1f} N")

    print(f"\n--- ATIS PENCERESI ICINDE ---")
    print(f"  drone'a göre : {Z[m].min():.2f} – {Z[m].max():.2f} m")
    print(f"  YERDE yol    : {S_yer[m].min():.2f} – {S_yer[m].max():.2f} m  "
          f"<-- ağın havada süpürdüğü mesafe")
    print(f"  süre         : {ts[m].min()*1e3:.0f} – {ts[m].max()*1e3:.0f} ms")
    print(f"  bu sürede drone/hedef {V_DRONE*(ts[m].max()-ts[m].min()):.2f} m ilerliyor")

    # Enerji dengesi HAVA cercevesinde (surukleme burada is yapar).
    # Not: yukaridaki Fd yalnizca kaba bir gostergedir (duz-disk yaklasimi);
    # asagidaki hesap dogrudan simulasyonun hiz alanindan gelir.
    KE = 0.5 * t.m_ucan * V_hava ** 2
    print(f"\n--- ENERJI (HAVA cercevesinde) ---")
    print(f"  namlunun verdigi (agiz enerjisi)      : "
          f"{0.5*t.m_ucan*L['v_exit']**2:6.1f} J")
    print(f"  drone hizindan gelen 'bedava' enerji  : "
          f"{KE[0] - 0.5*t.m_ucan*L['v_exit']**2:6.1f} J")
    print(f"  atis anindaki toplam (havaya gore)    : {KE[0]:6.1f} J")
    print(f"  pencere sonunda kalan                 : {KE[m][-1]:6.1f} J")
    print(f"  SURUKLEMENIN YUTTUGU                  : {KE[0]-KE[m][-1]:6.1f} J"
          f"   (%{100*(KE[0]-KE[m][-1])/KE[0]:.0f})")
    print("""
  Kritik nokta: ag namludan yalnizca %.1f J ile cikiyor ama HAVAYA GORE
  %.0f J ile yola basliyor - farki drone'un kendi hizi veriyor. Surukleme
  iste bu %.0f J'un buyuk kismini yiyor. Menzili kisaltan sey budur.""" % (
        0.5*t.m_ucan*L['v_exit']**2, KE[0], KE[0]))
