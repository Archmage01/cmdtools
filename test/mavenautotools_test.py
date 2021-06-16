import unittest
import sys,os
sys.path.append('../cpptools')
from mavenautotools import *
from pub import *
from pom import Pom


class MyTestCase(unittest.TestCase):
    def test_get_last_version(self):
        test = MavenAutoTools('../resources/pom.xml')
        ret = test.get_last_version("com.utest.cppunit")
        self.assertEqual(ret, '0.0.1')

    def test_get_child_module_pom(self):
        test = MavenAutoTools('../resources/pom.xml')
        ret = test.get_child_module_pom("com.utest.cppunit",'0.0.1')
    
    def test_transform_lib_absolute_address(self):
        test = MavenAutoTools('../resources/pom.xml')

        ret = test.transform_lib_absolute_address("com.utest.cppunit",'0.0.1', "Windows",'pull')
        print(ret)
        self.assertEqual(True, ret['project'].endswith('lib\\Windows\\cppunit.lib'))
        self.assertEqual(True, ret['depository'].endswith('com\\utest\\cppunit\\0.0.1\\cppunit.lib'))

        ret = test.transform_lib_absolute_address("com.utest.cppunit",'0.0.1', "Windows",'push')
        self.assertEqual(True, ret['project'].endswith('lib\\Debug\\cppunit.lib'))
        self.assertEqual(True, ret['depository'].endswith('com\\utest\\cppunit\\0.0.1\\cppunit.lib'))

        ret = test.transform_lib_absolute_address("com.utest.cppunit",'0.0.1', "Linux",'pull')
        self.assertEqual(True, ret['project'].endswith('lib\\Linux\\cppunit.a'))
        self.assertEqual(True, ret['depository'].endswith('com\\utest\\cppunit\\0.0.1\\cppunit.a'))

        ret = test.transform_lib_absolute_address("com.utest.cppunit",'0.0.1', "Linux",'push')
        self.assertEqual(True, ret['project'].endswith('lib\\cppunit.a'))
        self.assertEqual(True, ret['depository'].endswith('com\\utest\\cppunit\\0.0.1\\cppunit.a'))

    def test_transform_pom_absolute_address(self):
        test = MavenAutoTools('../resources/pom.xml')

        ret = test.transform_pom_absolute_address("com.utest.cppunit",'0.0.1', 'pull')
        #print(ret)
        self.assertEqual(True, ret['project'].endswith('\\pom\\pom-com.utest.cppunit-0.0.1.xml'))
        self.assertEqual(True, ret['depository'].endswith('\\com\\utest\\cppunit\\pom.xml'))

        ret = test.transform_pom_absolute_address("com.utest.cppunit",'0.0.1', 'push')
        #print(ret)
        self.assertEqual(True, ret['project'].endswith('pom.xml'))
        self.assertEqual(True, ret['depository'].endswith('\\com\\utest\\cppunit\\pom.xml'))


if __name__ == '__main__':
    unittest.main()
