"""BAGIL HIZ TOLERANSI.

Onceki tum analizler "hedef de 100 km/h, ayni yon" (takip, bagil hiz ~0)
varsayimiyla yapildi. Gercekte drone hedefe kapanirken bagil hiz sifir olmaz.

Ag dinamigi hedeften BAGIMSIZ oldugu icin TEK simulasyon yeterli; sonra
hedefin  d(t) = d0 + v_bagil * t  yorungesiyle kesistiriyoruz.
"""
import sys
sys.path.insert(0, '/home/kayra/Masaüstü/ag_firlatma')
import numpy as np
from run_cerceve import kos, R_GER, V_DRONE


def kesisme(ts, Z, R, d0, v_bagil):
    """Hedef d0'dan baslayip v_bagil ile uzaklasir/yaklasir. Yakalandi mi?"""
    d = d0 + v_bagil * ts
    fark = Z - d
    isaret = np.sign(fark)
    gecis = np.where(np.diff(isaret) != 0)[0]
    for i in gecis:
        w = fark[i] / (fark[i] - fark[i + 1]) if fark[i] != fark[i + 1] else 0.0
        Rk = R[i] + w * (R[i + 1] - R[i])
        if Rk >= R_GER:
            return True, ts[i] + w * (ts[i + 1] - ts[i]), Rk
    return False, np.nan, np.nan


if __name__ == "__main__":
    t, L, S = kos(alpha_deg=18, v_hedef=20.0, T=0.80)
    R, ts, P, bd = S['R'], S['t'], S['P_snap'], S['bilye_dug']
    Z = np.array([p[bd, 2].mean() for p in P])
    i = int(np.argmax(R[:len(R) // 2]))
    j = i + int(np.argmin(R[i:]))
    R = R[:j + 1]; ts = ts[:j + 1]; Z = Z[:j + 1]      # ilk acilma cevrimi

    print("=== BAGIL HIZ TOLERANSI (α=18°, v_çıkış=20 m/s, Ø3.0 m ağ) ===")
    print("  v_bağıl > 0  : hedef bizden HIZLI (uzaklaşıyor)")
    print("  v_bağıl < 0  : biz hedefe KAPANIYORUZ\n")
    print(f"{'v_bağıl':>9} {'km/h':>7} {'tetiklenebilir d0 aralığı':>28} {'genişlik':>9}")
    d0_ara = np.arange(0.2, 8.0, 0.02)
    for v_b in [-10, -8, -6, -4, -2, 0, 2, 4, 6, 8]:
        ok = np.array([kesisme(ts, Z, R, d0, v_b)[0] for d0 in d0_ara])
        if not ok.any():
            print(f"{v_b:8.0f} {v_b*3.6:6.0f}  --- yakalama YOK ---")
            continue
        d = d0_ara[ok]
        # bitisik aralik mi?
        print(f"{v_b:8.0f} {v_b*3.6:6.0f} {d.min():14.2f} – {d.max():5.2f} m "
              f"{d.max()-d.min():8.2f} m")

    print("\n=== PEKI KAPANMA HIZI NE KADAR OLMALI? ===")
    print("  (hedefi 3 m'den vurmak icin gereken bagil hiz araligi)")
    for d0 in [2.0, 2.5, 3.0, 3.5, 4.0]:
        vb = np.arange(-14, 10, 0.1)
        ok = np.array([kesisme(ts, Z, R, d0, v)[0] for v in vb])
        if ok.any():
            print(f"  d0={d0:.1f} m -> v_bağıl {vb[ok].min():+.1f} … "
                  f"{vb[ok].max():+.1f} m/s "
                  f"({vb[ok].min()*3.6:+.0f} … {vb[ok].max()*3.6:+.0f} km/h)")
        else:
            print(f"  d0={d0:.1f} m -> hiçbir bağıl hızda yakalanmıyor")
