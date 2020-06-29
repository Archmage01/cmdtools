#!/usr/bin/env python3 
# -*- coding:utf-8 -*-
# Author: Lancer  2020-05-15 13:48:41
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import os, sys, re,shutil,getpass
import  template as tp
from basetools import  run_cmd 
from  readpom import  ParsePom



class CppProject(object):
    def __init__(self,args):
        self.root_path = os.getcwd()
        self.paaser_cppproject_cmd(args)
        self.project_name = ""

    def paaser_cppproject_cmd(self, args):
        cmd_dict = {
            self.project_init : "init",
            self.project_build: "build",
            self.project_utest: "utest",
            self.project_clean: "clean",
            self.project_install: "install",
            
        }

        for key,value in cmd_dict.items():
            if args[0] == value :
                #print(key, value)
                run_cmd({ key:args[1:]})

        if 2 == len(args):
            if args[0] == "create":
                if  args[1] == "leetcode":
                    self.create_leetcode_project()
                else:
                    self.project_name = args[1]
                    self.create_normal_project()
        else:
            pass

    def  write_file(self,  file_path, template_str):
        """
        create new  file
        """
        filename = ""
        create_path = ""
        file_path = file_path.split("\\")
        if 1 == len(file_path):
            filename = file_path[0]
        else:
            filename = file_path[-1]
            file_path.pop()
            create_path = "\\".join(file_path)
            if  False ==   os.path.exists(create_path):
                os.makedirs(create_path)
            os.chdir(create_path)
        with  open(filename,mode="w",encoding='utf-8') as file:
            file.write(template_str)
            file.close()
            os.chdir(self.root_path)

    def create_normal_project(self):
        if not os.listdir(os.getcwd()):
            if 0 == len(self.project_name):
                print("cmd err: no  project name: create projectname")
                return
            #write CMakeList.txt file
            projectname = {"prjname": self.project_name }
            up_projectname = {"prjname": self.project_name.upper() }
            self.write_file(r"CMakeLists.txt",  tp.topcmake%(projectname) )
            self.write_file(r"src\CMakeLists.txt",  tp.src_leve_cmake%(projectname) )
            #write  cppunit  test file
            self.write_file(r"src\test_cppunit\%s_test.cpp"%(self.project_name)  ,(tp.cppunit_testfile%(projectname)) )
            self.write_file(r"src\test_cppunit\main_cppunit.cpp",  tp.cppunit_testmain )
            #write  cpp/h  src file
            self.write_file( r"src\main\%s.cpp"%self.project_name,tp.cppfile_template )
            self.write_file( r"src\include\%s.h"%self.project_name, tp.hhp_template%(up_projectname))
            #ftest
            self.write_file( r"src\ftest\ftest.cpp",tp.cppfile_template_lintcode )
            self.write_file( r"readme.md",tp.readme_template )
            self.write_file( r"pom.xml",tp.pom_template )
        else:
            print("dir not  empty  please  create in empty dir")


    def create_leetcode_project(self):
        self.project_name = "Solution"
        #if not os.listdir(os.getcwd()):
        if True:
            projectname = {"prjname": self.project_name }
            self.write_file(r"CMakeLists.txt",  tp.topcmake%(projectname) )
            self.write_file(r"src\CMakeLists.txt",  tp.leetcode_cmake )
            #write  cpp/h  src file
            self.write_file( r"src\main\%s.cpp"%self.project_name,tp.cppfile_template_lintcode )

    
    def project_init(self, args):
        version_dict = {
            "vs12":  "-G \"Visual Studio 11 2012\"" , #-G "Visual Studio 11 2012"
            "vs13":  "-G \"Visual Studio 12 2013\"" , #-G "Visual Studio 12 2013"
            "vs15":  "-G \"Visual Studio 14 2015\"" , #-G "Visual Studio 14 2015"
            "vs17":  "-G \"Visual Studio 15 2017\"" , #-G "Visual Studio 15 2017"
            "vs19":  "-G \"Visual Studio 16 2019\"" , #-G "Visual Studio 16 2019"
        }
        print(args)
        if False == os.path.exists("lib"):
            os.mkdir("lib")
        if True == os.path.exists("projects"):
            pass
        else:
            os.mkdir("projects")
        try:
            os.makedirs("bin/Debug")
        except Exception:
            pass
        os.chdir("projects")
        if args:
            if args[0] in version_dict.keys():
                cmd = "cmake  .. %s && cd .."%(version_dict[args[0]])
                run_cmd(cmd) 
        else:
            run_cmd("cmake  .. && cd ..")


    def project_build(self,*args):
        if False == os.path.exists("target"):
            os.mkdir("target")
        else:
            os.chdir("target")
            ls = os.listdir(os.getcwd())
            for i in ls:
                c_path = os.path.join(os.getcwd(), i)
                if os.path.isdir(c_path):
                    pass
                else:
                    os.remove(c_path)
        os.chdir(self.root_path)
        if False == os.path.exists("bin"):
            os.makedirs("bin/Debug")

        os.system("cmake --build projects    ")
        if True == os.path.exists("bin"):
            os.chdir("bin/Debug")
            print("chdir>> ", os.getcwd())
            names = os.listdir(os.getcwd())
            for name in names:
                #if name.endswith('.lib') or name.endswith('.exe') or name.endswith('.a') or name.endswith('.dll') or name.endswith('.ilk') or name.endswith('.pdb') :
                if  name.endswith('.exe'):
                    shutil.copy(name, self.root_path + "\\target")
                if  name.endswith('.lib'):
                    shutil.copy(name, self.root_path + "\\lib")

    def project_utest(self,*args):
        print("\n")
        if  True == os.path.exists("bin") :
            os.chdir("bin/Debug")
            if True == os.path.exists("t_Solution.exe") :
                os.system("t_Solution.exe")
                return
            else:
                os.chdir(self.root_path)
        if True == os.path.exists("bin"):
            os.chdir("bin/Debug")
            print("chdir>> ",os.getcwd() )
            names = os.listdir(os.getcwd())
            for name in names:
               if name.endswith('.exe') :
                   os.system(name)
                   print("\n")
                   break
        else:
            print("cppunit target not find ")
            return 0

    def project_clean(self,*args):
        print("\n")
        if True == os.path.exists("projects"):
            shutil.rmtree("projects")
        if True == os.path.exists("target"):
            shutil.rmtree("target")
        if True == os.path.exists("lib"):
            shutil.rmtree("lib")

    def project_install(self,*args ):
        usr_name = getpass.getuser()
        local_lib_path = r"C:\Users\%s"%(usr_name)
        out_path = ""
        version = ""
        lib = ""
        if os.path.exists("pom.xml"):
            pom = ParsePom("pom.xml")
            ret = pom.get_pom_text(["groupId","artifactId","version"])
            version = ret[-1]
            out_path = ".".join(ret[0:-1:]).replace(".","\\")
            lib = "".join(pom.get_pom_text("lib"))
            #print(out_path)
            print(version, lib )
        else:
            print("== err pom.xml not exist ")
            return 

        # print(local_lib_path)
        os.chdir(local_lib_path)
        if os.path.exists(".mavenlib"):
            os.chdir(".mavenlib")
            if False == os.path.exists(out_path):
                os.makedirs(out_path)
            dst_path = local_lib_path + "\\.mavenlib\\"+ out_path
            try:
                shutil.copy(self.root_path+"\lib\Debug\%s.lib"%(lib), dst_path)
                os.chdir(dst_path)
                #os.rename("%s.lib"%(lib), "%s_%s.lib"%(version,lib) )
            finally:
                if os.path.exists("%s_%s.lib"%(version,lib)):
                    os.remove("%s_%s.lib"%(version,lib))
                os.rename("%s.lib"%(lib), "%s_%s.lib"%(version,lib) )
        else:
            os.makedirs(".mavenlib")

if __name__ == "__main__":
    pass