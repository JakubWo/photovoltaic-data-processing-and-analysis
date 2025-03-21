import os
import pandas as pd

import matplotlib.pyplot as plt

from src.Const.MessageConst import MessageConst
from src.Utils.PrintUtils import PrintUtils

PROCESSED_DIR = r'./data/processed'
PLOT_PATH = r'./data/plot'


def run():
    for file_name in os.listdir(PROCESSED_DIR):
        process_file(file_name)


def process_file(file_name: str) -> None:
    PrintUtils.print_line(MessageConst.ANALYZE_START, file_name, should_print_hash=True)

    df = pd.read_csv(
        f'{PROCESSED_DIR}/{file_name}',
        dtype={
            'X_Value': 'str',
            'Voltage': 'float64',
            'Current': 'float64',
            'Power': 'float64'
        },
        parse_dates=['X_Value']
    )

    sample_plot_directory = f'{PLOT_PATH}/{file_name.split(".")[0]}'

    if os.path.exists(f'{sample_plot_directory}') is False:
        os.mkdir(f'{sample_plot_directory}')

    create_plot(df['X_Value'], df['Voltage'], 'Voltage', sample_plot_directory)
    create_plot(df['X_Value'], df['Current'], 'Current', sample_plot_directory)
    create_plot(df['X_Value'], df['Power'], 'Power', sample_plot_directory)

    PrintUtils.print_line(MessageConst.ANALYZE_FINISH)


def create_plot(x, y, name: str, plot_directory: str) -> None:
    plt.xlabel('DateTime')
    plt.ylabel(name)
    plt.xticks(rotation=45, ha='right')

    plt.plot(x, y, marker='o', linestyle='')
    plt.savefig(f'{plot_directory}/{name.lower()}.png')
    plt.clf()

