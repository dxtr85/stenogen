#!/usr/bin/env python3
from logowanie import Logger
from generator import Generator
from jezyk import Język
from klawiatura import Klawiatura
from pomocnicy import Czytacz, Pisarz
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
    parser.add_argument('--baza', default='wyniki/baza-0.json',
                        help='początkowy plik słownika w formacie JSON')
    parser.add_argument('--konfiguracja', default='ustawienia/konfiguracja.py',
                        help='plik konfiguracji generatora')
    parser.add_argument('--slownik', default='wyniki/spektralny-slowik.json',
                        help='wynikowy plik JSON do załadowania do Plovera')
    args = parser.parse_args()

    czytacz = Czytacz()
    czytacz.stwórz_katalogi_jeśli_trzeba([args.log, args.slownik])
    # Spróbuj otworzyć plik logu
    log = Logger(args.log)
    log.info(f'Argumenty: {str(args)[10:-1]}')

    # Słownik wyjściowy, dane w formie:
    # {tekst: {"Kombinacja": niedopasowanie}}
    konfiguracja = czytacz.wczytaj_konfigurację(args.konfiguracja)
    if args.baza:
        log.info(f"Czytam bazę słownika z {args.baza}")
        (słownik, linie_bazy) = czytacz.wczytaj_bazę_do_słownika(args.baza)
        log.info(f"Baza wczytana")
    else:
        słownik = collections.defaultdict(dict)
        linie_bazy = 0

    istniejące_słowa = słownik.keys()
    (sylaby_słowa, ile_słów_wczytano) = czytacz.wczytaj_słowa(log, args.slowa)
    język = Język(log, konfiguracja.KonfiguracjaJęzyka)
    klawiatura = Klawiatura(log, konfiguracja.KonfiguracjaKlawiatury, język)
    generator = Generator(log, język, klawiatura, konfiguracja, słownik, sylaby_słowa)
    numer_generacji = 0
    loguj_postęp_co = 10000
    czas_start = time.time()
    niepowodzenia = []

    (przedrostki, ile_przedrostków_wczytano) = czytacz.wczytaj_słowa(log, args.przedrostki)
    log.info(f"Wczytałem {ile_przedrostków_wczytano} przedrostków, generuję...")
    for przedrostek in przedrostki:
        przedrostek_do_słownika = "{" + przedrostek + "^}"
        if przedrostek_do_słownika in istniejące_słowa or przedrostek.isnumeric():
            continue
        # sylaby = język.sylabizuj(przedrostek)
        akordy = generator.wygeneruj_akordy(przedrostek,
                                            limit_niedopasowania=2,
                                            limit_prób=10,
                                            z_gwiazdką=True)
        log.info(f"Akordy: {akordy}")
        dodane = generator.dodaj_akordy_do_słownika(przedrostek_do_słownika, akordy)
        udało_się = len(dodane) > 0
        if not udało_się:
            specjalne_akordy = generator.dodaj_znaki_specjalne_do_akordów(akordy,
                                                                          limit_niedopasowania=4)
            dodane = generator.dodaj_akordy_do_słownika(przedrostek_do_słownika, specjalne_akordy)
            if not len(dodane) > 0:
                niepowodzenia.append((przedrostek, 10))                
        numer_generacji += 1
    nowe_niepowodzenia = []
    for przedrostek, freq in niepowodzenia:
        akordy = generator.wygeneruj_akordy(przedrostek,
                                            limit_niedopasowania=5,
                                            limit_prób=10,
                                            bez_środka=True,
                                            z_gwiazdką=True)
        dodane = generator.dodaj_akordy_do_słownika(przedrostek_do_słownika, akordy)
        if len(dodane) == 0:
            log.error(f"Nie dodano przedrostka {przedrostek}")
            nowe_niepowodzenia.append((przedrostek, freq))
    niepowodzenia = nowe_niepowodzenia

     
    # log.info(f"Wczytałem sylaby dla {ile_słów_wczytano} słów, generuję klawisze...")
    # for (słowo, frekwencja) in czytacz.czytaj_z_pliku_frekwencji(args.frekwencja):
    #     if słowo in istniejące_słowa or słowo.isnumeric():
    #         continue

    #     akordy = generator.wygeneruj_akordy(słowo, limit_niedopasowania=0, limit_prób=10)
    #     dodane = generator.dodaj_akordy_do_słownika(słowo, akordy)
    #     udało_się = len(dodane) > 0
    #     if not udało_się:
    #         niepowodzenia.append((słowo, frekwencja))
    #     numer_generacji += 1        
    #     if numer_generacji % loguj_postęp_co == 0:
    #         log.info(f"{numer_generacji}: {słowo} - wygenerowano")
    #     if numer_generacji % 100 == 0:
    #         log.debug(f"{numer_generacji}: {słowo} - wygenerowano")

    # log.info(f"Dodano {len(słownik) - linie_bazy} słów.")


    # ##  Na czas developmentu wyłączone
    # log.info("Dodaję słowa bez podanej częstotliwości")
    # istniejące_słowa = słownik.keys()
    # frekwencja = 1
    # for słowo in sylaby_słowa.keys():
    #     if słowo in istniejące_słowa or słowo.isnumeric():
    #         continue
    #     akordy = generator.wygeneruj_akordy(słowo, limit_niedopasowania=10, limit_prób=10)
    #     dodane = generator.dodaj_akordy_do_słownika(słowo, akordy)
    #     udało_się = len(dodane) > 0
    #     if not udało_się:
    #         niepowodzenia.append((słowo, frekwencja))
    #     numer_generacji += 1


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


    # ##  Na czas developmentu wyłączone
    # log.info("Dodaję słowa bez podanej częstotliwości")
    # istniejące_słowa = słownik.keys()
    # frekwencja = 1
    # for słowo in sylaby_słowa.keys():
    #     if słowo in istniejące_słowa or słowo.isnumeric():
    #         continue
    #     udało_się = generator.wygeneruj_akordy(słowo, limit_niedopasowania=10, limit_prób=10)
    #     if not udało_się:
    #         niepowodzenia.append((słowo, frekwencja))
    #     numer_generacji += 1


    log.info(f"Dodano {len(słownik) - linie_bazy} słów w {time.time() - czas_start} sekund.")
    log.info(f"Nie powiodło się dodawanie kombinacji dla {len(niepowodzenia)} słów.")

    log.info("Słownik utworzony, zapisuję...")
    pisarz = Pisarz(args.slownik)
    pisarz.zapisz_niesortowane(generator.generuj_do_pliku())

    log.info("Zapis niesortowanego słownika zakończony, sortuję...")
    # kolejność = '/XFZSKTPVLRJE-~*IAUCRLBSGTWOY'
    kolejność = '/XFZDNTPVKRJE-~*IAUKZDWNTYOBC'
    # log.debug(f"{generator.kombinacje.items()}")
    try:
        posortowany_słownik = collections.OrderedDict(
            sorted(generator.kombinacje.items(), key=lambda wpis:
                   [kolejność.index(k) for k in wpis[0]]))
    except ValueError as e:
        log.error(f"Coś nie sortuje: {e}")
    log.info("Sortowanie zakończone, zapisuję...")
    pisarz.zapisz_sortowane(posortowany_słownik)

    log.info(f"Zapisuję porażki")
    pisarz.zapisz_porażki(niepowodzenia)
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

