#!/usr/bin/env python
# -*- coding:utf-8 -*-


import os,sys,getopt
from pub import *
from cppproject import *

Usage = '''\

Usage
    create   <projectname like: com.lancer.demo>
    init     =  at project root path  get dependencies .lib or .h file to target project path
    build    =  use cmake tools  build  project file 
    install  =  install .lib or .h to  user local lib manage path
    utest    =  run target .exe  utest
    ftest    =  run target .exe  ftest
    clean    =  delete  project file 
    update   =  update moduel version (now not add this function)
    -h       =  get tools help info [cs --help]
    -v       =  get tools version and last modify time [cs --version]
'''

class Main(object):
    def __init__(self):
        try:
            apts, msgs = getopt.getopt(sys.argv[1:], shortopts="vh", longopts=["help", "version"])
            # print(apts)
            # print(msgs)
            for apt, _ in apts:
                if apt in ("-v", "--version"):
                    print("\n version: 1.0.1 time:2020-06-20 author:Zero ")
                elif apt in ("-h", "--help"):
                    print(Usage)
            if not apts:
                if msgs:
                    if msgs[0] == 'create':
                        if len(msgs)>1:
                            create_project(msgs[1])
                    elif msgs[0] in ('init','build','install','utest','ftest','clean'):
                        # global global_cmd
                        cppobj = CppProject('pom.xml')
                        global_cmd["init"] = cppobj.cppproject_init
                        global_cmd["build"] = cppobj.cppproject_build
                        global_cmd["install"] = cppobj.cppproject_install
                        global_cmd["utest"] = cppobj.cppproject_utest
                        global_cmd["ftest"] = cppobj.cppproject_ftest
                        global_cmd["update"] = cppobj.cppproject_updateversion
                        global_cmd["clean"] = cppobj.cppproject_clean
                        global_cmd[msgs[0]]()
                else:
                    pass

        except getopt.GetoptError:
            print("cmd err please read help info : -h  gettools use info ")



if __name__ == '__main__':
    test = Main()
