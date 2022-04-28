#!/usr/bin/env python3
from logowanie import Logger
from fabryka import Fabryka
from pomocnicy import Czytacz, Pisarz, SłownikDomyślny
from drzewo_sylab import utwórz_drzewo_binarne_z_listy_par_sylaba_frekwencja
import argparse

import collections
import time


def main():
    parser = argparse.ArgumentParser(
        description='Generuj słownik na podstawie słów podzielonych na sylaby',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--log', default='wyniki/generuj_slownik.log',
                        help='log przebiegu generacji słownika')
    parser.add_argument('--frekwencja', default='data/frekwencja_Kazojc.csv',
                        help='dane frekwencyjne (w formacie linii csv: "słowo",częstość)')
    parser.add_argument('--przedrostki', default='data/przedrostki.txt',
                        help='dane frekwencyjne (w formacie linii csv: "słowo",częstość)')
    parser.add_argument('--slowa', default='data/slownik',
                        help='słowa do utworzenia słownika podzielone na sy=la=by')
    # parser.add_argument('--baza', default='wyniki/spektralny-slowik_niesortowany.json',
    parser.add_argument('--słowa_z_drzewa', default='wyniki/slowa_z_drzewa.csv',
                        help='rezultaty f-cji utwórz_drzewo_binarne_z_listy_par_sylaba_frekwencja')
    parser.add_argument('--baza', default='wyniki/baza-1.json',
                        help='początkowy plik słownika w formacie JSON')
    parser.add_argument('--max_niedopasowanie', default='7',
                        help='Parametr generatora, 0 - tylko słowa idealnie pasujące, więcej niż 0 - słowa z brakującymi literami w akordzie')
    parser.add_argument('--max_słów_na_akord', default='7',
                        help='Ile maksymalnie słów może zawierać jeden akord')
    parser.add_argument('--konfiguracja', default='ustawienia/konfiguracja_nowa.py',
                        help='plik konfiguracji generatora')
    parser.add_argument('--slownik', default='wyniki/spektralny-slowik.json',
                        help='wynikowy plik JSON do załadowania do Plovera')
    args = parser.parse_args()
    max_niedopasowanie = int(args.max_niedopasowanie)
    max_słów_na_akord = int(args.max_słów_na_akord)
    czytacz = Czytacz()
    czytacz.stwórz_katalogi_jeśli_trzeba([args.log, args.slownik])
    # Spróbuj otworzyć plik logu
    log = Logger(args.log)
    log.info(f'Argumenty: {str(args)[10:-1]}')

    # Słownik wyjściowy, dane w formie:
    # {tekst: {"Kombinacja": niedopasowanie}}
    konfiguracja = czytacz.wczytaj_konfigurację(args.konfiguracja)


    from generator import Generator
    from jezyk import Język, Słowo
    from klawiatura import Klawiatura
    język = Język(log, konfiguracja.KonfiguracjaJęzyka)
    klawiatura = Klawiatura(log, konfiguracja.KonfiguracjaKlawiatury, język)
    numer_generacji = 0
    loguj_postęp_co = 10000
    przedrostki = []
    istniejące_słowa = set()

    if args.baza:
        log.info(f"Czytam bazę słownika z {args.baza}")
        (słownik, linie_bazy) = czytacz.wczytaj_bazę_do_słownika(log, args.baza)
        log.info(f"Baza wczytana")
    else:
        słownik = collections.defaultdict(dict)
        linie_bazy = 0

 
    (sylaby_słowa, ile_słów_wczytano) = czytacz.wczytaj_słowa(log, args.slowa)
    # generator = Generator(log, język, klawiatura, konfiguracja, słownik, sylaby_słowa)
    fabryka = Fabryka(log, konfiguracja, słownik, przedrostki)
    czas_start = time.time()
    niepowodzenia = []
    niepowodzenia_przedrostków = []

    log.info(f"Generuję klawisze dla liter alfabetu...")
    wejścia = konfiguracja.KonfiguracjaJęzyka.samogłoski +\
      konfiguracja.KonfiguracjaJęzyka.spółgłoski
    for wejście in wejścia:
        # log.info(f"litera: {wejście}")
        ile_dodano = fabryka.uruchom_linie(wejście, nazwa_ustawień="litery")
        if ile_dodano == 0:
            niepowodzenia.append((wejście, 1))

    
    pisarz = Pisarz(args.slownik)
    if not czytacz.sprawdź_czy_plik_istnieje(args.słowa_z_drzewa):
        log.info(f"Plik {args.słowa_z_drzewa} nie istnieje, generuję sylaby wg frekwencji...")
        postęp = 0
        lista_par = []
        frekwencje = SłownikDomyślny(lambda x: 1)
        for (wejście, frekwencja) in czytacz.czytaj_z_pliku_frekwencji(args.frekwencja):
            frekwencje[wejście] = frekwencja
        log.info("Plik frekwencji wczytany, tworzę plik wejściowy dla binarnego drzewa sylab...")
        for (słowo, sylaby) in sylaby_słowa.items():
            lista_par.append((sylaby, frekwencje[słowo]))
            postęp += 1
            if postęp % 100000 == 0:
                log.info(f"{postęp}: {słowo}")
        leg.info("Plik wejściowy utworzony, generuję drzewo...")
        drzewo = utwórz_drzewo_binarne_z_listy_par_sylaba_frekwencja(lista_par)
        leg.info("Drzewo utworzone, zapisuję...")
        pisarz.zapisz_surowe(args.słowa_z_drzewa, drzewo.następny())
        log.info(f"Plik {args.słowa_z_drzewa} zapisany na dysku")
    log.info(f"Czytam z pliku {args.słowa_z_drzewa}")
    for (wejście, sylaby) in czytacz.czytaj_sylaby(args.słowa_z_drzewa):
        if wejście.startswith('*'):
            wejście = wejście[1:]
            fabryka.uruchom_linie(wejście, nazwa_ustawień="rdzeń")
            ile_dodano = 1
        elif wejście.startswith('&'):
            wejście = wejście[1:]
            ile_dodano = fabryka.uruchom_linie(wejście, nazwa_ustawień="przedrostki")
        else:
            ile_dodano = fabryka.uruchom_linie(wejście, nazwa_ustawień="frekwencja_0")
        if ile_dodano == 0:
            niepowodzenia.append((wejście, 1))


    # log.info(f"Wczytałem sylaby dla {ile_słów_wczytano} słów, generuję klawisze...")

    # for (wejście, frekwencja) in czytacz.czytaj_z_pliku_frekwencji(args.frekwencja):
    #     ile_dodano = fabryka.uruchom_linie(wejście, nazwa_ustawień="frekwencja_0")
    #     if ile_dodano == 0:
    #         niepowodzenia.append((wejście, frekwencja))

    # (przedrostki, ile_przedrostków_wczytano) = czytacz.wczytaj_słowa(log, args.przedrostki)
    # log.info(f"Wczytałem {ile_przedrostków_wczytano} przedrostków, generuję...")
    # for przedrostek in przedrostki:
    #     ile_dodano = fabryka.uruchom_linie(przedrostek, nazwa_ustawień="przedrostki")
    #     if ile_dodano == 0:
    #         niepowodzenia_przedrostków.append((przedrostek, 10))


    ## Teraz z przedrostkami
    for limit_niedopasowania in range(1, max_niedopasowanie):
        log.info(f"Pętla {limit_niedopasowania + 1} z {max_niedopasowanie - 1}")
        nowe_niepowodzenia = []
        nazwa_ustawień=f"frekwencja_{limit_niedopasowania}"

        for (niepowodzenie, frekwencja) in niepowodzenia:
            ile_dodano = fabryka.uruchom_linie(niepowodzenie, nazwa_ustawień)
            if ile_dodano == 0:
                nowe_niepowodzenia.append((niepowodzenie, frekwencja))
        niepowodzenia = nowe_niepowodzenia
    log.info(f"Dodano {len(słownik) - linie_bazy} słów.")


    # log.info("Dodaję słowa bez podanej częstotliwości")
    # nazwa_ustawień=f"frekwencja_{max_niedopasowanie}"
    # for słowo in sylaby_słowa.keys():
    #     ile_dodano = fabryka.uruchom_linie(słowo, nazwa_ustawień)
    #     if ile_dodano == 0:
    #         niepowodzenia.append((słowo, 1))


    log.info(f"Dodano {len(słownik) - linie_bazy} słów w {time.time() - czas_start} sekund.")
    log.info(f"Nie powiodło się dodawanie kombinacji dla {len(niepowodzenia)} słów.")
    log.info(f"Nie powiodło się dodawanie kombinacji dla {len(niepowodzenia_przedrostków)} przedrostków.")

    log.info("Słownik utworzony, zapisuję...")
    log.info(f"Zapisuję porażki")
    pisarz.zapisz_porażki(niepowodzenia+niepowodzenia_przedrostków)
    fabryka.zapisz_rezultaty(pisarz)

    log.info("Fajrant")
            

    # log.info("Analizuję częstotliwość występowania fonemów...")
    # zanalizowane = 0
    # for (słowo, frekwencja) in czytacz.czytaj_z_pliku_frekwencji(args.frekwencja):
    #     generator.analizuj_słowo(słowo, frekwencja)
    #     zanalizowane += 1
    # log.info(f"Zanalizowano {zanalizowane} słów:\n")
    # log.info(f"Fonem\tCzęstotliwość występowania")
    # i =0
    # for ki, wi in {k: v for k, v in sorted(generator.analizowane_fonemy.items(),\
    #                                        key=lambda item: item[1])}.items():
    #     log.info(f"{i:2}: {ki:5}|{wi:10}")
    #     i += 1


    # log.info("Analizuję końcówki słów...")
    # zanalizowane = 0
    # for (słowo, frekwencja) in czytacz.czytaj_z_pliku_frekwencji(args.frekwencja):
    #     generator.analizuj_końcówki(słowo, frekwencja)
    #     zanalizowane += 1
    # for słowo in sylaby_słowa.keys():
    #     generator.analizuj_końcówki(słowo, 1)
    #     zanalizowane += 1
    # log.info(f"Zanalizowano {zanalizowane} słów:\n")
    # log.info(f"Końcówka\tCzęstotliwość występowania")
    # i =0
    # for ki, wi in {k: v for k, v in sorted(generator.analizowane_końcówki.items(),\
    #                                        key=lambda item: item[1])}.items():
    #     log.info(f"{i:2}: {ki:5}|{wi:10}")
    #     i += 1
    # log.info(f"Fonem\tCzęstotliwość występowania")
    # i =0
    # for ki, wi in {k: v for k, v in sorted(generator.analizowane_fonemy.items(),\
    #                                        key=lambda item: item[1])}.items():
    #     log.info(f"{i:2}: {ki:5}|{wi:10}")
    #     i += 1


#  TODO: usystematyzować to wszystko
#  class Czytacz
#  class Pisarz
#  class Generator
#  class KonfiguracjaGeneratora
#  class Żądanie
#  class Odpowiedź
#  class Język
#  class KonfiguracjaJęzyka
#  class Słowo
#  class Słownik
#  class Sylaba
#  class Fonem
#  class Klawiatura
#  class KonfiguracjaKlawiatury
#  class Klawisz
#  class Kombinacja
#  class RękaLewa
#  class RękaPrawa

#  Czytacz wczytuje KonfiguracjęGeneratora.
#  Czytacz wczytuje KonfiguracjęKlawiatury.  -- zaczęte
#  Czytacz wczytuje KonfiguracjęJęzyka.  -- zaczęte
#  Czytacz wczytuje Słowa do wygenerowania Kombinacji.  -- działa
#  Czytacz wczytuje bazowe Kombinacje do Słownika.  -- działa
#  Język jest tworzony na podstawie KonfiguracjiJęzyka.
#  Język tworzy Słowo zawierające Sylaby.
#  Sylaby zawierają Fonemy.
#  Generator jest tworzony na podstawie KonfiguracjiGeneratora.
#  Generator otrzymuje Słowo.
#  Klawiatura jest tworzona na podstawie KonfiguracjiKlawiatury.
#  Klawiatura zawiera RekęLewą i RękęPrawą i Środek.
#  RekaLewa i RękaPrawa i Środek zawierają Klawisze.
#  Generator wysyła do Klawiatury Żądanie.
#  Żądanie zawiera Słowo i niezbędne ParametryKombinacji.
#  W pętli do wyczerpania ParametrówKombinacji:
#      Klawiatura aktualizuje RękęLewą, RękęPrawą i Środek.
#      RękaLewa, RękaPrawa i Środek aktualizują swoje Klawisze.
#      Klawiatura tworzy Kombinację na podstawie stanu RękiLewej, RękiPrawej i Środka.
#      Klawiatura dodaje Kombinację do Odpowiedzi.
#  Klawiatura zwraca do Generatora Odpowiedź.
#  Generator porównuje Kombinacje zawarte w Odpowiedzi ze Słownikiem
#  W razie niepowodzenia dodania Kombinacji do Słownika,
#   Generator może wysłać ponowne Żądanie dla danego Słowa.
#  Pisarz zapisuje wygenerowany Słownik do pliku wyjściowego.

if __name__ == '__main__':
    main()

