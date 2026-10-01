"""Agin 3B yolu ve sekli: ram-hava konisi, acilma-kapanma salinimi, atis penceresi."""
import sys; sys.path.insert(0,'/home/kayra/Masaüstü/ag_firlatma')
import numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

S1, S2, S3 = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#d8d7d2"
RAMP = LinearSegmentedColormap.from_list("m", ["#a8c8ee", "#2a78d6", "#12365f"])
plt.rcParams.update({"figure.facecolor":"#fcfcfb", "axes.facecolor":"#fcfcfb",
    "axes.edgecolor":GRID, "axes.labelcolor":INK, "text.color":INK,
    "xtick.color":INK2, "ytick.color":INK2, "grid.color":GRID, "font.size":9,
    "axes.titlesize":10})

D = np.load('out/sim3d.npz')
ts, P, E, bd = D['t'], D['P'], D['E'], D['bd']
R_ag, V_d, v_ex = float(D['R_ag']), float(D['V_drone']), float(D['v_exit'])
R  = np.array([np.linalg.norm(p[bd,:2],axis=1).mean() for p in P])
Z  = np.array([p[bd,2].mean() for p in P])
Zc = np.array([p[0,2] for p in P])
R_ger = 0.75
_d = np.diff(R); i_max = int(np.argmax(_d < 0)) if (_d<0).any() else int(np.argmax(R))
i_cok = i_max + int(np.argmin(R[i_max:]))
m = (R >= R_ger) & (np.arange(len(R)) <= i_cok)
ANLAR = [0.015, 0.040, 0.070, 0.100, 0.150]

fig = plt.figure(figsize=(15.5, 9.6))
gs = fig.add_gridspec(2, 3, height_ratios=[1.25, 1], hspace=.34, wspace=.24,
                      left=.045, right=.985, top=.90, bottom=.07)

# ---------- (a) 3B ------------------------------------------------------------
ax = fig.add_subplot(gs[0, :2], projection='3d')
for k, tt in enumerate(ANLAR):
    i = np.argmin(abs(ts-tt)); p = P[i]; c = RAMP(k/(len(ANLAR)-1))
    seg = np.stack([p[E[:,0]], p[E[:,1]]], 1)
    for a, b in seg:
        ax.plot([a[2],b[2]], [a[0],b[0]], [a[1],b[1]], color=c, lw=.4, alpha=.65)
    ax.scatter(p[bd,2], p[bd,0], p[bd,1], color=c, s=34, depthshade=False,
               edgecolors="white", linewidths=.6, zorder=5)
    ax.text(p[bd,2].mean(), 0, -2.25, f"{tt*1e3:.0f} ms", color=c, fontsize=10,
            fontweight="bold", ha="center")
ax.set_xlabel("drone'a göre ileri mesafe  z [m]", labelpad=14)
ax.set_ylabel("x [m]", labelpad=4); ax.set_zlabel("y [m]", labelpad=2)
ax.set_box_aspect((2.9, 1, 1)); ax.view_init(16, -66)
ax.set_zlim(-1.8, 1.8); ax.set_ylim(-1.8, 1.8)
ax.set_yticks([-1.5, 0, 1.5]); ax.set_zticks([-1.5, 0, 1.5])
ax.tick_params(labelsize=8, pad=-1)
ax.set_title("(a) Ağın 3B yolu ve şekli — bilyeler önde, ağ arkada koni oluşturuyor",
             loc="left", fontweight="bold", pad=-6)
ax.grid(False)
for a_ in (ax.xaxis, ax.yaxis, ax.zaxis): a_.pane.set_alpha(.02)

# ---------- (b) yan kesit: ram-hava konisi ------------------------------------
ax = fig.add_subplot(gs[0, 2])
# dugumleri halkalara ayir (merkez=0, sonra n_spoke'luk bloklar)
nN = P.shape[1]; nS = len(bd)*3          # n_spoke = 18
n_ring = (nN-1)//nS
for k, tt in enumerate(ANLAR[1:]):
    i = np.argmin(abs(ts-tt)); p = P[i]; c = RAMP(k/3)
    dz_h, r_h = [p[0,2]-p[bd,2].mean()], [0.0]
    for ring in range(1, n_ring+1):
        sl = slice(1+(ring-1)*nS, 1+ring*nS)
        r_h.append(float(np.hypot(p[sl,0], p[sl,1]).mean()))
        dz_h.append(float(p[sl,2].mean() - p[bd,2].mean()))
    dz_h, r_h = np.array(dz_h), np.array(r_h)
    ax.plot(np.r_[dz_h[::-1], dz_h], np.r_[-r_h[::-1], r_h], '-o', color=c,
            lw=1.8, ms=3.5, label=f"{tt*1e3:.0f} ms")
    ax.plot([dz_h[-1], dz_h[-1]], [-r_h[-1], r_h[-1]], 'o', color=c, ms=8,
            mec="white", mew=.8)
ax.axvline(0, color=GRID, lw=1.2)
ax.annotate("", xy=(-0.88, -1.62), xytext=(-0.18, -1.62),
            arrowprops=dict(arrowstyle="->", color=INK2, lw=1.4))
ax.text(-0.53, -1.50, "bağıl hava akışı", color=INK2, fontsize=8.5, ha="center")
ax.text(0.02, 1.58, "bilye\ndüzlemi", color=INK2, fontsize=8, ha="left", va="top")
ax.set(xlabel="bilye düzlemine göre geri kalma [m]", ylabel="yarıçap [m]",
       ylim=(-1.75, 1.75))
ax.set_title("(b) RAM-HAVA: hafif ağ geriye şişip\nkoni alıyor (paraşüt gibi)",
             loc="left", fontweight="bold")
ax.legend(fontsize=8, frameon=False, loc="upper left", ncol=2, columnspacing=1)
ax.grid(alpha=.3)

# ---------- (c) R(t) -----------------------------------------------------------
ax = fig.add_subplot(gs[1, 0])
ax.plot(ts*1e3, R, color=S1, lw=2.2, label="ağ yarıçapı R(t)")
ax.axhline(R_ger, color=S2, lw=2, ls="--", label=f"gerekli yarıçap {R_ger} m")
ax.axhline(R_ag, color=GRID, lw=1.4, ls=":")
ax.text(ts[-1]*1e3*.99, R_ag-.10, "ağın tam boyu", va="top", ha="right",
        fontsize=8, color=INK2)
ax.fill_between(ts*1e3, 0, R, where=m, color=S1, alpha=.12)
ax.plot(ts[i_max]*1e3, R[i_max], "o", color=S1, ms=9, mec="white", mew=1.4)
ax.annotate(f"en açık {R[i_max]:.2f} m @ {ts[i_max]*1e3:.0f} ms",
            xy=(ts[i_max]*1e3, R[i_max]), xytext=(ts[i_max]*1e3-95, R[i_max]+.26),
            fontsize=9, fontweight="bold", color=S1)
ax.set(xlabel="zaman [ms]", ylabel="ağ yarıçapı [m]", ylim=(0, 1.95))
ax.set_title("(c) Açılma bir SALINIM: iplikler gerilip\nbilyeleri geri fırlatıyor",
             loc="left", fontweight="bold")
ax.legend(fontsize=8, frameon=False, loc="lower center"); ax.grid(alpha=.3)

# ---------- (d) angajman zarfi -------------------------------------------------
ax = fig.add_subplot(gs[1, 1])
zi = Z[m]
ax.axvspan(zi.min(), zi.max(), color=S3, alpha=.15, lw=0)
ax.plot(Z[:i_cok+1], R[:i_cok+1], color=S1, lw=2.2, label="bilye halkası")
ax.plot(Z[i_cok:], R[i_cok:], color=GRID, lw=1.6, ls=":", label="çöküş sonrası")
ax.axhline(R_ger, color=S2, lw=2, ls="--", label=f"gerekli {R_ger} m")
ax.plot(Z[i_max], R[i_max], "o", color=S1, ms=9, mec="white", mew=1.4)
ax.text((zi.min()+zi.max())/2, .22, f"ATIŞ PENCERESİ\n{zi.min():.1f} – {zi.max():.1f} m",
        ha="center", fontsize=9.5, fontweight="bold", color="#0f6e4c")
ax.annotate(f"en açık\n{Z[i_max]:.1f} m", xy=(Z[i_max], R[i_max]),
            xytext=(Z[i_max]-1.9, R[i_max]+.22), fontsize=9, fontweight="bold",
            color=S1, arrowprops=dict(arrowstyle="->", color=S1, lw=1.3))
ax.set(xlabel="drone'a göre ileri mesafe [m]", ylabel="ağ yarıçapı [m]",
       xlim=(0, 8), ylim=(0, 1.95))
ax.set_title("(d) Hedefi BU aralıkta iken tetikle", loc="left", fontweight="bold")
ax.legend(fontsize=8, frameon=False, loc="upper right"); ax.grid(alpha=.3)

# ---------- (e) bilye vs merkez ------------------------------------------------
ax = fig.add_subplot(gs[1, 2])
ax.plot(ts*1e3, Z,  color=S1, lw=2.2, label="bilyeler  (ağır, λ≈234 m)")
ax.plot(ts*1e3, Zc, color=S2, lw=2.2, label="ağ merkezi (hafif, λ≈0.24 m)")
ax.fill_between(ts*1e3, Zc, Z, color=S2, alpha=.14)
k = np.argmin(abs(ts-.25))
ax.annotate("ram-hava\ngeri kalması", xy=(ts[k]*1e3, (Z[k]+Zc[k])/2),
            xytext=(105, 1.2), fontsize=9, color=INK2,
            arrowprops=dict(arrowstyle="->", color=INK2, lw=1.2))
ax.set(xlabel="zaman [ms]", ylabel="ileri mesafe [m]")
ax.set_title("(e) Ağır bilyeler hafif ağı peşinden çekiyor", loc="left",
             fontweight="bold")
ax.legend(fontsize=8, frameon=False, loc="upper left"); ax.grid(alpha=.3)

fig.suptitle(f"Ağ fırlatma — 3B kütle-yay-sönümleyici simülasyonu   "
             f"(100 km/h uçuş, v_çıkış {v_ex:.0f} m/s, Ø{2*R_ag:.1f} m ağ, 6×Ø12.9 mm bilye)",
             fontsize=13, fontweight="bold", x=.045, ha="left", y=.965)
plt.savefig("out/ag_3d.png", dpi=125)
print(f"-> out/ag_3d.png | R_max={R[i_max]:.2f} m @ {ts[i_max]*1e3:.0f} ms, z={Z[i_max]:.2f} m")
print(f"   ATIS PENCERESI {zi.min():.2f}-{zi.max():.2f} m ({(ts[m].max()-ts[m].min())*1e3:.0f} ms)")
