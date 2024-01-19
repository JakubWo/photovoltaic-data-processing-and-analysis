import os
import shutil

from src.Config.ConfigService import ConfigService

from src.Config.Config import Config
from src.Utils.PrintUtils import PrintUtils
from src.Const import FilenameConst

from src.Process import PostProcessData
from src.Process import ProcessData


def run() -> None:
    if Config.REPROCESS_FILES:
        remove_files(FilenameConst.PROCESSED_PATH)
        with open(FilenameConst.PROCESSED_FILES_LIST, 'w'):
            pass

    with open(FilenameConst.PROCESSED_FILES_LIST, 'a+') as processed_files_list_file:
        processed_files_list_file.seek(0)
        processed_files_list = [
            file_name.replace("\n", "") for file_name in processed_files_list_file.readlines()
        ]

        for file_name, configuration in ConfigService.get_config().items():
            if not configuration['samples']:
                PrintUtils.print_line('file.error.no_config', file_name)
                continue

            if file_name in processed_files_list:
                continue

            ProcessData.process_file(file_name, configuration)
            processed_files_list_file.write(f"{file_name}\n")

    if Config.POST_PROCESS_FILES:
        post_process(FilenameConst.PROCESSED_PATH)


def remove_files(path: str) -> None:
    for file_name in os.listdir(path):
        full_path = f'{path}/{file_name}'

        if os.path.isdir(full_path):
            remove_files(full_path)

        shutil.rmtree(full_path, ignore_errors=True)


def post_process(path: str) -> None:
    for file_name in os.listdir(path):
        full_path = f'{path}/{file_name}'

        _, extension = os.path.splitext(full_path)

        if os.path.isdir(full_path):
            post_process(full_path)
        elif '.csv' == extension:
            PostProcessData.post_process_file(full_path)
