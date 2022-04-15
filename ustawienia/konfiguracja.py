class KonfiguracjaGeneratora:
    pass

class KonfiguracjaJęzyka:
    spółgłoski = ['b', 'c', 'ć', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ł', 'm', 'n', 'ń', 'p', 'q', 'r', 's', 'ś', 't', 'v', 'w', 'x', 'z', 'ź', 'ż']
    nic = ""
    samogłoski = ['a', 'ą', 'e', 'ę', 'i', 'o', 'ó', 'u', 'y']
    jednoliterowe_wyrazy  = ['a', 'i', 'o', 'u', 'w', 'z']
    # {"Fonem": ("Lewa ręka", "Prawa ręka")}
    fonemy_spółgłoskowe = {"b": ("PV", "KN"),
                           "bi": ("PVJ", "KNC"),
                           "c": ("TV", "WNT"),
                           "ci": ("TVJ", "WNTC"),
                           "ch": ("X", "ZWT"),
                           "chi": ("XJ", "ZWTC"),
                           "cz": ("XZ", "ZNT"),
                           "czi": ("XZJ", "ZNTC"),
                           "ć": ("TVJ", "WNTC"),
                           "d": ("D", "D"),
                           "di": ("DJ", "DC"),
                           "dz": ("ZD", "KD"),
                           "dzi": ("ZDJ", "KDC"),
                           "dź": ("ZDJ", "KDC"),
                           "dż": ("XFZD", "KZDW"),
                           "f": ("F", "YOBC"),
                           "fi": ("FJ", "TYOBC"),
                           "g": ("PK", "DN"),
                           "gi": ("PKJ", "DNC"),
                           "h": ("X", "ZWT"),
                           "hi": ("XJ", "ZWTC"),
                           "j": ("J", "NT"),
                           "ji": ("J", "NTC"),
                           "k": ("K", "K"),
                           "ki": ("KJ", "KC"),
                           "l": ("KR", "WT"),
                           "li": ("KRJ", "WTC"),
                           "ł": ("NK", "KWT"),
                           "łi": ("NKJ", "KWTC"),
                           "m": ("VR", "KNT"),
                           "mi": ("VRJ", "KNTC"),
                           "n": ("N", "N"),
                           "ni": ("NJ", "NC"),
                           "ń": ("NJ", "NC"),
                           "p": ("P", "DNT"),
                           "pi": ("PJ", "DNTC"),
                           "q": ("VK", "~O"),
                           "r": ("R", "ZT"),
                           "ri": ("RJ", "ZTC"),
                           "rz": ("FD", "KZ"),
                           "s": ("NT", "DW"),
                           "si": ("NTJ", "DWC"),
                           "sz": ("ZN", "ZW"),
                           "ś": ("NTJ", "ZWC"),
                           "t": ("T", "T"),
                           "ti": ("TJ", "TC"),
                           "v": ("V", "W"),
                           "vi": ("VJ", "WC"),
                           "w": ("V", "W"),
                           "wi": ("VJ", "WC"),
                           "x": ("XF", "~K"),
                           "xi": ("XFJ", "~KC"),
                           "z": ("Z", "Z"),
                           "zi": ("ZJ", "ZC"),
                           "ź": ("ZJ", "ZC"),
                           "ż": ("FD", "KZ")}


    fonemy_spółgłoskowe_klucze = ["b", "bi", "c", "ci", "ch", "chi", "cz", "czi", "ć",
                                  "d", "di", "dz", "dzi", "dź", "dż", "f", "fi", "g",
                                  "gi", "h", "hi", "j", "ji", "k", "ki", "l", "li",
                                  "ł", "łi", "m", "mi", "n", "ni", "ń", "p", "pi",
                                  "q", "r", "ri", "rz", "s", "si", "sz", "ś", "t", 
                                  "ti", "v", "vi", "w", "wi", "x", "xi", "z", "zi",
                                  "ź", "ż"]

    # {"Fonem": ("Środek", "Prawa ręka")}
    fonemy_samogłoskowe = {"a": ("A", "B"),
                           "ą": ("~A", "BC"),
                           "e": ("E", "Y"),
                           "ę": ("E~", "YO"),
                           "i": ("I", "C"),
                           "o": ("AU", "O"),
                           "ó": ("U", nic),
                           # Tutaj zabrałem prawą rękę z "i"
                           "u": ("U", "OC"),
                           "y": ("IAU", "YB")}
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
                  ("Y", "O", "B", "C")]
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
                              "Y": 9, "O": 9, "YO": 9, "YB": 9, "OC": 9, "YOBC": 9,
                              "B": 10, "C": 10, "BC": 10}


    znaki_środka = [jot, ee, tylda, gwiazdka, ii, aa, uu]

