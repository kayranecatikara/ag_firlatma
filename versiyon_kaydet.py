#!/usr/bin/env python3
"""Tasarimin o anki halini versiyonlar/<ad>/ altina DONDURUR.

Kaydedilen: iki konfig dosyasi, CAD olculeri/hacimleri, basilacak STL+STEP,
ilgili dokumanlar ve bir SURUM.md ozeti. Amac: her versiyonun hangi
sayilarla basildigini sonradan kesin bilmek.

Kullanim:  python3 versiyon_kaydet.py v1 "kisa aciklama"
"""
import os, sys, json, shutil, subprocess, datetime

KOK = os.path.dirname(os.path.abspath(__file__))


def kopyala(src, hedef_dir, ad=None):
    s = os.path.join(KOK, src)
    if not os.path.exists(s):
        return None
    d = os.path.join(hedef_dir, ad or os.path.basename(src))
    os.makedirs(os.path.dirname(d), exist_ok=True)
    shutil.copy2(s, d)
    return d


def main(ad, aciklama):
    hedef = os.path.join(KOK, "versiyonlar", ad)
    if os.path.exists(hedef):
        sys.exit(f"HATA: {hedef} zaten var. Once sil ya da baska ad ver.")
    os.makedirs(os.path.join(hedef, "baski"))

    # DIKKAT: cad/ ve out/ altinda AYNI ADLI v4_konfig.json var; duz
    # kopyalarsan biri otekini eziyordu. Kaynak klasoru ada eklenir.
    for f in ("cad/v4_konfig.json", "out/v4_konfig.json",
              "cad/v4_olcu.json", "cad/v4_hacim.json"):
        kaynak_kl, dosya_ad = f.split("/")
        kopyala(f, os.path.join(hedef, "konfig"),
                f"{kaynak_kl}_{dosya_ad}")

    bd = os.path.join(KOK, "baski")
    for f in sorted(os.listdir(bd)):
        if f.endswith((".stl", ".step", ".md", ".json")):
            kopyala(os.path.join("baski", f), os.path.join(hedef, "baski"))

    for f in ("malzeme_listesi.md", "out/AG_ORME_KILAVUZU.png",
              "out/TEST_1.md", "out/v10_test_6boncuk.json"):
        kopyala(f, os.path.join(hedef, "dok"))

    P = json.load(open(os.path.join(KOK, "cad", "v4_olcu.json")))
    K = json.load(open(os.path.join(KOK, "out", "v4_konfig.json")))
    try:
        sha = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"],
                                      cwd=KOK, text=True).strip()
    except Exception:
        sha = "?"

    with open(os.path.join(hedef, "SURUM.md"), "w", encoding="utf-8") as f:
        f.write(f"""# {ad.upper()} — {aciklama}

Dondurulma: {datetime.date.today()} · commit `{sha}`

## Namlu / tahrik
| | |
|---|---|
| Namlu boyu | **{P['L_namlu']:.1f} mm** |
| İç çap | Ø{P['D_bore']:.1f} mm |
| Strok | **{P['STROK']:.0f} mm** |
| Bant serbest boy L0 | **{P['L0']:.1f} mm** |
| Kurulu uzama λ | **×{P['lam']:.1f}** |
| Bant | Ø{P['bant_OD']:.0f} / iç Ø{P['bant_ID']:.0f} mm, **{K['n_bant']} kol** |
| Iraksak koni | {P['koni_acisi']:.0f}° |
| İki parça bölme | y = {P['y_bol']:.0f} mm |

## Kapsül / boncuk
| | |
|---|---|
| Kapsül boyu | {P['L_kapsul']:.1f} mm |
| Yuva eğimi | **{P['ALFA']:.0f}°** |
| Yuva | Ø{P['D_yuva']:.1f} mm, derinlik {P['derinlik']:.1f}, R_pitch {P['R_pitch']:.1f} |
| Boncuk | **{K['n_boncuk_top']} × Ø{K['D_boncuk']*1e3:.0f} mm**, yuva başına {K['n_boncuk']}, toplam {K['n_boncuk_top']*K['m_boncuk']*1e3:.0f} g |

## Ağ
| | |
|---|---|
| Çap | **Ø{2*K['R_ag']:.1f} m** |
| Göz | {K['goz']*1e3:.0f} mm kare |
| İp | Dyneema Ø{K['d_ip']*1e3:.2f} mm |

## Bant ankrajı
Ø{P['d_bant_delik']:.0f} mm geçiş deliği + Ø{P['d_pim_bant']:.0f} mm delen pim,
ankraj yarıçapı {P['r_bant']:.0f} mm, kenar başına {P['n_ankraj_yan']:.0f} bant.

## İçerik
- `konfig/` — bu versiyonu birebir yeniden üretecek dosyalar
- `baski/` — STL + STEP + baskı ayarları
- `dok/` — malzeme listesi, ağ örme kılavuzu, test protokolü
""")
    print(f"-> versiyonlar/{ad}  ({aciklama})")
    print(f"   namlu {P['L_namlu']:.1f} mm · strok {P['STROK']:.0f} · L0 {P['L0']:.1f} · "
          f"lam {P['lam']:.1f} · {K['n_bant']} bant · {K['n_boncuk_top']} boncuk · "
          f"yuva {P['ALFA']:.0f}d")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("kullanim: versiyon_kaydet.py <ad> <aciklama>")
    main(sys.argv[1], sys.argv[2])
