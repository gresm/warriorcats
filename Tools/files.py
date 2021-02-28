import csv
from typing import TextIO, Union, AnyStr as PathLike, Literal, List, Dict, NoReturn

modes = Literal["r", "w", "a"]


class CsvOpen:
    modes = Literal["r", "w", "a"]

    def __init__(self, file: Union[TextIO, PathLike], mode: modes):
        self.__mode = mode
        self.file = file

    def __enter__(self):
        if self.__mode == "r":
            if type(self.file) == TextIO:
                return csv.reader(self.file)
            else:
                return csv.reader(open(self.file, mode="r"))
        elif self.__mode == "w":
            if type(self.file) == TextIO:
                return csv.writer(self.file)
            else:
                return csv.writer(open(self.file, mode="w"))
        elif self.__mode == "w+":
            if type(self.file) == TextIO:
                return csv.writer(self.file)
            else:
                return csv.writer(open(self.file, mode="a"))
        else:
            msg = f"Invalid mode {self.__mode}," \
                  " it can be r - read," \
                  " w - write (clean file)," \
                  " a - write (do not clean file, cursor end)"
            raise ValueError(msg)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class _PropsIO:

    def __init__(self):
        self.__mode = "x"

    def read(self, *args, **kwargs):
        raise ValueError(f"Mode {self.__mode} can not read")

    def write(self, *args, **kwargs):
        raise ValueError(f"Mode {self.__mode} can not write")


class _PropsIOw(_PropsIO):

    def __init__(self, file: PathLike):
        super(_PropsIOw, self).__init__()
        self.file = file
        self.__mode = "w"

    # TODO
    def write(self, data: Dict) -> NoReturn:
        pass


class _PropsIOr(_PropsIO):

    def __init__(self, file: PathLike):
        super(_PropsIOr, self).__init__()
        self.file = file
        self.__mode = "r"

    def read(self, sep: str = "=", comments: Union[List[str], str] = "#"):
        if type(comments) == str:
            comments = [comments]

        file = open(self.file)
        data = {}

        for i in file:
            if i[0] not in comments:
                data.update(dict(*[v.strip() for v in i.split(sep)]))

        return data

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class PropsIO:

    def __init__(self, file: Union[TextIO, PathLike], mode: modes):
        self.__mode = mode
        self.file = file

    def __enter__(self):
        if self.__mode == "r":
            if type(self.file) == TextIO:
                self.file.close()
                return _PropsIOr(self.file.name)
            else:
                return _PropsIOr(self.file)
        elif self.__mode == "w":
            if type(self.file) == TextIO:
                self.file.close()
                return _PropsIOw(self.file.name)
            else:
                return _PropsIOw(self.file)
        else:
            msg = f"Invalid mode {self.__mode}, it can be r - read or w - write"
            raise ValueError(msg)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class PropsOpen:

    def __init__(self, file: Union[TextIO, PathLike], mode: modes):
        self.__mode = mode
        self.file = file

    def __enter__(self):
        return PropsIO(self.file, self.__mode)
