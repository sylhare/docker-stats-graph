import os
import unittest

from src import ROOT_PATH
from src.jmeter import Jmeter


class ParserTest(unittest.TestCase):

    def setUp(self):
        path = os.path.join(ROOT_PATH, "tests", "resources", "output.csv")
        print(path)
        self.jm = Jmeter(path)

    def test_latency(self):
        self.assertEqual(38.569, self.jm.latency_avg())

    def test_response_time(self):
        self.assertEqual(77.211, self.jm.response_time_avg())

    def test_conversion_to_datetime(self):
        print(self.jm.df["DATE"])
        print(self.jm.df["DATE"][1])

        # self.assertEqual(22, self.jm.df["DATE"][0].hour)
        # self.assertEqual(36, self.jm.df["DATE"][0].minute)
        # self.assertEqual(29, self.jm.df["DATE"][0].second)
