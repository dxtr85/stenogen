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
        self.ręka_lewa = RękaLewa(log, konfiguracja)
        self.ręka_prawa = RękaPrawa(log, konfiguracja)
        # self.środek = Kciuki(log, konfiguracja)
        self.rozdzielacz = SłownikDomyślny(lambda x: dzielniki_dla_słowa_o_długości(x))

    def wygeneruj_akordy(self, słowo, sylaby, limit_prób):
        dzielniki_słowa = self.rozdzielacz[len(sylaby)]
        akordy = []
        for gdzie_podzielić in dzielniki_słowa:
            (sylaby_lewe,
            sylaba_środkowa,
            sylaby_prawe) = self.podziel_sylaby_na_strony(sylaby,
                                                          gdzie_podzielić)
            bez_inwersji = True
            malejące_lewe = []
            malejące_prawe = []
            pozostały_kombinacje_do_przetestowania = True

            indeks_odjemników = -1
            odjemniki_sylab = []
            odejmuj = False
            bez_środka = False
            niemalejące_zainicjalizowane = False

            while limit_prób > 0:
                # if słowo == "ona":
                #        self.log.info(f"limit: {limit_prób}")
                # Wszystkie literki powinny być dopasowane
                # nagłos - lewa, śródgłos - kciuk(i), wygłos - prawa
                # self.log.debug(f"Sylaby: {sylaby_lewe}|{sylaba_środkowa}|{sylaby_prawe}")
                wzrost_niedopasowania = 0
                (fonemy_lewe,
                 śródgłos,
                 fonemy_prawe) = self.język.rozbij_sylaby_na_fonemy(sylaby_lewe,
                                                            sylaba_środkowa,
                                                            sylaby_prawe)
                # if słowo == "ona":
                #    self.log.info(f"{fonemy_lewe} | {śródgłos} | {fonemy_prawe}")
                #     śródgłos = []
                waga_słowa = 0
                for fonem in fonemy_lewe + śródgłos + fonemy_prawe:
                    waga_słowa += fonem[1]
                if bez_środka:
                    # if słowo == "nać":
                    #     self.log.info(f"nać bez środka śródgłos: {śródgłos}")
                    śródgłos = []

                kombinacja_środkowa = nic
                if not niemalejące_zainicjalizowane:
                    fonemy_niemalejące = False
                    while not fonemy_niemalejące:
                        fonemy_lewe = self.język.odejmij_fonemy(fonemy_lewe, malejące_lewe)
                        # self.log.info(f"Odjęte lewe: {fonemy_lewe}")
                        fonemy_prawe = self.język.odejmij_fonemy(fonemy_prawe, malejące_prawe)
                        (fonemy_niemalejące, który, gdzie) = self.niemalejące(fonemy_lewe,
                                                                              fonemy_prawe,
                                                                              bez_inwersji)
                        #  Zbieramy informacje o fonemach, które być może
                        #  trzeba będzie wyciszyć aby uzyskać unikalną
                        #  kombinację
                        if not fonemy_niemalejące:
                            if który == 0:
                                malejące_lewe.append(gdzie[2])
                            else:
                                malejące_prawe.append(gdzie[2])
                    odjemniki_sylab = self.wygeneruj_odjemniki(malejące_lewe, malejące_prawe)
                    niemalejące_zainicjalizowane = True
                if odejmuj and indeks_odjemników < len(odjemniki_sylab) and indeks_odjemników >= 0:
                    # self.log.info(f"odjemniki: {odjemniki_sylab}")
                    (do_odjęcia_lewe,
                    do_odjęcia_prawe,
                    wzrost_niedopasowania) = odjemniki_sylab[indeks_odjemników]
                    fonemy_lewe = self.język.odejmij_fonemy(fonemy_lewe, do_odjęcia_lewe)
                                                    # malejące_lewe[indeks_odjemników])
                    fonemy_prawe = self.język.odejmij_fonemy(fonemy_prawe, do_odjęcia_prawe)
                                                    # malejące_prawe[indeks_odjemników])

                pierwsza = True
                ostatnia = False
                długość_lewych = len(fonemy_lewe)
                for i in range(długość_lewych):
                    fonem = fonemy_lewe[i]
                    if i == długość_lewych -1:
                        ostatnia = True
                    znaki = self.klawisze_dla_fonemu(fonem)
                    self.ręka_lewa.zbuduj_kombinację(znaki, pierwsza, ostatnia)
                    pierwsza = False
                for fonem in śródgłos:
                    znaki = self.język.fonemy_samogłoskowe[fonem[0]][0]
                    kombinacja_środkowa += znaki
                pierwsza = True
                ostatnia = False
                długość_fonemów_prawych = len(fonemy_prawe)
                for i in range(długość_fonemów_prawych):
                    fonem = fonemy_prawe[i]
                    if i + 1 == długość_fonemów_prawych:
                        ostatnia = True
                    znaki = self.klawisze_dla_fonemu(fonem, prawe=True)
                    self.ręka_prawa.zbuduj_kombinację(znaki, pierwsza, ostatnia)
                    pierwsza = False
                # self.log.debug(f"{słowo} {waga_słowa}, Lewa:{ręka_lewa.waga()} Prawa: {ręka_prawa.waga()}")
                niedopasowanie = waga_słowa + wzrost_niedopasowania\
                  - self.ręka_lewa.waga() - self.ręka_prawa.waga()
                # self.log.debug(f"{słowo} NPo: {niedopasowanie}")
                # kompletny_akord: ("ZN~*AKI",
                #   ( (dodanie_tyldy_z_lewej, czy_wszystkie_klawisze),
                #     (dodanie_tyldy_z_prawej, czy_wszystkie_klawisze) ),
                #   ( (dodanie_gwiazdki_z_lewej, czy_wszystkie_klawisze),
                #     (dodanie_gwiazdki_z_prawej, czy_wszystkie_klawisze) ),
                #   ( (dodanie_tyldogwiazdki_z_lewej, czy_wszystkie_klawisze),
                #     (dodanie_tyldogwiazdki_z_prawej, czy_wszystkie_klawisze) ) )
                kompletny_akord = self.połącz_kombinacje(#self.ręka_lewa.akord_lewy(),
                                                            kombinacja_środkowa)#,
                                                            #self.ręka_prawa.akord_prawy())
                akordy.append((kompletny_akord, niedopasowanie))
                limit_prób -= 1
                if bez_środka:
                    break
                    # if słowo == "nać":
                    #     self.log.info("nać bez środka")
                    # bez_inwersji = False
                    bez_środka = True
                if odejmuj:
                    indeks_odjemników += 1
                    if indeks_odjemników >= len(odjemniki_sylab):
                        odejmuj = False
                        bez_środka = True
                        pozostały_kombinacje_do_przetestowania = False
                if bez_inwersji:
                    #bez_środka = True
                    odejmuj = True
                    bez_inwersji = False
                # if limit_prób % 3 == 0:
                #     break
            self.zresetuj_klawisze()
        # if słowo == "ona":
        #    self.log.info(f"{akordy}")
        return akordy

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
                sylaby_prawe = [sylaby[gdzie_podzielić + 1]]
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
                (ręka_lewa[3], ręka_prawa[3]),)  # dodanie tyldogwiazdki możliwe

    def wygeneruj_odjemniki(self, malejące_lewe, malejące_prawe):
        łączna_waga = 0
        odjemniki = []
        for sylaba in malejące_lewe + malejące_prawe:
            łączna_waga += sylaba[1]
        for sylaba in malejące_lewe:
            odjemniki.append(([sylaba], malejące_prawe, łączna_waga - sylaba[1]))
        for sylaba in malejące_prawe:
            odjemniki.append((malejące_lewe, [sylaba], łączna_waga - sylaba[1]))
        return odjemniki

    def niemalejące(self, fonemy_lewe, fonemy_prawe, bez_inwersji=False):
        # print(f"Niemalejące?: {fonemy_lewe}|{fonemy_prawe}")
        inwersja_użyta = False
        if bez_inwersji:
            inwersja_użyta = True
        indeksy = self.lewe_indeksy_klawiszy
        indeksy_fonemów_lewe = [(0, 0, nic)]  # (indeks_klawisza, indeks_pomocniczy, (fonem, waga))
        j = 0
        for i in range(len(fonemy_lewe)):
            fonem = fonemy_lewe[i]
            minimalny_indeks_klawisza = 5
            # print(f"Fonem:{fonem} w {fonemy_lewe}")
            for klawisz in self.klawisze_dla_fonemu(fonem[0]):
                bieżący_indeks = indeksy[klawisz]
                if bieżący_indeks < minimalny_indeks_klawisza:
                    minimalny_indeks_klawisza = bieżący_indeks
            if minimalny_indeks_klawisza != indeksy_fonemów_lewe[-1][0]:
                indeksy_fonemów_lewe.append((minimalny_indeks_klawisza, j, fonem))
                j += 1
        indeksy_fonemów_lewe = indeksy_fonemów_lewe[1:]
        (jest_niemalejący, gdzie_nie_jest) = self.ciąg_niemalejący(indeksy_fonemów_lewe[1:])
        if not jest_niemalejący:
            if not inwersja_użyta:
                # print(f"nie jest: {gdzie_nie_jest} indeksy: {indeksy_fonemów_lewe}")
                tymczasowy = indeksy_fonemów_lewe[gdzie_nie_jest[1] - 1]
                indeksy_fonemów_lewe[gdzie_nie_jest[1] - 1] = indeksy_fonemów_lewe[gdzie_nie_jest[1]]
                indeksy_fonemów_lewe[gdzie_nie_jest[1]] = tymczasowy
                inwersja_użyta = True
                (jest_niemalejący, gdzie_nie_jest) = self.ciąg_niemalejący(indeksy_fonemów_lewe)
                if not jest_niemalejący:
                    return (False, 0, gdzie_nie_jest)
            else:
                return (False, 0, gdzie_nie_jest)

        indeksy_fonemów_prawe = [(5, 0, nic)]
        # print(f"sprawdzam: {fonemy_lewe}||{fonemy_prawe}")
        indeksy = self.prawe_indeksy_klawiszy
        j = 0
        for i in range(len(fonemy_prawe)):
            fonem = fonemy_prawe[i]  # ('di', waga)
            minimalny_indeks_klawisza = 10
            for klawisz in self.klawisze_dla_fonemu(fonem[0], prawe=True):
                bieżący_indeks = indeksy[klawisz]
                if bieżący_indeks < minimalny_indeks_klawisza:
                    minimalny_indeks_klawisza = bieżący_indeks
            if minimalny_indeks_klawisza != indeksy_fonemów_prawe[-1][0]:
                indeksy_fonemów_prawe.append((minimalny_indeks_klawisza, j, fonem))
                j += 1
        indeksy_fonemów_prawe = indeksy_fonemów_prawe[1:]
        (jest_niemalejący, gdzie_nie_jest) = self.ciąg_niemalejący(indeksy_fonemów_prawe)
        if not jest_niemalejący and not inwersja_użyta:
            # print(f"male: {gdzie_nie_jest} - {indeksy_fonemów_prawe}")
            tymczasowy = indeksy_fonemów_prawe[gdzie_nie_jest[1] - 1]
            indeksy_fonemów_prawe[gdzie_nie_jest[1] - 1] = indeksy_fonemów_prawe[gdzie_nie_jest[1]]
            indeksy_fonemów_prawe[gdzie_nie_jest[1]] = tymczasowy
            inwersja_użyta = True
            (jest_niemalejący, gdzie_nie_jest) = self.ciąg_niemalejący(indeksy_fonemów_prawe)
            if not jest_niemalejący:
                return (False, 1, gdzie_nie_jest)
            return (True, None, None)
        elif jest_niemalejący:
            return (True, None, None)
        return (False, 1, gdzie_nie_jest)

    def ciąg_niemalejący(self, ciąg):
        długość_ciągu = len(ciąg)
        if długość_ciągu < 2:
            return (True, None)
        else:
            for i in range(1, długość_ciągu):
                if ciąg[i][0] < ciąg[i-1][0]:
                    return (False, ciąg[i])
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
            znaki_lewe, znaki_prawe = znaki.split(ee)
            znaki_lewe = znaki_lewe + ee
        elif ii in znaki:
            znaki_lewe, znaki_prawe = znaki.split(ii)
            znaki_prawe = ii + znaki_prawe
        elif aa in znaki:
            znaki_lewe, znaki_prawe = znaki.split(aa)
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

        if not tylda_już_jest and (l_tylda or p_tylda):
            nowe_kombinacje.append(gołe_lewe + tylda + istniejąca_gwiazdka + gołe_prawe)
        if not gwiazdka_już_jest and (l_gwiazdka or p_gwiazdka):
            nowe_kombinacje.append(gołe_lewe + istniejąca_tylda + gwiazdka + gołe_prawe)
        if not (tylda_już_jest and gwiazdka_już_jest) and (l_tyldogwiazdka or p_tyldogwiazdka):
            nowe_kombinacje.append(gołe_lewe + tylda + gwiazdka + gołe_prawe)
        output = []
        for nowa in nowe_kombinacje:
            output.append( ((nowa, ((l_tylda, lt_wszystko),(p_tylda, pt_wszystko)),
                                   ((l_gwiazdka, lg_wszystko), (p_gwiazdka, pg_wszystko)),
                                   ((l_tyldogwiazdka, ltg_wszystko), (p_tyldogwiazdka, ptg_wszystko))),
                            niedopasowanie))
        return output

    def zresetuj_klawisze(self):
        # self.ręka_lewa = RękaLewa(self.log, self.konfiguracja)
        # self.ręka_prawa = RękaPrawa(self.log, self.konfiguracja)

        self.ręka_lewa.zresetuj_klawisze()
        self.ręka_prawa.zresetuj_klawisze()
        # self.środek.zresetuj_klawisze()

class Klawisz:
    def __init__(self, znak, indeks, kombinacja_id, waga=1, samodzielny=0, początkowy=False, końcowy=False):
        self.znak = znak
        self.waga = waga
        # if początkowy or końcowy:
        #     self.waga += 1
        self.indeks = indeks
        self.kombinacja = set()
        self.kombinacja.add(kombinacja_id)
        self.początkowy = początkowy
        self.końcowy = końcowy
        self.samodzielny = samodzielny

    def zresetuj(self):
        self.waga = 0
        self.początkowy = False
        self.końcowy = False
        self.samodzielny = False
        self.kombinacja = set()

    def aktualizuj(self, inny_klawisz, id_kombinacji, długość_kombinacji):
        self.kombinacja.add(id_kombinacji)
        samodzielny = 0
        if długość_kombinacji == 1:
            samodzielny = 1
        self.samodzielny += samodzielny
        if inny_klawisz.początkowy:
            self.początkowy = True
        if inny_klawisz.końcowy:
            self.końcowy = True
        self.waga += inny_klawisz.waga

    def musi_zostać(self):
        return self.początkowy or self.końcowy

class Kciuki:
    def __init__(self, log, konfiguracja):
        self.log = log
        self.konfiguracja = konfiguracja
        klawisz_jot = Klawisz(jot, None)
        klawisz_ee = Klawisz(ee, None)
        klawisz_ii = Klawisz(ii, None)
        klawisz_aa = Klawisz(aa, None)
        klawisz_uu = Klawisz(uu, None)
        self.kciuk_lewy = Palec(log, [klawisz_jot, klawisz_ee, klawisz_ii])
        self.kciuk_prawy = Palec(log, [klawisz_ii, klawisz_aa, klawisz_uu])
        self.kombinacje = []  # Można tylko dodawać elementy do kombinacji, żeby IDki się zgadzały!!!

    def zresetuj_klawisze(self):
        for palec in [self.kciuk_lewy,
                      self.kciuk_prawy]:
            for klawisz in palec.klawisze.values():
                klawisz.zresetuj()

    def waga(self):
        waga = 0
        for palec in [self.palec_mały, self.palec_serdeczny, self.palec_środkowy,
                      self.palec_wskazujący, self.kciuk_lewy]:
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

    def zbuduj_kombinację(self, znaki, pierwsza=False, ostatnia=False):
        id_kombinacji = self.dostępne_id_kombinacji
        self.dostępne_id_kombinacji += 1
        kombinacja = Kombinacja(self.konfiguracja,
                                id_kombinacji,
                                znaki,
                                prawa=False,
                                pierwsza_kombinacja=pierwsza,
                                ostatnia_kombinacja=ostatnia)
        self.dodaj_kombinację(kombinacja)

    def dodaj_kombinację(self, kombinacja):
        self.kombinacje.append(kombinacja)
        for klawisz in kombinacja.zwróć_klawisze():
            palec = self.palec_dla_indeksu(klawisz.indeks)
            if klawisz.znak not in palec.wspierane_kombinacje:
                self.log.error(f"Nie mogę dodać klawisza {klawisz.znak} {klawisz.indeks}")
            else:
                palec.dodaj_klawisz(klawisz, kombinacja.id_kombinacji, kombinacja.długość_kombinacji)

    def akordy_kciukowe(self):
        tekst = self.palec_mały.tekst()
        tekst += self.palec_serdeczny.tekst()
        tekst += self.palec_środkowy.tekst()
        tekst += self.palec_wskazujący.tekst()
        tekst += self.kciuk_lewy.tekst()
        dodanie_tyldy = self.palec_wskazujący.dodanie_tyldy_możliwe()
        dodanie_gwiazdki = self.palec_wskazujący.dodanie_gwiazdki_możliwe()
        dodanie_tyldogwiazdki = self.palec_wskazujący.dodanie_tyldy_i_gwiazdki_możliwe()
        return (tekst, dodanie_tyldy, dodanie_gwiazdki, dodanie_tyldogwiazdki)


class RękaLewa:
    def __init__(self, log, konfiguracja):
        self.log = log
        self.konfiguracja = konfiguracja
        self.palec_mały = Palec(log, ["X", "F", "Z", "S"])
        self.palec_serdeczny = Palec(log, ["K", "T"])
        self.palec_środkowy = Palec(log, ["P", "V"])
        self.palec_wskazujący = Palec(log, ["L", "R", "~", "*"])
        self.kciuk_lewy = Palec(log, ["J", "E"])  # tutaj do logiki ważne jest tylko "J"
        self.kombinacje = []  # Można tylko dodawać elementy do kombinacji, żeby IDki się zgadzały!!!
        self.dostępne_id_kombinacji = 0

    def zresetuj_klawisze(self):
        self.dostępne_id_kombinacji = 0
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

    def zbuduj_kombinację(self, znaki, pierwsza=False, ostatnia=False):
        id_kombinacji = self.dostępne_id_kombinacji
        self.dostępne_id_kombinacji += 1
        kombinacja = Kombinacja(self.konfiguracja,
                                id_kombinacji,
                                znaki,
                                prawa=False,
                                pierwsza_kombinacja=pierwsza,
                                ostatnia_kombinacja=ostatnia)
        self.dodaj_kombinację(kombinacja)

    def dodaj_kombinację(self, kombinacja):
        self.kombinacje.append(kombinacja)
        for klawisz in kombinacja.zwróć_klawisze():
            palec = self.palec_dla_indeksu(klawisz.indeks)
            if klawisz.znak not in palec.wspierane_kombinacje:
                self.log.error(f"Nie mogę dodać klawisza {klawisz.znak} {klawisz.indeks}")
            else:
                palec.dodaj_klawisz(klawisz, kombinacja.id_kombinacji, kombinacja.długość_kombinacji)

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
        self.konfiguracja = konfiguracja
        self.palec_wskazujący = Palec(log, ["~", "*", "C", "R"])
        self.palec_środkowy = Palec(log, ["L", "B"])
        self.palec_serdeczny = Palec(log, ["S", "G"])
        self.palec_mały = Palec(log, ["T", "W", "O", "Y"])
        self.kombinacje = []  # Można tylko dodawać elementy do kombinacji, żeby IDki się zgadzały!!!
        self.dostępne_id_kombinacji = 0

    def zresetuj_klawisze(self):
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

    def zbuduj_kombinację(self, znaki, pierwsza=False, ostatnia=False):
        id_kombinacji = self.dostępne_id_kombinacji
        self.dostępne_id_kombinacji += 1
        kombinacja = Kombinacja(self.konfiguracja,
                                id_kombinacji,
                                znaki,
                                prawa=True,
                                pierwsza_kombinacja=pierwsza,
                                ostatnia_kombinacja=ostatnia)
        self.dodaj_kombinację(kombinacja)

    def dodaj_kombinację(self, kombinacja):
        self.kombinacje.append(kombinacja)
        for klawisz in kombinacja.zwróć_klawisze():
            palec = self.palec_dla_indeksu(klawisz.indeks)
            if klawisz.znak not in palec.wspierane_kombinacje:
                self.log.error(f"Nie mogę dodać klawisza {klawisz.znak} {klawisz.indeks}")
            else:
                palec.dodaj_klawisz(klawisz, kombinacja.id_kombinacji, kombinacja.długość_kombinacji)

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

    def dodaj_klawisz(self, klawisz, id_kombinacji, długość_kombinacji):
        if klawisz.znak not in self.obsługiwane_klawisze:
            self.log.error(f"{klawisz.znak} nieobsługiwany ({self.obsługiwane_klawisze})")
        elif klawisz.znak not in self.klawisze.keys():
            self.klawisze[klawisz.znak] = klawisz
        else:
            self.klawisze[klawisz.znak].aktualizuj(klawisz, id_kombinacji, długość_kombinacji)

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
            self.log.error(f"Nie znalazłem prawidłowej kombinacji dla {self.klawisze.keys()}")
            return tekst  # To się nie powinno zdarzyć
        else:
            return tekst.replace(klawisz_do_deaktywacji.znak, nic)

        # ile_klawiszy_użytych = len(self.klawisze)
        # if ile_klawiszy_użytych == 3:
        #     # Musimy coś wywalić, pierwszy i ostatni musi zostać
        #     musi_zostać = self.pierwszy_lub_ostatni_klawisz()
        #     if not musi_zostać:
        #         usuwany_klawisz = Klawisz('', -1, -1, 100)
        #         for klawisz in self.klawisze.values():
        #             if klawisz.waga < usuwany_klawisz.waga\
        #               and self.można_deaktywować(klawisz):
        #                 usuwany_klawisz = klawisz
        #         self.klawisze.pop(usuwany_klawisz.znak)
        #     else:
        #         for klawisz in self.klawisze.values():
        #             if klawisz.znak == musi_zostać:
        #                 continue
        #             if musi_zostać+klawisz.znak in self.wspierane_kombinacje:
        #                 return musi_zostać+klawisz.znak
        #             elif klawisz.znak+musi_zostać in self.wspierane_kombinacje:
        #                 return klawisz.znak+musi_zostać
        #         self.log.error(f"Nie znalazłem prawidłowej kombinacji dla {self.klawisze.keys()}")
        # for klawisz in self.obsługiwane_klawisze:
        #     if klawisz in self.klawisze.keys():
        #         tekst += klawisz
        # return tekst

    def można_deaktywować(self, usuwany_klawisz):
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
        if gwiazdka not in self.obsługiwane_klawisze:
            return (False, False)
        elif gwiazdka in self.klawisze.keys():
            return (False, False)
        elif len(self.klawisze) == 3:
            # return (True, self.wspierane_kombinacje[-1])
            return (True, True)  # Gwiazdka wspierana, wtedy wszystkie klawisze aktywowane
        elif len(self.klawisze) == 1\
          and ("R" in self.klawisze.keys() or tylda in self.klawisze.keys()):
            # if self.obsługiwane_klawisze[0] == "L"
            #     return (True, "R*")
            # else:
            #     return (True, "*R")
            return (True, False)  # Gwiazdka wspierana, wtedy nie wszystkie klawisze aktywowane
        elif len(self.klawisze) == 0:
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
                 konfiguracja,
                 id_kombinacji,
                 znaki,
                 waga=1,
                 prawa=False,
                 pierwsza_kombinacja=False,
                 ostatnia_kombinacja=False):
        self.indeksy = konfiguracja.lewe_indeksy_klawiszy
        if prawa:
            self.indeksy = konfiguracja.prawe_indeksy_klawiszy
        self.id_kombinacji = id_kombinacji
        self.klawisze = dict()
        self.długość_kombinacji = len(znaki)
        for znak in znaki:
            indeks = self.indeksy[znak]
            samodzielny = 0
            if self.długość_kombinacji == 1:
                samodzielny = 1
            self.klawisze[znak] = Klawisz(znak,
                                          indeks,
                                          id_kombinacji,
                                          waga,
                                          samodzielny,
                                          pierwsza_kombinacja,
                                          ostatnia_kombinacja)
    def zwróć_klawisze(self):
        for klawisz in self.klawisze.values():
            yield klawisz
            

