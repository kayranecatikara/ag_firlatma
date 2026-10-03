#!/usr/bin/env python3
"""v9 — eldeki malzemelerle ag/boncuk/aci taramasi.
METRIK: ILK yerel tepe (ag serbest duserken yeniden yayilmasi SAYILMAZ).
"""
import os,sys,numpy as np,json
sys.path.insert(0,os.getcwd())
import run_menzil_nihai as M
from agsim.params import BILYE_MALZEME
from agsim.lastik import Bant, firlat_lastik
from agsim.hexag import kare_ag, cevre_ipi_ekle
from agsim.netfull import simule
K=json.load(open('out/v4_konfig.json'))
GEREK=1.718/2
def analiz(R,ts,Z):
    """ILK yerel tepe + o tepe etrafinda R>=GEREK olan z araligi."""
    dR=np.diff(R); neg=np.where(dR<0)[0]
    i=int(neg[0]) if len(neg) else int(np.argmax(R))
    if R[i]<GEREK: return i,R[i],np.nan,np.nan
    k=i
    while k>0 and R[k-1]>=GEREK: k-=1
    j=i
    while j<len(R)-1 and R[j+1]>=GEREK: j+=1
    return i,R[i],Z[k],Z[j]
def kos(Rag,goz,al,nb,G,Lkap=0.045,mkap=0.0385,T=0.35):
    P0,E0,_=kare_ag(Rag,goz); P0,E0,bd=cevre_ipi_ekle(P0,E0,Rag)
    De=9e-3*np.sqrt(nb); BILYE_MALZEME["_g"]=dict(rho=(nb*4e-3)/((np.pi/6)*De**3))
    t,_=M.kur(); t.ag.R_ag,t.ag.goz,t.ag.d_iplik=Rag,goz,0.60e-3
    t.bilye.malzeme,t.bilye.D="_g",De
    t.kapsul.alpha_cep=np.radians(al); t.kapsul.L_kap=Lkap; t.kapsul.m_kapsul=mkap
    b=Bant(n=4,OD=13e-3,ID=4e-3,L0=K['L0'],H=K['H'],Gmod=G)
    L=firlat_lastik(t,b,K['D_son']+K['strok'],K['strok'])
    S=simule(t,L,T=T,kayit=int(T*1500),topoloji=(P0,E0,bd))
    R,ts=np.array(S['R']),np.array(S['t'])
    Z=np.array([p[bd,2].mean() for p in S['P_snap']])
    i,Rt,lo,hi=analiz(R,ts,Z)
    Lip=float(np.linalg.norm(P0[E0[:,1]]-P0[E0[:,0]],axis=1).sum())
    return dict(v=L['v_exit'],F=L['F_kurma'],t=ts[i],Rt=Rt,lo=lo,hi=hi,Lip=Lip)
if __name__=="__main__":
    print(f"DUZELTILMIS METRIK: ilk yerel tepe, R>={GEREK:.3f} m (yari kanat) araligi")
    print(f"{'ag':>5} {'goz':>4} {'a':>4} {'nb':>3} {'Rtepe':>7} {'pay':>5} {'PENCERE z':>13} {'gen':>5} {'ip':>5}")
    en=None
    for Rag in (0.9,1.0,1.1,1.2):
        for goz in (0.20,0.22):
            for al in (25,30,35,40):
                for nb in (2,3):
                    r=kos(Rag,goz,al,nb,0.45e6)
                    if not np.isfinite(r['hi']): continue
                    g=r['hi']-r['lo']
                    print(f"O{2*Rag:4.1f} {goz*1e3:4.0f} {al:3.0f}d {nb:3d} {r['Rt']:7.3f} "
                          f"{r['Rt']/GEREK:4.2f}x {r['lo']:5.2f}–{r['hi']:5.2f} {g:5.2f} {r['Lip']:5.1f}")
                    if en is None or g>en[0]: en=(g,Rag,goz,al,nb,r)
    if en: print(f"\nEN GENIS PENCERE: O{2*en[1]:.1f} · goz {en[2]*1e3:.0f} · {en[3]}d · {en[4]} boncuk"
                 f" -> {en[5]['lo']:.2f}-{en[5]['hi']:.2f} m ({en[0]:.2f} m), R_tepe {en[5]['Rt']:.3f}")

def final():
    GEREK=1.718/2
    AD=[("A2  O2.2/220/30d/2bon  namlu O43.4",1.1,0.22,30,2,0.0385),
        ("C3  O2.2/220/25d/3bon  namlu O48",  1.1,0.22,25,3,0.0466),
        ("D3  O2.2/220/30d/3bon  namlu O51",  1.1,0.22,30,3,0.0526)]
    for ad,Rag,goz,al,nb,mk in AD:
        print(f"\n### {ad}   (boncuk {6*nb} ad = {6*nb*4} g)")
        print(f"{'Gmod':>6} {'F_kur':>7} {'v_exit':>7} {'R_tepe':>7} {'pay':>6} {'PENCERE':>13} {'gen':>5}")
        for G in (0.25e6,0.35e6,0.45e6,0.55e6,0.65e6):
            r=kos(Rag,goz,al,nb,G,mkap=mk)
            g=r['hi']-r['lo'] if np.isfinite(r['hi']) else float('nan')
            print(f"{G/1e6:5.2f}M {r['F']:6.0f}N {r['v']:6.1f} {r['Rt']:7.3f} "
                  f"{r['Rt']/GEREK:5.2f}x {r['lo']:5.2f}–{r['hi']:5.2f} {g:5.2f}"
                  f" {'OK' if r['Rt']>=GEREK and np.isfinite(r['hi']) else 'X'}")
