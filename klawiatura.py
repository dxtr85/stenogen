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


class Klawiatura:
    def __init__(self, log, konfiguracja, język):
        self.log = log
        self.język = język
        self.konfiguracja = konfiguracja
        self.lewe_indeksy_klawiszy = konfiguracja.lewe_indeksy_klawiszy
        self.prawe_indeksy_klawiszy = konfiguracja.prawe_indeksy_klawiszy
        self.znaki_środka = konfiguracja.znaki_środka
        self.dostępne_id_kombinacji = 0
        self.kombinacje = []
        self.ręka_lewa = RękaLewa(log, konfiguracja)
        self.ręka_prawa = RękaPrawa(log, konfiguracja)
        # self.środek = Kciuki(log, konfiguracja)
        self.rozdzielacz = SłownikDomyślny(lambda x: dzielniki_dla_słowa_o_długości(x))

    def wygeneruj_akordy(self, słowo,
                         sylaby,
                         limit_niedopasowania,
                         limit_prób,
                         bez_środka=False,
                         z_gwiazdką=False):
        dzielniki_słowa = self.rozdzielacz[len(sylaby)]
        akordy = []
        for gdzie_podzielić in dzielniki_słowa:
            if limit_prób <= 0:
                break
            limit_prób -= 1
            
            # self.log.debug(f"Dzielę {słowo} w {gdzie_podzielić}, limit: {limit_prób}")
            kombinacje  = self.zbuduj_kombinacje_dla_sylab(sylaby, gdzie_podzielić, z_gwiazdką)
            if not kombinacje:
                #  Przypadek kiedy pierwsza sylaba zaczyna się od samogłoski
                #  a podział jest inny niż na pierwszej sylabie
                self.log.info(f"{sylaby}/{gdzie_podzielić} - nic z tego")
                continue
            (id_środkowej_kombinacji,
             kombinacja_środkowa,
             waga_środka,
             waga_słowa) = kombinacje
            # self.log.debug(f"Waga słowa: {waga_słowa}")
            if bez_środka:
                kombinacja_środkowa = ""
                waga_środka = 0
            if z_gwiazdką:  # TODO: Może to inaczej rozwiązać?
                waga_słowa += 1

            kombinacje_do_odjęcia_lewe = self.do_odjęcia_aby_uzyskać_ciąg_niemalejący(self.minimalne_indeksy_lewe)
            kombinacje_do_odjęcia_prawe = self.do_odjęcia_aby_uzyskać_ciąg_niemalejący(self.minimalne_indeksy_prawe, id_środkowej_kombinacji + 1)

            (akord, waga_akordu) = self.akord_bez_inwersji(kombinacje_do_odjęcia_lewe,
                                            kombinacja_środkowa,
                                            kombinacje_do_odjęcia_prawe)
            niedopasowanie = waga_słowa - waga_środka - waga_akordu
            # self.log.debug(f"Niedopasowanie: {niedopasowanie}")
            if niedopasowanie < 0:
                self.log.error(f"Niedopasowanie dla {słowo}: {niedopasowanie}")
                self.log.error(f"  waga słowa {waga_słowa}, waga środka: {waga_środka}")
                self.log.error(f"  waga akordu {waga_akordu}")
            elif niedopasowanie <= limit_niedopasowania:
                akordy.append((akord, niedopasowanie))
            # self.log.debug(f"Bez inv: {akordy}")
            if limit_prób > 0:
                akordy += self.akordy_z_inwersją(kombinacje_do_odjęcia_lewe,
                                                kombinacja_środkowa,
                                                kombinacje_do_odjęcia_prawe,
                                                waga_słowa,
                                                waga_środka,
                                                limit_niedopasowania,
                                                limit_prób)
            # self.log.debug(f"Z inv: {akordy}")
            self.zresetuj_klawiaturę()
        return akordy

    def akord_bez_inwersji(self, od_lewe, środek, od_prawe):
        komb_lewe = []
        komb_prawe = []
        max_idx = len(self.kombinacje) - 1
        for idx_kombinacji in od_lewe:
            if idx_kombinacji > max_idx:
                self.log.error(f"BIL Idx za duży: {idx_kombinacji}, dostępne komb: {self.kombinacje}")
                continue
            lewa_do_odj = self.kombinacje[idx_kombinacji]
            self.ręka_lewa.deaktywuj_kombinację(lewa_do_odj)
            komb_lewe.append(idx_kombinacji)
        for idx_kombinacji in od_prawe:
            if idx_kombinacji > max_idx:
                self.log.error(f"BIP Idx za duży: {idx_kombinacji}, dostępne komb: {self.kombinacje}")
                continue
            prawa_do_odj = self.kombinacje[idx_kombinacji]
            self.ręka_prawa.deaktywuj_kombinację(prawa_do_odj)
            komb_prawe.append(idx_kombinacji)
        akord = self.połącz_kombinacje(środek)
        waga = self.waga_na_klawiaturze()
        # self.log.debug(f"Ko0 do aktywacji: {komb_lewe}")
        for idx_kombinacji in komb_lewe:
            lewa_do_dod = self.kombinacje[idx_kombinacji]
            self.ręka_lewa.aktywuj_kombinację(lewa_do_dod)
        for idx_kombinacji in komb_prawe:
            prawa_do_dod = self.kombinacje[idx_kombinacji]
            self.ręka_prawa.aktywuj_kombinację(prawa_do_dod)
        return (akord, waga)

    def akordy_z_inwersją(self, od_lewe, środek, od_prawe,
                          waga_słowa, waga_środka,
                          limit_niedopasowania, limit_prób):
        # self.log.debug(f"z inw, limit: {limit_prób}")
        dł_lewe = len(od_lewe)
        dł_prawe = len(od_prawe)
        akordy = []
        wszystkie_lewe_odjęte = False
        wszystkie_prawe_odjęte = False
        następny_do_pominięcia_lewy = 0
        następny_do_pominięcia_prawy = 0

        max_idx = len(self.kombinacje) - 1
        while limit_prób > 0:
            komb_lewe = []
            komb_prawe = []
            # self.log.debug(f"z inw w pętli, limit: {limit_prób}")
            if not wszystkie_lewe_odjęte:
                # Odejmujemy wszystkie prawe aby prawa strona była niemalejąca
                for id in od_prawe:
                    if id > max_idx:
                        self.log.error(f"ZIP Idx za duży: {id} (w {od_prawe}), dostępne: [0..{max_idx}]")
                        self.log.debug(f"Kombos: {self.kombinacje}")
                        continue

                    prawa_do_odj = self.kombinacje[id]
                    self.ręka_prawa.deaktywuj_kombinację(prawa_do_odj)
                    komb_prawe.append(prawa_do_odj)
                # A z lewej strony zostawiamy jedną malejącą kombinację, aby skorzystać z inwersji
                if następny_do_pominięcia_lewy >= dł_lewe:
                    wszystkie_lewe_odjęte = True
                else:
                    for idx in range(dł_lewe):
                        if idx == następny_do_pominięcia_lewy:
                            continue
                        elif od_lewe[idx] > max_idx:
                            self.log.error(f"ZIL Idx za duży: {od_lewe[idx]} (w {od_lewe}), dostępne: {self.kombinacje}")
                            continue
                        lewa_do_odj = self.kombinacje[od_lewe[idx]]
                        self.ręka_lewa.deaktywuj_kombinację(lewa_do_odj)
                        komb_lewe.append(lewa_do_odj)
                    akord = self.połącz_kombinacje(środek)
                    waga_akordu = self.ręka_lewa.waga() + self.ręka_prawa.waga()
                    niedopasowanie = waga_słowa - waga_środka - waga_akordu
                    # self.log.debug(f"Akord: {akord}(waga: {waga_słowa}), niedo: {niedopasowanie}(waga ako: {waga_akordu})")
                    if niedopasowanie <= limit_niedopasowania:
                        # self.log.debug(f"Dodaję: {akord}")
                        akordy.append((akord, niedopasowanie))
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
                for id in od_lewe:
                    if id > max_idx:
                        self.log.error(f"EZIL Index za duży: {id} (w {od_lewe}), dostępne: {self.kombinacje}")
                        continue

                    lewa_do_odj = self.kombinacje[id]
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
                        elif od_prawe[idx] > max_idx:
                            self.log.error(f"EZIP Idx za duży: {od_prawe[idx]} (w {od_prawe}),dostępne: {self.kombinacje}")
                            continue
                        prawa_do_odj = self.kombinacje[od_prawe[idx]]
                        self.ręka_prawa.deaktywuj_kombinację(prawa_do_odj)
                        komb_prawe.append(prawa_do_odj)
                    akord = self.połącz_kombinacje(środek)
                    waga_akordu = self.ręka_lewa.waga() + self.ręka_prawa.waga()
                    niedopasowanie = waga_słowa - waga_środka - waga_akordu
                    if niedopasowanie <= limit_niedopasowania:
                        akordy.append((akord, niedopasowanie))
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
        return akordy
    # TODO obsługa 'z_gwiazdką'
    def zbuduj_kombinacje_dla_sylab(self, sylaby, gdzie_podzielić, z_gwiazdką):
        (sylaby_lewe,
        sylaba_środkowa,
        sylaby_prawe) = self.podziel_sylaby_na_strony(sylaby,
                                                      gdzie_podzielić)
        if len(sylaby_lewe) > 0 and sylaby_lewe[0][0] in self.język.samogłoski:
            return None
            
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
        dbg = []#["po", "sło", "wie"]]
        if sylaby in dbg:
            self.log.debug(f"{sylaby} ({waga_słowa} {waga_środka}): L:{fonemy_lewe_orig}|Ś:{śródgłos_orig}|P:{fonemy_prawe_orig}")
        pierwsza = True
        ostatnia = False
        długość_lewych = len(fonemy_lewe_orig)
        for i in range(długość_lewych):
            fonem = fonemy_lewe_orig[i]
            # if i == długość_lewych -1:
            #     ostatnia = True
            znaki = self.klawisze_dla_fonemu(fonem)
            if sylaby in dbg:
                self.log.debug(f"{sylaby} lewe: {znaki} id: {dostępne_id_kombinacji}")
            kombinacja = self.ręka_lewa.zbuduj_kombinację(dostępne_id_kombinacji,
                                                            znaki,
                                                            pierwsza,
                                                            ostatnia)
            pierwsza = False
            kombinacje_lewe.append(kombinacja)
            dostępne_id_kombinacji += 1
            if sylaby in dbg and kombinacja:
                self.log.debug(f"{sylaby}: klaw L: {kombinacja.klawisze.keys()}")

        id_środkowej_kombinacji = len(kombinacje_lewe) - 1  # Workaround na pusty środek
        for fonem in śródgłos_orig:
            znaki = self.język.fonemy_samogłoskowe[fonem[0]][0]
            for znak in znaki:
                if znak not in kombinacja_środkowa:
                    kombinacja_środkowa += znak
            id_środkowej_kombinacji = dostępne_id_kombinacji
            dostępne_id_kombinacji += 1
        if sylaby in dbg:
            self.log.debug(f"{sylaby}: środek: {kombinacja_środkowa}")
        pierwsza = False
        ostatnia = False
        długość_prawych = len(fonemy_prawe_orig)
        for i in range(długość_prawych):
            fonem = fonemy_prawe_orig[i]
            if i == długość_prawych -1:
                ostatnia = True
            znaki = self.klawisze_dla_fonemu(fonem, prawe=True)
            if sylaby in dbg:
                self.log.debug(f"{sylaby} prawe: {znaki} id: {dostępne_id_kombinacji}(ost: {ostatnia})")
            kombinacja = self.ręka_prawa.zbuduj_kombinację(dostępne_id_kombinacji,
                                                           znaki,
                                                           pierwsza,
                                                           ostatnia)
            # pierwsza = False
            kombinacje_prawe.append(kombinacja)
            dostępne_id_kombinacji += 1
            if sylaby in dbg and kombinacja:
                self.log.debug(f"{sylaby}: klaw P: {kombinacja.klawisze.keys()}")
        if z_gwiazdką:
            self.log.info(f"z_gwiazdką")
            dodanie_gwiazdki_możliwe = self.ręka_lewa.dodanie_gwiazdki_możliwe() or\
              self.ręka_prawa.dodanie_gwiazdki_możliwe()
            kombinacja_gwiazdki = None
            if dodanie_gwiazdki_możliwe:
                self.log.info(f"można dodać gwiazdkę")
                kombinacja_gwiazdki = self.ręka_lewa.dodaj_gwiazdkę(dostępne_id_kombinacji)
                self.log.info(f"lewa: {kombinacja_gwiazdki}")
                if kombinacja_gwiazdki:
                    self.log.info(f"dodaję lewą")
                    kombinacje_lewe.append(kombinacja_gwiazdki)
                else:
                    self.log.info(f"może prawa")
                    kombinacja_gwiazdki = self.ręka_prawa.dodaj_gwiazdkę(dostępne_id_kombinacji)
                    self.log.info(f"prawa: {kombinacja_gwiazdki}")
                    if kombinacja_gwiazdki:
                        self.log.info(f"dodaję prawą")
                        kombinacje_prawe.append(kombinacja_gwiazdki)
                    else:
                        self.log.error(f"Nie udało się dodać gwiazdki")

        self.kombinacje = kombinacje_lewe + [kombinacja_środkowa] + kombinacje_prawe
        if sylaby in dbg and kombinacja:
                self.log.debug(f"{sylaby}: kombinacje: {kombinacje_lewe} {kombinacja_środkowa} {kombinacje_prawe}")
        self.minimalne_indeksy_lewe = self.minimalne_indeksy_kombinacji(kombinacje_lewe)
        self.minimalne_indeksy_prawe = self.minimalne_indeksy_kombinacji(kombinacje_prawe)
        return (id_środkowej_kombinacji, kombinacja_środkowa, waga_środka, waga_słowa)

    def minimalne_indeksy_kombinacji(self, kombinacje):
        minimalne = []
        for kombinacja in kombinacje:
            minimalne.append(kombinacja.minimalny_indeks)
        return minimalne

    def podziel_sylaby_na_strony(self, sylaby, gdzie_podzielić=-2):
        ilość_sylab = len(sylaby)
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

    def klawisze_dla_fonemu(self, fonem, prawe=False):
        fonem = fonem[0]
        if prawe:
            if fonem in self.język.samogłoski:
                return self.język.fonemy_samogłoskowe[fonem][1]
            return self.język.fonemy_spółgłoskowe[fonem][1]           
        else:
            if fonem in self.język.samogłoski:
                return nic
            return self.język.fonemy_spółgłoskowe[fonem][0]

    def połącz_kombinacje(self, kombinacja_środkowa): #, ręka_lewa, kombinacja_środkowa, ręka_prawa):
        ręka_lewa = self.ręka_lewa.akord_lewy()
        # (środek_l, środek_p) = self.środek.akordy_środka()
        ręka_prawa = self.ręka_prawa.akord_prawy()
        tylda_lewa = tylda in ręka_lewa[0]
        tylda_prawa = tylda in ręka_prawa[0]
        gwiazdka_lewa = gwiazdka in ręka_lewa[0]
        gwiazdka_prawa = gwiazdka in ręka_prawa[0]
        ptyldogwiazdka = nic
        ręka_lewa_znaki = ręka_lewa[0]
        ręka_prawa_znaki = ręka_prawa[0]
        if tylda_lewa or tylda_prawa:
            ręka_lewa_znaki = ręka_lewa_znaki.replace(tylda, nic)
            ręka_prawa_znaki = ręka_prawa_znaki.replace(tylda, nic)
            kombinacja_środkowa = kombinacja_środkowa.replace(tylda, nic)
            ptyldogwiazdka = tylda

        if gwiazdka_lewa or gwiazdka_prawa:
            ręka_lewa_znaki = ręka_lewa_znaki.replace(gwiazdka, nic)
            ręka_prawa_znaki = ręka_prawa_znaki.replace(gwiazdka, nic)
            kombinacja_środkowa = kombinacja_środkowa.replace(gwiazdka, nic)
            ptyldogwiazdka += gwiazdka
        if len(ptyldogwiazdka) == 0:
            ptyldogwiazdka = myślnik  # TODO jest więcej przypadków gdzie myślnik można ominąć
        kombinacja_środkowa += ptyldogwiazdka
        wynik = nic
        for znak in self.znaki_środka:
            if znak in kombinacja_środkowa:
                wynik += znak
        if wynik == nic and not ręka_lewa_znaki.endswith(jot):
            wynik = myślnik

        return (ręka_lewa_znaki + wynik + ręka_prawa_znaki,
                (ręka_lewa[1], ręka_prawa[1]),  # dodanie tyldy możliwe
                (ręka_lewa[2], ręka_prawa[2]),  # dodanie gwiazdki możliwe
                (ręka_lewa[3], ręka_prawa[3]))  # dodanie tyldogwiazdki możliwe
    def waga_na_klawiaturze(self):
        # self.log.info(f"L:{self.ręka_lewa.waga()} P:{self.ręka_prawa.waga()}")
        return self.ręka_lewa.waga() + self.ręka_prawa.waga()

    def do_odjęcia_aby_uzyskać_ciąg_niemalejący(self, ciąg, dodaj_do_indeksów=0):
        # z_inwersją = False
        do_odjęcia = []
        odjęto = 0
        (niemalejący, co_odjąć) = self.ciąg_niemalejący(ciąg)
        while not niemalejący:
            do_odjęcia.append(odjęto + co_odjąć + dodaj_do_indeksów)
            ciąg = ciąg[:co_odjąć] + ciąg[co_odjąć + 1:]
            (niemalejący, co_odjąć) = self.ciąg_niemalejący(ciąg)
            odjęto += 1
        return do_odjęcia
        
    def ciąg_niemalejący(self, ciąg):
        długość_ciągu = len(ciąg)
        if długość_ciągu < 2:
            return (True, None)
        else:
            for i in range(1, długość_ciągu):
                if ciąg[i] < ciąg[i-1]:
                    return (False, i)
        return (True, None)

    def dodaj_znaki_specjalne_do_kombinacji(self, kombinacja):
        #   ( (dodanie_tyldy_z_lewej, czy_wszystkie_klawisze),
        #     (dodanie_tyldy_z_prawej, czy_wszystkie_klawisze) ),
        #   ( (dodanie_gwiazdki_z_lewej, czy_wszystkie_klawisze),
        #     (dodanie_gwiazdki_z_prawej, czy_wszystkie_klawisze) ),
        #   ( (dodanie_tyldogwiazdki_z_lewej, czy_wszystkie_klawisze),
        #     (dodanie_tyldogwiazdki_z_prawej, czy_wszystkie_klawisze) ) )
        nowe_kombinacje = []
        (kombo, niedopasowanie) = kombinacja
        #('TLE~GO', ((False, False), (False, False)), ((False, False), (False, False)), ((False, False), (True, False)))
        (znaki, ((l_tylda, lt_wszystko),(p_tylda, pt_wszystko)),
                ((l_gwiazdka, lg_wszystko), (p_gwiazdka, pg_wszystko)),
                ((l_tyldogwiazdka, ltg_wszystko), (p_tyldogwiazdka, ptg_wszystko))) = kombo
        tylda_już_jest = tylda in znaki
        gwiazdka_już_jest = gwiazdka in znaki
        if myślnik in znaki:
            znaki_lewe, znaki_prawe = znaki.split(myślnik)
        elif tylda in znaki:
            znaki_lewe, znaki_prawe = znaki.split(tylda)
            znaki_prawe = tylda + znaki_prawe
        elif gwiazdka in znaki:
            znaki_lewe, znaki_prawe = znaki.split(gwiazdka)
            znaki_prawe = gwiazdka + znaki_prawe
        elif jot in znaki:
            znaki_lewe, znaki_prawe = znaki.split(jot)
            znaki_lewe = znaki_lewe + jot
        elif ee in znaki:
            znaki_lewe, znaki_prawe = znaki.split(ee, 1)  # z 1., bo te znaki są też na końcu układu
            znaki_lewe = znaki_lewe + ee
        elif ii in znaki:
            znaki_lewe, znaki_prawe = znaki.split(ii, 1)
            znaki_prawe = ii + znaki_prawe
        elif aa in znaki:
            znaki_lewe, znaki_prawe = znaki.split(aa, 1)
            znaki_prawe = aa + znaki_prawe
        elif uu in znaki:
            znaki_lewe, znaki_prawe = znaki.split(uu)
            znaki_prawe = uu + znaki_prawe
        else:
            print(f"ERR: Nie wiem jak podzielić {znaki} w {kombo}")
            return []
        znaki_lewe = znaki_lewe.replace(myślnik, nic)
        znaki_prawe = znaki_prawe.replace(myślnik, nic)
        gołe_lewe = znaki_lewe.replace(gwiazdka, nic).replace(tylda, nic)
        gołe_prawe = znaki_prawe.replace(gwiazdka, nic).replace(tylda, nic)
        istniejąca_tylda = nic
        if tylda_już_jest:
            istniejąca_tylda = tylda
        istniejąca_gwiazdka = nic
        if gwiazdka_już_jest:
            istniejąca_gwiazdka = gwiazdka
        wzrost_niedopasowania = 0
        if not tylda_już_jest and (l_tylda or p_tylda):
            nowe_kombinacje.append(gołe_lewe + tylda + istniejąca_gwiazdka + gołe_prawe)
            wzrost_niedopasowania += 1
        if not gwiazdka_już_jest and (l_gwiazdka or p_gwiazdka):
            nowe_kombinacje.append(gołe_lewe + istniejąca_tylda + gwiazdka + gołe_prawe)
            wzrost_niedopasowania += 1
        if not (tylda_już_jest and gwiazdka_już_jest) and (l_tyldogwiazdka or p_tyldogwiazdka):
            nowe_kombinacje.append(gołe_lewe + tylda + gwiazdka + gołe_prawe)
            wzrost_niedopasowania += 1
        output = []
        for nowa in nowe_kombinacje:
            output.append( ((nowa, ((l_tylda, lt_wszystko),(p_tylda, pt_wszystko)),
                                   ((l_gwiazdka, lg_wszystko), (p_gwiazdka, pg_wszystko)),
                                   ((l_tyldogwiazdka, ltg_wszystko), (p_tyldogwiazdka, ptg_wszystko))),
                            niedopasowanie + wzrost_niedopasowania))
        return output

    def zresetuj_klawiaturę(self):
        self.ręka_lewa.zresetuj_rękę()
        self.ręka_prawa.zresetuj_rękę()
        self.minimalne_indeksy_lewe = []
        self.minimalne_indeksy_prawe = []
        # self.środek.zresetuj_kciuki()

class Klawisz:
    def __init__(self, log, znak, indeks, kombinacja_id,
                 waga=1, samodzielny=0,
                 początkowy=False, końcowy=False):
        self.log = log
        self.znak = znak
        self.waga = waga
        self.indeks = indeks
        self.kombinacje = SłownikDomyślny(lambda x: 0)
        self.kombinacje[kombinacja_id] = 1
        self.początkowy = początkowy
        self.końcowy = końcowy
        self.samodzielny = samodzielny

    def __repr__(self):
        return f"({self.znak} wg:{self.waga} ({'P' if self.początkowy else ''}{'K' if self.końcowy else ''}{'S' if self.samodzielny else ''})"

    def zresetuj(self):
        self.waga = 0
        self.początkowy = False
        self.końcowy = False
        self.samodzielny = 0
        self.kombinacje = SłownikDomyślny(lambda x: 0)

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
        self.palec_wskazujący = Palec(log, konfiguracja.palce_lewe[3])
        self.kciuk_lewy = Palec(log, konfiguracja.palce_lewe[4])#  Palec(log, ["J", "E"])  # tutaj do logiki ważne jest tylko "J"
        self.kombinacje = {}  # Można tylko dodawać elementy do kombinacji, żeby IDki się zgadzały!!!

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

    def palec_dla_indeksu(self, indeks):
        if indeks in [0, 1]:
            return self.palec_mały
        elif indeks == 2:
            return self.palec_serdeczny
        elif indeks == 3:
            return self.palec_środkowy
        elif indeks in [4, 5]:
            return self.palec_wskazujący
        elif indeks == 6:
            return self.kciuk_lewy
        else:
            self.log.error(f"Lewa ręka nie ma palca dla indeksu: {indeks}")

    def zbuduj_kombinację(self, id_kombinacji, znaki, pierwsza=False, ostatnia=False):
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
            palec = self.palec_dla_indeksu(klawisz.indeks)
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
            self.log.error(f"RękaLewa nie ma kombinacji: {id_komb}")
            return
        elif self.kombinacje[id_komb]:
            self.log.error(f"RękaLewa komb. {id_komb} już aktywna.")
            return
        self.kombinacje[id_komb] = True

        for klawisz in kombinacja.zwróć_klawisze():
            palec = self.palec_dla_indeksu(klawisz.indeks)
            if klawisz.znak not in palec.wspierane_kombinacje:
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
            palec = self.palec_dla_indeksu(klawisz.indeks)
            if klawisz.znak not in palec.wspierane_kombinacje:
                self.log.error(f"Nie mogę deaktywować klawisza {klawisz.znak} dla {palec.wspierane_kombinacje}")
            else:
                palec.deaktywuj_klawisz(klawisz, kombinacja)

    def akord_lewy(self):
        tekst = self.palec_mały.tekst()
        tekst += self.palec_serdeczny.tekst()
        tekst += self.palec_środkowy.tekst()
        tekst += self.palec_wskazujący.tekst()
        tekst += self.kciuk_lewy.tekst()
        dodanie_tyldy = self.palec_wskazujący.dodanie_tyldy_możliwe()
        dodanie_gwiazdki = self.palec_wskazujący.dodanie_gwiazdki_możliwe()
        dodanie_tyldogwiazdki = self.palec_wskazujący.dodanie_tyldy_i_gwiazdki_możliwe()
        return (tekst, dodanie_tyldy, dodanie_gwiazdki, dodanie_tyldogwiazdki)


class RękaPrawa:
    def __init__(self, log, konfiguracja):
        self.log = log
        self.indeksy = konfiguracja.prawe_indeksy_klawiszy
        self.palec_wskazujący = Palec(log, konfiguracja.palce_prawe[0]) #Palec(log, ["~", "*", "C", "R"])
        self.palec_środkowy = Palec(log, konfiguracja.palce_prawe[1]) # Palec(log, ["L", "B"])
        self.palec_serdeczny = Palec(log, konfiguracja.palce_prawe[2]) # Palec(log, ["S", "G"])
        self.palec_mały = Palec(log, konfiguracja.palce_prawe[3]) # Palec(log, ["T", "W", "O", "Y"])
        self.kombinacje = {}  # Można tylko dodawać elementy do kombinacji, żeby IDki się zgadzały!!!
        self.dostępne_id_kombinacji = 0

    def zresetuj_rękę(self):
        self.kombinacje = {}
        self.dostępne_id_kombinacji = 0
        for palec in [self.palec_mały,
                      self.palec_serdeczny,
                      self.palec_środkowy,
                      self.palec_wskazujący]:
            for klawisz in palec.klawisze.values():
                klawisz.zresetuj()

    def waga(self):
        waga = 0
        for palec in [self.palec_mały, self.palec_serdeczny, self.palec_środkowy,
                      self.palec_wskazujący]:
            # self.log.info(f"Prawy palec: {palec.waga()}")
            waga += palec.waga()
        return waga

    def palec_dla_indeksu(self, indeks):
        if indeks in [5, 6]:
            return self.palec_wskazujący
        elif indeks == 7:
            return self.palec_środkowy
        elif indeks == 8:
            return self.palec_serdeczny
        elif indeks in [9, 10]:
            return self.palec_mały
        else:
            self.log.error(f"Prawa ręka nie ma palca dla indeksu: {indeks}")

    def zbuduj_kombinację(self, id_kombinacji, znaki, pierwsza=False, ostatnia=False):
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
            palec = self.palec_dla_indeksu(klawisz.indeks)
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
            self.log.error(f"RękaPrawa nie ma kombinacji: {id_komb}")
            return
        elif self.kombinacje[id_komb]:
            self.log.error(f"RękaPrawa komb. {id_komb} już aktywna.")
            return
        self.kombinacje[id_komb] = True
            
        for klawisz in kombinacja.zwróć_klawisze():
            palec = self.palec_dla_indeksu(klawisz.indeks)
            if klawisz.znak not in palec.wspierane_kombinacje:
                self.log.error(f"Nie mogę dodać klawisza {klawisz.znak} {klawisz.indeks}")
            else:
                palec.aktywuj_klawisz(klawisz, kombinacja)       
        
    def deaktywuj_kombinację(self, kombinacja):
        id_komb = kombinacja.id_kombinacji
        if id_komb not in self.kombinacje.keys():
            self.log.error(f"RękaPrawa nie ma kombinacji: {id_komb}")
            return
        elif not self.kombinacje[id_komb]:
            self.log.error(f"RękaPrawa komb. {id_komb} już nieaktywna.")
            return
        self.kombinacje[id_komb] = False

        for klawisz in kombinacja.zwróć_klawisze():
            palec = self.palec_dla_indeksu(klawisz.indeks)
            if klawisz.znak not in palec.wspierane_kombinacje:
                self.log.error(f"Nie mogę deaktywować klawisza {klawisz.znak} dla {palec.wspierane_kombinacje}")
            else:
                palec.deaktywuj_klawisz(klawisz, kombinacja)

    def akord_prawy(self):
        tekst = self.palec_wskazujący.tekst()
        tekst += self.palec_środkowy.tekst()
        tekst += self.palec_serdeczny.tekst()
        tekst += self.palec_mały.tekst()
        dodanie_tyldy = self.palec_wskazujący.dodanie_tyldy_możliwe()
        dodanie_gwiazdki = self.palec_wskazujący.dodanie_gwiazdki_możliwe()
        dodanie_tyldogwiazdki = self.palec_wskazujący.dodanie_tyldy_i_gwiazdki_możliwe()
        return (tekst, dodanie_tyldy, dodanie_gwiazdki, dodanie_tyldogwiazdki)
        

class Palec:
    def __init__(self, log, obsługiwane_klawisze):
        self.log = log
        self.wspierane_kombinacje = [nic,
                                     obsługiwane_klawisze[0],
                                     obsługiwane_klawisze[1],
                                     obsługiwane_klawisze[0]+obsługiwane_klawisze[1]]
        if len(obsługiwane_klawisze) == 4:
            self.wspierane_kombinacje += [obsługiwane_klawisze[2],
                                          obsługiwane_klawisze[3],
                                          obsługiwane_klawisze[2]+obsługiwane_klawisze[3],
                                          obsługiwane_klawisze[0]+obsługiwane_klawisze[2],
                                          obsługiwane_klawisze[1]+obsługiwane_klawisze[3],
                                          obsługiwane_klawisze[0]+obsługiwane_klawisze[1]+\
                                          obsługiwane_klawisze[2]+obsługiwane_klawisze[3]]
        elif len(obsługiwane_klawisze) == 3:  # Kciuki
            self.wspierane_kombinacje += [obsługiwane_klawisze[2],
                                          obsługiwane_klawisze[1]+obsługiwane_klawisze[2],
                                          obsługiwane_klawisze[0]+obsługiwane_klawisze[2]+\
                                          obsługiwane_klawisze[3]]
        self.obsługiwane_klawisze = obsługiwane_klawisze
        self.klawisze = {}

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
        for klawisz in self.obsługiwane_klawisze:
            if klawisz in self.klawisze.keys() and self.klawisze[klawisz].waga > 0:
                tekst += klawisz
        if tekst in self.wspierane_kombinacje:
            return tekst
        # self.log.debug(f"{tekst} nie jest wspierany")
        klawisz_do_deaktywacji = None
        for klawisz in self.klawisze.values():
            if klawisz.waga > 0 and self.można_deaktywować(klawisz):
            # if not użyty_klawisz.musi_zostać() \
            #   and self.można_deaktywować(użyty_klawisz):
                if not klawisz_do_deaktywacji:
                    klawisz_do_deaktywacji = klawisz
                elif klawisz_do_deaktywacji.waga > klawisz.waga:
                    klawisz_do_deaktywacji = klawisz

        if not klawisz_do_deaktywacji:
            self.log.error(f"Nie wiem jaki klawisz deaktywować: {[k for k in self.klawisze.values() if k.waga>0]}")
            return tekst  # To się nie powinno zdarzyć
        else:
            # klawisz_do_deaktywacji.waga = 0 # Kombinacje stają się niekompletne! (OK?)
            return tekst.replace(klawisz_do_deaktywacji.znak, nic)

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
            waga += klawisz.waga
        return waga

    def dodanie_tyldy_możliwe(self):
        if tylda not in self.obsługiwane_klawisze:
            return (False, False)
        elif tylda in self.klawisze.keys():
            return (False, False)
        elif len(self.klawisze) == 3:
            # return (True, self.wspierane_kombinacje[-1])
            return (True, True)  # tylda wspierana, wtedy wszystkie klawisze palca aktywne
        elif len(self.klawisze) == 1\
          and "L" in self.klawisze.keys():
            return (True, False)
        elif len(self.klawisze) == 1\
          and "C" in self.klawisze.keys():
            # return (True, "~C")
            return (True, False)  # tylda wspierana, wtedy nie wszystkie klawisze palca aktywne
        elif len(self.klawisze) == 0:
            return (True, False)
        return (False, False)

    def dodanie_gwiazdki_możliwe(self):
        ile_jest = 0
        for klawisz in self.klawisze.values():
            if klawisz.waga > 0:
                ile_jest += 1
        if gwiazdka not in self.obsługiwane_klawisze:
            return (False, False)
        elif gwiazdka in self.klawisze.keys():
            return (False, False)
        elif ile_jest == 3:
            # return (True, self.wspierane_kombinacje[-1])
            return (True, True)  # Gwiazdka wspierana, wtedy wszystkie klawisze aktywowane
        elif ile_jest == 1 and "K" in self.klawisze.keys():
            return (False, False)  # Gwiazdka wspierana, wtedy nie wszystkie klawisze aktywowane
        elif ile_jest == 1:
            return (True, False)  # Gwiazdka wspierana, wtedy nie wszystkie klawisze aktywowane
        elif ile_jest == 0:
            return (True, False)
        return (False, False)

    def dodanie_tyldy_i_gwiazdki_możliwe(self):
        if tylda not in self.obsługiwane_klawisze or\
          gwiazdka not in self.obsługiwane_klawisze:
            return (False, False)
        elif tylda in self.klawisze.keys() or\
          gwiazdka in self.klawisze.keys():
            return (False, False)
        elif len(self.klawisze) == 2:
            return (True, True)
        elif len(self.klawisze) == 0:
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
        return f"<ID:{self.id_kombinacji}{[klawisz for klawisz in self.klawisze.values()]}"
            

