"""Tasarim uzayi kesfi: Sobol taramasi + duyarlilik + Pareto + optimizasyon."""
import sys, time, json
sys.path.insert(0, '/home/kayra/Masaüstü/ag_firlatma')
import numpy as np, pandas as pd
from scipy.stats import spearmanr
from scipy.optimize import differential_evolution
from agsim.dse import (sobol_ornekle, degerlendir_vektor, pareto_front,
                       ADLAR, ALT, UST, BILYE_SET)

N_LOG2 = 12
t0 = time.time()
X = sobol_ornekle(N_LOG2, seed=7)
R = [degerlendir_vektor(x) for x in X]
df = pd.DataFrame(R)
for i, a in enumerate(ADLAR):
    df[a] = X[:, i]
df["mlz"] = [BILYE_SET[int(v)] for v in df["mlz_bilye"]]
print(f"[1] Sobol {len(X)} tasarim, {time.time()-t0:.1f} s, "
      f"uygun oran %{100*df.uygun.mean():.1f}")

U = df[df.uygun].copy()
print(f"\n[2] UYGUN TASARIMLAR (n={len(U)})")
print(U[["R_eff","v_exit","v_radyal","E_depo","J_geri","m_sistem","F_sok"]]
      .describe().loc[["min","50%","max"]].round(3).to_string())

print("\n[3] DUYARLILIK  (Spearman rho, R_eff ile)")
for a in ADLAR:
    rho, p = spearmanr(U[a], U["R_eff"])
    bar = "#"*int(abs(rho)*40)
    print(f"   {a:11s} rho={rho:+.3f} p={p:7.1e}  {bar}")
print("   malzemeye gore ortalama R_eff:")
print(U.groupby("mlz")["R_eff"].agg(["mean","max","count"]).round(3).to_string())

print("\n[4] PARETO FRONTU  (R_eff max / E_depo min / m_sistem min)")
F = U[["R_eff","E_depo","m_sistem"]].values
msk = pareto_front(F, [+1,-1,-1])
P = U[msk].sort_values("R_eff", ascending=False)
print(f"   baskin olmayan tasarim sayisi: {msk.sum()}")
kol = ["R_eff","E_depo","m_sistem","J_geri","v_exit","v_radyal","D_bore",
       "L_namlu","D_bilye","mlz","alpha_deg","R_ag","goz","d_iplik"]
print(P[kol].head(12).round(4).to_string(index=False))

print("\n[5] OPTIMIZASYON: R_eff maksimize (differential_evolution)")
E_BUT, M_BUT = 120.0, 1.2      # enerji [J] ve sistem kutlesi [kg] butcesi
def amac(x):
    d = degerlendir_vektor(x)
    if not d["uygun"]:
        return 10.0
    ceza = (max(0, d["E_depo"]-E_BUT)/E_BUT + max(0, d["m_sistem"]-M_BUT)/M_BUT)
    return -d["R_eff"] + 5.0*ceza

res = differential_evolution(amac, list(zip(ALT, UST)), seed=3, maxiter=160,
                             popsize=26, tol=1e-8, polish=False, init='sobol',
                             mutation=(0.4,1.0), recombination=0.85)
opt = degerlendir_vektor(res.x)
print(f"   R_eff = {opt['R_eff']:.2f} m")
print("   tasarim:")
for a, v in zip(ADLAR, res.x):
    if a == "mlz_bilye":
        print(f"     {a:11s} = {BILYE_SET[int(v)]}")
    elif a == "twist_inv":
        print(f"     yiv_adimi   = {'duz (yiv yok)' if v<0.5 else f'{1000/v:.0f} mm/tur'}")
    else:
        print(f"     {a:11s} = {v:.5g}")
print("   metrikler:", {k: round(float(opt[k]),4) for k in
      ["v_exit","v_radyal","E_depo","J_geri","m_sistem","m_ucan","m_ag",
       "F_sok","F_max","verim","t_acilma","kopma_SF","strok","L_kapsul","SF_gerilme"]})

df.to_csv("out/sobol.csv", index=False)
P.to_csv("out/pareto.csv", index=False)
np.save("out/x_opt.npy", res.x)
print("\n-> out/sobol.csv, out/pareto.csv, out/x_opt.npy yazildi")
