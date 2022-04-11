class KonfiguracjaGeneratora:
    pass

class KonfiguracjaJęzyka:
    nic = ""
    samogłoski = ['a', 'ą', 'e', 'ę', 'i', 'o', 'ó', 'u', 'y']
    # {"Fonem": ("Lewa ręka", "Prawa ręka")}
    fonemy_spółgłoskowe = {"b": ("PV", "KN"),
                           "bi": ("PVJ", "KNI"),
                           "c": ("TV", "WNT"),
                           "ci": ("TVJ", "WNTI"),
                           "ch": ("X", "ZWT"),
                           "chi": ("XJ", "ZWTI"),
                           "cz": ("XZ", "ZNT"),
                           "czi": ("XZJ", "ZNTI"),
                           "ć": ("TVJ", "WNTI"),
                           "d": ("D", "D"),
                           "di": ("DJ", "DI"),
                           "dz": ("ZD", "KD"),
                           "dzi": ("ZDJ", "KDI"),
                           "dź": ("ZDJ", "KDI"),
                           "dż": ("XFZD", "KZDW"),
                           "f": ("F", "EOAI"),
                           "fi": ("FJ", "TEOAI"),
                           "g": ("PK", "DN"),
                           "gi": ("PKJ", "DNI"),
                           "h": ("X", "ZWT"),
                           "hi": ("XJ", "ZWTI"),
                           "j": ("J", "NT"),
                           "ji": ("J", "NTI"),
                           "k": ("K", "K"),
                           "ki": ("KJ", "KI"),
                           "l": ("KR", "WT"),
                           "li": ("KRJ", "WTI"),
                           "ł": ("NK", "KWT"),
                           "łi": ("NKJ", "KWTI"),
                           "m": ("VR", "KNT"),
                           "mi": ("VRJ", "KNTI"),
                           "n": ("N", "N"),
                           "ni": ("NJ", "NI"),
                           "ń": ("NJ", "NI"),
                           "p": ("P", "DNT"),
                           "pi": ("PJ", "DNTI"),
                           "q": ("VK", "~O"),
                           "r": ("R", "ZT"),
                           "ri": ("RJ", "ZTI"),
                           "rz": ("FD", "KZ"),
                           "s": ("NT", "DW"),
                           "si": ("NTJ", "DWI"),
                           "sz": ("ZN", "ZW"),
                           "ś": ("NTJ", "ZWI"),
                           "t": ("T", "T"),
                           "ti": ("TJ", "TI"),
                           "v": ("V", "W"),
                           "vi": ("VJ", "WI"),
                           "w": ("V", "W"),
                           "wi": ("VJ", "WI"),
                           "x": ("XF", "~K"),
                           "xi": ("XFJ", "~KI"),
                           "z": ("Z", "Z"),
                           "zi": ("ZJ", "ZI"),
                           "ź": ("ZJ", "ZI"),
                           "ż": ("FD", "KZ")}


    fonemy_spółgłoskowe_klucze = ["b", "bi", "c", "ci", "ch", "chi", "cz", "czi", "ć",
                                  "d", "di", "dz", "dzi", "dź", "dż", "f", "fi", "g",
                                  "gi", "h", "hi", "j", "ji", "k", "ki", "l", "li",
                                  "ł", "łi", "m", "mi", "n", "ni", "ń", "p", "pi",
                                  "q", "r", "ri", "rz", "s", "si", "sz", "ś", "t", 
                                  "ti", "v", "vi", "w", "wi", "x", "xi", "z", "zi",
                                  "ź", "ż"]

    # {"Fonem": ("Środek", "Prawa ręka")}
    fonemy_samogłoskowe = {"a": ("A", "A"),
                           "ą": ("~O", "AI"),
                           "e": ("E", "E"),
                           "ę": ("E~", "EO"),
                           "i": ("I", "I"),
                           "o": ("AU", "O"),
                           "ó": ("U", nic),
                           # Tutaj zabrałem prawą rękę z "i"
                           "u": ("U", "OI"),
                           "y": ("IAU", "EA")}
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
    palce_prawe = [(tylda, gwiazdka, "K", "Z"),
                  ("D", "W"),
                  ("N", "T"),
                  ("E", "O", "A", "I")]
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
                              "K": 6, "Z": 6, "KZ": 6,
                              "D": 7, "W": 7, "DW": 7,
                              "N": 8, "T": 8, "NT": 8,
                              "E": 9, "O": 9, "EO": 9, "EA": 9, "OI": 9, "EOAI": 9,
                              "A": 10, "I": 10, "AI": 10}


    znaki_środka = [jot, ee, tylda, gwiazdka, ii, aa, uu]

