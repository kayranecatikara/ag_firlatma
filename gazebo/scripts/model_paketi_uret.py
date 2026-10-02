#!/usr/bin/env python3
"""MONTE EDILEBILIR GAZEBO MODEL PAKETI uretir.

gazebo/models/ag_firlatici/  ->  model.config + model.sdf + meshes/

Bu, ag_atis.sdf'ten (uretilmis TEST DUNYASI) FARKLIDIR: baska bir araca
<include> ile eklenip tek <joint> ile baglanabilen, gercek kutle/atalet
tasiyan bir MODEL paketidir.

EKSEN DUZENI:  +X namlu ekseni (agiz yonu),  +Z yukari.
ORIJIN      :  namlunun ARKA yuzunun merkezi (yukleme agzi).
MONTAJ      :  <frame name="montaj"> -- namlu ortasinda, UST yuzeyde.
"""
import os, json, shutil
import numpy as np

KOK = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MOD = os.path.join(KOK, "gazebo", "models", "ag_firlatici")
P = json.load(open(os.path.join(KOK, "cad", "v4_konfig.json")))

L_NAMLU = 28.5 + P["STROK"] * (1 + 1 / (P["lam"] - 1))      # mm
D_DIS, D_IC = 55.4, P.get("D_bore", 43.4)
D_KAPSUL, L_KAPSUL = 43.1, 40.0
SERVO = (32.0, 16.0, 30.0)

# --- kutleler (malzeme_listesi.md'den, bkz. model.config) ---
M_NAMLU, M_KAPSUL, M_SERVO, M_PIM = 0.2162, 0.1380, 0.0143, 0.0033


def silindir_atalet(m, ro, ri, L):
    """Ici bos silindir; eksen = X."""
    Ixx = 0.5 * m * (ro**2 + ri**2)
    Iyy = m / 12.0 * (3 * (ro**2 + ri**2) + L**2)
    return Ixx, Iyy, Iyy


def kutu_atalet(m, a, b, c):
    return (m/12*(b*b+c*c), m/12*(a*a+c*c), m/12*(a*a+b*b))


def inertial(m, I, cx=0.0, cy=0.0, cz=0.0):
    return (f"""      <inertial>
        <pose>{cx:.5f} {cy:.5f} {cz:.5f} 0 0 0</pose>
        <mass>{m:.5f}</mass>
        <inertia><ixx>{I[0]:.3e}</ixx><iyy>{I[1]:.3e}</iyy><izz>{I[2]:.3e}</izz>
          <ixy>0</ixy><ixz>0</ixz><iyz>0</iyz></inertia>
      </inertial>""")


def main():
    os.makedirs(os.path.join(MOD, "meshes"), exist_ok=True)
    for src, dst in (("01_namlu.stl", "namlu.stl"), ("02_kapsul.stl", "kapsul.stl")):
        shutil.copy(os.path.join(KOK, "baski", src),
                    os.path.join(MOD, "meshes", dst))

    Ln, ro, ri = L_NAMLU*1e-3, D_DIS/2e3, D_IC/2e3
    I_namlu = silindir_atalet(M_NAMLU, ro, ri, Ln)
    rk, Lk = D_KAPSUL/2e3, L_KAPSUL*1e-3
    I_kaps = silindir_atalet(M_KAPSUL, rk, 0.0, Lk)
    I_srv = kutu_atalet(M_SERVO, *[x*1e-3 for x in SERVO])

    # STL'ler BASKI yonunde (eksen Z, taban z=0) -> Y ekseni etrafinda +90 ile +X'e cevir
    MESH_POSE = "0 0 0 0 1.5708 0"
    x_mid = Ln/2
    x_kaps = 0.005 + Lk/2            # dinlenmede kapsul arkada

    sdf = f"""<?xml version="1.0"?>
<!-- URETILMIS DOSYA — gazebo/scripts/model_paketi_uret.py ile uretildi.
     AG FIRLATICI v6 — baska bir araca monte edilebilir model paketi.

     EKSEN: +X namlu ekseni (agiz yonu), +Z yukari.
     ORIJIN: namlunun ARKA yuzunun merkezi.
     MONTAJ: <frame name="montaj"> — namlu ortasi, ust yuzey.

     KULLANIM (bkz. README "Baska bir araca entegrasyon"):
       <include><uri>model://ag_firlatici</uri>
         <pose relative_to="govdem">0 0 -0.08 0 0 0</pose></include>
       <joint name="firlatici_baglanti" type="fixed">
         <parent>govdem</parent><child>ag_firlatici::namlu</child></joint>
-->
<sdf version="1.9">
  <model name="ag_firlatici">

    <!-- ===== TASIYICI GOVDE (namlu + bantlar + tetik donanimi) ===== -->
    <link name="namlu">
{inertial(M_NAMLU, I_namlu, cx=x_mid)}
      <visual name="v_namlu">
        <pose>{MESH_POSE}</pose>
        <geometry><mesh><uri>model://ag_firlatici/meshes/namlu.stl</uri>
          <scale>0.001 0.001 0.001</scale></mesh></geometry>
        <material><ambient>0.18 0.20 0.24 1</ambient>
                  <diffuse>0.22 0.25 0.30 1</diffuse></material>
      </visual>
      <!-- Carpisma: STL yerine SILINDIR. Ucus simulasyonunda namlunun
           ic detayi gereksiz; silindir hem hizli hem kararli. -->
      <collision name="c_namlu">
        <pose>{x_mid:.5f} 0 0 0 1.5708 0</pose>
        <geometry><cylinder><radius>{ro:.5f}</radius>
          <length>{Ln:.5f}</length></cylinder></geometry>
      </collision>
    </link>

    <!-- ===== KAPSUL (ag + 6 bilye icinde) =====
         Dinlenmede strok sonunda; atista ileri kayip tamponlara carpar.
         Prizmatik eklem NAMLU EKSENINDE (+X). -->
    <link name="kapsul">
      <pose>{x_kaps:.5f} 0 0 0 0 0</pose>
{inertial(M_KAPSUL, I_kaps)}
      <visual name="v_kapsul">
        <pose>{-Lk/2:.5f} 0 0 0 1.5708 0</pose>
        <geometry><mesh><uri>model://ag_firlatici/meshes/kapsul.stl</uri>
          <scale>0.001 0.001 0.001</scale></mesh></geometry>
        <material><ambient>0.65 0.30 0.12 1</ambient>
                  <diffuse>0.80 0.38 0.16 1</diffuse></material>
      </visual>
    </link>
    <joint name="kapsul_kayit" type="prismatic">
      <parent>namlu</parent><child>kapsul</child>
      <axis><xyz>1 0 0</xyz>
        <limit><lower>0</lower><upper>{P['STROK']*1e-3:.4f}</upper></limit>
        <dynamics><damping>0.5</damping></dynamics></axis>
    </joint>

    <!-- ===== SERVOLAR (mikro, metal disli, ~14 g) ===== -->"""

    for ad, zy in (("servo_sag", +1), ("servo_sol", -1)):
        yv = zy * (ro + SERVO[1]/2e3)
        sdf += f"""
    <link name="{ad}">
      <pose>{x_mid:.5f} {yv:.5f} 0 0 0 0</pose>
{inertial(M_SERVO, I_srv)}
      <visual name="v_{ad}"><geometry><box><size>
        {SERVO[0]*1e-3:.4f} {SERVO[1]*1e-3:.4f} {SERVO[2]*1e-3:.4f}</size></box></geometry>
        <material><ambient>0.08 0.08 0.09 1</ambient>
                  <diffuse>0.12 0.12 0.14 1</diffuse></material></visual>
    </link>
    <joint name="{ad}_baglanti" type="fixed">
      <parent>namlu</parent><child>{ad}</child>
    </joint>"""

    sdf += f"""

    <!-- ===== MONTAJ ARAYUZU =====
         Kendi govdene baglarken BU cerceveyi referans al.
         Namlu ortasi, ust yuzey. -->
    <frame name="montaj" attached_to="namlu">
      <pose>{x_mid:.5f} 0 {ro:.5f} 0 0 0</pose>
    </frame>
    <!-- Agiz ucu: ag buradan cikar; tetikleme mesafesi buradan olculur -->
    <frame name="agiz" attached_to="namlu">
      <pose>{Ln:.5f} 0 0 0 0 0</pose>
    </frame>

  </model>
</sdf>
"""
    open(os.path.join(MOD, "model.sdf"), "w").write(sdf)

    cfg = f"""<?xml version="1.0"?>
<model>
  <name>ag_firlatici</name>
  <version>6.0</version>
  <sdf version="1.9">model.sdf</sdf>
  <author><name>ag_firlatma projesi</name></author>
  <description>
    Lastik bant tahrikli ag firlatici. Tail-sitter VTOL altina monte edilir.
    Hedef: X-UAV Talon sinifi sabit kanat (1718 mm kanat acikligi).

    Namlu {L_NAMLU:.1f} mm, strok {P['STROK']:.0f} mm, 4 x lateks bant (lam=4.0).
    Cikis hizi 31.1 m/s. Toplam kutle {M_NAMLU+M_KAPSUL+2*M_SERVO+2*M_PIM:.3f} kg.

    KUTLE DAGILIMI:
      namlu    {M_NAMLU*1e3:.1f} g  (govde + bantlar + tetik donanimi + kablolar)
      kapsul   {M_KAPSUL*1e3:.1f} g  (kapsul + capraz pim + AG + 6 kursun bilye)
      servo    {M_SERVO*1e3:.1f} g  x2 (mikro, metal disli)

    AG FIZIGI BU MODELDE DEGILDIR. Ag dugumleri AYRI MODEL'ler olarak
    uretilir (gazebo/scripts/ag_sdf_uret.py) ve AgFizik plugin'i ile
    cozulur. Bkz. README "Baska bir araca entegrasyon".

    GERI TEPME: atista ~2.3 kg.m/s (ag + bilyeler 74 g @ 31.1 m/s).
    Kapsul namlu icinde kalir.
  </description>
</model>
"""
    open(os.path.join(MOD, "model.config"), "w").write(cfg)

    print(f"-> {MOD}")
    print(f"   namlu  {L_NAMLU:6.1f} mm,  {M_NAMLU*1e3:5.1f} g")
    print(f"   kapsul {L_KAPSUL:6.1f} mm,  {M_KAPSUL*1e3:5.1f} g  (ag + bilye dahil)")
    print(f"   servo  x2            {M_SERVO*1e3:5.1f} g")
    print(f"   TOPLAM               {(M_NAMLU+M_KAPSUL+2*M_SERVO+2*M_PIM)*1e3:5.1f} g")
    print(f"   atalet namlu Ixx={I_namlu[0]:.3e} Iyy={I_namlu[1]:.3e}")


if __name__ == "__main__":
    main()
