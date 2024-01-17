import pandas as pd

from src.Utils.PrintUtils import PrintUtils


def post_process_file(file_name: str) -> None:
    PrintUtils.print_line('file.postprocess.start', file_name, should_print_hash=True)

    df_csv = pd.read_csv(
        f'{file_name}',
        dtype={
            'X_Value': 'str',
            'Voltage': 'float64',
            'Current': 'float64',
            'Power': 'float64'
        },
        parse_dates=['X_Value']
    ).sort_values('X_Value')

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

    PrintUtils.print_line('file.postprocess.finish')
