"""Faz-1 HIZLI MODEL (ROM): agin acilmasi + ucusu, 6 serbestlik dereceli.

Durum:  [x, z, vx, vz, R, vR]
  x,z : ag agirlik merkezinin HAVA cercevesindeki konumu (ileri, yukari)
  R   : agin anlik acilma yaricapi
Tasarim kesif dongusu (binlerce kosum) bunu kullanir; tam kutle-yay-sonumleyici
modeli (netfull.py) bunu kalibre eder ve secilen tasarimlari dogrular.
"""
import numpy as np
from scipy.integrate import solve_ivp
from .aero import G

KAPPA_M = 0.50      # agin radyal etkin kutle orani  <r^2>/R^2 ~ 1/2
KAPPA_R = 2.963     # radyal surukleme kalibrasyonu (netfull.py ile ayarlandi, RMS %12)


def _CdA_eks(R, ag, D_paket, Cd_pak=0.9):
    """Eksenel esdeger surukleme alani: paket -> acik gecisi."""
    A_pak = Cd_pak*np.pi*0.25*D_paket**2
    A_acik = ag.Cdn*ag.solidite*np.pi*R**2
    return np.maximum(A_pak, A_acik)


def _k_radyal(ag):
    """Ag tam gerildiginde radyal geri-cagirici sertlik [N/m] ve yuk tasiyan iplik sayisi."""
    n_yuk = max(2.0*np.floor(2.0*ag.R_ag/ag.goz), 2.0)
    k = n_yuk*ag.E_iplik*ag.A_iplik/ag.R_ag*ag.E_olcek
    return k, n_yuk


def uc(t, launch, T=0.60, n_ornek=400):
    """Agi firlatma anindan itibaren entegre eder.

    launch: launcher.firlat() ciktisi
    Donus: sozluk (zaman serileri + metrikler)
    """
    ag, hava, ang, kap = t.ag, t.hava, t.ang, t.kapsul
    m_ucan = t.m_ucan
    m_rad = kap.n_bilye*t.bilye.m + KAPPA_M*ag.m_ag
    k_rad, n_yuk = _k_radyal(ag)
    # Orgulu ag + dugum surtunmesi + aero: ilk cevrimde yuksek dissipasyon
    c_rad = 0.35*2*np.sqrt(k_rad*m_rad)        # %35 kritik sonumleme
    D_pak = kap.D_hazne
    V_d = ang.V_drone
    Vw = hava.ruzgar[0]

    # baslangic: drone hizi + namlu cikis hizi (eksenel bilesen)
    a_el = ang.atis_elev
    v_ax = launch["v_exit"]*np.cos(kap.alpha_cep)
    vx0 = V_d + v_ax*np.cos(a_el)
    vz0 = v_ax*np.sin(a_el)
    R0 = kap.R_pitch
    vR0 = launch["v_radyal"]

    def rhs(tt, s):
        x, z, vx, vz, R, vR = s
        R = max(R, 1e-4)
        CdA = _CdA_eks(R, ag, D_pak)
        vrx, vrz = vx - Vw, vz
        V = np.hypot(vrx, vrz)
        q = 0.5*hava.rho*CdA*V/m_ucan
        ax = -q*vrx
        az = -q*vrz - G
        # radyal denge
        CdAr = KAPPA_R*ag.Cdn*ag.solidite*np.pi*R**2
        F_drag = -0.5*hava.rho*CdAr*abs(vR)*vR
        F_ten = -(k_rad*(R-ag.R_ag) + c_rad*vR) if R > ag.R_ag else 0.0
        aR = (F_drag + F_ten)/m_rad
        if R <= 1.1e-4 and aR < 0:              # ag kendi uzerine kapanamaz
            aR = 0.0
        return [vx, vz, ax, az, vR, aR]

    def ev_acildi(tt, s):  return s[4] - 0.90*ag.R_ag
    ev_acildi.terminal = False
    def ev_yere(tt, s):    return s[1] + 60.0
    ev_yere.terminal = True

    sol = solve_ivp(rhs, [0, T], [0, 0, vx0, vz0, R0, vR0],
                    rtol=1e-7, atol=1e-9, dense_output=True,
                    events=[ev_acildi, ev_yere], max_step=T/200)

    ts = np.linspace(0, sol.t[-1], n_ornek)
    Y = sol.sol(ts)
    x, z, vx, vz, R, vR = Y
    x_d = V_d*ts                                  # drone konumu
    dx = x - x_d                                  # DRONE'A GORE ileri mesafe

    t_ac = sol.t_events[0][0] if len(sol.t_events[0]) else np.nan
    if np.isfinite(t_ac):
        xa = sol.sol(t_ac)
        d_ac = xa[0] - V_d*t_ac
    else:
        d_ac = np.nan
    i_max = int(np.argmax(dx))

    # tepe iplik gerilimi (kopma tahkiki)
    R = np.maximum(R, 0.0)
    R_over = np.maximum(R - ag.R_ag, 0.0)
    T_iplik = (k_rad*R_over + c_rad*np.maximum(vR, 0)*(R_over > 0))/max(n_yuk, 1.0)

    return dict(t=ts, x=x, z=z, vx=vx, vz=vz, R=R, vR=vR, dx=dx,
                t_acilma=t_ac, d_acilma=d_ac,
                dx_max=dx[i_max], t_dx_max=ts[i_max],
                R_at_dxmax=R[i_max],
                T_iplik_tepe=float(np.max(T_iplik)),
                kopma_SF=ag.F_kopma/max(float(np.max(T_iplik)), 1e-9),
                sol=sol)
