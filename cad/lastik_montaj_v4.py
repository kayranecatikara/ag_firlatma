# -*- coding: utf-8 -*-
"""LASTIK BANT TAHRIKLI AG FIRLATICI — v4 (namlu <=180 mm, 4 bant).

v1'den farklar:
  * DURDURMA OMUZU KALDIRILDI: omuzun ic yaricapi (18.7) bilyelerin dis
    kenarindan (~19.9) kucuktu -> kapsul durduktan sonra bilyeler omuza
    CARPIYORDU. Artik kapsulu capraz pimin yarik SONUNA carpmasi durdurur
    (yarik sonlarinda TPU tampon). Delik agiza kadar acik.
  * Namlu boyu parametrik: L = 5 + 4.5 + STROK + D_son + 3
    (D_son = L0 + H: bant, capraz pim durdugu anda tam gevsek olur).
  * Tetik kartusu kapaklari AYRI parca (M2 ile vidalanir) — pim+yay
    montajdan sonra takilabilsin diye.
  * Servo yataklari: MIKRO SERVO (Savox SH-0255MG / MG92B sinifi, ~14 g),
    M2 oval delik, 28 mm aralik. MG996R DEGIL -- bkz. README.
  * Bilye O12.7 (standart 1/2").
Koordinatlar: +Y ileri (agiz), y=0 acik arka agiz, bantlar +/-Z, tetik +/-X.
"""
import FreeCAD as App, Part, math, os, json
from FreeCAD import Vector as V

OUT = os.path.dirname(os.path.abspath(__file__))
KONFIG = os.path.join(OUT, "v4_konfig.json")

P = dict(
    STROK=120.0, L_hazne=10.0, H=18.0, lam=3.5, bant_OD=16.0, bant_ID=4.0,
    D_bore=43.4, t_duvar=6.0, bosluk=0.30, arka=5.0,
    ALFA=19.0, koni_acisi=21.0, D_bilye=12.7, D_yuva=12.9, R_pitch=13.5,
    derinlik=4.2,
    # kapsul: arka blok (capraz pim) + tutma kanali + hazne + on kapak
    y_capraz=4.5, d_capraz=6.0, capraz_uzun=78.0,
    kanal_y0=9.0, kanal_w=5.4, kanal_d=5.0, t_arka_blok=16.0, t_kapak=8.0,
    t_govde=3.0,
    yarik_w=9.4, tampon=3.0, r_bant=33.0, dz_bant=11.0,
    kulak_R=42.0, bilezik_R=32.0, bilezik_L=14.0, d_ankraj=6.5,
    # tetik kartusu
    d_pim=5.0, boss_d=18.0, boss_h=16.5, d_yuva_pim=10.6, kapak_t=3.0, d_ip=2.0,
    d_M2=1.7, pad_l=36.0, pad_w=15.0, pad_t=4.0, pad_ofset=30.0,
    # namluyu iki parcaya bolme (bkz. namlu_bol)
    y_bol=128.0, t_spigot=14.0, spigot_derin=3.0, spigot_bosluk=0.25,
    servo_delik=14.0, servo_slot=2.0,   # +-14 mm (28 mm aralik), oval
)
if os.path.exists(KONFIG):
    P.update(json.load(open(KONFIG)))

Rb = 0.5 * P["D_bore"]; Ro = Rb + P["t_duvar"]
L0 = P["STROK"] / (P["lam"] - 1.0)
P["L0"] = L0
P["D_son"] = L0 + P["H"]
P["L_kapsul"] = P["t_arka_blok"] + P["L_hazne"] + P["t_kapak"]
P["y_capraz0"] = P["arka"] + P["y_capraz"]
P["y_capraz1"] = P["y_capraz0"] + P["STROK"]
P["y_ankraj"] = P["y_capraz1"] + P["D_son"]
P["L_namlu"] = max(P["y_ankraj"] + 5.0,
                   P["arka"] + P["L_kapsul"] + P["STROK"] + 6.0)
P["y_yuz_dur"] = P["y_capraz1"] - P["y_capraz"] + P["L_kapsul"]   # durmus kapsul agzi
P["y_tetik"] = P["arka"] + P["kanal_y0"] + 0.5 * P["kanal_w"]


def kutu(x0, x1, y0, y1, z0, z1):
    return Part.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))


def sil(r, h, p, d):
    return Part.makeCylinder(r, h, p, d)


def namlu(p):
    L = p["L_namlu"]
    g = sil(Ro, L, V(0, 0, 0), V(0, 1, 0)).cut(sil(Rb, L + 4, V(0, -2, 0), V(0, 1, 0)))
    # iraksak koni: durmus kapsul agzindan namlu agzina (bilye yolundan genis)
    yk = p["y_yuz_dur"]; Lk = L - yk
    R2 = Rb + Lk * math.tan(math.radians(p["koni_acisi"]))
    # agiz bilezigi + bant kulaklari: SADECE on ucta (bant arkada namlu
    # borusunun ustunden gecer). Delik bilezik boyunca TAMAMEN acilir.
    y0 = p["y_ankraj"] - 9.0; y1 = L
    bil = sil(p["bilezik_R"], y1 - y0, V(0, y0, 0), V(0, 1, 0))
    for s in (+1, -1):
        z0, z1 = (Ro - 1, p["kulak_R"]) if s > 0 else (-p["kulak_R"], -(Ro - 1))
        bil = bil.fuse(kutu(-7, 7, y0, y1, z0, z1))
    bil = bil.cut(sil(Rb, y1 - y0 + 2, V(0, y0 - 1, 0), V(0, 1, 0)))
    ya = p["y_ankraj"]
    for s in (+1, -1):    # her kenarda 2 ankraj (2 bant)
        for zc in (s * p["r_bant"], s * (p["r_bant"] + p["dz_bant"])):
            bil = bil.cut(kutu(-2.8, 2.8, ya - 7, y1 + 1, zc - 4.5, zc + 4.5))
            bil = bil.cut(sil(2.05, 24, V(-12, ya, zc), V(1, 0, 0)))
    g = g.fuse(bil)
    # iraksak koni en son: bilezik dahil her seyi keser
    g = g.cut(Part.makeCone(Rb, R2, Lk + 0.5, V(0, yk, 0), V(0, 1, 0)))
    # capraz pim yariklari: arka ucu kurulu pimin arkasi, ON UCU = DURDURMA
    w = p["yarik_w"] / 2
    ya = p["y_capraz0"] - p["d_capraz"] / 2 - 1.0
    yb = p["y_capraz1"] + p["d_capraz"] / 2 + p["tampon"]
    for s in (+1, -1):
        z0, z1 = (Rb - 1, Ro + 1) if s > 0 else (-(Ro + 1), -(Rb - 1))
        g = g.cut(kutu(-w, w, ya, yb, z0, z1))
    # tetik kartusu gobekleri (+/-X)
    y_t = p["y_tetik"]
    r_yuva0 = 29.0             # yaka oturma yuzeyi (pim ucu kanal dibine 0.3 mm pay)
    for s in (+1, -1):
        u = V(s, 0, 0)
        g = g.fuse(sil(p["boss_d"] / 2, p["boss_h"] + 2, V(s * (Ro - 2), y_t, 0), u))
        g = g.cut(sil(p["d_pim"] / 2 + 0.1, r_yuva0 - Rb + 1, V(s * (Rb - 0.5), y_t, 0), u))
        g = g.cut(sil(p["d_yuva_pim"] / 2, p["boss_h"], V(s * r_yuva0, y_t, 0), u))
        for dz in (-5.0, 5.0):        # kapak vidalari (M2, isil insert)
            if abs(dz) < p["boss_d"] / 2:
                pass
        # servo yatagi (tetigin ONUNDE, M2)
        pad = kutu(-p["pad_t"] / 2, p["pad_t"] / 2, -p["pad_l"] / 2, p["pad_l"] / 2,
                   -p["pad_w"] / 2, p["pad_w"] / 2)
        pad.translate(V(s * (Ro + 1.0), y_t + p["pad_ofset"], 0))
        g = g.fuse(pad)
        # MIKRO SERVO baglanti delikleri: 28 mm aralik (+-14), OVAL.
        # Oval olmasi marka farkini (26-30 mm) tolere eder.
        for dy in (-p["servo_delik"], p["servo_delik"]):
            yk = y_t + p["pad_ofset"] + dy
            for ds in (-p["servo_slot"] / 2, p["servo_slot"] / 2):
                g = g.cut(sil(p["d_M2"] / 2, 10, V(s * (Ro - 3), yk + ds, 0), u))
            g = g.cut(kutu(s * (Ro - 3) - 0.1, s * (Ro - 3) + 10 * s,
                           yk - p["servo_slot"] / 2, yk + p["servo_slot"] / 2,
                           -p["d_M2"] / 2, p["d_M2"] / 2) if s > 0 else
                      kutu(s * (Ro - 3) + 10 * s, s * (Ro - 3) + 0.1,
                           yk - p["servo_slot"] / 2, yk + p["servo_slot"] / 2,
                           -p["d_M2"] / 2, p["d_M2"] / 2))
    # gobek ust yuzunde kapak icin 2x M2 delik (Z yonunde kaydirilmis)
    for s in (+1, -1):
        for dz in (-6.0, 6.0):
            g = g.cut(sil(p["d_M2"] / 2, 6, V(s * (Ro + p["boss_h"] - 5), y_t, dz),
                          V(s, 0, 0)))
    return g.removeSplitter()


def namlu_bol(p):
    """Namluyu IKI BASILABILIR PARCAYA boler.

    NEDEN: agiz basligi (bilezik + bant kulaklari, O104 mm) tek parca
    basimda ya tablada oturur (govdeyi ters cevirir) ya da HAVADA kalip
    destek ister. Ayirinca her parca kendi dogal yonunde basilir:
      * GOVDE : dik, dairesel kesit, sadece tetik gobekleri destek ister
      * BASLIK: flans yuzu tablada DUZ yatar -> SIFIR destek

    YUK YOLU: bantlar basligin kulaklarina baglanir ve kapsulu ILERI
    ceker; tepkisi basligi GERIYE, yani govdeye BASTIRIR. Yani ek
    BASMA yuku tasir -- omuz yeter, vida yalnizca bant gevsekken
    basligin dusmesini onler.
    """
    g = namlu(p)
    yb = p["y_bol"]; ts = p["t_spigot"]; rs = Ro - p["spigot_derin"]
    # --- GOVDE: yb+ts'ye kadar; son ts mm'de cap kuculur (spigot)
    gov = g.common(kutu(-80, 80, -2, yb + ts, -80, 80))
    # DIKKAT: kulaklar R=52'ye uzanir; halkayi Ro+1'e kadar kesersen
    # kulaklar GOVDEDE KALIR ve baslikla CAKISIR. 80 mm'ye kadar kes.
    halka = sil(80.0, ts, V(0, yb, 0), V(0, 1, 0)).cut(
            sil(rs, ts + 2, V(0, yb - 1, 0), V(0, 1, 0)))
    gov = gov.cut(halka)
    # --- BASLIK: yb'den uca; spigotun girecegi yuva acilir
    bas = g.common(kutu(-80, 80, yb, p["L_namlu"] + 2, -80, 80))
    bas = bas.cut(sil(rs + p["spigot_bosluk"], ts + 0.2, V(0, yb - 0.1, 0), V(0, 1, 0)))
    # --- 3 x M3 radyal tutma vidasi (bant gevsekken baslik dusmesin)
    ym = yb + ts * 0.55
    for k in range(3):
        a = k * 2 * math.pi / 3 + math.pi / 6      # yariklardan kacin
        u = V(math.cos(a), 0, math.sin(a))
        bas = bas.cut(sil(1.6, 20, V(-18 * math.cos(a), ym, -18 * math.sin(a)), u))
        gov = gov.cut(sil(1.3, 20, V(-18 * math.cos(a), ym, -18 * math.sin(a)), u))
    return gov, bas


def tetik_kapaklari(p):
    """Gobek ustune vidalanan kapak: ortada ip deligi, 2x M2 delik."""
    y_t = p["y_tetik"]; r0 = Ro + p["boss_h"]
    out = []
    for s in (+1, -1):
        u = V(s, 0, 0)
        k = sil(p["boss_d"] / 2, p["kapak_t"], V(s * r0, y_t, 0), u)
        k = k.cut(sil(p["d_ip"] / 2, p["kapak_t"] + 2, V(s * (r0 - 1), y_t, 0), u))
        for dz in (-6.0, 6.0):
            k = k.cut(sil(1.1, p["kapak_t"] + 2, V(s * (r0 - 1), y_t, dz), u))
        out.append(k)
    return out


def tamponlar(p):
    """Yarik on ucundaki TPU durdurma tamponlari."""
    w = p["yarik_w"] / 2
    y1 = p["y_capraz1"] + p["d_capraz"] / 2
    out = []
    for s in (+1, -1):
        z0, z1 = (Rb - 0.5, Ro + 0.5) if s > 0 else (-(Ro + 0.5), -(Rb - 0.5))
        out.append(kutu(-w + 0.1, w - 0.1, y1, y1 + p["tampon"], z0, z1))
    return out


def kapsul(p, y0):
    Rk = Rb - p["bosluk"] / 2; Rh = Rk - p["t_govde"]
    L = p["L_kapsul"]; a = math.radians(p["ALFA"])
    g = sil(Rk, L, V(0, 0, 0), V(0, 1, 0))
    g = g.cut(sil(Rh, p["L_hazne"], V(0, p["t_arka_blok"], 0), V(0, 1, 0)))
    g = g.cut(sil(Rk + 4, p["kanal_w"], V(0, p["kanal_y0"], 0), V(0, 1, 0)).cut(
        sil(Rk - p["kanal_d"], p["kanal_w"] + 2, V(0, p["kanal_y0"] - 1, 0), V(0, 1, 0))))
    g = g.cut(sil(p["d_capraz"] / 2 + 0.05, 2 * Rk + 4, V(0, p["y_capraz"], -(Rk + 2)),
                  V(0, 0, 1)))
    for i in range(6):
        th = math.radians(60 * i)
        ur = V(math.cos(th), 0, math.sin(th))
        eks = V(ur.x * math.sin(a), math.cos(a), ur.z * math.sin(a))
        taban = V(ur.x * p["R_pitch"], L, ur.z * p["R_pitch"]) - eks * p["derinlik"]
        g = g.cut(Part.makeSphere(p["D_yuva"] / 2, taban).fuse(
            sil(p["D_yuva"] / 2, p["derinlik"] + 8, taban, eks)))
    # ag cikis agzi: bilye yuvalarinin icinden, kenari pahli (ag takilmasin)
    g = g.cut(Part.makeCone(Rh * 0.60, Rh * 0.72, p["t_kapak"] + 0.2,
                            V(0, L - p["t_kapak"] - 0.1, 0), V(0, 1, 0)))
    g = g.removeSplitter(); g.translate(V(0, y0, 0))
    return g


def bilyeler(p, y0):
    a = math.radians(p["ALFA"]); L = p["L_kapsul"]; s = None
    for i in range(6):
        th = math.radians(60 * i)
        ur = V(math.cos(th), 0, math.sin(th))
        eks = V(ur.x * math.sin(a), math.cos(a), ur.z * math.sin(a))
        c = V(ur.x * p["R_pitch"], y0 + L, ur.z * p["R_pitch"]) - eks * p["derinlik"]
        k = Part.makeSphere(p["D_bilye"] / 2, c)
        s = k if s is None else s.fuse(k)
    return s


def capraz_pim(p):
    """O8 pim; her ucta IKI bant olugu (kenar basina 2 bant)."""
    y = p["y_capraz0"]; h = p["capraz_uzun"]
    c = sil(p["d_capraz"] / 2, h, V(0, y, -h / 2), V(0, 0, 1))
    for s in (+1, -1):
        for zc in (s * p["r_bant"], s * (p["r_bant"] + p["dz_bant"])):
            c = c.cut(sil(p["d_capraz"] / 2 + 1, 2.4, V(0, y, zc - 1.2), V(0, 0, 1)).cut(
                sil(p["d_capraz"] / 2 - 1.0, 3.4, V(0, y, zc - 1.7), V(0, 0, 1))))
    return c


def bantlar(p):
    """4 bant: her kenarda 2 adet (z = +/-r_bant ve +/-(r_bant+dz))."""
    d = p["bant_OD"] / math.sqrt(p["lam"])
    y0 = p["y_capraz0"] + 10.0; y1 = p["y_ankraj"] - 10.0
    out = []
    for s in (+1, -1):
        for zc in (s * p["r_bant"], s * (p["r_bant"] + p["dz_bant"])):
            out.append(sil(d / 2, y1 - y0, V(0, y0, zc), V(0, 1, 0)))
    return out


def tetik_pimleri(p):
    """O5 celik pim + O5 mil bilezigi (O10x5). Ust ucta O1.5 ip deligi.
    Dinlenmede: uc r=16.85, bilezik r=29-34, pim tepesi r=37.5.
    6 mm cekildiginde tepe r=43.5 < kapak ic yuzu 44.2 -> kapaga CARPMAZ;
    arada yay (blok boyu ~3.5 mm) icin 44.2-40 = 4.2 mm kalir."""
    y = p["y_tetik"]; r_uc = Rb - p["kanal_d"] + 0.15
    r_yaka, r_tepe = 29.0, 37.5
    out = []
    for s in (+1, -1):
        u = V(s, 0, 0)
        g = sil(p["d_pim"] / 2 - 0.05, r_tepe - r_uc, V(s * r_uc, y, 0), u)
        g = g.fuse(sil(5.0, 5.0, V(s * r_yaka, y, 0), u))
        g = g.cut(sil(0.75, 12, V(s * (r_tepe - 1.0), y, -6), V(0, 0, 1)))  # ip deligi
        out.append(g)
    return out


if __name__ == "__main__":
    yk = P["arka"]
    k1, k2 = tetik_kapaklari(P); t1, t2 = tetik_pimleri(P)
    tp1, tp2 = tamponlar(P); bs = bantlar(P)
    parcalar = {"V4_namlu": namlu(P), "V4_kapsul": kapsul(P, yk),
                "V4_bilye": bilyeler(P, yk), "V4_capraz_pim": capraz_pim(P),
                "V4_bant_1": bs[0], "V4_bant_2": bs[1],
                "V4_bant_3": bs[2], "V4_bant_4": bs[3],
                "V4_pim_sag": t1, "V4_pim_sol": t2,
                "V4_kapak_sag": k1, "V4_kapak_sol": k2,
                "V4_tampon_ust": tp1, "V4_tampon_alt": tp2}
    tum = None
    for ad, sh in parcalar.items():
        sh.exportBrep(os.path.join(OUT, ad + ".brep"))
        sh.exportStep(os.path.join(OUT, ad + ".step"))
        print(f"{ad:15s} hacim={sh.Volume/1000:8.2f} cm3 gecerli={sh.isValid()}")
        tum = sh if tum is None else tum.fuse(sh)
    Part.Shape(tum).exportStep(os.path.join(OUT, "V4_MONTAJ.step"))
    json.dump({k: v for k, v in P.items() if isinstance(v, (int, float))},
              open(os.path.join(OUT, "v4_olcu.json"), "w"), indent=1)
    print(f"V4 | namlu {P['L_namlu']:.1f} mm, strok {P['STROK']:.0f}, kapsul "
          f"{P['L_kapsul']:.1f}, L0 {P['L0']:.1f}, ankraj y={P['y_ankraj']:.1f}, "
          f"durmus agiz y={P['y_yuz_dur']:.1f}")
