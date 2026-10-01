# -*- coding: utf-8 -*-
"""LASTIK BANT TAHRIKLI AG FIRLATICI — tam montaj (parametrik).

Yerlesim (+Y ileri, y=0 namlunun ACIK arka agzi = yukleme agzi):
      0 ..   5   arka pay
      5 ..  55   kapsul (kurulu konum)
     55 .. 234   STROK 179 mm
    234 .. 238   durdurma omuzu
    238 .. 260   iraksak agiz konisi (ALFA)
    244 .. 258   agiz bilezigi + bant kulaklari (+/-Z)

Tahrik: 2 adet 14/4 mm lateks tup, namlunun DISINDA +/-Z boyunca.
  on uc  : agiz bilezigindeki kulaga (yuksuk/civata)
  arka uc: kapsuldeki CAPRAZ PIMIN ucuna (Dyneema kopru ile)
Capraz pim namludaki iki DUZ YARIKTAN (+/-Z) disari cikar; hem bant
bagiantisi hem donme engelleyicidir -> YIV YOK (bkz. run_lastik.py:
alpha=19 yivsiz ~= alpha=18 yivli).
Tetik: iki karsilikli pim (+/-X), kapsuldeki tutma kanalina oturur.
Pim yuvasi kapakli: geri-getirme yayi icerde, ip RADYAL cikar.
"""
import FreeCAD as App, Part, math, os
from FreeCAD import Vector as V

P = dict(
    L_namlu=260.0, arka=5.0, L_kapsul=50.0, L_omuz=4.0, L_koni=22.0,
    D_bore=43.4, t_duvar=6.0, bosluk=0.30, omuz=3.0,
    ALFA=19.0, D_bilye=12.9, R_pitch=13.5, derinlik=4.2,
    t_kapak=8.0, t_govde=3.0,
    # kapsul arka bolgesi
    y_capraz=4.5, d_capraz=6.0, capraz_uzun=74.0,
    kanal_y0=9.0, kanal_w=5.4, kanal_d=5.0, hazne_y0=16.0,
    # yarik + bant
    yarik_w=6.4, r_bant=34.0, d_bant_gergin=7.5,
    bilezik_y0=244.0, bilezik_y1=258.0, bilezik_R=32.0, kulak_R=40.0,
    # tetik kartusu
    d_pim=5.0, boss_d=16.0, boss_h=18.0, d_yuva=9.6, d_ip=3.2,
    pad_l=26.0, pad_w=24.0, pad_t=4.0, d_vida=3.2,
)
Rb = 0.5 * P["D_bore"]; Ro = Rb + P["t_duvar"]
P["y_kap0"] = P["arka"]
P["STROK"] = P["L_namlu"] - P["arka"] - P["L_kapsul"] - P["L_omuz"] - P["L_koni"]
P["y_omuz"] = P["y_kap0"] + P["L_kapsul"] + P["STROK"]
P["y_capraz0"] = P["y_kap0"] + P["y_capraz"]
P["y_tetik"] = P["y_kap0"] + P["kanal_y0"] + 0.5 * P["kanal_w"]


def kutu(x0, x1, y0, y1, z0, z1):
    return Part.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))


def silindir(r, h, p, d):
    return Part.makeCylinder(r, h, p, d)


# ------------------------------------------------------------------ NAMLU
def namlu(p):
    L = p["L_namlu"]
    g = silindir(Ro, L, V(0, 0, 0), V(0, 1, 0))
    g = g.cut(silindir(Rb, L + 4, V(0, -2, 0), V(0, 1, 0)))

    # agiz bilezigi (koninin inceltti­gi duvari da takviye eder) + bant kulaklari
    bil = silindir(p["bilezik_R"], p["bilezik_y1"] - p["bilezik_y0"],
                   V(0, p["bilezik_y0"], 0), V(0, 1, 0))
    for s in (+1, -1):
        z0, z1 = (Ro - 1, p["kulak_R"]) if s > 0 else (-p["kulak_R"], -(Ro - 1))
        bil = bil.fuse(kutu(-6, 6, p["bilezik_y0"], p["bilezik_y1"], z0, z1))
    bil = bil.cut(silindir(Rb, 40, V(0, p["bilezik_y0"] - 5, 0), V(0, 1, 0)))
    for s in (+1, -1):     # bant yuksugu / civata deligi (Y yonunde)
        bil = bil.cut(silindir(2.75, 30, V(0, p["bilezik_y0"] - 5, s * p["r_bant"]),
                               V(0, 1, 0)))
    g = g.fuse(bil)

    # durdurma omuzu
    y_o = p["y_omuz"]
    g = g.fuse(silindir(Rb, p["L_omuz"], V(0, y_o, 0), V(0, 1, 0)).cut(
        silindir(Rb - p["omuz"], p["L_omuz"] + 2, V(0, y_o - 1, 0), V(0, 1, 0))))
    # iraksak agiz konisi
    y_k = L - p["L_koni"]
    R2 = Rb + p["L_koni"] * math.tan(math.radians(p["ALFA"]))
    g = g.cut(Part.makeCone(Rb, R2, p["L_koni"] + 0.5, V(0, y_k, 0), V(0, 1, 0)))

    # capraz pim yariklari (+/-Z), strok boyunca DUZ
    ya = p["y_capraz0"] - p["d_capraz"] / 2 - 1.0
    yb = p["y_capraz0"] + p["STROK"] + p["d_capraz"] / 2 + 1.0
    w = p["yarik_w"] / 2
    for s in (+1, -1):
        z0, z1 = (Rb - 1, Ro + 1) if s > 0 else (-(Ro + 1), -(Rb - 1))
        g = g.cut(kutu(-w, w, ya, yb, z0, z1))

    # tetik kartusu (+/-X): gobek + ic yuva + kapak ipi deligi
    y_t = p["y_tetik"]
    for s in (+1, -1):
        u = V(s, 0, 0)
        boss = silindir(p["boss_d"] / 2, p["boss_h"] + 2, V(s * (Ro - 2), y_t, 0), u)
        g = g.fuse(boss)
        pad = kutu(-p["pad_t"] / 2, p["pad_t"] / 2, -p["pad_l"] / 2, p["pad_l"] / 2,
                   -p["pad_w"] / 2, p["pad_w"] / 2)
        pad.translate(V(s * (Ro + 1.0), y_t + 34.0, 0))
        g = g.fuse(pad)
        for dz in (-8.0, 8.0):
            g = g.cut(silindir(p["d_vida"] / 2, 12, V(s * (Ro - 4), y_t + 34.0, dz), u))
    # pim deligi (duvar) + yay yuvasi (gobek ici) + ip deligi (kapak)
    r_yuva0, r_yuva1 = Ro + 3.3, Ro + p["boss_h"] - 2.0
    for s in (+1, -1):
        u = V(s, 0, 0)
        g = g.cut(silindir(p["d_pim"] / 2 + 0.1, r_yuva0 - Rb + 1,
                           V(s * (Rb - 0.5), y_t, 0), u))
        g = g.cut(silindir(p["d_yuva"] / 2, r_yuva1 - r_yuva0,
                           V(s * r_yuva0, y_t, 0), u))
        g = g.cut(silindir(p["d_ip"] / 2, 6, V(s * (r_yuva1 - 0.5), y_t, 0), u))
    return g.removeSplitter()


# ------------------------------------------------------------------ KAPSUL
def kapsul(p, y0):
    Rk = Rb - p["bosluk"] / 2
    Rh = Rk - p["t_govde"]
    L, tk = p["L_kapsul"], p["t_kapak"]
    a = math.radians(p["ALFA"])
    g = silindir(Rk, L, V(0, 0, 0), V(0, 1, 0))
    g = g.cut(silindir(Rh, L - tk - p["hazne_y0"], V(0, p["hazne_y0"], 0), V(0, 1, 0)))
    # tutma kanali (tetik pimleri buraya oturur)
    g = g.cut(silindir(Rk + 4, p["kanal_w"], V(0, p["kanal_y0"], 0), V(0, 1, 0)).cut(
        silindir(Rk - p["kanal_d"], p["kanal_w"] + 2, V(0, p["kanal_y0"] - 1, 0),
                 V(0, 1, 0))))
    # capraz pim deligi (Z boyunca)
    g = g.cut(silindir(p["d_capraz"] / 2 + 0.05, 2 * Rk + 4,
                       V(0, p["y_capraz"], -(Rk + 2)), V(0, 0, 1)))
    # bilye yuvalari (ALFA kadar disa egik)
    for i in range(6):
        th = math.radians(60 * i)
        ur = V(math.cos(th), 0, math.sin(th))
        eks = V(ur.x * math.sin(a), math.cos(a), ur.z * math.sin(a))
        c = V(ur.x * p["R_pitch"], L, ur.z * p["R_pitch"])
        taban = c - eks * p["derinlik"]
        g = g.cut(Part.makeSphere(0.5 * p["D_bilye"], taban).fuse(
            silindir(0.5 * p["D_bilye"], p["derinlik"] + 8, taban, eks)))
    # ag cikis deligi
    g = g.cut(silindir(Rh * 0.62, tk + 2, V(0, L - tk - 1, 0), V(0, 1, 0)))
    g = g.removeSplitter()
    g.translate(V(0, y0, 0))
    return g


def bilyeler(p, y0):
    a = math.radians(p["ALFA"]); L = p["L_kapsul"]
    s = None
    for i in range(6):
        th = math.radians(60 * i)
        ur = V(math.cos(th), 0, math.sin(th))
        eks = V(ur.x * math.sin(a), math.cos(a), ur.z * math.sin(a))
        c = V(ur.x * p["R_pitch"], y0 + L, ur.z * p["R_pitch"]) - eks * p["derinlik"]
        k = Part.makeSphere(0.5 * p["D_bilye"] - 0.15, c)
        s = k if s is None else s.fuse(k)
    return s


def capraz_pim(p):
    y = p["y_capraz0"]; h = p["capraz_uzun"]
    c = silindir(p["d_capraz"] / 2, h, V(0, y, -h / 2), V(0, 0, 1))
    for s in (+1, -1):      # bant koprusu icin uc olukları
        zc = s * p["r_bant"]
        oluk = silindir(p["d_capraz"] / 2 + 1, 2.0, V(0, y, zc - 1.0), V(0, 0, 1)).cut(
            silindir(p["d_capraz"] / 2 - 0.8, 3.0, V(0, y, zc - 1.5), V(0, 0, 1)))
        c = c.cut(oluk)
    return c


def bantlar(p):
    """Gergin (kurulu) haldeki iki lateks tup."""
    y0 = p["y_capraz0"] + 6.0        # kopru ipi + arka yuksuk sonrasi
    y1 = p["bilezik_y0"]
    bs = []
    for s in (+1, -1):
        bs.append(silindir(p["d_bant_gergin"] / 2, y1 - y0,
                           V(0, y0, s * p["r_bant"]), V(0, 1, 0)))
    return bs


def tetik_pimleri(p):
    """Kartus ici pim: uc -> O5 govde -> O9 yaka -> O3 ip cubugu."""
    y = p["y_tetik"]
    r_uc = Rb - p["kanal_d"]                  # kanal dibine 0.15 mm pay
    r_yaka = Ro + 4.3
    out = []
    for s in (+1, -1):
        u = V(s, 0, 0)
        govde = silindir(p["d_pim"] / 2 - 0.1, r_yaka - r_uc + 0.15,
                         V(s * (r_uc + 0.15), y, 0), u)
        yaka = silindir(4.4, 3.0, V(s * r_yaka, y, 0), u)
        cubuk = silindir(1.4, 12.0, V(s * (r_yaka + 3.0), y, 0), u)
        out.append(govde.fuse(yaka).fuse(cubuk))
    return out


if __name__ == "__main__":
    out = os.path.dirname(os.path.abspath(__file__))
    yk = P["y_kap0"]
    b1, b2 = bantlar(P)
    t1, t2 = tetik_pimleri(P)
    parcalar = {
        "L_namlu": namlu(P), "L_kapsul": kapsul(P, yk), "L_bilye": bilyeler(P, yk),
        "L_capraz_pim": capraz_pim(P), "L_bant_ust": b1, "L_bant_alt": b2,
        "L_pim_sag": t1, "L_pim_sol": t2,
    }
    tum = None
    for ad, sh in parcalar.items():
        sh.exportBrep(os.path.join(out, ad + ".brep"))
        sh.exportStep(os.path.join(out, ad + ".step"))
        print(f"{ad:14s} hacim={sh.Volume/1000:8.2f} cm3 gecerli={sh.isValid()}")
        tum = sh if tum is None else tum.fuse(sh)
    Part.Shape(tum).exportStep(os.path.join(out, "LASTIK_MONTAJ.step"))
    print(f"LASTIK_MONTAJ.step | namlu {P['L_namlu']:.0f} mm, strok {P['STROK']:.0f} mm, "
          f"tetik y={P['y_tetik']:.1f}, capraz pim y={P['y_capraz0']:.1f}")
