import pandas as pd


class DockerStats:
    __header_list = ["Name", "CPU %", "MEM %", "MEM Usage", "NET IO", "BLOCK IO", "PID", "DATE"]

    def __init__(self, data_path):
        self.df = pd.read_csv(data_path, delimiter=";", names=DockerStats.__header_list)
        self.df["CPU %"] = self.df["CPU %"].apply(self.__remove_percentage())
        self.df["MEM %"] = self.df["MEM %"].apply(self.__remove_percentage())

    @staticmethod
    def __remove_percentage():
        return lambda x: x.replace("%", "")
