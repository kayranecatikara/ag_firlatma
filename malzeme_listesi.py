"""NAMLU (ag firlatici) — eksiksiz malzeme listesi (v2, lastik bant tahrikli).
Olculer cad/v2_olcu.json ve cad/v2_hacim.json'dan (CAD'den) gelir.
Cikti: malzeme_listesi.md + malzeme_listesi.csv
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                if os.path.basename(os.path.dirname(os.path.abspath(__file__))) == "cad"
                else os.path.dirname(os.path.abspath(__file__)))
from agsim.yollar import vyol, kyol
import json, csv, math

P = json.load(open(vyol(__file__, "cad", "v4_olcu.json")))
V = json.load(open(vyol(__file__, "cad", "v4_hacim.json")))
g = lambda ad, rho: V[ad]["V"] * rho                       # cm3 * g/cm3

# ag: altigen, kose yaricapi 1.1 m, goz 130 mm
# --- AG: out/v4_konfig.json'dan (nihai tasarim, eldeki 0.60 mm ip) ---
_KF = json.load(open(vyol(__file__, "out", "v4_konfig.json")))
R, GOZ = _KF["R_ag"], _KF["goz"]
D_IP   = _KF["d_ip"]                                       # m
N_BONCUK, D_BONCUK, M_BONCUK = _KF["n_boncuk_top"], _KF["D_boncuk"], _KF["m_boncuk"]
RHO_IP = 970.0 * (math.pi/4) * D_IP**2 * 1000              # g/m
A = 1.5 * math.sqrt(3) * R ** 2
L_goz = 2 * A / GOZ                                        # m
L_cevre = 6 * R
dugum = int(A / GOZ ** 2)
bant_kesim = P["L0"] + 2 * 10.0
N_BANT = 4                            # calisma boyu + 2 uc
pim_boy = 37.5 - (21.7 - 5.0 + 0.15)
F_TOP, F_BANT = 1200.0, 300.0

S = []   # (grup, no, parca, adet, malzeme/ozellik, olcu, kutle_g_toplam, not)
def ekle(*r): S.append(r)

G = "A. 3D BASKI"
ekle(G, "A1", "Namlu govdesi (bilezik + bant kulaklari + 2 tetik gobegi + 2 servo yatagi dahil)", 1,
     "PETG (tercih ASA - UV'ye dayanikli)",
     f"O55.4 dis / O43.4 ic x {P['L_namlu']:.1f} mm, 2 duz yarik 6.4 mm",
     g("V4_namlu", 1.00), "Dik bas (eksen Z), 4 cevre + %50 gyroid. Yariklar ve delikler destek istemez.")
ekle(G, "A2", "Kapsul (arka blok + tutma kanali + ag haznesi + 6 bilye yuvasi)", 1,
     "PETG", f"O43.1 x {P['L_kapsul']:.0f} mm, hazne O37.1 x {P['L_hazne']:.0f} mm, yuva acisi {P['ALFA']:.0f} derece",
     g("V4_kapsul", 1.00), "Agiz yukari bas. Arka blok 16 mm yuk tasir: 5 cevre + %60 dolgu.")
ekle(G, "A3", "Tetik kartus kapagi", 2, "PETG", "O18 x 3 mm, ortada O2 ip deligi, 2x O2.2 vida deligi",
     2 * g("V4_kapak_sag", 1.27), "%100 dolgu.")
ekle(G, "A4", "Servo ip makarasi", 2, "PETG", "O8 mm (r=4 mm) tambur, servo dislisine oturur, O1.5 ip deligi",
     2 * 0.4, "Servonun kendi kol vidasiyla sabitlenir.")
ekle(G, "A5", "Yarik sonu durdurma tamponu", 2, "TPU 95A", "6.2 x 3 x 7 mm",
     2 * g("V4_tampon_ust", 1.21), "Yarik on ucuna CA ile yapistir. Kapsulun carpma yukunu yumusatir (~450 N).")
ekle(G, "A6", "Arka toz kapagi (opsiyonel)", 1, "PETG", "O43 tapa, ortada O10 havalandirma", 2.0,
     "Arka agiz yukleme agzidir; ucusta toz/kir girmesin diye.")

G = "B. METAL / ISLEME PARCALAR"
ekle(G, "B1", "Capraz pim", 1, "Aluminyum 7075-T6 cubuk (alternatif: gumus celigi)",
     f"O8 x {P['capraz_uzun']:.0f} mm; her ucta IKI oluk: r={P['r_bant']:.0f} ve "
     f"r={P['r_bant']+P['dz_bant']:.0f} mm, 2.4 mm genislik x 1 mm derinlik",
     g("V4_capraz_pim", 2.81), "4 bant icin 4 oluk. Egilme SF 4.1 @ 1080 N. O6 YETERSIZ (SF 1.7).")
ekle(G, "B2", "Tetik pimi", 2, "Gumus celigi / paslanmaz cubuk",
     f"O5 x {pim_boy:.1f} mm, ust uctan 1 mm'de O1.5 enine ip deligi, uc hafif pahli",
     2 * 3.3, "Uc kapsul kanalina girer; yuzey puruzsuz olmali.")
ekle(G, "B3", "Mil bilezigi (pim yakasi / yay tablasi)", 2, "Celik, set vidali (DIN 705)",
     "O5 ic / O10 dis / 5 mm genislik, M3 set vida",
     2 * 2.2, "Pim ucundan 12.2 mm'ye sabitlenir (dinlenmede uc kanal dibine 0.3 mm pay).")
ekle(G, "B4", "Geri getirme yayi (basma)", 2, "Yay celigi",
     "ic O>=5.3, dis O<=10.2, tel ~0.5-0.6 mm, serbest boy ~13 mm, blok boy <=4 mm",
     2 * 0.3, "Dinlenmede 10 mm (on yuk), cekilince 4 mm. Hazir yay setlerinden secilebilir.")
ekle(G, "B5", "Bant ankraj pimi", N_BANT, "Paslanmaz celik pim", "O4 x 16 mm", 2 * 1.6,
     "Agiz kulagindaki enine delige gecer, bant halkasini tutar. Uclara CA damlasi veya kucuk segman.")
ekle(G, "B6", "Ip yonlendirme pimi", 2, "Paslanmaz celik pim", "O3 x 10 mm", 2 * 0.6,
     "Kapaktan radyal cikan ipi servo tamburuna cevirir. Puruzsuz olmali (veya O6 mini makara).")

G = "C. STANDART BAGLANTI ELEMANLARI"
ekle(G, "B7", "PTFE burc (tetik pimi)", 2, "PTFE/teflon burc", "ic O5.0 / dis O7 x 10 mm", 2*0.3,
     "Namlu delige gecer. Surtunmeyi mu=0.18'den 0.08'e dusurur - servo secimi buna bagli.")
ekle(G, "C1", "M2 isil gomme insert (heat-set)", 8, "Pirinc", "M2 x 3 mm", 8 * 0.15,
     "4 adet kapak vidasi + 4 adet servo vidasi icin (PETG'ye havyayla).")
ekle(G, "C2", "M2 x 6 civata (kapak)", 4, "Paslanmaz, silindir basli", "M2 x 6", 4 * 0.2, "")
ekle(G, "C3", "M2 x 8 civata (servo)", 4, "Paslanmaz", "M2 x 8", 4 * 0.25,
     "Servonun kendi vidalari kisa kalirsa.")
ekle(G, "C4", "M3 set vida (mil bileziklerinin kendi vidasi)", 2, "Celik", "M3 x 3", 0,
     "Bilezikle gelir; diş sabitleyiciyle (Loctite 243).")

G = "D. TAHRIK — LATEKS BANT"
ekle(G, "D1", "Lateks tup (zipkin lastigi)", N_BANT, "SAF DOGAL KAUCUK LATEKS (silikon/EPDM OLMAZ)",
     f"O15.2 dis / O4 ic; kesim boyu ~{bant_kesim:.0f} mm (calisma {P['L0']:.0f} mm + 2x10 mm uc)",
     N_BANT * math.pi / 4 * (15.2 ** 2 - 4 ** 2) * bant_kesim / 1000 * 0.95,
     f"KENAR BASINA 2 ADET. Kurulu uzama x{P['lam']:.0f}, {F_BANT:.0f} N/bant ({F_BANT/9.81:.0f} kg). "
     f"O14 bulunursa o da olur (kuvvet ~%7 duser).")
ekle(G, "D2", "Bant uc halkasi (Dyneema)", 2 * N_BANT, "Dyneema/UHMWPE orgu halat", "O1.5 mm, her biri ~60 mm",
     2 * N_BANT * 0.1, "Tup ucuna ic dugumle gomulur, disi sarilir. Arka halka capraz pim oluguna, on halka ankraj pimine.")
ekle(G, "D3", "Bant ucu sargi ipi", 1, "Naylon/Dyneema iplik (dikis/sargi)", "~2 m", 0.2,
     "Tup uclarini halka dugumu uzerine sikica sarmak icin. Uc basina donanim <= 7 mm olmali!")

G = "E. TETIK TAHRIK — ELEKTRIK"
ekle(G, "E1", "Servo", 2, "MG996R sinifi (>=11 kg.cm @6V, metal disli)", "40 x 20 x 37 mm",
     2 * 55.0, f"Pim basina {F_TOP/2:.0f} N yuk -> PTFE burcla ~{2*0.08*F_TOP/2:.0f} N cekme. "
     "Mikro servo YETMEZ. Iki servo AYNI sinyal (Y-kablo). Makara r=6 mm.")
ekle(G, "E2", "Servo Y-kablosu (1 giris -> 2 servo)", 1, "JR/Futaba 3 pin", "~15 cm", 4.0, "")
ekle(G, "E3", "Servo uzatma kablosu", 1, "JR/Futaba 3 pin", "gerekli boy (tarete gore)", 5.0,
     "Ucus kontrolcusundeki bir PWM cikisina.")
ekle(G, "E4", "Tetik ipi", 2, "PE/Dyneema orgu, PE #6 (~0.40 mm, ~30 kg)", "her biri ~120 mm",
     2 * 0.02, "Pim deliginden -> kapak deliginden -> yonlendirme piminden -> servo tamburuna.")
ekle(G, "E5", "Kablo bagi / spiral", 4, "Naylon", "2.5 mm genislik", 4 * 0.1, "Kablolari namluya sabitlemek icin.")

G = "F. AG VE BILYELER"
ekle(G, "F1", "Ag ipi — goz + cevre halati + radyal baglar (HEPSI AYNI IP)", 1,
     f"Hyper Dyneema orgu, O{D_IP*1e3:.2f} mm, 45.40 kg (ELDEKI IP)",
     f"altigen O{2*R:.1f} m, kare goz {GOZ*1e3:.0f} mm: {L_goz+L_cevre:.1f} m kafes+halat "
     f"+ radyal baglar ve baglama paylari -> ~47 m kes",
     47.0 * RHO_IP, "ELDE 90 m VAR — yeterli, 1 kez daha deneme payi birakir. "
     "Cevre halati icin ayri/kalin ip ALMA: ayni ip kullaniliyor.")
ekle("F. AG VE BILYELER", "F4", "Boncuk (bilye)", N_BONCUK,
     f"DELIKLI KURSUN boncuk — Captain 1216, O{D_BONCUK*1e3:.0f} mm, {M_BONCUK*1e3:.0f} g/ad (ELDE VAR)",
     f"O{D_BONCUK*1e3:.0f} mm, ortasi ~O2 mm delikli; yuva basina 2 ad (6 yuva)",
     N_BONCUK * M_BONCUK * 1000,
     "ELDE VAR, satin alinacak degil. Delik sart: ip boncuklarin icinden gecer.")
ekle(G, "F5", "Kirilgan on kapak (her atis icin 1)", 1, "Ince kagit / pelur", "O43 disk", 0.1,
     "Kapsul agzina yapistirici cubukla noktasal yapistirilir; bilyeleri ve ag paketini tutar, atista yirtilir.")

G = "G. SARF / YARDIMCI"
ekle(G, "G1", "Yag (pim yuzeyleri icin)", 1, "Ince makine yagi (veya PTFE kuru yaglayici sprey)", "birkac damla", 0,
     "PTFE sprey surtunmeyi yagin ~yarisina indirir -> servoya ek pay.")
ekle(G, "G2", "Dis sabitleyici", 1, "Loctite 243 (orta)", "", 0, "Mil bileziklerinin set vidalari.")
ekle(G, "G3", "Siyanoakrilat yapistirici (CA)", 1, "", "", 0, "TPU tampon, ankraj pimi uclari.")
ekle(G, "G4", "Yapistirici cubuk", 1, "", "", 0, "Kirilgan kagit kapak icin (zayif tutunmali).")
ekle(G, "G5", "Talk pudrasi (opsiyonel)", 1, "", "", 0, "Paketlenen agda iplerin birbirine yapismasini azaltir.")

G = "H. TEST / KURULUM EKIPMANI"
ekle(G, "H1", "Dijital bagaj kantari", 1, "0-50 kg", "", 0, "Bant cekme testi + tetik ipi cekme kuvveti olcumu.")
ekle(G, "H2", "Kurma eldiveni", 1, "Kalin is eldiveni", "", 0, "Her bant ~34 kg cekilir; tek tek takilir.")
ekle(G, "H3", "Yedek bant seti", 1, "D1-D3", "", 0, "Lateks yaslanir; testlerde surekli yedek bulundur.")
ekle(G, "H4", "Yuksek hizli kamera (telefon 240 fps)", 1, "", "", 0, "Yer atisinda acilma suresi/cap olcumu.")

# ------------------------------------------------------------------ yazdir
ucan = {"F1", "F2", "F3", "F4"}
m_top = sum(r[6] for r in S if r[0][0] in "ABCDEF")
with open("malzeme_listesi.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Grup", "No", "Parca", "Adet", "Malzeme / Ozellik", "Olcu", "Toplam kutle [g]", "Not"])
    for r in S:
        w.writerow(list(r[:6]) + [f"{r[6]:.1f}", r[7]])
with open("malzeme_listesi.md", "w") as f:
    f.write(f"# Ag Firlatici Namlu — Malzeme Listesi (v2, lastik bant)\n\n")
    f.write(f"Namlu {P['L_namlu']:.1f} mm · strok {P['STROK']:.0f} mm · kapsul {P['L_kapsul']:.0f} mm · "
            f"bant 2x O16/4 lateks x{P['lam']:.0f} · ag O{2*R:.1f} m altigen\n\n")
    grup = None
    for r in S:
        if r[0] != grup:
            grup = r[0]; f.write(f"\n## {grup}\n\n| No | Parca | Adet | Malzeme / Ozellik | Olcu | Kutle [g] | Not |\n|---|---|---|---|---|---|---|\n")
        f.write(f"| {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {r[6]:.1f} | {r[7]} |\n")
    f.write(f"\n**Toplam (A-F, test ekipmani haric): ~{m_top:.0f} g**\n")
print(f"{len(S)} kalem, toplam ~{m_top:.0f} g -> malzeme_listesi.md / .csv")
for grp in sorted({r[0] for r in S}):
    print(f"  {grp:34s} {sum(r[6] for r in S if r[0]==grp):6.1f} g")
