"""Aerodinamik modeller: kure suruklemesi, iplik (silindir) elemani suruklemesi,
gozenekli ag esdeger surukleme alani."""
import numpy as np

G = 9.80665


def cd_kure(Re):
    """Kure surukleme katsayisi, 1e-1 < Re < 2e5 (Morrison korelasyonu, sadelestirilmis)."""
    Re = np.maximum(Re, 1e-3)
    return (24.0/Re + 2.6*(Re/5.0)/(1+(Re/5.0)**1.52)
            + 0.411*(Re/2.63e5)**-7.94/(1+(Re/2.63e5)**-8.0) + 0.25*(Re/1e6)/(1+Re/1e6))


def cd_silindir(Re):
    """Capraz akista silindir (iplik) surukleme katsayisi."""
    Re = np.maximum(Re, 1e-3)
    return 1.18 + 6.8/Re**0.89 + 1.96/np.sqrt(Re) - 0.0004*Re/(1+3.64e-7*Re**2)


def surukleme_kure(v_rel, D, hava):
    """Tek kure icin surukleme kuvvet vektoru [N]. v_rel: (...,3)"""
    V = np.linalg.norm(v_rel, axis=-1, keepdims=True)
    Re = hava.rho*V[...,0]*D/hava.mu
    Cd = cd_kure(Re)[..., None]
    A = np.pi*0.25*D**2
    return -0.5*hava.rho*Cd*A*V*v_rel


def surukleme_iplik(p1, p2, v1, v2, d_iplik, hava, Cdn=1.10, Cdt=0.03):
    """Iplik elemani icin normal/teget ayrisimli surukleme.

    Dogru model budur: bir ipe teget akis neredeyse hic kuvvet uretmez
    (Cdt ~ 0.02-0.05), dik akis ise Cdn ~ 1.1 ile tam silindir suruklemesi
    uretir. Tek bir skaler Cd kullanmak agin acilma suresini 2-3x yanlis verir.

    Donus: (F1, F2) her dugume yarim kuvvet.
    """
    seg = p2 - p1
    L = np.linalg.norm(seg, axis=-1, keepdims=True)
    L = np.maximum(L, 1e-12)
    t = seg/L
    v = 0.5*(v1+v2) - hava.ruzgar
    vt = np.sum(v*t, axis=-1, keepdims=True)*t
    vn = v - vt
    nvn = np.linalg.norm(vn, axis=-1, keepdims=True)
    nvt = np.linalg.norm(vt, axis=-1, keepdims=True)
    q = 0.5*hava.rho*d_iplik*L
    F = -q*(Cdn*nvn*vn + Cdt*nvt*vt)
    return 0.5*F, 0.5*F


def CdA_ag_acik(R_ag, solidite, Cdn=1.10, kapali_R=None):
    """Tamamen acik agin eksenel esdeger surukleme alani Cd*A [m^2].

    Gozenekli ekran: engellenen alan = beta * A_cevrel.
    Yuksek gozeneklilikte (beta < 0.1) perdeleme ihmal edilir.
    """
    A = 1.5*np.sqrt(3.0)*R_ag**2        # altigen ag (6 bilye koselerde)
    return Cdn*solidite*A


def CdA_paket(D_paket, Cd=0.9):
    """Henuz acilmamis ag paketinin (silindir demeti) Cd*A."""
    return Cd*np.pi*0.25*D_paket**2


def balistik_uzunluk(m, CdA, rho=1.225):
    """lambda = 2m/(rho*Cd*A)  [m].

    Ikinci derece suruklemede hiz 1/e'ye dustugu karakteristik yol.
    Bu TEK BASINA en onemli sayi: agin menzilini bu belirler.
    """
    return 2.0*m/(rho*np.maximum(CdA, 1e-12))


def goreli_menzil_max(v_muzzle, V_serbest, lam):
    """Serbest akis V_serbest icine v_muzzle ile atilan cismin
    FIRLATICIYA GORE ulasabildigi maksimum ileri mesafe [m].

    Hava cercevesinde: v0 = V_serbest + v_muzzle, ikinci derece yavaslama
      v(t) = v0/(1+v0 t/lam),  x(t) = lam*ln(1+v0 t/lam)
    Firlatici sabit V_serbest ile gider. Goreli mesafe v = V_serbest
    olunca maksimuma ulasir:
      dx_max = lam*[ ln(v0/V) - 1 + V/v0 ]
    Bu, 100 km/h'te agin gercek etkili menzilidir.
    """
    v0 = V_serbest + v_muzzle
    if V_serbest <= 1e-6:
        return np.inf
    r = v0/V_serbest
    return lam*(np.log(r) - 1.0 + 1.0/r)
