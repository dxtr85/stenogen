#!/usr/bin/env python3
from logowanie import Logger
from fabryka import Fabryka
from pomocnicy import Czytacz, Pisarz, SłownikDomyślny
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
    parser.add_argument('--baza', default='wyniki/baza-0abs.json',
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
        (słownik, linie_bazy) = czytacz.wczytaj_bazę_do_słownika(args.baza)
        log.info(f"Baza wczytana")
    else:
        słownik = collections.defaultdict(dict)
        linie_bazy = 0

 
    (sylaby_słowa, ile_słów_wczytano) = czytacz.wczytaj_słowa(log, args.slowa)
    (przedrostki, ile_przedrostków_wczytano) = czytacz.wczytaj_słowa(log, args.przedrostki)
    generator = Generator(log, język, klawiatura, konfiguracja, słownik, sylaby_słowa)
    fabryka = Fabryka(log, konfiguracja, słownik, sylaby_słowa, przedrostki)
    czas_start = time.time()

    log.info(f"Generuję klawisze dla liter alfabetu...")
    niepowodzenia = []
    wejścia = konfiguracja.KonfiguracjaJęzyka.samogłoski +\
      konfiguracja.KonfiguracjaJęzyka.spółgłoski
    for wejście in wejścia:
        ile_dodano = fabryka.uruchom_linie(wejście, nazwa_ustawień="litery")
        if ile_dodano == 0:
            niepowodzenia.append((wejście, 1))
    # for litera in konfiguracja.KonfiguracjaJęzyka.samogłoski + konfiguracja.KonfiguracjaJęzyka.spółgłoski:
    #     if litera in istniejące_słowa or litera.isnumeric():
    #         continue
    #     czy_klejone = True
    #     if litera in konfiguracja.KonfiguracjaJęzyka.jednoliterowe_wyrazy:
    #         czy_klejone = False
    #     czy_przedrostek = False
    #     if litera in przedrostki:
    #         czy_przedrostek = True
    #     słowo = Słowo(litera,
    #                   jest_przedrostkiem=czy_przedrostek,
    #                   klejone=czy_klejone)
    #     stenosłowa = generator.wygeneruj(litera,
    #                                 limit_niedopasowania=0,
    #                                 limit_prób=10)
    #     dodane = generator.dodaj_słowa_do_słownika(słowo, stenosłowa)
    #     udało_się = len(dodane) > 0
    #     if not udało_się:
    #         # log.debug(f"Nie udało się dla {litera}, dodaje specjalne")
    #         nowe_stenosłowa = generator.dodaj_znaki_specjalne_do_słów(stenosłowa,
    #                                                               limit_niedopasowania=3,
    #                                                               limit_prób=10)
    #         log.debug(f"{litera} dodane specjalne: {nowe_stenosłowa} {type(nowe_stenosłowa[0])}")
    #         dodane = generator.dodaj_słowa_do_słownika(słowo, nowe_stenosłowa)
    #         udało_się = len(dodane) > 0
    #         if not udało_się:
    #             log.error(f"Nie dodałem litery '{litera}'")
    #         else:
    #             istniejące_słowa.add(litera)
    #     else:
    #         istniejące_słowa.add(litera)
    # niepowodzenia = []
    połowiczne_powodzenia = []
    niepowodzenia_przedrostków = []
        
    log.info(f"Wczytałem sylaby dla {ile_słów_wczytano} słów, generuję klawisze...")
    for (wejście, frekwencja) in czytacz.czytaj_z_pliku_frekwencji(args.frekwencja):
        ile_dodano = fabryka.uruchom_linie(wejście, nazwa_ustawień="frekwencja_0")
        if ile_dodano == 0:
            niepowodzenia.append((wejście, frekwencja))

    #     if litery in istniejące_słowa or litery.isnumeric():
    #         continue
    #     czy_przedrostek = False
    #     if litery in przedrostki:
    #         czy_przedrostek = True
    #     słowo = Słowo(litery,
    #                   jest_przedrostkiem=czy_przedrostek)

    #     stenosłowa = generator.wygeneruj(litery,
    #                                         limit_niedopasowania=0,
    #                                         limit_prób=15)
    #     dodane = generator.dodaj_słowa_do_słownika(słowo, stenosłowa)
    #     udało_się = len(dodane) > 0
    #     if not udało_się:
    #         # niepowodzenia.append((litery, frekwencja))
    #         użyto_modyfikatorów = 0
    #         nowe_stenosłowa = stenosłowa
    #         while not udało_się and użyto_modyfikatorów < max_słów_na_akord:
    #             nowe_stenosłowa = generator.dodaj_modyfikator(nowe_stenosłowa)
    #             dodane = generator.dodaj_słowa_do_słownika(słowo, nowe_stenosłowa)
    #             udało_się = len(dodane) > 0
    #             użyto_modyfikatorów += 1
    #         if not udało_się:
    #             stenosłowa = generator.wygeneruj(litery,
    #                                              limit_niedopasowania=0,
    #                                              limit_prób=10,
    #                                              z_przedrostkiem=True)
    #             dodane = generator.dodaj_słowa_do_słownika(słowo, stenosłowa)
    #             udało_się = len(dodane) > 0
    #             if not udało_się:
    #                 # nowe_akordy = generator.dodaj_znaki_specjalne_do_słów(stenosłowa,
    #                 #                                                       limit_niedopasowania=2,
    #                 #                                                       limit_prób=15)
    #                 użyto_modyfikatorów = 0
    #                 nowe_stenosłowa = stenosłowa
    #                 while not udało_się and użyto_modyfikatorów < max_słów_na_akord:
    #                     nowe_stenosłowa = generator.dodaj_modyfikator(nowe_stenosłowa)
    #                     dodane = generator.dodaj_słowa_do_słownika(słowo, nowe_stenosłowa)
    #                     udało_się = len(dodane) > 0
    #                     użyto_modyfikatorów += 1
    #                 if not udało_się:
    #                     niepowodzenia.append((litery, frekwencja))
    #                 else:
    #                     istniejące_słowa.add(litery)
    #             else:
    #                 istniejące_słowa.add(litery)
    #         else:
    #             istniejące_słowa.add(litery)
    #     else:
    #         istniejące_słowa.add(litery)
    #     numer_generacji += 1        
    #     if numer_generacji % loguj_postęp_co == 0:
    #         log.info(f"{numer_generacji}: {litery} - wygenerowano")
    #     if numer_generacji % 100 == 0:
    #         log.debug(f"{numer_generacji}: {litery} - wygenerowano")


    log.info(f"Wczytałem {ile_przedrostków_wczytano} przedrostków, generuję...")
    for przedrostek in przedrostki:
        ile_dodano = fabryka.uruchom_linie(przedrostek, nazwa_ustawień="przedrostki")
        if ile_dodano == 0:
            niepowodzenia_przedrostków.append((przedrostek, 10))
    #     if przedrostek in istniejące_słowa or przedrostek.isnumeric():
    #         continue
    #     słowo = Słowo(przedrostek, jest_przedrostkiem=True)
    #     stenosłowa = generator.wygeneruj(przedrostek,
    #                                  limit_niedopasowania=1,
    #                                  limit_prób=10,
    #                                  z_gwiazdką=False)
    #     # if przedrostek == "by":
    #     #     log.error(f"prz {przedrostek}: {stenosłowa}")
    #     dodane = generator.dodaj_słowa_do_słownika(słowo, stenosłowa)
    #     udało_się = len(dodane) > 0
    #     if not udało_się:
    #         użyto_modyfikatorów = 0
    #         nowe_stenosłowa = stenosłowa
    #         while not udało_się and użyto_modyfikatorów < max_słów_na_akord:
    #             nowe_stenosłowa = generator.dodaj_modyfikator(nowe_stenosłowa)
    #             dodane = generator.dodaj_słowa_do_słownika(słowo, nowe_stenosłowa)
    #             udało_się = len(dodane) > 0
    #             użyto_modyfikatorów += 1
    #         if not udało_się:
    #             specjalne_stenosłowa = generator.dodaj_znaki_specjalne_do_słów(stenosłowa,
    #                                                                           limit_niedopasowania=3)
    #             dodane = generator.dodaj_słowa_do_słownika(słowo,
    #                                                         specjalne_stenosłowa)
    #             if not len(dodane) > 0:
    #                 niepowodzenia_przedrostków.append((przedrostek, 10))
    #             else:
    #                 istniejące_słowa.add(przedrostek)
    #         else:
    #             istniejące_słowa.add(przedrostek)
    #     else:
    #         istniejące_słowa.add(przedrostek)
    #     numer_generacji += 1
    # niepowodzenia_przedrostków_nowe = []
    # for przedrostek, freq in niepowodzenia_przedrostków:
    #     stenosłowa = generator.wygeneruj(przedrostek,
    #                                         limit_niedopasowania=3,
    #                                         limit_prób=10,
    #                                         bez_środka=True,
    #                                         z_gwiazdką=True)
    #     dodane = generator.dodaj_słowa_do_słownika(słowo,
    #                                                 stenosłowa)
    #     if len(dodane) == 0:
    #         log.error(f"Nie dodano przedrostka {przedrostek}")
    #         niepowodzenia_przedrostków_nowe.append((przedrostek, freq))
    #     else:
    #         istniejące_słowa.add(przedrostek)
    # niepowodzenia_przedrostków = niepowodzenia_przedrostków_nowe

    # ## Teraz z przedrostkami
    for limit_niedopasowania in range(max_niedopasowanie):
        log.info(f"Pętla {limit_niedopasowania + 1} z {max_niedopasowanie}")
        nowe_niepowodzenia = []
        nazwa_ustawień=f"frekwencja_{limit_niedopasowania}"

        for (niepowodzenie, frekwencja) in niepowodzenia:
            ile_dodano = fabryka.uruchom_linie(niepowodzenie, nazwa_ustawień)
            if ile_dodano == 0:
                nowe_niepowodzenia.append((niepowodzenie, frekwencja))
        niepowodzenia = nowe_niepowodzenia

    #         if litery in istniejące_słowa or litery.isnumeric():
    #             continue
    #         słowo = Słowo(litery)

    #         stenosłowa = generator.wygeneruj(litery, limit_niedopasowania, limit_prób=10)
    #         dodane = generator.dodaj_słowa_do_słownika(słowo, stenosłowa)
    #         udało_się = len(dodane) > 0
    #         if not udało_się:
    #             użyto_modyfikatorów = 0
    #             nowe_stenosłowa = stenosłowa
    #             while not udało_się and użyto_modyfikatorów < max_słów_na_akord:
    #                 nowe_stenosłowa = generator.dodaj_modyfikator(nowe_stenosłowa)
    #                 dodane = generator.dodaj_słowa_do_słownika(słowo, nowe_stenosłowa)
    #                 udało_się = len(dodane) > 0
    #                 użyto_modyfikatorów += 1
    #             stenosłowa = generator.wygeneruj(litery,
    #                                                 limit_niedopasowania,
    #                                                 z_przedrostkiem=True,
    #                                                 limit_prób=10)
    #             dodane = generator.dodaj_słowa_do_słownika(słowo, stenosłowa)
    #             udało_się = len(dodane) > 0
    #             if not udało_się:
    #                 użyto_modyfikatorów = 0
    #                 nowe_stenosłowa = stenosłowa
    #                 while not udało_się and użyto_modyfikatorów < max_słów_na_akord:
    #                     nowe_stenosłowa = generator.dodaj_modyfikator(nowe_stenosłowa)
    #                     dodane = generator.dodaj_słowa_do_słownika(słowo, nowe_stenosłowa)
    #                     udało_się = len(dodane) > 0
    #                     użyto_modyfikatorów += 1
    #                 if not udało_się:
    #                     nowe_niepowodzenia.append((litery, frekwencja))
    #             else:
    #                 istniejące_słowa.add(litery)
    #         else:
    #             istniejące_słowa.add(litery)
    #         numer_generacji += 1        
    #         if numer_generacji % loguj_postęp_co == 0:
    #             log.info(f"{numer_generacji}: {słowo} - wygenerowano")
    #         if numer_generacji % 100 == 0:
    #             log.debug(f"{numer_generacji}: {słowo} - wygenerowano")
    #     niepowodzenia = nowe_niepowodzenia
    # ## Za pętlą
    log.info(f"Dodano {len(słownik) - linie_bazy} słów.")


    log.info("Dodaję słowa bez podanej częstotliwości")
    nazwa_ustawień=f"frekwencja_{max_niedopasowanie}"
    for słowo in sylaby_słowa.keys():
        ile_dodano = fabryka.uruchom_linie(słowo, nazwa_ustawień)
        if ile_dodano == 0:
            niepowodzenia.append((słowo, 1))

    # istniejące_słowa = słownik.keys()
    #     if litery in istniejące_słowa or litery.isnumeric():
    #         continue
    #     słowo = Słowo(litery)
    #     stenosłowa = generator.wygeneruj(litery,
    #                                         limit_niedopasowania=max_niedopasowanie,
    #                                         limit_prób=10)
    #     dodane = generator.dodaj_słowa_do_słownika(słowo, stenosłowa)
    #     udało_się = len(dodane) > 0
    #     if not udało_się:
    #         użyto_modyfikatorów = 0
    #         nowe_stenosłowa = stenosłowa
    #         while not udało_się and użyto_modyfikatorów < max_słów_na_akord:
    #             nowe_stenosłowa = generator.dodaj_modyfikator(nowe_stenosłowa)
    #             dodane = generator.dodaj_słowa_do_słownika(słowo, nowe_stenosłowa)
    #             udało_się = len(dodane) > 0
    #             użyto_modyfikatorów += 1

    #         stenosłowa = generator.wygeneruj(litery,
    #                                             limit_niedopasowania=max_niedopasowanie,
    #                                             limit_prób=10,
    #                                             z_przedrostkiem=True)
    #         dodane = generator.dodaj_słowa_do_słownika(słowo, stenosłowa)
    #         udało_się = len(dodane) > 0
    #         if not udało_się:
    #             użyto_modyfikatorów = 0
    #             nowe_stenosłowa = stenosłowa
    #             while not udało_się and użyto_modyfikatorów < max_słów_na_akord:
    #                 nowe_stenosłowa = generator.dodaj_modyfikator(nowe_stenosłowa)
    #                 dodane = generator.dodaj_słowa_do_słownika(słowo, nowe_stenosłowa)
    #                 udało_się = len(dodane) > 0
    #                 użyto_modyfikatorów += 1
    #             if not udało_się:
    #                 niepowodzenia.append((litery, frekwencja))
    #     numer_generacji += 1
    #     if numer_generacji % loguj_postęp_co == 0:
    #         log.info(f"{numer_generacji}: {litery} - wygenerowano")
    #     if numer_generacji % 100 == 0:
    #         log.debug(f"{numer_generacji}: {litery} - wygenerowano")


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


    log.info(f"Dodano {len(słownik) - linie_bazy} słów w {time.time() - czas_start} sekund.")
    log.info(f"Nie powiodło się dodawanie kombinacji dla {len(niepowodzenia)} słów.")
    log.info(f"Nie powiodło się dodawanie kombinacji dla {len(niepowodzenia_przedrostków)} przedrostków.")

    log.info("Słownik utworzony, zapisuję...")
    pisarz = Pisarz(args.slownik)
    fabryka.zapisz_rezultaty(pisarz)

    log.info(f"Zapisuję porażki")
    pisarz.zapisz_porażki(niepowodzenia+niepowodzenia_przedrostków)
    log.info("Fajrant")
            

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

