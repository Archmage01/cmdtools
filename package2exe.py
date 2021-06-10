#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @brief: 打包脚本为 .exe

import os,sys
import shutil


class  Package_tools(object):
    def __init__(self):
        self.rootpath = os.getcwd()
        print(self.rootpath)
        if os.path.exists("bin") == True:
            self.del_file(os.path.join(self.rootpath,'bin') )
        else:
            os.mkdir("bin")
        self.filename = 'cppcompile'

    def create2exe(self):
        if True == os.path.exists("cpptools"):
            os.chdir('cpptools')
            if True == os.path.exists("%s.py"%(self.filename)):
                os.system("pyinstaller -F cppcompile.py")
                try:
                    shutil.copy("dist/%s.exe"%(self.filename),os.path.join(self.rootpath,'bin') )
                except IOError as e:
                    print("Unable to copy file. %s"% e)
                except:
                    print("Unexpected error:", sys.exc_info())
        #clean  temp build file
        if  True ==   os.path.exists("%s.spec"%(self.filename)):
            os.remove("%s.spec"%(self.filename))
        if  True ==   os.path.exists("dist"):
            shutil.rmtree("dist")
        if  True ==   os.path.exists("build"):
            shutil.rmtree("build")
        os.chdir(os.path.join(self.rootpath,'bin'))
        if os.path.exists("%s.exe"%(self.filename)):
            os.rename("%s.exe"%(self.filename), "cmvn.exe")
        py_script_path = "\\".join(sys.executable.split("\\")[0:-1:]) + "\\Scripts"
        print("python: ",py_script_path )
        try:
            shutil.copy("cmvn.exe", py_script_path)
        except IOError as e:
            print("Unable to copy file. %s" % e)

    def del_file(self,filepath):
        """
        删除某一目录下的所有文件或文件夹
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


