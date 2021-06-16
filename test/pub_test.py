import unittest
import sys,os
sys.path.append('../cpptools')
from cppproject import *
from pub import *


class MyTestCase(unittest.TestCase):
    def test_path_join(self):
        ret = path_join(r"D:\code\python",'cmdtools',"cpptools")
        print(ret)
        if os.path.exists(ret):
            pass
        else:
            print(ret,"不存在")
        os.chdir(ret)
        print(os.getcwd())
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
