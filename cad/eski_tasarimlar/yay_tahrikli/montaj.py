# -*- coding: utf-8 -*-
"""TAM MONTAJ: namlu + yay + kapsul + bilyeler + tetik pimleri.

Yerlesim (+Y ileri, y=0 dipcik):
    0 ........ L_yay_kurulu : yay (kurulu halde)
    .......... +L_kapsul    : kapsul (kurulu konum)
    .......... +STROK       : kapsulun gittigi yol
    .......... omuz         : durdurma omuzu (kapsul burada durur)
    .......... +L_koni      : iraksak agiz konisi -> namlu agzi
"""
import FreeCAD as App, Part, math, os
from FreeCAD import Vector as V

P = dict(
    D_bore=43.4, t_duvar=6.0,
    L_yay_kurulu=160.0, L_kapsul=50.0, STROK=250.0,
    L_omuz=4.0, L_koni=22.0, omuz=3.0,
    twist=730.0, n_yiv=6, yiv_w=3.4, yiv_d=1.4,
    ALFA=18.0, D_bilye=12.9, R_pitch=13.5, derinlik=4.2,
    t_kapak=8.0, t_govde=3.0, t_arka=14.0, bosluk=0.30,
    # kapsul uzerindeki TUTMA KANALI (pimler buraya oturur)
    kanal_y0=4.0, kanal_w=5.4, kanal_d=5.0,
    d_tel=3.5, D_yay=30.0, n_sarim=44.0,
    # --- TETIK: iki AYRI pim, karsilikli, iki servo + ip ile cekilir ---
    d_pim=5.0,          # celik pim capi
    pim_girinti=5.0,    # pimin namlu icine giris derinligi
    boss_h=10.0,        # pim kilavuz gobegi yuksekligi (OD disina)
    boss_d=14.0,        # gobek capi
    pad_l=26.0, pad_w=24.0, pad_t=4.0,   # servo montaj yatagi
    d_vida=3.2,
)
P["L_namlu"] = (P["L_yay_kurulu"] + P["L_kapsul"] + P["STROK"]
                + P["L_omuz"] + P["L_koni"])
P["y_omuz"] = P["L_yay_kurulu"] + P["L_kapsul"] + P["STROK"]
# pim, kapsulun arka yuzune temas edecek sekilde
# Pim, kapsul uzerindeki tutma kanalinin ICINE oturur. Kapsul ileri
# itildiginde kanalin ARKA duvari (ileri bakan yuz) pime dayanir.
P["y_pim"] = P["L_yay_kurulu"] + P["kanal_y0"] + 0.5 * P["kanal_w"]


def helis_kanal(Rb, L, twist, th0, w, d, y0=-3.0):
    h = Part.makeHelix(twist, L + 6.0, Rb)
    # makePlane(uzunluk_x, genislik_y): x = RADYAL, y = CEVRESEL
    prof = Part.makePlane(d + 0.2, w, V(Rb - 0.1, -w / 2.0, 0.0))
    m = App.Matrix(); m.rotateZ(math.radians(th0))
    h = h.copy(); h.transformShape(m)
    prof = prof.copy(); prof.transformShape(m)
    k = Part.Wire(h.Edges).makePipeShell([Part.Wire(prof.Edges)], True, True)
    k = k.Solids[0] if k.Solids else Part.Solid(Part.Shell(k.Faces))
    mr = App.Matrix(); mr.rotateX(math.radians(-90))
    k = k.copy(); k.transformShape(mr)
    k.translate(V(0.0, y0, 0.0))
    return k


def helis_kama(Rk, L, twist, th0, w, d):
    """Kapsul uzerinde HELIS kama (namlu yivine oturur)."""
    h = Part.makeHelix(twist, L - 2.0, Rk - 0.8 + (d + 0.8) * 0.5)
    # kama: kapsul disindan (Rk) yiv dibine kadar, yanal bosluklu
    # profil kapsul yuzeyine TEGET olmamali; 0.8 mm iceri gomuyoruz ki
    # fuse temiz olsun (tegetlik gecersiz kati uretiyor)
    prof = Part.makePlane(d + 0.8, w, V(Rk - 0.8, -w / 2.0, 0.0))
    m = App.Matrix(); m.rotateZ(math.radians(th0))
    h = h.copy(); h.transformShape(m)
    prof = prof.copy(); prof.transformShape(m)
    k = Part.Wire(h.Edges).makePipeShell([Part.Wire(prof.Edges)], True, True)
    k = k.Solids[0] if k.Solids else Part.Solid(Part.Shell(k.Faces))
    mr = App.Matrix(); mr.rotateX(math.radians(-90))
    k = k.copy(); k.transformShape(mr)
    k.translate(V(0.0, 1.0, 0.0))
    return k


def namlu(p):
    Rb, Ro, L = 0.5 * p["D_bore"], 0.5 * p["D_bore"] + p["t_duvar"], p["L_namlu"]
    g = Part.makeCylinder(Ro, L, V(0, 0, 0), V(0, 1, 0))
    g = g.cut(Part.makeCylinder(Rb, L + 4, V(0, -2, 0), V(0, 1, 0)))
    for i in range(p["n_yiv"]):
        try:
            g = g.cut(helis_kanal(Rb, L, p["twist"], 360.0 * i / p["n_yiv"],
                                  p["yiv_w"], p["yiv_d"]))
        except Exception:
            pass
    # iraksak agiz konisi
    y_k = L - p["L_koni"]
    R2 = Rb + p["L_koni"] * math.tan(math.radians(p["ALFA"]))
    g = g.cut(Part.makeCone(Rb, R2, p["L_koni"] + 0.5, V(0, y_k, 0), V(0, 1, 0)))
    # durdurma omuzu
    y_o = p["y_omuz"]
    bilezik = Part.makeCylinder(Rb, p["L_omuz"], V(0, y_o, 0), V(0, 1, 0)).cut(
        Part.makeCylinder(Rb - p["omuz"], p["L_omuz"] + 2, V(0, y_o - 1, 0), V(0, 1, 0)))
    g = g.fuse(bilezik)
    # ---- TETIK ISTASYONU: iki karsilikli pim, kilavuz gobegi, servo yatagi ----
    y_p = p["y_pim"]
    for th_d in (0.0, 180.0):
        th = math.radians(th_d)
        u = V(math.cos(th), 0.0, math.sin(th))      # disa radyal birim
        # 1) kilavuz gobegi (pimi cift noktadan destekler -> egilmez)
        boss = Part.makeCylinder(0.5 * p["boss_d"], p["boss_h"] + 2.0,
                                 V(u.x * (Ro - 2.0), y_p, u.z * (Ro - 2.0)), u)
        g = g.fuse(boss)
        # 2) servo montaj yatagi (duz yuzey + 2 vida)
        pad = Part.makeBox(p["pad_t"], p["pad_l"], p["pad_w"],
                           V(-p["pad_t"] / 2, -p["pad_l"] / 2, -p["pad_w"] / 2))
        mp = App.Matrix(); mp.rotateY(-th)
        pad = pad.copy(); pad.transformShape(mp)
        pad.translate(V(u.x * (Ro + p["boss_h"] * 0.35),
                        y_p - 30.0,
                        u.z * (Ro + p["boss_h"] * 0.35)))
        g = g.fuse(pad)
        for dy in (-9.0, 9.0):
            vida = Part.makeCylinder(0.5 * p["d_vida"], p["pad_t"] + 8,
                                     V(u.x * (Ro - 2), y_p - 30.0 + dy,
                                       u.z * (Ro - 2)), u)
            g = g.cut(vida)
    # 3) pim deligi: capraz gecen TEK delik (iki pim ayri ayri girer)
    delik = Part.makeCylinder(0.5 * p["d_pim"] + 0.1,
                              2 * (Ro + p["boss_h"]) + 8,
                              V(-(Ro + p["boss_h"] + 4), y_p, 0), V(1, 0, 0))
    g = g.cut(delik)
    return g.removeSplitter()


def kapsul(p, y0):
    Ro = 0.5 * (p["D_bore"] - p["bosluk"])
    Rh = Ro - p["t_govde"]
    L, tk, ta = p["L_kapsul"], p["t_kapak"], p["t_arka"]
    a = math.radians(p["ALFA"])
    g = Part.makeCylinder(Ro, L, V(0, 0, 0), V(0, 1, 0))
    g = g.cut(Part.makeCylinder(Rh, L - tk - ta, V(0, ta, 0), V(0, 1, 0)))
    for i in range(6):
        th = math.radians(60 * i)
        u = V(math.cos(th), 0, math.sin(th))
        eks = V(u.x * math.sin(a), math.cos(a), u.z * math.sin(a))
        c = V(u.x * p["R_pitch"], L, u.z * p["R_pitch"])
        taban = c - eks * p["derinlik"]
        g = g.cut(Part.makeSphere(0.5 * p["D_bilye"], taban).fuse(
            Part.makeCylinder(0.5 * p["D_bilye"], p["derinlik"] + 8, taban, eks)))
    # --- HELIS kamalar: namlu yiviyle AYNI adim (duz kama helis yive girmez) ---
    for i in range(p["n_yiv"]):
        th0 = 360.0 * i / p["n_yiv"]
        try:
            g = g.fuse(helis_kama(Ro, L, p["twist"], th0,
                                  p["yiv_w"] - 0.4, p["yiv_d"] - 0.15))
        except Exception:
            pass
    # --- pimlerin oturacagi TUTMA KANALI (arka masif bolgede) ---
    g = g.cut(Part.makeCylinder(Ro + 4, p["kanal_w"], V(0, p["kanal_y0"], 0),
                                V(0, 1, 0))
              .cut(Part.makeCylinder(Ro - p["kanal_d"], p["kanal_w"] + 2,
                                     V(0, p["kanal_y0"] - 1, 0), V(0, 1, 0))))
    g = g.cut(Part.makeCylinder(Rh * 0.62, tk + 2, V(0, L - tk - 1, 0), V(0, 1, 0)))
    g = g.removeSplitter()
    g.translate(V(0, y0, 0))
    return g


def bilyeler(p, y0):
    a = math.radians(p["ALFA"]); L = p["L_kapsul"]
    kureler = []
    for i in range(6):
        th = math.radians(60 * i)
        u = V(math.cos(th), 0, math.sin(th))
        eks = V(u.x * math.sin(a), math.cos(a), u.z * math.sin(a))
        c = V(u.x * p["R_pitch"], y0 + L, u.z * p["R_pitch"]) - eks * p["derinlik"]
        kureler.append(Part.makeSphere(0.5 * p["D_bilye"] - 0.15, c))
    s = kureler[0]
    for k in kureler[1:]:
        s = s.fuse(k)
    return s


def yay(p):
    d, D, n, Lk = p["d_tel"], p["D_yay"], p["n_sarim"], p["L_yay_kurulu"]
    h = Part.makeHelix(Lk / n, Lk, 0.5 * D)
    prof = Part.Wire(Part.makeCircle(0.5 * d, V(0.5 * D, 0, 0), V(0, 1, 0)).Edges)
    s = Part.Wire(h.Edges).makePipeShell([prof], True, True)
    s = s.Solids[0] if s.Solids else Part.Solid(Part.Shell(s.Faces))
    mr = App.Matrix(); mr.rotateX(math.radians(-90))
    s = s.copy(); s.transformShape(mr)
    return s


def pimler(p):
    """IKI AYRI pim. Her biri kendi tarafindan girer, namlu icine yalnizca
    pim_girinti kadar sokulur -> ortada BIRLESMEZLER. Disa dogru cekilirler."""
    Rb = 0.5 * p["D_bore"]
    Ro = Rb + p["t_duvar"]
    y = p["y_pim"]
    r_ic = Rb - p["pim_girinti"]                 # pim ucunun eksene mesafesi
    r_dis = Ro + p["boss_h"] + 6.0               # ip baglama gozu disarida
    ps = []
    for th_d in (0.0, 180.0):
        th = math.radians(th_d)
        u = V(math.cos(th), 0.0, math.sin(th))
        govde = Part.makeCylinder(0.5 * p["d_pim"] - 0.1, r_dis - r_ic,
                                  V(u.x * r_ic, y, u.z * r_ic), u)
        # ip baglama gozu (disaridaki halka)
        goz = Part.makeCylinder(0.5 * p["d_pim"] + 2.0, 3.0,
                                V(u.x * (r_dis - 3.0), y, u.z * (r_dis - 3.0)), u)
        goz = goz.cut(Part.makeCylinder(1.2, 20, V(u.x * (r_dis - 1.5), y - 10,
                                                   u.z * (r_dis - 1.5)), V(0, 1, 0)))
        ps.append(govde.fuse(goz))
    return ps[0], ps[1]


if __name__ == "__main__":
    out = os.path.dirname(os.path.abspath(__file__))
    y_kaps = P["L_yay_kurulu"]
    parcalar = {
        "M_namlu": namlu(P),
        "M_kapsul": kapsul(P, y_kaps),
        "M_bilye": bilyeler(P, y_kaps),
        "M_yay": yay(P),
        "M_pim_sag": pimler(P)[0],
        "M_pim_sol": pimler(P)[1],
    }
    tum = None
    for ad, sh in parcalar.items():
        sh.exportBrep(os.path.join(out, ad + ".brep"))
        print(f"{ad}: hacim={sh.Volume/1000:8.2f} cm3  gecerli={sh.isValid()}")
        tum = sh if tum is None else tum.fuse(sh)
    Part.Shape(tum).exportStep(os.path.join(out, "MONTAJ.step"))
    print(f"MONTAJ.step yazildi | namlu boyu = {P['L_namlu']:.0f} mm, "
          f"omuz @ {P['y_omuz']:.0f} mm")
