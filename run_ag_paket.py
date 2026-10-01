"""AG GEOMETRISI + PAKETLEME HACMI (gercek hesap, tahmin degil).

GOZ (mesh) = agdaki her bir KARE deligin kenar uzunlugu. 140 mm goz demek,
her delik 140x140 mm demek. Kucuk goz = daha cok iplik = daha cok surukleme
+ daha buyuk paket; buyuk goz = hedef delikten gecebilir.

Ag ALTIGEN: 6 bilye koselerde. R = kose yaricapi.
  kose-kose (en genis)  = 2R
  duz kenarlar arasi    = 2R*cos(30) = 1.732 R
  alan                  = 1.5*sqrt(3)*R^2
  iplik boyu            = 2*alan/goz  (iki yonde orgu) + 6R (cevre)
  dugum sayisi          ~ alan/goz^2
"""
import numpy as np

# PE orgu misina (Dyneema) — cap [mm], lineer yogunluk [g/m]
IP = {"PE #0.8": (0.148, 0.017), "PE #1": (0.165, 0.021), "PE #1.5": (0.205, 0.032),
      "PE #3": (0.285, 0.062)}
RHO = 970.0
HAZNE_D = 37.1e-3
HAZNE_A = np.pi * 0.25 * HAZNE_D ** 2


def ag(R, goz, ip_goz="PE #1", ip_cevre="PE #3"):
    A = 1.5 * np.sqrt(3) * R ** 2
    L_goz = 2 * A / goz
    L_cev = 6 * R
    dg, mg = IP[ip_goz]; dc, mc = IP[ip_cevre]
    V = (np.pi * 0.25 * (dg * 1e-3) ** 2 * L_goz
         + np.pi * 0.25 * (dc * 1e-3) ** 2 * L_cev)
    return dict(R=R, goz=goz, A=A, kose=2 * R, duz=2 * R * np.cos(np.pi / 6),
                L_goz=L_goz, L_cev=L_cev, L_top=L_goz + L_cev,
                dugum=int(A / goz ** 2), m=(L_goz * mg + L_cev * mc),
                V_kati=V * 1e6)


if __name__ == "__main__":
    print("=== GOZ NEDIR? ===")
    print("  Agdaki her KARE deligin kenari. 140 mm goz = 140x140 mm delik.")
    print("  X-UAV Talon pervanesi ~230 mm -> 140 mm goz pervaneyi GECIRMEZ.\n")

    print("=== MEVCUT AG (v3): R=1.4 m, goz 140 mm ===")
    a = ag(1.4, 0.140)
    print(f"  kose-kose genislik : {a['kose']:.2f} m   <-- 'ag capi' dedigim bu")
    print(f"  duz kenarlar arasi : {a['duz']:.2f} m")
    print(f"  alan               : {a['A']:.2f} m2")
    print(f"  iplik              : {a['L_goz']:.0f} m goz + {a['L_cev']:.0f} m cevre "
          f"= {a['L_top']:.0f} m")
    print(f"  dugum sayisi       : ~{a['dugum']}")
    print(f"  kutle              : {a['m']:.2f} g")
    print(f"  KATI hacim         : {a['V_kati']:.2f} cm3\n")

    print("=== PAKETLEME: elle katlanmis agin gercek hacmi ===")
    print("  Dugumlu misina serbest katlandiginda kati hacminin ancak")
    print("  %20-35'i kadar yogunluga ulasir (dugumler bosluk birakir).\n")
    print(f"{'dolgu':>7} {'paket hacim':>12} {'gereken hazne boyu (O37.1)':>28}")
    for dol in (0.20, 0.25, 0.30, 0.35):
        Vp = a['V_kati'] / dol
        L = Vp * 1e-6 / HAZNE_A * 1e3
        print(f"{dol*100:5.0f}% {Vp:10.1f} cm3 {L:22.1f} mm")
    print(f"\n  v3'te hazne 8 mm ({HAZNE_A*8e-3*1e6:.1f} cm3) idi -> "
          f"%{100*a['V_kati']/(HAZNE_A*8e-3*1e6):.0f} dolgu gerekir. COK SIKI!")
    print(f"  ONERI: hazne >= 16 mm ({HAZNE_A*16e-3*1e6:.1f} cm3) -> "
          f"%{100*a['V_kati']/(HAZNE_A*16e-3*1e6):.0f} dolgu. Rahat.\n")

    print("=== AG BOYUTU SECENEKLERI (hazne boyu %25 dolguya gore) ===")
    print(f"{'R':>5} {'kose-kose':>10} {'goz':>6} {'iplik':>7} {'kutle':>6} "
          f"{'kati':>7} {'hazne':>7}")
    for R in (1.2, 1.4, 1.6):
        for goz in (0.120, 0.140, 0.160):
            x = ag(R, goz)
            L = x['V_kati'] / 0.25 * 1e-6 / HAZNE_A * 1e3
            print(f"{R:5.1f} {x['kose']:9.2f}m {goz*1e3:5.0f}mm {x['L_top']:6.0f}m "
                  f"{x['m']:5.2f}g {x['V_kati']:6.2f}cc {L:6.1f}mm")
