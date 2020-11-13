import itertools

import pandas as pd


class DockerStats:
    __header_list = ["Name", "CPU %", "MEM %", "MEM Usage", "NET IO", "BLOCK IO", "PID", "DATE"]

    def __init__(self, data_path):
        self.df = pd.read_csv(data_path, delimiter=";", names=DockerStats.__header_list)
        self.df["CPU %"] = self.df["CPU %"].apply(self.__remove_percentage())
        self.df["MEM %"] = self.df["MEM %"].apply(self.__remove_percentage())
        self.df["MEM Usage"] = self.df["MEM Usage"].apply(lambda value: self.__take_usage(value))
        self.df[["NET INPUT", "NET OUTPUT"]] = self.df["NET IO"].str.split(" / ", expand=True)
        self.df[["BLOCK INPUT", "BLOCK OUTPUT"]] = self.df["BLOCK IO"].str.split(" / ", expand=True)

    @staticmethod
    def __remove_percentage():
        return lambda x: x.replace("%", "")

    @staticmethod
    def __take_usage(value):
        return ''.join(itertools.takewhile(lambda letter: not letter == "/", value))
