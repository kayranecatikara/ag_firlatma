"""Faz-1 YUKSEK COZUNURLUKLU MODEL: kutle-yay-sonumleyici ag (lumped-parameter).

Uzay enkazi yakalama literaturunun standart yaklasimi:
  - ag dugumlere yiginlastirilir, ipler yalnizca CEKME tasiyan viskoelastik
    elemanlardir (bas kuvveti tasimaz -> tek tarafli kisit),
  - her elemana NORMAL/TEGET ayrisimli silindir suruklemesi uygulanir,
  - acik entegrasyon (velocity-Verlet) + CFL zaman adimi.

Amaci: ROM'u (netrom.py) kalibre etmek ve secilen tasarimlari dogrulamak.
Tasarim kesfinde DEGIL, yalnizca son adimda kullanilir.
"""
import numpy as np
from .aero import G


def orumcek_ag(n_ring, n_spoke, R):
    """Dugum konumlari (tam acik hal) ve eleman baglantilari."""
    th = np.arange(n_spoke)*2*np.pi/n_spoke
    P = [np.zeros(3)]
    for i in range(1, n_ring+1):
        r = R*i/n_ring
        for j in range(n_spoke):
            P.append([r*np.cos(th[j]), r*np.sin(th[j]), 0.0])
    P = np.array(P)

    def idx(i, j): return 1 + (i-1)*n_spoke + (j % n_spoke)
    E = []
    for j in range(n_spoke):
        E.append((0, idx(1, j)))                       # merkez -> 1. halka
    for i in range(1, n_ring):
        for j in range(n_spoke):
            E.append((idx(i, j), idx(i+1, j)))         # radyal
    for i in range(1, n_ring+1):
        for j in range(n_spoke):
            E.append((idx(i, j), idx(i, j+1)))         # cevrel
    E = np.array(E)
    bilye_dug = np.array([idx(n_ring, j) for j in
                          range(0, n_spoke, max(n_spoke//6, 1))][:6])
    return P, E, bilye_dug


def simule(t, launch, T=0.35, R_pak=None, L_pak=None, dt_kat=0.25,
           kayit=250, E_olcek=None, zeta=0.30, aero_olcek=1.0, topoloji=None):
    """Agi firlatma anindan T saniyeye kadar entegre eder (HAVA cercevesinde).

    topoloji=None -> orumcek agi (kaba, tasarim taramasi icin)
    topoloji=(P0,E,bd) -> hazir orgu (orn. agsim.hexag.altigen_ag ile uretilen
                          GERCEK altigen kafes)
    """
    ag, kap, hava, ang = t.ag, t.kapsul, t.hava, t.ang
    nR, nS = ag.n_ring, ag.n_spoke
    P0, E, bd = orumcek_ag(nR, nS, ag.R_ag) if topoloji is None else topoloji
    nN, nE = len(P0), len(E)
    i1, i2 = E[:, 0], E[:, 1]

    L0 = np.linalg.norm(P0[i2]-P0[i1], axis=1)         # serbest (acik) boylar
    # DUZELTME: kaba orgu (n_ring x n_spoke) gercek agdan COK daha az iplik
    # icerir. Kutle zaten gercek aga olceklenmisti; surukleme OLCEKLENMIYORDU
    # -> ag suruklemesi ~2.5-3.5x dusuk hesaplaniyordu. Her elemanin
    # suruklemesini temsil ettigi gercek iplik boyuna gore olcekle.
    olcek_ag = ag.L_iplik / L0.sum()
    Eeff = ag.E_iplik*(E_olcek if E_olcek is not None else ag.E_olcek)
    k_el = Eeff*ag.A_iplik/L0
    c_el = zeta*2*np.sqrt(k_el*(ag.m_ag/nN))           # iplik sonumlemesi

    # dugum kutleleri: baglanan eleman boylarinin yarisiyla orantili
    w = np.zeros(nN)
    np.add.at(w, i1, 0.5*L0); np.add.at(w, i2, 0.5*L0)
    m = ag.m_ag*w/w.sum()
    m[bd] += t.bilye.m                                  # bilyeler

    # --- baslangic: paketlenmis demet, dis halka onde ("pay-out")
    R_pak = R_pak or 0.40*kap.D_hazne
    L_pak = L_pak or kap.L_hazne
    rr = np.linalg.norm(P0[:, :2], axis=1)
    f = rr/max(rr.max(), 1e-12)
    P = np.zeros((nN, 3))
    ang_n = np.arctan2(P0[:, 1], P0[:, 0])
    P[:, 0] = R_pak*f*np.cos(ang_n)
    P[:, 1] = R_pak*f*np.sin(ang_n)
    P[:, 2] = -L_pak*(1.0-f)                            # z = ucus ekseni

    V = np.zeros((nN, 3))
    v_ax = launch["v_exit"]*np.cos(kap.alpha_cep)
    V[:, 2] = v_ax
    u_r = np.stack([np.cos(ang_n), np.sin(ang_n), np.zeros(nN)], 1)
    u_t = np.stack([-np.sin(ang_n), np.cos(ang_n), np.zeros(nN)], 1)
    V[bd] += (launch["v_rad_cep"]*u_r[bd] + launch["v_theta"]*u_t[bd])

    ruzgar = np.array([0.0, 0.0, -ang.V_drone])         # drone ileri -> bagil ruzgar
    g_vec = np.array([0.0, -G, 0.0])

    dt = dt_kat*np.sqrt(m.min()/k_el.max())
    n_adim = int(T/dt)
    her = max(n_adim//kayit, 1)

    def kuvvet(P, V):
        F = np.tile(m[:, None]*g_vec, (1, 1))
        d = P[i2]-P[i1]
        L = np.linalg.norm(d, axis=1)
        L = np.maximum(L, 1e-12)
        u = d/L[:, None]
        Ldot = np.sum((V[i2]-V[i1])*u, axis=1)
        Tn = k_el*(L-L0) + c_el*Ldot
        Tn = np.where(L > L0, np.maximum(Tn, 0.0), 0.0)  # SADECE cekme
        Fe = Tn[:, None]*u
        np.add.at(F, i1,  Fe); np.add.at(F, i2, -Fe)
        # eleman aerodinamigi (normal/teget)
        vm = 0.5*(V[i1]+V[i2]) - ruzgar
        vt = np.sum(vm*u, axis=1)[:, None]*u
        vn = vm - vt
        q = 0.5*hava.rho*ag.d_iplik*L*aero_olcek*olcek_ag
        Fa = -(q*ag.Cdn*np.linalg.norm(vn, axis=1))[:, None]*vn \
             - (q*ag.Cdt*np.linalg.norm(vt, axis=1))[:, None]*vt
        np.add.at(F, i1, 0.5*Fa); np.add.at(F, i2, 0.5*Fa)
        # bilye kure suruklemesi
        vb = V[bd]-ruzgar
        nb = np.linalg.norm(vb, axis=1, keepdims=True)
        F[bd] -= aero_olcek*0.5*hava.rho*t.bilye.Cd*np.pi*0.25*t.bilye.D**2*nb*vb
        return F, Tn

    A = kuvvet(P, V)[0]/m[:, None]
    out = dict(t=[], R=[], z=[], A_proj=[], T_max=[], kare=[], P_snap=[], V_snap=[])
    for s in range(n_adim):
        V += 0.5*dt*A
        P += dt*V
        Fn, Tn = kuvvet(P, V)
        A = Fn/m[:, None]
        V += 0.5*dt*A
        if s % her == 0:
            out["t"].append(s*dt)
            out["R"].append(float(np.mean(np.linalg.norm(P[bd, :2], axis=1))))
            out["z"].append(float(P[:, 2].mean()))
            # ucus eksenine dik izdusum alani (cevrel kabuk)
            rr2 = np.linalg.norm(P[:, :2], axis=1)
            out["A_proj"].append(float(np.pi*rr2.max()**2))
            out["T_max"].append(float(Tn.max()))
            # ucus eksenine dik gercek izdusum alani (konveks kabuk yerine
            # dugum bulutunun kare izdusumu) + tam anlik goruntu
            out["kare"].append(float((P[:, 0].max()-P[:, 0].min()) *
                                     (P[:, 1].max()-P[:, 1].min())))
            out["P_snap"].append(P.copy())
            out["V_snap"].append(V.copy())
    for k in out: out[k] = np.array(out[k])
    out["E"] = E                      # eleman baglanti listesi (cizim icin)
    out["olcek_ag"] = olcek_ag
    out["L0"] = L0
    out["dt"] = dt; out["n_adim"] = n_adim; out["nN"] = nN; out["nE"] = nE
    out["P"], out["V"], out["bilye_dug"] = P, V, bd
    return out
