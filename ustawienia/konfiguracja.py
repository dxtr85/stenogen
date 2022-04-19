class KonfiguracjaGeneratora:
    pass

class KonfiguracjaJęzyka:
    spółgłoski = ['b', 'c', 'ć', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ł', 'm', 'n', 'ń', 'p', 'q', 'r', 's', 'ś', 't', 'v', 'w', 'x', 'z', 'ź', 'ż']
    nic = ""
    samogłoski = ['a', 'ą', 'e', 'ę', 'i', 'o', 'ó', 'u', 'y']
    jednoliterowe_wyrazy  = ['a', 'i', 'o', 'u', 'w', 'z']
    # {"Fonem": ("Lewa ręka", "Prawa ręka")}
    fonemy_spółgłoskowe = {"b": ("PV", "KN"),
                           "bi": ("PVI", "KNC"),
                           "c": ("TV", "WNT"),
                           "ci": ("TVI", "WNTC"),
                           "ch": ("X", "ZWT"),
                           "chi": ("XI", "ZWTC"),
                           "cz": ("XZ", "ZNT"),
                           "czi": ("XZI", "ZNTC"),
                           "ć": ("TVI", "WNTC"),
                           "d": ("D", "D"),
                           "di": ("DI", "DC"),
                           "dz": ("ZD", "KD"),
                           "dzi": ("ZDI", "KDC"),
                           "dź": ("ZDI", "KDC"),
                           "dż": ("XFZD", "KZDW"),
                           "f": ("F", "YOBC"),
                           "fi": ("FI", "TYOBC"),
                           "g": ("PK", "DN"),
                           "gi": ("PKI", "DNC"),
                           "h": ("X", "ZWT"),
                           "hi": ("XI", "ZWTC"),
                           "j": ("J", "NT"),
                           "ji": ("J", "NTC"),
                           "k": ("K", "K"),
                           "ki": ("KI", "KC"),
                           "l": ("KR", "WT"),
                           "li": ("KRI", "WTC"),
                           "ł": ("NK", "KWT"),
                           "łi": ("NKI", "KWTC"),
                           "m": ("VR", "KNT"),
                           "mi": ("VRI", "KNTC"),
                           "n": ("N", "N"),
                           "ni": ("NI", "NC"),
                           "ń": ("NI", "NC"),
                           "p": ("P", "DNT"),
                           "pi": ("PI", "DNTC"),
                           "q": ("VK", "~O"),
                           "r": ("R", "ZT"),
                           "ri": ("RI", "ZTC"),
                           "rz": ("FD", "KZ"),
                           "s": ("NT", "DW"),
                           "si": ("NTI", "DWC"),
                           "sz": ("ZN", "ZW"),
                           "ś": ("NTI", "ZWC"),
                           "t": ("T", "T"),
                           "ti": ("TI", "TC"),
                           "v": ("V", "W"),
                           "vi": ("VI", "WC"),
                           "w": ("V", "W"),
                           "wi": ("VI", "WC"),
                           "x": ("XF", "~K"),
                           "xi": ("XFI", "~KC"),
                           "z": ("Z", "Z"),
                           "zi": ("ZI", "ZC"),
                           "ź": ("ZI", "ZC"),
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
    kolejność = '/XFZDNTPVKRJE-~*IAUKZDWNTYOBC'
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
                  ("J", "E", "I")]
    palce_prawe = [("I", "A", "U"),
                  (tylda, gwiazdka, "K", "Z"),
                  ("D", "W"),
                  ("N", "T"),
                  ("Y", "O", "B", "C")]
    # indeksy kolumn po lewej stronie od 0
    lewe_indeksy_klawiszy = {"X": 0, "F": 0, "XF": 0, "XZ": 0, "FD": 0, "XFZD": 0,
                             "Z": 1, "D": 1, "ZD": 1,
                             "N": 2, "T": 2, "NT": 2,
                             "P": 3, "V": 3, "PV": 3, jot: 3,
                             "K": 4, "R": 4, "KR": 4, ee: 4,
                             tylda: 5, gwiazdka: 5, ii: 5}


    # indeksy kolumn po prawej stronie od 0
    prawe_indeksy_klawiszy = {tylda: 5, gwiazdka: 5, ii: 5,
                              "K": 6, "Z": 6, "KZ": 6, aa: 6,
                              "D": 7, "W": 7, "DW": 7, uu:7,
                              "N": 8, "T": 8, "NT": 8,
                              "Y": 9, "O": 9, "YO": 9, "YB": 9, "OC": 9, "YOBC": 9,
                              "B": 10, "C": 10, "BC": 10}


    znaki_środka = [jot, ee, tylda, gwiazdka, ii, aa, uu]

