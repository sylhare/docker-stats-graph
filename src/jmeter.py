import datetime

import pandas as pd


class Jmeter:
    def __init__(self, output_path):
        self.df = pd.read_csv(output_path, delimiter=",")
        self.df = self.df.iloc[1:]
        self.df["DATE"] = pd.to_datetime(self.df["timeStamp"], unit='ms').apply(lambda x: x - datetime.timedelta(hours=5))

    def latency_avg(self):
        return round(self.df["Latency"].mean(), 3)

    def response_time_avg(self):
        return round(self.df["elapsed"].mean(), 3)

    @staticmethod
    def __to_datetime(timestamp):
        return datetime.datetime.fromtimestamp(timestamp / 1000.0)
