class MessageConst:
    HASH_LINE = '######################################################################################################'

    ERROR_NO_CONFIG = 'Brak konfiguracji dla pliku: %s - plik zostanie ominięty'

    REPROCESS_CLEAN_FILES_START = 'Rozpoczęto czyszczenie przeprocesowanych plików'
    REPROCESS_CLEAN_FILE = 'Usunięto plik: %s'
    REPROCESS_CLEAN_PROCESSED_FILES_LIST = 'Wyczyszczono plik zawierający liste przeprocesowanych plików'


    PROCESS_START = 'Rozpoczęto procesowanie pliku: %s'
    PROCESS_NO_TABLE_FOUND = 'Wiersz rozpoczynający nie został znaleziony tabele - plik zostanie ominięty'
    PROCESS_ROWS_COUNT = 'Przekopiowano %d wierszy'
    PROCESS_FINISH = 'Zakończono procesowanie pliku'
    PROCESS_NO_COLUMN_FOUND = (
        'Nie znaleziono kolumn o numerach %d - prawdopodobnie konfiguracja w pliku '
        'config.yaml jest błędna'
    )

    POST_PROCESS_START = 'Rozpoczęto post-processing pliku: %s'
    POST_PROCESS_FINISH = 'Zakończono post-processing pliku'

    ANALYZE_START = 'Rozpoczęto analizowanie pliku: %s'
    ANALYZE_FINISH = 'Zakończono analizowanie pliku'

    MESSAGES = [
        HASH_LINE,
        ERROR_NO_CONFIG,
        REPROCESS_CLEAN_FILES_START,
        REPROCESS_CLEAN_FILE,
        REPROCESS_CLEAN_PROCESSED_FILES_LIST,
        PROCESS_START,
        PROCESS_NO_TABLE_FOUND,
        PROCESS_ROWS_COUNT,
        PROCESS_FINISH,
        PROCESS_NO_COLUMN_FOUND,
        POST_PROCESS_START,
        POST_PROCESS_FINISH,
        ANALYZE_START,
        ANALYZE_FINISH
    ]