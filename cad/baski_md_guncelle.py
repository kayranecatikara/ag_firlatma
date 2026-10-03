#!/usr/bin/env python3
"""baski/BASKI_AYARLARI.md icindeki PARCA LISTESI tablosunu parcalar.json'dan
yeniden yazar. Tablo elle duzenlenmez; CAD degisince bu betik kosulur."""
import os, sys, json, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agsim.yollar import kyol

B = kyol("baski")
P = json.load(open(os.path.join(B, "parcalar.json")))
md_yol = os.path.join(B, "BASKI_AYARLARI.md")
s = open(md_yol, encoding="utf-8").read()

ADLAR = {
 "01a_namlu_govde": "Namlu gövdesi (arka parça)",
 "01b_agiz_basligi": "Ağız başlığı (ıraksak koni)",
 "02_kapsul": "Kapsül",
 "03_tetik_kapagi_sag": "Tetik kartuş kapağı (sağ)",
 "04_tetik_kapagi_sol": "Tetik kartuş kapağı (sol)",
 "05_servo_makarasi": "Servo ip makarası",
 "06_toz_kapagi": "Arka toz kapağı (opsiyonel)",
 "07_tampon_ust": "Yarık sonu tamponu (üst)",
 "08_tampon_alt": "Yarık sonu tamponu (alt)",
}
sat = ["| Dosya | Parça | Adet | Filament | Ölçü (X×Y×Z mm) | Filament |",
       "|---|---|---|---|---|---|"]
pet = tpu = 0.0
for p in P:
    g = p["filament_g"] * p["adet"]
    if p["malzeme"] == "PETG": pet += g
    else: tpu += g
    sat.append(f"| `{p['ad']}` | {ADLAR.get(p['ad'], p['ad'])} | "
               f"{'**%d**' % p['adet'] if p['adet'] > 1 else p['adet']} | "
               f"**{p['malzeme']}** | {p['x']:.0f} × {p['y']:.0f} × "
               f"**{p['z']:.1f}** | ~{g:.1f} g |")
tablo = "\n".join(sat) + f"\n\n**TOPLAM: PETG ~{pet:.0f} g · TPU ~{tpu:.1f} g**"

yeni, n = re.subn(r"\| Dosya \| Parça \|.*?\*\*TOPLAM: PETG[^\n]*\*\*",
                  tablo, s, count=1, flags=re.S)
assert n == 1, "tablo bloku bulunamadi"

zmax = max(p["z"] for p in P)
yeni = re.sub(r"\*\*Z yüksekliği ≥ \d+ mm\*\* gerekli \([^)]*\)",
              f"**Z yüksekliği ≥ {zmax + 5:.0f} mm** gerekli "
              f"(en uzun parça {zmax:.1f} mm)", yeni, count=1)
open(md_yol, "w", encoding="utf-8").write(yeni)
print(f"BASKI_AYARLARI.md tablosu guncellendi: {len(P)} parca, "
      f"PETG {pet:.0f} g, TPU {tpu:.1f} g, Z>={zmax + 5:.0f} mm")
