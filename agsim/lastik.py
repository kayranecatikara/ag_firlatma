"""Lastik bant (zipkin tufegi tipi) tahrik modeli.

Kaucuk dogrusal bir yay DEGILDIR. Neo-Hookean model (dogal kaucuk icin
lambda <= ~4 araliginda iyi bir yaklasim):

    nominal gerilme   sigma(lam) = G * (lam - 1/lam^2)
    enerji yogunlugu  W(lam)     = G/2 * (lam^2 + 2/lam - 3)

G = kayma modulu. Dogal lateks icin ~0.35-0.55 MPa; URUNE GORE DEGISIR ve
basit bir cekme testiyle (bagaj kantari + cetvel) olculmelidir (bkz.
cekme_testi_tablosu). Bant bir ucu sabit, diger ucu kapsulle hareket ettigi
icin hiz profili dogrusal -> etkin hareketli kutle m_bant/3.

Bant geometrisi (namlu disinda, agizdaki bilezikten capraz pime):
    L_top     : bant + baglanti donanimi toplam boyu (anlik)
    H         : uzamayan donanim boyu (yuksuk + kopru ipi)
    L0        : kaucugun serbest (gerilmemis) calisma boyu
    lam       = (L_top - H) / L0 ;  lam <= 1 ise bant GEVSEK, kuvvet yok
"""
from dataclasses import dataclass
import numpy as np
from scipy.integrate import solve_ivp
from .aero import G as g0
from .launcher import _atalet

RHO_LATEKS = 950.0


@dataclass
class Bant:
    n: int = 2                 # bant sayisi (capraz pimin iki ucu)
    OD: float = 14.0e-3        # dis cap
    ID: float = 4.0e-3         # ic cap
    L0: float = 0.067          # kaucuk calisma boyu (serbest)
    H: float = 0.012           # uzamayan donanim boyu
    Gmod: float = 0.45e6       # kayma modulu [Pa]
    eta: float = 0.88          # histerezis: bosalmada geri donen oran

    @property
    def A0(self):
        return np.pi * 0.25 * (self.OD ** 2 - self.ID ** 2)

    @property
    def m(self):
        return self.n * RHO_LATEKS * self.A0 * self.L0

    def lam(self, L_top):
        return max((L_top - self.H) / self.L0, 1.0)

    def F(self, L_top, bosalma=True):
        """Toplam cekme kuvveti [N] (tum bantlar)."""
        la = (L_top - self.H) / self.L0
        if la <= 1.0:
            return 0.0
        f = self.n * self.Gmod * self.A0 * (la - 1.0 / la ** 2)
        return f * (self.eta if bosalma else 1.0)

    def W(self, la):
        return 0.5 * self.Gmod * (la ** 2 + 2.0 / la - 3.0)

    def E_depo(self, L_top):
        return self.n * self.A0 * self.L0 * self.W(self.lam(L_top))


def firlat_lastik(t, bant, L_kurulu, strok, dt_carpma=1.5e-3):
    """Lastik bantla ic balistik. launcher.firlat() ile ayni cikti yapisi.

    L_kurulu : kurulu halde bant toplam boyu (bilezik -> capraz pim)
    strok    : kapsulun omuza kadar gittigi yol
    """
    n_, k_ = t.namlu, t.kapsul
    m_eff = t.m_hareketli + bant.m / 3.0
    I = _atalet(t)
    m_rot = I * (2 * np.pi / n_.twist_L) ** 2 if n_.twist_L > 0 else 0.0
    m_eff += m_rot
    A_bore = np.pi * 0.25 * n_.D_bore ** 2
    F_fric = n_.F_surtunme0 + n_.mu_surtunme * t.m_hareketli * g0
    if n_.twist_L > 0:
        F_fric *= (1.0 + 2 * np.pi * k_.R_pitch / n_.twist_L)

    def rhs(x, s):
        v = max(s[1], 1e-9)
        F = (bant.F(L_kurulu - x) - F_fric
             - 0.5 * t.hava.rho * n_.Cd_bore * A_bore * v * v)
        return [1.0 / v, F / (m_eff * v)]

    sol = solve_ivp(rhs, [0.0, strok], [0.0, 1e-6], rtol=1e-8, atol=1e-10,
                    max_step=strok / 400)
    v, te = float(sol.y[1, -1]), float(sol.y[0, -1])
    if not np.isfinite(v) or v <= 0:
        return dict(basarisiz=True)
    omega = 2 * np.pi * v / n_.twist_L if n_.twist_L > 0 else 0.0
    E = bant.E_depo(L_kurulu)
    L_gevsek = bant.L0 + bant.H
    return dict(
        basarisiz=False, v_exit=v, t_exit=te, strok=strok,
        omega=omega, v_theta=omega * k_.R_pitch,
        v_rad_cep=v * np.tan(k_.alpha_cep),
        v_radyal=np.hypot(v * np.tan(k_.alpha_cep), omega * k_.R_pitch),
        m_eff=m_eff, m_bant=bant.m, E_depo=E,
        F_kurma=bant.F(L_kurulu, bosalma=False),
        lam_kurulu=bant.lam(L_kurulu),
        gucsuz_yol=max(0.0, strok - (L_kurulu - L_gevsek)),
        E_cikan=0.5 * t.m_ucan * v ** 2, verim=0.5 * t.m_ucan * v ** 2 / max(E, 1e-9),
        J_geri=t.m_ucan * v, F_sok=k_.m_kapsul * v / dt_carpma,
        # netrom/netfull uyumu
        m_yay=0.0, k=np.nan, F_max=bant.F(L_kurulu, bosalma=False),
        ok_gerilme=True, ok_solid=True, ok_namlu=True, ok_burkulma=True,
        SF_gerilme=np.nan, L_solid=0.0, bosluk_namlu=0.0,
    )


def cekme_testi_tablosu(bant, lams=(1.5, 2.0, 2.5, 3.0, 3.5, 4.0)):
    """Kullanicinin elindeki bantla karsilastirma icin beklenen kuvvetler.
    Bir bant, bagaj kantariyla bu uzamalara cekilip kuvvet okunur;
    olculen/tablo orani G'yi dogrudan duzeltir."""
    tek = Bant(n=1, OD=bant.OD, ID=bant.ID, L0=bant.L0, H=0.0, Gmod=bant.Gmod)
    return [(la, la * tek.L0, tek.F(la * tek.L0, bosalma=False)) for la in lams]
