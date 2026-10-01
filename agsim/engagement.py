"""Faz-2: Angajman - hedefe gore goreli kinematik ve yakalama olcutu."""
import numpy as np


def degerlendir(t, uc_sonuc, kapsama=1.0):
    """Ag ucusunu hedef senaryosuna gore puanlar."""
    ang, ag = t.ang, t.ag
    ts, dx, R = uc_sonuc["t"], uc_sonuc["dx"], uc_sonuc["R"]

    # hedefin drone'a gore ileri mesafesi
    v_rel = ang.V_hedef*np.cos(ang.psi) - ang.V_drone
    d_hedef = ang.menzil0 + v_rel*ts

    # kesisme: agin drone-goreli mesafesi hedefinkini gecerse
    fark = dx - d_hedef
    idx = np.where(np.diff(np.sign(fark)) > 0)[0]
    R_ger = 0.5*ang.hedef_kanat*kapsama

    if len(idx) == 0:
        return dict(kesisme=False, t_kesisme=np.nan, R_kesisme=np.nan,
                    A_kesisme=0.0, ort_kapsama=0.0, basari=False,
                    R_gerekli=R_ger, marj_menzil=uc_sonuc["dx_max"]-ang.menzil0)

    i = idx[0]
    w = fark[i]/(fark[i]-fark[i+1]) if fark[i] != fark[i+1] else 0.0
    t_k = ts[i] + w*(ts[i+1]-ts[i])
    R_k = R[i] + w*(R[i+1]-R[i])

    basari = (R_k >= R_ger) and (ag.goz <= 0.5*ang.hedef_boy) \
             and (uc_sonuc["kopma_SF"] > 1.0)
    return dict(kesisme=True, t_kesisme=t_k, R_kesisme=R_k,
                A_kesisme=np.pi*R_k**2, ort_kapsama=min(R_k/R_ger, 1.0),
                basari=bool(basari), R_gerekli=R_ger,
                marj_menzil=uc_sonuc["dx_max"]-ang.menzil0)


def etkin_menzil(uc_sonuc, R_gerekli):
    """ETKIN MENZIL: agin YETERINCE ACIK oldugu en uzak drone-goreli mesafe [m].

    Sistemin tek en onemli performans olcutu budur. Ag acilmadan once ne kadar
    ileri giderse gitsin ise yaramaz; acildiktan sonra surukleme onu hizla
    geri supurur. Ikisinin kesisimi gercek angajman zarfidir.
    """
    dx, R = uc_sonuc["dx"], uc_sonuc["R"]
    m = R >= R_gerekli
    return float(dx[m].max()) if m.any() else 0.0
