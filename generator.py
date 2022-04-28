from pomocnicy import SłownikDomyślny
from klawiatura import Klawiatura, RękaLewa, RękaPrawa, Akord, StenoSłowo
from jezyk import Słowo
from collections import defaultdict

tylda = "~"
gwiazdka = "*"
myślnik = "-"
jot = "J"
ee = "E"
ii = "I"
aa = "A"
uu = "U"
nic = ""
tyldogwiazdka = "~*"
slash = "/"

class Generator():
    def __init__(self, log, język, klawiatura, konfiguracja, słownik_ostateczny): #, sylaby_słowa):
        self.log = log
        self.konfiguracja = konfiguracja
        self.język = język
        self.klawiatura = klawiatura
        # {tekst: {"Kombinacja": niedopasowanie}}
        # self.język = język
        self.słownik = słownik_ostateczny
        # self.sylaby_słowa = sylaby_słowa
        self.sylaby_słowa = SłownikDomyślny(lambda x: self.język.pseudo_sylabizuj(x))
        self.kombinacje = dict()
        self.przedrostki = set()
        self.rdzenie = dict()
        self._zainicjalizuj_kombinacje()
        self.loguj_postęp_co = 10000 # Będzie log po tylu wygenerowanych słowach
        # self.postęp = 0
        self.minimum_kombinacji_per_słowo = konfiguracja.KonfiguracjaGeneratora.minimum_kombinacji_per_słowo
        self.niepowodzenia = []
        self.analizowane_fonemy = defaultdict(lambda: 0)
        self.analizowane_końcówki = defaultdict(lambda: 0)
        self.modyfikator = Akord(self.log, "~", 0)
        self.dbg = []

    def dodaj_rdzeń(self, tekst, kombinacja):
        self.rdzenie[tekst] = kombinacja

    def _zainicjalizuj_kombinacje(self):
        self.log.info(f"Inicjalizuję bazę generatora ze słownika z {len(self.słownik)} wpisów")
        for (tekst, kombinacje) in self.słownik.items():
            for kombinacja in kombinacje.keys():
                self.kombinacje[kombinacja] = Słowo(tekst)
        self.log.info(f"Baza zainicjalizowana w pamięci ({len(self.kombinacje)} wpisów)")

    def dopasuj_słowa(self, słowo, stenosłowa):
        # if słowo.litery in self.dbg:
        # self.log.debug(f"Dopasowuje dla {słowo}, {stenosłowa}")
        słowa_dodane = []
        for stenosłowo in stenosłowa:
            # self.log.info(f"Teraz {stenosłowo} {type(stenosłowo)}")
            # if isinstance(akord, list):
            #     znaki = ""
            #     dł_ciągu = len(akord)
            #     for i in range(dł_ciągu):
            #         znaki +=f"{akord[i]}"
            #         if i < dł_ciągu -1:
            #             znaki +="/"
            #     niedopasowanie = akord[-1].niedopasowanie
            # else:
            #     niedopasowanie = akord.niedopasowanie
            #     znaki = f"{akord}"

            obecny_właściciel = None
            znaki = f"{stenosłowo}"
            niedopasowanie = stenosłowo.niedopasowanie
            if słowo.litery in self.dbg:
                self.log.debug(f"Niedo dla {stenosłowo}, {niedopasowanie}")

            if znaki not in self.kombinacje.keys():
                if słowo.litery in self.dbg:
                    self.log.debug(f"Nie ma, dodaje")
                self.kombinacje[znaki] = słowo
                self.słownik[słowo.litery][znaki] = niedopasowanie
                if słowo.litery in self.dbg:
                    self.log.debug(f"Po dodaniu: {self.słownik[słowo.litery]}, {self.kombinacje[znaki]}")

                słowa_dodane.append(stenosłowo)
            else:
                if słowo.litery in self.dbg:
                    self.log.debug(f"{znaki} już jest w słowniku")
                obecny_właściciel = self.kombinacje[znaki].litery
                if obecny_właściciel == słowo.litery:
                    słowa_dodane.append(stenosłowo)
                    continue
                kombinacje_właściciela = self.słownik[obecny_właściciel]
                ilość_kombinacji_właściciela = len(kombinacje_właściciela.keys())
                if ilość_kombinacji_właściciela <= self.minimum_kombinacji_per_słowo:
                    continue
                else:
                    # self.log.info(f"KW: {kombinacje_właściciela} {obecny_właściciel} {słowo.litery}")
                    obecne_niedopasowanie = kombinacje_właściciela[znaki]
                    #  Nie zabieramy kombinacji jeśli ich dopasowanie jest takie samo
                    # if obecne_niedopasowanie <= niedopasowanie:
                    #     continue

                    minimalne_niedopasowanie_u_właściciela = obecne_niedopasowanie
                    for obca_kombinacja, obce_niedopasowanie in kombinacje_właściciela.items():
                        if obce_niedopasowanie < minimalne_niedopasowanie_u_właściciela:
                            minimalne_niedopasowanie_u_właściciela = obce_niedopasowanie
                            break
                        elif obce_niedopasowanie == minimalne_niedopasowanie_u_właściciela and\
                             obca_kombinacja != znaki:
                            minimalne_niedopasowanie_u_właściciela = obce_niedopasowanie -1
                            break
                    if obecne_niedopasowanie > minimalne_niedopasowanie_u_właściciela:
                        # self.log.info(f"odbieram kombo, przed: {self.słownik[obecny_właściciel]}")
                        kombinacje_właściciela.pop(znaki)
                        # self.log.info(f"odbieram kombo, przed: {self.słownik[obecny_właściciel]}")
                        self.słownik[słowo.litery][znaki] = niedopasowanie
                        self.kombinacje[znaki] = słowo
                        słowa_dodane.append(stenosłowo)
        return słowa_dodane
                
    def wygeneruj(self, słowo,
                         limit_niedopasowania,
                         sylaby=None,
                         limit_prób=2,
                         bez_środka=False,
                         z_przedrostkiem=False,
                         z_gwiazdką=False):
        # self.postęp += 1

        # Dla 'w', 'z'
        if not sylaby:
            try:
                sylaby = self.sylaby_słowa[słowo]
            except KeyError as e:
                # słowo_text = f"{słowo}"
                if słowo.isnumeric():
                    return []
                if len(słowo) == 1:
                    sylaby = [słowo]
                else:
                    sylaby = self.język.sylabizuj(słowo)
                    # raise KeyError(f"Nie znam sylab, {e}")
        if słowo in self.dbg:
            self.log.debug(f"Szukam dla: {słowo} - {sylaby}")
        if z_przedrostkiem:
            akordy = []
            (przedrostek, sylaby, steno_przedrostki) = self.znajdź_przedrostek_dla_sylab(sylaby)
            if not przedrostek:
                return akordy
            # self.log.info(f"Z przedrostkiem {przedrostek}")
            podsłowo = ''.join(sylaby)
            if podsłowo in self.słownik.keys():
                # self.log.info(f"Z podsłowem {podsłowo}")
                steno_podsłowa = self.stenosłowa_dla_liter(podsłowo)
                # self.log.debug(f"Dostałem podakordy: {steno_podsłowa}")
                for akord in steno_podsłowa:
                    # self.log.info(f"AKtualizuję {kombinacja}")
                    akordy.append(akord)  ## TODO
                    # if isinstance(akord, list):
                    #     multi_akord = ""
                    #     dł_ciągu = len(akord)
                    #     for i in dł_ciągu:
                    #         multi_akord +=f"{akord[i]}"
                    #         if i < dł_ciągu -1:
                    #             multi_akord +="/"
                    #     słowo = self.kombinacje[f"{multi_akord}"]
                    # else:
                    #     słowo = self.kombinacje[f"{akord}"]
                    # if słowo.klejone:
                # self.log.info(f"w słowniku: {self.słownik[podsłowo]}")
                # self.log.info(f"{podsłowo} ma akordy: {steno_podsłowa}")
                # self.log.info(f"ako pod: {steno_podsłowa} dla {słowo}({przedrostek}/{podsłowo})")
                if isinstance(steno_podsłowa[0], list):
                    litery = ""
                    for podsłowo in steno_podsłowa[0]:
                        litery += f"{podsłowo}/"
                    self.kombinacje[f"{litery[:-1]}"].ustaw_klejone()  # TODO: to można zrobić tylko raz
                else:
                    self.kombinacje[f"{steno_podsłowa[0]}"].ustaw_klejone()  # TODO: to można zrobić tylko raz
                    
                # TODO uaktualnij obiekt Słowo dla podsłowo
            # else:
                # self.log.debug(f"bez podsłowa")
            akordy += self.klawiatura.wygeneruj_słowa(słowo,
                                                       sylaby,
                                                       limit_niedopasowania,
                                                       limit_prób, bez_środka,
                                                       z_gwiazdką)
        else:
            # self.log.debug(f"bez przedrostka")
            # self.log.info(f"{słowo} {type(słowo)}, {sylaby} {type(sylaby)}")
            akordy = self.klawiatura.wygeneruj_słowa(słowo,
                                                      sylaby,
                                                      limit_niedopasowania,
                                                      limit_prób, bez_środka,
                                                      z_gwiazdką)
            if słowo in self.dbg:
                self.log.debug(f"Bez przedrostka {słowo}: {akordy}")

        if z_przedrostkiem and przedrostek:
            nowe_akordy = []
            # for wygenerowany_akord in akordy:
            if not steno_przedrostki:
                steno_przedrostki = self.stenosłowa_dla_liter(przedrostek)
                ## TODO: przypadek gdy więcej kombinacji ma takie samo niedopasowanie
                ## wtedy jedna z tych kombinacji może zostać zabrana do innego słowa
            ile_przedrostkow_uwzględnić = min(self.minimum_kombinacji_per_słowo,\
                                              len(steno_przedrostki))
            for i in range(ile_przedrostkow_uwzględnić):
                steno_przedrostek = steno_przedrostki[i]
                multi_akord = steno_przedrostek.kombinuj(akordy)
                    # if isinstance(steno_przedrostek, list):
                    #     if isinstance(wygenerowany_akord, list):
                    #         multi_akord += wygenerowany_akord
                    #     else:
                    #         multi_akord.append(wygenerowany_akord)
                    # else:
                    #     if isinstance(wygenerowany_akord, list):
                    #         multi_akord = [multi_akord]
                    #         multi_akord += wygenerowany_akord
                    #     else:
                    #         multi_akord = [multi_akord, wygenerowany_akord]
                nowe_akordy += multi_akord
            # self.log.info(f"Zwracam z przedrostkiem: {nowe_akordy}")
            return nowe_akordy #.sort(key=lambda x: x.niedopasowanie)
        if słowo in self.dbg:
            self.log.debug(f"zwracam dla {słowo}: {akordy}")
        return akordy #.sort(key=lambda x: x.niedopasowanie)

    def dodaj_modyfikator(self, słowa):
        nowe_słowa = []
        for słowo in słowa:
            nowe_słowa.append(słowo + self.modyfikator)
        return nowe_słowa
        
    def dodaj_znaki_specjalne_do_słów(self,
                                         słowa,
                                         limit_niedopasowania,
                                         limit_prób=2):
        nowe_słowa = []
        for słowo in słowa:
            # if isinstance(akord, list):
            #     niedopasowanie = akord[-1].niedopasowanie
            # else:
            #     niedopasowanie = akord.niedopasowanie
            if słowo.niedopasowanie < limit_niedopasowania:
                # self.log.info(f"Dodaję po specjalne: {kombinacja}")
                nowe_słowo = self.klawiatura.dodaj_znaki_specjalne_do_słowa(słowo)
                nowe_słowa += nowe_słowo
        # self.log.info(f"Zwracam: {nowe_słowa}")
        return nowe_słowa

    def dodaj_słowa_do_słownika(self, słowo, stenosłowa):
        if słowo.litery in self.dbg:
            self.log.debug(f"Dostałem StenoSłowa: {stenosłowa}")
        dodane = []
        if not stenosłowa:
            # self.log.error(f"Brak akordów dla {słowo} ({stenosłowa})")
            return dodane
        dodane = self.dopasuj_słowa(słowo, stenosłowa)
        if słowo.jest_przedrostkiem and len(dodane) > 0:
            self.przedrostki.add(słowo.litery)
        return dodane

    # Ponieważ sortowanie może trochę zająć, warto zapisać co już mamy
    # w razie gdyby skończył się zapas RAMu
    def generuj_do_pliku(self):
        for (kombinacja, słowo) in self.kombinacje.items():
            # if tekst == "moc":
            #     self.log.info(f"generuje: {kombinacja}: {tekst}")

            yield f' "{kombinacja}": "{słowo}"'

    def analizuj_słowo(self, słowo, częstotliwość):
        try:
            sylaby = self.sylaby_słowa[słowo]
        except KeyError as e:
            if len(słowo) == 1:
                sylaby = [słowo]
            else:
                raise KeyError(f"Nie znam sylab, {e}")
        for sylaba in sylaby:
            (nagłos, _śródgłos, wygłos) = self.język.fonemy_sylaby[sylaba]
            for fonem in nagłos + wygłos:
                self.analizowane_fonemy[fonem] += częstotliwość

    def analizuj_końcówki(self, słowo, częstotliwość):
        try:
            sylaby = self.sylaby_słowa[słowo]
        except KeyError as e:
            if len(słowo) == 1:
                sylaby = [słowo]
            else:
                raise KeyError(f"Nie znam sylab, {e}")
        if len(sylaby) > 2:
            sylaba = sylaby[-1]
            self.analizowane_końcówki[sylaba] += częstotliwość
            self.analizuj_końcówkę(sylaba, częstotliwość)

    def analizuj_końcówkę(self, sylaba, częstotliwość):
            (nagłos, śródgłos, wygłos) = self.język.fonemy_sylaby[sylaba]
            if not wygłos:
                for fonem in nagłos + śródgłos:
                    self.analizowane_fonemy[fonem] += częstotliwość
            else:
                for fonem in nagłos + wygłos:
                    self.analizowane_fonemy[fonem] += częstotliwość

    def znajdź_przedrostek_dla_sylab(self, sylaby):
        sklejone_sylaby = sylaby[0]
        najdłuższy_przedrostek = None
        indeks_pozostałych_sylab = 0
        rdzenie = self.rdzenie.keys()
        if sklejone_sylaby in self.przedrostki or\
          sklejone_sylaby in rdzenie:
            najdłuższy_przedrostek = sklejone_sylaby
            indeks_pozostałych_sylab = 1
        for i in range(1, len(sylaby)):
            sklejone_sylaby += sylaby[i]
            if sklejone_sylaby in self.przedrostki or\
              sklejone_sylaby in rdzenie:
                najdłuższy_przedrostek = sklejone_sylaby
                indeks_pozostałych_sylab = i + 1
        steno_słowo = None
        if najdłuższy_przedrostek in rdzenie:
            steno_słowo = [self.rdzenie[najdłuższy_przedrostek]]
        return (najdłuższy_przedrostek, sylaby[indeks_pozostałych_sylab:], steno_słowo)

    def stenosłowa_dla_liter(self, litery):
        stenosłowa = []
        # self.log.info(f"jakie są: {self.słownik[litery]}")
        for (kombinacja, niedopasowanie) in self.słownik[litery].items():
            # TODO: a co jeśli mamy akord dwuczłonowy w słowniku?
            if slash in kombinacja:
                stenosłowo = StenoSłowo(self.log, [])
                # self.log.debug(f"jest slash")
                for podkombinacja in kombinacja.split(slash):
                    stenosłowo += Akord(self.log, podkombinacja, 0)
                # podakordy[-1].niedopasowanie = niedopasowanie
                stenosłowa.append(stenosłowo)
            else:
                # self.log.debug(f"bez slasha")
                stenosłowa.append(StenoSłowo(self.log,
                                             [Akord(self.log,
                                                    kombinacja,
                                                    niedopasowanie)]))
        # self.log.info(f"jakie zwracam: {akordy}")
        return stenosłowa
