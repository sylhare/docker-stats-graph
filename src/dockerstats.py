import itertools
import re

import pandas as pd


class DockerStats:
    __header_list = ["Name", "CPU %", "MEM %", "MEM Usage", "NET IO", "BLOCK IO", "PID", "DATE"]

    def __init__(self, data_path):
        self.df = pd.read_csv(data_path, delimiter=";", names=DockerStats.__header_list)
        self.df["CPU %"] = self.df["CPU %"].apply(self.__remove_percentage())
        self.df["MEM %"] = self.df["MEM %"].apply(self.__remove_percentage())
        self.df["MEM Usage"] = self.df["MEM Usage"].apply(lambda value: self.__take_usage(value))
        self.df[["NET INPUT", "NET OUTPUT"]] = self.df["NET IO"].str.split(" / ", expand=True)
        self.df["NET INPUT"] = self.df["NET INPUT"].apply(lambda x: self.__to_mb(x))
        self.df["NET OUTPUT"] = self.df["NET OUTPUT"].apply(lambda x: self.__to_mb(x))
        self.df[["BLOCK INPUT", "BLOCK OUTPUT"]] = self.df["BLOCK IO"].str.split(" / ", expand=True)
        self.df["BLOCK INPUT"] = self.df["BLOCK INPUT"].apply(lambda x: self.__to_mb(x))
        self.df["BLOCK OUTPUT"] = self.df["BLOCK OUTPUT"].apply(lambda x: self.__to_mb(x))
        self.df["MEM Usage"] = self.df["MEM Usage"].apply(lambda x: self.__to_mb(x))
        self.df["DATE"] = pd.to_datetime(self.df["DATE"])

    @staticmethod
    def __remove_percentage():
        return lambda x: x.replace("%", "")

    @staticmethod
    def __take_usage(value):
        return ''.join(itertools.takewhile(lambda letter: not letter == "/", value))

    @staticmethod
    def __to_mb(value):
        multi = 1.0
        value = str(value).upper()
        if "G" in value:
            multi = 1000.0
        elif "K" in value:
            multi = 0.001

        return multi * float("".join(re.findall("[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+", value)))
