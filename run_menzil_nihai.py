"""NIHAI TASARIM — menzil, tetikleme mesafesi, hava suruklemesinin etkisi.

Senaryo: drone 100 km/h, hedef 100 km/h ayni yonde (takip). Tetikleme
gecikmesi: servo pimi ~120 ms'de cekiyor.
Cikti:
  1) atis penceresi, en acik nokta
  2) hava suruklemesi agi ne kadar GERI cekiyor (suruklemesiz ile fark)
  3) hedefe kapanma hizina gore pencere
  4) tetikleme gecikmesi telafisi
  5) gurbuzluk (Monte Carlo)
"""
import sys, json
sys.path.insert(0, '/home/kayra/Masaüstü/ag_firlatma')
import numpy as np
from agsim.lastik import Bant, firlat_lastik
from agsim.netfull import simule
from run_lastik import tasarim

R_GER = 0.859     # X-UAV Talon: 1718 mm kanat acikligi
V100 = 100 / 3.6
K = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "out/nihai_konfig.json"))


def kur(V_drone=V100, rng=None):
    t = tasarim(K["alpha"], False)
    t.ag.R_ag, t.ag.goz, t.ag.d_iplik = K["R_ag"], K["goz"], K["d_ip"]
    t.bilye.malzeme, t.bilye.D = K["mlz"], 12.7e-3
    t.kapsul.m_kapsul, t.kapsul.L_kapsul = K["m_kap"], K["L_kap"]
    t.namlu.L_namlu = K["L_namlu"]
    t.ang.V_drone = V_drone
    t.ag.n_ring, t.ag.n_spoke = 7, 18
    b = Bant(n=K.get("n_bant", 2), OD=K["bant_OD"], ID=4e-3, L0=K["L0"], H=K["H"])
    s = K["strok"]
    if rng is not None:
        t.kapsul.m_kapsul *= 1 + 0.08 * rng.normal()
        t.namlu.mu_surtunme *= max(.1, 1 + 0.30 * rng.normal())
        t.kapsul.alpha_cep = max(0., t.kapsul.alpha_cep + np.radians(2.0) * rng.normal())
        t.hava.ruzgar = np.array([3.0 * rng.normal(), 0., 0.])
        b.Gmod *= 1 + 0.10 * rng.normal()          # bant sertligi (olculmezse +-%25!)
    return t, firlat_lastik(t, b, K["D_son"] + s, s)


def yol(t, L, T=0.9, aero=1.0):
    S = simule(t, L, T=T, kayit=int(T * 400), aero_olcek=aero)
    R, ts, P, bd = S['R'], S['t'], S['P_snap'], S['bilye_dug']
    Z = np.array([p[bd, 2].mean() for p in P])
    return ts, Z, R


def ilk_cevrim(ts, Z, R):
    i = int(np.argmax(R[:max(len(R) // 2, 2)])); j = i + int(np.argmin(R[i:]))
    return ts[:j + 1], Z[:j + 1], R[:j + 1], i


def pencere_bagil(ts, Z, R, v_bagil):
    d0s = np.arange(0.2, 10.0, 0.02); ok = np.zeros(len(d0s), bool)
    for n, d0 in enumerate(d0s):
        f = Z - (d0 + v_bagil * ts)
        for q in np.where(np.diff(np.sign(f)) != 0)[0]:
            w = f[q] / (f[q] - f[q + 1]) if f[q] != f[q + 1] else 0.
            if R[q] + w * (R[q + 1] - R[q]) >= R_GER:
                ok[n] = True; break
    return (d0s[ok].min(), d0s[ok].max()) if ok.any() else (np.nan, np.nan)


if __name__ == "__main__":
    t, L = kur()
    ts, Z, R = yol(t, L)
    tw, Zw, Rw, i = ilk_cevrim(ts, Z, R)
    lo, hi = pencere_bagil(tw, Zw, Rw, 0.0)
    print(f"=== 1) ATIS PENCERESI (drone & hedef 100 km/h, ayni yon) ===")
    print(f"  v_cikis {L['v_exit']:.1f} m/s,  ag en acik {Rw[i]:.2f} m @ {tw[i]*1e3:.0f} ms, "
          f"drone'a gore {Zw[i]:.2f} m")
    print(f"  PENCERE: hedef {lo:.2f} – {hi:.2f} m arasindayken ag ACIK ulasir "
          f"(genislik {hi-lo:.2f} m)")

    print(f"\n=== 2) HAVA SURUKLEMESI AGI NE KADAR GERI CEKIYOR? ===")
    ts0, Z0, R0 = yol(t, L, aero=0.0)
    print(f"{'t':>6} {'suruklemeli':>12} {'suruklemesiz':>13} {'GERI CEKME':>11} "
          f"{'yerde yol':>10} {'hava hizi':>10} {'R':>6}")
    for tt in (0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40):
        j = np.argmin(abs(ts - tt)); j0 = np.argmin(abs(ts0 - tt))
        vh = V100 + (Z[min(j + 1, len(Z) - 1)] - Z[max(j - 1, 0)]) / (ts[min(j + 1, len(ts) - 1)] - ts[max(j - 1, 0)])
        print(f"{tt*1e3:4.0f}ms {Z[j]:10.2f} m {Z0[j0]:11.2f} m {Z0[j0]-Z[j]:9.2f} m "
              f"{Z[j]+V100*tt:8.2f} m {vh:8.1f} m/s {R[j]:5.2f}")

    print(f"\n=== 3) HEDEFE KAPANMA HIZI (hedef 100 km/h) ===")
    for kmh in (100, 110, 120, 130):
        t2, L2 = kur(V_drone=kmh / 3.6)
        a, b = pencere_bagil(*ilk_cevrim(*yol(t2, L2))[:3], V100 - kmh / 3.6)
        print(f"  drone {kmh:3d} km/h (fark {kmh-100:+3d}) -> tetik penceresi "
              f"{a:.2f} – {b:.2f} m (gen {b-a:.2f} m)")

    print(f"\n=== 4) TETIK GECIKMESI (servo ~120 ms) ===")
    print("  Esit hizda (takip) hedef drone'a gore hareket etmez -> gecikme mesafeyi")
    print("  DEGISTIRMEZ. Kapanirken hedef gecikme boyunca yaklasir:")
    for kmh in (110, 120, 130):
        print(f"   drone {kmh} km/h: 120 ms'de {(kmh-100)/3.6*0.12:.2f} m yaklasir "
              f"-> tetigi bu kadar ONCE (uzakta) ver")

    print(f"\n=== 5) GURBUZLUK (Monte Carlo, n={K.get('n_mc', 60)}) ===")
    hedef = 0.5 * (lo + hi)
    rng = np.random.default_rng(7); n = K.get("n_mc", 60)
    for sig in (0.25, 0.10):
        ok = 0
        for _ in range(n):
            t3, L3 = kur(rng=rng)
            tw3, Zw3, Rw3, _ = ilk_cevrim(*yol(t3, L3))
            a3, b3 = pencere_bagil(tw3, Zw3, Rw3, 0.0)
            d = hedef + sig * rng.normal()
            ok += bool(np.isfinite(a3) and a3 <= d <= b3)
        print(f"  tetik @ {hedef:.2f} m, mesafeolcer sig={sig:.2f} m -> yakalama %{100*ok/n:.0f}",
              flush=True)
