import yaml

from src.Const import FilenameConst


class ConfigService:

    @staticmethod
    def get_config() -> dict:
        with open(FilenameConst.CONFIG_FILE, 'r') as config_file:
            config = yaml.safe_load(config_file)

        if not config:
            raise RuntimeError(f'Niepoprawnie skonfigurowany plik {FilenameConst.CONFIG_FILE}')

        return config['samples_in_file']
