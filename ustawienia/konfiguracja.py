class KonfiguracjaGeneratora:
    pass

class KonfiguracjaJęzyka:
    nic = ""
    samogłoski = ['a', 'ą', 'e', 'ę', 'i', 'o', 'ó', 'u', 'y']
    # {"Fonem": ("Lewa ręka", "Prawa ręka")}
    fonemy_spółgłoskowe = {"b": ("PV", "B"),  # zm. lewe z P~
                           "bi": ("PVJ", "BW"),  # zm. lewe z PJ~
                           "c": ("TV", "C"),
                           "ci": ("TVJ", "CW"),
                           "ch": ("X", "CB"),
                           "chi": ("XJ", "CBW"),
                           "cz": ("XZ", "CL"),
                           "czi": ("XZJ", "CLW"),
                           "ć": ("TVJ", "CW"),  # zm. lewe z TJ, prawe z TW
                           "d": ("D", "BT"),  # zm. lewe z T~
                           "di": ("DJ", "BTW"),  # zm. lewe z TJ~
                           "dz": ("ZD", "C"),  # Dodałem
                           "dzi": ("ZDJ", "CW"),  # Dodałem
                           "dź": ("ZDJ", "LST"),  # zm. lewe z ZTJ~
                           "dż": ("XFZD", "RBTW"),  # zm. lewe z PV~, prawe z CLW
                           "f": ("F", "W"),
                           "fi": ("FJ", "LT"),  # zm. prawe z W
                           "g": ("PK", "G"),  # zm. lewe z K~
                           "gi": ("PKJ", "GW"),  # zm. lewe z KJ~
                           "h": ("X", "~CB"),  # zm. lewe z XK~, prawe z CB~
                           "hi": ("XJ", "~CBW"),  # zm. lewe z XKJ~, prawe z CBW
                           "j": ("J", "CR"),
                           "ji": ("J", "CRW"),
                           "k": ("K", "ST"),  # zm. prawe z GW
                           "ki": ("KJ", "STW"),  # zm. prawe z GW
                           "l": ("KR", "L"),
                           "li": ("KRJ", "LW"),
                           "ł": ("NK", "LB"),  #  zm. lewe z LJ
                           "łi": ("NKJ", "LBW"),  #  zm. lewe z LJ
                           "m": ("VR", "CS"),
                           "mi": ("VRJ", "CSW"),
                           "n": ("N", "LS"),  # zm. prawe z CL
                           "ni": ("NJ", "LSW"),  # zm. prawe z CLW
                           "ń": ("NJ", "LSW"),  # zm. prawe z CLW
                           # Tu zmieniłem prawą, bo nie ma "P" po prawej stronie
                           "p": ("P", "RG"),
                           "pi": ("PJ", "RGW"),
                           "q": ("VK", "GWY"),
                           "r": ("R", "R"),
                           "ri": ("RJ", "RW"),
                           "rz": ("FD", "RBW"),  # zm. lewe z RJ
                           "s": ("NT", "S"),
                           "si": ("NTJ", "SW"),
                           "sz": ("ZN", "RB"),
                           "ś": ("NTJ", "SW"),
                           "t": ("T", "T"),
                           "ti": ("TJ", "TW"),
                           "v": ("V", "W"),
                           "vi": ("VJ", "LT"),  # zm. prawe z W
                           "w": ("V", "W"),
                           "wi": ("VJ", "LT"),  # zm. prawe z ~W
                           "x": ("XF", "BSG"),
                           "xi": ("XFJ", "BSGW"),
                           "z": ("Z", "BS"),
                           "zi": ("ZJ", "BSW"),
                           "ź": ("ZJ", "BSW"),
                           "ż": ("FD", "RBW")}  # zm. lewe z TP~


    fonemy_spółgłoskowe_klucze = ["b", "bi", "c", "ci", "ch", "chi", "cz", "czi", "ć",
                                  "d", "di", "dz", "dzi", "dź", "dż", "f", "fi", "g",
                                  "gi", "h", "hi", "j", "ji", "k", "ki", "l", "li",
                                  "ł", "łi", "m", "mi", "n", "ni", "ń", "p", "pi",
                                  "q", "r", "ri", "rz", "s", "si", "sz", "ś", "t", 
                                  "ti", "v", "vi", "w", "wi", "x", "xi", "z", "zi",
                                  "ź", "ż"]

    # {"Fonem": ("Środek", "Prawa ręka")}
    fonemy_samogłoskowe = {"a": ("A", "TO"),
                           "ą": ("~O", "TW"),
                           "e": ("E", "TWOY"),
                           "ę": ("E~", "OY"),
                           "i": ("I", "W"),
                           "o": ("AU", "O"),
                           "ó": ("U", nic),
                           # Tutaj zabrałem prawą rękę z "i"
                           "u": ("U", "WY"),
                           "y": ("IAU", "Y")}
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
    tylda = "~"
    gwiazdka = "*"
    myślnik = "-"
    jot = "J"
    ee = "E"
    ii = "I"
    aa = "A"
    uu = "U"

    palce_lewe = [("X", "F", "Z", "D"),
                  ("N", "T"),
                  ("P", "V"),
                  ("K", "R", tylda, gwiazdka),
                  ("J", "E")]
    palce_prawe = [(tylda, gwiazdka, "C", "R"),
                  ("L", "B"),
                  ("S", "G"),
                  ("T", "W", "O", "Y")]
    # indeksy kolumn po lewej stronie od 0
    lewe_indeksy_klawiszy = {"X": 0, "F": 0, "XF": 0, "XZ": 0, "FD": 0, "XFZD": 0,
                             "Z": 1, "D": 1, "ZD": 1,
                             "N": 2, "T": 2, "NT": 2,
                             "P": 3, "V": 3, "PV": 3,
                             "K": 4, "R": 4, "KR": 4,
                             tylda: 5, gwiazdka: 5,
                             jot: 6}


    # indeksy kolumn po prawej stronie od 0
    prawe_indeksy_klawiszy = {tylda: 5, gwiazdka: 5,
                              "C": 6, "R": 6, "CR": 6,
                              "L": 7, "B": 7, "LB": 7,
                              "S": 8, "G": 8, "SG": 8,
                              "T": 9, "W": 9, "TW": 9, "TO": 9, "WY": 9, "TWOY": 9,
                              "O": 10, "Y": 10, "OY": 10}


    znaki_środka = [jot, ee, tylda, gwiazdka, ii, aa, uu]

