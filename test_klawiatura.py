from klawiatura import Akord
from collections import OrderedDict
import unittest

class TestAkord(unittest.TestCase):
    def setUp(self):
        self.znaki_środka = OrderedDict({"J": False,
                                         "E": False,
                                         "~": False,
                                         "*": False,
                                         "U": False,
                                         "A": False,
                                         "I": False})
        
    def test_tworzenie(self):
        akord = Akord(log=None,
                      tekst_lewy="X",
                      znaki_środka = self.znaki_środka,
                      niedopasowanie = 0,
                      tekst_prawy = "",
                      dodanie_tyldy = (False, False),
                      dodanie_gwiazdki = (False, False),
                      dodanie_tyldogwiazdki = (False, False))

        assert akord, "Akord powinien zostać stworzony"

    def test_kopiowanie(self):
        akord = Akord(log=None,
                      tekst_lewy="X",
                      znaki_środka = self.znaki_środka,
                      niedopasowanie = 0,
                      tekst_prawy = "",
                      dodanie_tyldy = (False, False),
                      dodanie_gwiazdki = (False, False),
                      dodanie_tyldogwiazdki = (False, False))
        akord2 = akord.kopia()
        # print(f"{akord} {akord2}")
        assert akord == akord2, "Akordy powininny być identyczne"

    def test_dodawanie(self):
        akord = Akord(log=None,
                      tekst_lewy="X",
                      znaki_środka = self.znaki_środka,
                      niedopasowanie = 0,
                      tekst_prawy = "",
                      dodanie_tyldy = (False, False),
                      dodanie_gwiazdki = (False, False),
                      dodanie_tyldogwiazdki = (False, False))
        akord2 = Akord(log=None,
                       tekst_lewy="",
                      znaki_środka = self.znaki_środka,
                     niedopasowanie = 0,
                     tekst_prawy = "Y",
                     dodanie_tyldy = (False, False),
                     dodanie_gwiazdki = (False, False),
                     dodanie_tyldogwiazdki = (False, False))
        akord3 = akord + akord2
        akord4 = Akord(log=None,
                     tekst_lewy="X",
                      znaki_środka = self.znaki_środka,
                     niedopasowanie = 0,
                     tekst_prawy = "Y",
                     dodanie_tyldy = (False, False),
                     dodanie_gwiazdki = (False, False),
                     dodanie_tyldogwiazdki = (False, False))
        assert akord3 == akord4, "Akordy powininny się dodawać"

    def test_dzielenie(self):
        akord = Akord(log=None,
                     tekst_lewy="KTURY",
                      znaki_środka = self.znaki_środka,
                     niedopasowanie = 0,
                     tekst_prawy = "",
                     dodanie_tyldy = (False, False),
                     dodanie_gwiazdki = (False, False),
                     dodanie_tyldogwiazdki = (False, False))

        assert akord.tekst_lewy == "KT", "Akord powinien zostać dobrze podzielony"
        assert akord.tekst_prawy == "RY", f"Akord {akord} powinien zostać dobrze podzielony"
        assert f"{akord}" == "KTURY", "Akord nieprawidłowo reprezentowany"

    def test_opuszczanie_tyldy(self):
        akord = Akord(log=None,
                     tekst_lewy="KT~",
                      znaki_środka = self.znaki_środka,
                     niedopasowanie = 0,
                     tekst_prawy = "",
                     dodanie_tyldy = (False, False),
                     dodanie_gwiazdki = (False, False),
                     dodanie_tyldogwiazdki = (False, False))

        assert akord.tekst_lewy == "KT", f"Akord {akord.l_tekst()} powinien zostać dobrze podzielony"
        assert akord.znaki_środka["~"], "Akord powinien mieć ustawioną flage tyldy"

    def test_opuszczanie_gwiazdki(self):
        akord = Akord(log=None,
                     tekst_lewy="*URY",
                      znaki_środka = self.znaki_środka,
                     niedopasowanie = 0,
                     tekst_prawy = "",
                     dodanie_tyldy = (False, False),
                     dodanie_gwiazdki = (False, False),
                     dodanie_tyldogwiazdki = (False, False))

        assert akord.tekst_lewy == "", f"Akord {akord} powinien zostać dobrze podzielony"
        assert akord.znaki_środka["*"], "Akord powinien mieć ustawioną flage gwiazdki"
        assert akord.znaki_środka["U"], "Akord powinien mieć ustawioną flage U"
        assert akord.tekst_prawy == "RY", f"Akord {akord} powinien zostać dobrze podzielony"

    
if __name__ == "__main__":
    # test_tworzenie()
    # test_kopiowanie()
    # test_dodawanie()
    unittest.main()
    print("Everything passed")
