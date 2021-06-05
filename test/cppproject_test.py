import unittest
import sys,os
sys.path.append('../cpptools')
from cppproject import *
from pub import *

class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.rootpath = os.getcwd()

    def tearDown(self) -> None:
        os.chdir(self.rootpath)

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

    def test_join_change_path(self):
        ret = join_change_path(default_libpath,['lrts','ws','demo'],'2.2.5')
        self.assertEqual(ret, default_libpath+r'\lrts\ws\demo\2.2.5')
        ret = join_change_path(default_libpath, ['lrts', 'ws', 'demo'])
        self.assertEqual(ret, default_libpath + r'\lrts\ws\demo')

    def test_is_dirs_exists(self):
        ret = is_dirs_exists( join_change_path(default_libpath,['lrts','ws','demo'],'2.2.5'),True)
        self.assertEqual(ret, True )
        #删除目录
        os.chdir(default_libpath)
        os.removedirs('lrts/ws/demo/2.2.5')
        ret = is_dirs_exists( join_change_path(default_libpath,['lrts','ws','demo'],'2.2.5'))
        self.assertEqual(ret, False )


    def test_is_file_exists(self):
        ret = is_file_exists(join_change_path(default_libpath,['lrts','test.py']),True)
        self.assertEqual(ret, False)
        ret = is_file_exists(join_change_path(default_libpath, ['config.ini']), True)
        self.assertEqual(ret, True)


    def test_get_last_version(self):
        test = MavenAutoTools('../resources/pom.xml')
        ret  = test.get_last_version( ['lrts','ws'],["demo"])
        self.assertEqual(ret, "9.0.0" )

    def test_get_transform_libs_path(self):
        test = MavenAutoTools('../resources/pom.xml')
        ret = test.pull_transform_libs_path('lrts.ws.interface')
        print(ret)



    def test_get_transform_header_path(self):
        test = MavenAutoTools('../resources/pom.xml')
        ret = test.pull_transform_header_path('lrts.ws.interface')
        print(ret)



    def test_get_transform_pom_path(self):
        test = MavenAutoTools('../resources/pom.xml')
        ret = test.pull_transform_pom_path('lrts.ws.interface')
        print(ret)


    def test_push_transform_header_path(self):
        test = MavenAutoTools('../resources/pom.xml')
        ret = test.push_transform_header_path('lrts.ws.interface')


if __name__ == '__main__':
    unittest.main()
