#!/usr/bin/env python
# -*- coding:utf-8 -*-

from pom import Pom
from pub import *
import os,logging,platform
import template  as tp

class  ManageLibs(object):
    def __init__(self,pompath):
        self.rootpath = os.getcwd()
        self.pom = None
        self.dependencys = None

    def update_pom_info(self,pom):
        '''
        获得pom信息
        '''
        self.pom = Pom(pom)
        return self.pom

    def get_dependencys(self,pom):
        self.dependencys = Pom(pom).dependencies



    def install_local_file(self,groupid_artifactid):
        '''
        安装头文件  库到本地仓库
        '''
        pass

    def repo_dependencys_file(self):
        '''
        拉取本模块依赖的头文件及库
        '''

    def repo_dependency_sigle(self):
        pass





def create_project(project_info:str):
    project_str = project_info
    if project_str.count(r'.') != 2:
        logging.info("project format err like ==> com.lancer.moduelname")
        return
    groupId = ".".join(project_str.split('.')[0:-1:])
    moduelname = project_str.split('.')[-1]
    logging.info("groupId: %s  moduel_name: %s " % (groupId, moduelname))
    # create  file
    create_file(r'CMakeLists.txt', tp.topcmake % ({"prjname": moduelname}))
    create_file(r"src/CMakeLists.txt", tp.src_leve_cmake % ({"prjname": moduelname}))
    # write  cppunit  test file
    create_file(r"src/test_cppunit/%s_test.cpp" % (moduelname), (tp.cppunit_testfile % ({"prjname": moduelname})))
    create_file(r"src/test_cppunit/main_cppunit.cpp", tp.cppunit_testmain)
    # write  cpp/h  src file
    create_file(r"src/main/%s.cpp" % moduelname, tp.cppfile_template)
    create_file(r"src/include/%s.h" % moduelname, tp.hhp_template % ({"prjname": moduelname.upper()}))
    # ftest
    create_file(r"src/ftest/ftest.cpp", tp.cppfile_template_lintcode)
    create_file(r"readme.md", tp.readme_template)
    create_file(r"pom.xml", tp.pom_template % ({"groupId": groupId, "prjname": moduelname}))


class  CppProject(object):
    def __init__(self,pom):
        self.rootpath = os.getcwd()
        #self.pom = Pom(pom)

    def cppproject_init(self):
        new_dir = [r'projects/bdef', r'bin/Debug', r'include', r'pom']
        if "Windows" == platform.system():
            new_dir.append(r'lib/Windows')
        elif "Linux" == platform.system():
            new_dir.append(r'lib/Linux')
        for dir in new_dir:
            make_dirs(dir)
        ###############
        if os.path.exists("pom.xml"):
            os.chdir(self.rootpath)
            ### 拉取依赖库 及头文件
            print("=======================================")
            #pull_local_file(self.pom.dependencies)
            print("=======================================")
            ###
            os.chdir(r'projects/bdef')
            os.system("cmake  ../.. && cd ../..")
        else:
            logging.info("dir not exist pom.xml")

    def cppproject_build(self):
        os.system(r'cmake --build projects/bdef')


    def cppproject_install(self):
        if os.path.exists("pom.xml"):
            #push_local_file()
            print("install files ")
        else:
            logging.info("pom.xml not exist  install fail ")

    def cppproject_utest(self):
        if True == os.path.exists(r'bin/Debug'):
            os.chdir(r'bin/Debug')
            exenames = os.listdir(os.getcwd())
            for name in exenames:
                if name.endswith('.exe') and name.startswith('cppunit') and platform.system() == "Windows":
                    os.system(name)
                    break
                elif name.startswith('t') and platform.system() == "Linux":
                    print("====================Linux====================\n")
                    os.system('./%s' % (name))
                    break
        else:
            logging.info("not find dir bin\Debug ")

    def cppproject_ftest(self):
        if True == os.path.exists(r'bin/Debug'):
            os.chdir(r'bin\Debug')
            exenames = os.listdir(os.getcwd())
            for name in exenames:
                if name.endswith('.exe') and name.startswith('ftest') and platform.system() == "Windows":
                    os.system(name)
                    break
                elif name.startswith('ftest') and platform.system() == "Linux":
                    print("====================Linux====================\n")
                    os.system('./%s' % (name))
                    break
        else:
            logging.info("not find dir bin\Debug ")

    def cppproject_updateversion(self, dst_version):
        logging.info("升级版本号to: %s"%dst_version)

    def  cppproject_clean(self):
        logging.info("clean project file")
        delfile(filepath=os.path.join(os.getcwd(),'bin'))
        delfile(filepath=os.path.join(os.getcwd(),'projects'))
        delfile(filepath=os.path.join(os.getcwd(),'pom'))
        delfile(filepath=os.path.join(os.getcwd(),'lib'))
        delfile(filepath=os.path.join(os.getcwd(),'include'))



if __name__ == '__main__':
    test = CppProject('pom.xml')