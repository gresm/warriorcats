from Tools import csvH as csv

WALL = "#"
GRASS = "_"
WATER = "-"
NOTHING = "="


def csv_to_board(file_path):
    with csv.Open(file_path, "r") as file:
        pass
