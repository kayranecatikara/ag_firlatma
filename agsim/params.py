"""Tasarim parametreleri ve malzeme veritabani.

Tum SI birimleri (m, kg, s, N, Pa). Kullanici arayuzunde mm/g kullanilir,
donusum burada yapilir.
"""
from dataclasses import dataclass, field, asdict
import numpy as np

# ---------------------------------------------------------------- malzemeler
# rho [kg/m^3], E [Pa], sigma_u [Pa]
BILYE_MALZEME = {
    "POM":       dict(rho=1410.0),
    "PLA":       dict(rho=1240.0),
    "Naylon":    dict(rho=1150.0),
    "Aluminyum": dict(rho=2700.0),
    "Celik":     dict(rho=7850.0),
    "Pirinc":    dict(rho=8500.0),
    "Kursun":    dict(rho=11340.0),
    "Tungsten":  dict(rho=18000.0),
    # ELDEKI BILYE: O8 mm olculdu, 4 g tartildi -> 14921 kg/m3.
    # Kursundan agir, tungstenden hafif: muhtemelen tungsten alasimi,
    # ya da cap/kutle yaklasik olculmus. BALISTIKTE KUTLE belirleyicidir,
    # o yuzden olculen 4 g'i esas aliyoruz.
    "Eldeki_O8":  dict(rho=14921.0),
}

# Ag ipligi: E_eff = orgulu ipin efektif elastik modulu (ham lif degil)
IPLIK_MALZEME = {
    "Dyneema_SK78": dict(rho=970.0,  E=90e9, sigma_u=3000e6),
    "Kevlar_29":    dict(rho=1440.0, E=70e9, sigma_u=2900e6),
    "Naylon_66":    dict(rho=1140.0, E=3.0e9, sigma_u=800e6),
    "Polyester":    dict(rho=1380.0, E=12e9, sigma_u=1100e6),
}

# Yay teli (ASTM A228 muzik teli): Sut = A / d^m  [MPa, d in mm]
YAY_TELI = dict(G=79.3e9, rho=7850.0, A_MPa=2211.0, m=0.145, tau_oran=0.45)


# ---------------------------------------------------------------- CAD sabitleri
@dataclass
class Namlu:
    """VAKKAS_NAMLU.STEP'ten olculen degerler (baseline)."""
    D_bore:     float = 39.0e-3   # R19.5 silindir  -> Ø39 mm
    L_namlu:    float = 118.0e-3  # Y: -59..+59
    mu_surtunme:float = 0.20      # PETG/PLA - PLA kuru kayma
    F_surtunme0:float = 2.0       # N, on-yuk/keci sizdirmazlik surtunmesi
    Cd_bore:    float = 1.0       # namlu icindeki hava itme katsayisi
    twist_L:    float = 0.0       # yiv helis adimi [m]; 0 = duz yiv (donme yok)
    theta_atis: float = 0.0       # namlu egim acisi [rad], 0 = yatay ileri


@dataclass
class Kapsul:
    """VAKKAS_NAMLU_ICI_AG_KAPSULU.STEP'ten olculen degerler (baseline)."""
    m_kapsul:  float = 20.0e-3    # kg  (PETG %40 dolgu tahmini - TARTILMALI)
    L_kapsul:  float = 50.0e-3
    D_hazne:   float = 30.0e-3    # R15 -> merkezi ag haznesi
    L_hazne:   float = 43.0e-3
    D_cep:     float = 9.0e-3     # R4.5 x12 yuzey = 6 bilye cebi
    R_pitch:   float = 14.5e-3    # cep merkezlerinin eksen mesafesi
    n_bilye:   int   = 6
    alpha_cep: float = 0.0        # cep eksen acisi [rad] -- CAD'DE SIFIR!
    paket_dol: float = 0.45       # ag paketleme dolgu orani (hacimsel)


@dataclass
class Yay:
    d_tel:   float = 3.0e-3
    D_orta:  float = 25.0e-3    # ortalama cap
    n_aktif: float = 10.0
    L_serbest:float= 110.0e-3
    x0:      float = 50.0e-3    # on-sikistirma = strok


@dataclass
class Bilye:
    malzeme: str   = "Celik"
    D:       float = 9.0e-3     # cep capina esit (bosluk ihmal)
    Cd:      float = 0.47

    @property
    def m(self):
        return BILYE_MALZEME[self.malzeme]["rho"] * (np.pi/6.0) * self.D**3


@dataclass
class Ag:
    malzeme:  str   = "Dyneema_SK78"
    R_ag:     float = 0.75      # acik agin cevrel yaricapi [m]
    goz:      float = 0.060     # goz (mesh) araligi [m]
    d_iplik:  float = 0.30e-3
    n_ring:   int   = 6         # ROM disi tam model icin
    n_spoke:  int   = 12
    Cdn:      float = 1.10      # iplige dik surukleme
    Cdt:      float = 0.03      # iplige teget surukleme
    E_olcek:  float = 0.05      # sayisal sertlik olcegi (explicit dt icin)

    @property
    def rho_iplik(self): return IPLIK_MALZEME[self.malzeme]["rho"]
    @property
    def E_iplik(self):   return IPLIK_MALZEME[self.malzeme]["E"]
    @property
    def sigma_u(self):   return IPLIK_MALZEME[self.malzeme]["sigma_u"]
    @property
    def A_iplik(self):   return np.pi*0.25*self.d_iplik**2
    @property
    def F_kopma(self):   return self.sigma_u * self.A_iplik

    @property
    def L_iplik(self):
        """Gercek kare-goz agin toplam iplik uzunlugu [m].

        Kenar S = 2*R_ag olan kare ag, goz araligi a:
        her yonde (S/a + 1) iplik, her biri S uzunlugunda.
        (Mekanik model kaba-tanecikli orumcek agi kullanir; kutle
         bu gercek degerden olceklenir.)
        """
        # 6 bilyeli ag ALTIGENDIR (bilyeler koselerde, R_ag = kose yaricapi).
        # Kare goz, iki yonde iplik: alan basina 2/goz metre + cevre ipi.
        A = self.A_ag
        return 2.0 * A / self.goz + 6.0 * self.R_ag

    @property
    def A_ag(self):
        """Altigen agin alani [m2] (kose yaricapi R_ag)."""
        return 1.5 * np.sqrt(3.0) * self.R_ag ** 2

    @property
    def m_ag(self):
        return self.rho_iplik * self.A_iplik * self.L_iplik

    @property
    def solidite(self):
        """Kare goz icin doluluk orani beta ~ 2d/a (d<<a)."""
        b = 2*self.d_iplik/self.goz
        return min(b - (self.d_iplik/self.goz)**2, 1.0)

    @property
    def V_paket(self):
        return self.A_iplik * self.L_iplik


@dataclass
class Hava:
    rho:  float = 1.225
    mu:   float = 1.81e-5
    ruzgar: np.ndarray = field(default_factory=lambda: np.zeros(3))


@dataclass
class Angajman:
    """Goreli hareket senaryosu. x = ileri, y = saga, z = yukari."""
    V_drone:  float = 100/3.6     # 27.78 m/s
    V_hedef:  float = 100/3.6
    # hedefin drone'a gore yaklasma acisi [rad]:
    #   0    = ayni yonde (takip/pursuit)  -> goreli hiz ~0
    #   pi   = karsidan karsiya (head-on)  -> goreli hiz 2V
    psi:      float = 0.0
    menzil0:  float = 5.0         # atis anindaki mesafe [m]
    # hedef gabarisi (yakalanmasi gereken alan)
    hedef_kanat: float = 1.5      # kanat acikligi [m]
    hedef_boy:   float = 1.0      # govde boyu [m]
    # atis yonu: namlunun drone govde eksenine gore acisi [rad]
    atis_elev: float = 0.0


@dataclass
class Tasarim:
    namlu:  Namlu     = field(default_factory=Namlu)
    kapsul: Kapsul    = field(default_factory=Kapsul)
    yay:    Yay       = field(default_factory=Yay)
    bilye:  Bilye     = field(default_factory=Bilye)
    ag:     Ag        = field(default_factory=Ag)
    hava:   Hava      = field(default_factory=Hava)
    ang:    Angajman  = field(default_factory=Angajman)

    @property
    def m_ucan(self):
        """Namludan cikan kutle (bilyeler + ag). Kapsul namluda kalir."""
        return self.kapsul.n_bilye*self.bilye.m + self.ag.m_ag

    @property
    def m_hareketli(self):
        """Namlu icinde ivmelenen toplam kutle (yay etkin kutlesi haric)."""
        return self.kapsul.m_kapsul + self.m_ucan

    def ozet(self):
        d = {}
        d["m_kapsul [g]"]   = self.kapsul.m_kapsul*1e3
        d["m_bilye_tek [g]"]= self.bilye.m*1e3
        d["m_bilye_top [g]"]= self.kapsul.n_bilye*self.bilye.m*1e3
        d["m_ag [g]"]       = self.ag.m_ag*1e3
        d["m_ucan [g]"]     = self.m_ucan*1e3
        d["m_hareketli [g]"]= self.m_hareketli*1e3
        d["ag iplik [m]"]   = self.ag.L_iplik
        d["ag solidite [%]"]= self.ag.solidite*100
        d["ag paket hacim [cm3]"] = self.ag.V_paket*1e6
        return d
