class Stos():
    def __init__(self, log, generator):
        self.log = log
        self.generator = generator
        self.wysokość = 0
        self.elementy = dict()

    def połóż_na_stosie(self, sylaby, słowo, stenosłowa):
        długość_sylab = len(sylaby)
        min_długość = min(długość_sylab, self.wysokość)
        if min_długość < self.wysokość:
            for i in range(min_długość, self.wysokość):
                (_sylaba, rdzeń, _stenosłowa) = self.elementy.pop(i)
                if rdzeń:
                    self.generator.usuń_rdzeń(rdzeń)
        for i in range(min_długość):
            sylaba = sylaby[i]
            if self.elementy[i][0] != sylaba:
                self.elementy[i] = (sylaba, None, None)
        for i in range(min_długość, długość_sylab):
            sylaba = sylaby[i]
            self.elementy[i] = (sylaba, None, None)
        self.elementy[długość_sylab - 1] = (sylaby[-1], słowo, stenosłowa)
        self.wysokość = długość_sylab

    def dopasuj_do_sylab(self, sylaby):
        wynik = []
        długość_sylab = len(sylaby)
        min_długość = min(długość_sylab, self.wysokość)
        for i in range(min_długość):
            sylaba = sylaby[i]
            element = self.elementy[i]
            # Stos nie jest dopasowany do sylab zadanych
            if element[0] != sylaba:
                break
            # Opuszczamy sylaby bez stenosłowa
            if not element[1]:
                continue
            #  Najdłuższe dopasowanie na początku listy
            wynik.insert(0, (i + 1, element[1], element[2]))
        return wynik
