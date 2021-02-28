from Tools.files import CsvOpen
from typing import Dict


def csv_to_board(file_path):
    with CsvOpen(file_path, "r") as file:
        data = list(file)
    pass
