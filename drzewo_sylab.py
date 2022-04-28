import sys
sys.setrecursionlimit(5000)
import collections
from logowanie import Logger
from pomocnicy import Czytacz, Pisarz, SłownikDomyślny
log = Logger('wyniki/drzewo.log')

# l = []
# czytacz = Czytacz()
# (sylaby_słowa, ile_słów_wczytano) = czytacz.wczytaj_słowa(log, 'data/slownik')
# frekwencje = SłownikDomyślny(lambda x: 1)
# for (wejście, frekwencja) in czytacz.czytaj_z_pliku_frekwencji('data/frekwencja_Kazojc.csv'):
#     frekwencje[wejście] = frekwencja
# log.info("Frekwencje wczytane")
# for (słowo, sylaby) in sylaby_słowa.items():
#     l.append((sylaby, frekwencje[słowo]))

# l = [(["ba", "be", "bo", "bu", ], 2),
#      (["ba", "be" ], 3),
#      (["ba", "be", "bo", ], 1),
#      (["ba", "be", "bo", "bu", "by", ], 8),
#      (["da" ], 7),
#      (["da", "de", "do" ], 5),
#      (["da", "de", "di" ], 6),
#      (["pa", "pe", "pi"], 9),
#      (["pa", "pe", ], 4),
#      (["pa", ], 12),
#      (["pa", "pe", "po", "pu", ], 10)]

# l = [
#      (["pa", ], 12),
#      (["pa", "pe", ], 4),
#      (["pa", "pe", "po", "pu", ], 10),
#      (["pa", "pe", "pi"], 9),

#      (["da" ], 7),
#      (["da", "de", "di" ], 6),
#      (["da", "de", "do" ], 5),

#      (["ba", "be" ], 3),
#      (["ba", "be", "bo", ], 1),
#      (["ba", "be", "bo", "bu", ], 2),
#      (["ba", "be", "bo", "bu", "by", ], 8),
#      ]


class WpisSłownika:
    def __init__(self, długość, częstotliwość, ostatnia_sylaba_słowa, pozostałe_sylaby):
        self.długość = długość
        self.częstotliwość = częstotliwość
        self.ostatnia_sylaba_słowa = ostatnia_sylaba_słowa
        self.pozostałe_sylaby = pozostałe_sylaby

    def __repr__(self):
        string = f"\nL:{self.długość}, Fq:{self.częstotliwość}, SŁ:{self.ostatnia_sylaba_słowa}, {self.pozostałe_sylaby}"
        return string

def zamień_listę_na_słownik(l):
    # print(f"zamieniam liste {type(l)}: {l}")
    if len(l) == 0:
        return None
    d = collections.defaultdict(list)
    for element in l:
        długość = len(element[0])
        if długość == 0:
            # print(f"Co mam z tym zrobić: {element} (z {l})")
            continue
        ostatnia_sylaba_słowa = False
        if długość == 1:
            ostatnia_sylaba_słowa = True
        d[element[0][0]].append(WpisSłownika(długość, element[1], ostatnia_sylaba_słowa, (element[0][1:], element[1])))
    return d

# d = zamień_listę_na_słownik(l)

def zamień_wpisy_na_słownik(wpisy):
    lista = []
    # print(f"zamieniam wpisy {wpisy}")
    for element in wpisy:
        lista.append(element.pozostałe_sylaby)
    return zamień_listę_na_słownik(lista)

class WęzełBinarny:
    def __init__(self, sylaba, częstotliwość, ostatnia_sylaba_słowa, sylaby_do_przetworzenia):
        if sylaba == None:
            self.pusty()
        else:
            self.sylaba = sylaba
            self.częstotliwość = częstotliwość
            self.ostatnia_sylaba_słowa = ostatnia_sylaba_słowa
            self.sylaby_do_przetworzenia = sylaby_do_przetworzenia
            self.lewy_potomek = WęzełBinarny(None, 0, False, [])
            self.prawy_potomek = WęzełBinarny(None, 0, False, [])
            self.węzeł_pochodny = None

    def pusty(self):
        self.sylaba = None
        self.lewy_potomek = None
        self.prawy_potomek = None
        self.częstotliwość = 0
        self.ostatnia_sylaba_słowa = False
        self.sylaby_do_przetworzenia = []
        self.węzeł_pochodny = None

    def dodaj(self, sylaba, inny_węzeł):
        if not self.sylaba:
            self = inny_węzeł
            return self
        elif self.częstotliwość < inny_węzeł.częstotliwość:
            if not self.lewy_potomek.sylaba:
                self.lewy_potomek = inny_węzeł
            else:
                self.lewy_potomek.dodaj(sylaba, inny_węzeł)
        else:
            if not self.prawy_potomek.sylaba:
                self.prawy_potomek = inny_węzeł
            else:
                self.prawy_potomek.dodaj(sylaba, inny_węzeł)

    def następny(self, poprzednie_sylaby=[]):
        if not self.sylaba:
            return
            log.info(f"L: {self.lewy_potomek}")
            log.info(f"P: {self.prawy_potomek}")
            log.info(f"PRZ: {self.sylaby_do_przetworzenia}")
        # log.info(f"{self.sylaba}, poprz: {poprzednie_sylaby}")
        if self.lewy_potomek and self.lewy_potomek.sylaba:
            # print(f"lewy: {self.lewy_potomek.sylaba}")
            for nast in self.lewy_potomek.następny(poprzednie_sylaby):
                yield nast
            self.lewy_potomek = None
        # print(f"ja: {self.sylaba}")

        dotychczasowe_sylaby = []
        for sylaba in poprzednie_sylaby:
            dotychczasowe_sylaby.append(sylaba)
        dotychczasowe_sylaby.append(self.sylaba)
        # print(f"ostatnia: {self.ostatnia_sylaba_słowa}")
        if self.ostatnia_sylaba_słowa:
            # yield (dotychczasowe_sylaby, self.częstotliwość)
            # log.info(f"do pr: {self.sylaby_do_przetworzenia}")
            if len(self.sylaby_do_przetworzenia) > 1:
                yield f"&{''.join(dotychczasowe_sylaby)},{'='.join(dotychczasowe_sylaby)}\n"
            else:
                yield f"{''.join(dotychczasowe_sylaby)},{'='.join(dotychczasowe_sylaby)}\n"
        else:
            if self.sylaba:
                # log.info(f"Przerabiam {dotychczasowe_sylaby}")
                sylaby=dotychczasowe_sylaby
                if sylaby[-1] == None:
                    sylaby = sylaby[:-1]
                # log.info("yield 2")
                yield f"*{''.join(sylaby)},{'='.join(sylaby)}\n"
        if self.sylaby_do_przetworzenia:
            # print("w następny")
            słownik = zamień_wpisy_na_słownik(self.sylaby_do_przetworzenia)
            # print(f"drugie drzewo: {słownik}")
            self.węzeł_pochodny = zamień_na_drzewo(słownik)
            # print(f"{self.sylaba} częst: {self.częstotliwość}")
            for nast in self.węzeł_pochodny.następny(dotychczasowe_sylaby):
                yield nast

        if self.prawy_potomek and self.prawy_potomek.sylaba:
            for nast in self.prawy_potomek.następny(poprzednie_sylaby):
            # print(f"prawy: {self.prawy_potomek.sylaba}")
                yield nast
            self.prawy_potomek = None

    def __repr__(self):
        if not self.sylaba:
            return ""
        string = f"\t{self.sylaba} - {self.częstotliwość}\n{self.lewy_potomek}\t\t{self.prawy_potomek}"
        return string
        

def zamień_na_drzewo(słownik):
    # print(f"na drzewo: {słownik}")
    drzewo = WęzełBinarny(None, 0, False, [])
    for sylaba, wpisy in słownik.items():
        częstotliwość = 0
        koniec_słowa = False
        for wpis in wpisy:
            częstotliwość += wpis.częstotliwość
            # print(f"{sylaba} freq: {częstotliwość}")
            if wpis.ostatnia_sylaba_słowa:
                # print(f"ostatnia sylaba: {wpis}")
                koniec_słowa = True
        # print(f"tworzę węzeł: {wpisy}")
        węzeł = WęzełBinarny(sylaba, częstotliwość, koniec_słowa, wpisy)
        if not drzewo.sylaba:
            drzewo = węzeł
        else:
            drzewo.dodaj(sylaba, węzeł)
    return drzewo

# drzewo = zamień_na_drzewo(d)
# pisarz = Pisarz("nic")
# pisarz.zapisz_surowe("wyniki/drzewo.csv", drzewo.następny())

def utwórz_drzewo_binarne_z_listy_par_sylaba_frekwencja(lista_par):
    słownik = zamień_listę_na_słownik(lista_par)
    drzewo = zamień_na_drzewo(słownik)
    return drzewo
