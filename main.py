from src.Process import Process
from src import AnalyzeData

from src.Config.Config import Config


if __name__ == '__main__':
    try:
        # Do przerzucenia do pliku .yaml i tutaj tylko pobieranie tego za pomocą ConfigService
        Config.PROCESS_FILES = True
        Config.REPROCESS_FILES = True
        Config.POST_PROCESS_FILES = True
        Config.SPLIT_FILES = False
  
        Config.PROCESS_TIME_COUNTING = True
        Config.TIME_INTERVAL = False

        Config.ANALYZE_DATA = False
        Config.ENABLE_PRINTING = True

        Config.validate_configuration()

        if Config.PROCESS_FILES:
            Process.run()

        if Config.ANALYZE_DATA:
            AnalyzeData.run()

    except RuntimeError as error:
        print(error)
