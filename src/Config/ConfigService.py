import yaml

from src.Const.FileConst import FileConst
from src.Utils.FileUtils import FileUtils


class ConfigService:

    @staticmethod
    def get_config() -> dict:
        with open(FileUtils.get_absolute_path(FileConst.CONFIG_FILE), 'r') as config_file:
            config = yaml.safe_load(config_file)

        if not config:
            raise RuntimeError(f'Niepoprawnie skonfigurowany plik {FileConst.CONFIG_FILE}')

        return config['samples_in_file']
