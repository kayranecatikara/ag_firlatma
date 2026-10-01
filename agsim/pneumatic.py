"""Faz-0 ALTERNATIF: pnomatik tahrik (basincli hava / CO2).

Politropik genlesme modeli:
  - V0 hacimli depo p0 basincinda, valf acildiginda piston arkasindaki
    hacim A*x kadar buyur,
  - gaz politropik genlesir:  p(x) = p0 * (V0/(V0+A*x))^n
  - valf kisitlamasi bir bosaltim katsayisi (Cd_valf) ile temsil edilir.

Yay modelinin aksine HAREKETLI KUTLE YOK: pnomatigin temel ustunlugu budur.
"""
import numpy as np
from scipy.integrate import solve_ivp
from .aero import G
from .launcher import _atalet

P_ATM = 101325.0


def firlat_pnomatik(t, p0_bar=6.0, V0_cm3=100.0, n_pol=1.30,
                    Cd_valf=0.75, dt_carpma=1.5e-3):
    """Pnomatik ic balistik. Donus yapisi launcher.firlat() ile ayni."""
    n_, k_ = t.namlu, t.kapsul
    A = np.pi*0.25*n_.D_bore**2
    strok = n_.L_namlu - k_.L_kapsul - 0.010          # 10 mm valf/manifold payi
    if strok <= 0:
        return dict(basarisiz=True)
    p0 = p0_bar*1e5
    V0 = V0_cm3*1e-6

    m_tr = t.m_hareketli                               # YAY KUTLESI YOK
    I = _atalet(t)
    m_rot = I*(2*np.pi/n_.twist_L)**2 if n_.twist_L > 0 else 0.0
    m_eff = m_tr + m_rot

    F_fric = n_.F_surtunme0 + n_.mu_surtunme*t.m_hareketli*G*np.cos(n_.theta_atis)
    if n_.twist_L > 0:
        F_fric *= (1.0 + 2*np.pi*k_.R_pitch/n_.twist_L)

    def basinc(x):
        return p0*(V0/(V0 + A*x))**n_pol

    def rhs(x, s):
        v = max(s[1], 1e-9)
        # valf kisitlamasi: etkin basinci hiz arttikca dusuren basit model
        p = basinc(x)
        dp = (p - P_ATM)*Cd_valf
        F = (dp*A - F_fric
             - 0.5*t.hava.rho*n_.Cd_bore*A*v*v
             - t.m_hareketli*G*np.sin(n_.theta_atis))
        return [1.0/v, F/(m_eff*v)]

    sol = solve_ivp(rhs, [0.0, strok], [0.0, 1e-6], rtol=1e-8, atol=1e-10,
                    max_step=strok/300)
    v_exit, t_exit = float(sol.y[1, -1]), float(sol.y[0, -1])
    if not np.isfinite(v_exit) or v_exit <= 0:
        return dict(basarisiz=True)

    # depolanan/harcanan is
    xs = np.linspace(0, strok, 400)
    W = np.trapz((basinc(xs)-P_ATM)*Cd_valf*A, xs)
    omega = 2*np.pi*v_exit/n_.twist_L if n_.twist_L > 0 else 0.0

    return dict(
        basarisiz=False, v_exit=v_exit, t_exit=t_exit, strok=strok,
        omega=omega, v_theta=omega*k_.R_pitch,
        v_rad_cep=v_exit*np.tan(k_.alpha_cep),
        v_radyal=np.hypot(v_exit*np.tan(k_.alpha_cep), omega*k_.R_pitch),
        m_eff=m_eff, m_yay=0.0, E_depo=W,
        p_ilk=p0/1e5, p_son=basinc(strok)/1e5,
        F_piston_ilk=(p0-P_ATM)*A, F_piston_son=(basinc(strok)-P_ATM)*A,
        E_cikan=0.5*t.m_ucan*v_exit**2,
        E_kapsul=0.5*k_.m_kapsul*v_exit**2,
        verim=0.5*t.m_ucan*v_exit**2/max(W, 1e-9),
        J_geri=t.m_ucan*v_exit,
        F_geri_ort=t.m_ucan*v_exit/max(t_exit, 1e-6),
        F_sok=k_.m_kapsul*v_exit/dt_carpma,
        ok_gerilme=True, ok_solid=True, ok_namlu=True, ok_burkulma=True,
        SF_gerilme=np.inf, L_solid=0.0, bosluk_namlu=0.0, k=np.nan, F_max=np.nan,
    )
