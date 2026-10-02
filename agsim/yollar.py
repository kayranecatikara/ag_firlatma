"""YOL COZUMLEME — betikler nereden calistirilirsa calistirilsin dogru yolu bulur.

Onceki surumde her betikte `sys.path.insert(0, '/home/kayra/...')` gibi
MUTLAK yol gomuluydu: baska makinede calismiyordu ve depo yeniden
duzenlenince 33 dosya birden kiriliyordu. Artik yollar __file__'dan
turetiliyor.

Kullanim (betigin basinda):
    import os, sys
    _K = os.path.abspath(__file__)
    while _K != os.path.dirname(_K) and not os.path.isdir(os.path.join(_K, "agsim")):
        _K = os.path.dirname(_K)
    sys.path.insert(0, _K)
    from agsim.yollar import KOK, varyant
    VAR = varyant(__file__)
"""
import os


def kok():
    """Depo koku = `agsim/` paketinin bulundugu dizin."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


KOK = kok()


def varyant(dosya):
    """Betigin ait oldugu VARYANT koku (orn. .../esnek_bantli).

    Kokun hemen altindaki ilk klasor varyant kabul edilir. Kokte duran
    bir betik icin kokun kendisini doner.
    """
    p = os.path.abspath(dosya)
    rel = os.path.relpath(p, KOK).split(os.sep)
    return os.path.join(KOK, rel[0]) if len(rel) > 1 else KOK


def vyol(dosya, *parcalar):
    """Varyant kokune gore yol kur:  vyol(__file__, 'out', 'x.json')"""
    return os.path.join(varyant(dosya), *parcalar)


def kyol(*parcalar):
    """Depo kokune gore yol kur:  kyol('gazebo', 'models')"""
    return os.path.join(KOK, *parcalar)
