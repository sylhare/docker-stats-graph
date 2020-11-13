import os
import unittest

from src import ROOT_PATH
from src.dockerstats import DockerStats


class ParserTest(unittest.TestCase):

    def setUp(self):
        path = os.path.join(ROOT_PATH, "tests", "resources", "data.csv")
        print(path)
        self.ds = DockerStats(path)

    def test_dataframe_creation(self):
        self.assertFalse(0 == len(self.ds.df.values))
        self.assertFalse(0 == len(self.ds.df.keys()))
        print(self.ds.df)

    def test_no_percentage(self):
        self.assertTrue("%" not in self.ds.df["CPU %"][1], "% should not be in " + self.ds.df["CPU %"][1])
        self.assertTrue("%" not in self.ds.df["MEM %"][1], "% should not be in " + self.ds.df["MEM %"][1])

    def test_only_usage(self):
        self.assertTrue("/" not in self.ds.df["MEM Usage"][1], "Only usage value in " + self.ds.df["MEM Usage"][1])

    def test_separate_io(self):
        self.assertEqual("106MB", self.ds.df["NET INPUT"][0])
        self.assertEqual("2.17MB", self.ds.df["NET OUTPUT"][0])
        self.assertEqual("262kB", self.ds.df["BLOCK INPUT"][0])
        self.assertEqual("2.14MB", self.ds.df["BLOCK OUTPUT"][0])


if __name__ == "__main__":
    unittest.main()
