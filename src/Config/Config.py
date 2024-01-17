class Config:
    PROCESS_FILES = False
    PROCESS_TIME_COUNTING = False
    REPROCESS_FILES = False
    POST_PROCESS_FILES = False
    SPLIT_FILES = False

    TIME_INTERVAL = False

    ANALYZE_DATA = False

    ENABLE_PRINTING = False

    @staticmethod
    def validate_configuration() -> None:
        if Config.PROCESS_TIME_COUNTING is True and Config.TIME_INTERVAL is True:
            raise RuntimeError('Skonfigurowano więcej niż jeden sposób obliczania czasu.')


