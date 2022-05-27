from ustawienia.konfiguracja_fabryki import KonfiguracjaGeneratora
from ustawienia.konfiguracja_fabryki import KonfiguracjaFabryki
from ustawienia.konfiguracja_fabryki import TypyGeneracji


class KonfiguracjaJęzyka:
    spółgłoski = ['b', 'c', 'ć', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ł', 'm',
                  'n', 'ń', 'p', 'q', 'r', 's', 'ś', 't', 'v', 'w', 'x', 'z',
                  'ź', 'ż']
    nic = ""
    zmiękczenie = "i"
    samogłoski = ['a', 'ą', 'e', 'ę', 'i', 'o', 'ó', 'u', 'y']
    jednoliterowe_wyrazy  = ['a', 'i', 'o', 'u', 'w', 'z']
    # {"Fonem": ("Lewa ręka", "Prawa ręka")}
    fonemy_spółgłoskowe = {"b": ("XP", "B"),  # zm. lewe z P~
                           "bi": ("XPJ", "BI"),  # zm. lewe z PJ~
                           "c": ("ZT", "C"),
                           "ci": ("ZTJ", "CI"),
                           "ch": ("X", "CB"),
                           "chi": ("XJ", "CBI"),
                           "cz": ("PV", "CL"),
                           "czi": ("PVJ", "CLI"),
                           "ć": ("ZTJ", "CI"),  # zm. lewe z TJ, prawe z TW
                           "d": ("FT", "SG"),  # zm. lewe z T~
                           "di": ("FTJ", "ISG"),  # zm. lewe z TJ~
                           "dz": ("ST", "LG"),  # Dodałem
                           "dzi": ("STJ", "LIG"),  # Dodałem
                           "dź": ("STJ", "LIG"),  # zm. lewe z ZTJ~
                           "dż": ("FST", "BG"),  # zm. lewe z PV~, prawe z CLW
                           "dżi": ("FSTJ", "BIG"),  # zm. lewe z PV~, prawe z CLW
                           "f": ("F", "CG"),
                           "fi": ("FJ", "CIG"),  # zm. prawe z W
                           "g": ("XK", "G"),  # zm. lewe z K~
                           "gi": ("XKJ", "IG"),  # zm. lewe z KJ~
                           "h": ("X", "CB"),  # zm. lewe z XK~, prawe z CB~
                           "hi": ("XJ", "CBI"),  # zm. lewe z XKJ~, prawe z CBW
                           "j": ("J", "CR"),
                           "ji": ("J", "CRI"),
                           "k": ("K", "RL"),  # zm. prawe z GW
                           "ki": ("KJ", "RLI"),  # zm. prawe z GW
                           "l": ("L", "L"),
                           "li": ("LJ", "LI"),
                           "ł": ("LR", "LB"),  #  zm. lewe z LJ
                           "łi": ("LRJ", "LBI"),  #  zm. lewe z LJ
                           "m": ("KP", "CS"),
                           "mi": ("KPJ", "CIS"),
                           "n": ("TV", "LS"),  # zm. prawe z CL
                           "ni": ("TVJ", "LIS"),  # zm. prawe z CLW
                           "ń": ("TVJ", "LIS"),  # zm. prawe z CLW
                           # Tu zmieniłem prawą, bo nie ma "P" po prawej stronie
                           "p": ("P", "RG"),
                           "pi": ("PJ", "RIG"),
                           "q": ("KV", "~LB"),
                           "r": ("R", "R"),
                           "ri": ("RJ", "RI"),
                           "rz": ("XZ", "RS"),  # zm. lewe z RJ
                           "s": ("S", "S"),
                           "si": ("SJ", "IS"),
                           "sz": ("TP", "RB"),
                           "ś": ("SJ", "IS"),
                           "t": ("T", "T"),
                           "ti": ("TJ", "IT"),
                           "v": ("V~", "W~"),
                           "vi": ("VJ~", "IW~"),  # zm. prawe z W
                           "w": ("V", "W"),
                           "wi": ("VJ", "IW"),  # zm. prawe z ~W
                           "x": ("XF", "~SG"),
                           "xi": ("XFJ", "~ISG"),
                           "z": ("Z", "BS"),
                           "zi": ("ZJ", "BIS"),
                           "ź": ("ZJ", "BIS"),
                           "ż": ("XZ", "RS")}  # zm. lewe z TP~

    # {"Fonem": ("Środek", "Prawa ręka")}
    fonemy_samogłoskowe = {"a": ("A", "TO"),
                           "ą": ("UA", "TW"),
                           "e": ("E", "TWOY"),
                           "ę": ("EU", "OY"),
                           "i": ("J", "I"),
                           "o": ("AI", "O"),
                           "ó": ("U", "~O"),
                           # Tutaj zabrałem prawą rękę z "i"
                           "u": ("U", "WY"),
                           "y": ("EUA", "Y")}

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

    fonemy_niesamodzielne = ["ps", "st", "br"]
    for fonem in fonemy_spółgłoskowe.keys():
        if fonem == "ł":
            continue
        fonemy_niesamodzielne.append(fonem + "ł")
    for fonem in fonemy_spółgłoskowe.keys():
        if fonem == "ż":
            continue
        fonemy_niesamodzielne.append(fonem + "ż")
    for fonem in fonemy_spółgłoskowe.keys():
        if fonem == "rz":
            continue
        fonemy_niesamodzielne.append(fonem + "rz")


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
                  (jot, ee, uu, aa)]

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
                             tylda: 5, gwiazdka: 5, uu: 5,
                             aa: 6}

    # indeksy kolumn po prawej stronie od 0
    prawe_indeksy_klawiszy = {tylda: 5, gwiazdka: 5, uu: 5,
                              "C": 6, "R": 6, "CR": 6, aa: 6,
                              "L": 7, "B": 7, "LB": 7, ii: 7,
                              "S": 8, "G": 8, "SG": 8,
                              "T": 9, "W": 9, "TW": 9, "TO": 9, "WY": 9, "TWOY": 9,
                              "O": 10, "Y": 10, "OY": 10}
