# -*- encoding: utf-8 -*-
#@File    : corecpp.py
#@Time    : 2020/6/19 22:15
#@Author  : Lancer

import  sys,os,re
import  logging
import  template_file as tp
from    util import *
from    pom  import Pom
from    repo  import  ManageLib
from    config  import * 

logging.basicConfig(level=logging.INFO, format='%(message)s')

class UserCmdmap(object):
    def __init__(self):
        self.cmddict = {}

    def usr_addcmd(self, key, value ):
        self.cmddict[key] = value

    def  usr_delcmd(self,key):
        del(self.cmddict[key])

    def  do_cmd(self, cmdstr):
        #logging.info("cmdstr: %s"%(cmdstr))
        try:
            self.cmddict[cmdstr[0]](" ".join(cmdstr[1:]))
        except NameError as e:
            logging.info("expect function: dict=> %s not define"%cmdstr.strip())
        except KeyError as e:
            logging.info("cmd: [ %s ] not in keys"%(cmdstr.strip() ))
        # except Exception:
        #     print("cmd err")
        #     for cmd in self.cmddict.keys():
        #         print("cmd ==> %s"%(cmd))


class  CppTools(UserCmdmap):
    def __init__(self,*args):
        super(CppTools, self).__init__()
        self.rootpath = os.getcwd()
        self.usr_addcmd("create", self.create_cpp_project)
        self.usr_addcmd("init", self.init_project)
        self.usr_addcmd("build", self.build_project)
        self.usr_addcmd("install", self.install_project)
        self.usr_addcmd("utest", self.utest_project)
        self.usr_addcmd("ftest", self.ftest_project)
        self.do_cmd(list(args[0]))

    def init_project(self, args):
        ## repo .h  and .lib
        logging.info(args)
        version_dict = {
            "vs12":  "-G \"Visual Studio 11 2012\"" , #-G "Visual Studio 11 2012"
            "vs13":  "-G \"Visual Studio 12 2013\"" , #-G "Visual Studio 12 2013"
            "vs15":  "-G \"Visual Studio 14 2015\"" , #-G "Visual Studio 14 2015"
            "vs17":  "-G \"Visual Studio 15 2017\"" , #-G "Visual Studio 15 2017"
            "vs19":  "-G \"Visual Studio 16 2019\"" , #-G "Visual Studio 16 2019"
        }
        if os.path.exists("pom.xml"):
            make_dirs("lib\Windows")
            make_dirs(r'projects\bdef')
            make_dirs(r'bin\Debug')
            make_dirs(r'include')
            #  拉取依赖的子模块lib 库和头文件
            managelib  = ManageLib("pom.xml")
            logging.info("start repo moduel .lib or .h")
            managelib.repo_files()
            logging.info("end repo moduel .lib or .h\n")
            os.chdir(self.rootpath)
            os.chdir(r'projects\bdef')
            if args:
                if args in version_dict.keys():
                    cmd = 'cmake  ../.. %s && cd ../..'%(version_dict[args])
                    run_cmd(cmd) 
            else:
                run_cmd("cmake  ../.. && cd ../..")
        else:
            logging.info("dir not exist pom.xml")

    def build_project(self, args):
        run_cmd(r'cmake --build projects/bdef') 

    def install_project(self, args):
        if os.path.exists("pom.xml"):
            managelib  = ManageLib("pom.xml")
            ###  安装输出文件到本地仓库
            managelib.install_files()
        else:
            logging.info("pom.xml not exist  install fail ")


    def utest_project(self, args):
        if  True == os.path.exists(r'bin\Debug') :
            os.chdir(r'bin\Debug')
            exenames = os.listdir(os.getcwd())
            for name in exenames:
                if name.endswith('.exe') and name.startswith('cppunit'):
                    run_cmd(name)
                    break 
        else:
            logging.info("not find dir bin\Debug ")

    def ftest_project(self, args):
        if  True == os.path.exists(r'bin\Debug') :
            os.chdir(r'bin\Debug')
            exenames = os.listdir(os.getcwd())
            for name in exenames:
                if name.endswith('.exe') and name.startswith('ftest'):
                    run_cmd(name)
                    break 
        else:
            logging.info("not find dir bin\Debug ")

    def create_cpp_project(self, args ):
        print(args)
        if args.count(r'.') != 2:
            logging.info("project format err like ==> com.lancer.moduelname")
            return
        groupId = ".".join(args.split('.')[0:-1:])
        moduelname = args.split('.')[-1]
        logging.info("groupId: %s  moduel_name: %s "%(groupId,moduelname ))
        # create  file
        create_file(r'CMakeLists.txt', tp.topcmake%({"prjname": moduelname }) )
        create_file(r"src\CMakeLists.txt",tp.src_leve_cmake%({"prjname": moduelname }))
        # write  cppunit  test file
        create_file(r"src\test_cppunit\%s_test.cpp"%(moduelname)  ,(tp.cppunit_testfile%({"prjname": moduelname })) )
        create_file(r"src\test_cppunit\main_cppunit.cpp",  tp.cppunit_testmain )
        # write  cpp/h  src file
        create_file(r"src\main\%s.cpp" %moduelname, tp.cppfile_template)
        create_file(r"src\include\%s.h" % moduelname, tp.hhp_template % ({"prjname": moduelname.upper() }))
        # ftest
        create_file(r"src\ftest\ftest.cpp", tp.cppfile_template_lintcode)
        create_file(r"readme.md", tp.readme_template)
        create_file(r"pom.xml", tp.pom_template%({ "groupId": groupId,"prjname": moduelname }) )


if __name__ == '__main__':
    test = CppTools(sys.argv[1:])



# def test01(*args):
#     print("------------------")
#
# test = UserCmdmap()
# print(test.usr_addcmd("init", test01 ))
# test.do_cmd("init")