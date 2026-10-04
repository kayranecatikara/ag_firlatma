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
    derinlik=4.2, n_boncuk=3,
    t_yuva=1.4,            # boncuk yuvasi boru cidari
    t_ara=0.8,             # merkezi gecis ile boru arasi cidar
    h_takoz=12.0,          # durdurma takozunun radyal yuksekligi
    w_takoz=5.0,           # takozun yarik disina tasmasi (her yan)
    L_takoz=16.0,          # takozun eksenel boyu
    t_pad=5.0,             # takoz arkasindaki TPU pad cebi
    t_pim_tavan=2.0,       # capraz pim deliginin ustunde birakilan malzeme
    lip_dar=0.8,           # agizdaki daralma (boncugu tutan dudak)
    lip_boy=1.2,           # dudagin boyu
    d_ip_delik=3.0,        # yuva tabanindan hazneye ip deligi
    R_pitch_hazneli=13.4,  # 02b varyanti: bolum dairesi en disa itildi
    h_hazne_koni=12.0,     # hazne -> baslik koni boyu
    # DURDURMA OMUZU (geri geldi): kapsulun halka kenari namlu agzindaki
    # ice cikintiya oturur. Capraz pimin yarik ucuna carpmasindan 4.6x
    # daha genis temas alani. Boncuk cemberi kuculmeden ANLAMSIZDIR.
    omuz_bosluk=1.0,   # boncuk ile koni arasinda istenen NET aciklik
    t_omuz=2.5,        # omuza yapistirilan TPU halkanin kalinligi
    # kapsul: arka blok (capraz pim) + tutma kanali + hazne + on kapak
    y_capraz=4.5, d_capraz=6.0, capraz_uzun=78.0,
    kanal_y0=9.0, kanal_w=5.4, kanal_d=5.0, t_arka_blok=16.0, t_kapak=8.0,
    t_govde=3.0,
    yarik_w=9.4, tampon=3.0, r_bant=33.0, dz_bant=11.0,
    kulak_R=42.0, bilezik_R=32.0, bilezik_L=14.0, d_ankraj=6.5,
    # BANT ANKRAJI: bant deligin icinden gecer, tasiyici pim banti DELER.
    # Dyneema halka YOK. Bilezik y_ankraj'da biter -> pim tam tasarim
    # noktasina oturur, boylece L0/H/lam degismez.
    kulak_w=11.0,          # kulak yari kalinligi (X) — O14 delige 4 mm cidar
    d_bant_delik=14.0,     # banttan 1 mm buyuk gecis deligi
    d_pim_ankraj=4.0,      # banti DELEN enine tutma pimi (celik)
    pim_bosluk=0.2,        # pim deligi = pim + bu
    pim_geri=6.0,          # pim ekseni, bilezik on yuzunden bu kadar geride
    bilezik_geri=16.0,     # bilezigin y_ankraj'dan geriye uzanimi
    n_ankraj_yan=1,        # kenar basina bant (O13 ile 1 tane sigar)
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
    # DURDURMA OMUZU: delik sadece omuz duzlemine kadar acilir; otesini
    # iraksak koni acar. Aradaki basamak kapsulu durduran yuzeydir.
    # Koni, TPU kalinligi kadar GERIDEN basliyor; bu kayma aciklikan
    # erir. O yuzden kalinlik x tan(ALFA) kadar fazladan eklenir.
    # OMUZ YOK: boncuklar kapsulun en kenarinda (R22) oldugu icin koni
    # R29.1'den baslamak zorunda; kapsul yaricapi 27.1 -> omuza yer kalmiyor.
    # Kapsulu CAPRAZ PIM + namlu disindaki DURDURMA TAKOZU durdurur.
    R_omuz = Rb
    y_om = p["y_yuz_dur"]
    g = sil(Ro, L, V(0, 0, 0), V(0, 1, 0)).cut(
        sil(Rb, L + 4, V(0, -2, 0), V(0, 1, 0)))
    # iraksak koni: durmus kapsul agzindan namlu agzina (bilye yolundan genis)
    yk = p["y_yuz_dur"]; Lk = L - yk
    R2 = Rb + Lk * math.tan(math.radians(p["koni_acisi"]))
    # agiz bilezigi + bant kulaklari: SADECE on ucta (bant arkada namlu
    # borusunun ustunden gecer). Delik bilezik boyunca TAMAMEN acilir.
    ya = p["y_ankraj"]
    kw = p["kulak_w"]
    y0 = ya - p["bilezik_geri"]; y1 = ya        # bilezik ANKRAJDA biter
    bil = sil(p["bilezik_R"], y1 - y0, V(0, y0, 0), V(0, 1, 0))
    for s in (+1, -1):
        z0, z1 = (Ro - 1, p["kulak_R"]) if s > 0 else (-p["kulak_R"], -(Ro - 1))
        bil = bil.fuse(kutu(-kw, kw, y0, y1, z0, z1))
    bil = bil.cut(sil(Rb, y1 - y0 + 2, V(0, y0 - 1, 0), V(0, 1, 0)))
    db = p["d_bant_delik"]
    dp = p["d_pim_ankraj"] + p["pim_bosluk"]      # enine tutma pimi deligi
    y_pim = y1 - p["pim_geri"]                    # on yuzden geride
    for s in (+1, -1):
        for i in range(int(p["n_ankraj_yan"])):
            zc = s * (p["r_bant"] + i * p["dz_bant"])
            # bant gecis deligi (Y ekseninde, bilezigi bastan sona deler)
            bil = bil.cut(sil(db / 2, y1 - y0 + 6, V(0, y0 - 3, zc), V(0, 1, 0)))
            # arka agizda pah: gergin bant kenarda kesilmesin
            bil = bil.cut(Part.makeCone(db / 2 + 2.5, db / 2, 2.5,
                                        V(0, y0 - 0.1, zc), V(0, 1, 0)))
            # ENINE TUTMA PIMI: kulagin bir yan duvarindan girer, bandi
            # deler, karsi duvardaki delige oturur. Pim X ekseninde.
            bil = bil.cut(sil(dp / 2, 2 * kw + 6, V(-(kw + 3), y_pim, zc),
                              V(1, 0, 0)))
    g = g.fuse(bil)
    # iraksak koni: OMUZ YARICAPINDAN baslar, bilezik dahil her seyi keser
    Lk2 = L - y_om
    R2b = R_omuz + Lk2 * math.tan(math.radians(p["koni_acisi"]))
    g = g.cut(Part.makeCone(R_omuz, R2b, Lk2 + 0.5, V(0, y_om, 0), V(0, 1, 0)))
    # DURDURMA TAKOZU: omuz olmadigi icin kapsulu CAPRAZ PIM durdurur.
    # Yarik sonundaki yatak alanini radyal olarak derinlestirir:
    # pim O8 x (R_takoz - Rb+1) x 2 kenar.
    y_dur = p["y_capraz1"] + p["d_capraz"] / 2          # pimin on yuzu
    R_tak = Ro + p["h_takoz"]
    wt = p["yarik_w"] / 2 + p["w_takoz"]
    for s2 in (+1, -1):
        z0, z1 = (Ro - 1, R_tak) if s2 > 0 else (-R_tak, -(Ro - 1))
        g = g.fuse(kutu(-wt, wt, y_dur, y_dur + p["L_takoz"], z0, z1))
    # takozun arka yuzunde TPU pad cebi
    for s2 in (+1, -1):
        z0, z1 = (Ro - 1, R_tak + 1) if s2 > 0 else (-(R_tak + 1), -(Ro - 1))
        g = g.cut(kutu(-p["yarik_w"] / 2, p["yarik_w"] / 2,
                       y_dur, y_dur + p["t_pad"], z0, z1))

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


def takoz_padi(p):
    """Durdurma takozunun arka yuzundeki TPU ped. Kapsulu durduran capraz
    pim once buna carpar; PETG takoz yedektir. Gorevi enerjiyi yutmak
    degil, DURMAYI UZATIP kuvvet tepesini dusurmektir (F = E/d)."""
    y = p["y_capraz1"] + p["d_capraz"] / 2
    R_tak = Ro + p["h_takoz"]
    w = p["yarik_w"] / 2 - 0.15
    out = []
    for s2 in (+1, -1):
        z0, z1 = (Ro - 0.9, R_tak + 0.9) if s2 > 0 else (-(R_tak + 0.9), -(Ro - 0.9))
        out.append(kutu(-w, w, y + 0.1, y + p["t_pad"], z0, z1))
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
    """KAPSUL — v1.3.

    Ilk baskidan gelen uc duzeltme:
      1. Yuva dipleri ACIKTI: ag cikis konisi yuvalarin tabanini yiyordu,
         boncuklar hazneye dusuyordu. Artik her yuvanin etrafina BORU
         fuzelenip tabani KAPATILIYOR; sadece O3 ip deligi kaliyor.
      2. Boncugu tutan dudak: yuva agzinda hafif daralma (D_yuva - lip_dar).
         Elde dururken boncuk dusmez; atista 4 g x ~50000 g atalet kuvveti
         (~2000 N) dudagi kolayca gecer.
      3. Ag KAPSULDEN CIKMIYOR: namluda, kapsulun onunde duruyor.
         Baslik masif; ic bosluk sadece agirlik icin ve KONI
         (agiz yukari basimda tavan yok, destek gerekmiyor).
    """
    Rk = Rb - p["bosluk"] / 2; Rh = Rk - p["t_govde"]
    L = p["L_kapsul"]; a = math.radians(p["ALFA"])
    t_k = p["t_kapak"]; y_kap = L - t_k            # baslik dibi

    g = sil(Rk, L, V(0, 0, 0), V(0, 1, 0))
    # --- IC BOSLUK (agirlik azaltma) ---
    # AG ARTIK KAPSULUN ICINDE DEGIL. 6 boncuk borusu agzi neredeyse tamamen
    # kapatiyordu: merkezde sadece 55 mm2 (O8.3) kaliyordu ve 39 m ip oradan
    # gecemez. Omuz >=250 mm2 isterken R_pitch <= 12.26 olmak zorunda, o
    # durumda bile merkez 62 mm2 -- yani DURDURMA OMZU ile MERKEZI AG CIKISI
    # ayni anda mumkun degil. Ag namluya, kapsulun ONUNE yerlestiriliyor;
    # kapsul pistondur. Boylece baslik MASIF kalabiliyor.
    # Bosluk KONI: agiz yukari basimda tavan yok, kendini tasir.
    y_sil = p["t_arka_blok"]
    g = g.cut(Part.makeCone(Rh, 0.0, y_kap - y_sil, V(0, y_sil, 0), V(0, 1, 0)))
    # --- tutma kanali + capraz pim deligi ---
    g = g.cut(sil(Rk + 4, p["kanal_w"], V(0, p["kanal_y0"], 0), V(0, 1, 0)).cut(
        sil(Rk - p["kanal_d"], p["kanal_w"] + 2, V(0, p["kanal_y0"] - 1, 0), V(0, 1, 0))))
    g = g.cut(sil(p["d_capraz"] / 2 + 0.05, 2 * Rk + 4, V(0, p["y_capraz"], -(Rk + 2)),
                  V(0, 0, 1)))

    # --- 6 BONCUK YUVASI: once BORU fuzele, sonra ic bosalt ---
    rp, dy, der = p["R_pitch"], p["D_yuva"], p["derinlik"]
    r_boru = dy / 2 + p["t_yuva"]
    for i in range(6):
        th = math.radians(60 * i)
        ur = V(math.cos(th), 0, math.sin(th))
        eks = V(ur.x * math.sin(a), math.cos(a), ur.z * math.sin(a))
        agiz = V(ur.x * rp, L, ur.z * rp)
        taban = agiz - eks * der
        # boru: tabandan agza; dis yuzu hazne cidarina degip birlesir
        g = g.fuse(sil(r_boru, der + p["t_yuva"] + 2,
                       taban - eks * p["t_yuva"], eks))
    g = g.cut(sil(Rk, 20, V(0, L, 0), V(0, 1, 0)))      # agzi duzelt
    for i in range(6):
        th = math.radians(60 * i)
        ur = V(math.cos(th), 0, math.sin(th))
        eks = V(ur.x * math.sin(a), math.cos(a), ur.z * math.sin(a))
        agiz = V(ur.x * rp, L, ur.z * rp)
        taban = agiz - eks * der
        # yuva bosluğu: DUZ tabanli silindir. Kure oturak boru cidarini
        # delip tabani aciyordu (ilk baskida boncuklar hazneye dusuyordu).
        lip = p["lip_boy"]
        g = g.cut(sil(dy / 2, der - lip, taban, eks))
        # TUTMA DUDAGI: agizda daralmis kisa delik
        g = g.cut(sil((dy - p["lip_dar"]) / 2, lip + 2, agiz - eks * lip, eks))
        # ip deligi: tabandan hazneye
        g = g.cut(sil(p["d_ip_delik"] / 2, der + 14, taban, -eks))
    g = g.removeSplitter(); g.translate(V(0, y0, 0))
    return g


def kapsul_hazneli(p, y0):
    """KAPSUL v2.1 — boncuklar KENARDA, merkez TAMAMEN ACIK.

    v2.0'da yuvalar R18.2'deydi ve 40 derece egimden oturu agiz duzleminde
    elips kesit verip ustu kapatiyordu; merkezde aga 271 mm2 kaliyordu.
    Burada yuvalar kapsulun EN KENARINA (R22.0) alindi:

      * yuva dis kenari 30.1 > kapsul 27.1 -> yuva cidari delip disa
        **6.0 mm genisliginde radyal yarik** aciyor. Boncuk O8.8 oldugu
        icin o yariktan CIKAMAZ: plastik boncugu sariyor, namlu deligi de
        disaridan kapatiyor. Ayri bir tutma dudagina gerek yok.
      * merkezde aga **523 mm2 (O25.8)** kaliyor — v2.0'in 1.9 kati.

    Kapsulu artik omuz degil CAPRAZ PIM durdurur (koni R29.1'den baslamak
    zorunda, kapsul yaricapi 27.1 — omuza yer yok). Namluda dis durdurma
    takozu var.
    """
    Rk = Rb - p["bosluk"] / 2; Rh = Rk - p["t_govde"]
    L = p["L_kapsul"]; a = math.radians(p["ALFA"])
    rp = p["R_pitch_hazneli"]
    dy, der = p["D_yuva"], p["derinlik"]
    yari = (dy / 2 + p["t_yuva"]) / math.cos(a)
    r_cap = rp - yari - p["t_ara"]                  # merkezi ag gecisi
    h_koni = p["h_hazne_koni"]

    g = sil(Rk, L, V(0, 0, 0), V(0, 1, 0))
    y_sil = p["t_arka_blok"]; y_kon = L - h_koni
    # ARKA BLOK HAFIFLETME: ic bosluk capraz pimin hemen ustunden baslar.
    # Masif 16 mm disk kapsulun 38/54 g'ini olusturuyordu. Koni biciminde
    # (agiz yukari basimda tavan yok) ve capraz pim deliginin ustunde
    # t_pim_tavan kadar malzeme birakir.
    y_bos = p["y_capraz"] + p["d_capraz"] / 2 + p["t_pim_tavan"]
    r_bos = Rh - (y_sil - y_bos) * math.tan(math.radians(45.0))
    if y_bos < y_sil and r_bos > 2.0:
        g = g.cut(Part.makeCone(r_bos, Rh, y_sil - y_bos, V(0, y_bos, 0), V(0, 1, 0)))
    g = g.cut(sil(Rh, y_kon - y_sil, V(0, y_sil, 0), V(0, 1, 0)))
    # hazne -> agiz: basamaksiz koni, agizda r_cap'e acilir (ag buradan cikar)
    g = g.cut(Part.makeCone(Rh, r_cap, h_koni, V(0, y_kon, 0), V(0, 1, 0))
              if Rh > r_cap else
              Part.makeCone(r_cap, Rh, h_koni, V(0, y_kon, 0), V(0, 1, 0)))
    g = g.cut(sil(r_cap, 3.0, V(0, L - 1.5, 0), V(0, 1, 0)))
    g = g.cut(sil(Rk + 4, p["kanal_w"], V(0, p["kanal_y0"], 0), V(0, 1, 0)).cut(
        sil(Rk - p["kanal_d"], p["kanal_w"] + 2, V(0, p["kanal_y0"] - 1, 0), V(0, 1, 0))))
    g = g.cut(sil(p["d_capraz"] / 2 + 0.05, 2 * Rk + 4, V(0, p["y_capraz"], -(Rk + 2)),
                  V(0, 0, 1)))

    for i in range(6):
        th = math.radians(60 * i)
        ur = V(math.cos(th), 0, math.sin(th))
        eks = V(ur.x * math.sin(a), math.cos(a), ur.z * math.sin(a))
        agiz = V(ur.x * rp, L, ur.z * rp)
        taban = agiz - eks * der
        # yuva: duz tabanli silindir; disa tasan kismi cidari delip yarik acar
        g = g.cut(sil(dy / 2, der + 6, taban, eks))
        # ip deligi (tabandan hazneye)
        g = g.cut(sil(p["d_ip_delik"] / 2, der + 14, taban, -eks))
    g = g.cut(sil(Rk, 20, V(0, L, 0), V(0, 1, 0)))     # agzi duzelt
    g = g.removeSplitter(); g.translate(V(0, y0, 0))
    return g


def bilyeler(p, y0):
    """18 x O9 boncuk: yuva basina 3 tane, HEPSI AYNI IPE dizili.
    Oncu boncuk egik yuvada; arkadaki 2 tanesi hazne icinde ayni eksende.
    Captain 1216: O9 kursun, ortasinda ~O2 gecme deligi -> 4.0 g."""
    a = math.radians(p["ALFA"]); L = p["L_kapsul"]; s = None
    Db = p["D_bilye"]; d_delik = 2.0
    for i in range(6):
        th = math.radians(60 * i)
        ur = V(math.cos(th), 0, math.sin(th))
        eks = V(ur.x * math.sin(a), math.cos(a), ur.z * math.sin(a))
        # oncu boncugun merkezi: yuva dibinden yarim boncuk iceri
        c0 = V(ur.x * p["R_pitch"], y0 + L, ur.z * p["R_pitch"]) - eks * (Db / 2)
        for j in range(int(p.get("n_boncuk", 3))):   # oncu + arkadakiler
            c = c0 - eks * (j * Db)
            k = Part.makeSphere(Db / 2, c).cut(
                sil(d_delik / 2, Db + 2, c - eks * (Db / 2 + 1), eks))
            s = k if s is None else s.fuse(k)
    return s


def capraz_pim(p):
    """O8 pim; her ucta IKI bant olugu (kenar basina 2 bant)."""
    y = p["y_capraz0"]; h = p["capraz_uzun"]
    c = sil(p["d_capraz"] / 2, h, V(0, y, -h / 2), V(0, 0, 1))
    w = p["d_bant_delik"]                      # bant O13 -> 14 mm genis oluk
    for s in (+1, -1):
        for i in range(int(p["n_ankraj_yan"])):
            zc = s * (p["r_bant"] + i * p["dz_bant"])
            c = c.cut(sil(p["d_capraz"] / 2 + 1, w, V(0, y, zc - w / 2), V(0, 0, 1)).cut(
                sil(p["d_capraz"] / 2 - 1.0, w + 2, V(0, y, zc - w / 2 - 1), V(0, 0, 1))))
    return c


def bantlar(p):
    """Bant gorselleri. ADET konfigdeki n_ankraj_yan'a UYAR: O13 bant ve
    O14 ankraj deligiyle kenar basina 1 bant siginca liste 2 elemanlidir.
    (Eski surum her zaman 4 uretiyordu; biri ankraji olmayan z=+47'ye
    dusuyordu.) Gergin bant kesiti incelir: d = OD/sqrt(lam)."""
    d = p["bant_OD"] / math.sqrt(p["lam"])
    y0 = p["y_capraz0"] + 10.0; y1 = p["y_ankraj"] - 10.0
    out = []
    for s in (+1, -1):
        for i in range(int(p["n_ankraj_yan"])):
            zc = s * (p["r_bant"] + i * p["dz_bant"])
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
                "V4_kapsul_hazneli": kapsul_hazneli(P, yk),
                "V4_bilye": bilyeler(P, yk), "V4_capraz_pim": capraz_pim(P),
                **{f"V4_bant_{i+1}": sh for i, sh in enumerate(bs)},
                "V4_pim_sag": t1, "V4_pim_sol": t2,
                "V4_kapak_sag": k1, "V4_kapak_sol": k2,
                "V4_tampon_ust": tp1, "V4_tampon_alt": tp2,
                **{f"V4_takoz_pad_{i+1}": sh for i, sh in enumerate(takoz_padi(P))}}
    tum = None
    hacim = {}
    for ad, sh in parcalar.items():
        sh.exportBrep(os.path.join(OUT, ad + ".brep"))
        sh.exportStep(os.path.join(OUT, ad + ".step"))
        bb = sh.BoundBox
        hacim[ad] = {"V": sh.Volume / 1000.0, "X": bb.XLength,
                     "Y": bb.YLength, "Z": bb.ZLength}
        print(f"{ad:15s} hacim={sh.Volume/1000:8.2f} cm3 gecerli={sh.isValid()}")
        tum = sh if tum is None else tum.fuse(sh)
    # v4_hacim.json: malzeme_listesi.py bunu okur. Daha once HICBIR betik
    # yazmiyordu -> BOM kutleleri eski CAD'den geliyordu.
    json.dump(hacim, open(os.path.join(OUT, "v4_hacim.json"), "w"), indent=1)
    Part.Shape(tum).exportStep(os.path.join(OUT, "V4_MONTAJ.step"))
    json.dump({k: v for k, v in P.items() if isinstance(v, (int, float))},
              open(os.path.join(OUT, "v4_olcu.json"), "w"), indent=1)
    print(f"V4 | namlu {P['L_namlu']:.1f} mm, strok {P['STROK']:.0f}, kapsul "
          f"{P['L_kapsul']:.1f}, L0 {P['L0']:.1f}, ankraj y={P['y_ankraj']:.1f}, "
          f"durmus agiz y={P['y_yuz_dur']:.1f}")
