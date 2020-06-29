#!/usr/bin/env python3 
# -*- coding:utf-8 -*-
# Author: Lancer  2020-05-08 08:45:33

import os
import sys
import shutil


#打包脚本为 .exe
class  Package_tools(object):
    def __init__(self):
        self.rootpath = os.getcwd()
        print(self.rootpath)
        if os.path.exists("bin") == True:
            self.del_file(self.rootpath+"\\bin")
        else:
            os.mkdir("bin")

    def create2exe(self):
        if True == os.path.exists("project"):
            os.chdir("project")
            if True == os.path.exists("main.py"):
                os.system("pyinstaller -F main.py")
                try:
                    shutil.copy("dist/main.exe", self.rootpath+"\\bin")
                except IOError as e:
                    print("Unable to copy file. %s" % e)
                except:
                    print("Unexpected error:", sys.exc_info())
        #clean  temp build file
        if  True ==   os.path.exists("main.spec"):
            os.remove("main.spec")  
        if  True ==   os.path.exists("dist"):
            shutil.rmtree("dist")
        if  True ==   os.path.exists("build"):
            shutil.rmtree("build")
        os.chdir(self.rootpath+"\\bin")
        if os.path.exists("main.exe"):  
            os.rename("main.exe", "cs.exe")
        py_script_path = "\\".join(sys.executable.split("\\")[0:-1:]) + "\\Scripts"
        print("python: ",py_script_path )
        try:
            shutil.copy("cs.exe", py_script_path)
        except IOError as e:
            print("Unable to copy file. %s" % e)

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

