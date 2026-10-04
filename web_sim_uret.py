#!/usr/bin/env python3
"""Web gorsellestirmesi icin GERCEK firlatma simulasyonunu kosturur ve
ag dugumlerinin yorungesini disa aktarir -> web/sim.json

Animasyon uydurma degil: agsim/netfull.py'nin cozdugu ayni hareket.
Koordinat donusumu: sim'de +z menzil yonu, CAD'de +Y namlu ekseni.
  CAD_x = sim_x · CAD_y = namlu_agzi + sim_z · CAD_z = sim_y
"""
import os, sys, json
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_menzil_nihai as M                                   # noqa: E402
from agsim.params import BILYE_MALZEME                         # noqa: E402
from agsim.lastik import Bant, firlat_lastik                   # noqa: E402
from agsim.hexag import kare_ag, cevre_ipi_ekle                # noqa: E402
from agsim.netfull import simule                               # noqa: E402
from agsim.yollar import kyol                                  # noqa: E402

K = json.load(open(kyol("out", "v4_konfig.json")))
CAD = json.load(open(kyol("cad", "v4_olcu.json")))
GEREK = 1.718 / 2
GMOD = 0.45e6                      # bant sertligi VARSAYIM (olculmedi)
T_SON, FPS = 0.32, 300

Rag, goz, al, n_bant = K["R_ag"], K["goz"], K["alpha"], K["n_bant"]
P0, E0, _ = kare_ag(Rag, goz)
N_IC_DUGUM, N_IC_ELEMAN = P0.shape[0], E0.shape[0]   # kafes; otesi halat+radyal
P0, E0, bd = cevre_ipi_ekle(P0, E0, Rag)

De = K["D_boncuk"] * np.sqrt(K["n_boncuk"])
BILYE_MALZEME["_g"] = dict(
    rho=(K["n_boncuk"] * K["m_boncuk"]) / ((np.pi / 6) * De ** 3))

t, _ = M.kur()
t.ag.R_ag, t.ag.goz, t.ag.d_iplik = Rag, goz, K["d_ip"]
t.bilye.malzeme, t.bilye.D = "_g", De
t.kapsul.alpha_cep = np.radians(al)
t.kapsul.L_kap = K["L_kap"]
t.kapsul.m_kapsul = K["m_kap"]
b = Bant(n=n_bant, OD=K["bant_OD"], ID=4e-3,
         L0=K["L0"], H=K["H"], Gmod=GMOD)
L = firlat_lastik(t, b, K["L0"] + K["H"] + K["strok"], K["strok"])
S = simule(t, L, T=T_SON, kayit=int(T_SON * FPS), topoloji=(P0, E0, bd))

ts = np.array(S["t"])
R = np.array(S["R"])
AGIZ = CAD["L_namlu"]                      # mm, namlu agzi

# --- ilk yerel tepe: agin GERCEKTEN acildigi an ---
dR = np.diff(R)
neg = np.where(dR < 0)[0]
i_tepe = int(neg[0]) if len(neg) else int(np.argmax(R))

kareler = []
for p in S["P_snap"]:
    f = np.empty(p.shape[0] * 3, dtype=np.float32)
    f[0::3] = p[:, 0] * 1000.0                 # CAD x
    f[1::3] = AGIZ + p[:, 2] * 1000.0          # CAD y (menzil)
    f[2::3] = p[:, 1] * 1000.0                 # CAD z
    kareler.append([round(float(v), 1) for v in f])

# tasarim (gerilmemis) kafes: gerinim renklendirmesi ve "hedef ag" hayaleti
tasarim = np.empty(P0.shape[0] * 3)
tasarim[0::3] = P0[:, 0] * 1000.0
tasarim[1::3] = AGIZ + P0[:, 2] * 1000.0
tasarim[2::3] = P0[:, 1] * 1000.0
boy0 = np.linalg.norm(P0[E0[:, 1]] - P0[E0[:, 0]], axis=1) * 1000.0

veri = {
    "_not": "agsim/netfull.py cozumu — animasyon gercek simulasyon verisi",
    "gmod_varsayim": GMOD / 1e6,
    "bant_sayisi": n_bant,
    "v_cikis": round(float(L["v_exit"]), 2),
    "F_kurma": round(float(L["F_kurma"]), 0),
    "E_depo": round(float(L["E_depo"]), 2),
    "gerek_R": round(GEREK, 3),
    "agiz_y": AGIZ,
    "strok": CAD["STROK"],
    "dugum": int(P0.shape[0]),
    "n_ic_dugum": int(N_IC_DUGUM),
    "n_ic_eleman": int(N_IC_ELEMAN),
    "eleman": [[int(a), int(c)] for a, c in E0],
    "bilye_dugum": [int(x) for x in bd],
    "t_ms": [round(float(x) * 1000, 2) for x in ts],
    "R_m": [round(float(x), 4) for x in R],
    "T_max_N": [round(float(x), 2) for x in S["T_max"]],
    "i_tepe": i_tepe,
    "R_tepe": round(float(R[i_tepe]), 3),
    "kareler": kareler,
    "dugum_tasarim": [round(float(v), 1) for v in tasarim],
    "eleman_boy0": [round(float(v), 2) for v in boy0],
}
yol = kyol("web", "sim.json")
os.makedirs(os.path.dirname(yol), exist_ok=True)
json.dump(veri, open(yol, "w"), separators=(",", ":"))
kb = os.path.getsize(yol) / 1024
print(f"v_cikis {L['v_exit']:.1f} m/s · F_kurma {L['F_kurma']:.0f} N · "
      f"{n_bant} bant · Gmod {GMOD/1e6:.2f} MPa")
print(f"ag acilma tepesi: t={ts[i_tepe]*1000:.0f} ms · R={R[i_tepe]:.3f} m "
      f"(gerekli {GEREK:.3f}) · pay {R[i_tepe]/GEREK:.2f}x")
print(f"{len(kareler)} kare · {P0.shape[0]} dugum · {len(E0)} eleman "
      f"-> web/sim.json ({kb:.0f} kB)")
