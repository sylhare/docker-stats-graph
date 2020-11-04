import unittest

from src.app import hello


class ParserTest(unittest.TestCase):

    def setUp(self):
        print("\nSet up - Before each test")

    def test_hello_world(self):
        self.assertEqual("Hello World!", hello())

    def tearDown(self):
        print("Tear Down - After each Test\n")


if __name__ == "__main__":
    unittest.main()
