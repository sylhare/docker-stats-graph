import datetime

import matplotlib.pyplot as plt
import pandas as pd

from src import setup_plot


class Jmeter:
    def __init__(self, output_path):
        self.df = pd.read_csv(output_path, delimiter=",")
        self.df = self.df.iloc[1:]
        self.df["DATE"] = pd.to_datetime(self.df["timeStamp"], unit='ms').apply(
            lambda x: x - datetime.timedelta(hours=5))
        setup_plot()
        self.dt = self.df.set_index('DATE').resample('s')
        self.tps = self.dt.count()

    def latency_avg(self):
        return round(self.df["Latency"].mean(), 3)

    def response_time_avg(self):
        return round(self.df["elapsed"].mean(), 3)

    def duration_min(self):
        delta = self.df["timeStamp"].iloc[-1] - self.df["timeStamp"][1]
        return round(delta / 1000 / 60, 2)

    def tps_avg(self):
        return self.tps["timeStamp"].mean()

    def plot_success(self):
        self.df["responseMessage"].groupby(self.df["responseMessage"]).count().plot(kind='pie', autopct='%1.1f%%')
        plt.axis('equal')
        plt.show()

    def plot_latency(self):
        fig, ax = plt.subplots()
        self.df.reset_index().plot(x='DATE', y="Latency", ax=ax)
        plt.xlabel('Time')
        plt.xlabel('Latency ms')
        plt.show()

    def plot_tps(self):
        fig, ax = plt.subplots()
        self.tps.plot(y="timeStamp", ax=ax)
        ax.legend(["tps"])
        plt.show()

    def plot_both(self):
        fig, ax1 = plt.subplots()

        color = 'tab:red'
        ax1.set_xlabel('time')
        ax1.set_ylabel('Latency (ms)', color=color)
        self.dt.mean().fillna(0).plot(y="Latency", ax=ax1, color=color, label="latency")
        plt.legend(loc='upper left')
        ax1.tick_params(axis='y', labelcolor=color)

        ax2 = ax1.twinx()
        color = 'tab:blue'
        ax2.set_ylabel('t p s', color=color)  # we already handled the x-label with ax1
        self.dt.count().plot(y="timeStamp", ax=ax2, color=color, label="tps")
        ax2.tick_params(axis='y', labelcolor=color)
        plt.legend(loc='upper right')

        fig.tight_layout()
        plt.show()

    @staticmethod
    def __to_datetime(timestamp):
        return datetime.datetime.fromtimestamp(timestamp / 1000.0)
