class Logger:
    def __init__(self, plik_logowania, rozmiar_bufora=1024, pisz_na_ekran=True):
        self.plik_logowania = open(plik_logowania, 'a', buffering=rozmiar_bufora)
        self.pisz_na_ekran = pisz_na_ekran

    def __exit__(self):
        self.plik_logowania.flush()
        self.plik_logowania.close()

    def _loguj(self, poziom_logowania, dane):
        self.plik_logowania.write(f"{poziom_logowania}: {dane}\n")

    def info(self, dane):
        self._loguj("INF", dane)
        if self.pisz_na_ekran:
            print(f"INF: {dane}")

    def debug(self, dane):
        self._loguj("DBG", dane)

    def error(self, dane):
        self._loguj("ERR", dane)
        if self.pisz_na_ekran:
            print(f"ERR: {dane}")


