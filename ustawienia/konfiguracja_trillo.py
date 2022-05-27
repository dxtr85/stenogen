from ustawienia.konfiguracja_fabryki import KonfiguracjaGeneratora
from ustawienia.konfiguracja_fabryki import KonfiguracjaFabryki
from ustawienia.konfiguracja_fabryki import TypyGeneracji

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

    # {"Fonem": ("Środek", "Prawa ręka")}
    fonemy_samogłoskowe = {"a": ("A", "TO"),
                           "ą": ("~A", "TW"),
                           "e": ("E", "TWOY"),
                           "ę": ("E~", "OY"),
                           "i": ("I", nic),
                           "o": ("AU", "O"),
                           "ó": ("U", nic),
                           # Tutaj zabrałem prawą rękę z "i"
                           "u": ("U", "WY"),
                           "y": ("IAU", "Y")}

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
    kolejność = '#/XFZSKTPVLRJE-~*IAUCRLBSGTWOY'
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
                  ("J", "E", "I")]

    znaki_środka = [jot, ee, tylda, gwiazdka, ii, aa, uu]

    palce_prawe = [("I", "A", "U"),
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
                             tylda: 5, gwiazdka: 5, ii: 5}

    # indeksy kolumn po prawej stronie od 0
    prawe_indeksy_klawiszy = {tylda: 5, gwiazdka: 5, ii: 5,
                              "C": 6, "R": 6, "CR": 6, aa: 6,
                              "L": 7, "B": 7, "LB": 7, uu: 7,
                              "S": 8, "G": 8, "SG": 8,
                              "T": 9, "W": 9, "TW": 9, "TO": 9, "WY": 9, "TWOY": 9,
                              "O": 10, "Y": 10, "OY": 10}
