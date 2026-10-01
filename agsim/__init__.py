"""Ag firlatma mekanizmasi - cok fazli modelleme ve tasarim uzayi kesfi.

Fazlar:
  launcher.py   Faz-0  yay ic balistigi  -> namlu cikis hizi, geri tepme, yay tahkiki
  netrom.py     Faz-1a hizli ag modeli (6-DOF ROM)   -> tasarim kesfi icin
  netfull.py    Faz-1b kutle-yay-sonumleyici ag      -> kalibrasyon + dogrulama
  engagement.py Faz-2  goreli kinematik, etkin menzil, yakalama olcutu
  dse.py        Faz-3  Sobol taramasi, duyarlilik, Pareto, optimizasyon

Betikler:  run_baseline.py, run_dse.py, run_dogrula.py
"""
__all__ = ["params","aero","launcher","netrom","netfull","engagement","dse"]
