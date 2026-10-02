#!/usr/bin/env python3
"""Ag + hedef + dunya SDF'lerini URETIR — topoloji agsim/netfull.py'dan gelir.

Boylece Gazebo modeli ile Python modeli AYNI agi kullanir; sonuclar
dogrudan karsilastirilabilir.

Kullanim:
    python3 gazebo/scripts/ag_sdf_uret.py
Cikti:
    gazebo/worlds/ag_atis.sdf
"""
import sys, os, json
KOK = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, KOK)
import numpy as np
from agsim.params import Ag, Bilye
from agsim.netfull import orumcek_ag
from agsim.hexag import altigen_ag, kare_ag, cevre_ipi_ekle, bilye_dugumleri

# ------------------------------------------------------------------ tasarim
K = json.load(open(os.path.join(KOK, "out", "v4_konfig.json")))
R_AG = float(os.environ.get("AG_RAG", K["R_ag"]))
GOZ  = float(os.environ.get("AG_GOZ", K["goz"]))
# iplik capi ortam degiskeniyle taranabilir (menzil/kesilme odunlesmesi)
D_IP = float(os.environ.get("AG_DIP", K["d_ip"]))
ALPHA = np.radians(K["alpha"])
# --- cozunurluk / kosu anahtarlari (ortam degiskeniyle degistirilebilir)
N_RING  = int(os.environ.get("AG_NRING", 5))
N_SPOKE = int(os.environ.get("AG_NSPOKE", 12))
# CARPISMA=0 -> dugum/hedef carpisma geometrisi YOK (sadece ag dinamigi; hizli
#               DOGRULAMA kosusu, Python ile birebir karsilastirma icin)
# CARPISMA=1 -> temas + hedef var (YAKALAMA/dolanma kosusu)
CARPISMA = os.environ.get("AG_CARPISMA", "1") != "0"
# HEDEF: Talon modeli dunyaya konsun mu (CARPISMA'dan BAGIMSIZ)
HEDEF_VAR = os.environ.get("AG_HEDEF", "1" if CARPISMA else "0") != "0"
# FIRLATICI: monte edilebilir model paketini dunyaya ekle ve agi onun
#   AGZINDA dogur. Ag, atisa kadar firlaticiyla birlikte KINEMATIK tasinir.
FIRLATICI = os.environ.get("AG_FIRLATICI", "0") != "0"
# TETIK: "zamanli" (firlatma_t) | "harici" (gz topic)
TETIK = os.environ.get("AG_TETIK", "zamanli")
TETIK_KONU = os.environ.get("AG_TETIK_KONU", "/ag_firlatici/ates")
# ORGU: "orumcek" = kaba halka/parmaklik (hizli, ag ACILMASI icin yeterli)
#       "hex"     = GERCEK altigen kafes, goz = 140 mm
#   DOLANMA ancak "hex" ile gorunur: kaba orgunun goz acikligi 0.73 m iken
#   hedefin govdesi 0.085 m'dir, ag aradan gecip gider.
#       "kare"    = GERCEK kare goz + CEVRE HALATI  <- URETILECEK TASARIM
ORGU = os.environ.get("AG_ORGU", "orumcek")
# DEVIR ANI [s]: agin KAPSULDEN CIKISI rijit-cisim temas problemi degildir --
# paketli halde 709 carpisma kuresi 16 mm'lik hazneye tikilidir ve DART'in
# LCP cozucusu yuz binlerce temasla coker. Cozum HIBRIT:
#   * paketten acilma  -> DOGRULANMIS Python modeli (netfull, hex topoloji)
#   * temas/dolanma    -> Gazebo, agi ACIK halde devralir
# AG_DEVIR=0 -> devir yok, eski davranis (kapsulden firlat).
DEVIR = float(os.environ.get("AG_DEVIR",
                             "0.08" if ORGU in ("hex", "kare") else "0"))

V_EKS = 34.504                    # namlu cikis hizi [m/s]  (NIHAI analiz)
V_RAD_CEP = 7.966                 # bilye radyal acilma hizi [m/s] (cep acisi)
V_DRONE = 100 / 3.6
MENZIL0 = float(os.environ.get("AG_MENZIL", "4.65"))  # hedef mesafesi [m]
# hedef (X-UAV Talon) geometrisi -- plugin blogu da kullandigi icin BURADA
KANAT, GOVDE_L, PERVANE = 1.718, 0.90, 0.230
FIRLATMA_T = 0.02                 # sim basladiktan sonra atis ani [s]

ag = Ag(R_ag=R_AG, goz=GOZ, d_iplik=D_IP, n_ring=N_RING, n_spoke=N_SPOKE)
bilye = Bilye(malzeme="Kursun", D=0.0127)
if ORGU == "kare":
    P0, E, _c = kare_ag(R_AG, GOZ)
    P0, E, BILYE_DUG = cevre_ipi_ekle(P0, E, R_AG)   # bilyeler halat kosesinde
elif ORGU == "hex":
    P0, E, _cevre = altigen_ag(R_AG, GOZ)
    BILYE_DUG = bilye_dugumleri(P0, _cevre)
else:
    P0, E, BILYE_DUG = orumcek_ag(N_RING, N_SPOKE, R_AG)
L0 = np.linalg.norm(P0[E[:, 1]] - P0[E[:, 0]], axis=1)
AERO_OLCEK = ag.L_iplik / L0.sum()      # kaba orgu -> gercek ag (hex'te ~1)

# dugum kutleleri: baglanan eleman boylarinin yarisiyla orantili
w = np.zeros(len(P0))
np.add.at(w, E[:, 0], 0.5 * L0); np.add.at(w, E[:, 1], 0.5 * L0)
M_DUG = ag.m_ag * w / w.sum()
M_BILYE = bilye.m
M_NOM = ag.m_ag / len(P0)              # Python'daki sonumleme olcegi
EA = ag.E_iplik * ag.E_olcek * ag.A_iplik
K_EL = EA / L0.min()                   # en sert eleman
DT_KARARLI = 2 * np.pi * np.sqrt(M_NOM / K_EL) / 15.0
DT = float(os.environ.get("AG_DT", f"{DT_KARARLI:.6f}"))

# --------------------------------------------------------- DEVIR (hibrit)
# Python -> Gazebo eksen donusumu (cevrimsel, sag el):
#   Gazebo (x ileri, y sag, z yukari)  =  Python (z ucus ekseni, x, y)
# Python tasarim nesnesi + firlatma cozumu (hem paket geometrisi hem devir icin)
import run_menzil_nihai as _M
_t, _L = _M.kur()
_t.ag.d_iplik = D_IP            # taranan cap devir cozumune de uygulansin

V0 = None
if DEVIR > 0:
    from agsim.netfull import simule as _sim
    _S = _sim(_t, _L, T=DEVIR * 1.02, kayit=400, topoloji=(P0, E, BILYE_DUG))
    _i = int(np.argmin(np.abs(_S["t"] - DEVIR)))
    _P, _V = _S["P_snap"][_i], _S["V_snap"][_i]
    POS_DEV = np.stack([_P[:, 2], _P[:, 0], _P[:, 1]], axis=1)
    V0      = np.stack([_V[:, 2], _V[:, 0], _V[:, 1]], axis=1)
    X_DEVIR = float(POS_DEV[:, 0].mean())
    POS_DEV[:, 0] -= X_DEVIR          # model pose'u X_DEVIR'e tasinacak
    R_DEVIR = float(np.mean(np.linalg.norm(
        POS_DEV[BILYE_DUG][:, 1:], axis=1)))

# ------------------------------------------------------------ baslangic konum
# Paketlenmis hal: dugumler eksende toplu, dis halka onde ("pay-out")
# DEGERLER PYTHON MODELINDEN (yukarida kurulan _t, _L)
R_PAK, L_PAK = 0.40 * _t.kapsul.D_hazne, _t.kapsul.L_hazne
rr = np.linalg.norm(P0[:, :2], axis=1)
f = rr / max(rr.max(), 1e-12)
ang = np.arctan2(P0[:, 1], P0[:, 0])
# Gazebo: +X ileri (ucus), +Y saga, +Z yukari
POS = np.zeros((len(P0), 3))
POS[:, 0] = L_PAK * (f - 1.0)                 # x: dis halka onde
POS[:, 1] = R_PAK * f * np.cos(ang)
POS[:, 2] = R_PAK * f * np.sin(ang)
if DEVIR > 0:
    POS = POS_DEV                      # devir anindaki GERCEK konumlar
# NOT: bilyeler AYRI bir bolme cemberine TASINMIYOR -- Python modeli de
# onlari dis halka yaricapinda baslatir; birebir karsilastirma icin ayni.


# Firlatici modeli: agzi X_AGIZ'da olacak sekilde yerlestirilir; ag da
# oradan dogar. Boylece ag firlaticinin O ANKI konumuna gore baslar.
X_AGIZ = 0.0
L_NAMLU_M = 0.1498
firlatici_blok = ("" if not FIRLATICI else f"""    <!-- MONTE EDILEBILIR FIRLATICI MODELI
         Gercek kullanimda bu <include> SENIN dunyanda olur ve kendi
         govdene bir <joint> ile baglanir. Burada serbest duruyor. -->
    <include>
      <uri>model://ag_firlatici</uri>
      <name>ag_firlatici</name>
      <pose>{-L_NAMLU_M:.4f} 0 2.0 0 0 0</pose>
    </include>
    <!-- firlaticiyi havada sabitle (test icin; gercekte drona baglanir) -->
    <joint name="firlatici_sabit" type="fixed">
      <parent>world</parent><child>ag_firlatici::namlu</child>
    </joint>""")

X_OFS = X_DEVIR if DEVIR > 0 else 0.0


def link(ad, m, p, gorsel_r, renk, carpisma_r=None, bitmask="0x02"):
    """Her dugum AYRI MODEL: tek model icindeki eklemsiz linkleri
    gz-physics/DART tek govdeye kaynaklar ve hicbiri hareket etmez."""
    cr = carpisma_r if carpisma_r is not None else gorsel_r
    I = 0.4 * m * cr * cr
    carp = f"""
        <collision name="c"><geometry><sphere><radius>{cr:.5f}</radius></sphere></geometry>
          <surface><friction><ode><mu>1.2</mu><mu2>1.2</mu2></ode></friction>
            <contact><collide_bitmask>{bitmask}</collide_bitmask>
              <ode><kp>1e5</kp><kd>10</kd></ode></contact></surface></collision>""" \
        if CARPISMA else ""
    return f"""    <model name="m_{ad}">
      <pose>{p[0]+X_OFS:.5f} {p[1]:.5f} {p[2]+2.0:.5f} 0 0 0</pose>
      <link name="{ad}">
        <pose>0 0 0 0 0 0</pose>
        <inertial><mass>{m:.6e}</mass><inertia>
          <ixx>{I:.6e}</ixx><iyy>{I:.6e}</iyy><izz>{I:.6e}</izz>
          <ixy>0</ixy><ixz>0</ixz><iyz>0</iyz></inertia></inertial>
        <visual name="v"><geometry><sphere><radius>{gorsel_r:.5f}</radius></sphere></geometry>
          <material><ambient>{renk}</ambient><diffuse>{renk}</diffuse></material></visual>{carp}
      </link>
    </model>"""


# ------------------------------------------------------------------ AG modeli
bilye_set = set(BILYE_DUG.tolist())
linkler = []
for k in range(len(P0)):
    if k in bilye_set:
        linkler.append(link(f"dugum_{k}", M_BILYE, POS[k], 0.00635, "0.25 0.25 0.22 1"))
    else:
        rg = 0.0035 if ORGU in ("hex", "kare") else 0.006
        linkler.append(link(f"dugum_{k}", max(M_DUG[k], 1e-6), POS[k],
                            rg, "0.16 0.47 0.84 1", carpisma_r=rg))

elemanlar = "\n".join(
    f"        <eleman>{int(i)} {int(j)} {l:.6f}</eleman>"
    for (i, j), l in zip(E, L0))

BILYE_IDX = " ".join(str(int(b)) for b in BILYE_DUG)
hizlar = "" if V0 is None else "\n".join(
    f"        <hiz>{k} {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}</hiz>"
    for k, v in enumerate(V0))
LOG_YOL = os.path.join(KOK, "out", "gazebo_ag.csv")
POZ_YOL = os.path.join(KOK, "out", "gazebo_poz.txt")

ag_model = f"""{chr(10).join(linkler)}

    <plugin filename="AgFizik" name="ag::AgFizik">
        <dugum_on_ek>dugum_</dugum_on_ek>
        <bilye_on_ek>__yok__</bilye_on_ek>
        <bilye_indis>{BILYE_IDX}</bilye_indis>
        <log_dosya>{LOG_YOL}</log_dosya>
        <log_dt>0.004</log_dt>
        <poz_dosya>{POZ_YOL}</poz_dosya>
        <poz_dt>0.010</poz_dt>
        <EA>{EA:.4f}</EA>
        <zeta>0.30</zeta>
        <!-- sonumleme olcegi: Python c = zeta*2*sqrt(k*m_ag/nN) ile AYNI -->
        <m_dugum>{M_NOM:.6e}</m_dugum>
        <d_iplik>{D_IP:.6e}</d_iplik>
        <Cdn>1.10</Cdn><Cdt>0.03</Cdt>
        <aero_olcek>{AERO_OLCEK:.4f}</aero_olcek>
        <rho>1.225</rho>
        <ruzgar>{-V_DRONE:.4f} 0 0</ruzgar>
        <bilye_Cd>0.47</bilye_Cd><bilye_D>0.0127</bilye_D>
        <firlatma_t>{FIRLATMA_T if TETIK == "zamanli" else -1}</firlatma_t>
        <tetik_konu>{TETIK_KONU}</tetik_konu>
        <firlatici_link>{"namlu" if FIRLATICI else ""}</firlatici_link>
        <!-- Dugum pozlari MUTLAK yazili; bu, uretim anindaki varsayilan
             firlatici pozu. Plugin agi firlaticinin GERCEK pozuna tasir,
             yani firlaticiyi dunyada istedigin yere koyabilirsin. -->
        <uretim_firlatici_poz>{-L_NAMLU_M:.4f} 0 2.0 0 0 0</uretim_firlatici_poz>
        <devir_t>{DEVIR}</devir_t>
        <v_eksenel>{V_EKS*np.cos(ALPHA):.4f}</v_eksenel>
        <!-- radyal hiz YALNIZCA bilyelere verilir (Python modeliyle ayni) -->
        <v_radyal>{V_RAD_CEP:.4f}</v_radyal>
        <!-- sadece sayisal guvenlik: fiziksel yuklerin cok uzerinde -->
        <F_sinir>200.0</F_sinir>
        <T_kopma>{ag.F_kopma:.2f}</T_kopma>
        <!-- elle dugumlenmis Dyneema agin GERCEK kopma yuku (~%55) -->
        <T_dugum>{ag.F_kopma*0.55:.2f}</T_dugum>
        <hedef_ad>{"talon_govde" if HEDEF_VAR else ""}</hedef_ad>
        <perv_x>-0.47</perv_x><perv_r>{PERVANE/2}</perv_r>
{hizlar}
{elemanlar}
    </plugin>"""

# ------------------------------------------------------------------ HEDEF
hedef = f"""    <model name="talon">
      <pose>{MENZIL0:.3f} 0 2.0 0 0 0</pose>
      <link name="talon_govde">
        <inertial><mass>1.8</mass><inertia>
          <ixx>0.30</ixx><iyy>0.12</iyy><izz>0.38</izz>
          <ixy>0</ixy><ixz>0</ixz><iyz>0</iyz></inertia></inertial>
        <visual name="v_govde"><geometry>
            <box><size>{GOVDE_L} 0.085 0.095</size></box></geometry>
          <material><ambient>0.75 0.34 0.23 1</ambient>
                    <diffuse>0.75 0.34 0.23 1</diffuse></material></visual>
        <collision name="c_govde"><geometry>
            <box><size>{GOVDE_L} 0.085 0.095</size></box></geometry>
          <surface><contact><collide_bitmask>0x02</collide_bitmask></contact></surface></collision>
        <visual name="v_kanat"><pose>-0.05 0 0.03 0 0 0</pose><geometry>
            <box><size>0.22 {KANAT} 0.014</size></box></geometry>
          <material><ambient>0.75 0.34 0.23 1</ambient>
                    <diffuse>0.75 0.34 0.23 1</diffuse></material></visual>
        <collision name="c_kanat"><pose>-0.05 0 0.03 0 0 0</pose><geometry>
            <box><size>0.22 {KANAT} 0.014</size></box></geometry></collision>
        <visual name="v_kuyruk"><pose>-0.40 0 0.10 0 0 0</pose><geometry>
            <box><size>0.16 0.52 0.012</size></box></geometry>
          <material><ambient>0.75 0.34 0.23 1</ambient>
                    <diffuse>0.75 0.34 0.23 1</diffuse></material></visual>
        <collision name="c_kuyruk"><pose>-0.40 0 0.10 0 0 0</pose><geometry>
            <box><size>0.16 0.52 0.012</size></box></geometry></collision>
        <visual name="v_pervane"><pose>-0.47 0 0 0 1.5708 0</pose><geometry>
            <cylinder><radius>{PERVANE/2}</radius><length>0.012</length></cylinder>
          </geometry><material><ambient>0.2 0.2 0.2 0.45</ambient>
                    <diffuse>0.2 0.2 0.2 0.45</diffuse></material></visual>
        <collision name="c_pervane"><pose>-0.47 0 0 0 1.5708 0</pose><geometry>
            <cylinder><radius>{PERVANE/2}</radius><length>0.012</length></cylinder>
          </geometry></collision>
      </link>
    </model>"""

# ------------------------------------------------------------------ DUNYA
dunya = f"""<?xml version="1.0" ?>
<!-- URETILMIS DOSYA — gazebo/scripts/ag_sdf_uret.py ile uretildi, elle duzenlemeyin.
     Cerceve: DRONE cercevesi. Drone ve hedef 100 km/h ayni yonde gittigi icin
     ikisi de bu cercevede DURAGAN; hava {V_DRONE:.1f} m/s karsi ruzgar olarak
     plugin'e veriliyor.
     dt = {DT*1e6:.0f} us  (iplik periyodunun 1/15'i -> acik entegrasyon KARARLI)
     carpisma/hedef: {"VAR (yakalama kosusu)" if CARPISMA else "YOK (dogrulama kosusu)"} -->
<sdf version="1.9">
  <world name="ag_atis">
    <physics name="hizli" type="dart">
      <max_step_size>{DT:.6f}</max_step_size>
      <!-- 0 = sinir yok: mumkun oldugunca hizli kos -->
      <real_time_factor>0</real_time_factor>
    </physics>
    <!-- Python modeli de yercekimini ucus eksenine DIK uygular -->
    <gravity>0 0 -9.81</gravity>

    <plugin filename="gz-sim-physics-system" name="gz::sim::systems::Physics"/>
    <plugin filename="gz-sim-user-commands-system"
            name="gz::sim::systems::UserCommands"/>
    <plugin filename="gz-sim-scene-broadcaster-system"
            name="gz::sim::systems::SceneBroadcaster"/>
    <plugin filename="gz-sim-contact-system"
            name="gz::sim::systems::Contact"/>

    <scene><ambient>0.85 0.85 0.85</ambient>
      <background>0.75 0.83 0.92</background><grid>false</grid></scene>
    <light type="directional" name="gunes">
      <pose>0 0 10 0 0 0</pose><diffuse>0.9 0.9 0.9 1</diffuse>
      <direction>-0.4 0.3 -0.9</direction></light>

{firlatici_blok}

{ag_model}

{hedef if HEDEF_VAR else "    <!-- hedef yok (AG_HEDEF=0) -->"}
  </world>
</sdf>
"""

PARCA_BASLIK = f"""<!-- ======================================================================
     AG EKLENTISI — KENDI DUNYANA YAPISTIRILACAK PARCA
     gazebo/scripts/ag_sdf_uret.py ile uretildi. ELLE DUZENLEME.

     NE ISE YARAR: <include> ile eklenen ag_firlatici modeli SADECE
     NAMLUDUR -- icinde ag da plugin de YOKTUR, tek basina ATES ETMEZ.
     Ates edebilmesi icin BU PARCAYI da kendi <world> etiketinin icine
     yapistirmalisin.

     NASIL:
       1) Asagidaki her seyi kendi dunyandaki <world> ... </world>
          arasina kopyala.
       1b) !! KENDI DUNYANDAKI <physics> BLOGUNU DA AYARLA !!
           <max_step_size>{{dt_s}}</max_step_size>
           Gazebo varsayilani 1 ms'dir; bu tasarim {{dt}} us ister.
           OLCULDU: 1 ms ile ag 1.08 m yerine 0.57 m aciliyor ve
           HIC HATA VERMIYOR -- yani sessizce YANLIS sonuc alirsin.
           Bu blok BURADA DEGILDIR, kendi dunyanda ayarlaman gerekir.
       2) <plugin> blogundaki <firlatici_link> degerini KENDI tasiyici
          link adinla degistir (varsayilan: namlu).
       3) GZ_SIM_SYSTEM_PLUGIN_PATH'i plugin build klasorune ayarla.
       4) Atesle:
          gz topic -t {TETIK_KONU} -m gz.msgs.Boolean -p "data: true"

     DIKKAT: ag dugumlerinin her biri AYRI <model> olmak ZORUNDADIR.
     Tek model icine toplarsan DART hepsini tek govdeye kaynaklar ve
     hicbiri hareket etmez. Bkz. README "Baska bir araca entegrasyon".

     Bu parca: {{n_dugum}} ag dugumu + 1 AgFizik plugin.
     Uretim: ORGU={ORGU}, R_ag={R_AG} m, goz={GOZ*1e3:.0f} mm, dt={{dt}} us
====================================================================== -->"""


if __name__ == "__main__":
    yol = os.path.join(KOK, "gazebo", "worlds", "ag_atis.sdf")
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    open(yol, "w").write(dunya)

    # --- YAPISTIRILABILIR PARCA: ag dugumleri + plugin (namlu HARIC)
    parca_yol = os.path.join(KOK, "gazebo", "worlds", "ag_eklentisi.sdf")
    basl = PARCA_BASLIK.replace("{n_dugum}", str(len(P0))) \
                       .replace("{dt_s}", f"{DT:.6f}") \
                       .replace("{dt}", f"{DT*1e6:.0f}")
    open(parca_yol, "w").write(basl + "\n" + ag_model + "\n")

    print(f"-> {yol}")
    print(f"-> {parca_yol}   (kendi dunyana YAPISTIRILACAK parca)")
    print(f"   {len(P0)} dugum ({len(BILYE_DUG)} bilye), {len(E)} eleman")
    print(f"   ag: O{2*R_AG:.2f} m, goz {GOZ*1e3:.0f} mm, {ag.L_iplik:.0f} m iplik, "
          f"{ag.m_ag*1e3:.2f} g")
    print(f"   aero_olcek = {AERO_OLCEK:.2f}  (kaba {L0.sum():.1f} m -> gercek "
          f"{ag.L_iplik:.0f} m)")
    print(f"   EA = {EA:.1f} N, bilye {M_BILYE*1e3:.2f} g x {len(BILYE_DUG)}")
    print(f"   v_eksenel {V_EKS*np.cos(ALPHA):.1f} m/s, v_radyal {V_RAD_CEP:.2f} m/s (sadece bilyeler)")
    print(f"   hedef {MENZIL0} m'de, atis t={FIRLATMA_T}s")
    print(f"   k_el = {K_EL:.0f} N/m, m_dugum = {M_NOM*1e6:.1f} mg")
    print(f"   dt = {DT*1e6:.0f} us  (kararli sinir {DT_KARARLI*1e6:.0f} us)")
    print(f"   carpisma: {'VAR' if CARPISMA else 'YOK'} | hedef: "
          f"{'VAR' if HEDEF_VAR else 'YOK'} | firlatici modeli: "
          f"{'VAR' if FIRLATICI else 'YOK'}")
    print(f"   tetik: {TETIK}" + (f" -> {TETIK_KONU}" if TETIK == "harici" else
          f" (t={FIRLATMA_T}s)"))
    print(f"   ORGU: {ORGU}" + (f"  (gercek goz {GOZ*1e3:.0f} mm, kenar "
          f"{L0.mean()*1e3:.1f} mm)" if ORGU == "hex" else
          f"  (kaba: dis cevre goz acikligi "
          f"{2*np.pi*R_AG/N_SPOKE*1e3:.0f} mm)"))
