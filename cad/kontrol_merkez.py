#!/usr/bin/env python3
"""Kapsul AGZINDA agin kullanabilecegi MERKEZI BOS ALANI olcer.

"Acik alan" diye kesit bosluklarini toplamak yaniltici: boncuk yuvalari da
bosluk sayilir ama ag oradan gecemez. Bu betik agiz duzlemini tarayip
EKSENDEN BASLAYAN BAGLI bosluk bolgesini sayar.

Kullanim:  freecadcmd cad/kontrol_merkez.py
"""
import os, sys, json, math
from collections import deque
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import FreeCAD, Part                                          # noqa: E402
from FreeCAD import Vector as V                               # noqa: E402
from agsim.yollar import kyol                                 # noqa: E402

P = json.load(open(kyol("cad", "v4_olcu.json")))
y0 = P["arka"]; L = P["L_kapsul"]
Rk = P["D_bore"] / 2 - P["bosluk"] / 2
N = 141
h = 2 * Rk / (N - 1)
V_IP = 39.2 * 1000 * math.pi / 4 * 0.60 ** 2 / 1000.0          # cm3

sek = Part.Shape(); sek.read(kyol("cad", "V4_kapsul_hazneli.step"))
y = y0 + L - 0.5
grid = [[False] * N for _ in range(N)]
for i in range(N):
    x = -Rk + i * h
    for j in range(N):
        z = -Rk + j * h
        if x * x + z * z <= Rk * Rk:
            grid[i][j] = not sek.isInside(V(x, y, z), 0.01, True)

c = N // 2
A = 0.0
if grid[c][c]:
    gor = [[False] * N for _ in range(N)]
    q = deque([(c, c)]); gor[c][c] = True; n = 0
    while q:
        i, j = q.popleft(); n += 1
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            a, b = i + di, j + dj
            if 0 <= a < N and 0 <= b < N and grid[a][b] and not gor[a][b]:
                gor[a][b] = True; q.append((a, b))
    A = n * h * h

zarf = Part.makeCylinder(Rk, L, V(0, y0, 0), V(0, 1, 0))
ic = (zarf.Volume - sek.common(zarf).Volume) / 1000.0

print(f"namlu ici O{2*Rk+P['bosluk']:.1f} · kapsul dis R{Rk:.2f} · "
      f"R_pitch {P['R_pitch_hazneli']:.1f}")
print(f"\n  MERKEZI BAGLI BOS ALAN  {A:6.0f} mm2  = O{2*math.sqrt(A/math.pi):.1f}")
print(f"  hazne ic bosluk         {ic:6.1f} cm3")
print(f"  ag ipi (39.2 m)         {V_IP:6.1f} cm3  -> doluluk %{V_IP/ic*100:.0f}")
print(f"  kapsul kati             {sek.Volume/1000:6.1f} cm3 "
      f"-> ~{sek.Volume/1000*1.27*0.82:.1f} g")
print("\nSONUC:", "AG GECISI YETERLI" if A > 300 else "!!! MERKEZ DAR !!!")
