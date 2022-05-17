from pomocnicy import SłownikDomyślny, dzielniki_dla_słowa_o_długości
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


class Klawiatura:
    def __init__(self, log, konfiguracja, język):
        self.log = log
        self.język = język
        self.konfiguracja = konfiguracja
        self.lewe_indeksy_klawiszy = konfiguracja.lewe_indeksy_klawiszy
        self.prawe_indeksy_klawiszy = konfiguracja.prawe_indeksy_klawiszy
        self.znaki_środka = konfiguracja.znaki_środka
        self.dostępne_id_kombinacji = 0
        self.kombinacje = {}
        self.ręka_lewa = RękaLewa(log, konfiguracja)
        wspólne_klawisze = self.ręka_lewa.zwróć_wspólne_klawisze()
        self.ręka_prawa = RękaPrawa(log, konfiguracja, wspólne_klawisze)
        self.rozdzielacz = SłownikDomyślny(lambda x: dzielniki_dla_słowa_o_długości(x))
        self.dbg = []#["mię", "kko"],["kra", "i", "na"]]

    def wygeneruj_słowa(self, słowo,
                        sylaby,
                        limit_niedopasowania,
                        limit_prób,
                        bez_środka=False,
                        z_gwiazdką=False):
        self.kombinacje = {}
        dzielniki_słowa = self.rozdzielacz[len(sylaby)]
        słowa = []
        # if sylaby in self.dbg:
        # self.log.debug(f"wygeneruj: {sylaby}")
        for gdzie_podzielić in dzielniki_słowa:
            if limit_prób <= 0:
                break
            limit_prób -= 1
            
            # self.log.debug(f"Dzielę {słowo} w {gdzie_podzielić}, limit: {limit_prób}")
            # (waga_słowa, id_środkowej_kombinacji)  = self.zbuduj_kombinacje_dla_sylab(sylaby, gdzie_podzielić, z_gwiazdką)
            waga_słowa  = self.zbuduj_kombinacje_dla_sylab(sylaby, gdzie_podzielić, z_gwiazdką)
            if sylaby in self.dbg:
                self.log.debug(f"waga słowa: {waga_słowa}")

            if not waga_słowa:
                #  Przypadek kiedy pierwsza sylaba zaczyna się od samogłoski
                #  a podział jest inny niż na pierwszej sylabie
                # self.log.info(f"{sylaby}/{gdzie_podzielić} - nic z tego")  # TODO
                continue
            # (id_środkowej_kombinacji,
            #  kombinacja_środkowa,
            #  waga_środka,
            #  waga_słowa) = kombinacje
            if sylaby in self.dbg:
                self.log.debug(f"po zbuduj: {sylaby} kombi:{self.kombinacje}")
                self.log.debug(f"Waga słowa: {waga_słowa}")
            if bez_środka:
                kombinacja_środkowa = ""
                waga_środka = 0
            if z_gwiazdką:  # TODO: Może to inaczej rozwiązać?
                waga_słowa += 1

            kombinacje_do_odjęcia_lewe = self.do_odjęcia_aby_uzyskać_ciąg_niemalejący(self.minimalne_indeksy_lewe)
            kombinacje_do_odjęcia_prawe = self.do_odjęcia_aby_uzyskać_ciąg_niemalejący(self.minimalne_indeksy_prawe)#, id_środkowej_kombinacji) ## TODO sprawdzić czy dla prawej działa

            akord = self.akord_bez_inwersji(kombinacje_do_odjęcia_lewe,
                                            kombinacje_do_odjęcia_prawe,
                                            waga_słowa)# + waga_środka)
            if sylaby in self.dbg:
                self.log.debug(f"bez inversji: {sylaby} ako:{akord} {akord.niedopasowanie}")
            # niedopasowanie = waga_słowa - waga_środka - waga_akordu
            # self.log.debug(f"Niedopasowanie: {niedopasowanie}")
            if akord.niedopasowanie < 0:
                self.log.error(f"Niedopasowanie dla {słowo}: {akord.niedopasowanie}")
                self.log.error(f"  waga słowa {waga_słowa}")
            elif akord.niedopasowanie <= limit_niedopasowania:
                if sylaby in self.dbg:
                    self.log.debug(f"jest ok: {sylaby} ako:{akord}")
                słowo = StenoSłowo(self.log, [akord])
                słowa.append(słowo)#, niedopasowanie))
            # self.log.debug(f"Bez inv: {słowa}")
            if limit_prób > 0:
                słowa += self.słowa_z_inwersją(kombinacje_do_odjęcia_lewe,
                                               kombinacje_do_odjęcia_prawe,
                                               waga_słowa,# + waga_środka,
                                               limit_niedopasowania,
                                               limit_prób)
            if sylaby in self.dbg:
                self.log.debug(f"z inversjią: {sylaby} ako:{słowa}")
            # self.log.debug(f"Z inv: {słowa}")
            self.zresetuj_klawiaturę()
        if sylaby in self.dbg:
            self.log.debug(f"{sylaby} zwracam: {słowa}")
        return słowa

    def akord_bez_inwersji(self, od_lewe, od_prawe, waga_słowa):
        # self.log.debug(f"W bez inw: {od_lewe}, {od_prawe}")
        # self.log.debug(f"kombi: {self.kombinacje}")
        # self.log.debug(f"waga na rękach: {self.ręka_lewa.waga()}, {self.ręka_prawa.waga()}")
        
        komb_lewe = []
        komb_prawe = []
        max_idx = len(self.kombinacje) - 1
        for idx_kombinacji in od_lewe:
            # if idx_kombinacji > max_idx:
            #     self.log.error(f"BIL Idx za duży: {idx_kombinacji}, dostępne komb: {self.kombinacje}")
            #     continue
            lewa_do_odj = self.kombinacje[idx_kombinacji]
            # self.log.debug(f"Odejmuję {lewa_do_odj}")
            # self.log.debug(f"1 {idx_kombinacji}")
            self.ręka_lewa.deaktywuj_kombinację(lewa_do_odj)
            komb_lewe.append(idx_kombinacji)
        for idx_kombinacji in od_prawe:
            # if idx_kombinacji > max_idx:
            #     self.log.error(f"BIP Idx za duży: {idx_kombinacji}, dostępne komb: {self.kombinacje}")
            #     continue
            prawa_do_odj = self.kombinacje[idx_kombinacji]
            # self.log.debug(f"Deaktywuję z prawej: {idx_kombinacji} {self.kombinacje} (wszystkie: {od_prawe})")
            # self.log.debug(f"2")
            self.ręka_prawa.deaktywuj_kombinację(prawa_do_odj)
            komb_prawe.append(idx_kombinacji)
        akord = self.połącz_ręce(waga_słowa) ## TODO: może waga_środka=0?
        # self.log.debug(f"Ko0 do aktywacji: {komb_lewe}")
        for idx_kombinacji in komb_lewe:
            lewa_do_dod = self.kombinacje[idx_kombinacji]
            self.ręka_lewa.aktywuj_kombinację(lewa_do_dod)
        for idx_kombinacji in komb_prawe:
            prawa_do_dod = self.kombinacje[idx_kombinacji]
            self.ręka_prawa.aktywuj_kombinację(prawa_do_dod)
        # self.log.debug(f"wyjście waga na rękach: {self.ręka_lewa.waga()}, {self.ręka_prawa.waga()}")
        # self.log.debug(f"wyjście akord: {akord}")
        return akord

    def słowa_z_inwersją(self, od_lewe, od_prawe,
                          waga_słowa,
                          limit_niedopasowania, limit_prób):
        # self.log.debug(f"z inw, prób: {limit_prób}")
        # self.log.debug(f"z inw, limit niedo: {limit_niedopasowania}")
        # self.log.debug(f"Z lewe do odj: {od_lewe}")
        # self.log.debug(f"Z prawe do odj: {od_prawe}")
        # self.log.debug(f"Z wszystkie: {self.kombinacje}")
        # self.log.debug(f"wag: {waga_słowa}")
        dł_lewe = len(od_lewe)
        dł_prawe = len(od_prawe)
        słowa = []
        wszystkie_lewe_odjęte = False
        wszystkie_prawe_odjęte = False
        następny_do_pominięcia_lewy = 0
        następny_do_pominięcia_prawy = 0

        max_idx = len(self.kombinacje) - 1
        # self.log.debug(f"Przed pętlą: {self.połącz_ręce(waga_słowa)}")
        while limit_prób > 0:
            komb_lewe = []
            komb_prawe = []
            # self.log.debug(f"z inw w pętli, limit: {limit_prób}")
            if not wszystkie_lewe_odjęte:
                # Odejmujemy wszystkie prawe aby prawa strona była niemalejąca
                for id in od_prawe:
                    # if id > max_idx:
                    #     self.log.error(f"ZIP Idx za duży: {id} (w {od_prawe}), dostępne: [0..{max_idx}]")
                    #     # self.log.debug(f"Kombos: {self.kombinacje}")
                    #     continue

                    prawa_do_odj = self.kombinacje[id]
                    # self.log.debug(f"3")
                    self.ręka_prawa.deaktywuj_kombinację(prawa_do_odj)
                    komb_prawe.append(prawa_do_odj)
                # A z lewej strony zostawiamy jedną malejącą kombinację, aby skorzystać z inwersji
                if następny_do_pominięcia_lewy >= dł_lewe:
                    # self.log.debug("Więcej lewych nie pomijam")
                    wszystkie_lewe_odjęte = True
                else:
                    for idx in range(dł_lewe):
                        if idx == następny_do_pominięcia_lewy:
                            # self.log.debug(f"kombo {idx} pomijam")
                            continue
                        # elif od_lewe[idx] > max_idx:
                        #     self.log.error(f"ZIL Idx za duży: {od_lewe[idx]} (w {od_lewe}), dostępne: {self.kombinacje}")
                        #     continue
                        lewa_do_odj = self.kombinacje[od_lewe[idx]]
                        # self.log.debug(f"Odejmuję {lewa_do_odj}")
                        # self.log.debug(f"4")
                        self.ręka_lewa.deaktywuj_kombinację(lewa_do_odj)
                        komb_lewe.append(lewa_do_odj)
                    akord = self.połącz_ręce(waga_słowa)
                    # self.log.debug(f"Akord: {akord}(waga: {waga_słowa}), niedo: {akord.niedopasowanie}")
                    if akord.niedopasowanie <= limit_niedopasowania:
                        # self.log.debug(f"Dodaję: {akord}")
                        słowo = StenoSłowo(self.log, [akord])
                        słowa.append(słowo)
                        # akordy.append(akord)#, waga_akordu))
                    # self.log.debug(f"KoMb do aktywacji: {komb_lewe}")
                    # Aktywujemy spowrotem kombinacje lewe
                    for komb in komb_lewe:
                        self.ręka_lewa.aktywuj_kombinację(komb)
                    następny_do_pominięcia_lewy += 1
                    limit_prób -= 1
                # Aktywujemy spowrotem kombinacje prawe
                for kombo in komb_prawe:
                    self.ręka_prawa.aktywuj_kombinację(kombo)
                if limit_prób <= 0:
                    break

            elif not wszystkie_prawe_odjęte:
                # A tu na odwrót: wywalamy wszystkie malejące lewe kombinacje
                # self.log.debug("i prawa")
                for id in od_lewe:
                    # if id > max_idx:
                    #     self.log.error(f"EZIL Index za duży: {id} (w {od_lewe}), dostępne: {self.kombinacje}")
                    #     continue

                    lewa_do_odj = self.kombinacje[id]
                    # self.log.debug(f"5 {lewa_do_odj} id: {id}")
                    self.ręka_lewa.deaktywuj_kombinację(lewa_do_odj)
                    komb_lewe.append(lewa_do_odj)
                # I z drugiej strony usuwamy wszystkie kombinacje oprócz jednej
                # w każdej iteracji innej kombinacji
                if następny_do_pominięcia_prawy >= dł_prawe:
                    wszystkie_prawe_odjęte = True
                else:
                    for idx in range(dł_prawe):
                        if idx == następny_do_pominięcia_prawy:
                            continue
                        # elif od_prawe[idx] > max_idx:
                        #     self.log.error(f"EZIP Idx za duży: {od_prawe[idx]} (w {od_prawe}),dostępne: {self.kombinacje}")
                        #     continue
                        prawa_do_odj = self.kombinacje[od_prawe[idx]]
                        # self.log.debug(f"6")
                        self.ręka_prawa.deaktywuj_kombinację(prawa_do_odj)
                        komb_prawe.append(prawa_do_odj)
                    akord = self.połącz_ręce(waga_słowa)
                    # waga_akordu = self.ręka_lewa.waga() + self.ręka_prawa.waga()
                    # niedopasowanie = waga_słowa - waga_środka - waga_akordu
                    if akord.niedopasowanie <= limit_niedopasowania:
                        # self.log.debug(f"Dodaję: {akord}")
                        słowo = StenoSłowo(self.log, [akord])
                        słowa.append(słowo)
                        # akordy.append(akord)
                    for kombo in komb_prawe:
                        self.ręka_prawa.aktywuj_kombinację(kombo)
                    następny_do_pominięcia_prawy += 1
                    limit_prób -= 1
                # self.log.debug(f"Ko do aktywacji: {komb_lewe}")
                for kombo in komb_lewe:
                    self.ręka_lewa.aktywuj_kombinację(kombo)
                if limit_prób <= 0:
                    break
            else:
                break
        return słowa

    # TODO obsługa 'z_gwiazdką'
    def zbuduj_kombinacje_dla_sylab(self, sylaby, gdzie_podzielić, z_gwiazdką):
        (sylaby_lewe,
        sylaba_środkowa,
        sylaby_prawe) = self.podziel_sylaby_na_strony(sylaby,
                                                      gdzie_podzielić)
        if sylaby in self.dbg:
            self.log.debug(f"zbuduj: {sylaby}")
        # if len(sylaby_lewe) > 0 and sylaby_lewe[0][0] in self.język.samogłoski:
        #     if sylaby in self.dbg:
        #         self.log.debug(f"??? {sylaby}")
        #     return None
            
        # self.log.info(f"Podzielone: {sylaby_lewe} {sylaba_środkowa} {sylaby_prawe}")
        kombinacje_lewe = []
        kombinacja_środkowa = ""
        kombinacje_prawe = []
        dostępne_id_kombinacji = 0
        (fonemy_lewe_orig,
         śródgłos_orig,
         fonemy_prawe_orig,
         waga_słowa,
         waga_środka) = self.język.rozbij_sylaby_na_fonemy(sylaby_lewe,
                                                    sylaba_środkowa,
                                                    sylaby_prawe)
        if sylaby in self.dbg:
            self.log.debug(f"{sylaby} ({waga_słowa} {waga_środka}): L:{fonemy_lewe_orig}|Ś:{śródgłos_orig}|P:{fonemy_prawe_orig}")
        pierwsza = True
        ostatnia = False
        długość_lewych = len(fonemy_lewe_orig)
        for i in range(długość_lewych):
            fonem = fonemy_lewe_orig[i]
            # if i == długość_lewych -1:
            #     ostatnia = True
            znaki = self.klawisze_dla_fonemu(fonem)
            if sylaby in self.dbg:
                self.log.debug(f"{sylaby} lewe: {znaki} id: {dostępne_id_kombinacji}")
            kombinacja = self.ręka_lewa.zbuduj_kombinację(dostępne_id_kombinacji,
                                                            znaki,
                                                            pierwsza,
                                                            ostatnia)
            pierwsza = False
            kombinacje_lewe.append(kombinacja)
            dostępne_id_kombinacji += 1
            if sylaby in self.dbg and kombinacja:
                self.log.debug(f"{sylaby}: klaw L: {kombinacja.klawisze.keys()}")

        # id_środkowej_kombinacji = None # len(kombinacje_lewe) - 1  # Workaround na pusty środek
        for fonem in śródgłos_orig:
            # znaki = self.język.fonemy_samogłoskowe[fonem[0]][0]
            # for znak in znaki:
            #     if znak not in kombinacja_środkowa:
            #         kombinacja_środkowa += znak
            # id_środkowej_kombinacji = None
            if sylaby in self.dbg:
                self.log.debug(f"Trzepiemy środek dla fonemu: {fonem}")
            znaki = self.klawisze_dla_fonemu(fonem)
            dodana_prawa = True
            dodana_lewa = self.ręka_lewa.zbuduj_kombinację(dostępne_id_kombinacji,
                                                                   znaki,
                                                                   pierwsza=False,
                                                                   ostatnia=True,
                                                                   testuj=True)
            if sylaby in self.dbg:
                    self.log.debug(f"dod lewa: {dodana_lewa}")
            if not dodana_lewa:
                if sylaby in self.dbg:
                    self.log.debug(f"Z lewej nie poszło")
                dodana_prawa = self.ręka_prawa.zbuduj_kombinację(dostępne_id_kombinacji,
                                                                       znaki,
                                                                       pierwsza=True,
                                                                       ostatnia=False,
                                                                       testuj=True)
                if not dodana_prawa:
                    if sylaby in self.dbg:
                        self.log.debug(f"Z prawej też nie poszło")
                    self.log.error(f"Nie dodałem kombinacji dla {znaki}")
                else:
                    dostępne_id_kombinacji += 1
                    # id_środkowej_kombinacji = dostępne_id_kombinacji - 1
                    kombinacje_prawe.append(dodana_prawa)
                    if sylaby in self.dbg:
                        self.log.debug(f"dod prawa: {dodana_prawa}")
            else:
                dostępne_id_kombinacji += 1
                # id_środkowej_kombinacji = dostępne_id_kombinacji
                dodana_prawa = False
                kombinacje_lewe.append(dodana_lewa)
        # if not id_środkowej_kombinacji:
        #     self.log.debug(f"Nie ma jeszcze id środka?!")
        #     id_środkowej_kombinacji = dostępne_id_kombinacji
        if sylaby in self.dbg:
            self.log.debug(f"{sylaby}: {kombinacje_lewe} {kombinacje_prawe}")
        pierwsza = False
        ostatnia = False
        długość_prawych = len(fonemy_prawe_orig)
        for i in range(długość_prawych):
            fonem = fonemy_prawe_orig[i]
            if i == długość_prawych -1:
                ostatnia = True
            znaki = self.klawisze_dla_fonemu(fonem, prawe=True)
            if sylaby in self.dbg:
                self.log.debug(f"{sylaby} prawe: {znaki} id: {dostępne_id_kombinacji}(ost: {ostatnia})")
            kombinacja = self.ręka_prawa.zbuduj_kombinację(dostępne_id_kombinacji,
                                                           znaki,
                                                           pierwsza,
                                                           ostatnia)
            # pierwsza = False
            kombinacje_prawe.append(kombinacja)
            dostępne_id_kombinacji += 1
            if sylaby in self.dbg and kombinacja:
                self.log.debug(f"{sylaby}: klaw P: {kombinacja.klawisze.keys()}")
        if z_gwiazdką:
            # self.log.info(f"z_gwiazdką")
            dodanie_gwiazdki_możliwe = self.ręka_lewa.dodanie_gwiazdki_możliwe() or\
              self.ręka_prawa.dodanie_gwiazdki_możliwe()
            kombinacja_gwiazdki = None
            if dodanie_gwiazdki_możliwe:
                # self.log.info(f"można dodać gwiazdkę")
                kombinacja_gwiazdki = self.ręka_lewa.dodaj_gwiazdkę(dostępne_id_kombinacji)
                # self.log.info(f"lewa: {kombinacja_gwiazdki}")
                if kombinacja_gwiazdki:
                    # self.log.info(f"dodaję lewą")
                    kombinacje_lewe.append(kombinacja_gwiazdki)
                else:
                    # self.log.info(f"może prawa")
                    kombinacja_gwiazdki = self.ręka_prawa.dodaj_gwiazdkę(dostępne_id_kombinacji)
                    # self.log.info(f"prawa: {kombinacja_gwiazdki}")
                    if kombinacja_gwiazdki:
                        # self.log.info(f"dodaję prawą")
                        kombinacje_prawe.append(kombinacja_gwiazdki)
                    else:
                        self.log.error(f"Nie udało się dodać gwiazdki")
        for kombinacja in kombinacje_lewe + kombinacje_prawe:
            self.kombinacje[kombinacja.id_kombinacji] = kombinacja
        # for kombinacja in kombinacje_prawe:
        #     self.ręka_prawa.aktywuj_kombinację(kombinacja)
        # self.kombinacje = kombinacje_lewe + kombinacje_prawe
        if sylaby in self.dbg:
                self.log.debug(f"{sylaby} kombinacje: {self.kombinacje}")
                self.log.debug(f"lewe: {kombinacje_lewe}")
                self.log.debug(f"prawe: {kombinacje_prawe}")
        self.minimalne_indeksy_lewe = self.minimalne_indeksy_kombinacji(kombinacje_lewe)
        self.minimalne_indeksy_prawe = self.minimalne_indeksy_kombinacji(kombinacje_prawe)
        # self.log.debug(f"min lewe: {self.minimalne_indeksy_lewe}")
        # self.log.debug(f"min prawe: {self.minimalne_indeksy_prawe}")
        # return (waga_słowa, id_środkowej_kombinacji)
        return waga_słowa
                
    def minimalne_indeksy_kombinacji(self, kombinacje):
        minimalne = []
        for kombinacja in kombinacje:
            # self.log.debug(f"minimalne dla: {kombinacja}")
            minimalne.append((kombinacja.minimalny_indeks, kombinacja.id_kombinacji))
        return minimalne

    def podziel_sylaby_na_strony(self, sylaby, gdzie_podzielić=-2):
        ilość_sylab = len(sylaby)
        if ilość_sylab == 1:
            return self.podziel_sylabę_na_strony(sylaby[0])
        if gdzie_podzielić < 0:
            gdzie_podzielić = ilość_sylab + gdzie_podzielić
            if gdzie_podzielić < 0:
                gdzie_podzielić = 0
        if gdzie_podzielić > ilość_sylab -1:
            gdzie_podzielić = ilość_sylab -1
        sylaby_lewe = []
        sylaby_prawe = []
        if ilość_sylab == 1:
            return (sylaby_lewe, sylaby[0], sylaby_prawe)
        else:
            for i in range(gdzie_podzielić):
                sylaby_lewe.append(sylaby[i])
            if gdzie_podzielić == ilość_sylab - 1:
                sylaby_prawe = []
            else:
                sylaby_prawe = sylaby[gdzie_podzielić + 1:]
            return (sylaby_lewe,
                    sylaby[gdzie_podzielić],
                    sylaby_prawe)

    def podziel_sylabę_na_strony(self, sylaba):
         #and sylaby[0][-1] in self.język.samogłoski
        (nagłos, śródgłos, wygłos) = self.język.fonemy_sylaby[sylaba]
        środek = ""
        for fonem in śródgłos:
            środek += fonem
        śródgłos = środek
        if wygłos:
            return (nagłos, śródgłos, wygłos)
        if nagłos:
            (lewa, prawa) = self.rozbij_nagłos_na_strony(nagłos)
            return ([], lewa, [prawa + śródgłos])
        return ([], śródgłos, [])

    def rozbij_nagłos_na_strony(self, nagłos):
        lewa = nagłos[0]
        prawa = ""
        ile_fonemów = len(nagłos)
        if ile_fonemów == 1:
            return (nagłos[0], "")
        elif ile_fonemów == 2:
            return (nagłos[0], nagłos[1])
        elif ile_fonemów == 3:
            return (nagłos[0] + nagłos[1],  nagłos[2])
        elif ile_fonemów == 4:
            return (nagłos[0] + nagłos[1],  nagłos[2] + nagłos[3])
        else:
            self.log.debug(f"Forfiter, qwa: {nagłos}")
            lewa = nagłos[0]
            for i in range(1, int(ile_fonemów/2)+1):
                lewa += nagłos[i]
            prawa = ""
            for i in range(int(ile_fonemów/2)+1, ile_fonemów):
                prawa += nagłos[i]
            return (lewa, prawa)
        
    def klawisze_dla_fonemu(self, fonem, prawe=False):
        fonem = fonem[0]
        if prawe:
            if fonem in self.język.samogłoski:
                return self.język.fonemy_samogłoskowe[fonem][1]
            return self.język.fonemy_spółgłoskowe[fonem][1]           
        else:
            if fonem in self.język.samogłoski:
                # return nic
                return self.język.fonemy_samogłoskowe[fonem][0]
            return self.język.fonemy_spółgłoskowe[fonem][0]

    def połącz_ręce(self, waga_słowa): #, ręka_lewa, kombinacja_środkowa, ręka_prawa):
        # self.log.debug(f"{waga_słowa}/{self.waga_na_klawiaturze()} łączę {self.kombinacje}")
        akord_lewy = self.ręka_lewa.akord_lewy()
        # akord_środkowy = Akord(self.log, kombinacja_środkowa) #, len(kombinacja_środkowa))  ## TODO waga środka
        # (środek_l, środek_p) = self.środek.akordy_środka()
        akord_prawy = self.ręka_prawa.akord_prawy()
        # self.log.info(f"Łączę: {akord_lewy}({akord_lewy.jest_tylda}) + {akord_prawy} ({akord_prawy.jest_tylda})")
        połączony_akord = akord_lewy + akord_prawy
        # self.log.info(f"Łączę LS+P: {połączony_akord} + {akord_prawy}")
        # wyjściowy_akord = połączony_akord + akord_prawy
        # self.log.debug(f"na klawie: {self.waga_na_klawiaturze()}")
        połączony_akord.niedopasowanie = waga_słowa - self.waga_na_klawiaturze()# - len(kombinacja_środkowa)
        return połączony_akord
        
        # tylda_lewa = tylda in akord_lewy.tekst
        # tylda_prawa = tylda in akord_prawy.tekst
        # gwiazdka_lewa = gwiazdka in akord_lewy.tekst
        # gwiazdka_prawa = gwiazdka in akord_prawy.tekst
        # ptyldogwiazdka = nic
        # ręka_lewa_znaki = akord_lewy.tekst
        # ręka_prawa_znaki = akord_prawy.tekst
        # if tylda_lewa or tylda_prawa:
        #     ręka_lewa_znaki = ręka_lewa_znaki.replace(tylda, nic)
        #     ręka_prawa_znaki = ręka_prawa_znaki.replace(tylda, nic)
        #     kombinacja_środkowa = kombinacja_środkowa.replace(tylda, nic)
        #     ptyldogwiazdka = tylda

        # if gwiazdka_lewa or gwiazdka_prawa:
        #     ręka_lewa_znaki = ręka_lewa_znaki.replace(gwiazdka, nic)
        #     ręka_prawa_znaki = ręka_prawa_znaki.replace(gwiazdka, nic)
        #     kombinacja_środkowa = kombinacja_środkowa.replace(gwiazdka, nic)
        #     ptyldogwiazdka += gwiazdka
        # if len(ptyldogwiazdka) == 0:
        #     ptyldogwiazdka = myślnik  # TODO jest więcej przypadków gdzie myślnik można ominąć
        # kombinacja_środkowa += ptyldogwiazdka
        # wynik = nic
        # for znak in self.znaki_środka:
        #     if znak in kombinacja_środkowa:
        #         wynik += znak
        # if wynik == nic and not ręka_lewa_znaki.endswith(jot):
        #     wynik = myślnik

        # return (ręka_lewa_znaki + wynik + ręka_prawa_znaki,
        #         (ręka_lewa[1], ręka_prawa[1]),  # dodanie tyldy możliwe
        #         (ręka_lewa[2], ręka_prawa[2]),  # dodanie gwiazdki możliwe
        #         (ręka_lewa[3], ręka_prawa[3]))  # dodanie tyldogwiazdki możliwe

        
    def waga_na_klawiaturze(self):
        # self.log.info(f"L:{self.ręka_lewa.waga()} P:{self.ręka_prawa.waga()}")
        return self.ręka_lewa.waga() + self.ręka_prawa.waga()

    def do_odjęcia_aby_uzyskać_ciąg_niemalejący(self, ciąg, dodaj_do_indeksów=0):
        # self.log.debug(f"Sprawdzam: {ciąg}")
        # z_inwersją = False
        do_odjęcia = []
        # odjęto = 0
        (niemalejący, (co_odjąć, id_komb)) = self.ciąg_niemalejący(ciąg)
        while not niemalejący:
            do_odjęcia.append(id_komb)# + dodaj_do_indeksów)
            ciąg = ciąg[:co_odjąć] + ciąg[co_odjąć + 1:]
            (niemalejący, (co_odjąć, id_komb)) = self.ciąg_niemalejący(ciąg)
            # odjęto += 1
        # self.log.debug(f"Zwracam: {do_odjęcia}")
        return do_odjęcia
        
    def ciąg_niemalejący(self, ciąg):
        # self.log.debug(f"sprawdzam: {ciąg}")
        długość_ciągu = len(ciąg)
        if długość_ciągu < 2:
            return (True, (None, None))
        else:
            for i in range(1, długość_ciągu):
                if ciąg[i][0] < ciąg[i-1][0]:
                    return (False, (i, ciąg[i][1]))
        return (True, (None, None))

    def dodaj_znaki_specjalne_do_słowa(self, słowo):
        # TODO: obsługa ciągów akordów
        # self.log.debug(f"Próbuję dodać znaki dla {akord} ({akord.dodanie_tyldy[0]}, {akord.dodanie_gwiazdki[0]}, {akord.dodanie_tyldogwiazdki[0]})")
        # ciąg = False
        # if isinstance(akord, list):
        #     ciąg = akord[:-1]
        #     akord = akord[-1]
        akord = słowo.ostatni_akord()
        nowe_akordy = []
        # TODO: obsługa drugich booli
        if akord.dodanie_tyldy[0]:
            nowy_akord = akord.kopia()
            nowy_akord.jest_tylda = True
            nowe_akordy.append(nowy_akord)
        if akord.dodanie_gwiazdki[0]:
            nowy_akord = akord.kopia()
            nowy_akord.jest_gwiazdka = True
            nowe_akordy.append(nowy_akord)
        if akord.dodanie_tyldogwiazdki[0]:
            nowy_akord = akord.kopia()
            nowy_akord.jest_tylda = True
            nowy_akord.jest_gwiazdka = True
            nowe_akordy.append(nowy_akord)

        nowe_słowa = słowo.kombinuj_bez_ostatniego_akordu(nowe_akordy)
        # if not ciąg:
        #     # self.log.debug(f"koniec prób 1: {nowe_akordy}")
        #     return nowe_akordy
        # nowe_ciągi = []
        # for akord in nowe_akordy:
        #     nowy_ciąg = []
        #     for istniejący_akord in ciąg:
        #         nowy_ciąg.append(istniejący_akord)
        #     nowy_ciąg.append(akord)
        #     # self.log.debug(f"Dorzucam {akord} do {ciąg}): {nowy_ciąg}")
        #     nowe_ciągi.append(nowy_ciąg)
        # self.log.debug(f"Koniec prób 2: {nowe_słowa}")
        return nowe_słowa

    def zresetuj_klawiaturę(self):
        self.ręka_lewa.zresetuj_rękę()
        self.ręka_prawa.zresetuj_rękę()
        self.minimalne_indeksy_lewe = []
        self.minimalne_indeksy_prawe = []
        self.kombinacje = {}
        # self.środek.zresetuj_kciuki()

class Klawisz:
    def __init__(self, log, znak, indeks, kombinacja_id=None,
                 waga=1, samodzielny=0,
                 początkowy=False, końcowy=False,
                 ile_palców_może_aktywować=1):
        self.log = log
        self.znak = znak
        self.waga = waga
        self.indeks = indeks
        self.kombinacje = SłownikDomyślny(lambda x: 0)
        if kombinacja_id:
            self.kombinacje[kombinacja_id] = 1
        self.początkowy = początkowy
        self.końcowy = końcowy
        self.samodzielny = samodzielny
        self.ile_palców_może_aktywować = ile_palców_może_aktywować
        self.ile_palców_obecnie_może_aktywować = ile_palców_może_aktywować
        self.już_zważone = False

    def __repr__(self):
        return f"({self.znak} ({self.waga}-{'P' if self.początkowy else ''}{'K' if self.końcowy else ''}{'S' if self.samodzielny else ''})"

    def zresetuj(self):
        self.waga = 0
        self.początkowy = False
        self.końcowy = False
        self.samodzielny = 0
        self.kombinacje = SłownikDomyślny(lambda x: 0)
        self.ile_palców_obecnie_może_aktywować = self.ile_palców_może_aktywować
        self.już_zważone = False

    def zważ(self):
        if self.ile_palców_może_aktywować > 1:
            if self.już_zważone:
                self.już_zważone = False
                return 0
            else:
                self.już_zważone = True
                return self.waga
        return self.waga

    def zważ_nieinwazyjnie(self):
        return self.waga

    def aktualizuj(self, kombinacja):
        self.kombinacje[kombinacja.id_kombinacji] += 1
        samodzielny = 0
        if kombinacja.długość_kombinacji == 1:
            samodzielny = 1
        self.samodzielny += samodzielny
        if kombinacja.początkowa:
            self.początkowy = True
        if kombinacja.końcowa:
            self.końcowy = True
        self.waga += kombinacja.waga

    def aktywuj(self, kombinacja):
        id_komb = kombinacja.id_kombinacji
        self.kombinacje[id_komb] += 1
        samodzielny = 0
        if kombinacja.długość_kombinacji == 1:
            samodzielny = 1
        self.samodzielny += samodzielny
        if kombinacja.początkowa:
            self.początkowy = True
        if kombinacja.końcowa:
            self.końcowy = True
        self.waga += kombinacja.waga

    def deaktywuj(self, kombinacja):
        id_komb = kombinacja.id_kombinacji
        if self.kombinacje[id_komb] <= 0:
            self.log.error(f"Nie mogę deaktywować kombinacji {id_komb} dla {self.znak}(k: {self.kombinacje})")
            return
        else:
            self.kombinacje[id_komb] -= 1
        samodzielny = 0
        if kombinacja.długość_kombinacji == 1:
            samodzielny = -1
        self.samodzielny += samodzielny
        if kombinacja.początkowa:
            self.początkowy = False
        if kombinacja.końcowa:
            self.końcowy = False
        if self.waga > 0:
            self.waga -= kombinacja.waga
        else:
            self.log.error(f"Za mała waga do deaktywacji: {self.waga}")

    def musi_zostać(self):
        return self.początkowy or self.końcowy


class RękaLewa:
    def __init__(self, log, konfiguracja):
        self.log = log
        self.indeksy = konfiguracja.lewe_indeksy_klawiszy
        self.palec_mały = Palec(log, konfiguracja.palce_lewe[0])
        self.palec_serdeczny = Palec(log, konfiguracja.palce_lewe[1])
        self.palec_środkowy = Palec(log, konfiguracja.palce_lewe[2])
        self.palec_wskazujący = Palec(log, konfiguracja.palce_lewe[3], ma_wspólne_klawisze=True)
        self.kciuk_lewy = Palec(log, konfiguracja.palce_lewe[4], ma_wspólne_klawisze=True, jest_kciukiem=True)
        self.kombinacje = {}  # Można tylko dodawać elementy do kombinacji, żeby IDki się zgadzały!!!

    def zwróć_wspólne_klawisze(self):
        wspólne_klawisze = self.palec_wskazujący.zwróć_wspólne_klawisze()
        wspólne_klawisze += self.kciuk_lewy.zwróć_wspólne_klawisze()
        return wspólne_klawisze

    def zresetuj_rękę(self):
        self.kombinacje = {}
        for palec in [self.palec_mały,
                      self.palec_serdeczny,
                      self.palec_środkowy,
                      self.palec_wskazujący,
                      self.kciuk_lewy]:
            for klawisz in palec.klawisze.values():
                klawisz.zresetuj()

    def waga(self):
        waga = 0
        for palec in [self.palec_mały, self.palec_serdeczny, self.palec_środkowy,
                      self.palec_wskazujący, self.kciuk_lewy]:
            # self.log.info(f"Lewy Palec: {palec.waga()}")
            waga += palec.waga()
        
        return waga

    def palec_dla_klawisza(self, klawisz):
        indeks = klawisz.indeks
        znak = klawisz.znak
        if indeks in [0, 1]:
            return self.palec_mały
        elif indeks == 2:
            return self.palec_serdeczny
        elif indeks == 3:
            if znak in self.palec_środkowy.obsługiwane_klawisze:
                return self.palec_środkowy
            return self.kciuk_lewy
        elif indeks in [4, 5]:
            if znak in self.palec_wskazujący.obsługiwane_klawisze:
                return self.palec_wskazujący
            return self.kciuk_lewy
        elif indeks == 6:
            return self.kciuk_lewy
        else:
            self.log.debug(f"Lewa ręka nie ma palca dla indeksu: {znak} {indeks}")

    def zbuduj_kombinację(self, id_kombinacji, znaki, pierwsza=False, ostatnia=False, testuj=False):
        if testuj and not all([znak in self.indeksy for znak in znaki]):
            # self.log.debug(f"Kombinacja nie wspierana: {znaki} dla Lewej Ręki")
            return None
        # if testuj:
        #     self.log.debug(f"Kombinacja wspierana: {znaki} dla Lewej Ręki")
        kombinacja = Kombinacja(self.log,
                                self.indeksy,
                                id_kombinacji,
                                znaki,
                                waga=1,
                                pierwsza_kombinacja=pierwsza,
                                ostatnia_kombinacja=ostatnia)
        self.dodaj_kombinację(kombinacja)
        return kombinacja

    def dodaj_kombinację(self, kombinacja):
        self.kombinacje[kombinacja.id_kombinacji] = True  # Czy jest aktywna
        for klawisz in kombinacja.zwróć_klawisze():
            palec = self.palec_dla_klawisza(klawisz)
            if klawisz.znak not in palec.wspierane_kombinacje:
                self.log.error(f"Nie mogę dodać klawisza {klawisz.znak} {klawisz.indeks} {palec.wspierane_kombinacje}")
            else:
                # self.log.info(f"Dodaje {klawisz.znak} dla {kombinacja.id_kombinacji}")
                palec.dodaj_klawisz(klawisz, kombinacja)

    def dodaj_gwiazdkę(self, id_kombinacji):
        return self.zbuduj_kombinację(id_kombinacji,
                                      znaki='*',
                                      pierwsza=False,
                                      ostatnia=True)

    def dodanie_gwiazdki_możliwe(self):
        return not self.palec_wskazujący.dodanie_gwiazdki_możliwe()[0]

    def aktywuj_kombinację(self, kombinacja):
        id_komb = kombinacja.id_kombinacji
        if id_komb not in self.kombinacje.keys():
            self.log.error(f"RękaLewa nie ma kombinacji: {id_komb}")
            return
        elif self.kombinacje[id_komb]:
            self.log.error(f"RękaLewa komb. {id_komb} już aktywna.")
            return
        self.kombinacje[id_komb] = True

        for klawisz in kombinacja.zwróć_klawisze():
            palec = self.palec_dla_klawisza(klawisz)
            if not palec:
                self.log.debug(f"Nie znalazłem lewego palca dla {klawisz.znak} - nie mogę aktywować")
            elif klawisz.znak not in palec.wspierane_kombinacje:
                self.log.error(f"Nie mogę dodać klawisza {klawisz.znak} {klawisz.indeks}")
            else:
                palec.aktywuj_klawisz(klawisz, kombinacja)       
        
    def deaktywuj_kombinację(self, kombinacja):
        id_komb = kombinacja.id_kombinacji
        if id_komb not in self.kombinacje.keys():
            self.log.error(f"RękaLewa nie ma kombinacji: {id_komb}")
            return
        elif not self.kombinacje[id_komb]:
            self.log.error(f"RękaLewa komb. {id_komb} już nieaktywna.")
            return
        self.kombinacje[id_komb] = False

        for klawisz in kombinacja.zwróć_klawisze():
            palec = self.palec_dla_klawisza(klawisz)
            if not palec:
                ## Przy podziale na pierwszej sylabie gdy pierwsza litera to A - pierwsze A powinno zawsze zostać
                self.log.debug(f"Nie znalazłem lewego palca dla {klawisz.znak} - nie mogę deaktywować")
            elif klawisz.znak not in palec.wspierane_kombinacje:
                self.log.error(f"Nie mogę deaktywować klawisza {klawisz.znak} dla {palec.wspierane_kombinacje}")
            else:
                palec.deaktywuj_klawisz(klawisz, kombinacja)

    def akord_lewy(self):
        tekst = self.palec_mały.tekst()
        # waga =  self.palec_mały.waga()
        tekst += self.palec_serdeczny.tekst()
        # waga += self.palec_serdeczny.waga()
        tekst += self.palec_środkowy.tekst()
        # waga += self.palec_środkowy.waga()
        tekst += self.palec_wskazujący.tekst()
        # waga += self.palec_wskazujący.waga()
        tekst += self.kciuk_lewy.tekst()
        # waga += self.kciuk_lewy.waga()
        dodanie_tyldy = self.palec_wskazujący.dodanie_tyldy_możliwe()
        dodanie_gwiazdki = self.palec_wskazujący.dodanie_gwiazdki_możliwe()
        dodanie_tyldogwiazdki = self.palec_wskazujący.dodanie_tyldy_i_gwiazdki_możliwe()
        # self.log.debug(f"{tekst} T{dodanie_tyldy}, G{dodanie_gwiazdki}, TG{dodanie_tyldogwiazdki}")
        return Akord(self.log, tekst, 0, nic, dodanie_tyldy, dodanie_gwiazdki, dodanie_tyldogwiazdki)


class RękaPrawa:
    def __init__(self, log, konfiguracja, wspólne_klawisze):
        self.log = log
        self.indeksy = konfiguracja.prawe_indeksy_klawiszy
        self.kciuk_prawy = Palec(log,
                                 konfiguracja.palce_prawe[0],
                                 ma_wspólne_klawisze=True,
                                 wspólne_klawisze=wspólne_klawisze[2:],
                                 jest_kciukiem=True)  # nie wszystkie kombinacje dla kciuka dozwolone
        self.palec_wskazujący = Palec(log,
                                      konfiguracja.palce_prawe[1],
                                      ma_wspólne_klawisze=True,
                                      wspólne_klawisze=wspólne_klawisze[:2])
        self.palec_środkowy = Palec(log, konfiguracja.palce_prawe[2])
        self.palec_serdeczny = Palec(log, konfiguracja.palce_prawe[3])
        self.palec_mały = Palec(log, konfiguracja.palce_prawe[4])
        self.kombinacje = {}  # Można tylko dodawać elementy do kombinacji, żeby IDki się zgadzały!!!
        self.dostępne_id_kombinacji = 0

    def zresetuj_rękę(self):
        self.kombinacje = {}
        self.dostępne_id_kombinacji = 0
        for palec in [self.palec_mały,
                      self.palec_serdeczny,
                      self.palec_środkowy,
                      self.palec_wskazujący,
                      self.kciuk_prawy]:
            for klawisz in palec.klawisze.values():
                klawisz.zresetuj()

    def waga(self):
        waga = 0
        for palec in [self.palec_mały, self.palec_serdeczny, self.palec_środkowy,
                      self.palec_wskazujący, self.kciuk_prawy]:
            # self.log.info(f"Prawy palec: {palec.waga()}")
            waga += palec.waga()
        return waga

    def palec_dla_klawisza(self, klawisz):
        indeks = klawisz.indeks
        znak = klawisz.znak
        if indeks in [4, 5, 6]:
            if znak in self.palec_wskazujący.obsługiwane_klawisze:
                return self.palec_wskazujący
            return self.kciuk_prawy
        elif indeks == 7:
            if znak in self.palec_środkowy.obsługiwane_klawisze:
                return self.palec_środkowy
            return self.kciuk_prawy
        elif indeks == 8:
            return self.palec_serdeczny
        elif indeks in [9, 10]:
            return self.palec_mały
        else:
            self.log.error(f"Prawa ręka nie ma palca dla indeksu: {indeks}")

    def zbuduj_kombinację(self, id_kombinacji, znaki, pierwsza=False, ostatnia=False, testuj=False):
        if testuj and not all([znak in self.indeksy for znak in znaki]):
            # self.log.debug(f"Kombinacja nie wspierana: {znaki} dla Prawej Ręki")
            return None
        # if testuj:
        #     self.log.debug(f"Kombinacja wspierana: {znaki} dla Prawej Ręki")
        kombinacja = Kombinacja(self.log,
                                self.indeksy,
                                id_kombinacji,
                                znaki,
                                waga=1,
                                pierwsza_kombinacja=pierwsza,
                                ostatnia_kombinacja=ostatnia)
        self.dodaj_kombinację(kombinacja)
        return kombinacja

    def dodaj_kombinację(self, kombinacja):
        self.kombinacje[kombinacja.id_kombinacji] = True  # Czy jest aktywna
        for klawisz in kombinacja.zwróć_klawisze():
            palec = self.palec_dla_klawisza(klawisz)
            if klawisz.znak not in palec.wspierane_kombinacje:
                self.log.error(f"Nie mogę dodać klawisza {klawisz.znak} {klawisz.indeks}")
            else:
                # self.log.info(f"Dodaje {klawisz.znak} dla {kombinacja.id_kombinacji}")
                palec.dodaj_klawisz(klawisz, kombinacja)

    def dodaj_gwiazdkę(self, id_kombinacji):
        return self.zbuduj_kombinację(id_kombinacji,
                                      znaki='*',
                                      pierwsza=False,
                                      ostatnia=True)

    def dodanie_gwiazdki_możliwe(self):
        return not self.palec_wskazujący.dodanie_gwiazdki_możliwe()[0]

    def aktywuj_kombinację(self, kombinacja):
        id_komb = kombinacja.id_kombinacji
        if id_komb not in self.kombinacje.keys():
            self.log.error(f"RękaPrawa nie ma kombinacji: {id_komb}({self.kombinacje.keys()})")
            return
        elif self.kombinacje[id_komb]:
            self.log.error(f"RękaPrawa komb. {id_komb} już aktywna.")
            return
        self.kombinacje[id_komb] = True
            
        for klawisz in kombinacja.zwróć_klawisze():
            palec = self.palec_dla_klawisza(klawisz)
            if klawisz.znak not in palec.wspierane_kombinacje:
                self.log.error(f"Nie mogę dodać klawisza {klawisz.znak} {klawisz.indeks}")
            else:
                palec.aktywuj_klawisz(klawisz, kombinacja)       
        
    def deaktywuj_kombinację(self, kombinacja):
        # self.log.debug(f"Do deaktywacji: {kombinacja}")
        id_komb = kombinacja.id_kombinacji
        if id_komb not in self.kombinacje.keys():
            self.log.error(f"RękaPrawa nie ma kombinacji: {id_komb}({self.kombinacje.keys()})")
            return
        elif not self.kombinacje[id_komb]:
            self.log.error(f"RękaPrawa komb. {id_komb} już nieaktywna.")
            return
        self.kombinacje[id_komb] = False

        for klawisz in kombinacja.zwróć_klawisze():
            palec = self.palec_dla_klawisza(klawisz)
            if klawisz.znak not in palec.wspierane_kombinacje:
                self.log.error(f"Nie mogę deaktywować klawisza {klawisz.znak} dla {palec.wspierane_kombinacje}")
            else:
                palec.deaktywuj_klawisz(klawisz, kombinacja)

    def akord_prawy(self):
        tekst = self.kciuk_prawy.tekst()
        tekst += self.palec_wskazujący.tekst()
        # waga = self.palec_wskazujący.waga()
        tekst += self.palec_środkowy.tekst()
        # waga += self.palec_środkowy.waga()
        tekst += self.palec_serdeczny.tekst()
        # waga += self.palec_serdeczny.waga()
        tekst += self.palec_mały.tekst()
        # waga += self.palec_mały.waga()
        dodanie_tyldy = self.palec_wskazujący.dodanie_tyldy_możliwe()
        dodanie_gwiazdki = self.palec_wskazujący.dodanie_gwiazdki_możliwe()
        dodanie_tyldogwiazdki = self.palec_wskazujący.dodanie_tyldy_i_gwiazdki_możliwe()
        # self.log.debug(f"{tekst} T{dodanie_tyldy}, G{dodanie_gwiazdki}, TG{dodanie_tyldogwiazdki}")
        return Akord(self.log, nic, 0, tekst, dodanie_tyldy, dodanie_gwiazdki, dodanie_tyldogwiazdki)
        

class Palec:
    def __init__(self, log, obsługiwane_klawisze, ma_wspólne_klawisze=False, wspólne_klawisze=None, jest_kciukiem=False):
        self.log = log
        # self.log.debug(f"Tworzę palec dla {obsługiwane_klawisze}")
        self.ustaw_wspierane_kombinacje(obsługiwane_klawisze, jest_kciukiem)
        self.klawisze = {}
        self.ma_wspólne_klawisze = ma_wspólne_klawisze
        if ma_wspólne_klawisze:
            if wspólne_klawisze:
                for klawisz in wspólne_klawisze:
                    znak = klawisz.znak
                    if znak not in self.obsługiwane_klawisze:
                        self.log.error(f"{znak} nieobsługiwany ({self.obsługiwane_klawisze})")
                    else:
                        self.klawisze[znak] = klawisz
            else:
                ile_klawiszy_obsługuje = len(self.obsługiwane_klawisze)
                wspólne_klawisze = []
                if ile_klawiszy_obsługuje == 4:
                    if jest_kciukiem:
                        klawisz = Klawisz(self.log,
                                      self.obsługiwane_klawisze[2],
                                      indeks=5,
                                      waga=0,
                                      ile_palców_może_aktywować=2)
                        self.klawisze[klawisz.znak] = klawisz
                        klawisz = Klawisz(self.log,
                                      self.obsługiwane_klawisze[3],
                                      indeks=6,
                                      waga=0,
                                      ile_palców_może_aktywować=2)
                        self.klawisze[klawisz.znak] = klawisz
                    else:
                        klawisz = Klawisz(self.log,
                                      self.obsługiwane_klawisze[2],
                                      indeks=5,
                                      waga=0,
                                      ile_palców_może_aktywować=2)
                        self.klawisze[klawisz.znak] = klawisz
                        klawisz = Klawisz(self.log,
                                      self.obsługiwane_klawisze[3],
                                      indeks=5,
                                      waga=0,
                                      ile_palców_może_aktywować=2)
                        self.klawisze[klawisz.znak] = klawisz
                elif ile_klawiszy_obsługuje == 3:
                    klawisz = Klawisz(self.log,
                                      self.obsługiwane_klawisze[2],
                                      indeks=5,
                                      waga=0,
                                      ile_palców_może_aktywować=2)
                    self.klawisze[klawisz.znak] = klawisz

    def ustaw_wspierane_kombinacje(self, obsługiwane_klawisze, jest_kciukiem):
        ile_klawiszy = len(obsługiwane_klawisze)
        if ile_klawiszy == 2:
            self.wspierane_kombinacje = [nic,
                                        obsługiwane_klawisze[0],
                                        obsługiwane_klawisze[0]+obsługiwane_klawisze[1],
                                        obsługiwane_klawisze[1]]
        elif ile_klawiszy == 4:
            if not jest_kciukiem:
                self.wspierane_kombinacje = [nic,
                                            obsługiwane_klawisze[0],
                                            obsługiwane_klawisze[0]+obsługiwane_klawisze[1],
                                            obsługiwane_klawisze[0]+obsługiwane_klawisze[2],
                                            obsługiwane_klawisze[0]+obsługiwane_klawisze[1]+obsługiwane_klawisze[2]+obsługiwane_klawisze[3],
                                            obsługiwane_klawisze[1],
                                            obsługiwane_klawisze[1]+obsługiwane_klawisze[3],
                                            obsługiwane_klawisze[2],
                                            obsługiwane_klawisze[2]+obsługiwane_klawisze[3],
                                            obsługiwane_klawisze[3]]
            else:
                self.wspierane_kombinacje = [nic,
                                            obsługiwane_klawisze[0],
                                            obsługiwane_klawisze[0]+obsługiwane_klawisze[1],
                                            obsługiwane_klawisze[0]+obsługiwane_klawisze[1]+obsługiwane_klawisze[2],
                                            obsługiwane_klawisze[0]+obsługiwane_klawisze[1]+obsługiwane_klawisze[2]+obsługiwane_klawisze[3],
                                            obsługiwane_klawisze[1],
                                            obsługiwane_klawisze[1]+obsługiwane_klawisze[2],
                                            obsługiwane_klawisze[1]+obsługiwane_klawisze[2]+obsługiwane_klawisze[3],
                                            obsługiwane_klawisze[2],
                                            obsługiwane_klawisze[2]+obsługiwane_klawisze[3],
                                            obsługiwane_klawisze[3]]
                
        elif ile_klawiszy == 3:  # Kciuki
            if jest_kciukiem:
                self.wspierane_kombinacje = [nic,
                                            obsługiwane_klawisze[0],
                                            obsługiwane_klawisze[0]+obsługiwane_klawisze[1],
                                            obsługiwane_klawisze[0]+obsługiwane_klawisze[1]+obsługiwane_klawisze[2],
                                            # obsługiwane_klawisze[0]+obsługiwane_klawisze[2],  # Nie na każdej klawiaturze
                                            obsługiwane_klawisze[1],
                                            obsługiwane_klawisze[1]+obsługiwane_klawisze[2],
                                            obsługiwane_klawisze[2]]
            else:
                self.wspierane_kombinacje = [nic,
                                            obsługiwane_klawisze[0],
                                            obsługiwane_klawisze[0]+obsługiwane_klawisze[1],
                                            obsługiwane_klawisze[0]+obsługiwane_klawisze[1]+obsługiwane_klawisze[2],
                                            obsługiwane_klawisze[0]+obsługiwane_klawisze[2],
                                            obsługiwane_klawisze[1],
                                            obsługiwane_klawisze[1]+obsługiwane_klawisze[2],
                                            obsługiwane_klawisze[2]]
            # self.log.info(f"Wspierany trójpalec: {self.wspierane_kombinacje}")
        self.obsługiwane_klawisze = obsługiwane_klawisze

    def zwróć_wspólne_klawisze(self):
        # self.log.debug(f"Wołać tylko z ręki lewej!")
        if not self.ma_wspólne_klawisze:
            self.log.error(f"Nie mam wspólnych klawiszy")
            return []
        else:
            ile_klawiszy_obsługuje = len(self.obsługiwane_klawisze)
            wspólne_klawisze = []
            if ile_klawiszy_obsługuje == 4:
                wspólne_klawisze.append(self.klawisze[self.obsługiwane_klawisze[2]])
                wspólne_klawisze.append(self.klawisze[self.obsługiwane_klawisze[3]])
            elif ile_klawiszy_obsługuje == 3:
                wspólne_klawisze.append(self.klawisze[self.obsługiwane_klawisze[2]])
            # self.log.debug(f"Zwracam wspólne klawisze: {wspólne_klawisze}")
            return wspólne_klawisze

    def dodaj_klawisz(self, klawisz, kombinacja):
        if klawisz.znak not in self.obsługiwane_klawisze:
            self.log.error(f"{klawisz.znak} nieobsługiwany ({self.obsługiwane_klawisze})")
        elif klawisz.znak not in self.klawisze.keys():
            self.klawisze[klawisz.znak] = klawisz
        else:
            self.klawisze[klawisz.znak].aktualizuj(kombinacja)

    def aktywuj_klawisz(self, klawisz, kombinacja):
        if klawisz.znak not in self.obsługiwane_klawisze:
            self.log.error(f"{klawisz.znak} nieobsługiwany ({self.obsługiwane_klawisze}) A")
        elif klawisz.znak not in self.klawisze.keys():
            self.log.error(f"{klawisz.znak} niedodany, nie mogę aktywować")
        self.klawisze[klawisz.znak].aktywuj(kombinacja)

    def deaktywuj_klawisz(self, klawisz, kombinacja):
        if klawisz.znak not in self.obsługiwane_klawisze:
            self.log.error(f"{klawisz.znak} nieobsługiwany ({self.obsługiwane_klawisze}) D")
        elif klawisz.znak not in self.klawisze.keys():
            self.log.error(f"{klawisz.znak} niedodany, nie mogę deaktywować")
        self.klawisze[klawisz.znak].deaktywuj(kombinacja)

    def pierwszy_lub_ostatni_klawisz(self):
        for klawisz in self.klawisze.values():
            if klawisz.początkowy or klawisz.końcowy:
                return klawisz.znak
        return False

    def tekst(self):
        tekst = nic
        klucze = self.klawisze.keys()
        wagi = {}
        for znak in self.obsługiwane_klawisze:
            if znak in klucze:
                waga = self.klawisze[znak].zważ()
                wagi[znak] = waga
                if waga > 0:
                    tekst += znak
        if tekst in self.wspierane_kombinacje:
            return tekst
        # self.log.debug(f"'{tekst}' nie jest wspierany ({self.wspierane_kombinacje})")
        klawisz_do_deaktywacji = None
        klawisz_opuszczony = False
        for znak in self.obsługiwane_klawisze:
            if znak in klucze:
                klawisz = self.klawisze[znak]
                if wagi[znak] > 0:
                    klawisz_opuszczony = self.spróbuj_opuścić_klawisz(klawisz)
                    if klawisz_opuszczony:
                        klawisz_opuszczony.zważ()  # Potrzebne, żeby druga ręka wiedziała żeby go użyć!
                        return tekst.replace(znak, nic)
                if wagi[znak] > 0 and self.można_deaktywować(klawisz):
                # if not użyty_klawisz.musi_zostać() \
                #   and self.można_deaktywować(użyty_klawisz):
                    if not klawisz_do_deaktywacji:
                        klawisz_do_deaktywacji = klawisz
                    elif wagi[klawisz_do_deaktywacji.znak] > wagi[znak]:
                        klawisz_do_deaktywacji = klawisz

        if not klawisz_do_deaktywacji:
            if ii in tekst:
                # self.log.debug(f"Opuszczam zmiękczenie '{ii}'")
                return tekst.replace(ii, nic)
            ## Lepsza metoda zamiast dorzucania tyldy/gwiazdki to dokładać modyfikator do istniejącej kombinacji
            self.log.debug(f"{tekst}: Nie wiem jaki klawisz deaktywować: {[k.znak for k in self.klawisze.values() if k.waga>0]}")
            return tekst  # To się nie powinno zdarzyć
        else:
            # klawisz_do_deaktywacji.waga = 0 # Kombinacje stają się niekompletne! (OK?)
            nowy_tekst = tekst.replace(klawisz_do_deaktywacji.znak, nic)
            # self.log.debug(f"{tekst} zmieniłem na: {nowy_tekst}")
            return nowy_tekst

    def spróbuj_opuścić_klawisz(self, klawisz):
        # self.log.debug(f"Próbuję opuścić {klawisz.znak} ({klawisz.ile_palców_może_aktywować}, {klawisz.ile_palców_obecnie_może_aktywować})")
        if klawisz.ile_palców_może_aktywować > 1 and klawisz.ile_palców_obecnie_może_aktywować > 1:
            klawisz.ile_palców_obecnie_może_aktywować -= 1
            # self.log.debug(f"Opuszczam {klawisz.znak}")
            return klawisz
        return False

    def można_deaktywować(self, usuwany_klawisz):
        if usuwany_klawisz.początkowy or usuwany_klawisz.końcowy:
            return False
        tekst = ""
        for znak in self.obsługiwane_klawisze:
            if znak in self.klawisze.keys() and self.klawisze[znak].waga > 0:
                tekst += znak
        tekst = tekst.replace(usuwany_klawisz.znak, nic)
        return tekst in self.wspierane_kombinacje
        
    def waga(self):
        waga = 0
        for klawisz in self.klawisze.values():
            waga += klawisz.zważ()
        return waga

    def dodanie_tyldy_możliwe(self):
        if tylda not in self.obsługiwane_klawisze:
            return (False, False)
        klucze = self.klawisze.keys()
        użyte_klucze = []
        wagi = {}
        idx_tyldy = self.obsługiwane_klawisze.index(tylda)
        przy_tyldzie = self.obsługiwane_klawisze[idx_tyldy - 2]
        użytych_klawiszy = 0
        for znak in self.obsługiwane_klawisze:
            if znak in klucze:
                waga = self.klawisze[znak].waga
                if waga > 0:
                    użyte_klucze.append(znak)
                    użytych_klawiszy += 1
                wagi[znak] = waga
        if tylda in użyte_klucze:
            return (False, False)
        elif użytych_klawiszy == 3:
            return (True, True)  # gwiazdka wspierana, wtedy wszystkie klawisze palca aktywne
        elif użytych_klawiszy == 1\
             and przy_tyldzie in klucze:
            # self.log.debug(f"{przy_tyldzie} tylko aktywny - tylda wchodzi")
            return (True, False)
        elif użytych_klawiszy == 0:
            return (True, False)
        return (False, False)

    def dodanie_gwiazdki_możliwe(self):
        if gwiazdka not in self.obsługiwane_klawisze:
            return (False, False)
        klucze = self.klawisze.keys()
        użyte_klucze = []
        wagi = {}
        idx_gwiazdki = self.obsługiwane_klawisze.index(gwiazdka)
        przy_gwiazdce = self.obsługiwane_klawisze[idx_gwiazdki - 2]
        użytych_klawiszy = 0
        for znak in self.obsługiwane_klawisze:
            if znak in klucze:
                waga = self.klawisze[znak].waga
                if waga > 0:
                    użyte_klucze.append(znak)
                    użytych_klawiszy += 1
                wagi[znak] = waga
        if gwiazdka in użyte_klucze:
            return (False, False)
        elif użytych_klawiszy == 3:
            return (True, True)  # gwiazdka wspierana, wtedy wszystkie klawisze palca aktywne
        elif użytych_klawiszy == 1\
             and przy_gwiazdce in klucze:
            # self.log.debug(f"{przy_gwiazdce} tylko aktywny - gwiazdka wchodzi")
            return (True, False)
        elif użytych_klawiszy == 0:
            return (True, False)
        return (False, False)

    def dodanie_tyldy_i_gwiazdki_możliwe(self):
        if tylda not in self.obsługiwane_klawisze or\
          gwiazdka not in self.obsługiwane_klawisze:
            return (False, False)
        klucze = self.klawisze.keys()
        wagi = {}
        użytych_klawiszy = 0
        for znak in self.obsługiwane_klawisze:
            if znak in klucze:
                waga = self.klawisze[znak].waga
                if waga > 0:
                    użytych_klawiszy += 1
                wagi[znak] = waga
        if gwiazdka in klucze and wagi[gwiazdka] > 0:
            return (False, False)
        if tylda in klucze and wagi[tylda] > 0:
            return (False, False)
        if użytych_klawiszy == 2:
            return (True, True)
        elif użytych_klawiszy == 0:
            return (True, False)
        return (False, False)


class Kombinacja:
    def __init__(self,
                 log,
                 indeksy,
                 id_kombinacji,
                 znaki,
                 waga=1,
                 pierwsza_kombinacja=False,
                 ostatnia_kombinacja=False):
        self.log = log
        self.minimalny_indeks = 10
        self.id_kombinacji = id_kombinacji
        self.klawisze = dict()
        self.waga = waga
        self.długość_kombinacji = len(znaki)
        self.początkowa = pierwsza_kombinacja
        self.końcowa = ostatnia_kombinacja
        for znak in znaki:
            indeks = indeksy[znak]
            if indeks < self.minimalny_indeks:
                self.minimalny_indeks = indeks
            samodzielny = 0
            if self.długość_kombinacji == 1:
                samodzielny = 1
            self.klawisze[znak] = Klawisz(log,
                                          znak,
                                          indeks,
                                          id_kombinacji,
                                          waga,
                                          samodzielny,
                                          pierwsza_kombinacja,
                                          ostatnia_kombinacja)
    def zwróć_klawisze(self):
        for klawisz in self.klawisze.values():
            yield klawisz

    def __repr__(self):
        return f"<{self.id_kombinacji}:{[klawisz for klawisz in self.klawisze.values()]}>\n"
            

class Akord:
    def __init__(self,
                 log,
                 tekst_lewy,
                 niedopasowanie = 0,
                 tekst_prawy = "",
                 dodanie_tyldy = (False, False),
                 dodanie_gwiazdki = (False, False),
                 dodanie_tyldogwiazdki = (False, False)):
        self.log = log
        self.niedopasowanie = niedopasowanie
        self.dodanie_tyldy = dodanie_tyldy
        self.dodanie_gwiazdki = dodanie_gwiazdki
        self.dodanie_tyldogwiazdki = dodanie_tyldogwiazdki
        tekst_łączony = f"{tekst_lewy}{tekst_prawy}"
        # self.log.debug(f"tlewy: {tekst_lewy}, tprawy: {tekst_prawy}")
        self.jest_tylda = tylda in tekst_łączony   # TODO dla dwuczłonowych akordów z przedrostkiem
        self.jest_gwiazdka = gwiazdka in tekst_łączony #tekst_lewy or gwiazdka in tekst_prawy  # TODO j.w.
        self.jest_jot = jot in tekst_łączony #tekst_lewy or jot in tekst_prawy
        self.jest_ee = ee in tekst_łączony #tekst_lewy or ee in tekst_prawy
        self.jest_ii = ii in tekst_łączony #tekst_lewy or ii in tekst_prawy
        self.jest_aa = aa in tekst_łączony #tekst_lewy or aa in tekst_prawy
        self.jest_uu = uu in tekst_łączony #tekst_lewy or uu in tekst_prawy
        if tekst_prawy == "":
            (tekst_lewy, tekst_prawy) = self.tekst_na_pół(f"{tekst_lewy}")
            # self.log.debug(f"Podzielony: {tekst_lewy} {tekst_prawy}")
        if self.jest_tylda:
            tekst_lewy = tekst_lewy.replace(tylda, nic)
            tekst_prawy = tekst_prawy.replace(tylda, nic)
        if self.jest_gwiazdka:
            tekst_lewy = tekst_lewy.replace(gwiazdka, nic)
            tekst_prawy = tekst_prawy.replace(gwiazdka, nic)
        if self.jest_jot:
            tekst_lewy = tekst_lewy.replace(jot, nic)
            tekst_prawy = tekst_prawy.replace(jot, nic)
        if self.jest_ee:
            tekst_lewy = tekst_lewy.replace(ee, nic)
            tekst_prawy = tekst_prawy.replace(ee, nic)
        if self.jest_ii:
            tekst_lewy = tekst_lewy.replace(ii, nic)
            tekst_prawy = tekst_prawy.replace(ii, nic)
        if self.jest_aa:
            tekst_lewy = tekst_lewy.replace(aa, nic)
            tekst_prawy = tekst_prawy.replace(aa, nic)
        if self.jest_uu:
            tekst_lewy = tekst_lewy.replace(uu, nic)
            tekst_prawy = tekst_prawy.replace(uu, nic)

        self.tekst_lewy = tekst_lewy
        self.tekst_prawy = tekst_prawy
        # self.log.debug(f"Akord: {self}")

    # def __truediv__(self, akord):
    #     return Akord(f"{self}{slash}{akord}",
    #                  self.waga + akord.waga,
    #                  tekst_prawy=nic,
    #                  akord.dodanie_tyldy,
    #                  akord.dodanie_gwiazdki,
    #                  akord.dodanie_tyldogwiazdki)

    def kopia(self):
        kopia = Akord(self.log,
                      self.tekst_lewy,
                      self.niedopasowanie,
                      self.tekst_prawy,
                      self.dodanie_tyldy,
                      self.dodanie_gwiazdki,
                      self.dodanie_tyldogwiazdki)
        kopia.jest_tylda = self.jest_tylda
        kopia.jest_gwiazdka = self.jest_gwiazdka
        kopia.jest_jot = self.jest_jot
        kopia.jest_ee = self.jest_ee
        kopia.jest_ii = self.jest_ii
        kopia.jest_aa = self.jest_aa
        kopia.jest_uu = self.jest_uu
        return kopia

    def __add__(self, akord):
        # self.log.info(f"Dodaję {self} + {akord}")
        if slash in f"{self}{akord}":
            self.log.error(f"Nie mogę połączyć multiakordu ({self} {akord})")
            return Akord(self.log, "", 999)
        jest_jot = self.jest_jot
        if akord.jest_jot:
            jest_jot = True
        jest_ee = self.jest_ee
        if akord.jest_ee:
            jest_ee = True
            
        jest_tylda = self.jest_tylda
        if akord.jest_tylda:
            jest_tylda = True
        dodanie_tyldy = (False, False)
        if not jest_tylda:
            if self.dodanie_tyldy[0]:
                dodanie_tyldy = self.dodanie_tyldy
            elif akord.dodanie_tyldy[0]:
                dodanie_tyldy = akord.dodanie_tyldy

        jest_gwiazdka = self.jest_gwiazdka
        if akord.jest_gwiazdka:
            jest_gwiazdka = True
        dodanie_gwiazdki = (False, False)
        if not jest_gwiazdka:
            if self.dodanie_gwiazdki[0]:
                dodanie_gwiazdki = self.dodanie_gwiazdki
            elif akord.dodanie_gwiazdki[0]:
                dodanie_gwiazdki = akord.dodanie_gwiazdki

        dodanie_tyldogwiazdki = (False, False)
        if not jest_gwiazdka and not jest_tylda:
            if self.dodanie_tyldogwiazdki[0]:
                dodanie_tyldogwiazdki = self.dodanie_tyldogwiazdki
            elif akord.dodanie_tyldogwiazdki[0]:
                dodanie_tyldogwiazdki = akord.dodanie_tyldogwiazdki

        jest_ii = self.jest_ii
        if akord.jest_ii:
            jest_ii = True
        jest_aa = self.jest_aa
        if akord.jest_aa:
            jest_aa = True
        jest_uu = self.jest_uu
        if akord.jest_uu:
            jest_uu = True
        # self.log.info(f"nowy lewy: {self.tekst_lewy}+{akord.tekst_lewy}")
        tekst_lewy = self.l_tekst() + akord.l_tekst()
        # self.log.info(f"nowy prawy: {self.tekst_prawy}+{akord.tekst_prawy}")
        tekst_prawy = self.p_tekst() + akord.p_tekst()
        wyjściowy = Akord(self.log,
                          tekst_lewy,
                          self.niedopasowanie + akord.niedopasowanie,
                          tekst_prawy,
                          dodanie_tyldy,
                          dodanie_gwiazdki,
                          dodanie_tyldogwiazdki)
        wyjściowy.jest_jot = jest_jot
        wyjściowy.jest_ee = jest_ee
        wyjściowy.jest_tylda = jest_tylda
        wyjściowy.jest_gwiazdka = jest_gwiazdka
        wyjściowy.jest_ii = jest_ii
        wyjściowy.jest_aa = jest_aa
        wyjściowy.jest_uu = jest_uu
        return wyjściowy

    def tekst_na_pół(self, tekst):
        # self.log.info(f"DZielę na pół: {tekst}")
        if self.jest_tylda:
            return (tekst.split(tylda))
        elif self.jest_gwiazdka:
            return (tekst.split(gwiazdka))
        elif self.jest_jot:
            return (tekst.split(jot))
        elif self.jest_ee:
            return (tekst.split(ee))
        elif self.jest_ii:
            return (tekst.split(ii))
        elif self.jest_aa:
            return (tekst.split(aa))
        elif self.jest_uu:
            return (tekst.split(uu))
        return (tekst, "")
        
    def l_tekst(self):
        return f"{self.tekst_lewy}{jot if self.jest_jot else nic}{ee if self.jest_ee else nic}{tylda if self.jest_tylda else nic}{gwiazdka if self.jest_gwiazdka else nic}"

    def p_tekst(self):
        return f"{ii if self.jest_ii else nic}{aa if self.jest_aa else nic}{uu if self.jest_uu else nic}{self.tekst_prawy}"

    def __repr__(self):
        myślnik_wymagany = True
        if self.jest_tylda or self.jest_gwiazdka or self.jest_jot or self.jest_ee or self.jest_ii or self.jest_aa or self.jest_uu:
            myślnik_wymagany = False
        l_tekst = self.l_tekst()
        p_tekst = self.p_tekst()
        if myślnik in l_tekst or myślnik in p_tekst:
            myślnik_wymagany = False            
        return f"{l_tekst}{myślnik if myślnik_wymagany else nic}{p_tekst}"


class StenoSłowo:
    def __init__(self, log, akordy):
        self.log = log
        self.akordy = akordy
        self.niedopasowanie = 0
        for akord in akordy:
            self.niedopasowanie += akord.niedopasowanie

    def __add__(self, akord):
        # self.log.info(f"Dodaję {akord} {type(akord)}")
        if isinstance(akord, Akord):
            self.akordy.append(akord)
            self.niedopasowanie += akord.niedopasowanie
            return self
        elif isinstance(akord, StenoSłowo):
            for ako in akord.akordy:
                self.akordy.append(ako)
            self.niedopasowanie += akord.niedopasowanie
            return self
        elif isinstance(akord, list):
            for ako in akord:
                self.akordy.append(ako)
                self.niedopasowanie += ako.niedopasowanie
            return self
        else:
            self.log.error(f"Nie wiem jak dodać: {akord} {type(akord)}")
            
    def __repr__(self):
        słowo = ""
        for akord in self.akordy:
            słowo += f"{akord}/"
        return słowo[:-1]

    def ostatni_akord(self):
        return self.akordy[-1]

    def kopia(self):
        nowe_akordy = []
        for akord in self.akordy:
            nowe_akordy.append(akord.kopia())
        kopia = StenoSłowo(self.log,
                           nowe_akordy)
        return kopia

    def kombinuj(self, słowa):
        nowe_słowa = []
        # self.log.info(f"Kombinuję: {słowa} {type(słowa[0])}")
        for słowo in słowa:
            kopia = self.kopia()
            # self.log.info(f"kopia: {kopia}")
            nowe_słowo = kopia + słowo
            # self.log.info(f"nowe: {nowe_słowo}")
            nowe_słowa.append(nowe_słowo)
        return nowe_słowa

    def kombinuj_bez_ostatniego_akordu(self, słowa):
        if not słowa:
            return []
        if len(self.akordy) == 1:
            nowe_stenosłowa = []
            for słowo in słowa:
                nowe_stenosłowo = StenoSłowo(self.log, [słowo])
                nowe_stenosłowa.append(nowe_stenosłowo)
            return nowe_stenosłowa
        kopia = self.kopia()
        kopia.niedopasowanie -= kopia.akordy[-1].niedopasowanie
        kopia.akordy = kopia.akordy[:-1]
        return kopia.kombinuj(słowa)
