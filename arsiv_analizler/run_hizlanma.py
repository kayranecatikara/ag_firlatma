"""DRONE'U ATIS ONCESI HIZLANDIRMAK ISE YARAR MI?

Onceki bagil-hiz calismasi (run_bagil_hiz.py) drone hizini 100 km/h'te SABIT
tutup HEDEFIN hizini degistiriyordu. Kullanicinin sorusu bunun TERSI:
biz hizlanirsak ne olur?

Iki etki ters yonde calisir:
  (+) hedefe kapaniyoruz  -> hedef aga dogru geliyor
  (-) kendi hava hizimiz artiyor -> aga etkiyen KARSI RUZGAR artiyor,
      surukleme v^2 ile buyuyor, ag daha hizli yavasliyor
Hangisi baskin? Her drone hizi icin AYRI simulasyon gerekir.
"""
import os, sys
_K = os.path.abspath(__file__)
while _K != os.path.dirname(_K) and not os.path.isdir(os.path.join(_K, "agsim")):
    _K = os.path.dirname(_K)
sys.path.insert(0, _K)
import numpy as np
from agsim.dse import vektor_to_tasarim
from agsim.launcher import firlat_genel
from agsim.netfull import simule

R_GER = 0.75
V_HEDEF = 100 / 3.6          # hedef sabit 100 km/h
X = np.load("out/x_final.npy")


def pencere_vs_hedef(V_drone, alpha_deg=18, v_hedef=20.0, R_ag=1.50,
                     m_yay=0.400, x0=0.25, T=0.80):
    """Verilen drone hizinda: hedefe gore tetiklenebilir d0 araligi."""
    t, _, _ = vektor_to_tasarim(X)
    t.kapsul.L_kapsul, t.kapsul.m_kapsul = 0.050, 0.032
    t.ag.R_ag = R_ag
    t.kapsul.alpha_cep = np.radians(alpha_deg)
    t.ag.n_ring, t.ag.n_spoke = 7, 18
    t.ang.V_drone = V_drone                      # <<< karsi ruzgari belirler
    k = (t.m_hareketli + m_yay / 3) * v_hedef ** 2 / x0 ** 2
    L = firlat_genel(t, k, m_yay, x0, x0)
    S = simule(t, L, T=T, kayit=int(T * 400))
    R, ts, P, bd = S['R'], S['t'], S['P_snap'], S['bilye_dug']
    Z = np.array([p[bd, 2].mean() for p in P])   # DRONE cercevesinde
    i = int(np.argmax(R[:len(R) // 2])); j = i + int(np.argmin(R[i:]))
    R, ts, Z = R[:j + 1], ts[:j + 1], Z[:j + 1]

    # hedef drone cercevesinde:  d(t) = d0 + (V_hedef - V_drone)*t
    v_bagil = V_HEDEF - V_drone
    d0_ara = np.arange(0.2, 12.0, 0.02)
    ok = np.zeros(len(d0_ara), bool)
    for n, d0 in enumerate(d0_ara):
        fark = Z - (d0 + v_bagil * ts)
        g = np.where(np.diff(np.sign(fark)) != 0)[0]
        for q in g:
            w = fark[q] / (fark[q] - fark[q + 1]) if fark[q] != fark[q + 1] else 0.
            if R[q] + w * (R[q + 1] - R[q]) >= R_GER:
                ok[n] = True
                break
    return (d0_ara[ok].min(), d0_ara[ok].max()) if ok.any() else (np.nan, np.nan), \
           Z.max(), R.max(), L["v_exit"]


if __name__ == "__main__":
    print("=== DRONE HIZINI ARTIRMAK: hedef sabit 100 km/h ===")
    print("  (her satir AYRI 3B simulasyon - karsi ruzgar da degisiyor)\n")
    print(f"{'drone':>8} {'bağıl':>8} {'karşı rüzgâr':>13} {'tetikleme aralığı':>21} "
          f"{'genişlik':>9} {'Z_max':>7}")
    for kmh in [100, 110, 120, 130, 140, 160]:
        Vd = kmh / 3.6
        (a, b), Zmax, Rmax, vex = pencere_vs_hedef(Vd)
        if not np.isfinite(a):
            print(f"{kmh:6.0f}km/h  --- yakalama YOK ---"); continue
        print(f"{kmh:6.0f}km/h {kmh-100:+6.0f}km/h {Vd:10.1f} m/s "
              f"{a:12.2f} – {b:5.2f} m {b-a:8.2f} m {Zmax:6.2f}m", flush=True)

    print("\n=== KARSILASTIRMA: HEDEF yavaslarsa (biz 100 km/h sabit) ===")
    print("  (run_bagil_hiz.py sonuclari - karsi ruzgar DEGISMIYOR)")
    print("   hedef  80 km/h (bağıl -20) -> 2.6 – 5.5 m")
    print("   hedef  86 km/h (bağıl -14) -> 2.4 – 4.6 m")
    print("   hedef 100 km/h (bağıl   0) -> 2.0 – 3.2 m")
