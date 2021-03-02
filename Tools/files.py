import csv
from typing import TextIO, Union, AnyStr as PathLike, Literal, Dict, NoReturn, Tuple


class _IO:

    def __init__(self, name):
        self.__mode = "x"
        self.__name = name

    @property
    def name(self):
        return self.__name

    @property
    def mode(self):
        return self.__mode

    def read(self, *args, **kwargs):
        raise ValueError(f"Mode {self.__mode} can not read")

    def write(self, *args, **kwargs):
        raise ValueError(f"Mode {self.__mode} can not write")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


# CSV file - Coma Separated Values

class CsvOpen:
    modes = Literal["r", "w", "a"]

    def __init__(self, name: Union[TextIO, PathLike], mode: modes):
        self.__mode = mode
        self.name = name

    def __enter__(self):
        if self.__mode == "r":
            if type(self.name) == TextIO:
                return csv.reader(self.name)
            else:
                return csv.reader(open(self.name, mode="r"))
        elif self.__mode == "w":
            if type(self.name) == TextIO:
                return csv.writer(self.name)
            else:
                return csv.writer(open(self.name, mode="w"))
        elif self.__mode == "w+":
            if type(self.name) == TextIO:
                return csv.writer(self.name)
            else:
                return csv.writer(open(self.name, mode="a"))
        else:
            msg = f"Invalid mode {self.__mode}," \
                  " it can be r - read," \
                  " w - write (clean file)," \
                  " a - write (do not clean file, cursor at end)"
            raise ValueError(msg)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


# Properties file

class _PropsIOWriter(_IO):
    modes = Literal["w", "a"]

    def __init__(self, name: PathLike, mode: modes = "w"):
        super(_PropsIOWriter, self).__init__(name)
        self.__mode = mode

    def write(self, data: Dict) -> NoReturn:
        data_l = []
        for key, value in data.items():
            data_l.append(f"{key} = {value}")
        with open(self.name, mode="w") as f:
            f.write("\n".join(data_l))
        return


class _PropsIOReader(_IO):

    def __init__(self, name: PathLike):
        super(_PropsIOReader, self).__init__(name)
        self.__mode = "r"

    def read(self, sep: str = "=", comments: Union[Tuple[str], str] = ("#", "!")):
        if type(comments) == str:
            comments = tuple(comments)

        with open(self.__name) as file:
            data = {}

            for i in file:
                if i[0] not in comments:
                    data.update(dict(*[v.strip() for v in i.split(sep)]))

        return data


class PropsIO:
    modes = Literal["r", "w", "a"]

    def __init__(self, file: Union[TextIO, PathLike], mode: modes):
        self.__file = file
        self.__mode = mode

    def __enter__(self):
        if self.__mode == "r":
            if type(self.__file) == TextIO:
                self.__file.close()
                return _PropsIOReader(self.__file.name)
            else:
                return _PropsIOReader(self.__file)
        elif self.__mode == "w":
            if type(self.__file) == TextIO:
                self.__file.close()
                return _PropsIOWriter(self.__file.name)
            else:
                return _PropsIOWriter(self.__file)
        elif self.__mode == "a":
            if type(self.__file) == TextIO:
                self.__file.close()
                return _PropsIOWriter(self.__file.name, "a")
            else:
                return _PropsIOWriter(self.__file, "a")
        else:
            msg = f"Invalid mode {self.__mode}," \
                  " it can be r - read," \
                  " w - write (clean file)," \
                  " a - write (do not clean file, cursor at end)"
            raise ValueError(msg)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class PropsOpen:
    modes = Literal["r", "w"]

    def __init__(self, file: Union[TextIO, PathLike], mode: modes):
        self.__mode = mode
        self.file = file

    def __enter__(self):
        return PropsIO(self.file, self.__mode)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


__all__ = ["CsvOpen", "PropsOpen", "PropsIO"]
