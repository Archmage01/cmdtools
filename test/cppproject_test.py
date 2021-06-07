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

    @unittest.skip('do not run this case')
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
        #os.rmdir('pom')
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

    @unittest.skip('do not run this case')
    def test_join_change_path(self):
        ret = join_change_path(default_libpath,['lrts','ws','demo'],'2.2.5')
        self.assertEqual(ret, default_libpath+r'\lrts\ws\demo\2.2.5')
        ret = join_change_path(default_libpath, ['lrts', 'ws', 'demo'])
        self.assertEqual(ret, default_libpath + r'\lrts\ws\demo')

    @unittest.skip('do not run this case')
    def test_is_dirs_exists(self):
        ret = is_dirs_exists( join_change_path(default_libpath,['lrts','ws','demo'],'2.2.5'),True)
        self.assertEqual(ret, True )
        #删除目录
        os.chdir(default_libpath)
        os.removedirs('lrts/ws/demo/2.2.5')
        ret = is_dirs_exists( join_change_path(default_libpath,['lrts','ws','demo'],'2.2.5'))
        self.assertEqual(ret, False )

    @unittest.skip('do not run this case')
    def test_is_file_exists(self):
        ret = is_file_exists(join_change_path(default_libpath,['lrts','test.py']),True)
        self.assertEqual(ret, False)
        ret = is_file_exists(join_change_path(default_libpath, ['config.ini']), True)
        self.assertEqual(ret, True)

    @unittest.skip('do not run this case')
    def test_get_last_version(self):
        test = MavenAutoTools('../resources/pom.xml')
        ret  = test.get_last_version( ['lrts','ws'],["demo"])
        self.assertEqual(ret, "9.0.0" )

    @unittest.skip('do not run this case')
    def testpull_transform_libs_path(self):
        test = MavenAutoTools('../resources/pom.xml')
        ret = test.pull_transform_libs_path('lrts.ws.interface','1.0.0')
        print(ret)

    @unittest.skip('do not run this case')
    def test_pull_transform_header_path(self):
        test = MavenAutoTools('../resources/pom.xml')
        ret = test.pull_transform_header_path('lrts.ws.interface','1.0.0')
        print(ret)



    def test_pull_transform_pom_path(self):
        test = MavenAutoTools('../resources/pom.xml')
        ret = test.pull_transform_pom_path('lrts.ws.interface','1.0.0')
        print(ret)
        print("=====================")

    @unittest.skip('do not run this case')
    def test_push_libs_to_repository(self):
        test = MavenAutoTools('../resources/pom.xml')
        test.push_libs_to_repository("lrts.ws.protocol",'1.0.0')

    @unittest.skip('do not run this case')
    def test_push_pom_to_repository(self):
        test = MavenAutoTools('../resources/pom.xml')
        #print("\ncppunit============================start")
        test.push_pom_to_repository("lrts.ws.protocol",'1.0.0')
        #print("cppunit============================end")

    @unittest.skip('do not run this case')
    def test_push_header_to_repository(self):
        test = MavenAutoTools('../resources/pom.xml')
        #print("\ncppunit============================start")
        test.push_header_to_repository("lrts.ws.protocol",'1.0.0')
        #print("cppunit============================end")

    @unittest.skip('do not run this case')
    def test_install_all_interface_files(self):
        test = MavenAutoTools('../resources/pom.xml')
        #print("\ncppunit============================start")
        test.install_all_interface_files()
        #print("cppunit============================end")

    #@unittest.skip('do not run this case')
    def test_repo_dependencys_file(self):
        test = MavenAutoTools('../resources/pom.xml')
        test.repo_dependencys_file()




if __name__ == '__main__':
    unittest.main()
