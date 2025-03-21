import pandas as pd

from src.Const.MessageConst import MessageConst
from src.Utils.FileUtils import FileUtils
from src.Utils.PrintUtils import PrintUtils


def post_process_file(file_name: str) -> None:
    PrintUtils.print_line(MessageConst.POST_PROCESS_START, file_name, should_print_hash=True)

    df_csv = pd.read_csv(
        f'{file_name}',
        dtype={
            'X_Value': 'object',
            'Voltage': 'float64',
            'Current': 'float64',
            'Power': 'float64'
        },
    ).sort_values('X_Value')

    df_csv['X_Value'] = pd.to_datetime(df_csv['X_Value'], format='%Y-%m-%d %H:%M:%S.%f')

    if len(df_csv.index) < 2:
        return

    df_with_indexer = pd.DataFrame({
        'idx': pd.date_range(
            df_csv['X_Value'].min(),
            df_csv['X_Value'].max(),
            freq='10min'
        )
    })

    df = pd.merge_asof(
        df_with_indexer,
        df_csv,
        left_on='idx',
        right_on='X_Value',
        direction='forward'
    ).drop(columns='idx').drop_duplicates()

    df.to_csv(
        f'{file_name}',
        mode='w',
        index=False,
        columns=[
            'X_Value',
            'Voltage',
            'Current',
            'Power'
        ]
    )

    PrintUtils.print_line(MessageConst.POST_PROCESS_FINISH)
