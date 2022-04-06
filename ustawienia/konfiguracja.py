class KonfiguracjaGeneratora:
    pass

class KonfiguracjaJęzyka:
    nic = ""
    samogłoski = ['a', 'ą', 'e', 'ę', 'i', 'o', 'ó', 'u', 'y']
    # {"Fonem": ("Lewa ręka", "Prawa ręka")}
    fonemy_spółgłoskowe = {"b": ("P~", "B"),
                           "bi": ("PJ~", "BW"),
                           "c": ("ZT", "C"),
                           "ci": ("ZTJ", "CW"),
                           "ch": ("X", "CB"),
                           "chi": ("XJ", "CBW"),
                           "cz": ("PV", "CL"),
                           "czi": ("PVJ", "CLW"),
                           "ć": ("TJ", "TW"),
                           "d": ("T~", "BT"),
                           "di": ("TJ~", "BTW"),
                           "dz": ("ZT~", "C"),  # Dodałem
                           "dzi": ("ZTJ~", "CW"),  # Dodałem
                           "dź": ("ZTJ~", "LST"),
                           "dż": ("PV~", "CLW"),
                           "f": ("F", "W"),
                           "fi": ("FJ", "W"),
                           "g": ("K~", "G"),
                           "gi": ("KJ~", "GW"),
                           "h": ("X~", "CBW"),  # Zamieniłem z XK~
                           "hi": ("XJ~", "CBW"),  # Zamieniłem z XKJ~
                           "j": ("J", "CR"),
                           "ji": ("J", "CRW"),
                           "k": ("K", "GW"),
                           "ki": ("KJ", "GW"),
                           "l": ("L", "L"),
                           "li": ("LJ", "LW"),
                           "ł": ("LJ", "LB"),
                           "łi": ("LJ", "LBW"),
                           "m": ("KP", "CS"),
                           "mi": ("KPJ", "CSW"),
                           "n": ("TV", "CL"),
                           "ni": ("TVJ", "CLW"),
                           "ń": ("TVJ", "CLW"),
                           # Tu zmieniłem prawą, bo nie ma "P" po prawej stronie
                           "p": ("P", "RG"),
                           "pi": ("PJ", "RGW"),
                           "q": ("KV", "GWY"),
                           "r": ("R", "R"),
                           "ri": ("RJ", "RW"),
                           "rz": ("RJ", "RBW"),
                           "s": ("S", "S"),
                           "si": ("SJ", "SW"),
                           "sz": ("TP", "RB"),
                           "ś": ("SJ", "SW"),
                           "t": ("T", "T"),
                           "ti": ("TJ", "TW"),
                           "v": ("V", "W"),
                           "vi": ("VJ", "W"),
                           "w": ("V", "W"),
                           "wi": ("VJ", "~W"),
                           "x": ("SK", "BSG"),
                           "xi": ("SKJ", "BSGW"),
                           "z": ("Z", "BS"),
                           "zi": ("ZJ", "BSW"),
                           "ź": ("ZJ", "BSW"),
                           "ż": ("TP~", "RBW")}


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
                           "i": ("I", nic),
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

    # indeksy kolumn po lewej stronie od 0
    lewe_indeksy_klawiszy = {"X": 0, "F": 0, "XF": 0, "XZ": 0, "FS": 0, "XFZS": 0,
                             "Z": 1, "S": 1, "ZS": 1,
                             "K": 2, "T": 2, "KT": 2,
                             "P": 3, "V": 3, "PV": 3,
                             "L": 4, "R": 4, "LR": 4,
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

