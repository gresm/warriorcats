import csv


class Open:

    def __init__(self, file_path, mode):
        self.__mode = mode
        self.file_path = file_path

    def __enter__(self):
        if self.__mode == "r":
            return csv.reader(open(self.file_path))
        elif self.__mode == "w":
            return csv.writer(open(self.file_path))

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
