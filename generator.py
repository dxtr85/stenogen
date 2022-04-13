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

    def _dopasuj_kombinacje(self, tekst, kombinacje):
        kombinacje_dodane = []
        for kombinacja in kombinacje:
            niedopasowanie = kombinacja[1]
            obecny_właściciel = None

            if kombinacja[0][0] not in self.kombinacje.keys():
                self.kombinacje[kombinacja[0][0]] = tekst
                self.słownik[tekst][kombinacja[0][0]] = niedopasowanie

                kombinacje_dodane.append(kombinacja)
            else:
                obecny_właściciel = self.kombinacje[kombinacja[0][0]]
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
                        self.kombinacje[kombinacja[0][0]] = tekst
                        kombinacje_dodane.append(kombinacja)
        return kombinacje_dodane
                
    def wygeneruj_akordy(self, słowo,
                         limit_niedopasowania,
                         limit_prób=2,
                         bez_środka=False,
                         z_gwiazdką=False):
        # self.log.debug(f"Szukam dla: {słowo}")
        self.postęp += 1

        # Dla 'w', 'z'
        try:
            sylaby = self.sylaby_słowa[słowo]
        except KeyError as e:
            if len(słowo) == 1:
                sylaby = [słowo]
            else:
                sylaby = self.język.sylabizuj(słowo)
                # raise KeyError(f"Nie znam sylab, {e}")
        akordy = self.klawiatura.wygeneruj_akordy(słowo,
                                                      sylaby,
                                                      limit_niedopasowania,
                                                      limit_prób, bez_środka,
                                                      z_gwiazdką)
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
        return dodane

    # Ponieważ sortowanie może trochę zająć, warto zapisać co już mamy
    # w razie gdyby skończył się zapas RAMu
    def generuj_do_pliku(self):
        for (kombinacja, tekst) in self.kombinacje.items():
            # if tekst == "moc":
            #     self.log.info(f"generuje: {kombinacja}: {tekst}")

            yield f'"{kombinacja}": "{tekst}"'

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
