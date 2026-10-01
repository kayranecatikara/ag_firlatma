"""Faz-0: Ic balistik. Yay -> namlu cikis hizi, geri tepme, yay tahkiki."""
import numpy as np
from scipy.integrate import solve_ivp
from .params import YAY_TELI
from .aero import G


# --------------------------------------------------------------- yay tahkiki
def yay_ozet(yay, L_namlu, L_kapsul):
    d, D, n, Lf, x0 = yay.d_tel, yay.D_orta, yay.n_aktif, yay.L_serbest, yay.x0
    G_mod = YAY_TELI["G"]
    C = D/d
    k = G_mod*d**4/(8*D**3*n)
    n_t = n + 2.0                      # kapali-taslanmis uc
    L_solid = n_t*d
    L_cocked = Lf - x0
    F_max = k*x0
    Kw = (4*C-1)/(4*C-4) + 0.615/C
    tau = Kw*8*F_max*D/(np.pi*d**3)
    Sut = YAY_TELI["A_MPa"]*1e6/((d*1e3)**YAY_TELI["m"])
    tau_izin = YAY_TELI["tau_oran"]*Sut
    L_tel = np.pi*D*n_t
    m_yay = YAY_TELI["rho"]*np.pi*0.25*d**2*L_tel
    return dict(
        k=k, C=C, L_solid=L_solid, L_cocked=L_cocked, F_max=F_max,
        tau=tau, tau_izin=tau_izin, SF_gerilme=tau_izin/tau,
        m_yay=m_yay, E_depo=0.5*k*x0**2,
        # tahkikler
        ok_solid   = L_cocked >= L_solid,
        ok_gerilme = tau <= tau_izin,
        ok_namlu   = (L_cocked + L_kapsul) <= L_namlu,
        ok_burkulma= (Lf/D) <= 5.2,                 # kilavuzsuz sinir
        bosluk_namlu = L_namlu - L_kapsul - L_cocked,
        strok_max  = min(x0, Lf - L_solid),
    )


def _atalet(t):
    """Hareketli grubun namlu ekseni etrafindaki atalet momenti [kg m^2]."""
    k_, b_, a_ = t.kapsul, t.bilye, t.ag
    I_b = k_.n_bilye*b_.m*k_.R_pitch**2
    R_out, R_in = 0.5*46.2e-3, 0.5*k_.D_hazne
    I_c = 0.5*k_.m_kapsul*(R_out**2 + R_in**2)
    I_n = 0.5*a_.m_ag*(0.35*k_.D_hazne)**2
    return I_b + I_c + I_n


def firlat(t, dt_carpma=1.5e-3):
    """Namlu ici ivmelenmeyi entegre eder, cikis durumunu dondurur."""
    y_, n_, k_ = t.yay, t.namlu, t.kapsul
    sp = yay_ozet(y_, n_.L_namlu, k_.L_kapsul)
    kk = sp["k"]
    strok = sp["strok_max"]
    if strok <= 0 or not sp["ok_solid"]:
        return dict(basarisiz=True, **sp)

    m_tr = t.m_hareketli + sp["m_yay"]/3.0      # otelenme etkin kutlesi
    I = _atalet(t)
    # yiv (helis) -> donme, esdeger ek atalet:  m_rot = I*(2pi/L_twist)^2
    m_rot = I*(2*np.pi/n_.twist_L)**2 if n_.twist_L > 0 else 0.0
    m_eff = m_tr + m_rot

    A_bore = np.pi*0.25*n_.D_bore**2
    F_fric = n_.F_surtunme0 + n_.mu_surtunme*t.m_hareketli*G*np.cos(n_.theta_atis)
    # yiv surtunmesi: teget kuvvetin surtunmeye katkisi
    if n_.twist_L > 0:
        F_fric *= (1.0 + 2*np.pi*k_.R_pitch/n_.twist_L)

    def rhs(x, s):
        v = max(s[1], 1e-9)
        F = (kk*(y_.x0 - x)
             - F_fric
             - 0.5*t.hava.rho*n_.Cd_bore*A_bore*v*v
             - t.m_hareketli*G*np.sin(n_.theta_atis))
        return [1.0/v, F/(m_eff*v)]     # d/dx of [t, v]

    sol = solve_ivp(rhs, [0.0, strok], [0.0, 1e-6], rtol=1e-8, atol=1e-10,
                    dense_output=True, max_step=strok/200)
    v_exit = float(sol.y[1, -1])
    t_exit = float(sol.y[0, -1])
    if not np.isfinite(v_exit) or v_exit <= 0:
        return dict(basarisiz=True, **sp)

    omega = 2*np.pi*v_exit/n_.twist_L if n_.twist_L > 0 else 0.0
    v_theta = omega*k_.R_pitch                   # bilyenin teget hizi
    v_rad_cep = v_exit*np.tan(k_.alpha_cep)      # konik cepten gelen radyal hiz

    E_yay   = sp["E_depo"]
    E_cikan = 0.5*t.m_ucan*v_exit**2
    E_kapsul= 0.5*k_.m_kapsul*v_exit**2
    E_rot   = 0.5*I*omega**2

    return dict(
        basarisiz=False, **sp,
        v_exit=v_exit, t_exit=t_exit, strok=strok,
        omega=omega, v_theta=v_theta, v_rad_cep=v_rad_cep,
        # radyal acilma hizi: konik cep ve donme katkilari
        v_radyal=np.hypot(v_rad_cep, v_theta),
        m_eff=m_eff, m_rot=m_rot, I=I,
        E_cikan=E_cikan, E_kapsul=E_kapsul, E_rot=E_rot,
        verim=E_cikan/E_yay,
        # drone'a etkiyen net geri tepme impulsu (kapsul namluda durdugu icin
        # onun momentumu geri kazanilir)
        J_geri=t.m_ucan*v_exit,
        F_geri_ort=t.m_ucan*v_exit/max(t_exit, 1e-6),
        # kapsulun agza carpma sok yuku
        F_sok=k_.m_kapsul*v_exit/dt_carpma,
    )


def firlat_genel(t, k, m_yay, x0, strok, dt_carpma=1.5e-3):
    """Verilen yay paketi (k, m_yay) ile ic balistik.

    yay_ozet()'e bagli degildir; ic ice / yan yana yay paketleri icin.
    """
    n_, k_ = t.namlu, t.kapsul
    m_tr = t.m_hareketli + m_yay/3.0
    I = _atalet(t)
    m_rot = I*(2*np.pi/n_.twist_L)**2 if n_.twist_L > 0 else 0.0
    m_eff = m_tr + m_rot
    A_bore = np.pi*0.25*n_.D_bore**2
    F_fric = n_.F_surtunme0 + n_.mu_surtunme*t.m_hareketli*G*np.cos(n_.theta_atis)
    if n_.twist_L > 0:
        F_fric *= (1.0 + 2*np.pi*k_.R_pitch/n_.twist_L)

    def rhs(x, s):
        v = max(s[1], 1e-9)
        F = (k*(x0 - x) - F_fric
             - 0.5*t.hava.rho*n_.Cd_bore*A_bore*v*v
             - t.m_hareketli*G*np.sin(n_.theta_atis))
        return [1.0/v, F/(m_eff*v)]

    sol = solve_ivp(rhs, [0.0, strok], [0.0, 1e-6], rtol=1e-8, atol=1e-10,
                    max_step=strok/300)
    v = float(sol.y[1, -1]); te = float(sol.y[0, -1])
    if not np.isfinite(v) or v <= 0:
        return dict(basarisiz=True)
    omega = 2*np.pi*v/n_.twist_L if n_.twist_L > 0 else 0.0
    E = 0.5*k*(x0**2 - max(x0-strok, 0)**2)
    return dict(basarisiz=False, v_exit=v, t_exit=te, strok=strok, k=k,
                omega=omega, v_theta=omega*k_.R_pitch,
                v_rad_cep=v*np.tan(k_.alpha_cep),
                v_radyal=np.hypot(v*np.tan(k_.alpha_cep), omega*k_.R_pitch),
                m_eff=m_eff, m_yay=m_yay, E_depo=E, F_max=k*x0,
                E_cikan=0.5*t.m_ucan*v**2, E_kapsul=0.5*k_.m_kapsul*v**2,
                verim=0.5*t.m_ucan*v**2/max(E, 1e-9),
                J_geri=t.m_ucan*v, F_geri_ort=t.m_ucan*v/max(te, 1e-6),
                F_sok=k_.m_kapsul*v/dt_carpma,
                ok_gerilme=True, ok_solid=True, ok_namlu=True, ok_burkulma=True,
                SF_gerilme=np.nan, L_solid=0.0, bosluk_namlu=0.0)
