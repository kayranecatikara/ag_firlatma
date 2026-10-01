"""v3 NIHAI ADAYLAR — Talon (R_ger 0.859 m), hedef uzak kenar 5-6 m."""
import sys
sys.path.insert(0, '/home/kayra/Masaüstü/ag_firlatma')
import numpy as np
import run_v3_tarama as V

kgcm = 0.0981
SERVO = {"MG92B": 3.5, "MG996R": 11.0, "DS3218MG": 21.0}

ADAY = [
    ("A  2 bant, a=13, goz 140", 0.140, 2, 360.0, 13, 1.4, 0.140),
    ("B  3 bant, a=13, goz 140", 0.140, 3, 360.0, 13, 1.4, 0.140),
    ("C  3 bant, a=13, goz 170", 0.140, 3, 360.0, 13, 1.4, 0.170),
    ("D  3 bant, a=10, goz 140", 0.140, 3, 360.0, 10, 1.4, 0.140),
    ("E  2 bant, a=13, goz 140, strok 170", 0.170, 2, 360.0, 13, 1.4, 0.140),
    ("F  3 bant, a=13, goz 140, strok 170", 0.170, 3, 360.0, 13, 1.4, 0.140),
]

print(f"R_ger = {V.R_GER} m (Talon 1718 mm kanat)\n")
print(f"{'aday':>36} {'namlu':>7} {'v':>6} {'R_tepe':>7} {'F_top':>7} "
      f"{'pencere':>14} {'gen':>6}")
sonuc = {}
for ad, strok, n, F, a, R_ag, goz in ADAY:
    r = V.kos(strok, n, F, 4.0, a, R_ag, goz, 0.165e-3)
    if r is None:
        print(f"{ad:>36}  --- basarisiz ---"); continue
    sonuc[ad] = r
    pen = f"{r['lo']:5.2f}-{r['hi']:5.2f}" if np.isfinite(r['lo']) else " ACILMIYOR  "
    print(f"{ad:>36} {r['L_namlu']:5.0f}mm {r['v']:5.1f} {r['R_tepe']:6.3f} "
          f"{r['F_top']:6.0f}N {pen:>14} {r['w']:5.2f}", flush=True)

print("\n=== MEKANIK SONUCLAR ===")
print(f"{'aday':>36} {'capraz pim':>22} {'tetik (PTFE)':>14} {'servo':>22}")
for ad, r in sonuc.items():
    F_yan = r["F_top"] / 2
    M = F_yan * (33.0 - 21.5) * 1e-3
    d_ok = next((d for d in (6, 8, 10)
                 if 503e6 / (M / (np.pi * (d * 1e-3) ** 3 / 32)) >= 2.5), None)
    SF = 503e6 / (M / (np.pi * (d_ok * 1e-3) ** 3 / 32)) if d_ok else 0
    N_pim = r["F_top"] / 2
    F_cek = 2 * 0.08 * N_pim
    uygun = [s for s, T in SERVO.items() if (T * kgcm / 6e-3) / F_cek >= 2.0]
    print(f"{ad:>36} O{d_ok} mm 7075 (SF {SF:.1f}) {F_cek:9.0f} N "
          f"{(uygun[0] if uygun else 'YETERSIZ'):>22}")

print("\n=== KURMA (bant basina el kuvveti) ===")
for ad, r in sonuc.items():
    print(f"{ad:>36} {r['n']} x {r['F_bant']:.0f} N = {r['F_bant']/9.81:.0f} kg/bant, "
          f"bant O{r['OD']:.1f} mm, kaucuk {r['L0']:.0f} mm, toplam {r['m_bant']:.0f} g")
