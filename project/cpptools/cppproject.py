#!/usr/bin/env python3 
# -*- coding:utf-8 -*-
# Author: Lancer  2020-07-20 12:03

import  logging,os
from    unifwbase import * 
from    pom  import Pom 
import  template  as tp


class  ManageLib(object):
    def __init__(self,pomfile):
        self.pom = Pom("pom.xml")
        self.rootpath = os.getcwd()
        

    def install_local_file(self,groupid_artifactid):
        '''
        安装头文件  库到本地仓库
        '''
        dst_path = default_libpath + "\\" + groupid_artifactid.replace(".", "\\") + "\\"+self.pom.version
        src_lib =   os.getcwd()+"\\"+"lib\\Debug\\%s.lib"%(self.pom.out_lib)
        src_hhp =   os.getcwd()+"\\"+"src\\include\\%s"%(self.pom.out_header[0])
        src_pom =   os.getcwd()+"\\pom.xml"
        dst_lib = dst_path+"\\%s.lib"%(self.pom.out_lib)
        dst_hhp = dst_path+"\\%s"%(self.pom.out_header[0])
        dst_pom = dst_path+"\\%s.pom.xml"%(groupid_artifactid)
        try:
            os.chdir(dst_path)
        except FileNotFoundError:
            copy_file(srcfile=src_lib, dstfile= dst_lib  )
            copy_file(srcfile=src_hhp, dstfile= dst_hhp  )
            copy_file(srcfile=src_pom, dstfile= dst_pom  )
            return 
        file_list = os.listdir(os.getcwd())
        for filename in file_list:
            if os.path.isfile(filename) and filename.endswith('.xml'):
                if True == is_same_file(filename,src_pom ):
                    logging.info("xml is not change")
                else:
                    copy_file(srcfile=src_pom, dstfile= dst_pom  )
                    logging.info("%s install success"%(filename))
            elif os.path.isfile(filename) and filename.endswith('.lib'):
                if True == is_same_file(filename,src_lib ):
                    logging.info("lib %s is not change"%(filename))
                else:
                    copy_file(srcfile=src_lib, dstfile= dst_lib  )
                    logging.info("%s install success"%(filename))
            elif os.path.isfile(filename) and filename.endswith('.h'):
                if True == is_same_file(filename,src_hhp ):
                    logging.info("hhp %s is not change"%(filename))
                else:
                    copy_file(srcfile=src_hhp, dstfile= dst_hhp  )
                    logging.info("%s install success"%(filename))
        os.chdir(self.rootpath)



    def repo_dependency_file(self):
        '''
        拉取本模块依赖的头文件及库
        '''
        print("==repo lib")
        for i in range(len(self.pom.dependencies)):
            if  self.pom.dependencies[i][1] is None:
                self.pom.dependencies[i][1] = get_max_version(self.pom.dependencies[i][0])
            print("== ",self.pom.dependencies[i][0], self.pom.dependencies[i][1])
            if self.pom.dependencies[i][1] is None:
                print("== err %s repo connot find suit version "%(self.pom.dependencies[i][0]))
                continue
            else:
                pass
            ### 拉取pom lib .h文件
            print("------------")
            src_path = default_libpath + "\\" + self.pom.dependencies[i][0].replace(".", "\\") + "\\"+self.pom.dependencies[i][1]
            os.chdir(src_path)
            file_list = os.listdir(os.getcwd())
            #print(file_list)
            for filename in file_list:
                if os.path.isfile(filename) and filename.endswith('.xml'):
                    src_pom = src_path + "\\%s"%(filename)
                    dst_pom = self.rootpath + "\\pom\\%s"%(filename)
                    copy_file(srcfile=src_pom, dstfile= dst_pom  )
                    # print("==src ",src_pom )
                    # print("==to  ",dst_pom )
                elif os.path.isfile(filename) and filename.endswith('.lib'):
                    src_lib = src_path + "\\%s"%(filename)
                    dst_lib = self.rootpath + "\\lib\\Windows\\%s"%(filename)
                    copy_file(srcfile=src_lib, dstfile= dst_lib  )
                    # print("==src ",src_lib )
                    # print("==to  ",dst_lib )
                elif  os.path.isfile(filename) and filename.endswith('.h'):
                    src_hhp = src_path + "\\%s"%(filename)
                    dst_hhp = self.rootpath + "\\include\\%s"%(filename)
                    copy_file(srcfile=src_hhp, dstfile= dst_hhp  )
                    # print("==src ",src_hhp )
                    # print("==to  ",dst_hhp )
            os.chdir(self.rootpath)

class  CppProject(object):
    def __init__(self):
        self.rootpath = os.getcwd()

    def cppproject_create(self,project_str):
        project_str = project_str[0]
        if project_str.count(r'.') != 2:
            logging.info("project format err like ==> com.lancer.moduelname")
            return
        groupId = ".".join(project_str.split('.')[0:-1:])
        moduelname = project_str.split('.')[-1]
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


    def cppproject_init(self,default_cmd=None):
        new_dir = [ r'lib\Windows', r'projects\bdef', r'bin\Debug',r'include',r'pom' ]
        for dir in new_dir:
            make_dirs(dir)
        ###############
        if os.path.exists("pom.xml"):
            os.chdir(self.rootpath)
            ### 拉取依赖库 及头文件
            print("=======================================")
            mglib = ManageLib("pom.xml")
            mglib.repo_dependency_file()
            print("=======================================")
            ###
            os.chdir(r'projects\bdef')
            run_cmd("cmake  ../.. && cd ../..")
        else:
            logging.info("dir not exist pom.xml")



    def cppproject_build(self,default_cmd=None):
        run_cmd(r'cmake --build projects/bdef') 

    def cppproject_install(self,default_cmd=None):
        if os.path.exists("pom.xml"):
            mglib = ManageLib("pom.xml")
            mglib.install_local_file(mglib.pom.groupId_artifactId)
        else:
            logging.info("pom.xml not exist  install fail ")

    def cppproject_utest(self,default_cmd=None):
        if  True == os.path.exists(r'bin\Debug') :
            os.chdir(r'bin\Debug')
            exenames = os.listdir(os.getcwd())
            for name in exenames:
                if name.endswith('.exe') and name.startswith('cppunit'):
                    run_cmd(name)
                    break 
        else:
            logging.info("not find dir bin\Debug ")

    def cppproject_ftest(self,default_cmd=None):
        if  True == os.path.exists(r'bin\Debug') :
            os.chdir(r'bin\Debug')
            exenames = os.listdir(os.getcwd())
            for name in exenames:
                if name.endswith('.exe') and name.startswith('ftest'):
                    run_cmd(name)
                    break 
        else:
            logging.info("not find dir bin\Debug ")

    def cppproject_updateversion(self, to_version):
        logging.info("升级版本号to: %s"%to_version)
        pass

    def  cppproject_clean(self, default_cmd=None):
        logging.info("clean project file")
        delfile(filepath=os.getcwd()+"\\bin")
        delfile(filepath=os.getcwd()+"\\projects")
        delfile(filepath=os.getcwd()+"\\pom")
        delfile(filepath=os.getcwd()+"\\lib")
        delfile(filepath=os.getcwd()+"\\include")




if __name__ == "__main__":
    test = ManageLib("pom.xml")
    test.install_local_file("com.lancer.protocol")