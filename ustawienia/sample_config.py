from ustawienia.konfiguracja_fabryki import KonfiguracjaGeneratora
from ustawienia.konfiguracja_fabryki import KonfiguracjaFabryki
from ustawienia.konfiguracja_fabryki import TypyGeneracji


# Required: language config
class KonfiguracjaJęzyka:
    # Optional helper for class attribute definitions
    nic = ""

    # Required: characted used for palatalization,
    # set to None in order to disable palatalization
    zmiękczenie = "i"

    # Required: consonants
    spółgłoski = ['b', 'c', 'ć', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ł', 'm',
                  'n', 'ń', 'p', 'q', 'r', 's', 'ś', 't', 'v', 'w', 'x', 'z',
                  'ź', 'ż']

    # Required: vowels
    samogłoski = ['a', 'ą', 'e', 'ę', 'i', 'o', 'ó', 'u', 'y']

    # Required: one letter words
    jednoliterowe_wyrazy  = ['a', 'i', 'o', 'u', 'w', 'z']

    # Required: consonant phonemes
    # {"Phoneme as part of written word": ("Left hand combo", "Right hand combo")}
    # Hint: have same-sounding phonems share the same combos
    fonemy_spółgłoskowe = {"b": ("XP", "B"),
                           "bi": ("XPJ", "BI"),
                           "c": ("ZT", "C"),
                           "ci": ("ZTJ", "CI"),
                           "ch": ("X", "CB"),
                           "chi": ("XJ", "CBI"),
                           "cz": ("PV", "CL"),
                           "czi": ("PVJ", "CLI"),
                           "ć": ("ZTJ", "CI"),
                           "d": ("FT", "SG"),
                           "di": ("FTJ", "ISG"),
                           "dz": ("ST", "LG"),
                           "dzi": ("STJ", "LIG"),
                           "dź": ("STJ", "LIG"),
                           "dż": ("FST", "BG"),
                           "dżi": ("FSTJ", "BIG"),
                           "f": ("F", "CG"),
                           "fi": ("FJ", "CIG"),
                           "g": ("XK", "G"),
                           "gi": ("XKJ", "IG"),
                           "h": ("X", "CB"),
                           "hi": ("XJ", "CBI"),
                           "j": ("J", "CR"),
                           "ji": ("J", "CRI"),
                           "k": ("K", "RL"),
                           "ki": ("KJ", "RLI"),
                           "l": ("L", "L"),
                           "li": ("LJ", "LI"),
                           "ł": ("LR", "LB"),
                           "łi": ("LRJ", "LBI"),
                           "m": ("KP", "CS"),
                           "mi": ("KPJ", "CIS"),
                           "n": ("TV", "LS"),
                           "ni": ("TVJ", "LIS"),
                           "ń": ("TVJ", "LIS"),
                           "p": ("P", "RG"),
                           "pi": ("PJ", "RIG"),
                           "q": ("KV", "~LB"),
                           "r": ("R", "R"),
                           "ri": ("RJ", "RI"),
                           "rz": ("XZ", "RS"),
                           "s": ("S", "S"),
                           "si": ("SJ", "IS"),
                           "sz": ("TP", "RB"),
                           "ś": ("SJ", "IS"),
                           "t": ("T", "T"),
                           "ti": ("TJ", "IT"),
                           "v": ("V~", "W~"),
                           "vi": ("VJ~", "IW~"),
                           "w": ("V", "W"),
                           "wi": ("VJ", "IW"),
                           "x": ("XF", "~SG"),
                           "xi": ("XFJ", "~ISG"),
                           "z": ("Z", "BS"),
                           "zi": ("ZJ", "BIS"),
                           "ź": ("ZJ", "BIS"),
                           "ż": ("XZ", "RS")}

    # Required: vowel phonemes
    # {"Phoneme": ("Center combo", "Right hand combo")}
    fonemy_samogłoskowe = {"a": ("A", "TO"),
                           "ą": ("UA", "TW"),
                           "e": ("E", "TWOY"),
                           "ę": ("EU", "OY"),
                           "i": ("J", "I"),
                           "o": ("AI", "O"),
                           "ó": ("U", "~O"),
                           "u": ("U", "WY"),
                           "y": ("EUA", "Y")}

    # Required: two-char phonemes
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

# Required: Keyboard configuration, keys in steno order
class KonfiguracjaKlawiatury:
    # Required: character ordering
    kolejność = '#/XFZSKTPVLRJE-~*UAICRLBSGTWOY'

    # Optional helpers for attribute definitions
    tylda = "~"
    gwiazdka = "*"
    myślnik = "-"
    jot = "J"
    ee = "E"
    ii = "I"
    aa = "A"
    uu = "U"

    # Required: left fingers from left to right
    palce_lewe = [("X", "F", "Z", "S"),
                  ("K", "T"),
                  ("P", "V"),
                  ("L", "R", tylda, gwiazdka),
                  (jot, ee, uu, aa)]

    # Required: center keys on the keyboard (thumbs and shared index fingers keys)
    znaki_środka = [jot, ee, tylda, gwiazdka, uu, aa, ii]

    # Required: right fingers from left to right
    palce_prawe = [(uu, aa, ii),
                  (tylda, gwiazdka, "C", "R"),
                  ("L", "B"),
                  ("S", "G"),
                  ("T", "W", "O", "Y")]

    # Required: left side steno column indices starting from 0
    # include allowed one finger combos
    lewe_indeksy_klawiszy = {"X": 0, "F": 0, "XF": 0, "XZ": 0, "FS": 0, "XFZS": 0,
                             "Z": 1, "S": 1, "ZS": 1,
                             "K": 2, "T": 2, "KT": 2,
                             "P": 3, "V": 3, "PV": 3, jot: 3,
                             "L": 4, "R": 4, "LR": 4, ee: 4,
                             tylda: 5, gwiazdka: 5, uu: 5,
                             aa: 6}

    # Required: right side steno column indices
    # include allowed one finger combos 
    prawe_indeksy_klawiszy = {tylda: 5, gwiazdka: 5, uu: 5,
                              "C": 6, "R": 6, "CR": 6, aa: 6,
                              "L": 7, "B": 7, "LB": 7, ii: 7,
                              "S": 8, "G": 8, "SG": 8,
                              "T": 9, "W": 9, "TW": 9, "TO": 9, "WY": 9, "TWOY": 9,
                              "O": 10, "Y": 10, "OY": 10}
