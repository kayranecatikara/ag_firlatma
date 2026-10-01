"""Faz-3: Tasarim Uzayi Kesfi (Design Space Exploration).

Tasarim vektoru -> tutarli geometri -> ic balistik -> ag ucusu -> metrikler.
Tum geometrik/mekanik bagimliliklar burada zorlanir, boylece Sobol/optimize
adimlari HER ZAMAN imal edilebilir tasarimlar uretir.
"""
import numpy as np
from scipy.stats import qmc
from .params import Tasarim, BILYE_MALZEME
from .launcher import firlat, yay_ozet
from .pneumatic import firlat_pnomatik
from .netrom import uc
from .engagement import etkin_menzil, degerlendir

BILYE_SET = ["Celik", "Pirinc", "Kursun", "Tungsten"]
IPLIK_SET = ["Dyneema_SK78", "Kevlar_29"]

# ad, alt, ust
DEGISKENLER = [
    ("D_bore",     0.039, 0.070),   # namlu ic capi [m]
    ("L_namlu",    0.118, 0.400),   # namlu boyu [m]
    ("d_tel",     0.0020, 0.0055),  # yay tel capi [m]
    ("C_yay",        5.0, 10.0),    # yay indeksi D/d
    ("n_aktif",      6.0, 32.0),    # aktif sarim
    ("strok_or",    0.20, 0.80),    # strok / kullanilabilir boy
    ("D_bilye",    0.007, 0.022),   # bilye capi [m]
    ("mlz_bilye",    0.0, 3.999),   # kategorik indeks
    ("alpha_deg",    0.0, 40.0),    # konik cep acisi
    ("twist_inv",    0.0, 20.0),    # 1/yiv_adimi [1/m]; <0.5 -> duz yiv
    ("R_ag",        0.40, 1.50),    # ag yaricapi [m]
    ("goz",        0.030, 0.120),   # goz araligi [m]
    ("d_iplik",  0.00015, 0.00080), # iplik capi [m]
]
ALT = np.array([d[1] for d in DEGISKENLER])
UST = np.array([d[2] for d in DEGISKENLER])
ADLAR = [d[0] for d in DEGISKENLER]

RHO_KAPSUL = 700.0     # baskili PETG, dolgulu efektif yogunluk [kg/m^3]
DUVAR = 0.5e-3


def vektor_to_tasarim(x):
    """Tasarim vektorunu tutarli bir Tasarim nesnesine cevirir.
    Donus: (Tasarim, uygun_mu, sebep)"""
    (D_bore, L_namlu, d_tel, C_yay, n_aktif, strok_or,
     D_bilye, mlz_i, alpha_deg, twist_inv, R_ag, goz, d_iplik) = x

    t = Tasarim()
    t.namlu.D_bore = D_bore
    t.namlu.L_namlu = L_namlu
    t.namlu.twist_L = (1.0/twist_inv) if twist_inv > 0.5 else 0.0
    t.bilye.D = D_bilye
    t.bilye.malzeme = BILYE_SET[int(mlz_i)]
    t.kapsul.alpha_cep = np.radians(alpha_deg)
    t.ag.R_ag, t.ag.goz, t.ag.d_iplik = R_ag, goz, d_iplik

    # --- geometri: 6 bilye bolme cemberine sigmali
    R_pitch = 0.5*D_bore - 0.5*D_bilye - DUVAR
    if R_pitch < D_bilye:                       # komsu bilyeler cakisir
        return None, False, "bilyeler namluya sigmiyor"
    t.kapsul.R_pitch = R_pitch

    # --- ag haznesi: paketlenmis agi almali
    D_hazne = D_bore - 3e-3
    V_ger = t.ag.V_paket/t.kapsul.paket_dol
    L_hazne = V_ger/(np.pi*0.25*D_hazne**2)
    L_kapsul = L_hazne + 12e-3                  # on kapak (bilye yuvalari) + arka
    t.kapsul.D_hazne, t.kapsul.L_hazne, t.kapsul.L_kapsul = D_hazne, L_hazne, L_kapsul

    # --- kapsul kutlesi (hacimden)
    V_mlz = (np.pi*0.25*(D_bore**2 - D_hazne**2)*L_kapsul
             + np.pi*0.25*D_bore**2*8e-3)
    t.kapsul.m_kapsul = RHO_KAPSUL*V_mlz

    # --- yay: namluya sigmali, strok kapsulden arta kalan boy
    L_kul = L_namlu - L_kapsul                  # yay icin kullanilabilir boy
    if L_kul <= 0.02:
        return None, False, "kapsul namluya sigmiyor"
    strok = strok_or*L_kul
    L_cocked = L_kul - strok
    L_solid = (n_aktif + 2.0)*d_tel
    if L_cocked < L_solid:
        return None, False, "yay blok boyu asiliyor"
    t.yay.d_tel, t.yay.D_orta = d_tel, C_yay*d_tel
    t.yay.n_aktif, t.yay.x0 = n_aktif, strok
    t.yay.L_serbest = L_cocked + strok
    if t.yay.D_orta + d_tel > D_bore - 1e-3:
        return None, False, "yay namluya sigmiyor"
    return t, True, ""


def degerlendir_vektor(x, F_sok_limit=2000.0, SF_kopma_min=2.0,
                       F_kurma_limit=300.0, t_acilma_limit=0.30,
                       menzil0=None, pnomatik=None):
    """Tam degerlendirme zinciri. Donus: metrik sozlugu."""
    kotu = dict(uygun=False, R_eff=0.0, kapsama=0.0, R_kesisme=0.0,
                E_depo=np.inf, J_geri=np.inf, m_sistem=np.inf, v_exit=0.0,
                v_radyal=0.0, t_acilma=np.nan, F_max=np.nan, F_sok=np.inf,
                kopma_SF=0.0, verim=0.0, m_ucan=0.0, m_kapsul=0.0, m_ag=0.0,
                L_kapsul=0.0, strok=0.0, SF_gerilme=0.0, sebep="")
    t, ok, sebep = vektor_to_tasarim(x)
    if not ok:
        kotu["sebep"] = sebep; return kotu
    if menzil0 is not None:
        t.ang.menzil0 = menzil0
    try:
        L = (firlat_pnomatik(t, *pnomatik) if pnomatik else firlat(t))
        if L.get("basarisiz"):
            kotu["sebep"] = "ic balistik basarisiz"; return kotu
        if not (L["ok_gerilme"] and L["ok_solid"]):
            kotu["sebep"] = "yay gerilme/blok"; return kotu
        F = uc(t, L)
        R_ger = 0.5*t.ang.hedef_kanat
        R_eff = etkin_menzil(F, R_ger)
        E = degerlendir(t, F)
    except Exception as e:
        kotu["sebep"] = f"hata: {e}"; return kotu

    # sistem kutlesi: namlu + yay + kapsul + ucan
    V_namlu = np.pi*0.25*((t.namlu.D_bore+8e-3)**2 - t.namlu.D_bore**2)*t.namlu.L_namlu
    m_namlu = RHO_KAPSUL*V_namlu
    m_sis = m_namlu + L["m_yay"] + t.kapsul.m_kapsul + t.m_ucan

    # --- KRITIK: agin HEDEFE VARDIGINDA acik olmasi gerekir, "bir ara" degil.
    # R_eff tek basina yaniltici bir amactir: cok yavas acilan bir ag, paket
    # halinde cok uzaga gider ve R_eff'i buyuk gosterir; oysa her gercekci
    # tetikleme mesafesinde hala kapalidir. Monte Carlo bunu %0 yakalama
    # olarak ortaya cikarir. Dogru amac KESISME ANINDAKI kapsamadir.
    tahkik = {
        "yay":      bool(L["ok_gerilme"] and L["ok_solid"] and L["ok_namlu"]),
        "kopma":    bool(F["kopma_SF"] >= SF_kopma_min),
        "goz":      bool(t.ag.goz <= 0.5*t.ang.hedef_boy),
        "sok":      bool(L["F_sok"] <= F_sok_limit),
        # kurma kuvveti yalnizca YAY icin anlamli (pnomatikte NaN)
        "kurma":    bool(not np.isfinite(L["F_max"]) or L["F_max"] <= F_kurma_limit),
        "acilma":   bool(np.isfinite(F["t_acilma"]) and F["t_acilma"] <= t_acilma_limit),
        "kesisme":  bool(E["kesisme"] and R_eff > 0.0),
    }
    uygun = all(tahkik.values())
    if not uygun:
        kotu["sebog"] = ""
        kotu["sebep"] = "+".join(k for k, v in tahkik.items() if not v)
        kotu["tahkik"] = tahkik
        return kotu
    return dict(uygun=True, tahkik=tahkik, R_eff=R_eff,
                kapsama=E["ort_kapsama"], R_kesisme=E["R_kesisme"],
                t_acilma=F["t_acilma"], E_depo=L["E_depo"],
                J_geri=L["J_geri"], m_sistem=m_sis, v_exit=L["v_exit"],
                v_radyal=L["v_radyal"], F_sok=L["F_sok"], F_max=L["F_max"],
                verim=L["verim"], kopma_SF=F["kopma_SF"],
                m_ucan=t.m_ucan, m_kapsul=t.kapsul.m_kapsul, m_ag=t.ag.m_ag,
                L_kapsul=t.kapsul.L_kapsul, strok=L["strok"],
                SF_gerilme=L["SF_gerilme"], sebep="")


def sobol_ornekle(n_log2=12, seed=0):
    s = qmc.Sobol(d=len(DEGISKENLER), scramble=True, seed=seed)
    return qmc.scale(s.random_base2(n_log2), ALT, UST)


def pareto_front(F, yonler):
    """Baskin olmayan noktalarin maskesi. yonler: +1 maksimize, -1 minimize."""
    Z = F*np.asarray(yonler)          # hepsi maksimize
    n = len(Z); maske = np.ones(n, bool)
    for i in range(n):
        if not maske[i]:
            continue
        baskin = np.all(Z >= Z[i], axis=1) & np.any(Z > Z[i], axis=1)
        if baskin.any():
            maske[i] = False
    return maske
