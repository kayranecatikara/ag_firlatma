#!/usr/bin/env python3
"""AG ORME KILAVUZU — tezgahta kullanilacak olculu cizim."""
import os, sys
_K=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,_K)
import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch
from agsim.hexag import kare_ag, cevre_ipi_ekle

R, G = 0.9, 0.22
INK,INK2,GRID = "#0b0b0b","#55534f","#d6d4d0"
MESH,HALAT,BILYE,OLC = "#2a78d6","#1baf7a","#2b2b2b","#eb6834"
plt.rcParams.update({"figure.facecolor":"#fcfcfb","axes.facecolor":"#fcfcfb",
  "text.color":INK,"font.size":9.5})

P,E,_ = kare_ag(R,G)
xs = np.unique(np.round(P[:,0]/G).astype(int))*G
ys = np.unique(np.round(P[:,1]/G).astype(int))*G
kose = np.stack([R*np.cos(np.arange(7)*np.pi/3), R*np.sin(np.arange(7)*np.pi/3)],1)

fig = plt.figure(figsize=(17.5,10.2))
gs = fig.add_gridspec(2,3, width_ratios=[2.0,1,1], height_ratios=[1,1],
                      hspace=.22, wspace=.20)

# ================= ANA PLAN =================
a = fig.add_subplot(gs[:,0]); a.set_aspect('equal')
a.plot(kose[:,0],kose[:,1],color=HALAT,lw=4.0,solid_joinstyle='round',zorder=3)
for v in ys:
    m=np.abs(P[:,1]-v)<1e-6
    if m.sum()>1: k=P[m][:,0]; a.plot([k.min(),k.max()],[v,v],color=MESH,lw=1.7,zorder=2)
for v in xs:
    m=np.abs(P[:,0]-v)<1e-6
    if m.sum()>1: k=P[m][:,1]; a.plot([v,v],[k.min(),k.max()],color=MESH,lw=1.7,zorder=2)
a.plot(P[:,0],P[:,1],'o',color=MESH,ms=4.5,mec='white',mew=.9,zorder=4)
for k in kose[:6]:
    a.add_patch(Circle(k,0.045,fc=BILYE,ec='white',lw=1.5,zorder=5))
# olculer
a.annotate("",(kose[0,0],kose[0,1]),(kose[3,0],kose[3,1]),
           arrowprops=dict(arrowstyle='<->',color=OLC,lw=1.4))
a.text(0,.055,"Ø1800  (köşeden köşeye)",color=OLC,fontweight='bold',ha='center',fontsize=10)
a.annotate("",(-0.66,-0.98),(-0.44,-0.98),arrowprops=dict(arrowstyle='<->',color=OLC,lw=1.3))
a.text(-0.55,-1.045,"220",color=OLC,fontweight='bold',ha='center',fontsize=9.5)
a.annotate("",(kose[0]*1.0),(kose[1]*1.0),arrowprops=dict(arrowstyle='<->',color=OLC,lw=1.3))
a.text(0.70,0.47,"900",color=OLC,fontweight='bold',rotation=-60,fontsize=9.5)
a.text(0,1.08,"AĞ ÖRME PLANI — 1:1 kurulum için ölçüler mm",
       ha='center',fontweight='bold',fontsize=13)
a.plot([],[],color=MESH,lw=1.7,label="göz ipi — Ø0.60 mm, SÜREKLİ (kesme!)")
a.plot([],[],color=HALAT,lw=4,label="çevre halatı — aynı ip, 5.4 m")
a.plot([],[],'o',color=BILYE,ms=9,label="bilye 2 × Ø8 (8 g) — 6 köşe")
a.legend(loc='lower center',bbox_to_anchor=(.5,-.17),frameon=False,fontsize=9.5,ncol=1)
a.set_xlim(-1.15,1.15); a.set_ylim(-1.2,1.15); a.axis('off')

# ================= IP LISTESI =================
b = fig.add_subplot(gs[0,1]); b.axis('off')
b.text(0,1.0,"① İP KESİM LİSTESİ",fontweight='bold',fontsize=11.5,va='top')
sat=["  YATAY (y sabit)      boy","  ───────────────────────"]
for v in ys:
    m=np.abs(P[:,1]-v)<1e-6
    if m.sum()>1:
        k=P[m][:,0]; sat.append(f"   y = {v*1e3:+5.0f}        {(k.max()-k.min())*1e3:5.0f} mm")
sat += ["","  DİKEY (x sabit)      boy","  ───────────────────────"]
for v in xs:
    m=np.abs(P[:,0]-v)<1e-6
    if m.sum()>1:
        k=P[m][:,1]; sat.append(f"   x = {v*1e3:+5.0f}        {(k.max()-k.min())*1e3:5.0f} mm")
b.text(0,.93,"\n".join(sat),va='top',family='monospace',fontsize=8.6)
b.text(0,.055,"14 hat · 15.0 m\n+ her ucta 80 mm bağlama payı\n→ 16.2 m kes",
       va='top',fontsize=9.3,color=OLC,fontweight='bold')

# ================= KESISIM BAGI =================
c = fig.add_subplot(gs[0,2]); c.set_aspect('equal'); c.axis('off')
c.text(.5,1.02,"② KESİŞİM BAĞI  (41 adet)",fontweight='bold',fontsize=11.5,
       ha='center',transform=c.transAxes)
c.plot([-1,1],[0,0],color=MESH,lw=3.5); c.plot([0,0],[-1,1],color=MESH,lw=3.5)
th=np.linspace(0,2*np.pi,200)
for rr,ph in ((.26,0),(.33,.5),(.40,1.0)):
    c.plot(rr*np.cos(th+ph)*1.5, rr*np.sin(th+ph), color=OLC,lw=1.6)
c.text(0,-1.35,"İki ip ÜST ÜSTE, kesilmez.\nAyrı 150 mm'lik ince bağ ipiyle\nçapraz sar (3+3 tur),\niki yarım düğüm, 2 mm bırak kes.\nÜstüne 1 damla japon yapıştırıcı.",
       ha='center',fontsize=9.2,va='top')
c.set_xlim(-1.2,1.2); c.set_ylim(-2.3,1.1)

# ================= CEVRE BAGI =================
d = fig.add_subplot(gs[1,1]); d.set_aspect('equal'); d.axis('off')
d.text(.5,1.02,"③ ÇEVRE BAĞI  (24 adet)",fontweight='bold',fontsize=11.5,
       ha='center',transform=d.transAxes)
d.plot([-1.3,1.3],[.75,.75],color=HALAT,lw=6)
d.plot([0,0],[-.9,.75],color=MESH,lw=3)
for i,yy in enumerate(np.linspace(.60,.90,4)):
    d.plot(np.linspace(-.22,.22,30), yy+.05*np.sin(np.linspace(0,np.pi,30)),
           color=MESH,lw=1.4)
d.text(0,-1.15,"Mesh ipini DÜĞÜMLEME —\nhalatın etrafına 3-4 TUR SAR,\nsonra kendi üstüne iki yarım düğüm.\n\nDüğümlü uç 245 N, sarılmış uç ~400 N\ntaşır. Ölçülen tepe yük ~17 N.",
       ha='center',fontsize=9.2,va='top')
d.set_xlim(-1.4,1.4); d.set_ylim(-2.4,1.1)

# ================= BILYE =================
e = fig.add_subplot(gs[1,2]); e.set_aspect('equal'); e.axis('off')
e.text(.5,1.02,"④ BİLYE BAĞI  (6 köşe)",fontweight='bold',fontsize=11.5,
       ha='center',transform=e.transAxes)
e.plot([-1.25,.35],[.6,.6],color=HALAT,lw=6)
e.plot([.35,.95],[.6,.1],color=MESH,lw=2.6)
e.add_patch(Circle((1.02,.02),.17,fc=BILYE,ec='white',lw=1.4))
e.add_patch(Circle((1.22,-.14),.17,fc=BILYE,ec='white',lw=1.4))
e.annotate("",(.40,.56),(.92,.10),arrowprops=dict(arrowstyle='<->',color=OLC,lw=1.3))
e.text(.52,.18,"40 mm",color=OLC,fontweight='bold',fontsize=9.3)
e.text(0,-.85,"Her köşeye 2 × Ø8 bilye (toplam 8 g).\nİp bilyelerin deliğinden geçer,\ndışta figure-8 durdurma düğümü.\nHalat köşesine 40 mm serbest boyla bağla.\n\nTOPLAM 12 BİLYE.",
       ha='center',fontsize=9.2,va='top')
e.set_xlim(-1.4,1.6); e.set_ylim(-2.3,1.0)

fig.suptitle("AĞ ÖRME KILAVUZU — Ø1.8 m · kare göz 220 mm · Dyneema Ø0.60 mm (eldeki ip)",
             fontsize=14.5,fontweight='bold',x=.035,ha='left',y=.985)
fig.text(.035,.012,"TOPLAM: 25.8 m iplik (elinde 90 m) · 65 bağ · ~1.1 saat   |   "
         "kesişim 41 + çevre 24   |   ağ 7.1 g + bilye 48 g",
         fontsize=10,color=INK2)
plt.savefig(os.path.join(_K,"out","AG_ORME_KILAVUZU.png"),dpi=125,
            bbox_inches='tight',facecolor="#fcfcfb")
print("-> out/AG_ORME_KILAVUZU.png")
