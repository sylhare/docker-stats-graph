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
        self.df_ms = self.df.copy()
        setup_plot()
        self.df = self.df.set_index('DATE').resample('s')
        self.tps = self.df.count()
        self.df = self.df.mean()

    def latency_avg(self):
        return round(self.df_ms["Latency"].mean(), 3)

    def latency_median(self):
        return round(self.df_ms["Latency"].median(), 3)

    def response_time_avg(self):
        return round(self.df_ms["elapsed"].mean(), 3)

    def duration_min(self):
        delta = self.df["timeStamp"].iloc[-1] - self.df["timeStamp"][1]
        return round(delta / 1000 / 60, 2)

    def tps_avg(self):
        return round(self.tps["timeStamp"].mean())

    def tps_median(self):
        return round(self.tps["timeStamp"].median())

    def plot_success(self):
        self.df_ms["responseMessage"].groupby(self.df_ms["responseMessage"]).count().plot(kind='pie',
                                                                                          autopct='%1.1f%%')
        plt.axis('equal')
        plt.show()

    def plot_label(self):
        self.df_ms["label"].groupby(self.df_ms["label"]).count().plot(kind='pie', autopct='%1.1f%%')
        plt.axis('equal')
        plt.show()

    def plot_latency(self, size=(20, 10)):
        fig, ax = plt.subplots(figsize=size)
        self.df.reset_index().plot(x='DATE', y="Latency", ax=ax)
        ax.legend(["Latency"])
        plt.legend(loc='upper left')
        plt.xlabel('Time')
        plt.ylabel('Latency (ms)')
        plt.show()

    def plot_tps(self):
        fig, ax = plt.subplots(figsize=(20, 10))
        self.tps.plot(y="timeStamp", ax=ax, color='Red')
        plt.legend(loc='upper left')
        ax.legend(["tps"])
        plt.xlabel('Time')
        plt.ylabel('Transaction per seconds')
        plt.show()

    def plot_both(self, size=(10, 5)):
        fig, ax1 = plt.subplots(figsize=size)

        color = 'tab:red'
        ax1.set_xlabel('time')
        ax1.set_ylabel('Latency (ms)', color=color)
        self.df.fillna(0).plot(y="Latency", ax=ax1, color=color, label="latency")
        plt.legend(loc='upper left')
        ax1.tick_params(axis='y', labelcolor=color)

        ax2 = ax1.twinx()
        color = 'tab:blue'
        ax2.set_ylabel('t p s', color=color)  # we already handled the x-label with ax1
        self.df.plot(y="timeStamp", ax=ax2, color=color, label="tps")
        ax2.tick_params(axis='y', labelcolor=color)
        plt.legend(loc='upper right')

        fig.tight_layout()
        plt.show()
