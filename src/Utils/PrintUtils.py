from src.Config.Config import Config


HASH_LINE = '##########################################################################################################'

TEMPLATES = {
    None: '%s',
    'file.error.no_config': 'Brak konfiguracji dla pliku: %s - plik zostanie ominięty',
    'file.process.start': 'Rozpoczęto procesowanie pliku: %s',
    'file.process.no_table_found': 'Wiersz rozpoczynający nie został znaleziony tabele - plik zostanie ominięty',
    'file.process.rows_count': 'Przekopiowano %d wierszy',
    'file.process.finish': 'Zakończono procesowanie pliku',
    'file.process.no_column_found': 'Nie znaleziono kolumn o numerach %d - prawdopodobnie konfiguracja w pliku '
                                    'config.yaml jest błędna',

    'file.postprocess.start': 'Rozpoczęto post-processing pliku: %s',
    'file.postprocess.finish': 'Zakończono post-processing pliku',

    'file.analyze.start': 'Rozpoczęto analizowanie pliku: %s',
    'file.analyze.finish': 'Zakończono analizowanie pliku',
}


class PrintUtils:
    @staticmethod
    def print_line(
            template: str = None,
            *args,
            should_print_hash: bool = False,
            additional_new_line: bool = False
    ) -> None:
        if template not in TEMPLATES:
            raise RuntimeError('Nieobsługiwany szablon komunikatu')

        if not Config.ENABLE_PRINTING:
            return

        if should_print_hash:
            PrintUtils.print_hash()

        print(TEMPLATES[template] % args, end="\n\n" if additional_new_line else "\n")

    @staticmethod
    def print_hash() -> None:
        if not Config.ENABLE_PRINTING:
            return

        print(HASH_LINE)
