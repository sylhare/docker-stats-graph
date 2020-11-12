import os
import unittest

import pandas as pd

from src import ROOT_PATH
from src.app import hello


class ParserTest(unittest.TestCase):

    def setUp(self):
        print("\nSet up - Before each test")

    def test_hello_world(self):
        self.assertEqual("Hello World!", hello())

    @staticmethod
    def test_open_file():
        """{{.Name}};{{.CPUPerc}};{{.MemPerc}};{{.MemUsage}};{{.NetIO}};{{.BlockIO}};{{.PIDs}}"""
        header_list = ["Name", "CPU %", "MEM %", "MEM Usage", "NET IO", "BLOCK IO", "PID", "DATE"]
        path = os.path.join(ROOT_PATH, "tests", "resources", "data.csv")
        print(path)
        df = pd.read_csv(path, delimiter=";", names=header_list)
        print(df)


    def tearDown(self):
        print("Tear Down - After each Test\n")


if __name__ == "__main__":
    unittest.main()
