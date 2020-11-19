import itertools
import re

import matplotlib.pyplot as plt
import pandas as pd

from src import setup_plot


class DockerStats:
    __header_list = ["NAME", "CPU %", "MEM %", "MEM Usage", "NET IO", "BLOCK IO", "PID", "DATE"]
    __category = ["CPU %", "MEM %", "NET INPUT", "NET OUTPUT", "BLOCK INPUT", "BLOCK OUTPUT"]

    def __init__(self, data_path):
        self.df = pd.read_csv(data_path, delimiter=";", names=DockerStats.__header_list)
        self.df["CPU %"] = self.df["CPU %"].apply(self.__percentage_to_float())
        self.df["MEM %"] = self.df["MEM %"].apply(self.__percentage_to_float())
        self.df["MEM Usage"] = self.df["MEM Usage"].apply(lambda value: self.__take_usage(value))
        self.df[["NET INPUT", "NET OUTPUT"]] = self.df["NET IO"].str.split(" / ", expand=True)
        self.df["NET INPUT"] = self.df["NET INPUT"].apply(lambda x: self.__to_float_mb(x))
        self.df["NET OUTPUT"] = self.df["NET OUTPUT"].apply(lambda x: self.__to_float_mb(x))
        self.df[["BLOCK INPUT", "BLOCK OUTPUT"]] = self.df["BLOCK IO"].str.split(" / ", expand=True)
        self.df["BLOCK INPUT"] = self.df["BLOCK INPUT"].apply(lambda x: self.__to_float_mb(x))
        self.df["BLOCK OUTPUT"] = self.df["BLOCK OUTPUT"].apply(lambda x: self.__to_float_mb(x))
        self.df["MEM Usage"] = self.df["MEM Usage"].apply(lambda x: self.__to_float_mb(x))
        self.df.drop(["NET IO", "BLOCK IO"], inplace=True, axis=1)
        self.df["DATE"] = pd.to_datetime(self.df["DATE"])
        setup_plot()

    def plot_category(self, category):
        fig, ax = plt.subplots()
        names = self.df["NAME"].unique()
        self.df.reset_index().groupby('NAME').plot(x='DATE', y=category, ax=ax)
        plt.legend(names, title='apps', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.ylabel(self.__category_label(category))
        plt.xlabel('Time')
        plt.show()

    def plot_category_all(self):
        for category in self.__category:
            self.plot_category(category)

    def duration_min(self):
        delta = self.df["DATE"].iloc[-1] - self.df["DATE"][1]
        return round(delta.total_seconds() / 60, 1)

    @staticmethod
    def __category_label(category):
        if "%" in category:
            add_on = ""
        else:
            add_on = " (MB)"
        return category + add_on

    @staticmethod
    def __percentage_to_float():
        return lambda x: float((x.replace("%", "")))

    @staticmethod
    def __take_usage(value):
        return ''.join(itertools.takewhile(lambda letter: not letter == "/", value))

    @staticmethod
    def __to_float_mb(value):
        multi = 1.0
        value = str(value).upper()
        if "G" in value:
            multi = 1000.0
        elif "K" in value:
            multi = 0.001

        return multi * float("".join(re.findall("[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+", value)))
