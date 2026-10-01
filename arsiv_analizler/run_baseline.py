"""Baseline analizi + temel grafikler."""
import sys; sys.path.insert(0,'/home/kayra/Masaüstü/ag_firlatma')
import numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from agsim.params import Tasarim
from agsim.launcher import firlat
from agsim.netrom import uc
from agsim.engagement import etkin_menzil
from agsim.aero import balistik_uzunluk, CdA_ag_acik, goreli_menzil_max

def kur(**kw):
    t = Tasarim()
    for k,v in kw.items():
        o,a = k.split('.'); setattr(getattr(t,o),a,v)
    return t

DUZ = dict()
IYI = {"kapsul.alpha_cep": np.radians(25), "bilye.D":12.6e-3,
       "bilye.malzeme":"Tungsten", "ag.R_ag":0.9, "ag.goz":0.090,
       "ag.d_iplik":0.20e-3, "namlu.L_namlu":0.300, "yay.L_serbest":0.260,
       "yay.x0":0.180, "yay.n_aktif":22.0}

fig, ax = plt.subplots(2, 2, figsize=(13, 9))
for ad, kw, c in [("Mevcut CAD tasarimi", DUZ, "tab:red"),
                  ("Duzeltilmis tasarim", IYI, "tab:blue")]:
    t = kur(**kw); L = firlat(t); F = uc(t, L)
    ax[0,0].plot(F["t"]*1e3, F["R"], c, label=f"{ad}  (v={L['v_exit']:.0f} m/s)")
    ax[0,1].plot(F["t"]*1e3, F["dx"], c, label=ad)
    ax[1,0].plot(F["dx"], F["R"], c, label=ad)
ax[0,0].axhline(0.75, ls="--", c="k", lw=1, label="gerekli yaricap (1.5 m kanat)")
ax[0,0].set(xlabel="zaman [ms]", ylabel="ag acilma yaricapi R [m]",
            title="(a) Ag acilmasi  -  sonra KAPANIYOR")
ax[0,1].axhline(0, ls=":", c="k", lw=1)
ax[0,1].set(xlabel="zaman [ms]", ylabel="drone'a gore ileri mesafe [m]",
            title="(b) 100 km/h'te ag geri supuruluyor")
ax[1,0].axhline(0.75, ls="--", c="k", lw=1)
ax[1,0].set(xlabel="drone'a gore mesafe [m]", ylabel="R [m]",
            title="(c) Angajman zarfi:  R >= 0.75 m olan mesafe = ETKIN MENZIL")
for a in ax.flat[:3]: a.legend(fontsize=8); a.grid(alpha=.3)

# (d) etkin menzil haritasi: cikis hizi x balistik uzunluk
vv = np.linspace(10, 80, 60); ll = np.linspace(1, 60, 60)
VV, LL = np.meshgrid(vv, ll)
DX = np.vectorize(goreli_menzil_max)(VV, 100/3.6, LL)
cs = ax[1,1].contourf(VV, LL, DX, levels=np.arange(0,16,1), cmap="viridis")
ax[1,1].contour(VV, LL, DX, levels=[2,5,10], colors="w", linewidths=1.2)
plt.colorbar(cs, ax=ax[1,1], label="ulasilabilir ileri mesafe [m]")
for ad, kw, m in [("mevcut", DUZ, "rX"), ("duzeltilmis", IYI, "b*")]:
    t = kur(**kw); L = firlat(t)
    lam = balistik_uzunluk(t.m_ucan, CdA_ag_acik(t.ag.R_ag, t.ag.solidite))
    ax[1,1].plot(L["v_exit"], lam, m, ms=14, label=f"{ad} (acik ag)")
ax[1,1].set(xlabel="namlu cikis hizi [m/s]",
            ylabel=r"balistik uzunluk $\lambda=2m/(\rho C_d A)$ [m]",
            title="(d) 100 km/h'te ULASILABILIR MENZIL  (kapali form)")
ax[1,1].legend(fontsize=8)
plt.tight_layout(); plt.savefig("out/baseline.png", dpi=130)
print("-> out/baseline.png")

print(f"\n{'':32s} {'v_cik':>7} {'lambda_acik':>12} {'R_eff':>7}")
for ad, kw in [("Mevcut CAD", DUZ), ("Duzeltilmis", IYI)]:
    t = kur(**kw); L = firlat(t); F = uc(t, L)
    lam = balistik_uzunluk(t.m_ucan, CdA_ag_acik(t.ag.R_ag, t.ag.solidite))
    print(f"{ad:32s} {L['v_exit']:7.1f} {lam:12.2f} {etkin_menzil(F,0.75):7.2f}")
