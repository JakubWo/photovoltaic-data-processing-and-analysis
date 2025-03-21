import os
from datetime import datetime as dt, timedelta

import numpy as np
import pandas as pd

from src.Config.Config import Config
from src.Const.MessageConst import MessageConst
from src.Utils.FileUtils import FileUtils
from src.Utils.PrintUtils import PrintUtils
from src.Const.FileConst import FileConst


def process_file(file_name: str, configuration: dict) -> None:
    file_path_from_project_root = f'{FileConst.PREPROCESSED_DIR}/{file_name}'

    PrintUtils.print_line(
        MessageConst.PROCESS_START,
        file_path_from_project_root,
        should_print_hash=True
    )

    with open(FileUtils.get_absolute_path(file_path_from_project_root), 'r', encoding='cp1252') as file:
        lines = file.readlines()

    file_table_header_line_number = get_file_table_header_line_number(lines)

    if -1 == file_table_header_line_number:
        PrintUtils.print_line(MessageConst.PROCESS_NO_TABLE_FOUND)
        return

    df = create_dataframe(lines[file_table_header_line_number:])

    count_time(df, lines, configuration, file_path_from_project_root)

    df = df.drop('X_Value', axis=1)
    df = df.rename(columns={'datetime': 'X_Value'})

    df = df.dropna()

    for index, name in enumerate(configuration['samples']):
        if 'skip' == name:
            continue

        if f'Voltage {index + 1}' not in df.columns:
            PrintUtils.print_line(MessageConst.PROCESS_NO_COLUMN_FOUND, index + 1)
            continue

        df_temp = pd.DataFrame().assign(
            X_Value=df['X_Value'],
            Voltage=df[f'Voltage {index + 1}'],
            Current=df[f'Current {index + 1}'],
            Power=df[f'Power {index + 1}']
        )

        if Config.SPLIT_FILES:
            if not os.path.isdir(f'{FileConst.PROCESSED_DIR}/{file_name.split(".")[0]}'):
                os.mkdir(f'{FileConst.PROCESSED_DIR}/{file_name.split(".")[0]}')

            df_temp.to_csv(
                FileUtils.get_absolute_path(f'{FileConst.PROCESSED_DIR}/{file_name.split(".")[0]}/{name}.csv'),
                mode='a',
                index=False,
                columns=[
                    'X_Value',
                    'Voltage',
                    'Current',
                    'Power'
                ]
            )
        else:
            df_temp.to_csv(
                FileUtils.get_absolute_path(f'{FileConst.PROCESSED_DIR}/{name}.csv'),
                mode='a',
                index=False,
                header=os.path.exists(f'{FileConst.PROCESSED_DIR}/{name}.csv') is False,
                columns=[
                    'X_Value',
                    'Voltage',
                    'Current',
                    'Power'
                ]
            )

    PrintUtils.print_line(MessageConst.PROCESS_FINISH)


def get_file_date_and_time(lines: list) -> str:
    date = None
    time = None
    microseconds = "000001"

    for line in lines:
        if "Date\t" in line and date is None:
            date = line.removeprefix("Date\t").removesuffix("\n")

        if "Time\t" in line and time is None:
            time_with_microseconds = line.removeprefix("Time\t").removesuffix("\n")

            time, microseconds = time_with_microseconds.split(
                "," if "," in time_with_microseconds else ".",
                1
            )
            microseconds = microseconds[0:6]

        if date is not None and time is not None:
            break

    if date is None or time is None:
        raise RuntimeError("W pliku nie znaleziono daty i czasu rozpoczęcia pomiaru")

    return "%s %s.%s" % (date, time, microseconds)


def get_file_table_header_line_number(lines: list) -> int:
    for line_number, line in enumerate(lines):
        if "X_Value\tVoltage 1\tCurrent 1\tPower 1\t" in line:
            return line_number

    return -1


def prepare_data_lines(lines: list) -> list:
    return [line.replace("\n", "").replace(",", ".").split("\t") for line in lines]


def create_dataframe(lines: list) -> pd.DataFrame:
    df = pd.DataFrame(prepare_data_lines(lines))
    df.columns = df.iloc[0]

    df = df[1:]
    df = df.drop('Comment', axis=1)
    df = df.reset_index(drop=True)
    df = df.replace('NaN', np.nan)

    for column in df.columns:
        if "X_Value" != column:
            df[column] = df[column].astype(float)

    return df


def count_time(df: pd.DataFrame, lines: list, configuration: dict, file_path_from_project_root: str) -> None:
    date_time = dt.strptime(get_file_date_and_time(lines), '%Y/%m/%d %H:%M:%S.%f')

    if Config.PROCESS_TIME_COUNTING:

        df.at[0, 'datetime'] = date_time

        last_difference = 0
        for i, r in enumerate(df.X_Value, 1):
            if i >= len(df.index):
                break

            current_difference = abs(float(df.at[i, 'X_Value']) - float(df.at[i - 1, 'X_Value']))
            if float(df.at[i, 'X_Value']) != 0:
                last_difference = current_difference

            df.at[i, 'datetime'] = df.at[i - 1, 'datetime'] + timedelta(seconds=last_difference)

    elif Config.TIME_INTERVAL:
        for i, r in enumerate(df.X_Value):
            df.at[i, 'X_Value'] = date_time + timedelta(seconds=(i * configuration['time_interval']))
    else:
        file_last_modified_date_time = dt.fromtimestamp(os.path.getmtime(file_path_from_project_root))
        data_gathering_time_in_seconds = (file_last_modified_date_time - date_time).total_seconds()
        time_between_records = (data_gathering_time_in_seconds / len(df.index))

        for i, r in enumerate(df.X_Value):
            df.at[i, 'X_Value'] = date_time + timedelta(seconds=int(i * time_between_records))


