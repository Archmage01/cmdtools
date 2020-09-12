#!/usr/bin/env python3 
# -*- coding:utf-8 -*-
# Author: Lancer  2020-05-08 08:45:33

import os
import sys
import shutil
import platform


#打包脚本为 
class  Package_tools(object):
    def __init__(self):
        self.rootpath = os.getcwd()
        print(self.rootpath)
        if os.path.exists("bin") == True:
            self.del_file(self.rootpath+"/bin")
        else:
            os.mkdir("bin")

    def create2exe(self):
        if True == os.path.exists("core.py"):
            os.system("pyinstaller -F core.py")
        else:
            print("core.py not exist  please check === ")
            return 
        
        ###window
        if 'Windows' == platform.system():
            print(" Windows package  scripttools ")
            try:
                shutil.copy("dist/core.exe", self.rootpath+"\\bin")
            except IOError as e:
                print("Windows Unable to copy file. %s" % e)
            except:
                print("Windows Unexpected error:", sys.exc_info())
            os.chdir(self.rootpath+"/bin")
            if os.path.exists("core.exe"):  
                os.rename("core.exe", "cs.exe")
            py_script_path = "\\".join(sys.executable.split("\\")[0:-1:]) + "\\Scripts"
            print("python: ",py_script_path )
            try:
                shutil.copy("cs.exe", py_script_path)
            except IOError as e:
                print("Unable to copy file. %s" % e)
        ###Linux
        elif  'Linux' == platform.system():
            print(" Linux  package  scripttools ")
            try:
                shutil.copy("dist/core", self.rootpath+"/bin")
            except IOError as e:
                print("Windows Unable to copy file. %s" % e)
            except:
                print("Windows Unexpected error:", sys.exc_info())
            os.chdir(self.rootpath+"/bin")
            if os.path.exists("core"):  
                os.rename("core", "mycs")
            py_script_path = '/usr/bin'
            print("python: ",py_script_path )
            try:
                shutil.copy("mycs", py_script_path)
            except IOError as e:
                print("Unable to copy file. %s" % e)
        else:
            print("error  unexpect system script is not support ! ")

        #clean  temp build file
        if  True ==   os.path.exists("core.spec"):
            os.remove("core.spec")  
        if  True ==   os.path.exists("dist"):
            shutil.rmtree("dist")
        if  True ==   os.path.exists("build"):
            shutil.rmtree("build")
        


    def del_file(self,filepath):
        """
        删除某一目录下的所有文件或文件夹
        :param filepath: 路径
        :return:
        """
        del_list = os.listdir(filepath)
        for f in del_list:
            file_path = os.path.join(filepath, f)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)


if __name__ == "__main__":
    test = Package_tools()
    test.create2exe()

