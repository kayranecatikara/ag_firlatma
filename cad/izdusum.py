# -*- coding: utf-8 -*-
"""Basit ortografik ucgen-mesh isleyici (ressam algoritmasi).

mplot3d uzun/ince parcalarda cerceveyi dolduramadigi ve derinlik siralamasini
dogru yapamadigi icin projeksiyonu kendimiz yapiyoruz.
"""
import numpy as np
import matplotlib
from matplotlib.collections import PolyCollection


def kamera(elev_deg, azim_deg):
    el, az = np.radians(elev_deg), np.radians(azim_deg)
    d = np.array([np.cos(el) * np.cos(az), np.cos(el) * np.sin(az), np.sin(el)])
    up = np.array([0.0, 0.0, 1.0])
    r = np.cross(d, up)
    if np.linalg.norm(r) < 1e-9:
        r = np.array([1.0, 0.0, 0.0])
    r /= np.linalg.norm(r)
    u = np.cross(r, d)
    return d, r, u


def ciz(ax, parcalar, elev=20, azim=-60, isik=(0.4, -0.6, 0.7), kenar=None):
    """parcalar: [(v, f, renk), ...]  v: (N,3) CAD koordinati, f: (M,3)"""
    d, r, u = kamera(elev, azim)
    L = np.array(isik, float); L /= np.linalg.norm(L)
    T, C, Z = [], [], []
    for v, f, renk in parcalar:
        tri = v[f]
        n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
        ln = np.linalg.norm(n, axis=1, keepdims=True); ln[ln == 0] = 1
        n = n / ln
        gor = n @ d > 0                      # yalnizca kameraya bakan yuzler
        tri, n = tri[gor], n[gor]
        if len(tri) == 0:
            continue
        sh = np.clip(n @ L, 0, 1) * 0.58 + 0.42
        base = np.array(matplotlib.colors.to_rgb(renk))
        T.append(np.stack([tri @ r, tri @ u], -1))
        C.append(np.clip(base * sh[:, None], 0, 1))
        Z.append((tri @ d).mean(1))
    if not T:
        return
    T = np.concatenate(T); C = np.concatenate(C); Z = np.concatenate(Z)
    o = np.argsort(Z)                        # uzaktan yakina
    ax.add_collection(PolyCollection(T[o], facecolors=C[o],
                                     edgecolors=kenar or "none",
                                     linewidths=.15 if kenar else 0))
    P = T.reshape(-1, 2)
    ax.set_xlim(P[:, 0].min(), P[:, 0].max())
    ax.set_ylim(P[:, 1].min(), P[:, 1].max())
    ax.set_aspect("equal")
    ax.axis("off")
