#!/usr/bin/env python3 
# -*- coding:utf-8 -*-
# Author: Lancer  2020-05-08 08:45:33

import  os,re,sys
import  getopt
from    unifwbase   import *
from    cppproject  import *


Usage = '''\

Usage
    cs  create   <projectname like: com.lancer.demo>
    cs  init     =  at project root path  get dependencies .lib or .h file to target project path
    cs  build    =  use cmake tools  build  project file 
    cs  install  =  install .lib or .h to  user local lib manage path
    cs  utest    =  run target .exe  utest
    cs  ftest    =  run target .exe  ftest
    cs  clean    =  delete  project file 
    cs  update   =  update moduel version (now not add this function)
    cs  -h       =  get tools help info [cs --help]
    cs  -v       =  get tools version and last modify time [cs --version]
'''


class  Main(object):
    def __init__(self):
        pass
    def main(self):
        #global global_cmd
        cppobj = CppProject()
        global_cmd["create"]  = cppobj.cppproject_create 
        global_cmd["init"]    = cppobj.cppproject_init
        global_cmd["build"]   = cppobj.cppproject_build
        global_cmd["install"] = cppobj.cppproject_install
        global_cmd["utest"]   = cppobj.cppproject_utest
        global_cmd["ftest"]   = cppobj.cppproject_ftest
        global_cmd["update"]  = cppobj.cppproject_updateversion
        global_cmd["clean"]   = cppobj.cppproject_clean
        
        try:
            apts, msgs = getopt.getopt(sys.argv[1:],shortopts="vhu",longopts = ["help","version"] )
            # print(apts)
            # print(msgs)
            for apt,_ in apts:
                if apt in ("-u"):
                    print("组合命令")
                elif apt in ("-v","--version"):
                    print("\n version: 1.0.0  time:2020-07-20 author:Lancer")
                elif apt in ("-h","--help"):
                    print(Usage)
            if not apts: 
                if msgs:
                    if msgs[0] in global_cmd.keys():
                        global_cmd[msgs[0]](msgs[1::])
                else:
                    print(global_cmd.keys())
                    print("cmd err please read help info : -h  gettools use info ")                      

        except getopt.GetoptError:
            print("cmd err please read help info : -h  gettools use info ")




if __name__ == "__main__":
    test =  Main()
    test.main()
