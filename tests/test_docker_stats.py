import os
import unittest

from src import ROOT_PATH
from src.dockerstats import DockerStats


class ParserTest(unittest.TestCase):

    def setUp(self):
        path = os.path.join(ROOT_PATH, "tests", "resources", "data.csv")
        self.ds = DockerStats(path)

    def test_dataframe_creation(self):
        self.assertFalse(0 == len(self.ds.df.values))
        self.assertFalse(0 == len(self.ds.df.keys()))

    def test_no_percentage(self):
        self.assertTrue(isinstance(self.ds.df["CPU %"][1], float))
        self.assertTrue(isinstance(self.ds.df["MEM %"][1], float))

    def test_separate_io(self):
        self.assertEqual(106.0, self.ds.df["NET INPUT"][0])
        self.assertEqual(2.17, self.ds.df["NET OUTPUT"][0])
        self.assertEqual(0.262, self.ds.df["BLOCK INPUT"][0])
        self.assertEqual(2.14, self.ds.df["BLOCK OUTPUT"][0])

    def test_mem_conversion_to_mb(self):
        self.assertTrue(isinstance(self.ds.df["MEM Usage"][1], float))
        self.assertEquals(7.465, self.ds.df["MEM Usage"][0])
        self.assertEquals(7465, self.ds.df["MEM Usage"][2])
        self.assertEquals(0.007465, self.ds.df["MEM Usage"][3])
        self.assertEquals(465, self.ds.df["MEM Usage"][1])

    def test_io_conversion_to_mb(self):
        self.assertTrue(isinstance(self.ds.df["NET OUTPUT"][1], float))
        self.assertTrue(isinstance(self.ds.df["NET INPUT"][1], float))
        self.assertTrue(isinstance(self.ds.df["BLOCK OUTPUT"][1], float))
        self.assertTrue(isinstance(self.ds.df["BLOCK INPUT"][1], float))

    def test_conversion_to_datetime(self):
        self.assertEqual(22, self.ds.df["DATE"][0].hour)
        self.assertEqual(36, self.ds.df["DATE"][0].minute)
        self.assertEqual(29, self.ds.df["DATE"][0].second)

    def test_duration_min(self):
        self.assertEquals(1, self.ds.duration_min())


if __name__ == "__main__":
    unittest.main()
