"""IPLIGIN PERVANE TARAFINDAN KESILMESINE DIRENCI.

Ag ipi ince yapilirsa menzil uzar (surukleme ~ d, kutle ~ d^2). Ama ip
pervane tarafindan kesilirse yakalama basarisiz olur. UC AYRI mekanizma
vardir ve CAPA BAGIMLILIKLARI FARKLIDIR -- karistirilmamalidir:

  1) ENINE DARBE (Smith teorisi).  Pervane kanadi SERBEST ucan ipe carpar.
     Ip bir ornege (anvil) dayali DEGILDIR; sadece hizlanip savrulur.
     Kritik hiz YALNIZCA MALZEMEYE baglidir, capa DEGIL:
         c   = sqrt(E/rho)                (boyuna dalga hizi)
         V_c = c * sqrt(2*eb*sqrt(eb*(1+eb)) - eb^2)
     Balistik lif literaturunde tek-lif V50'sinin cap-bagimsiz olmasinin
     sebebi budur.

  2) KENAR UZERINDE KESME (ip sarildiktan SONRA).  Ip kanada/gobege sarilip
     gerilince, kanat kenari bir ORNEK gorevi gorur. Gerilim T altinda,
     kenar yaricapi r_e uzerinde, birim boydaki normal kuvvet T/r_e; temas
     genisligi ~d:
         p = T / (r_e * d)
     DIKKAT: p ~ 1/d  -> INCELTMEK BU MEKANIZMADA ZARARLIDIR (dogrusal).
     UHMWPE (Dyneema) enine dayanimi DUSUKTUR; aramid cok daha iyidir.

  3) CEKME KOPMASI.  F_kopma = sigma_u * pi/4 * d^2  ->  d^2 ile zayiflar
     (en hizli bozulan mekanizma).

Sonuc: inceltmenin sinirini (1) degil, (2) ve (3) koyar.
"""
import numpy as np
from .params import IPLIK_MALZEME

# UHMWPE/aramid enine (lif eksenine dik) basma dayanimi [Pa].
# Kuvvetli ANIZOTROPI: eksenel 3 GPa iken enine ~100 MPa mertebesindedir.
ENINE_DAYANIM = {"Dyneema_SK78": 100e6, "Kevlar_29": 250e6,
                 "Naylon_66": 90e6, "Polyester": 110e6}


# DUGUM VERIMI: agin gercek dayanimi LIF dayanimi degil, DUGUM dayanimidir.
# Altigen agda her dugumde bag vardir; her eleman bir dugumde sonlanir.
#   * dugumlu ag (sheet bend / dokumaci dugumu): UHMWPE kaygandir, agir kayip
#   * dugumsuz (raschel/orme) ag: kayip cok az -> TASARIM TERCIHI
DUGUM_VERIMI = {"Dyneema_SK78": 0.55, "Kevlar_29": 0.60,
                "Naylon_66": 0.65, "Polyester": 0.65}
DUGUMSUZ_VERIM = 0.90


def smith_kritik_hiz(malzeme):
    """Enine darbede kopma hizi [m/s] -- CAPTAN BAGIMSIZ."""
    m = IPLIK_MALZEME[malzeme]
    c = np.sqrt(m["E"] / m["rho"])
    eb = m["sigma_u"] / m["E"]
    return c * np.sqrt(2 * eb * np.sqrt(eb * (1 + eb)) - eb ** 2), c, eb


def egilme_gerinimi(d_filament, r_kenar):
    """Kanat kenarina sarilan LIFIN dis yuzey gerinimi.

    KRITIK AYRIM: ip MONOFILAMENT mi yoksa ORGU (coklu filament) mu?
      * monofilament d=0.165 mm, kenar yaricapi 0.35 mm ->
            eps = (d/2)/(r_e + d/2) = %19   >> Dyneema kopma gerinimi %3.3
        yani tek carpmada KIRILIR.
      * orgu: her filament ~15-20 um; bukulme filament capiyla belirlenir,
            eps = %2.1  < %3.3  -> DAYANIR.
    Sonuc: ip MUTLAKA ORGU (braided multifilament) olmalidir. Ve inceltmek
    filament capini DEGISTIRMEZ (ayni filamentten daha az sayida) --
    bu mekanizma inceltmeden ETKILENMEZ.
    """
    return (d_filament / 2) / (r_kenar + d_filament / 2)


def kenar_basinci(T, d, r_kenar):
    """Gerilimli ipin kanat kenarina uyguladigi temas basinci [Pa]."""
    return T / (r_kenar * d)


def sarilma_gerilimi(tau_stall, r_sarim):
    """Motor stall torku ipi ne kadar gerer [N]."""
    return tau_stall / r_sarim


def uc_hizi(D_pervane, rpm):
    return np.pi * D_pervane * rpm / 60.0
