class Stos():
    def __init__(self, log, generator):
        self.log = log
        self.generator = generator
        self.wysokość = 0
        self.elementy = dict()
        # self.położono = 0

    def połóż_na_stosie(self, sylaby, słowo, stenosłowa):
        # self.położono += 1
        długość_sylab = len(sylaby)
        min_długość = min(długość_sylab, self.wysokość)
        if min_długość < self.wysokość:
            # self.log.info(f"Przed usuwaniem: {self.elementy.keys()}")
            # klucze = self.elementy.keys()
            for i in range(min_długość, self.wysokość):
                # if i in klucze:
                (_sylaba, rdzeń, _stenosłowa) = self.elementy.pop(i)
                if rdzeń:
                     self.generator.usuń_rdzeń(rdzeń)
            # self.log.info(f"Po usuwaniu: {długość_sylab}      {len(self.elementy)}")
        for i in range(min_długość):
            sylaba = sylaby[i]
            if self.elementy[i][0] != sylaba:
                if długość_sylab == i + 1:
                    # self.log.debug(f"Zamieniam: {self.elementy[i]} na niepuste {sylaba}")
                    self.elementy[i] = (sylaba, słowo, stenosłowa)
                else:
                    # self.log.debug(f"Zamieniam: {self.elementy[i]} na puste {sylaba}")
                    self.elementy[i] = (sylaba, None, None)
        for i in range(min_długość, długość_sylab):
            sylaba = sylaby[i]
            self.elementy[i] = (sylaba, None, None)
        self.elementy[długość_sylab - 1] = (sylaby[-1], słowo, stenosłowa)
        self.wysokość = długość_sylab
        # if self.położono % 1000 == 0:
        #     self.log.info(f"Elementów na stosie:                          {len(self.elementy)}")
            # for element in self.elementy.values():
            #     self.log.info(f"{element[0]}")

    def dopasuj_do_sylab(self, sylaby):
        # self.log.debug(f"Szukam dla {sylaby}")
        wynik = None
        długość_sylab = len(sylaby)
        min_długość = min(długość_sylab, self.wysokość)
        for i in range(min_długość):
            sylaba = sylaby[i]
            element = self.elementy[i]
            # Stos nie jest dopasowany do sylab zadanych
            if element[0] != sylaba:
                break
            # Opuszczamy sylaby bez stenosłowa
            if not element[2]:
                continue
            #  Najdłuższe dopasowanie na początku listy
            # wynik.insert(0, (i + 1, element[1], element[2]))
            wynik = (i + 1, element[1], element[2])
        if wynik:
            self.log.debug(f"Dopasowano ze stosu: {wynik}")
        return wynik
