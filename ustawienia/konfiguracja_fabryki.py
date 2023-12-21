from enum import Enum

class KonfiguracjaGeneratora:
    minimum_kombinacji_per_słowo = 1

class TypyGeneracji(Enum):
    StandardowaGeneracja = 1
    GeneracjaZnakówSpecjalnych = 2
    GeneracjaZModyfikatorami = 3
    SylabizowaniePoTrzy = 4
    SylabizowaniePoDwie = 5
    SylabizowaniePojedyncze = 6
    GeneracjaZDokładaniem = 7

class UstawienieFabryki:
    def __init__(self,
                 typ_generacji=TypyGeneracji.StandardowaGeneracja,
                 tylko_porażki_na_wejściu=False,
                 tylko_wyniki_porażek_na_wejściu=False,
                 sprawdzaj_czy_jednoliterowe_słowo=False,
                 czy_klejone=False,
                 z_przedrostkiem=False,
                 sprawdzaj_czy_jest_przedrostkiem=False,
                 jest_przedrostkiem=False,
                 jest_rdzeniem=False,
                 limit_niedopasowania=0,
                 limit_prób=10):
        self.typ_generacji= typ_generacji
        self.tylko_porażki_na_wejściu=tylko_porażki_na_wejściu
        self.tylko_wyniki_porażek_na_wejściu=tylko_wyniki_porażek_na_wejściu
        self.sprawdzaj_czy_jednoliterowe_słowo = sprawdzaj_czy_jednoliterowe_słowo
        self.czy_klejone = czy_klejone
        self.z_przedrostkiem = z_przedrostkiem
        self.sprawdzaj_czy_jest_przedrostkiem = sprawdzaj_czy_jest_przedrostkiem
        self.jest_przedrostkiem = jest_przedrostkiem
        self.jest_rdzeniem = jest_rdzeniem
        self.limit_niedopasowania = limit_niedopasowania
        self.limit_prób = limit_prób

class KonfiguracjaFabrykiClass:
    def __init__(self):
        self.ustawienia_fabryki = dict()
        self.loguj_postęp_co = 1000
        self.max_słów_na_akord = 7
        self.zawsze_startuj_wszystkie_linie = True
        self.minimum_kombinacji_dodanych_per_słowo = 3

KonfiguracjaFabryki = KonfiguracjaFabrykiClass()
KonfiguracjaFabryki.ustawienia_fabryki["litery"] =\
  [UstawienieFabryki(sprawdzaj_czy_jednoliterowe_słowo=True,
                     czy_klejone=True,
                     sprawdzaj_czy_jest_przedrostkiem=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZnakówSpecjalnych,
                     tylko_wyniki_porażek_na_wejściu=True,
                     limit_niedopasowania=2)]

KonfiguracjaFabryki.ustawienia_fabryki["jednosylabowiec"] =\
  [UstawienieFabryki(limit_prób=15,
                     limit_niedopasowania=5,
                     sprawdzaj_czy_jest_przedrostkiem=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZModyfikatorami,
                     tylko_wyniki_porażek_na_wejściu=True),
   # UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZnakówSpecjalnych,
   #                   tylko_wyniki_porażek_na_wejściu=True,
   #                   limit_niedopasowania=10)
   ]

KonfiguracjaFabryki.ustawienia_fabryki["dwusylabowiec"] =\
  [UstawienieFabryki(limit_prób=25,
                     limit_niedopasowania=10,
                     sprawdzaj_czy_jest_przedrostkiem=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZModyfikatorami,
                     tylko_wyniki_porażek_na_wejściu=True),
   # UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZnakówSpecjalnych,
   #                   tylko_wyniki_porażek_na_wejściu=True,
   #                   limit_niedopasowania=15)
   ]

KonfiguracjaFabryki.ustawienia_fabryki["frekwencja_0"] =\
  [UstawienieFabryki(limit_prób=15,
                     sprawdzaj_czy_jest_przedrostkiem=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZDokładaniem,
                     tylko_wyniki_porażek_na_wejściu=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZModyfikatorami,
                     tylko_wyniki_porażek_na_wejściu=True),
   UstawienieFabryki(z_przedrostkiem=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZModyfikatorami,
                     tylko_wyniki_porażek_na_wejściu=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.SylabizowaniePoTrzy,
                     limit_niedopasowania=1,
                     limit_prób=5),
   UstawienieFabryki(typ_generacji=TypyGeneracji.SylabizowaniePoDwie,
                     limit_niedopasowania=1,
                     limit_prób=5),
   UstawienieFabryki(typ_generacji=TypyGeneracji.SylabizowaniePojedyncze,
                     limit_niedopasowania=0,
                     limit_prób=5)]

KonfiguracjaFabryki.ustawienia_fabryki["frekwencja_1"] =\
  [UstawienieFabryki(limit_prób=15,
                     limit_niedopasowania=1,
                     sprawdzaj_czy_jest_przedrostkiem=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZDokładaniem,
                     limit_niedopasowania=1,
                     tylko_wyniki_porażek_na_wejściu=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZModyfikatorami,
                     tylko_wyniki_porażek_na_wejściu=True),
   UstawienieFabryki(z_przedrostkiem=True,
                    limit_niedopasowania=1),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZModyfikatorami,
                     tylko_wyniki_porażek_na_wejściu=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.SylabizowaniePoTrzy,
                     limit_niedopasowania=1,
                     limit_prób=5),
   UstawienieFabryki(typ_generacji=TypyGeneracji.SylabizowaniePoDwie,
                     limit_niedopasowania=1,
                     limit_prób=5),
   UstawienieFabryki(typ_generacji=TypyGeneracji.SylabizowaniePojedyncze,
                     limit_niedopasowania=0,
                     limit_prób=5)]

KonfiguracjaFabryki.ustawienia_fabryki["frekwencja_2"] =\
  [UstawienieFabryki(limit_prób=15,
                     limit_niedopasowania=2,
                     sprawdzaj_czy_jest_przedrostkiem=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZDokładaniem,
                     limit_niedopasowania=2,
                     tylko_wyniki_porażek_na_wejściu=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZModyfikatorami,
                     tylko_wyniki_porażek_na_wejściu=True),
   UstawienieFabryki(z_przedrostkiem=True,
                     limit_niedopasowania=2),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZModyfikatorami,
                     tylko_wyniki_porażek_na_wejściu=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.SylabizowaniePoTrzy,
                     limit_niedopasowania=1,
                     limit_prób=5),
   UstawienieFabryki(typ_generacji=TypyGeneracji.SylabizowaniePoDwie,
                     limit_niedopasowania=1,
                     limit_prób=5),
   UstawienieFabryki(typ_generacji=TypyGeneracji.SylabizowaniePojedyncze,
                     limit_niedopasowania=0,
                     limit_prób=5)]

KonfiguracjaFabryki.ustawienia_fabryki["frekwencja_3"] =\
  [UstawienieFabryki(limit_prób=15,
                     limit_niedopasowania=3,
                     sprawdzaj_czy_jest_przedrostkiem=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZDokładaniem,
                     limit_niedopasowania=3,
                     tylko_wyniki_porażek_na_wejściu=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZModyfikatorami,
                     tylko_wyniki_porażek_na_wejściu=True),
   UstawienieFabryki(z_przedrostkiem=True,
                     limit_niedopasowania=3),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZModyfikatorami,
                     tylko_wyniki_porażek_na_wejściu=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.SylabizowaniePoTrzy,
                     limit_niedopasowania=1,
                     limit_prób=5),
   UstawienieFabryki(typ_generacji=TypyGeneracji.SylabizowaniePoDwie,
                     limit_niedopasowania=1,
                     limit_prób=5),
   UstawienieFabryki(typ_generacji=TypyGeneracji.SylabizowaniePojedyncze,
                     limit_niedopasowania=0,
                     limit_prób=5)]

KonfiguracjaFabryki.ustawienia_fabryki["frekwencja_4"] =\
  [UstawienieFabryki(limit_prób=15,
                     limit_niedopasowania=4,
                     sprawdzaj_czy_jest_przedrostkiem=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZDokładaniem,
                     limit_niedopasowania=4,
                     tylko_wyniki_porażek_na_wejściu=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZModyfikatorami,
                     tylko_wyniki_porażek_na_wejściu=True),
   UstawienieFabryki(z_przedrostkiem=True,
                     limit_niedopasowania=4),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZModyfikatorami,
                     tylko_wyniki_porażek_na_wejściu=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.SylabizowaniePoTrzy,
                     limit_niedopasowania=1,
                     limit_prób=5),
   UstawienieFabryki(typ_generacji=TypyGeneracji.SylabizowaniePoDwie,
                     limit_niedopasowania=1,
                     limit_prób=5),
   UstawienieFabryki(typ_generacji=TypyGeneracji.SylabizowaniePojedyncze,
                     limit_niedopasowania=0,
                     limit_prób=5)]

KonfiguracjaFabryki.ustawienia_fabryki["frekwencja_5"] =\
  [UstawienieFabryki(limit_prób=15,
                     limit_niedopasowania=5,
                     sprawdzaj_czy_jest_przedrostkiem=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZDokładaniem,
                     limit_niedopasowania=5,
                     tylko_wyniki_porażek_na_wejściu=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZModyfikatorami,
                     tylko_wyniki_porażek_na_wejściu=True),
   UstawienieFabryki(z_przedrostkiem=True,
                     limit_niedopasowania=5),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZModyfikatorami,
                     tylko_wyniki_porażek_na_wejściu=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.SylabizowaniePoTrzy,
                     limit_niedopasowania=1,
                     limit_prób=5),
   UstawienieFabryki(typ_generacji=TypyGeneracji.SylabizowaniePoDwie,
                     limit_niedopasowania=1,
                     limit_prób=5),
   UstawienieFabryki(typ_generacji=TypyGeneracji.SylabizowaniePojedyncze,
                     limit_niedopasowania=0,
                     limit_prób=5)]

KonfiguracjaFabryki.ustawienia_fabryki["frekwencja_6"] =\
  [UstawienieFabryki(limit_prób=15,
                     limit_niedopasowania=6,
                     sprawdzaj_czy_jest_przedrostkiem=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZDokładaniem,
                     limit_niedopasowania=6,
                     tylko_wyniki_porażek_na_wejściu=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZModyfikatorami,
                     tylko_wyniki_porażek_na_wejściu=True),
   UstawienieFabryki(z_przedrostkiem=True,
                     limit_niedopasowania=6),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZModyfikatorami,
                     tylko_wyniki_porażek_na_wejściu=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.SylabizowaniePoTrzy,
                     limit_niedopasowania=1,
                     limit_prób=5),
   UstawienieFabryki(typ_generacji=TypyGeneracji.SylabizowaniePoDwie,
                     limit_niedopasowania=1,
                     limit_prób=5),
   UstawienieFabryki(typ_generacji=TypyGeneracji.SylabizowaniePojedyncze,
                     limit_niedopasowania=0,
                     limit_prób=5)]

KonfiguracjaFabryki.ustawienia_fabryki["frekwencja_7"] =\
  [UstawienieFabryki(limit_prób=15,
                     limit_niedopasowania=7,
                     sprawdzaj_czy_jest_przedrostkiem=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZDokładaniem,
                     limit_niedopasowania=7,
                     tylko_wyniki_porażek_na_wejściu=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZModyfikatorami,
                     tylko_wyniki_porażek_na_wejściu=True),
   UstawienieFabryki(z_przedrostkiem=True,
                     limit_niedopasowania=7),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZModyfikatorami,
                     tylko_wyniki_porażek_na_wejściu=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.SylabizowaniePoTrzy,
                     limit_niedopasowania=1,
                     limit_prób=5),
   UstawienieFabryki(typ_generacji=TypyGeneracji.SylabizowaniePoDwie,
                     limit_niedopasowania=1,
                     limit_prób=5),
   UstawienieFabryki(typ_generacji=TypyGeneracji.SylabizowaniePojedyncze,
                     limit_niedopasowania=0,
                     limit_prób=5)]

KonfiguracjaFabryki.ustawienia_fabryki["frekwencja_8"] =\
  [UstawienieFabryki(limit_prób=15,
                     limit_niedopasowania=8,
                     sprawdzaj_czy_jest_przedrostkiem=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZDokładaniem,
                     limit_niedopasowania=8,
                     tylko_wyniki_porażek_na_wejściu=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZModyfikatorami,
                     tylko_wyniki_porażek_na_wejściu=True),
   UstawienieFabryki(z_przedrostkiem=True,
                     limit_niedopasowania=8),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZModyfikatorami,
                     tylko_wyniki_porażek_na_wejściu=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.SylabizowaniePoTrzy,
                     limit_niedopasowania=1,
                     limit_prób=5),
   UstawienieFabryki(typ_generacji=TypyGeneracji.SylabizowaniePoDwie,
                     limit_niedopasowania=1,
                     limit_prób=5),
   UstawienieFabryki(typ_generacji=TypyGeneracji.SylabizowaniePojedyncze,
                     limit_niedopasowania=0,
                     limit_prób=5)]

KonfiguracjaFabryki.ustawienia_fabryki["frekwencja_9"] =\
  [UstawienieFabryki(limit_prób=15,
                     limit_niedopasowania=9,
                     sprawdzaj_czy_jest_przedrostkiem=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZDokładaniem,
                     limit_niedopasowania=9,
                     tylko_wyniki_porażek_na_wejściu=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZModyfikatorami,
                     tylko_wyniki_porażek_na_wejściu=True),
   UstawienieFabryki(z_przedrostkiem=True,
                     limit_niedopasowania=9),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZModyfikatorami,
                     tylko_wyniki_porażek_na_wejściu=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.SylabizowaniePoTrzy,
                     limit_niedopasowania=1,
                     limit_prób=5),
   UstawienieFabryki(typ_generacji=TypyGeneracji.SylabizowaniePoDwie,
                     limit_niedopasowania=1,
                     limit_prób=5),
   UstawienieFabryki(typ_generacji=TypyGeneracji.SylabizowaniePojedyncze,
                     limit_niedopasowania=0,
                     limit_prób=5)]

KonfiguracjaFabryki.ustawienia_fabryki["frekwencja_10"] =\
  [UstawienieFabryki(limit_prób=15,
                     limit_niedopasowania=10,
                     sprawdzaj_czy_jest_przedrostkiem=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZDokładaniem,
                     limit_niedopasowania=10,
                     tylko_wyniki_porażek_na_wejściu=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZModyfikatorami,
                     tylko_wyniki_porażek_na_wejściu=True),
   UstawienieFabryki(z_przedrostkiem=True,
                     limit_niedopasowania=10),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZModyfikatorami,
                     tylko_wyniki_porażek_na_wejściu=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.SylabizowaniePoTrzy,
                     limit_niedopasowania=1,
                     limit_prób=5),
   UstawienieFabryki(typ_generacji=TypyGeneracji.SylabizowaniePoDwie,
                     limit_niedopasowania=1,
                     limit_prób=5),
   UstawienieFabryki(typ_generacji=TypyGeneracji.SylabizowaniePojedyncze,
                     limit_niedopasowania=0,
                     limit_prób=5)]

KonfiguracjaFabryki.ustawienia_fabryki["przedrostki"] =\
  [UstawienieFabryki(limit_niedopasowania=1,
                     jest_przedrostkiem=True,
                     limit_prób=10),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZModyfikatorami,
                     jest_przedrostkiem=True,
                     tylko_wyniki_porażek_na_wejściu=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZnakówSpecjalnych,
                     jest_przedrostkiem=True,
                     tylko_wyniki_porażek_na_wejściu=True,
                     limit_niedopasowania=3)]

KonfiguracjaFabryki.ustawienia_fabryki["rdzeń"] =\
  [UstawienieFabryki(limit_prób=15,
                     limit_niedopasowania=8,
                     jest_rdzeniem=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.SylabizowaniePoTrzy,
                     limit_niedopasowania=3,
                     jest_rdzeniem=True,
                     limit_prób=5),
   UstawienieFabryki(typ_generacji=TypyGeneracji.SylabizowaniePoDwie,
                     limit_niedopasowania=3,
                     jest_rdzeniem=True,
                     limit_prób=5)]

KonfiguracjaFabryki.ustawienia_fabryki["sylaba"] =\
  [UstawienieFabryki(czy_klejone=True,
                     limit_niedopasowania=6,
                     sprawdzaj_czy_jest_przedrostkiem=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZnakówSpecjalnych,
                     czy_klejone=True,
                     sprawdzaj_czy_jest_przedrostkiem=True,
                     tylko_wyniki_porażek_na_wejściu=True,
                     limit_niedopasowania=8),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZModyfikatorami,
                     czy_klejone=True,
                     sprawdzaj_czy_jest_przedrostkiem=True,
                     tylko_wyniki_porażek_na_wejściu=True)]

KonfiguracjaFabryki.ustawienia_fabryki["sylaby"] =\
  [UstawienieFabryki(czy_klejone=True,
                     limit_niedopasowania=5,
                     sprawdzaj_czy_jest_przedrostkiem=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZnakówSpecjalnych,
                     czy_klejone=True,
                     sprawdzaj_czy_jest_przedrostkiem=True,
                     tylko_wyniki_porażek_na_wejściu=True,
                     limit_niedopasowania=7)]
