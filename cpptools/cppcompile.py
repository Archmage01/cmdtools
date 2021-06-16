#!/usr/bin/env python
# -*- coding:utf-8 -*-


import os,sys,getopt
from   pub  import *
from   cppproject import *
from   armproject import *

__version__ = 'version: 1.0.4 '
__autor__   = 'author : Zero  '
__TIME__    = 'time:2020-06-10'

Usage = \
'''

This tool is modeled on MVN for C/C++ project, need install cmake tools/ Visual Studio/ keil / mingw
usage: cmvn cmds [options] [optioninfo] 

cmds:
    create  projectinfo     projectinfo is Unique identification, for example: com.leetcode.demo
    init                    run at project root path prepare for compile project 
                            to get dependencies moduel files like  .h or .lib
    build                   compile this project, generate executable file or .lib 
    install                 Install the packaged project to the local warehouse for use by other projects
    utest                   Run the tests using the appropriate unit testing framework, such as cppunit
    ftest                   Run the tests in dir ftest, like integration testing
    clean                   Remove all files generated from the last build
    update destversion      destversion is version number to be upgraded, for example: 1.0.0
    deploy                  Copy the final project package to the remote warehouse for sharing with other developers and projects
    generate fileinfo       generate file, tools will analysis fileinfo by rules output template file
    verify                  verify version number consistency 

    arminit                 Generators MinGW Makefiles 
    armbuild                keil  build  project 
    arminstall              Install the packaged project to the local warehouse for use by other projects(arm)
    elf2bin                 from  change .elf to .bin  
options:
    -v, --version           Displays the tool version number and modification time
    -h, --help              Display help information for users to use tools


'''

def  init_cmd_function_pairs():
    cppobject = CppProject('pom.xml')
    global_cmd['init' ]   = cppobject.cppproject_init
    global_cmd['build']   = cppobject.cppproject_build
    global_cmd['install'] = cppobject.cppproject_install
    global_cmd['utest']   = cppobject.cppproject_utest
    global_cmd['ftest']   = cppobject.cppproject_ftest
    global_cmd['clean']   = cppobject.cppproject_clean
    global_cmd['verify']   = cppobject.verify_version_nums


    global_cmd['create']  = create_project
    global_cmd['update']  = cppobject.cppproject_updateversion
    global_cmd['generate']  = cppobject.auto_generate_file
    #交叉编译  arm
    armproject = ArmProject()
    global_cmd['arminit' ]     = armproject.arm_project_init
    global_cmd['armbuild']     = armproject.arm_project_build
    global_cmd['arminstall']   = armproject.arm_project_install
    global_cmd['elf2bin']        = armproject.arm_project_elf2bin


def main():
    #初始化命令和对应函数
    init_cmd_function_pairs()
    try:
        if not global_cmd: return 
        opts, msgs = getopt.getopt(sys.argv[1:], shortopts="vho:i:t:", longopts=["help", "version",'type'])
        for opt, _ in opts:
            if opt in ('-v','--version'):
                print('\n'+'  '+__version__+' '+  __TIME__ + ' ' + __autor__ )
            elif opt in ('-h','--help'):
                print(Usage)
            elif opt in ('-t','type'):
                logging.info(" 预留功能待添加")
            else:
                print(Usage)
        #解析单个命令
        if len(msgs) == 1:
            if msgs[0] in ('init','build','install', 'utest', 'ftest','clean','verify'):
                global_cmd[msgs[0]]()
            elif msgs[0] in ('arminit','armbuild','arminstall','elf2bin'):
                global_cmd[msgs[0]]()
            elif msgs[0] in ('deploy'):
                logging.info(" 预留命令 "+ msgs[0] )
            else:
                logging.error("Please read the user help information: -h or --help")
        elif len(msgs) == 2:
            if msgs[0] == 'create':
                global_cmd[msgs[0]](msgs[1])
            elif msgs[0] == 'update':
                global_cmd[msgs[0]](msgs[1])
            elif msgs[0] == 'generate':
                global_cmd[msgs[0]](msgs[1])
            else:
                logging.error("Please read the user help information: -h or --help")

    except getopt.GetoptError:
        logging.error("Please read the user help information: -h or --help")

if __name__ == '__main__':
    main()

