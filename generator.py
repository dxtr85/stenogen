from klawiatura import Klawiatura, RękaLewa, RękaPrawa, Akord
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
    def __init__(self, log, język, klawiatura, konfiguracja, słownik_ostateczny, sylaby_słowa):
        self.log = log
        self.konfiguracja = konfiguracja
        self.język = język
        self.klawiatura = klawiatura
        # {tekst: {"Kombinacja": niedopasowanie}}
        # self.język = język
        self.słownik = słownik_ostateczny
        self.sylaby_słowa = sylaby_słowa
        # self.lewe_wszystkie = "LR~*"
        # self.prawe_wszystkie = "~*CR"
        self.kombinacje = dict()
        self.przedrostki = set()
        self._zainicjalizuj_kombinacje()
        self.loguj_postęp_co = 10000 # Będzie log po tylu wygenerowanych słowach
        self.postęp = 0
        self.minimum_kombinacji_per_słowo = 1
        self.niepowodzenia = []
        self.analizowane_fonemy = defaultdict(lambda: 0)
        self.analizowane_końcówki = defaultdict(lambda: 0)
        self.dbg = ["użyć"]

    def _zainicjalizuj_kombinacje(self):
        self.log.info("Inicjalizuję bazę generatora")
        for (tekst, kombinacje) in self.słownik.items():
            for kombinacja in kombinacje.keys():
                self.kombinacje[kombinacja] = Słowo(tekst)
        self.log.info("Baza zainicjalizowana w pamięci")

    def _dopasuj_akordy(self, słowo, akordy):
        if słowo.litery in self.dbg:
            self.log.info(f"Dopasowuje dla {słowo}, {akordy}")
        akordy_dodane = []
        for akord in akordy:
            if isinstance(akord, list):
                znaki = ""
                dł_ciągu = len(akord)
                for i in range(dł_ciągu):
                    znaki +=f"{akord[i]}"
                    if i < dł_ciągu -1:
                        znaki +="/"
                niedopasowanie = akord[-1].niedopasowanie
            else:
                niedopasowanie = akord.niedopasowanie
                znaki = f"{akord}"
            if słowo.litery in self.dbg:
                self.log.info(f"Niedo dla {akord}, {niedopasowanie}")

            obecny_właściciel = None

            if znaki not in self.kombinacje.keys():
                if słowo.litery in self.dbg:
                    self.log.info(f"Nie ma, dodaje")
                self.kombinacje[znaki] = słowo
                self.słownik[słowo.litery][znaki] = niedopasowanie
                if słowo.litery in self.dbg:
                    self.log.info(f"Po dodaniu: {self.słownik[słowo.litery]}, {self.kombinacje[znaki]}")

                akordy_dodane.append(akord)
            else:
                if słowo.litery in self.dbg:
                    self.log.info(f"{znaki} już jest w słowniku")
                obecny_właściciel = self.kombinacje[znaki].litery
                if obecny_właściciel == słowo.litery:
                    akordy_dodane.append(akord)
                    continue
                kombinacje_właściciela = self.słownik[obecny_właściciel]
                ilość_kombinacji_właściciela = len(kombinacje_właściciela.keys())
                if ilość_kombinacji_właściciela <= self.minimum_kombinacji_per_słowo:
                    continue
                else:
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
                        kombinacje_właściciela.pop(znaki)
                        self.słownik[słowo.litery][znaki] = niedopasowanie
                        self.kombinacje[znaki] = słowo
                        akordy_dodane.append(akord)
        return akordy_dodane
                
    def wygeneruj_akordy(self, słowo,
                         limit_niedopasowania,
                         limit_prób=2,
                         bez_środka=False,
                         z_przedrostkiem=False,
                         z_gwiazdką=False):
        # if słowo in self.dbg:
        self.log.debug(f"Szukam dla: {słowo}")
        self.postęp += 1

        # Dla 'w', 'z'
        try:
            sylaby = self.sylaby_słowa[słowo]
        except KeyError as e:
            if słowo.isnumeric():
                return []
            if len(słowo) == 1:
                sylaby = [słowo]
            else:
                sylaby = self.język.sylabizuj(słowo)
                # raise KeyError(f"Nie znam sylab, {e}")
        if z_przedrostkiem:
            akordy = []
            (przedrostek, sylaby) = self.znajdź_przedrostek_dla_sylab(sylaby)
            self.log.debug(f"Z przedrostkiem {przedrostek}")
            podsłowo = ''.join(sylaby)
            if podsłowo in self.słownik.keys():
                # self.log.debug(f"Z podsłowem {podsłowo}")
                akordy_podsłowa = self.akordy_dla_liter(podsłowo)
                # self.log.debug(f"Dostałem podakordy: {akordy_podsłowa}")
                for akord in akordy_podsłowa:
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
                # self.log.info(f"ako pod {podsłowo}: {akordy_podsłowa[0]}")
                # self.log.info(f"w słowniku: {self.słownik[podsłowo]}")
                # self.log.info(f"{podsłowo} ma akordy: {akordy_podsłowa}")
                # self.log.info(f"ako pod: {akordy_podsłowa} dla {słowo}({przedrostek}/{podsłowo})")
                if isinstance(akordy_podsłowa[0], list):
                    litery = ""
                    for podsłowo in akordy_podsłowa[0]:
                        litery += f"{podsłowo}/"
                    self.kombinacje[f"{litery[:-1]}"].ustaw_klejone()  # TODO: to można zrobić tylko raz
                else:
                    self.kombinacje[f"{akordy_podsłowa[0]}"].ustaw_klejone()  # TODO: to można zrobić tylko raz
                    
                # TODO uaktualnij obiekt Słowo dla podsłowo
            else:
                # self.log.debug(f"bez podsłowa")
                akordy = self.klawiatura.wygeneruj_akordy(słowo,
                                                        sylaby,
                                                        limit_niedopasowania,
                                                        limit_prób, bez_środka,
                                                        z_gwiazdką)
        else:
            self.log.debug(f"bez przedrostka")
            akordy = self.klawiatura.wygeneruj_akordy(słowo,
                                                      sylaby,
                                                      limit_niedopasowania,
                                                      limit_prób, bez_środka,
                                                      z_gwiazdką)
            if słowo in self.dbg:
                self.log.info(f"Bez przedrostka {słowo}: {akordy}")

        if z_przedrostkiem and przedrostek:
            nowe_akordy = []
            for wygenerowany_akord in akordy:
                akordy_przedrostka = self.akordy_dla_liter(przedrostek)
                ## TODO: przypadek gdy więcej kombinacji ma takie samo niedopasowanie
                ## wtedy jedna z tych kombinacji może zostać zabrana do innego słowa
                ile_przedrostkow_uwzględnić = min(self.minimum_kombinacji_per_słowo,\
                                                  len(akordy_przedrostka))
                for i in range(ile_przedrostkow_uwzględnić):
                    akord_przedrostka = akordy_przedrostka[i]
                    multi_akord = akord_przedrostka
                    if isinstance(akord_przedrostka, list):
                        if isinstance(wygenerowany_akord, list):
                            multi_akord += wygenerowany_akord
                        else:
                            multi_akord.append(wygenerowany_akord)
                    else:
                        if isinstance(wygenerowany_akord, list):
                            multi_akord = [multi_akord]
                            multi_akord += wygenerowany_akord
                        else:
                            multi_akord = [multi_akord, wygenerowany_akord]
                    nowe_akordy.append(multi_akord)
            return nowe_akordy
        if słowo in self.dbg:
            self.log.info(f"zwracam dla {słowo}: {akordy}")
        return akordy

    def dodaj_znaki_specjalne_do_akordów(self,
                                         akordy,
                                         limit_niedopasowania,
                                         limit_prób=2):
        nowe_kombinacje = []
        for akord in akordy:
            if isinstance(akord, list):
                niedopasowanie = akord[-1].niedopasowanie
            else:
                niedopasowanie = akord.niedopasowanie
            if niedopasowanie < limit_niedopasowania:
                # self.log.info(f"Dodaję po specjalne: {kombinacja}")
                nowe_pkomb = self.klawiatura.dodaj_znaki_specjalne_do_akordu(akord)
                nowe_kombinacje += nowe_pkomb
        return nowe_kombinacje

    def dodaj_akordy_do_słownika(self, słowo, akordy):
        if słowo.litery in self.dbg:
            self.log.debug(f"Dostałem akordy: {akordy}")
        dodane = []
        if not akordy:
            self.log.error(f"Brak akordów dla {słowo} ({akordy})")
            return dodane
        dodane = self._dopasuj_akordy(słowo, akordy)
        if słowo.jest_przedrostkiem and len(dodane) > 0:
            self.przedrostki.add(słowo.litery)
        return dodane

    # Ponieważ sortowanie może trochę zająć, warto zapisać co już mamy
    # w razie gdyby skończył się zapas RAMu
    def generuj_do_pliku(self):
        for (kombinacja, słowo) in self.kombinacje.items():
            # if tekst == "moc":
            #     self.log.info(f"generuje: {kombinacja}: {tekst}")

            yield f'"{kombinacja}": "{słowo}"'

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
        if sklejone_sylaby in self.przedrostki:
            najdłuższy_przedrostek = sklejone_sylaby
            indeks_pozostałych_sylab = 1
        for i in range(1, len(sylaby)):
            sklejone_sylaby += sylaby[i]
            if sklejone_sylaby in self.przedrostki:
                najdłuższy_przedrostek = sklejone_sylaby
                indeks_pozostałych_sylab = i + 1
        return (najdłuższy_przedrostek, sylaby[indeks_pozostałych_sylab:])

    def akordy_dla_liter(self, litery):
        akordy = []
        # self.log.info(f"jakie są: {self.słownik[litery]}")
        for (kombinacja, niedopasowanie) in self.słownik[litery].items():
            # TODO: a co jeśli mamy akord dwuczłonowy w słowniku?
            if slash in kombinacja:
                # self.log.debug(f"jest slash")
                podakordy = []
                for podkombinacja in kombinacja.split(slash):
                    podakordy.append(Akord(self.log, podkombinacja, 0))
                podakordy[-1].niedopasowanie = niedopasowanie
                akordy.append(podakordy)
            else:
                # self.log.debug(f"bez slasha")
                akordy.append(Akord(self.log, kombinacja, niedopasowanie))
        # self.log.info(f"jakie zwracam: {akordy}")
        return akordy
