import unittest
import sys,os
sys.path.append('../cpptools')
from cppproject import *
from pub import *


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
