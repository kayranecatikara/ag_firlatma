"""Ic ice (konsantrik) veya yan yana coklu yay paketi.

Kullanicinin kurma konsepti: yay bir kez kurulur, iki celik pim gecer,
servolar pimleri cekince atis olur. Yani KURMA KUVVETI bir kisit degildir
(yerde krikoyla/vidayla kurulur); kisit yay gerilmesi ve namluya sigmasidir.
Bu, onceki 300 N kisitini gecersiz kilar.
"""
import numpy as np
from .params import YAY_TELI


def yay_k(d, D, n):
    return YAY_TELI["G"]*d**4/(8*D**3*n)


def yay_tau(d, D, F):
    C = D/d
    Kw = (4*C-1)/(4*C-4) + 0.615/C
    return Kw*8*F*D/(np.pi*d**3)


def tau_izin(d):
    Sut = YAY_TELI["A_MPa"]*1e6/((d*1e3)**YAY_TELI["m"])
    return YAY_TELI["tau_oran"]*Sut


def yay_m(d, D, n):
    return YAY_TELI["rho"]*np.pi*0.25*d**2*(np.pi*D*(n+2))


def paket_ic_ice(katmanlar, x0, L_serbest):
    """Ic ice yaylar: ayni strok, kuvvetler TOPLANIR.

    katmanlar: [(d, D, n), ...]  en ic -> en dis
    Donus: toplam k, kutle, her katman icin emniyet katsayisi, gecerlilik.
    """
    k_top, m_top, SF = 0.0, 0.0, []
    for (d, D, n) in katmanlar:
        k = yay_k(d, D, n)
        F = k*x0
        SF.append(tau_izin(d)/yay_tau(d, D, F))
        k_top += k; m_top += yay_m(d, D, n)
    # gecerlilik: ic ice gecme bosluklari + blok boyu
    ok_gecme = True
    for i in range(len(katmanlar)-1):
        d_i, D_i, _ = katmanlar[i]
        d_o, D_o, _ = katmanlar[i+1]
        # dis yayin ic capi > ic yayin dis capi + 1 mm bosluk
        if (D_o - d_o) < (D_i + d_i) + 1.5e-3:
            ok_gecme = False
    L_solid = max((n+2)*d for (d, D, n) in katmanlar)
    return dict(k=k_top, m_yay=m_top, SF=np.array(SF), SF_min=float(min(SF)),
                L_solid=L_solid, ok_gecme=ok_gecme,
                ok_solid=(L_serbest - x0) >= L_solid,
                E=0.5*k_top*x0**2, F_kurma=k_top*x0)


def paket_yan_yana(d, D, n, adet, D_bore, x0, L_serbest):
    """Yan yana N yay: ayni strok, kuvvetler toplanir, bolme cemberine sigmali."""
    k1 = yay_k(d, D, n)
    F1 = k1*x0
    SF = tau_izin(d)/yay_tau(d, D, F1)
    R_out = 0.5*(D + d)
    if adet == 1:
        ok_sig = (D + d) <= D_bore - 1e-3
    else:
        R_pitch = R_out/np.sin(np.pi/adet)          # komsu yaylar tegetlensin
        ok_sig = (R_pitch + R_out) <= 0.5*D_bore - 0.5e-3
    return dict(k=adet*k1, m_yay=adet*yay_m(d, D, n), SF_min=SF,
                L_solid=(n+2)*d, ok_gecme=ok_sig,
                ok_solid=(L_serbest - x0) >= (n+2)*d,
                E=0.5*adet*k1*x0**2, F_kurma=adet*k1*x0)
