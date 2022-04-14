from klawiatura import Klawiatura, RękaLewa, RękaPrawa
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
dwa_falsy = (False, False)

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
        self.minimum_kombinacji_per_słowo = 2
        self.niepowodzenia = []
        self.analizowane_fonemy = defaultdict(lambda: 0)
        self.analizowane_końcówki = defaultdict(lambda: 0)

    def _zainicjalizuj_kombinacje(self):
        self.log.info("Inicjalizuję bazę generatora")
        for (tekst, kombinacje) in self.słownik.items():
            for kombinacja in kombinacje.keys():
                self.kombinacje[kombinacja] = tekst
        self.log.info("Baza zainicjalizowana w pamięci")

    def _dopasuj_kombinacje(self, słowo, kombinacje):
        tekst = słowo.litery
        kombinacje_dodane = []
        for kombinacja in kombinacje:
            niedopasowanie = kombinacja[1]
            obecny_właściciel = None

            if kombinacja[0][0] not in self.kombinacje.keys():
                self.kombinacje[kombinacja[0][0]] = słowo
                self.słownik[tekst][kombinacja[0][0]] = niedopasowanie

                kombinacje_dodane.append(kombinacja)
            else:
                obecny_właściciel = self.kombinacje[kombinacja[0][0]].litery
                if obecny_właściciel == tekst:
                    kombinacje_dodane.append(kombinacja)
                    continue
                kombinacje_właściciela = self.słownik[obecny_właściciel]
                ilość_kombinacji_właściciela = len(kombinacje_właściciela.keys())
                if ilość_kombinacji_właściciela <= self.minimum_kombinacji_per_słowo:
                    continue
                else:
                    obecne_niedopasowanie = kombinacje_właściciela[kombinacja[0][0]]
                    #  Nie zabieramy kombinacji jeśli ich dopasowanie jest takie samo
                    # if obecne_niedopasowanie <= niedopasowanie:
                    #     continue

                    minimalne_niedopasowanie_u_właściciela = obecne_niedopasowanie
                    for obca_kombinacja, obce_niedopasowanie in kombinacje_właściciela.items():
                        if obce_niedopasowanie < minimalne_niedopasowanie_u_właściciela:
                            minimalne_niedopasowanie_u_właściciela = obce_niedopasowanie
                            break
                        elif obce_niedopasowanie == minimalne_niedopasowanie_u_właściciela and\
                             obca_kombinacja != kombinacja[0][0]:
                            minimalne_niedopasowanie_u_właściciela = obce_niedopasowanie -1
                            break
                    if obecne_niedopasowanie > minimalne_niedopasowanie_u_właściciela:
                        kombinacje_właściciela.pop(kombinacja[0][0])
                        self.słownik[tekst][kombinacja[0][0]] = niedopasowanie
                        self.kombinacje[kombinacja[0][0]] = słowo
                        kombinacje_dodane.append(kombinacja)
        return kombinacje_dodane
                
    def wygeneruj_akordy(self, słowo,
                         limit_niedopasowania,
                         limit_prób=2,
                         bez_środka=False,
                         z_przedrostkiem=False,
                         z_gwiazdką=False):
        # self.log.debug(f"Szukam dla: {słowo}")
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
            (przedrostek, sylaby) = self.znajdź_przedrostek_dla_sylab(sylaby)
            podsłowo = ''.join(sylaby)
            if podsłowo in self.słownik.keys():
                akordy = []
                kombinacje = self.kombinacje_dla_liter(podsłowo)
                for (kombinacja, niedopasowanie) in kombinacje:
                    # self.log.info(f"AKtualizuję {kombinacja}")
                    akordy.append(((kombinacja, dwa_falsy, dwa_falsy, dwa_falsy), niedopasowanie))
                    słowo = self.kombinacje[kombinacja]
                    # if słowo.klejone:
                    #     self.log.info(f"Już klejone, niemaco")
                    słowo.ustaw_klejone()  # TODO: to można zrobić tylko raz
                    
                # TODO uaktualnij obiekt Słowo dla podsłowo
            else:
                akordy = self.klawiatura.wygeneruj_akordy(słowo,
                                                        sylaby,
                                                        limit_niedopasowania,
                                                        limit_prób, bez_środka,
                                                        z_gwiazdką)
        else:
            akordy = self.klawiatura.wygeneruj_akordy(słowo,
                                                      sylaby,
                                                      limit_niedopasowania,
                                                      limit_prób, bez_środka,
                                                      z_gwiazdką)

        if z_przedrostkiem and przedrostek:
            nowe_akordy = []
            for akord in akordy:
                kombinacje_przedrostka = self.kombinacje_dla_liter(przedrostek)
                ## TODO: przypadek gdy więcej kombinacji ma takie samo niedopasowanie
                ## wtedy jedna z tych kombinacji może zostać zabrana do innego słowa
                ile_przedrostkow_uwzględnić = min(self.minimum_kombinacji_per_słowo,\
                                                  len(kombinacje_przedrostka))
                for i in range(ile_przedrostkow_uwzględnić):
                    (kombinacja_przedrostka, niedopasowanie) = kombinacje_przedrostka[i]
                    (stara_kombinacja, t, g, tg)  = akord[0]
                    kombinacja_łączona = kombinacja_przedrostka + "/" + stara_kombinacja
                    self.log.debug(f"zamieniam {stara_kombinacja} na {kombinacja_łączona}")
                    nowy_akord = ((kombinacja_łączona, t, g, tg), akord[1] + niedopasowanie)
                    nowe_akordy.append(nowy_akord)
            return nowe_akordy
        return akordy

    def dodaj_znaki_specjalne_do_akordów(self,
                                         akordy,
                                         limit_niedopasowania,
                                         limit_prób=2):
        nowe_kombinacje = []
        for kombinacja in akordy:
            if kombinacja[1] < limit_niedopasowania:
                # self.log.debug(f"Dodaję po specjalne: {kombinacja}")
                nowe_pkomb = self.klawiatura.dodaj_znaki_specjalne_do_kombinacji(kombinacja)
                nowe_kombinacje += nowe_pkomb
        return nowe_kombinacje

    def dodaj_akordy_do_słownika(self, słowo, akordy):
        # self.log.debug(f"Dostałem akordy: {akordy}")
        dodane = []
        dodane = self._dopasuj_kombinacje(słowo, akordy)
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

    def kombinacje_dla_liter(self, litery):
        kombinacje = []
        # self.log.info(f"jakie są: {self.słownik[litery]}")
        for (kombinacja, niedopasowanie) in self.słownik[litery].items():
            kombinacje.append((kombinacja, niedopasowanie))
        return kombinacje
