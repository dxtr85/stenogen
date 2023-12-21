from generator import Generator
from jezyk import Język, Słowo
from klawiatura import Klawiatura
from stos import Stos
import collections

class Fabryka():
    def __init__(self, log, konfiguracja, słownik_ostateczny, przedrostki):
        self.log = log
        self.słownik = słownik_ostateczny
        self.konfiguracja = konfiguracja
        self.jednoliterowe_wyrazy = konfiguracja.KonfiguracjaJęzyka.jednoliterowe_wyrazy
        self.zawsze_startuj_wszystkie_linie = konfiguracja.KonfiguracjaFabryki.zawsze_startuj_wszystkie_linie
        self.minimum_kombinacji_dodanych_per_słowo = konfiguracja.KonfiguracjaFabryki.minimum_kombinacji_dodanych_per_słowo
        self.ustawienia_fabryki = konfiguracja.KonfiguracjaFabryki.ustawienia_fabryki
        self.max_słów_na_akord = konfiguracja.KonfiguracjaFabryki.max_słów_na_akord
        self.loguj_postęp_co = konfiguracja.KonfiguracjaFabryki.loguj_postęp_co
        self.aktualne_ustawienia = []
        self.język = Język(log, konfiguracja.KonfiguracjaJęzyka)
        self.klawiatura = Klawiatura(log, konfiguracja.KonfiguracjaKlawiatury, self.język)
        self.generator = Generator(log,
                                   self.język,
                                   self.klawiatura,
                                   konfiguracja,
                                   słownik_ostateczny) #,
                                   # sylaby)
        self.stos = Stos(log, self.generator)
        self.typ_generacji = None
        self.numer_generacji = 0
        self.przedrostki = przedrostki
        # self.istniejące_słowa = set()
        self.niepowodzenie_linii = None
        self.wyjście_z_poprzedniej_linii_niepowodzenia = None
        self.wejścia = []

        # for słowo in self.słownik.keys():
        #     self.istniejące_słowa.add(słowo)

    def ustaw_przedrostki(self, przedrostki, generuj=False):
        self.przedrostki += przedrostki

    def ustaw_linie_produkcyjne(self, nazwa_ustawień):
        self.ile_dodano = 0
        self.aktualne_ustawienia = []
        for ustawienie in self.ustawienia_fabryki[nazwa_ustawień]:
            self.aktualne_ustawienia.append(ustawienie)

    def aktywuj_ustawienie(self, wejście):
        ustawienie = self.aktualne_ustawienia.pop(0)
        self.typ_generacji = ustawienie.typ_generacji
        self.z_przedrostkiem = ustawienie.z_przedrostkiem
        if ustawienie.tylko_porażki_na_wejściu:
            self.wejście = self.niepowodzenie_linii
            self.niepowodzenie_linii = None
            self.wyjścia_z_poprzedniej_linii = None
        elif ustawienie.tylko_wyniki_porażek_na_wejściu:
            self.wejście = self.wyjście_z_poprzedniej_linii_niepowodzenia
        else:
            self.wejście = wejście

        self.sprawdzaj_czy_jednoliterowe_słowo = ustawienie.sprawdzaj_czy_jednoliterowe_słowo
        self.jest_przedrostkiem = ustawienie.jest_przedrostkiem
        self.jest_rdzeniem = ustawienie.jest_rdzeniem
        self.czy_klejone = ustawienie.czy_klejone
        self.sprawdzaj_czy_jest_przedrostkiem = ustawienie.sprawdzaj_czy_jest_przedrostkiem
        self.limit_niedopasowania = ustawienie.limit_niedopasowania
        self.limit_prób = ustawienie.limit_prób

    def uruchom_linie(self, wejście, nazwa_ustawień, sylaby=None):
        self.ustaw_linie_produkcyjne(nazwa_ustawień)

        #  Poniższe jest zamotane dlatego, że chcę mieć tego loga do ulepszenia sylabizacji
        gen_sylaby = self.generator.sylaby_słowa[wejście]
        if not sylaby:
            sylaby = gen_sylaby
        else:
            if sylaby != gen_sylaby:
                self.log.debug(f"Generowane: {gen_sylaby} wczytane: {sylaby}")
                sylaby = gen_sylaby
        self.sylaby = sylaby

        self.można_przerwać = False
        # TODO: można zrobić, żeby opcjonalnie zawsze przechodzić wszystkie linie
        # self.log.info(f"uruchom_liniE {wejście}, {nazwa_ustawień} {self.typ_generacji}")
        while not self.można_przerwać and self.aktualne_ustawienia:
            self.aktywuj_ustawienie(wejście)
            self.uruchom_linię()
        return self.ile_dodano

    def uruchom_linię(self):
        self.niepowodzenie_linii = None
        self.wyjście_z_poprzedniej_linii_niepowodzenia = None
        # self.log.info(f"Fabryka wejście: {self.wejście}")
        if self.typ_generacji == self.konfiguracja.TypyGeneracji.StandardowaGeneracja:
            self.generacja_standardowa()
        elif self.typ_generacji == self.konfiguracja.TypyGeneracji.GeneracjaZDokładaniem:
            self.generacja_z_dokładaniem()
        elif self.typ_generacji == self.konfiguracja.TypyGeneracji.GeneracjaZnakówSpecjalnych:
            # self.log.info(f"spec: {self.wejście}")
            self.generacja_ze_znakami_specjalnymi()
        elif self.typ_generacji == self.konfiguracja.TypyGeneracji.GeneracjaZModyfikatorami:
            self.generacja_z_modyfikatorami()
        elif self.typ_generacji == self.konfiguracja.TypyGeneracji.SylabizowaniePoTrzy:
            self.generacja_sylabizowana(3)
        elif self.typ_generacji == self.konfiguracja.TypyGeneracji.SylabizowaniePoDwie:
            self.generacja_sylabizowana(2)
        elif self.typ_generacji == self.konfiguracja.TypyGeneracji.SylabizowaniePojedyncze: 
            self.generacja_sylabizowana(1)
        self.numer_generacji += 1        
        if self.numer_generacji % self.loguj_postęp_co == 0:
            self.log.info(f"{self.numer_generacji}: {self.sylaby} - wygenerowano")

    def generacja_standardowa(self):
        if not self.wejście:
            return
        if isinstance(self.wejście, tuple):
            (self.wejście, słowo_całe, stenosłowa) = self.wejście
        # self.log.info(f"std in: {self.wejście}")
        if self.wejście.isnumeric():
            # self.wejście_dodane = True
            # self.ile_dodano += 1
            return
        if self.sprawdzaj_czy_jednoliterowe_słowo and\
          self.wejście in self.jednoliterowe_wyrazy:
            self.czy_klejone = False

        czy_przedrostek = False
        if self.sprawdzaj_czy_jest_przedrostkiem and\
          self.wejście in self.przedrostki:
            # self.log.info(f"{self.wejście} jest przedrostkiem")
            czy_przedrostek = True

        słowo = Słowo(self.wejście,
                      jest_przedrostkiem=czy_przedrostek,
                      klejone=self.czy_klejone,
                      jest_rdzeniem=self.jest_rdzeniem)
        # self.log.info(f"Sylaby: {self.sylaby}")
        stenosłowa = self.generator.wygeneruj(self.wejście,
                                              limit_niedopasowania=self.limit_niedopasowania,
                                              sylaby=self.sylaby,
                                              limit_prób=self.limit_prób,
                                              z_przedrostkiem=self.z_przedrostkiem)
        # self.log.info(f"std: {stenosłowa} {self.z_przedrostkiem}")
        if self.jest_rdzeniem:
            if stenosłowa:
                ssłowo = stenosłowa[0]
                for isłowo in stenosłowa[1:]:
                    if isłowo.długość() < ssłowo.długość():
                        ssłowo = isłowo
                # self.stos.połóż_na_stosie(self.sylaby, słowo, ssłowo)
                stenosłowa = [ssłowo]
            else:
                self.log.error(f"Nie znalazłem kombinacji dla rdzenia '{self.wejście}'")
        dodane = self.generator.dodaj_słowa_do_słownika(słowo, stenosłowa)
        udało_się = len(dodane) > 0
        if udało_się and self.jest_przedrostkiem:
            self.generator.przedrostki.add(self.wejście)

        # self.log.info(f"koniec std, {udało_się}, {słowo}, {stenosłowa}")
        self.aktualizuj_wyjścia(udało_się, słowo, stenosłowa)

    def generacja_z_dokładaniem(self):
        if not self.wejście:
            return
        # self.log.info(f"Z dokładaniem: {self.wejście}")
        (self.wejście, słowo_całe, stenosłowa) = self.wejście
        #  TODO: znaleźć najdłuższy ciąg sylab, jaki już jest dodany do słownika
        #        i wygenerować akord dla pozostałych sylab;
        #        połączyć je razem i spróbować dodać do słownika.
        #        Można powtórzyć z drugim najdłuższym ciągiem sylab w przypadku
        #        niepowodzenia.
        #  TODO: uaktualnić słowo startowe jako przedrostek/łączone
        dopasowanie = self.stos.dopasuj_do_sylab(self.sylaby)
        # if dopasowania:
        #     self.log.info(f"Stos zadziałał: {self.sylaby} {dopasowania}")
        łączone_stenosłowa = []
        udało_się = False
        stenosłowa = []
        if dopasowanie:
            (która_sylaba, słowo, stare_stenosłowa) = dopasowanie
            stenosłowa = self.generator.wygeneruj(self.wejście,
                                                limit_niedopasowania=self.limit_niedopasowania,
                                                sylaby=self.sylaby[która_sylaba:],
                                                limit_prób=self.limit_prób)
            łączone_stenosłowa = []
            dodane = []
            if stare_stenosłowa:
                if isinstance(stare_stenosłowa, list):
                    for stare_stenosłowo in stare_stenosłowa:
                        łączone_stenosłowa += stare_stenosłowo.kombinuj(stenosłowa)
                else:
                    łączone_stenosłowa += stare_stenosłowa.kombinuj(stenosłowa)
                dodane = self.generator.dodaj_słowa_do_słownika(słowo_całe, łączone_stenosłowa)
            udało_się = len(dodane) > 0
            if udało_się:
                słowo.ustaw_rdzeń_użyty()
                # break

        # self.log.info(f"koniec std, {udało_się}, {słowo}, {stenosłowa}")
        self.aktualizuj_wyjścia(udało_się, słowo_całe, stenosłowa)

    def generacja_ze_znakami_specjalnymi(self):
        if not self.wejście:
            return
        # self.log.info(f"Ze znakami: {self.wejście}")
        (self.wejście, słowo, stenosłowa) = self.wejście
        nowe_stenosłowa = self.generator.dodaj_znaki_specjalne_do_słów(stenosłowa,
                                                                       limit_niedopasowania=self.limit_niedopasowania,
                                                                       limit_prób=self.limit_prób)
        # self.log.info(f"{słowo} dodane specjalne: {nowe_stenosłowa}")
        dodane = self.generator.dodaj_słowa_do_słownika(słowo, nowe_stenosłowa)
        udało_się = len(dodane) > 0
        self.aktualizuj_wyjścia(udało_się, słowo, stenosłowa)

    def generacja_z_modyfikatorami(self):
        if not self.wejście:
            return
        (self.wejście, słowo, stenosłowa) = self.wejście
        użyto_modyfikatorów = 0
        nowe_stenosłowa = stenosłowa
        udało_się = False
        while not udało_się and użyto_modyfikatorów < self.max_słów_na_akord:
            nowe_stenosłowa = self.generator.dodaj_modyfikator(nowe_stenosłowa)
            dodane = self.generator.dodaj_słowa_do_słownika(słowo, nowe_stenosłowa)
            udało_się = len(dodane) > 0
            użyto_modyfikatorów += 1
        self.aktualizuj_wyjścia(udało_się, słowo, stenosłowa)

    def generacja_sylabizowana(self, po_ile_sylab):
        if not self.wejście:
            return
        if isinstance(self.wejście, tuple):
            (self.wejście, słowo_całe, stenosłowa) = self.wejście
        # self.log.info(f"Grupuję po {po_ile_sylab}")
        czy_przedrostek = False
        if self.sprawdzaj_czy_jest_przedrostkiem and\
          self.wejście in self.przedrostki:
            czy_przedrostek = True
        słowo = Słowo(self.wejście,
                      jest_przedrostkiem=czy_przedrostek,
                      klejone=self.czy_klejone,
                      jest_rdzeniem=self.jest_rdzeniem)
        sylaby = self.podziel_na_sylaby()
        if len(sylaby) <= po_ile_sylab:
            return
        pogrupowane_sylaby = self.grupuj_sylaby(sylaby, po_ile_sylab)
        # self.log.info(f"Pogrupowane: {pogrupowane_sylaby}")
        steno_grupy = []
       
        for grupa in pogrupowane_sylaby:
            # self.log.info(f"Łączę: {grupa}")
            if len(grupa) == 0:
                return
            połączone_sylaby = ""
            for sylaba in grupa:
                połączone_sylaby += sylaba
            # self.log.info(f"Generuję dla {self.wejście} - {połączone_sylaby}")
            stenosłowa = self.generator.wygeneruj(połączone_sylaby,
                                                  sylaby=grupa,
                                                 limit_niedopasowania=self.limit_niedopasowania,  ## TODO aktualizacja limitu
                                                 limit_prób=self.limit_prób,
                                                 z_przedrostkiem=self.z_przedrostkiem)
            if not stenosłowa:
                return
            # self.log.info(f"Dodaję {stenosłowa}")
            steno_grupy.append(stenosłowa)
        # self.log.info(f"SGrupy: {steno_grupy}")
        if not steno_grupy:
            return
           
        początki = steno_grupy.pop(0)
        ile_grup_pozostało = len(steno_grupy)
        rezultaty = []
        while steno_grupy:
            # self.log.info(f"początki, {początki}")
            nowe_początki = []
            kontynuacje = steno_grupy.pop(0)           
            for początek in początki:
                nowe_początki += początek.kombinuj(kontynuacje)
            początki = nowe_początki
        if self.jest_rdzeniem:
            if początki:
                ssłowo = początki[0]
                self.stos.połóż_na_stosie(self.sylaby, słowo, ssłowo)
                self.generator.dodaj_rdzeń(słowo.litery, ssłowo)
            else:
                self.log.error(f"Nie znalazłem kombinacji dla rdzenia '{self.wejście}'")
            return
        dodane = self.generator.dodaj_słowa_do_słownika(słowo, początki)
        udało_się = len(dodane) > 0

        # self.log.info(f"koniec sylabizowania, {udało_się}, {słowo}, {początki}")
        self.aktualizuj_wyjścia(udało_się, słowo, początki)
       
    def aktualizuj_wyjścia(self, udało_się, słowo, stenosłowa):
        # self.log.info(f"Wejście przy aktualizuj: {self.wejście}")
        if not udało_się:
            self.niepowodzenie_linii = self.wejście
            self.wyjście_z_poprzedniej_linii_niepowodzenia = (self.wejście, słowo, stenosłowa)
        else:
            # self.log.debug(f"Kładę na stosie {self.sylaby} {stenosłowa}")
            self.stos.połóż_na_stosie(self.sylaby, słowo, stenosłowa)
            if self.jest_rdzeniem:
                self.generator.dodaj_rdzeń(słowo.litery, stenosłowa[0])
            self.ile_dodano += 1
            if not self.zawsze_startuj_wszystkie_linie and self.ile_dodano > self.minimum_kombinacji_dodanych_per_słowo:
                self.można_przerwać = True
            # self.wejście_dodane = True
            # self.istniejące_słowa.add(słowo.litery)

    def grupuj_sylaby(self, sylaby, po_ile_sylab):
        # self.log.info(f"{self.wejście} sylaby: {sylaby}")
        grupy = []
        ile_jest_w_grupie = 0
        grupa = []
        while sylaby and ile_jest_w_grupie < po_ile_sylab:
            grupa.append(sylaby.pop(0))
            ile_jest_w_grupie += 1
            if ile_jest_w_grupie >= po_ile_sylab:
                grupy.append(grupa)
                grupa = []
                ile_jest_w_grupie = 0
        if grupa:
            grupy.append(grupa)
        # self.log.info(f"Zgrupowałem: {grupy} {grupa}")
        return grupy

    def podziel_na_sylaby(self):
        try:
            # self.log.info(f"dzielę w traju")
            sylaby = self.generator.sylaby_słowa[self.wejście]
            sylaby = sylaby.copy()
        except KeyError as e:
            # self.log.info(f"dzielę except")
            # słowo_text = f"{słowo}"
            if self.wejście.isnumeric():
                # self.log.info(f"puste")
                sylaby = []
            if len(self.wejście) == 1:
                # self.log.info(f"len jeden")
                sylaby = [self.wejście]
                sylaby = sylaby.copy()
            else:
                # self.log.info(f"sylabizuje")
                sylaby = self.generator.język.pseudo_sylabizuj(self.wejście)
        # self.log.info(f"podzieliłem: {sylaby}")
        return sylaby

    def zapisz_rezultaty(self, pisarz):        
        pisarz.zapisz_niesortowane(self.generator.generuj_do_pliku())

        self.log.info("Zapis niesortowanego słownika zakończony, sortuję...")
        # self.log.debug(f"{self.generator.kombinacje.items()}")
        try:
            posortowany_słownik = collections.OrderedDict(
                sorted(self.generator.kombinacje.items(), key=lambda wpis:
                       [self.konfiguracja.KonfiguracjaKlawiatury.kolejność.index(k) for k in wpis[0]]))
        except ValueError as e:
            self.log.error(f"Coś nie sortuje: {e}")
            self.log.info(f"Czy na pewno plik bazy zawiera kombinacje tylko z dopuszczalnymi znakami dla tego układu?")
        self.log.info(f"Sortowanie zakończone, zapisuję  {len(posortowany_słownik)} wpisów...")
        pisarz.zapisz_sortowane(posortowany_słownik)
