import unittest
import sys,os
sys.path.append('../cpptools')
from cppproject import *
from pub import *

class MyTestCase(unittest.TestCase):
    def test_cppproject_init(self):
        test = CppProject('../resources/pom.xml')
        test.cppproject_init()
        self.assertEqual(True, os.path.exists('projects/bdef'))
        self.assertEqual(True, os.path.exists('bin/Debug'))
        self.assertEqual(True, os.path.exists('include'))
        self.assertEqual(True, os.path.exists('pom'))
        self.assertEqual(True, os.path.exists('lib/Windows'))
        #del dir
        os.removedirs('projects/bdef')
        os.removedirs('bin/Debug')
        os.rmdir('include')
        os.rmdir('pom')
        os.removedirs('lib/Windows')

    def test_create_project(self):
        pass
        # create_project("com.leetcode.demo")
        # self.assertEqual(True, os.path.exists('pom.xml'))
        # self.assertEqual(True, os.path.exists('readme.md'))
        # self.assertEqual(True, os.path.exists('CMakeLists.txt'))
        # delfile(filepath=os.path.join(os.getcwd(),'projects'))
        # delfile(filepath=os.path.join(os.getcwd(),'pom'))
        # delfile(filepath=os.path.join(os.getcwd(),'lib'))
        # delfile(filepath=os.path.join(os.getcwd(),'include'))

    def test_get_dependencys(self):
        test = ManageLibs('../resources/pom.xml')
        test.get_dependencys('../resources/pom.xml')

if __name__ == '__main__':
    unittest.main()
