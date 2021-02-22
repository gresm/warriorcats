from Tools import csvH as csv
from typing import Dict


data: Dict[str, str] = {
    "WALL": "#",
    "GRASS": "_",
    "WATER": "-",
    "NONE": "="
}


def csv_to_board(file_path):
    with csv.Open(file_path, "r") as file:
        pass
