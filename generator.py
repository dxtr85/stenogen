from klawiatura import Klawiatura, RękaLewa, RękaPrawa

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
    def __init__(self, log, klawiatura, konfiguracja, słownik_ostateczny, sylaby_słowa):
        self.log = log
        self.konfiguracja = konfiguracja
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
                
    def wygeneruj_kombinacje(self, słowo, limit_prób=2):
        self.postęp += 1

        # Dla 'w', 'z'
        try:
            sylaby = self.sylaby_słowa[słowo]
        except KeyError as e:
            if len(słowo) == 1:
                sylaby = [słowo]
            else:
                raise KeyError(f"Nie znam sylab, {e}")
        kombinacje = self.klawiatura.wygeneruj_kombinacje(sylaby, limit_prób)
        dodane = []
        if kombinacje:
            dodane = self._dopasuj_kombinacje(słowo, kombinacje)
        else:
            self.log.debug(f"Nie znalazłem kombinacji dla: {słowo}")
        nowe_kombinacje = []
        if len(dodane) == 0 and kombinacje:
            # if słowo == "nać":
            #     self.log.info(f"naci niet {kombinacje}")
            #  Możemy pokombinować z gwiazdkami
            #  Na razie logika minimalistyczna
            for kombinacja in kombinacje:
                nowe_podkombinacje = self.klawiatura.dodaj_znaki_specjalne_do_kombinacji(kombinacja)
                nowe_kombinacje += nowe_podkombinacje
                # if len(dodane) > 0:
                #     break
            if nowe_kombinacje:
                # if słowo == "nać":
                #     self.log.info(f"nowe dla nać: {nowe_podkombinacje}")
                dodane += self._dopasuj_kombinacje(słowo, nowe_kombinacje)
        self.klawiatura.zresetuj_klawisze()
        if self.postęp % self.loguj_postęp_co == 0:
            self.log.info(f"{self.postęp}: {słowo} - wygenerowano")
        if len(dodane) == 0:
            return False
        else:
            return True
        
    # Ponieważ sortowanie może trochę zająć, warto zapisać co już mamy
    # w razie gdyby skończył się zapas RAMu
    def generuj_do_pliku(self):
        for (kombinacja, tekst) in self.kombinacje.items():
            # if tekst == "moc":
            #     self.log.info(f"generuje: {kombinacja}: {tekst}")

            yield f'"{kombinacja}": "{tekst}"'


