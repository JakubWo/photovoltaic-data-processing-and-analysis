import os

from src.Config.Config import Config
from src.Config.ConfigService import ConfigService
from src.Const.FileConst import FileConst
from src.Const.MessageConst import MessageConst
from src.Process import PostProcessData
from src.Process import ProcessData
from src.Utils.FileUtils import FileUtils
from src.Utils.PrintUtils import PrintUtils


def run() -> None:
    if Config.REPROCESS_FILES:
        PrintUtils.print_line(MessageConst.REPROCESS_CLEAN_FILES_START, should_print_hash=True)

        remove_files(FileUtils.get_absolute_path(FileConst.PROCESSED_DIR))
        with open(FileUtils.get_absolute_path(FileConst.PROCESSED_FILES_LIST_FILE), 'w'):
            PrintUtils.print_line(MessageConst.REPROCESS_CLEAN_PROCESSED_FILES_LIST)
            pass

    with open(FileUtils.get_absolute_path(FileConst.PROCESSED_FILES_LIST_FILE), 'a+') as processed_files_list_file:
        processed_files_list_file.seek(0)
        processed_files_list = [
            file_name.replace("\n", "") for file_name in processed_files_list_file.readlines()
        ]

        for file_name, configuration in ConfigService.get_config().items():
            if not configuration['samples']:
                PrintUtils.print_line(MessageConst.ERROR_NO_CONFIG, file_name)
                continue

            if file_name in processed_files_list:
                continue

            ProcessData.process_file(file_name, configuration)
            processed_files_list_file.write(f"{file_name}\n")

    if Config.POST_PROCESS_FILES:
        post_process(FileUtils.get_absolute_path(FileConst.PROCESSED_DIR))


def remove_files(absolute_path: str) -> None:
    for file_name in os.listdir(absolute_path):
        if file_name == '.gitkeep':
            continue

        full_path = f'{absolute_path}/{file_name}'

        if os.path.isdir(full_path):
            remove_files(full_path)
            os.rmdir(full_path)
            continue

        PrintUtils.print_line(MessageConst.REPROCESS_CLEAN_FILE, full_path)
        os.remove(full_path)


def post_process(path: str) -> None:
    for file_name in os.listdir(path):
        full_path = f'{path}/{file_name}'

        _, extension = os.path.splitext(full_path)

        if os.path.isdir(full_path):
            post_process(full_path)
        elif '.csv' == extension:
            PostProcessData.post_process_file(full_path)
