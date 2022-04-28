from enum import Enum

class KonfiguracjaGeneratora:
    minimum_kombinacji_per_słowo = 2

class KonfiguracjaJęzyka:
    spółgłoski = ['b', 'c', 'ć', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ł', 'm', 'n', 'ń', 'p', 'q', 'r', 's', 'ś', 't', 'v', 'w', 'x', 'z', 'ź', 'ż']
    nic = ""
    samogłoski = ['a', 'ą', 'e', 'ę', 'i', 'o', 'ó', 'u', 'y']
    jednoliterowe_wyrazy  = ['a', 'i', 'o', 'u', 'w', 'z']
    # {"Fonem": ("Lewa ręka", "Prawa ręka")}
    fonemy_spółgłoskowe = {"b": ("XP", "B"),  # zm. lewe z P~
                           "bi": ("XPJ", "BW"),  # zm. lewe z PJ~
                           "c": ("ZT", "C"),
                           "ci": ("ZTJ", "CW"),
                           "ch": ("X", "CB"),
                           "chi": ("XJ", "CBW"),
                           "cz": ("PV", "CL"),
                           "czi": ("PVJ", "CLW"),
                           "ć": ("ZTJ", "CW"),  # zm. lewe z TJ, prawe z TW
                           "d": ("FT", "BT"),  # zm. lewe z T~
                           "di": ("FTJ", "BTW"),  # zm. lewe z TJ~
                           "dz": ("ST", "C"),  # Dodałem
                           "dzi": ("STJ", "CW"),  # Dodałem
                           "dź": ("STJ", "LST"),  # zm. lewe z ZTJ~
                           "dż": ("FST", "RBTW"),  # zm. lewe z PV~, prawe z CLW
                           "dżi": ("FSTJ", "RBTW"),  # zm. lewe z PV~, prawe z CLW
                           "f": ("F", "W"),
                           "fi": ("FJ", "LT"),  # zm. prawe z W
                           "g": ("XK", "G"),  # zm. lewe z K~
                           "gi": ("XKJ", "GW"),  # zm. lewe z KJ~
                           "h": ("XF", "~CB"),  # zm. lewe z XK~, prawe z CB~
                           "hi": ("XFJ", "~CBW"),  # zm. lewe z XKJ~, prawe z CBW
                           "j": ("J", "CR"),
                           "ji": ("J", "CRW"),
                           "k": ("K", "ST"),  # zm. prawe z GW
                           "ki": ("KJ", "STW"),  # zm. prawe z GW
                           "l": ("L", "L"),
                           "li": ("LJ", "LW"),
                           "ł": ("LR", "LB"),  #  zm. lewe z LJ
                           "łi": ("LRJ", "LBW"),  #  zm. lewe z LJ
                           "m": ("KP", "CS"),
                           "mi": ("KPJ", "CSW"),
                           "n": ("TV", "LS"),  # zm. prawe z CL
                           "ni": ("TVJ", "LSW"),  # zm. prawe z CLW
                           "ń": ("TVJ", "LSW"),  # zm. prawe z CLW
                           # Tu zmieniłem prawą, bo nie ma "P" po prawej stronie
                           "p": ("P", "RG"),
                           "pi": ("PJ", "RGW"),
                           "q": ("KV", "GWY"),
                           "r": ("R", "R"),
                           "ri": ("RJ", "RW"),
                           "rz": ("VR", "RBW"),  # zm. lewe z RJ
                           "s": ("S", "S"),
                           "si": ("SJ", "SW"),
                           "sz": ("TP", "RB"),
                           "ś": ("SJ", "SW"),
                           "t": ("T", "T"),
                           "ti": ("TJ", "TW"),
                           "v": ("V", "W"),
                           "vi": ("VJ", "LT"),  # zm. prawe z W
                           "w": ("V", "W"),
                           "wi": ("VJ", "LT"),  # zm. prawe z ~W
                           "x": ("SK", "BSG"),
                           "xi": ("SKJ", "BSGW"),
                           "z": ("Z", "BS"),
                           "zi": ("ZJ", "BSW"),
                           "ź": ("ZJ", "BSW"),
                           "ż": ("XZ", "RBW")}  # zm. lewe z TP~


    fonemy_spółgłoskowe_klucze = ["b", "bi", "c", "ci", "ch", "chi", "cz", "czi", "ć",
                                  "d", "di", "dz", "dzi", "dź", "dż", "f", "fi", "g",
                                  "gi", "h", "hi", "j", "ji", "k", "ki", "l", "li",
                                  "ł", "łi", "m", "mi", "n", "ni", "ń", "p", "pi",
                                  "q", "r", "ri", "rz", "s", "si", "sz", "ś", "t", 
                                  "ti", "v", "vi", "w", "wi", "x", "xi", "z", "zi",
                                  "ź", "ż"]

    # {"Fonem": ("Środek", "Prawa ręka")}
    fonemy_samogłoskowe = {"a": ("A", "TO"),
                           "ą": ("UA", "TW"),
                           "e": ("E", "TWOY"),
                           "ę": ("EU", "OY"),
                           "i": ("J", "I"),
                           "o": ("AI", "O"),
                           "ó": ("U", nic),
                           # Tutaj zabrałem prawą rękę z "i"
                           "u": ("U", "WY"),
                           "y": ("UAI", "Y")}
    fonemy_samogłoskowe_klucze = ["a", "ą", "e", "ę", "i",
                                  "o", "ó", "u", "y",]

    fonemy_dwuznakowe = {"b": ["i"],
                             "c": ["h", "i", "z"],
                             "d": ["i", "z", "ź", "ż"],
                             "f": ["i"],
                             "g": ["i"],
                             "h": ["i"],
                             "j": ["i"],
                             "k": ["i"],
                             "l": ["i"],
                             "ł": ["i"],
                             "m": ["i"],
                             "n": ["i"],
                             "p": ["i"],
                             "r": ["i", "z"],
                             "s": ["i", "z"],
                             "t": ["i"],
                             "w": ["i"],
                             "z": ["i"]}


class KonfiguracjaKlawiatury:
    kolejność = '#/XFZSKTPVLRJE-~*UAICRLBSGTWOY'
    tylda = "~"
    gwiazdka = "*"
    myślnik = "-"
    jot = "J"
    ee = "E"
    ii = "I"
    aa = "A"
    uu = "U"

    palce_lewe = [("X", "F", "Z", "S"),
                  ("K", "T"),
                  ("P", "V"),
                  ("L", "R", tylda, gwiazdka),
                  (jot, ee, uu)]

    znaki_środka = [jot, ee, tylda, gwiazdka, uu, aa, ii]

    palce_prawe = [(uu, aa, ii),
                  (tylda, gwiazdka, "C", "R"),
                  ("L", "B"),
                  ("S", "G"),
                  ("T", "W", "O", "Y")]

    # indeksy kolumn po lewej stronie od 0
    lewe_indeksy_klawiszy = {"X": 0, "F": 0, "XF": 0, "XZ": 0, "FS": 0, "XFZS": 0,
                             "Z": 1, "S": 1, "ZS": 1,
                             "K": 2, "T": 2, "KT": 2,
                             "P": 3, "V": 3, "PV": 3, jot: 3,
                             "L": 4, "R": 4, "LR": 4, ee: 4,
                             tylda: 5, gwiazdka: 5, uu: 5}

    # indeksy kolumn po prawej stronie od 0
    prawe_indeksy_klawiszy = {tylda: 5, gwiazdka: 5, uu: 5,
                              "C": 6, "R": 6, "CR": 6, aa: 6,
                              "L": 7, "B": 7, "LB": 7, ii: 7,
                              "S": 8, "G": 8, "SG": 8,
                              "T": 9, "W": 9, "TW": 9, "TO": 9, "WY": 9, "TWOY": 9,
                              "O": 10, "Y": 10, "OY": 10}

class TypyGeneracji(Enum):
    StandardowaGeneracja = 1
    GeneracjaZnakówSpecjalnych = 2
    GeneracjaZModyfikatorami = 3
    SylabizowaniePoTrzy = 4
    SylabizowaniePoDwie = 5
    SylabizowaniePojedyncze = 6

class UstawienieFabryki:
    def __init__(self,
                 typ_generacji=TypyGeneracji.StandardowaGeneracja,
                 tylko_porażki_na_wejściu=False,
                 tylko_wyniki_porażek_na_wejściu=False,
                 sprawdzaj_czy_jednowyrazowe_słowo=False,
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
        self.sprawdzaj_czy_jednowyrazowe_słowo =sprawdzaj_czy_jednowyrazowe_słowo
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
  [UstawienieFabryki(sprawdzaj_czy_jednowyrazowe_słowo=True,
                     czy_klejone=True,
                     sprawdzaj_czy_jest_przedrostkiem=True),
   UstawienieFabryki(typ_generacji=TypyGeneracji.GeneracjaZnakówSpecjalnych,
                     tylko_wyniki_porażek_na_wejściu=True,
                     limit_niedopasowania=2)]

KonfiguracjaFabryki.ustawienia_fabryki["frekwencja_0"] =\
  [UstawienieFabryki(limit_prób=15,
                     sprawdzaj_czy_jest_przedrostkiem=True),
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
