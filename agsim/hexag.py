"""GERCEK COZUNURLUKTE ALTIGEN AG ORGUSU.

netfull.orumcek_ag() bir "orumcek agi" (halka + parmaklik) uretir: tasarim
kararlari icin yeterli, cunku ag ACILMASI topolojiye degil kutle/surukleme
dagilimina bagli. Ama DOLANMA (entanglement) icin yetmez -- kaba orgunun
goz acikligi 0.7 m iken hedefin govdesi 0.085 m'dir, ag hedefin arasindan
gecip gider.

Burada gercek fiziksel orgu kuruluyor: bal petegi (honeycomb) kafes,
goz acikligi `goz` (karsilikli kenarlar arasi mesafe).
    kenar boyu a = goz / sqrt(3)
Bu, agsim.params'taki analitik iplik boyu formuluyle TUTARLIDIR:
    bal petegi iplik/alan = 1.1547/a = 2/goz   ->  L_iplik = 2*A/goz
"""
import numpy as np


def altigen_ag(R, goz):
    """Yaricapi R olan diske sigan bal petegi kafes.

    Donus: (P, E, cevre_dugum)
      P : (n,3) dugum konumlari, z=0 duzleminde
      E : (m,2) komsu dugum ciftleri (iplik elemanlari)
      cevre : dis cevredeki dugum indisleri (yaricapa gore sirali)
    """
    a = goz / np.sqrt(3.0)                       # bag (kenar) boyu
    a1 = a * np.array([1.5,  np.sqrt(3) / 2])
    a2 = a * np.array([1.5, -np.sqrt(3) / 2])
    baz = [np.zeros(2), np.array([a, 0.0])]      # hucre basina 2 dugum

    n = int(np.ceil(R / (a * 1.5))) + 2
    pts = []
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            o = i * a1 + j * a2
            for b in baz:
                p = o + b
                if p[0] * p[0] + p[1] * p[1] <= R * R:
                    pts.append(p)
    P2 = np.array(pts)
    # yinelenenleri at (kayan nokta toleransi)
    anah = np.round(P2 / (a * 1e-3)).astype(np.int64)
    _, tek = np.unique(anah, axis=0, return_index=True)
    P2 = P2[np.sort(tek)]

    # --- komsuluk: bal peteginde her dugumun 3 bagi var, uzunluk = a
    from scipy.spatial import cKDTree
    agac = cKDTree(P2)
    ciftler = agac.query_pairs(a * 1.05, output_type='ndarray')
    E = ciftler[np.argsort(ciftler[:, 0])]

    # --- ASILI dugumleri bud: kenarda tek bagli dugumler ag gibi davranmaz
    while True:
        derece = np.bincount(E.ravel(), minlength=len(P2))
        # DIKKAT: yalnizca derece==1 budanir. derece==0 olanlar zaten
        # hicbir kenarda degil; onlari da secersek dongu bitmez.
        kotu = np.where(derece == 1)[0]
        if len(kotu) == 0:
            break
        tut = ~np.isin(E, kotu).any(axis=1)
        E = E[tut]
    kalan = np.unique(E)
    yeni = -np.ones(len(P2), np.int64); yeni[kalan] = np.arange(len(kalan))
    P2, E = P2[kalan], yeni[E]

    P = np.zeros((len(P2), 3)); P[:, :2] = P2
    rr = np.linalg.norm(P2, axis=1)
    cevre = np.where(rr > rr.max() - 1.2 * a)[0]
    return P, E, cevre


def bilye_dugumleri(P, cevre, n_bilye=6):
    """Cevre dugumlerinden esit acili n tanesini bilye olarak sec."""
    th = np.arctan2(P[cevre, 1], P[cevre, 0])
    hedef = np.arange(n_bilye) * 2 * np.pi / n_bilye - np.pi
    sec = [cevre[int(np.argmin(np.abs(np.angle(
        np.exp(1j * (th - h))))))] for h in hedef]
    return np.array(sorted(set(sec)))


def kare_ag(R, goz):
    """ALTIGEN DIS HATLI, KARE GOZLU ag -- imalat icin tercih edilen.

    Ayni goz acikligi ve AYNI IPLIK BOYU ile altigen kafesin 2.3 KATI AZ
    baglanti noktasi verir:
        kare    : A/goz^2          = 260
        altigen : 2A/((v3/2)goz^2) = 600
    Ustelik kare gozde ipler SUREKLIDIR (bir uctan obur uca tek parca);
    kesisme noktalari iki kesik ucu BIRLESTIREN dugum degil, sadece
    kaymayi onleyen baglardir -> surekli ip DUGUM KAYBINA UGRAMAZ.

    Yakalama garantisi korunur: kenari `goz` olan kare hucreye sigan en
    buyuk cember capi goz*sqrt(2) = 198 mm'dir; Talon pervanesi O230 mm
    oldugundan her zaman en az bir dugum kapsar.
    """
    a = goz
    n = int(np.ceil(R / a)) + 2
    i, j = np.meshgrid(np.arange(-n, n + 1), np.arange(-n, n + 1), indexing="ij")
    P2 = np.stack([i.ravel() * a, j.ravel() * a], axis=1)

    # altigen dis hat (cevrel yaricap R, kosesi +x'te): uc cift paralel kenar
    ap = R * np.sqrt(3) / 2.0
    ic = np.ones(len(P2), bool)
    for th in (np.pi/6, np.pi/2, 5*np.pi/6):
        ic &= np.abs(P2[:, 0]*np.cos(th) + P2[:, 1]*np.sin(th)) <= ap + 1e-9
    P2 = P2[ic]

    from scipy.spatial import cKDTree
    agac = cKDTree(P2)
    E = agac.query_pairs(a * 1.05, output_type='ndarray')
    E = E[np.argsort(E[:, 0])]

    while True:                      # asili dugumleri buda
        der = np.bincount(E.ravel(), minlength=len(P2))
        kotu = np.where(der == 1)[0]
        if len(kotu) == 0:
            break
        E = E[~np.isin(E, kotu).any(axis=1)]
    kalan = np.unique(E)
    yeni = -np.ones(len(P2), np.int64); yeni[kalan] = np.arange(len(kalan))
    P2, E = P2[kalan], yeni[E]

    P = np.zeros((len(P2), 3)); P[:, :2] = P2
    rr = np.linalg.norm(P2, axis=1)
    cevre = np.where(rr > rr.max() - 1.6 * a)[0]
    return P, E, cevre


def cevre_ipi_ekle(P, E, R, n_kenar=6):
    """ALTIGEN CEVRE HALATI ekler ve dis dugumleri ona baglar.

    Gercek aglarda gozler serbest kenarla bitmez: cevreyi dolasan bir
    HALAT (bolt rope) vardir, bilyeler ona baglanir ve yuku kenar boyunca
    dagitir. params.py'daki L_iplik formulunun `+6R` terimi tam olarak
    budur (altigen kenari = R, 6 kenar) -- ama topolojide eksikti.

    Donus: (P, E, bilye_dug) -- bilyeler halatin 6 KOSESINDEDIR.
    """
    from scipy.spatial import cKDTree
    a = np.median(np.linalg.norm(P[E[:, 1]] - P[E[:, 0]], axis=1))
    # halat dugumleri: altigen cevre boyunca ~a araliklarla
    kose = np.stack([R*np.cos(np.arange(6)*np.pi/3),
                     R*np.sin(np.arange(6)*np.pi/3)], axis=1)
    halat, kose_idx = [], []
    for k in range(6):
        p0, p1 = kose[k], kose[(k+1) % 6]
        n = max(int(round(np.linalg.norm(p1-p0)/a)), 1)
        kose_idx.append(len(halat))
        for s in range(n):
            halat.append(p0 + (p1-p0)*s/n)
    halat = np.array(halat)
    n0 = len(P)
    P = np.vstack([P, np.c_[halat, np.zeros(len(halat))]])
    yeni = [(n0+i, n0+(i+1) % len(halat)) for i in range(len(halat))]

    # ag dis dugumlerini en yakin halat dugumune bagla
    rr = np.linalg.norm(P[:n0, :2], axis=1)
    dis = np.where(rr > rr.max() - 1.5*a)[0]
    agac = cKDTree(halat)
    _, j = agac.query(P[dis, :2])
    yeni += [(int(i), int(n0+jj)) for i, jj in zip(dis, j)]

    E = np.vstack([E, np.array(yeni)])
    bilye = np.array([n0+k for k in kose_idx])
    return P, E, bilye
