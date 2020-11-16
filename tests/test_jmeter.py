import os
import unittest

from src import ROOT_PATH
from src.jmeter import Jmeter


class ParserTest(unittest.TestCase):

    def setUp(self):
        path = os.path.join(ROOT_PATH, "tests", "resources", "output.jtl")
        print(path)
        self.jm = Jmeter(path)

    def test_latency(self):
        self.assertEqual(38.569, self.jm.latency_avg())

    def test_response_time(self):
        self.assertEqual(77.211, self.jm.response_time_avg())

    def test_conversion_to_datetime(self):
        self.assertEqual(12, self.jm.df["DATE"][1].hour)
        self.assertEqual(49, self.jm.df["DATE"][1].minute)
        self.assertEqual(8, self.jm.df["DATE"][1].second)

    def test_duration(self):
        self.assertEqual(0.15, self.jm.duration_min())

    def test_tps_avg(self):
        self.assertEqual(12.0, self.jm.tps_avg())