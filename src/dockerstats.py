import itertools
import re

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FuncAnimation

from src import setup_plot


class DockerStats:
    __header_list = ["NAME", "CPU %", "MEM %", "MEM Usage", "NET IO", "BLOCK IO", "PID", "DATE"]
    __category = ["CPU %", "MEM %", "NET INPUT", "NET OUTPUT", "BLOCK INPUT", "BLOCK OUTPUT"]

    def __init__(self, data_path):
        setup_plot()
        self.data_path = data_path
        self.load_data()

    def load_data(self):
        self.df = pd.read_csv(self.data_path, delimiter=";", names=DockerStats.__header_list)
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

    def prep_fix_and_ax(self, size):
        self.fig, self.ax = plt.subplots(figsize=size)

        # Leave more space for the legend
        plt.subplots_adjust(right=0.7)

    def plot_category(self, category, size=(10, 5)):
        self.prep_fix_and_ax(size=size)
        self._do_plot_category(category=category)
        plt.show()

    def plot_category_live(self, category, size=(10, 5), update_interval_ms=10000):

        self.prep_fix_and_ax(size=size)
        self._do_plot_category(category=category)

        def _update(_):
            # In lieu of something clever that updates the data in each of `self.ax.get_lines()`
            # instead just clear and re-plot the whole thing which is fine for slow refresh rates
            self.load_data()
            self.ax.clear()
            self._do_plot_category(category=category)

        animation = FuncAnimation(self.fig, _update, interval=update_interval_ms, cache_frame_data=False)
        plt.show()


    def _do_plot_category(self, category):
        names = self.df["NAME"].unique()
        self.df.reset_index().groupby('NAME').plot(x='DATE', y=category, ax=self.ax, marker="+")

        # groupby sorts the names so this is necessary too in order for the legend to be in the right order
        names.sort()
        plt.legend(names, title='apps', bbox_to_anchor=(1.05, 1), loc='upper left')

        plt.ylabel(self.__category_label(category))
        plt.xlabel('Time')
        plt.grid(alpha=0.5)

    def plot_category_all(self):
        for category in self.__category:
            self.plot_category(category)

    def mean_for_apps(self):
        return self.df.groupby(['NAME']).mean().apply(lambda x: round(x,2))

    def duration_min(self):
        delta = self.df["DATE"].iloc[-1] - self.df["DATE"][1]
        return round(delta.total_seconds() / 60, 1)

    def cpu_avg(self):
        return round(self.df["CPU %"].mean(), 2)

    def memory_avg(self):
        return round(self.df["MEM %"].mean(), 2)

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
