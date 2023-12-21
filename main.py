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
    parser.add_argument('--słowa_z_drzewa', default='wyniki/slowa_z_drzewa.csv',
                        help='rezultaty f-cji utwórz_drzewo_binarne_z_listy_par_sylaba_frekwencja')
    # parser.add_argument('--baza', default='wyniki/spektralny-slowik_niesortowany.json',
    parser.add_argument('--baza', default='wyniki/baza-0abs.json',
                        help='początkowy plik słownika w formacie JSON')
    parser.add_argument('--max_niedopasowanie', default='11',
                        help='Parametr generatora, 0 - tylko słowa idealnie pasujące, więcej niż 0 - słowa z brakującymi literami w akordzie')
    parser.add_argument('--max_słów_na_akord', default='7',
                        help='Ile maksymalnie słów może zawierać jeden akord')
    # parser.add_argument('--konfiguracja', default='ustawienia/konfiguracja_trillo.py',
    # parser.add_argument('--konfiguracja', default='ustawienia/konfiguracja_trillo_mod.py',
    parser.add_argument('--konfiguracja', default='ustawienia/konfiguracja_trillo_mod_kinesis.py',
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
    log.error(f'Argumenty: {str(args)[10:-1]}')

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
    for linia in czytacz.czytaj_linie_pliku(args.przedrostki):
        przedrostki.append(linia)
    istniejące_słowa = set()

    słownik = collections.defaultdict(dict)
    linie_bazy = 0
    if args.baza:
        log.info(f"Czytam bazę słownika z {args.baza}")
        (słownik, linie_bazy) = czytacz.wczytaj_bazę_do_słownika(log, args.baza)
        log.info(f"Baza wczytana")

    log.info("Generuję klawisze dla małych i dużych liter...")
    # TODO: to trzeba przepuścić przez Fabrykę, bo za dużo tu hakowania
    # wejścia = konfiguracja.KonfiguracjaJęzyka.fonemy_samogłoskowe +\
    #   konfiguracja.KonfiguracjaJęzyka.fonemy_spółgłoskowe
    klucze = []
    # log.info(f"slownik: {słownik.items()}")
    # for (slowo, (akord, _niedo)) in słownik.items():
    for item in słownik.items():
        # log.info(f"item: {item}")
        (_slowo, akordy) = item
        for akord in akordy.keys():
            klucze.append(akord)
    # log.info(f"klucze: {klucze}")
    for wejście in konfiguracja.KonfiguracjaJęzyka.fonemy_samogłoskowe.items():
        (fonem, (akord_lewy, akord_prawy)) = wejście
        if akord_lewy == "" or akord_prawy == "":
            continue

        if akord_lewy in klucze:
            akord_lewy += "~"
        klucz = fonem
        if fonem not in konfiguracja.KonfiguracjaJęzyka.jednoliterowe_wyrazy:
            klucz = "{&"+fonem+"}"
        słownik[klucz][akord_lewy] = 0
        if akord_prawy in klucze:
            akord_prawy = "~" + akord_prawy
        else:
            akord_prawy = "-" + akord_prawy
        klucz = klucz.upper()
        słownik[klucz][akord_prawy] = 0

    for wejście in konfiguracja.KonfiguracjaJęzyka.fonemy_spółgłoskowe.items():
        (fonem, (akord_lewy, akord_prawy)) = wejście
        if len(fonem) > 1:# and fonem.endswith("i"):
            continue
        if akord_lewy in klucze:
            akord_lewy += "~"
        klucz = fonem
        if fonem not in konfiguracja.KonfiguracjaJęzyka.jednoliterowe_wyrazy:
            klucz = "{&"+fonem+"}"
        słownik[klucz][akord_lewy] = 0
        if akord_prawy in klucze:
            akord_prawy = "~" + akord_prawy
        else:
            akord_prawy = "-" + akord_prawy
        klucz = klucz.upper()
        słownik[klucz][akord_prawy] = 0

    # (sylaby_słowa, ile_słów_wczytano) = czytacz.wczytaj_słowa(log, args.slowa)
    generator = Generator(log, język, klawiatura, konfiguracja, słownik)
    fabryka = Fabryka(log, konfiguracja, słownik, przedrostki)
    czas_start = time.time()
    niepowodzenia = []
    ilość_niepowodzeń = 0
    niepowodzenia_sylab = []
    niepowodzenia_sylab_podwójnych = []
    niepowodzenia_przedrostków = []
    potencjalne_niepowodzenia = []

    pisarz = Pisarz(args.slownik)
    frekwencje = SłownikDomyślny(lambda x: 1)
    if not czytacz.sprawdź_czy_plik_istnieje(args.słowa_z_drzewa):
        log.info(f"Plik {args.słowa_z_drzewa} nie istnieje, generuję sylaby wg frekwencji...")
        postęp = 0
        lista_par = []
        for (wejście, frekwencja) in czytacz.czytaj_z_pliku_frekwencji(args.frekwencja):
            frekwencje[wejście] = frekwencja
        log.info("Plik frekwencji wczytany, tworzę plik wejściowy dla binarnego drzewa sylab...")
        for (słowo, sylaby) in sylaby_słowa.items():
            # lista_par.append((sylaby, frekwencje[słowo]))
            lista_par.append((generator.sylaby_słowa[słowo], frekwencje[słowo]))
            postęp += 1
            if postęp % 100000 == 0:
                log.info(f"{postęp}: {słowo}")
        log.info("Plik wejściowy utworzony, generuję drzewo...")
        drzewo = utwórz_drzewo_binarne_z_listy_par_sylaba_frekwencja(lista_par)
        log.info("Drzewo utworzone, zapisuję...")
        pisarz.zapisz_surowe(args.słowa_z_drzewa, drzewo.następny())
        log.info(f"Plik {args.słowa_z_drzewa} zapisany na dysku")
    log.info(f"Czytam z pliku {args.słowa_z_drzewa}")

    nazwy_ustawień = []
    for limit_niedopasowania in range(max_niedopasowanie):
        nazwy_ustawień.append(f"frekwencja_{limit_niedopasowania}")

    log.info("Generuję słowa jednosylabowe")
    for (wejście, sylaby) in czytacz.czytaj_sylaby(args.słowa_z_drzewa):
        # log.info(f"> {wejście}")
        if len(sylaby) > 1:
            continue
        if wejście.startswith('*'):
            continue  # TODO: do poprawy
            # wejście = wejście[1:]
            # fabryka.uruchom_linie(wejście, nazwa_ustawień="rdzeń", sylaby=sylaby)
            # ile_dodano = 1
        elif wejście.startswith('&'):
            wejście = wejście[1:]
            ile_dodano = fabryka.uruchom_linie(wejście, nazwa_ustawień="przedrostki", sylaby=sylaby)
        else:
            # for limit_niedopasowania in range(max_niedopasowanie):
            ile_dodano = fabryka.uruchom_linie(wejście,
                                                   nazwa_ustawień="jednosylabowiec",
                                                   sylaby=sylaby)
                # if ile_dodano > 0:
                #     break
        if ile_dodano == 0:
            niepowodzenia.append((wejście, frekwencje[wejście]))
            ilość_niepowodzeń += 1

    # log.info(f"Pozostałe niepowodzenia: {ilość_niepowodzeń}")
    log.info("Generuję pojedyncze sylaby")
    ilość_niepowodzeń_sylab = 0
    pojedyncze_sylaby = collections.OrderedDict()
    for (wejście, sylaby) in czytacz.czytaj_sylaby(args.słowa_z_drzewa):
        for sylaba in sylaby:
            pojedyncze_sylaby[sylaba] = None
    for sylaba in pojedyncze_sylaby.keys():
        # for limit_niedopasowania in range(max_niedopasowanie):
        #     if limit_niedopasowania > 0:
        #         log.debug(f"Limit {limit_niedopasowania}, sylaba: {sylaba}")
        ile_dodano = fabryka.uruchom_linie(sylaba, nazwa_ustawień="sylaba")
                                           #nazwy_ustawień[limit_niedopasowania])
        # if ile_dodano > 0:
        #     break
        if ile_dodano == 0:
            niepowodzenia_sylab.append((sylaba, frekwencje[wejście]))
            ilość_niepowodzeń_sylab += 1
    log.info(f"Niepowodzenia sylab: {ilość_niepowodzeń_sylab}")
    klucze_słownika = słownik.keys()
    filtrowane_niepowodzenia = []
    for n in niepowodzenia:
        if n[0] not in klucze_słownika:
            filtrowane_niepowodzenia.append(n)
        # else:
        #     log.info(f"{n[0]} dodane")
    niepowodzenia_jednosylabowców = filtrowane_niepowodzenia
    niepowodzenia = []
    log.info(f"Niepowodzenia: {len(niepowodzenia_jednosylabowców)}")
    

    log.info("Generuję słowa dwusylabowe")
    for (wejście, sylaby) in czytacz.czytaj_sylaby(args.słowa_z_drzewa):
        if len(sylaby) != 2:
            continue
        if wejście.startswith('*'):
            continue  # TODO: do poprawy
            # wejście = wejście[1:]
            # fabryka.uruchom_linie(wejście, nazwa_ustawień="rdzeń")
            # ile_dodano = 1
        elif wejście.startswith('&'):
            wejście = wejście[1:]
            ile_dodano = fabryka.uruchom_linie(wejście, nazwa_ustawień="przedrostki", sylaby=sylaby)
        else:
            # for limit_niedopasowania in range(5, max_niedopasowanie):
            ile_dodano = fabryka.uruchom_linie(wejście,
                                                   nazwa_ustawień="dwusylabowiec",
                                                   sylaby=sylaby)
                # if ile_dodano > 0:
                #     break
        if ile_dodano == 0:
            niepowodzenia.append((wejście, frekwencje[wejście]))
            ilość_niepowodzeń += 1

    log.info(f"Pozostałe niepowodzenia: {ilość_niepowodzeń}")
    log.info("Generuję niektóre podwójne sylaby")
    podwójne_sylaby = collections.OrderedDict()
    for (wejście, sylaby) in czytacz.czytaj_sylaby(args.słowa_z_drzewa):
        ile_sylab = len(sylaby)
        for i in range(0, ile_sylab - 1, 2):
            podwójna_sylaba = sylaby[i] + sylaby[i+1]
            # if podwójna_sylaba[-1] in konfiguracja.KonfiguracjaJęzyka.samogłoski:
            podwójne_sylaby[podwójna_sylaba] = None
    for sylaba in podwójne_sylaby.keys():
        for limit_niedopasowania in range(max_niedopasowanie):
        #     if limit_niedopasowania > 0:
        #         log.debug(f"Limit {limit_niedopasowania}, sylaba: {sylaba}")
            ile_dodano = fabryka.uruchom_linie(sylaba, nazwa_ustawień=nazwy_ustawień[limit_niedopasowania])
            if ile_dodano > 0:
                break
        if ile_dodano == 0:
            niepowodzenia_sylab_podwójnych.append((sylaba, frekwencje[wejście]))
    log.info(f"Niepowodzenia sylab podwójnych: {niepowodzenia_sylab_podwójnych}")
    fabryka.zawsze_startuj_wszystkie_linie = False

    klucze_słownika = słownik.keys()
    filtrowane_niepowodzenia = []
    for n in niepowodzenia:
        if n[0] not in klucze_słownika:
            filtrowane_niepowodzenia.append(n)
        # else:
        #     log.info(f"{n[0]} dodane")
    niepowodzenia = niepowodzenia_jednosylabowców + filtrowane_niepowodzenia
    ilość_niepowodzeń = len(niepowodzenia)
    log.info(f"Niepowodzenia: {ilość_niepowodzeń}")


    # log.info("Generuję słowa trójsylabowe")
    # for (wejście, sylaby) in czytacz.czytaj_sylaby(args.słowa_z_drzewa):
    #     if len(sylaby) != 3:
    #         continue
    #     if wejście.startswith('*'):
    #         continue  # TODO: do poprawy
    #         # wejście = wejście[1:]
    #         # fabryka.uruchom_linie(wejście, nazwa_ustawień="rdzeń", sylaby=sylaby)
    #         # ile_dodano = 1
    #     elif wejście.startswith('&'):
    #         wejście = wejście[1:]
    #         ile_dodano = fabryka.uruchom_linie(wejście, nazwa_ustawień="przedrostki", sylaby=sylaby)
    #     else:
    #         for limit_niedopasowania in range(max_niedopasowanie):
    #             ile_dodano = fabryka.uruchom_linie(wejście,
    #                                                nazwa_ustawień=nazwy_ustawień[limit_niedopasowania], sylaby=sylaby)
    #             if ile_dodano > 0:
    #                 break
    #     if ile_dodano == 0:
    #         niepowodzenia.append((wejście, frekwencje[wejście]))
    #         ilość_niepowodzeń += 1

    # log.info(f"Pozostałe niepowodzenia: {ilość_niepowodzeń}")
    # log.info("Generuję niektóre potrójne sylaby")
    # potrójne_sylaby = collections.OrderedDict()
    # for (wejście, sylaby) in czytacz.czytaj_sylaby(args.słowa_z_drzewa):
    #     ile_sylab = len(sylaby)
    #     for i in range(0, ile_sylab - 2, 3):
    #         potrójna_sylaba = sylaby[i] + sylaby[i+1] + sylaby[i+2]
    #         # if potrójna_sylaba[-1] in konfiguracja.KonfiguracjaJęzyka.samogłoski:
    #         potrójne_sylaby[potrójna_sylaba] = None
    # for sylaba in potrójne_sylaby.keys():
    #     # for limit_niedopasowania in range(max_niedopasowanie):
    #     #     if limit_niedopasowania > 0:
    #     #         log.debug(f"Limit {limit_niedopasowania}, sylaba: {sylaba}")
    #     ile_dodano = fabryka.uruchom_linie(sylaba, nazwa_ustawień="sylaby", sylaby=sylaby)
    #                                        # =nazwy_ustawień[limit_niedopasowania])
    #         # if ile_dodano > 0:
    #         #     break
    #     if ile_dodano == 0:
    #         niepowodzenia_sylab_podwójnych.append((sylaba, frekwencje[wejście]))
    # log.info(f"Niepowodzenia sylab podwójnych: {niepowodzenia_sylab_podwójnych}")

    # wygeneruj_max = 10
    # wygenerowano = 0

    # log.info(f"Pozostałe niepowodzenia: {ilość_niepowodzeń}")
    # log.info("Dodaję słowa z drzewa")
    # for (wejście, sylaby) in czytacz.czytaj_sylaby(args.słowa_z_drzewa):
    #     if wejście.startswith('*'):
    #         # continue  # TODO: do poprawy
    #         wejście = wejście[1:]
    #         fabryka.uruchom_linie(wejście, nazwa_ustawień="rdzeń", sylaby=sylaby)
    #         ile_dodano = 1
    #     elif wejście.startswith('&'):
    #         wejście = wejście[1:]
    #         ile_dodano = fabryka.uruchom_linie(wejście, nazwa_ustawień="przedrostki", sylaby=sylaby)
    #     else:
    #         # for limit_niedopasowania in range(min(max_niedopasowanie, len(sylaby)), max_niedopasowanie):
    #         limit_niedopasowania = 10
    #         ile_dodano = fabryka.uruchom_linie(wejście,
    #                                                nazwa_ustawień=nazwy_ustawień[limit_niedopasowania],
    #                                                sylaby=sylaby)
    #             # if ile_dodano > 0:
    #             #     break
    #     if ile_dodano == 0:
    #         if len(sylaby) < 3:
    #             potencjalne_niepowodzenia.append((wejście, frekwencje[wejście]))
    #         else:
    #             niepowodzenia.append((wejście, frekwencje[wejście]))
    #             ilość_niepowodzeń += 1



    #     wygenerowano += 1
    #     # log.info(f"Wyg: {wygenerowano}, max: {wygeneruj_max}")
    #     if wygenerowano > wygeneruj_max:
    #         break

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
    log.info(f"Pozostałe niepowodzenia: {ilość_niepowodzeń}")
    for limit_niedopasowania in range(max_niedopasowanie):
        log.info(f"Pętla {limit_niedopasowania + 1} z {max_niedopasowanie}")
        nowe_niepowodzenia = []
        ilość_niepowodzeń = 0
        nazwa_ustawień=f"frekwencja_{limit_niedopasowania}"

        for (niepowodzenie, frekwencja) in niepowodzenia:
            ile_dodano = fabryka.uruchom_linie(niepowodzenie, nazwa_ustawień)
            if ile_dodano == 0:
                nowe_niepowodzenia.append((niepowodzenie, frekwencja))
                ilość_niepowodzeń += 1
        niepowodzenia = nowe_niepowodzenia
        log.info(f"Pozostałe niepowodzenia: {ilość_niepowodzeń}")
    log.info(f"Dodano {len(słownik) - linie_bazy} słów.")


    # log.info("Dodaję słowa bez podanej częstotliwości")
    # nazwa_ustawień=f"frekwencja_{max_niedopasowanie}"
    # for słowo in sylaby_słowa.keys():
    #     ile_dodano = fabryka.uruchom_linie(słowo, nazwa_ustawień)
    #     if ile_dodano == 0:
    #         niepowodzenia.append((słowo, 1))


    log.info(f"Dodano {len(słownik) - linie_bazy} słów w {time.time() - czas_start} sekund.")
    log.info(f"Nie powiodło się dodawanie kombinacji dla {len(niepowodzenia)} słów.")
    log.info(f"Nie powiodło się dodawanie kombinacji dla {len(niepowodzenia_sylab)} sylab.")
    # log.info(f"Nie powiodło się dodawanie kombinacji dla {len(niepowodzenia_sylab_podwójnych)} sylab podwójnych.")
    # log.info(f"Nie powiodło się dodawanie kombinacji dla {len(niepowodzenia_przedrostków)} przedrostków.")

    log.info("Słownik utworzony, zapisuję...")
    log.info(f"Zapisuję porażki")
    pisarz.zapisz_porażki(niepowodzenia \
                          # + niepowodzenia_sylab \
                          # + niepowodzenia_sylab_podwójnych \
                          # + niepowodzenia_przedrostków
                          # + potencjalne_niepowodzenia  # dla j. polskiego dodawane są wszystkie 1. i 2. sylabowce
                          )
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

