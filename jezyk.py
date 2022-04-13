from pomocnicy import SłownikDomyślny
import collections
import re
from pyphen import Pyphen

nic = ""

class Język:
    def __init__(self, log, konfiguracja):
        self.log = log
        self.fonemy_sylaby = SłownikDomyślny(lambda x: self.rozłóż_sylabę(x))
        self.wagi_fonemów = SłownikDomyślny(lambda x: self.policz_wagę_fonemu(x))
        self.fonemy_dwuznakowe = konfiguracja.fonemy_dwuznakowe
        self.fonemy_samogłoskowe_klucze = konfiguracja.fonemy_samogłoskowe_klucze
        self.fonemy_spółgłoskowe_klucze = konfiguracja.fonemy_spółgłoskowe_klucze
        self.fonemy_samogłoskowe = konfiguracja.fonemy_samogłoskowe
        self.fonemy_spółgłoskowe = konfiguracja.fonemy_spółgłoskowe
        self.samogłoski = konfiguracja.samogłoski
        self._samogłoski_re = re.compile(r'[aąeęioóuy]+')
        self.sylabizator = Pyphen(lang='pl_PL')

    def rozbij(self, słowo):
        return [char for char in słowo]

    def sylabizuj(self, słowo):
        return self.sylabizator.inserted(słowo).split('-')

    def rozłóż_sylabę(self, sylaba: str):
        m = self._samogłoski_re.search(sylaba)
        if not m:
            błąd = f"sylaba {sylaba} bez samogłosek"
            self.log.debug(błąd)
            return (sylaba, nic, nic)
        śródgłos = self.fonemy(m.group(0))

        # Wykryj "i" które tylko zmiękcza, przesuń je do nagłosu
        zmiękczenie = False
        if len(śródgłos) > 1 and śródgłos[0].startswith('i'):
            śródgłos = śródgłos[1:]
            zmiękczenie = True
        nagłos = self.fonemy(re.split(self._samogłoski_re, sylaba)[0], zmiękczenie)
        wygłos = self.fonemy(re.split(self._samogłoski_re, sylaba)[1])

        # self.log.debug(f"Rozłożyłem {sylaba} na N: {nagłos} Ś: {śródgłos} W: {wygłos}")
        return (nagłos, śródgłos, wygłos)

    def fonemy(self, słowo, zmiękczenie = False):    
        znaki = self.rozbij(słowo)
        if zmiękczenie:
            znaki.append("i")

        wynik = []
        i = 0
        ilość_znaków = len(znaki)
        while i < ilość_znaków:
            znak = znaki[i]
            if znak in self.fonemy_dwuznakowe.keys():
                if (i+1 < ilość_znaków) and znaki[i+1] in self.fonemy_dwuznakowe[znak]:
                    następny_znak = znaki[i+1]
                    if zmiękczenie and ((znak == "c" and następny_znak in ["z", "h"])\
                      or (znak == "d" and następny_znak =="z")):
                        if (i+2 < ilość_znaków) and znaki[i+2] == "i":
                            i += 3
                            wynik.append(znak + następny_znak + "i")
                        else:
                            i += 2
                            wynik.append(znak + następny_znak)
                    else:
                        i += 2
                        wynik.append(znak + następny_znak)
                else:
                    i += 1
                    wynik.append(znak)
            else:
                i += 1
                wynik.append(znak)
        return wynik

    def policz_wagę_fonemu(self, x):
        if x in self.fonemy_samogłoskowe_klucze:
            return (len(self.fonemy_samogłoskowe[x][0]),
                    len(self.fonemy_samogłoskowe[x][1]))
        elif x in self.fonemy_spółgłoskowe_klucze:
            return (len(self.fonemy_spółgłoskowe[x][0]),
                    len(self.fonemy_spółgłoskowe[x][1]))

    def rozbij_sylaby_na_fonemy(self, sylaby_lewe, sylaba_środkowa, sylaby_prawe):
        waga_słowa = 0
        waga_środka = 0
        fonemy_lewe = []
        śródgłosy = []
        fonemy_prawe = []
        for sylaba in sylaby_lewe:
            (nagłos, śródgłos, wygłos) = self.fonemy_sylaby[sylaba]
            for fonem in nagłos + wygłos:
                waga_słowa += self.wagi_fonemów[fonem][0]
                # self.log.debug(f"waga 1: {waga_słowa} {fonem}")
                fonemy_lewe.append(fonem)
            for fonem in śródgłos:
                waga_słowa += self.wagi_fonemów[fonem][0]
                # self.log.debug(f"waga 2: {waga_słowa} {fonem}")
        (nagłos, śródgłos, wygłos) = self.fonemy_sylaby[sylaba_środkowa]
        środek_bez_wygłosu = True
        for fonem in nagłos:
            waga_słowa += self.wagi_fonemów[fonem][0]
            # self.log.debug(f"waga 3: {waga_słowa} {fonem}")
            fonemy_lewe.append(fonem)
        for fonem in śródgłos:
            waga_słowa += self.wagi_fonemów[fonem][0]
            waga_środka += self.wagi_fonemów[fonem][0]
            # self.log.debug(f"waga 4: {waga_słowa} {fonem}")
            śródgłosy.append(fonem)
        for fonem in wygłos:
            waga_słowa += self.wagi_fonemów[fonem][1]
            # self.log.debug(f"waga 5: {waga_słowa} {fonem}")
            fonemy_prawe.append(fonem)
            środek_bez_wygłosu = False
        if sylaby_prawe:
            for sylaba in sylaby_prawe[:-2]:
                # self.log.info(f"syl prawe: {sylaba}")
                (nagłos, śródgłos, wygłos) = self.fonemy_sylaby[sylaba]
                if środek_bez_wygłosu and len(nagłos) == 0:
                    for fonem in śródgłos:
                        waga_słowa += self.wagi_fonemów[fonem][0]
                        waga_środka += self.wagi_fonemów[fonem][0]
                        # self.log.debug(f"waga 6: {waga_słowa} {fonem}")
                        śródgłosy.append(fonem)
                    for fonem in wygłos:
                        waga_słowa += self.wagi_fonemów[fonem][1]
                        # self.log.debug(f"waga 6b: {waga_słowa} {fonem}")
                        fonemy_prawe.append(fonem)
                else:
                    for fonem in nagłos + wygłos:
                        waga_słowa += self.wagi_fonemów[fonem][1]
                        # self.log.debug(f"waga 6: {waga_słowa} {fonem}")
                        fonemy_prawe.append(fonem)
                    for fonem in śródgłos:
                        waga_słowa += self.wagi_fonemów[fonem][1]
                        # self.log.debug(f"waga 7: {waga_słowa} {fonem}")
            if len(sylaby_prawe)>1:
                (nagłos, śródgłos, wygłos) = self.fonemy_sylaby[sylaby_prawe[-2]]
                (nagłos_o, śródgłos_o, wygłos_o) = self.fonemy_sylaby[sylaby_prawe[-1]]
                if len(wygłos) == 0 and len(nagłos_o) == 0 and not wygłos_o:
                    for fonem in nagłos:
                        waga_słowa += self.wagi_fonemów[fonem][1]
                        # self.log.debug(f"waga 8: {waga_słowa} {fonem}")
                        fonemy_prawe.append(fonem)
                    for fonem in śródgłos:
                        waga_słowa += self.wagi_fonemów[fonem][1]
                        # self.log.debug(f"waga 8: {waga_słowa} {fonem}")
                        fonemy_prawe.append(fonem)
                    for fonem in śródgłos_o:
                        waga_słowa += self.wagi_fonemów[fonem][1]
                        # self.log.debug(f"waga 8: {waga_słowa} {fonem}")
                        fonemy_prawe.append(fonem)
                elif len(wygłos_o) == 0:
                    for fonem in nagłos + wygłos + nagłos_o:
                        waga_słowa += self.wagi_fonemów[fonem][1]
                        # self.log.debug(f"waga 8: {waga_słowa} {fonem}")
                        fonemy_prawe.append(fonem)
                    for fonem in śródgłos_o:
                        waga_słowa += self.wagi_fonemów[fonem][1]
                        # self.log.debug(f"waga 8: {waga_słowa} {fonem}")
                        fonemy_prawe.append(fonem)
                else:
                    for fonem in nagłos + wygłos + nagłos_o + wygłos_o:
                        waga_słowa += self.wagi_fonemów[fonem][1]
                        # self.log.debug(f"waga 8: {waga_słowa} {fonem}")
                        fonemy_prawe.append(fonem)
            else:
                (nagłos, śródgłos, wygłos) = self.fonemy_sylaby[sylaby_prawe[-1]]
                if not wygłos:
                    for fonem in nagłos + śródgłos:
                        waga_słowa += self.wagi_fonemów[fonem][1]
                        # self.log.debug(f"waga 8: {waga_słowa} {fonem}")
                        fonemy_prawe.append(fonem)
                else:
                    for fonem in nagłos + wygłos:
                        waga_słowa += self.wagi_fonemów[fonem][1]
                        # self.log.debug(f"waga 9: {waga_słowa} {fonem}")
                        fonemy_prawe.append(fonem)
                    for fonem in śródgłos:
                        waga_słowa += self.wagi_fonemów[fonem][1]
                        # self.log.debug(f"waga 10: {waga_słowa} {fonem}")
        zważone_lewe = self.zważ_fonemy(fonemy_lewe)
        zważone_środkowe = self.zważ_fonemy(śródgłosy)
        zważone_prawe = self.zważ_fonemy(fonemy_prawe, prawe=True)
        return (zważone_lewe,
                zważone_środkowe,
                zważone_prawe,
                waga_słowa,
                waga_środka)

    def odejmij_fonemy(self, fonemy, do_odjęcia):
        nowe_fonemy = fonemy
        for fonem in do_odjęcia:
            if fonem in nowe_fonemy:
                nowe_fonemy.remove(fonem)
        return nowe_fonemy

    def zważ_fonemy(self, fonemy, prawe=0):
        wagi_fonemów = collections.defaultdict(lambda: 0)
        wyjściowe_fonemy = []
        for fonem in fonemy:
            waga = self.wagi_fonemów[fonem][prawe]
            wagi_fonemów[fonem] += waga
            if fonem not in wyjściowe_fonemy:
                wyjściowe_fonemy.append(fonem)
        zważone_fonemy = []
        for fonem in wyjściowe_fonemy:
            zważone_fonemy.append((fonem, wagi_fonemów[fonem]))
        # self.log.info(f"ZWA:{zważone_fonemy}")
        return zważone_fonemy


