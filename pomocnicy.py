import os, importlib.util
import collections


nic = ""

#  Alternatywa dla collections.defaultdict
class SłownikDomyślny(collections.UserDict):
    def __init__(self, domyślna_fabryka=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not callable(domyślna_fabryka) and domyślna_fabryka is not None:
            raise TypeError('Pierwszy argument musi być wykonywalny albo None')
        self.domyślna_fabryka = domyślna_fabryka

    def __missing__(self, klucz):
        if self.domyślna_fabryka is None:
            raise KeyError(klucz)
        if klucz not in self:
            self[klucz] = self.domyślna_fabryka(klucz)
        return self[klucz]


class Czytacz:
    def __init__(self):
        pass

    def stwórz_katalogi_jeśli_trzeba(self, katalogi):
        for plik_wyjściowy in katalogi:
            folder = os.path.dirname(plik_wyjściowy)
            if folder != '':
                os.makedirs(folder, exist_ok=True)

    def wczytaj_bazę_do_słownika(self, baza):
        słownik = collections.defaultdict(dict)
        numer_linii = 0
        for linia in self.czytaj_linie_pliku(baza):
            numer_linii += 1
            linia = linia.strip()
            if not linia\
              or linia.startswith('#')\
              or linia.startswith('{')\
              or linia.startswith('}'):
                continue
            (kombinacja, wyraz) = self.czytaj_znaki_między_cudzysłowem(linia)
            słownik[wyraz] = {kombinacja: 0}
        return (słownik, numer_linii)

    def wczytaj_słowa(self, log, plik_ze_słowami):
        sylaby_słowa = dict()
        numer_linii = 0
        for linia in self.czytaj_linie_pliku(plik_ze_słowami):
            numer_linii += 1
            linia = linia.strip()
            if linia.startswith('#'):
                continue

            sylaby = linia.split('=')
            tekst = ''.join(sylaby)
            sylaby_słowa[tekst] = sylaby #klawisze_słowa
            if numer_linii % 10000 == 0 and numer_linii != 0:
                log.info(f'Przetwarzanie linii {numer_linii}: {linia}')
        return (sylaby_słowa, numer_linii)

    def czytaj_z_pliku_frekwencji(self, plik):
        for linia in self.czytaj_linie_pliku(plik):
            linia = linia.strip()
            słowo = linia.split('"')[1]
            frekwencja = int(linia.split(',')[1])
            yield (słowo, frekwencja)

    def wczytaj_konfigurację(self, ścieżka_do_pliku):
        spec = importlib.util.spec_from_file_location("Konfiguracja", ścieżka_do_pliku)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def czytaj_linie_pliku(self, plik):
        for linia in open(plik, "r"):
            yield linia

    def czytaj_znaki_między_cudzysłowem(self, wiersz):
        lista = []
        token = nic
        cudzysłów_otwarty = False
        poprzedni_backslash = False
        for znak in wiersz:
            if cudzysłów_otwarty and znak != '"':
                token+=znak
                poprzedni_backslash = False
            elif cudzysłów_otwarty and znak == '"' and not poprzedni_backslash:
                lista.append(token)
                token = nic
                cudzysłów_otwarty = False
            elif cudzysłów_otwarty and znak == '"' and poprzedni_backslash:
                token+=znak
                poprzedni_backslash = False
            elif cudzysłów_otwarty and znak == '\\':
                token+=znak
                poprzedni_backslash = True
            elif not cudzysłów_otwarty and znak == '"':
                cudzysłów_otwarty = True
                poprzedni_backslash = False
            elif not cudzysłów_otwarty and znak != '"':
                poprzedni_backslash = False
                continue
        return lista


class Pisarz:
    def __init__(self, plik_docelowy):
        self.słownik_sortowany = plik_docelowy
        self.słownik_niesortowany = plik_docelowy[:-5]+"_niesortowany.json"
        self.porażki = plik_docelowy[:-5]+"_porazki.txt"

    def zapisz_sortowane(self, słownik):
        przecinek = ",\n"
        nowa_linia = nic
        with open(self.słownik_sortowany, 'w', buffering=1024000) as plik_wynikowy:
            plik_wynikowy.write('{\n')
            for klawisze, tekst in słownik.items():
                plik_wynikowy.write(f'{nowa_linia} "{klawisze}": "{tekst}"')
                nowa_linia = przecinek
            plik_wynikowy.write('}\n')

    def zapisz_porażki(self, niepowodzenia):
        with open(self.porażki, 'w', buffering=10240) as plik_wynikowy:
            for (słowo, frekwencja) in niepowodzenia:
                plik_wynikowy.write(f"{słowo} ({frekwencja})\n")

    def zapisz_niesortowane(self, linie):
        przecinek = ",\n"
        nowa_linia = nic
        with open(self.słownik_niesortowany, 'w', buffering=1024000) as plik_wynikowy:
            plik_wynikowy.write('{\n')
            for linia in linie:
                plik_wynikowy.write(nowa_linia + linia)
                nowa_linia = przecinek
            plik_wynikowy.write('}\n')


def dzielniki_dla_słowa_o_długości(n):
    if n == 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    elif n == 3:
        return [1, 2, 0]
    elif n == 4:
        return [2, 1, 3, 0]
    else:
        lista = [n - 2, 1 , n - 1, 0]
        # odj dod odj dod
        z_początku = False
        pozostałe = []
        for i in range(2, n - 2):
            pozostałe.append(i)
        while pozostałe:
            if z_początku:
                lista.append(pozostałe.pop(0))
            else:
                lista.append(pozostałe.pop(-1))
            z_początku = not z_początku
        return lista

