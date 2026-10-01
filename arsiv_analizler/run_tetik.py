"""TETIK MEKANIZMASI HESABI: pimleri cekmek icin ne kadar kuvvet gerekir?

Kurulu yayin kuvveti kapsulu pimlere bastirir. Pimi RADYAL cekmek icin
bu normal yukun yarattigi SURTUNMEYI yenmek gerekir:
    F_cekme = mu * N_pim
Servo bunu bir ip + makara yaricapi uzerinden saglar:
    F_servo = T_servo / r_makara
"""
import numpy as np

F_YAY = 316.0          # kurulu yay kuvveti [N]  (k=1.26 N/mm, x0=250 mm)
MU = {"PETG-celik (kuru)": 0.30, "PETG-celik (yagli)": 0.18,
      "PTFE burc-celik": 0.08}
D_PIM = 5.0e-3
T_DUVAR = 6.0e-3

print("=== 1) PIM BASINA YUK ===")
for n in (1, 2):
    print(f"  {n} pim -> pim basina normal yuk N = {F_YAY/n:6.1f} N")

print("\n=== 2) CEKME KUVVETI (2 pim, pim basina) ===")
N = F_YAY / 2
for ad, mu in MU.items():
    print(f"  {ad:22s} mu={mu:.2f} -> F_cekme = {mu*N:6.1f} N")

print("\n=== 3) SERVO YETER MI?  (F = T / r_makara) ===")
SERVO = {"SG90 (mikro)": 0.18, "MG90S (metal disli mikro)": 0.32,
         "MG996R @6V": 1.08, "DS3218 @6.8V": 2.06}
print(f"{'servo':>26} {'tork':>8} " + "".join(f"{f'r={r}mm':>9}" for r in (6, 8, 10, 14)))
for ad, T in SERVO.items():
    sat = "".join(f"{T/(r*1e-3):8.0f}N" for r in (6, 8, 10, 14))
    print(f"{ad:>26} {T:6.2f}Nm {sat}")
F_ger = 0.30 * N
print(f"\n  Gereken (kuru PETG, mu=0.30): {F_ger:.0f} N / pim")
print("  -> MG996R sinifi + r<=10 mm makara YETER (emniyet ~2x).")
print("  -> Mikro servo (SG90/MG90S) YETMEZ.")

print("\n=== 4) PIM MUKAVEMETI (cift kesme) ===")
A_kesme = 2 * np.pi * 0.25 * D_PIM ** 2
print(f"  celik pim Ø{D_PIM*1e3:.0f} mm, cift kesme alani {A_kesme*1e6:.1f} mm2")
print(f"  kesme gerilmesi tau = {N/A_kesme/1e6:.1f} MPa   (celik sinir ~200 MPa)"
      f"  -> SF = {200e6/(N/A_kesme):.0f}x")
A_ezilme = 2 * D_PIM * T_DUVAR
print(f"  PETG delik ezilme: {N/A_ezilme/1e6:.1f} MPa  (PETG ~50 MPa)"
      f"  -> SF = {50e6/(N/A_ezilme):.0f}x")

print("\n=== 5) SENKRONIZASYON: bir pim once cikarsa ne olur? ===")
m_har = 0.087          # kapsul + ucan kutle [kg]
a = F_YAY / m_har
print(f"  kapsul ivmesi a = F/m = {a:.0f} m/s^2")
for dt_ms in (5, 10, 20, 50):
    dt = dt_ms * 1e-3
    print(f"  {dt_ms:2d} ms gecikme -> tek pim {F_YAY:.0f} N'u TEK BASINA tasir, "
          f"eksen disi moment = {F_YAY*0.0192:.1f} N.m  (kol r=19 mm)")
    break
print("""
  Kapsul eksenel olarak hala BLOKELI (ikinci pim duruyor), yani firlamaz.
  Yuk tek tarafli olur: ~6 N.m moment (kol ~19 mm). Bunu 50 mm boyunca
  kamalar karsilar -> uclarda ~120 N tepki, egilme 0.34 derece. Yani etki
  KUCUK; sadece ilk mm'de biraz fazla surtunme.

  YINE DE: iki BAGIMSIZ servo 10-20 ms icinde senkronize olur ve bu
  sureden once kapsul zaten hareket edemez. Asil risk servolardan birinin
  TAKILMASI / arizasi. Mekanik olarak bagli tek tahrik bu riski kaldirir.""")
